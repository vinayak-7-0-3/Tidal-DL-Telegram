import subprocess
from bot import CMD
from pyrogram import Client, filters
from bot.helpers.utils.auth_check import check_id

@Client.on_message(filters.command(CMD.SHELL))
def shell(bot, update):
    if check_id(update.from_user.id, restricted=True):
        message = update.text
        cmd = update.text.split(' ', 1)
        if len(cmd) == 1:
            update.reply_text('No command to execute was given.')
            return
        cmd = cmd[1]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        reply = ''
        stderr = stderr.decode()
        stdout = stdout.decode()
        if stdout:
            reply += f"*Stdout*\n`{stdout}`\n"
        if stderr:
            reply += f"*Stderr*\n`{stderr}`\n"
        if len(reply) > 3000:
            with open('shell_output.txt', 'w') as file:
                file.write(reply)
            with open('shell_output.txt', 'rb') as doc:
                bot.send_document(
                    document=doc,
                    filename=doc.name,
                    reply_to_message_id=message.id,
                    chat_id=message.chat.id)
        else:
            update.reply_text(reply)