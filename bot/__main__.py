import os
from pyrogram import Client
from bot import Config, USER, LOGGER
from bot.helpers.utils.auth_check import get_chats
from bot.helpers.tidal_func.events import checkAPI
from bot.helpers.tidal_func.settings import SETTINGS, TOKEN

plugins = dict(
    root="bot/modules"
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            "TidalDLBot",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.TG_BOT_TOKEN,
            plugins=plugins,
            workdir=Config.WORK_DIR
        )

    async def start(self):
        await super().start()
        LOGGER.info('Loading Tidal DL Configs........')
        SETTINGS.read("./.tidal-dl.json")
        TOKEN.read("./tidal-dl.token.json")
        await checkAPI()
        if Config.USER_SESSION is not None and Config.USER_SESSION != "":
            await USER.start()
        LOGGER.info("Bot Started...... Now Enjoy")
        await get_chats()

    async def stop(self, *args):
        await super().stop()
        LOGGER.info('Exiting User........')
        if Config.USER_SESSION is not None:
            await USER.stop()
        LOGGER.info('Bot and User Exited Successfully ! Bye..........')

if __name__ == "__main__":
    if not os.path.isdir(Config.DOWNLOAD_BASE_DIR):
        os.makedirs(Config.DOWNLOAD_BASE_DIR)
    app = Bot()
    app.run()
