import json
import psycopg2
import datetime
import psycopg2.extras
from .postgres_db import DataBaseHandle

from bot import Config

#special_characters = ['!','#','$','%', '&','@','[',']',' ',']','_', ',', '.', ':', ';', '<', '>', '?', '\\', '^', '`', '{', '|', '}', '~']

"""
TIDAL-DL SETTINGS VARS

AUTH_TOKEN - Tidal main auth token
AUTH_CHATS - Chats where bot is allowed
AUTH_USERS - Users who can use bot
AUTH_ADMINS - Admins of the bot
"""

class TidalSettings(DataBaseHandle):

    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)

        settings_schema = """CREATE TABLE IF NOT EXISTS tidal_settings (
            id SERIAL PRIMARY KEY NOT NULL,
            var_name VARCHAR(50) NOT NULL UNIQUE,
            var_value VARCHAR(2000) DEFAULT NULL,
            vtype VARCHAR(20) DEFAULT NULL,
            blob_val BYTEA DEFAULT NULL,
            date_changed TIMESTAMP NOT NULL
        )"""

        cur = self.scur()
        try:
            cur.execute(settings_schema)
        except psycopg2.errors.UniqueViolation:
            pass

        self._conn.commit()
        self.ccur(cur)

    def set_variable(self, var_name, var_value, update_blob=False, blob_val=None):
        vtype = "str"
        if isinstance(var_value, bool):
            vtype = "bool"
        elif isinstance(var_value, int):
            vtype = "int"

        if update_blob:
            vtype = "blob"

        sql = "SELECT * FROM tidal_settings WHERE var_name=%s"
        cur = self.scur()

        cur.execute(sql, (var_name,))
        if cur.rowcount > 0:
            if not update_blob:
                sql = "UPDATE tidal_settings SET var_value=%s , vtype=%s WHERE var_name=%s"
            else:
                sql = "UPDATE tidal_settings SET blob_val=%s , vtype=%s WHERE var_name=%s"
                var_value = blob_val

            cur.execute(sql, (var_value, vtype, var_name))
        else:
            if not update_blob:
                sql = "INSERT INTO tidal_settings(var_name,var_value,date_changed,vtype) VALUES(%s,%s,%s,%s)"
            else:
                sql = "INSERT INTO tidal_settings(var_name,blob_val,date_changed,vtype) VALUES(%s,%s,%s,%s)"
                var_value = blob_val

            cur.execute(sql, (var_name, var_value, datetime.datetime.now(), vtype))

        self.ccur(cur)

    def get_variable(self, var_name):
        sql = "SELECT * FROM tidal_settings WHERE var_name=%s"
        cur = self.scur()

        cur.execute(sql, (var_name,))
        if cur.rowcount > 0:
            row = cur.fetchone()
            vtype = row[3]
            val = row[2]
            if vtype == "int":
                val = int(row[2])
            elif vtype == "str":
                val = str(row[2])
            elif vtype == "bool":
                if row[2] == "true":
                    val = True
                else:
                    val = False

            return val, row[4]
        else:
            return None, None

        self.ccur(cur)

    def __del__(self):
        super().__del__()

    def set_auth_chats(self, var_value: int):
        vtype = "int"
        var_name = "AUTH_CHATS"

        sql = "SELECT * FROM tidal_settings WHERE var_name=%s"
        cur = self.scur()
        cur.execute(sql, (var_name,))
        sql = "INSERT INTO tidal_settings(var_name,var_value,date_changed,vtype) VALUES(%s,%s,%s,%s)"
        cur.execute(sql, (var_name, var_value, datetime.datetime.now(), vtype))
        self.ccur(cur)


class AuthedUsers(DataBaseHandle):
    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)
        table_schema = """CREATE TABLE IF NOT EXISTS authed_users (
            uid bigint
        )"""
        cur = self.scur()
        try:
            cur.execute(table_schema)
        except psycopg2.errors.UniqueViolation:
            pass
        self._conn.commit()
        self.ccur(cur)

    def set_users(self, var_value):
        sql = "SELECT * FROM authed_users"
        cur = self.scur()
        cur.execute(sql)
        sql = "INSERT INTO authed_users VALUES({})".format(var_value)
        cur.execute(sql)
        self.ccur(cur)

    def get_users(self):
        sql = "SELECT * FROM authed_users"
        cur = self.scur()
        cur.execute(sql)
        if cur.rowcount > 0:
            rows = cur.fetchall()
            return rows
        else:
            return None, None
        self.ccur(cur)

    def __del__(self):
        super().__del__()

class AuthedAdmins(DataBaseHandle):
    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)
        table_schema = """CREATE TABLE IF NOT EXISTS authed_admins (
            uid bigint
        )"""
        cur = self.scur()
        try:
            cur.execute(table_schema)
        except psycopg2.errors.UniqueViolation:
            pass
        self._conn.commit()
        self.ccur(cur)

    def set_admins(self, var_value):
        sql = "SELECT * FROM authed_admins"
        cur = self.scur()
        cur.execute(sql)
        sql = "INSERT INTO authed_admins VALUES({})".format(var_value)
        cur.execute(sql)
        self.ccur(cur)

    def get_admins(self):
        sql = "SELECT * FROM authed_admins"
        cur = self.scur()
        cur.execute(sql)
        if cur.rowcount > 0:
            rows = cur.fetchall()
            return rows
        else:
            return None, None
        self.ccur(cur)

    def __del__(self):
        super().__del__()

