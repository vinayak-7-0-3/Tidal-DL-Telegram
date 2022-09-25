import json
import asyncio

from bot import BOT
from config import Config
from bot.helpers.database.postgres_impl import set_db, music_db

async def add_queue(dump_list):
    db_list, _ = set_db.get_variable("QUEUE")
    if db_list is None:
        main_list = []
    else:
        main_list = json.loads(db_list)

    main_list.append(dump_list)
    data = json.dumps(main_list)
    set_db.set_variable("QUEUE", data, False, None)

async def dump_from_queue():
    while True:
        try:
            await asyncio.sleep(13)
        except asyncio.CancelledError:
            break
        db_list, _ = set_db.get_variable("QUEUE")
        set_db.set_variable("QUEUE", "[]", False, None)

        if db_list is None or db_list == "[]":
            continue
        else:
            data = json.loads(db_list)
            data_copy = data[:]
            t = 0
            for task in data:
                task_copy = task[:]
                t_index = data.index(task)
                m = 0
                try:
                    for music in task:
                        m_index = task.index(music)
                        try:
                            copy = await BOT.copy_message(
                                chat_id=Config.LOG_CHANNEL_ID,
                                from_chat_id=music['chat_id'],
                                message_id=music['msg_id']
                            )
                            task_copy.pop(m_index - m)
                            m+=1
                            music_db.set_music(copy.id, music['title'], music['artist'], music['id'], music['type'])
                        except asyncio.CancelledError:
                            data_copy.pop(t_index - t)
                            data_copy.insert(0, task_copy)
                            data = json.dumps(data_copy)
                            set_db.set_variable("QUEUE", data, False, None)
                            return
                    data_copy.pop(t_index - t)
                    t+=1
                except asyncio.CancelledError:
                    data = json.dumps(data_copy)
                    set_db.set_variable("QUEUE", data, False, None)
                    return