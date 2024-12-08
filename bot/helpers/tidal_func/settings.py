import json
import aigpy
import base64

from bot.helpers.tidal_func.enums import *

from bot.helpers.database.postgres_impl import set_db


class Settings(aigpy.model.ModelBase):
    checkExist = False
    includeEP = True
    saveCovers = True
    language = 0
    lyricFile = False
    apiKeyIndex = 4
    showProgress = False
    showTrackInfo = True
    saveAlbumInfo = False

    downloadPath = "./bot/DOWNLOADS/"
    audioQuality = AudioQuality.Master
    usePlaylistFolder = True
    albumFolderFormat = R"{ArtistName}/{Flag} {AlbumTitle} [{AlbumID}] [{AlbumYear}]"
    trackFileFormat = R"{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"
    videoFileFormat = R"{VideoNumber} - {ArtistName} - {VideoTitle}{ExplicitFlag}"

    def getDefaultPathFormat(self, type: Type):
        if type == Type.Album:
            return R"{ArtistName}/{Flag} {AlbumTitle} [{AlbumID}] [{AlbumYear}]"
        elif type == Type.Track:
            return R"{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"
        elif type == Type.Video:
            return R"{VideoNumber} - {ArtistName} - {VideoTitle}{ExplicitFlag}"
        return ""

    def getAudioQuality(self, value):
        for item in AudioQuality:
            if item.name == value:
                return item
        return AudioQuality.Normal

    def getVideoQuality(self, value):
        for item in VideoQuality:
            if item.name == value:
                return item
        return VideoQuality.P360
    
    def read(self, path):
        self._path_ = path
        txt = aigpy.file.getContent(self._path_)
        if len(txt) > 0:
            data = json.loads(txt)
            if aigpy.model.dictToModel(data, self) is None:
                return

        self.audioQuality = self.getAudioQuality(self.audioQuality)

        if self.albumFolderFormat is None:
            self.albumFolderFormat = self.getDefaultPathFormat(Type.Album)
        if self.trackFileFormat is None:
            self.trackFileFormat = self.getDefaultPathFormat(Type.Track)
        if self.videoFileFormat is None:
            self.videoFileFormat = self.getDefaultPathFormat(Type.Video)
        if self.apiKeyIndex is None:
            self.apiKeyIndex = 0

        api_index, _ = set_db.get_variable("API_KEY_INDEX")
        if api_index:
            self.apiKeyIndex = int(api_index)

    def save(self):
        data = aigpy.model.modelToDict(self)
        data['audioQuality'] = self.audioQuality.name
        data['videoQuality'] = self.videoQuality.name
        txt = json.dumps(data)
        aigpy.file.write(self._path_, txt, 'w+')



class TokenSettings(aigpy.model.ModelBase):
    userid = None
    countryCode = None
    accessToken = None
    refreshToken = None
    expiresAfter = 0

    def __encode__(self, string):
        sw = bytes(string, 'utf-8')
        st = base64.b64encode(sw)
        return st

    def __decode__(self, string):
        try:
            sr = base64.b64decode(string)
            st = sr.decode()
            return st
        except:
            return string

    def read(self, path):
        self._path_ = path
        txt = aigpy.file.getContent(self._path_)
        if txt == "" or txt is None:
            _, txt = set_db.get_variable("AUTH_TOKEN")
        try:
            if len(txt) > 0:
                data = json.loads(self.__decode__(txt))
                aigpy.model.dictToModel(data, self)
        except TypeError:
            set_db.set_variable("AUTH_DONE", False, False, None)

    def save(self):
        data = aigpy.model.modelToDict(self)
        txt = json.dumps(data)
        set_db.set_variable("AUTH_TOKEN", 0, True, self.__encode__(txt))
        aigpy.file.write(self._path_, self.__encode__(txt), 'wb')


SETTINGS = Settings()
TOKEN = TokenSettings()
