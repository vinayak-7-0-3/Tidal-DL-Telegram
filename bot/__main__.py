import os
import asyncio
import warnings

from pyrogram import idle

from bot import Config, USER, LOGGER, BOT
from bot.helpers.utils.auth_check import get_chats
from bot.helpers.tidal_func.events import checkAPI
from bot.helpers.utils.file_dumping import dump_from_queue
from bot.helpers.tidal_func.settings import SETTINGS, TOKEN

plugins = dict(
    root="bot/modules"
)

async def start():
    LOGGER.info('Loading Tidal DL Configs........')
    SETTINGS.read("./.tidal-dl.json")
    TOKEN.read("./tidal-dl.token.json")
    await checkAPI()
    if Config.USER_SESSION is not None and Config.USER_SESSION != "":
        await USER.start()
    LOGGER.info("Bot Started...... Now Enjoy")
    await get_chats()
    await BOT.start()
    await idle()

def stop():
    if Config.USER_SESSION is not None and Config.USER_SESSION != "":
        LOGGER.info('Exiting User........')
        USER.stop()
    LOGGER.info('Bot and User Exited Successfully ! Bye..........')
    BOT.stop()

if __name__ == "__main__":
    if not os.path.isdir(Config.DOWNLOAD_BASE_DIR):
        os.makedirs(Config.DOWNLOAD_BASE_DIR)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)

        loop = asyncio.get_event_loop()
        
        if Config.ALLOW_DUMP == "True":
            LOGGER.info("QUEUE MODE TURNED ON")
            dump = asyncio.ensure_future(dump_from_queue())
        try:
            loop.run_until_complete(start())
        finally:
            try:
                dump.cancel()
            except:
                pass
            stop()
            loop.close()
            
        
    



