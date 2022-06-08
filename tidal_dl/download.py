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

from time import sleep
import logging
import os

from bot import Config
from bot.helpers.translations import lang
from bot.helpers.utils.media_search import check_file_exist_db, check_post_tg

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import aigpy
from config import LOGGER
import tidal_dl
from tidal_dl.enums import Type
from tidal_dl.model import Mix
from tidal_dl.printf import Printf
from tidal_dl.util import downloadTrack, downloadVideo, getAlbumPath, API

def __loadAPI__(user):
    API.key.accessToken = user.accessToken
    API.key.userId = user.userid
    API.key.countryCode = user.countryCode

async def __downloadCover__(conf, album, reply_to_id=None):
    if album == None:
        return
    if reply_to_id:
        path = Config.DOWNLOAD_BASE_DIR + f"/thumb/{reply_to_id}.jpg"
    else:
        path = await getAlbumPath(conf, album) + '/cover.jpg'
    url = API.getCoverUrl(album.cover, "80", "80")
    logging.info(f"Downloading cover: {url}")
    if url is not None:
        aigpy.net.downloadFile(url, path)

async def post_album_details(album, bot, chat_id, reply_to_id):
    album_art_path = Config.DOWNLOAD_BASE_DIR + f"/thumb/{reply_to_id}-ALBUM.jpg"
    album_art = API.getCoverUrl(album.cover, "1280", "1280")
    if album_art is not None:
        aigpy.net.downloadFile(album_art, album_art_path)
        photo = await bot.send_photo(
            chat_id=chat_id,
            photo=album_art_path,
            caption=lang.ALBUM_DETAILS.format(
                album.title,
                album.artist.name,
                album.releaseDate,
                album.numberOfTracks,
                album.duration,
                album.numberOfVolumes
            ),
            reply_to_message_id=reply_to_id
        )
        if Config.ALLOW_DUMP:
            await photo.copy(
                chat_id=Config.LOG_CHANNEL_ID,
            )
        os.remove(album_art_path)

async def __saveAlbumInfo__(conf, album, tracks):
    if album == None:
        return
    path = await getAlbumPath(conf, album) + '/AlbumInfo.txt'

    infos = ""
    infos += "[ID]          %s\n" % (str(album.id))
    infos += "[Title]       %s\n" % (str(album.title))
    infos += "[Artists]     %s\n" % (str(album.artist.name))
    infos += "[ReleaseDate] %s\n" % (str(album.releaseDate))
    infos += "[SongNum]     %s\n" % (str(album.numberOfTracks))
    infos += "[Duration]    %s\n" % (str(album.duration))
    infos += '\n'

    i = 0
    while True:
        if i >= int(album.numberOfVolumes):
            break
        i = i + 1
        infos += "===========CD %d=============\n" % i
        for item in tracks:
            if item.volumeNumber != i:
                continue
            infos += '{:<8}'.format("[%d]" % item.trackNumber)
            infos += "%s\n" % item.title
    aigpy.file.write(path, infos, "w+")


async def __album__(conf, obj, bot, chat_id, reply_to_id):
    msg, tracks, videos = API.getItems(obj.id, Type.Album)
    if not aigpy.string.isNull(msg):
        return
    if conf.saveAlbumInfo:
        await __saveAlbumInfo__(conf, obj, tracks)
    await post_album_details(obj, bot, chat_id, reply_to_id)
    for item in tracks:
        if conf.saveCovers:
            await __downloadCover__(conf, obj, reply_to_id)
        await downloadTrack(item, obj, bot=bot, chat_id=chat_id, reply_to_id=reply_to_id)
        sleep(1)
    """for item in videos:
        downloadVideo(item, obj)"""


async def __track__(conf, obj, bot, chat_id, reply_to_id):
    msg, album = API.getAlbum(obj.album.id)
    if conf.saveCovers:
        await __downloadCover__(conf, album, reply_to_id)
    await downloadTrack(obj, album, bot=bot, chat_id=chat_id, reply_to_id=reply_to_id)


