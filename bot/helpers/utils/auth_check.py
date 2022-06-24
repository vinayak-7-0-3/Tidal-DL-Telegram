from bot import Config
from bot.helpers.database.postgres_impl import users_db, admins_db, chats_db

allowed_chats = []
allowed_users = []
admins = []

# NOOB WAY TO HANDLE BOTH ENV AND DB XD

async def get_chats(return_msg=False):
    # CHATS 
    database_chats = chats_db.get_chats()
    for chat in Config.AUTH_CHAT:
        if chat not in allowed_chats:
            allowed_chats.append(chat)
    for chat in database_chats:
        if chat != None:
            if chat[0] not in allowed_chats and chat[0] != None:
                allowed_chats.append(chat[0])
    # ADMINS
    database_admins = admins_db.get_admins()
    for admin in Config.ADMINS:
        if admin not in admins:
            admins.append(admin)
    for admin in database_admins:
        if admin != None:
            if admin[0] not in admins and admin[0] != None:
                admins.append(admin[0])
    # USERS
    if not Config.IS_BOT_PUBLIC == "True":
        database_users = users_db.get_users()
        for user in Config.AUTH_USERS:
            if user not in allowed_users:
                allowed_users.append(user)
        for user in database_users:
            if user != None:
                if user[0] not in allowed_users and user[0] != None:
                    allowed_users.append(user[0])

    if return_msg:
        msg = "<b>ALLOWED CHATS</b>"
        for chat in allowed_chats:
            msg += f"\n<code>{chat}</code>"

        msg += "\n\n<b>ALLOWED USERS</b>"
        if Config.IS_BOT_PUBLIC == "True":
            msg += "\nAllowed For Everyone"
        try:
            for user in allowed_users:
                msg += f"\n<code>{user}</code>"
        except:
            pass

        msg += "\n\n<b>ADMINS</b>"
        for admin in admins:
            msg += f"\n<code>{admin}</code>"

        return msg

def check_id(id=None, message=None, restricted=False):
    all_list = allowed_chats + allowed_users + admins
    if restricted:
        if id in admins:
            return True
        else:
            return False
    else:
        if message.from_user.id != message.chat.id:
            id = message.chat.id
        else:
            id = message.from_user.id
        if Config.IS_BOT_PUBLIC == "True":
            return True
        elif id in all_list:
            return True
        else:
            return False




    


    
