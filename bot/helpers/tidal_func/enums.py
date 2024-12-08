from enum import Enum


class AudioQuality(Enum):
    Normal = 0
    High = 1
    HiFi = 2
    Master = 3
    Max = 4


class Type(Enum):
    Album = 0
    Track = 1
    Video = 2
    Playlist = 3
    Artist = 4
    Mix = 5
    Null = 6
