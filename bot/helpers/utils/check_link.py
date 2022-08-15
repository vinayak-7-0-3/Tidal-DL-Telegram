import requests
from urllib import parse

songs_api = 'https://api.song.link/v1-alpha.1/links?url='

tidal = ["https://tidal.com", "https://listen.tidal.com", "tidal.com", "listen.tidal.com"]

async def check_link(link):
    if link.startswith(tuple(tidal)):
        return link
    else:
        try:
            result = requests.get(songs_api + parse.quote(link))
            if result.status_code == 200:
                link = result.json()['linksByPlatform']['tidal']['url']
                return link
            else:
                return False
        except:
            return False