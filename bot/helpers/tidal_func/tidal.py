import re
import json
import aigpy
import base64
import requests

from xml.etree import ElementTree

from bot.helpers.tidal_func.model import *
from bot.helpers.tidal_func.enums import *

# SSL Warnings | retry number
requests.packages.urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5


class TidalAPI(object):
    def __init__(self):
        self.key = LoginKey()
        self.apiKey = {'clientId': '7m7Ap0JC9j1cOM3n',
                       'clientSecret': 'vRAdA108tlvkJpTsGZS8rGZ7xTlbJ0qaZ2K9saEzsgY='}

    def __get__(self, path, params={}, urlpre='https://api.tidalhifi.com/v1/'):
        header = {}
        header = {'authorization': f'Bearer {self.key.accessToken}'}
        params['countryCode'] = self.key.countryCode
        errmsg = "Get operation err!"
        for index in range(0, 3):
            try:
                respond = requests.get(urlpre + path, headers=header, params=params)
                result = json.loads(respond.text)
                if 'status' not in result:
                    return result

                if 'userMessage' in result and result['userMessage'] is not None:
                    errmsg += result['userMessage']
                break
            except Exception as e:
                if index >= 3:
                    errmsg += respond.text

        raise Exception(errmsg)

    def __getItems__(self, path, params={}):
        params['limit'] = 50
        params['offset'] = 0
        total = 0
        ret = []
        while True:
            data = self.__get__(path, params)
            if 'totalNumberOfItems' in data:
                total = data['totalNumberOfItems']
            if total > 0 and total <= len(ret):
                return ret

            ret += data["items"]
            num = len(data["items"])
            if num < 50:
                break
            params['offset'] += num
        return ret


    def __post__(self, path, data, auth=None, urlpre='https://auth.tidal.com/v1/oauth2'):
        for index in range(0, 3):
            try:
                result = requests.post(urlpre+path, data=data, auth=auth, verify=False).json()
                return result
            except Exception as e:
                if index >= 3:
                    raise e

    def getDeviceCode(self) -> str:
        data = {
            'client_id': self.apiKey['clientId'],
            'scope': 'r_usr+w_usr+w_sub'
        }
        result = self.__post__('/device_authorization', data)
        if 'status' in result and result['status'] != 200:
            raise Exception("Device authorization failed. Please choose another apikey.")

        self.key.deviceCode = result['deviceCode']
        self.key.userCode = result['userCode']
        self.key.verificationUrl = result['verificationUri']
        self.key.authCheckTimeout = result['expiresIn']
        self.key.authCheckInterval = result['interval']
        return "http://" + self.key.verificationUrl + "/" + self.key.userCode

    def checkAuthStatus(self) -> bool:
        data = {
            'client_id': self.apiKey['clientId'],
            'device_code': self.key.deviceCode,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'scope': 'r_usr+w_usr+w_sub'
        }
        auth = (self.apiKey['clientId'], self.apiKey['clientSecret'])
        result = self.__post__('/token', data, auth)
        if 'status' in result and result['status'] != 200:
            if result['status'] == 400 and result['sub_status'] == 1002:
                return False
            else:
                raise Exception("Error while checking for authorization. Trying again...")

        # if auth is successful:
        self.key.userId = result['user']['userId']
        self.key.countryCode = result['user']['countryCode']
        self.key.accessToken = result['access_token']
        self.key.refreshToken = result['refresh_token']
        self.key.expiresIn = result['expires_in']
        return True

    def verifyAccessToken(self, accessToken) -> bool:
        header = {'authorization': 'Bearer {}'.format(accessToken)}
        result = requests.get('https://api.tidal.com/v1/sessions', headers=header).json()
        if 'status' in result and result['status'] != 200:
            return False
        return True

    def refreshAccessToken(self, refreshToken) -> bool:
        data = {
            'client_id': self.apiKey['clientId'],
            'refresh_token': refreshToken,
            'grant_type': 'refresh_token',
            'scope': 'r_usr+w_usr+w_sub'
        }
        auth = (self.apiKey['clientId'], self.apiKey['clientSecret'])
        result = self.__post__('/token', data, auth)
        if 'status' in result and result['status'] != 200:
            return False

        # if auth is successful:
        self.key.userId = result['user']['userId']
        self.key.countryCode = result['user']['countryCode']
        self.key.accessToken = result['access_token']
        self.key.expiresIn = result['expires_in']
        return True

    def loginByAccessToken(self, accessToken, userid=None):
        header = {'authorization': 'Bearer {}'.format(accessToken)}
        result = requests.get('https://api.tidal.com/v1/sessions', headers=header).json()
        if 'status' in result and result['status'] != 200:
            raise Exception("Login failed!")

        if not aigpy.string.isNull(userid):
            if str(result['userId']) != str(userid):
                raise Exception("User mismatch! Please use your own accesstoken.",)

        self.key.userId = result['userId']
        self.key.countryCode = result['countryCode']
        self.key.accessToken = accessToken
        return

    def getAlbum(self, id) -> Album:
        return aigpy.model.dictToModel(self.__get__('albums/' + str(id)), Album())

    def getPlaylist(self, id) -> Playlist:
        return aigpy.model.dictToModel(self.__get__('playlists/' + str(id)), Playlist())

    def getArtist(self, id) -> Artist:
        return aigpy.model.dictToModel(self.__get__('artists/' + str(id)), Artist())

    def getTrack(self, id) -> Track:
        return aigpy.model.dictToModel(self.__get__('tracks/' + str(id)), Track())

    def getMix(self, id) -> Mix:
        mix = Mix()
        mix.id = id
        mix.tracks, mix.videos = self.getItems(id, Type.Mix)
        return None, mix

    def getTypeData(self, id, type: Type):
        if type == Type.Album:
            return self.getAlbum(id)
        if type == Type.Artist:
            return self.getArtist(id)
        if type == Type.Track:
            return self.getTrack(id)
        if type == Type.Video:
            return self.getVideo(id)
        if type == Type.Playlist:
            return self.getPlaylist(id)
        if type == Type.Mix:
            return self.getMix(id)
        return None

    def search(self, text: str, type: Type, offset: int = 0, limit: int = 10) -> SearchResult:
        typeStr = type.name.upper() + "S"
        if type == Type.Null:
            typeStr = "ARTISTS,ALBUMS,TRACKS,VIDEOS,PLAYLISTS"

        params = {"query": text,
                  "offset": offset,
                  "limit": limit,
                  "types": typeStr}
        return aigpy.model.dictToModel(self.__get__('search', params=params), SearchResult())

    def getSearchResultItems(self, result: SearchResult, type: Type):
        if type == Type.Track:
            return result.tracks.items
        if type == Type.Video:
            return result.videos.items
        if type == Type.Album:
            return result.albums.items
        if type == Type.Artist:
            return result.artists.items
        if type == Type.Playlist:
            return result.playlists.items
        return []

    def getLyrics(self, id) -> Lyrics:
        data = self.__get__(f'tracks/{str(id)}/lyrics', urlpre='https://listen.tidal.com/v1/')
        return aigpy.model.dictToModel(data, Lyrics())

    def getItems(self, id, type: Type):
        if type == Type.Playlist:
            data = self.__getItems__('playlists/' + str(id) + "/items")
        elif type == Type.Album:
            data = self.__getItems__('albums/' + str(id) + "/items")
        elif type == Type.Mix:
            data = self.__getItems__('mixes/' + str(id) + '/items')
        else:
            raise Exception("invalid Type!")

        tracks = []
        videos = []
        for item in data:
            if item['type'] == 'track':
                tracks.append(aigpy.model.dictToModel(item['item'], Track()))
            else:
                videos.append(aigpy.model.dictToModel(item['item'], Video()))
        return tracks, videos

    def getArtistAlbums(self, id, includeEP=False):
        data = self.__getItems__(f'artists/{str(id)}/albums')
        albums = list(aigpy.model.dictToModel(item, Album()) for item in data)
        if not includeEP:
            return albums

        data = self.__getItems__(f'artists/{str(id)}/albums', {"filter": "EPSANDSINGLES"})
        albums += list(aigpy.model.dictToModel(item, Album()) for item in data)
        return albums

    def getStreamUrl(self, id, quality: AudioQuality):
        squality = "HI_RES"
        if quality == AudioQuality.Normal:
            squality = "LOW"
        elif quality == AudioQuality.High:
            squality = "HIGH"
        elif quality == AudioQuality.HiFi:
            squality = "LOSSLESS"
        elif quality == AudioQuality.Max:
            squality = "HI_RES_LOSSLESS"

        paras = {"audioquality": squality, "playbackmode": "STREAM", "assetpresentation": "FULL", "prefetch": "false"}
        data = self.__get__(f'tracks/{str(id)}/playbackinfopostpaywall/v4', paras)
        resp = aigpy.model.dictToModel(data, StreamRespond())

        if "vnd.tidal.bt" in resp.manifestMimeType:
            manifest = json.loads(base64.b64decode(resp.manifest).decode('utf-8'))
            ret = StreamUrl()
            ret.trackid = resp.trackid
            ret.soundQuality = resp.audioQuality
            ret.codec = manifest['codecs']
            ret.encryptionKey = manifest['keyId'] if 'keyId' in manifest else ""
            ret.url = manifest['urls'][0]
            ret.urls = [ret.url]
            return ret
        elif "dash+xml" in resp.manifestMimeType:
            xmldata = base64.b64decode(resp.manifest).decode('utf-8')
            ret = StreamUrl()
            ret.trackid = resp.trackid
            ret.soundQuality = resp.audioQuality
            ret.codec = aigpy.string.getSub(xmldata, 'codecs="', '"')
            ret.encryptionKey = ""  # manifest['keyId'] if 'keyId' in manifest else ""
            ret.urls = self.parse_mpd(xmldata)[0]
            if len(ret.urls) > 0:
                ret.url = ret.urls[0]
            return ret

        raise Exception("Can't get the streamUrl, type is " + resp.manifestMimeType)


    def getTrackContributors(self, id):
        return self.__get__(f'tracks/{str(id)}/contributors')

    def getCoverUrl(self, sid, width="320", height="320"):
        return f"https://resources.tidal.com/images/{sid.replace('-', '/')}/{width}x{height}.jpg"

    def getCoverData(self, sid, width="320", height="320"):
        url = self.getCoverUrl(sid, width, height)
        try:
            return requests.get(url).content
        except:
            return ''

    def getArtistsName(self, artists=[]):
        array = list(item.name for item in artists)
        return ", ".join(array)

    def getFlag(self, data, type: Type, short=True, separator=" / "):
        master = False
        atmos = False
        explicit = False
        if type == Type.Album or type == Type.Track:
            if data.audioQuality == "HI_RES":
                master = True
            if type == Type.Album and "DOLBY_ATMOS" in data.audioModes:
                atmos = True
            if data.explicit is True:
                explicit = True
        if type == Type.Video:
            if data.explicit is True:
                explicit = True
        if not master and not atmos and not explicit:
            return ""
        array = []
        if master:
            array.append("M" if short else "Master")
        if atmos:
            array.append("A" if short else "Dolby Atmos")
        if explicit:
            array.append("E" if short else "Explicit")
        return separator.join(array)

    def parseUrl(self, url):
        if "tidal.com" not in url:
            return Type.Null, url

        url = url.lower()
        for index, item in enumerate(Type):
            if item.name.lower() in url:
                etype = item
                return etype, aigpy.string.getSub(url, etype.name.lower() + '/', '/')
        return Type.Null, url

    def getByString(self, string):
        if aigpy.string.isNull(string):
            raise Exception("Please enter something.")

        obj = None
        etype, sid = self.parseUrl(string)
        for index, item in enumerate(Type):
            if etype != Type.Null and etype != item:
                continue
            if item == Type.Null:
                continue
            try:
                obj = self.getTypeData(sid, item)
                return item, obj
            except:
                continue

        raise Exception("No result.")

    
    # from https://github.com/Dniel97/orpheusdl-tidal/blob/master/interface.py#L582
    def parse_mpd(self, xml: bytes) -> list:
        # Removes default namespace definition, don't do that!
        xml = re.sub(r'xmlns="[^"]+"', '', xml, count=1)
        root = ElementTree.fromstring(xml)

        # List of AudioTracks
        tracks = []

        for period in root.findall('Period'):
            for adaptation_set in period.findall('AdaptationSet'):
                for rep in adaptation_set.findall('Representation'):
                    # Check if representation is audio
                    content_type = adaptation_set.get('contentType')
                    if content_type != 'audio':
                        raise ValueError('Only supports audio MPDs!')

                    # Codec checks
                    codec = rep.get('codecs').upper()
                    if codec.startswith('MP4A'):
                        codec = 'AAC'

                    # Segment template
                    seg_template = rep.find('SegmentTemplate')
                    # Add init file to track_urls
                    track_urls = [seg_template.get('initialization')]
                    start_number = int(seg_template.get('startNumber') or 1)

                    # https://dashif-documents.azurewebsites.net/Guidelines-TimingModel/master/Guidelines-TimingModel.html#addressing-explicit
                    # Also see example 9
                    seg_timeline = seg_template.find('SegmentTimeline')
                    if seg_timeline is not None:
                        seg_time_list = []
                        cur_time = 0

                        for s in seg_timeline.findall('S'):
                            # Media segments start time
                            if s.get('t'):
                                cur_time = int(s.get('t'))

                            # Segment reference
                            for i in range((int(s.get('r') or 0) + 1)):
                                seg_time_list.append(cur_time)
                                # Add duration to current time
                                cur_time += int(s.get('d'))

                        # Create list with $Number$ indices
                        seg_num_list = list(range(start_number, len(seg_time_list) + start_number))
                        # Replace $Number$ with all the seg_num_list indices
                        track_urls += [seg_template.get('media').replace('$Number$', str(n)) for n in seg_num_list]

                    tracks.append(track_urls)
        return tracks


# Singleton
TIDAL_API = TidalAPI()
