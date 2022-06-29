from .postgres_db import DataBaseHandle
import psycopg2
import psycopg2.extras
import datetime

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
            artist VARCHAR(2000) DEFAULT NULL
        )"""

        cur = self.scur()
        try:
            cur.execute(music_schema)
        except psycopg2.errors.UniqueViolation:
            pass

        self._conn.commit()
        self.ccur(cur)

    def set_music(self, msg_id, title, artist):
        #title = ''.join(filter(lambda i:i not in special_characters, title))
        sql = "SELECT * FROM music_table"
        cur = self.scur()

        sql = "INSERT INTO music_table(msg_id,title,artist) VALUES(%s,%s,%s)"
        cur.execute(sql, (msg_id, title, artist))

        self.ccur(cur)

    def get_music_id(self, title):
        sql = "SELECT * FROM music_table WHERE title=%s"

        cur = self.scur()
        cur.execute(sql, (title,))
        if cur.rowcount > 0:
            row = cur.fetchone()
            return row[0], row[2]
        else:
            return None, None

        self.ccur(cur)

    def __del__(self):
        super().__del__()

set_db = TidalSettings()
users_db = AuthedUsers()
admins_db = AuthedAdmins()
chats_db = AuthedChats()
music_db = MusicDB()