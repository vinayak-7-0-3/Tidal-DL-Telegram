import aiohttp
from bot import Config, LOGGER
from bot.helpers.translations import lang
from bot.helpers.database.postgres_impl import TidalSettings

set_db = TidalSettings()

listen_tidal = "CzET4vdadNUFQ5JU"

async def search_track(query):
    title = []
    artist = []
    url = []
    msg = []
    thumb = []

    http_sess = aiohttp.ClientSession()

    token, _ = set_db.get_variable("TIDAL_SEARCH_TOKEN")
    if not token:
        token = listen_tidal
    
    resp = await http_sess.get(
        "https://listen.tidal.com/v1/search",
        params={
            "types": "TRACKS", 
            "includeContributors": "true", 
            "countryCode": Config.TIDAL_REGION, 
            "limit": Config.TIDAL_SEARCH_LIMIT, 
            "query": query
        },
        headers={
            "x-tidal-token": token
        }
        
    )
    for result in (await resp.json())['tracks']['items']:
        #print(result)
        title.append(result['title'])
        artist.append(result['artists'][0]['name'])
        url.append(result['url'])
        if result['album']['cover'] is not None:
            thumb_photo = f"https://resources.tidal.com/images/{result['album']['cover'].replace('-', '/')}/80x80.jpg"
            thumb.append(thumb_photo)
        else:
            thumb.append(None)

        text = lang.select.INPUT_MESSAGE_TRACK.format(
            result['title'],
            result['artists'][0]['name'],
            result['album']['title'],
            round(int(result['duration'])/60, 2)
        )
        msg.append(text)

    await http_sess.close()
    return msg, title, artist, url, thumb

async def search_album(query):
    title = []
    artist = []
    url = []
    msg = []
    thumb = []

    http_sess = aiohttp.ClientSession()

    token, _ = set_db.get_variable("TIDAL_SEARCH_TOKEN")
    if not token:
        token = listen_tidal

    resp = await http_sess.get(
        "https://listen.tidal.com/v1/search",
        params={
          "types": "ALBUMS", 
          "includeContributors": "true", 
          "countryCode": Config.TIDAL_REGION,
          "limit": Config.TIDAL_SEARCH_LIMIT,
          "query": query
        },
        headers={
            "x-tidal-token": token
        }
    )
    resp = (await resp.json())['albums']['items']
    for result in resp:
        title.append(result['title'])
        artist.append(result['artists'][0]['name'])
        url.append(result['url'])

        if result['cover'] is not None:
            thumb_photo = f"https://resources.tidal.com/images/{result['cover'].replace('-', '/')}/80x80.jpg"
            thumb.append(thumb_photo)
        else:
            thumb.append(None)

        text = lang.select.INPUT_MESSAGE_ALBUM.format(
            result['title'],
            result['artists'][0]['name'],
            result['numberOfTracks'],
            result['releaseDate']
        )
        msg.append(text)
        
    
    await http_sess.close()
    return msg, title, artist, url, thumb

async def start_api():
    LOGGER.info("Initiating Tidal Search API")
    """http_sess = aiohttp.ClientSession()
    resp = await http_sess.get("https://listen.tidal.com/")
    data = await resp.text()
    print("\n\n\n\n"+data)
    resp = await http_sess.get(f"https://listen.tidal.com" + re.search(r'<script defer="defer" src=\"(/app.+?.js)\">', data)[1])
    data = await resp.text()
    token = re.search(r":\"(.{16})\":[a-z]+\(\)?", data)[1]
    set_db.set_variable("TIDAL_SEARCH_TOKEN", token)
    await http_sess.close()"""
    LOGGER.info("Tidal Search API initiated")