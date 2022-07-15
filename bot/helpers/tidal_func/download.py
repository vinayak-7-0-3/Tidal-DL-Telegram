#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   download.py
@Time    :   2020/11/08
@Author  :   Yaronzz
@Version :   1.0
@Contact :   yaronhuang@foxmail.com
@Desc    :   
'''
import os
import aigpy

from bot import LOGGER
from config import Config
from bot.helpers.translations import lang
from bot.helpers.utils.media_search import check_duplicate
from bot.helpers.database.postgres_impl import music_db, user_settings

from bot.helpers.tidal_func.paths import *
from bot.helpers.tidal_func.tidal import *
from bot.helpers.tidal_func.decryption import *
from bot.helpers.tidal_func.settings import SETTINGS


def __isSkip__(finalpath, url):
    if not SETTINGS.checkExist:
        return False
    curSize = aigpy.file.getSize(finalpath)
    if curSize <= 0:
        return False
    netSize = aigpy.net.getSize(url)
    return curSize >= netSize


def __encrypted__(stream, srcPath, descPath):
    if aigpy.string.isNull(stream.encryptionKey):
        os.replace(srcPath, descPath)
    else:
        key, nonce = decrypt_security_token(stream.encryptionKey)
        decrypt_file(srcPath, descPath, key, nonce)
        os.remove(srcPath)


def __parseContributors__(roleType, Contributors):
    if Contributors is None:
        return None
    try:
        ret = []
        for item in Contributors['items']:
            if item['role'] == roleType:
                ret.append(item['name'])
        return ret
    except:
        return None


def __setMetaData__(track: Track, album: Album, filepath, contributors, lyrics):
    obj = aigpy.tag.TagTool(filepath)
    obj.album = track.album.title
    obj.title = track.title
    if not aigpy.string.isNull(track.version):
        obj.title += ' (' + track.version + ')'

    obj.artist = list(map(lambda artist: artist.name, track.artists))
    obj.copyright = track.copyRight
    obj.tracknumber = track.trackNumber
    obj.discnumber = track.volumeNumber
    obj.composer = __parseContributors__('Composer', contributors)
    obj.isrc = track.isrc

    obj.albumartist = list(map(lambda artist: artist.name, album.artists))
    obj.date = album.releaseDate
    obj.totaldisc = album.numberOfVolumes
    obj.lyrics = lyrics
    if obj.totaldisc <= 1:
        obj.totaltrack = album.numberOfTracks
    coverpath = TIDAL_API.getCoverUrl(album.cover, "1280", "1280")
    obj.save(coverpath)

async def downloadThumb(album, r_id):
    path = Config.DOWNLOAD_BASE_DIR + f"/thumb/{r_id}.jpg"
    url = TIDAL_API.getCoverUrl(album.cover, "80", "80")
    try:
        aigpy.net.downloadFile(url, path)
    except:
        LOGGER.warning(f"Download Cover Failed For The Album : {album.title}")
    return path

async def postCover(album, bot, c_id, r_id):
    album_art_path = Config.DOWNLOAD_BASE_DIR + f"/thumb/{r_id}-ALBUM.jpg"
    album_art = TIDAL_API.getCoverUrl(album.cover, "1280", "1280")
    if album_art is not None:
        aigpy.net.downloadFile(album_art, album_art_path)
        photo = await bot.send_photo(
            chat_id=c_id,
            photo=album_art_path,
            caption=lang.select.ALBUM_DETAILS.format(
                album.title,
                album.artist.name,
                album.releaseDate,
                album.numberOfTracks,
                album.duration,
                album.numberOfVolumes
            ),
            reply_to_message_id=r_id
        )
        if Config.ALLOW_DUMP=="True":
            copy = await photo.copy(
                chat_id=Config.LOG_CHANNEL_ID,
            )
            music_db.set_music(copy.id, album.title, album.artist.name, album.id, "album")
        os.remove(album_art_path)



def downloadAlbumInfo(album, tracks):
    if album is None:
        return
    
    path = getAlbumPath(album)
    aigpy.path.mkdirs(path)
    
    path += '/AlbumInfo.txt'
    infos = ""
    infos += "[ID]          %s\n" % (str(album.id))
    infos += "[Title]       %s\n" % (str(album.title))
    infos += "[Artists]     %s\n" % (TIDAL_API.getArtistsName(album.artists))
    infos += "[ReleaseDate] %s\n" % (str(album.releaseDate))
    infos += "[SongNum]     %s\n" % (str(album.numberOfTracks))
    infos += "[Duration]    %s\n" % (str(album.duration))
    infos += '\n'

    for index in range(0, album.numberOfVolumes):
        volumeNumber = index + 1
        infos += f"===========CD {volumeNumber}=============\n"
        for item in tracks:
            if item.volumeNumber != volumeNumber:
                continue
            infos += '{:<8}'.format("[%d]" % item.trackNumber)
            infos += "%s\n" % item.title
    aigpy.file.write(path, infos, "w+")

async def downloadTrack(track: Track, album=None, playlist=None, userProgress=None, partSize=1048576, \
    bot=None, c_id=None, r_id=None, u_id=None):
    try:
        if Config.SEARCH_CHANNEL or Config.LOG_CHANNEL_ID:
            check = await check_duplicate(track.title, track.artist.name, track.id, bot, c_id, r_id, Type.Track)
            if check:
                return
        quality = user_settings.get_var(u_id, "QUALITY")
        if quality:
            quality = SETTINGS.getAudioQuality(quality)
        else:
            quality = SETTINGS.audioQuality

        stream = TIDAL_API.getStreamUrl(track.id, quality)
        path = getTrackPath(track, stream, album, playlist)

        # download
        #logging.info("[DL Track] name=" + aigpy.path.getFileName(path) + "\nurl=" + stream.url)

        tool = aigpy.download.DownloadTool(path + '.part', [stream.url])
        tool.setUserProgress(userProgress)
        tool.setPartSize(partSize)
        check, err = tool.start(SETTINGS.showProgress)
        if not check:
            LOGGER.warning(f"DL Track[{track.title}] failed.{str(err)}")
            return False, str(err)

        # encrypted -> decrypt and remove encrypted file
        __encrypted__(stream, path + '.part', path)

        # contributors
        try:
            contributors = TIDAL_API.getTrackContributors(track.id)
        except:
            contributors = None

        # lyrics
        try:
            lyrics = TIDAL_API.getLyrics(track.id).subtitles
            if SETTINGS.lyricFile:
                lrcPath = path.rsplit(".", 1)[0] + '.lrc'
                aigpy.fileHelper.write(lrcPath, lyrics, 'w')
        except:
            lyrics = ''

        __setMetaData__(track, album, path, contributors, lyrics)

        thumb = await downloadThumb(album, r_id)

        media_file = await bot.send_audio(
            chat_id=c_id,
            audio=path,
            duration=track.duration,
            performer=TIDAL_API.getArtistsName(track.artists),
            title=track.title,
            thumb=thumb,
            reply_to_message_id=r_id
        )
        if Config.ALLOW_DUMP=="True":
            copy = await media_file.copy(
                chat_id=Config.LOG_CHANNEL_ID,
            )
            music_db.set_music(copy.id, track.title, track.artist.name, track.id, "track")

        # Remove the files after uploading
        os.remove(thumb)
        os.remove(path)

        LOGGER.info("Succesfully Downloaded " + track.title)
        return True, ''
    except Exception as e:
        LOGGER.warning(f"DL Track[{track.title}] failed.{str(e)}")
        return False, str(e)

async def downloadTracks(tracks, album: Album = None, playlist : Playlist=None, \
    bot=None, c_id=None, r_id=None, u_id=None):
    def __getAlbum__(item: Track):
        album = TIDAL_API.getAlbum(item.album.id)
        return album
    
    for index, item in enumerate(tracks):
        itemAlbum = album
        if itemAlbum is None:
            itemAlbum = __getAlbum__(item)
            item.trackNumberOnPlaylist = index + 1
        await downloadTrack(item, itemAlbum, playlist, bot=bot, c_id=c_id, r_id=r_id, u_id=u_id)