async def __video__(conf, obj, bot, chat_id, reply_to_id):
    downloadVideo(obj, obj.album)


async def __artist__(conf, obj, bot, chat_id, reply_to_id):
    msg, albums = API.getArtistAlbums(obj.id, conf.includeEP)
    #Printf.artist(obj, len(albums))
    if not aigpy.string.isNull(msg):
        return
    for item in albums:
        await __album__(conf, item)


async def __playlist__(conf, obj, bot, chat_id, reply_to_id):
    msg, tracks, videos = API.getItems(obj.uuid, Type.Playlist)
    if not aigpy.string.isNull(msg):
        return

    for index, item in enumerate(tracks):
        mag, album = API.getAlbum(item.album.id)
        item.trackNumberOnPlaylist = index + 1
        await downloadTrack(item, album, obj, bot=bot, chat_id=chat_id, reply_to_id=reply_to_id)
        if conf.saveCovers and not conf.usePlaylistFolder:
            await __downloadCover__(conf, album, reply_to_id)

        

async def __mix__(conf, obj: Mix, bot, chat_id, reply_to_id):
    for index, item in enumerate(obj.tracks):
        mag, album = API.getAlbum(item.album.id)
        item.trackNumberOnPlaylist = index + 1
        await downloadTrack(item, album, bot=bot, chat_id=chat_id, reply_to_id=reply_to_id)
        if conf.saveCovers and not conf.usePlaylistFolder:
            await __downloadCover__(conf, album, reply_to_id)

async def file(user, conf, string):
    txt = aigpy.file.getContent(string)
    if aigpy.string.isNull(txt):
        return
    array = txt.split('\n')
    for item in array:
        if aigpy.string.isNull(item):
            continue
        if item[0] == '#':
            continue
        if item[0] == '[':
            continue
        await start(user, conf, item)


async def start(user, conf, string, bot=None, chat_id=None, reply_to_id=None):
    __loadAPI__(user)
    if aigpy.string.isNull(string):
        return

    is_authed = tidal_dl.checkLogin()
    if not is_authed:
        return await bot.send_message(
            chat_id=chat_id,
            text=lang.AUTH_DISABLED,
            reply_to_message_id=reply_to_id
        )
    strings = string.split(" ")
    for item in strings:
        if aigpy.string.isNull(item):
            continue
        if os.path.exists(item):
            file(user, conf, item)
            return

        msg, etype, obj = API.getByString(item)
        if etype == Type.Null or not aigpy.string.isNull(msg):
            Printf.err(msg + " [" + item + "]")
            return

        if Config.SEARCH_CHANNEL:
            try:
                if Type.Album or Type.Playlist or Type.Mix:
                    msg_link = await check_post_tg(obj.title)
                else:
                    msg_link = await check_file_exist_db(obj.title, True)
                if msg_link:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=lang.FILE_EXIST.format(obj.title),
                        reply_to_message_id=reply_to_id,
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton(text="GET FILE", url=msg_link)]
                            ])
                    )
                    LOGGER.info(obj.title + " already exist")
                    return
            except Exception as e:
                LOGGER.warning(e)

        if etype == Type.Album:
            await __album__(conf, obj, bot, chat_id, reply_to_id)
        if etype == Type.Track:
            await __track__(conf, obj, bot, chat_id, reply_to_id)
        if etype == Type.Video:
            await __video__(conf, obj, bot, chat_id, reply_to_id)
        if etype == Type.Artist:
            await __artist__(conf, obj, bot, chat_id, reply_to_id)
        if etype == Type.Playlist:
            await __playlist__(conf, obj, bot, chat_id, reply_to_id)
        if etype == Type.Mix:
            await __mix__(conf, obj, bot, chat_id, reply_to_id)