class AuthedChats(DataBaseHandle):
    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)
        table_schema = """CREATE TABLE IF NOT EXISTS authed_chats (
            uid bigint
        )"""
        cur = self.scur()
        try:
            cur.execute(table_schema)
        except psycopg2.errors.UniqueViolation:
            pass
        self._conn.commit()
        self.ccur(cur)

    def set_chats(self, var_value):
        sql = "SELECT * FROM authed_chats"
        cur = self.scur()
        cur.execute(sql)
        sql = "INSERT INTO authed_chats VALUES({})".format(var_value)
        cur.execute(sql)
        self.ccur(cur)

    def get_chats(self):
        sql = "SELECT * FROM authed_chats"
        cur = self.scur()
        cur.execute(sql)
        if cur.rowcount > 0:
            rows = cur.fetchall()
            return rows
        else:
            return None, None
        self.ccur(cur)

    def __del__(self):
        super().__del__()

class MusicDB(DataBaseHandle):
    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)

        music_schema = """CREATE TABLE IF NOT EXISTS music_table (
            msg_id BIGINT UNIQUE,
            title VARCHAR(2000) DEFAULT NULL,
            artist VARCHAR(2000) DEFAULT NULL,
            track_id VARCHAR(50) DEFAULT NULL,
            type VARCHAR(30) DEFAULT NULL
        )"""

        cur = self.scur()
        try:
            cur.execute(music_schema)
        except psycopg2.errors.UniqueViolation:
            pass

        self._conn.commit()
        self.ccur(cur)


    # Type - "track" or "album"
    def set_music(self, msg_id, title, artist, track_id, type):
        #title = ''.join(filter(lambda i:i not in special_characters, title))
        sql = "SELECT * FROM music_table"
        cur = self.scur()

        sql = "INSERT INTO music_table(msg_id,title,artist,track_id,type) VALUES(%s,%s,%s,%s,%s)"
        try:
            cur.execute(sql, (msg_id, title, artist, track_id, type))
        except psycopg2.errors.UniqueViolation:
            cur.execute("rollback")

        self.ccur(cur)

    def get_music_id(self, title, artist, track_id, type):
        sql = "SELECT * FROM music_table WHERE title=%s"

        cur = self.scur()
        cur.execute(sql, (title,))
        if cur.rowcount > 0:
            row = cur.fetchall()
            for item in row:
                if item[2] == artist:
                    if track_id:
                        if item[3] == int(track_id):
                            return item[0], item[2]
                    if item[4] == type:
                        return item[0], item[2]
        return None, None

        self.ccur(cur)

    def __del__(self):
        super().__del__()

class UserSettings(DataBaseHandle):
    shared_users = {}

    def __init__(self, dburl=None):
        if dburl is None:
            dburl = Config.DATABASE_URL
        super().__init__(dburl)

        cur = self.scur()

        table = """CREATE TABLE IF NOT EXISTS user_settings (
            user_id VARCHAR(50) NOT NULL,
            json_data VARCHAR(1000) NOT NULL
        )"""

        try:
            cur.execute(table)
        except psycopg2.errors.UniqueViolation:
            pass

        self.ccur(cur)

    def set_var(self, user_id, var_name, var_value):
        user_id = str(user_id)
        sql = "SELECT * FROM user_settings WHERE user_id=%s"
        cur = self.scur(dictcur=True)

        user = self.shared_users.get(user_id)
        if user is not None:
            self.shared_users[user_id][var_name] = var_value
        else:
            cur.execute(sql, (user_id,))
            if cur.rowcount > 0:
                user = cur.fetchone()
                jdata = user.get("json_data")
                jdata = json.loads(jdata)
                jdata["LANGUAGE"] = var_value
                self.shared_users[user_id] = jdata
            else:
                self.shared_users[user_id] = {var_name: var_value}

        cur.execute(sql, (user_id,))
        if cur.rowcount > 0:
            insql = "UPDATE user_settings SET json_data = %s where user_id=%s"
            cur.execute(insql, (json.dumps(self.shared_users.get(user_id)), user_id))

        else:
            insql = "INSERT INTO user_settings(user_id, json_data) VALUES(%s, %s)"
            cur.execute(insql, (user_id, json.dumps(self.shared_users.get(user_id))))

        self.ccur(cur)

    def get_var(self, user_id, var_name):
        user_id = str(user_id)
        sql = "SELECT * FROM user_settings WHERE user_id=%s"
        # search the cache
        user = self.shared_users.get(user_id)
        if user is not None:
            return user.get(var_name)
        else:
            cur = self.scur(dictcur=True)

            cur.execute(sql, (user_id,))
            if cur.rowcount > 0:
                user = cur.fetchone()
                jdata = user.get("json_data")
                jdata = json.loads(jdata)
                self.shared_users[user_id] = jdata
                return jdata.get(var_name)
            else:
                return None

            self.ccur(cur)

set_db = TidalSettings()
users_db = AuthedUsers()
admins_db = AuthedAdmins()
chats_db = AuthedChats()
music_db = MusicDB()
user_settings = UserSettings()