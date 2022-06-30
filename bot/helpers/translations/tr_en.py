class EN(object):
    INIT_MSG = "<b>你好 {} </b>"

    START_TEXT = """
<b>你好 {} </b>,
我是一个可以下载Tidal平台上音乐的Bot
"""

    HELP_MSG = """
<b>你好 {} </b>,

我是一个可以下载Tidal平台上音乐的Bot

你可以以Master音质下载所有歌曲（视各区域情况而定，MQA）

查看 <code>/{}</code> 来获取命令
"""

     CMD_LIST = """
<b>你好 {0} </b>,

这是这个机器人的命令

<code>/{1}</code> - 展示帮助信息
<code>/{2}</code> - 展示命令列表
<code>/{3}</code> - 从Tidal链接下载音乐
<code>/{4}</code> - 将某一个群组授权<b>[仅限管理员]</b>.
<code>/{5}</code> - 运行一个Shell命令 <b>[仅限管理员]</b>.
<code>/{6}</code> - 打开设置菜单 <b>[仅限管理员]</b>.

当您在键入命令时会展示对应命令的帮助

"""

    INIT_DOWNLOAD = "正在尝试下载..."
    FILE_EXIST = "文件已经在频道中存在\n\n标题 : <code>{}</code>\n\n点击此处下载"
    ALREADY_AUTH = "你已经成功完成来自Tidal的授权\n有效期截至 {}"
    NO_AUTH = "授权无效"
#
#
# INLINE MODE TEXTS..............................................................
#
#
    INLINE_SEARCH_HELP = """
你可以使用这个Bot在任何地方直接搜索歌曲

在搜索队列中使用以下参数来帮助你找到对应的歌曲

<code>-s</code> 从tidal上搜索歌曲
<code>-a</code> 从tidal上搜索专辑
<code>-d</code> 从频道上搜索歌曲
"""
    INLINE_PLACEHOLDER = "点击此处获得帮助"
    INLINE_NO_RESULT = "未找到结果"

    INPUT_MESSAGE_TRACK = """
💽 <b>标题 :</b> {0}
👤 <b>艺术家:</b> {1}
💿 <b>专辑 :</b> {2}
🕒 <b>持续时长 :</b> {3}
"""

   INPUT_MESSAGE_ALBUM = """
💽 <b>标题 :</b> {0}
👤 <b>艺术家 :</b> {1}
📀 <b>曲目 :</b> {2}
📅 <b>发布时间 :</b> {3}
"""

    INLINE_MEDIA_SEARCH = """
<b>标题 :</b> {0}

<b>艺术家 :</b> {1}
"""
#
#
# ALBUM TEXT FORMAT...............................................................
#
#
    ALBUM_DETAILS = """
💽 <b>标题 :</b> {0}
👤 <b>艺术家 :</b> {1}
📅 <b>发布时间 :</b> {2}
📀 <b>曲目数量 :</b> {3}
🕒 <b>持续时长 :</b> {4}
🔢 <b>卷的数目 :</b> {5}
"""
#
#
# CHATS AUTH MSGS
#
#
    CHAT_AUTH = "成功为 : {} 授权."
    ADD_ADMIN = "成功添加 {} 为管理员"
   NO_ID_PROVIDED = "无法添加管理员\n提供User ID或者回复被添加者的消息以完成管理员的添加"
#
#
# SETTINGS PANEL
#
#
    INIT_SETTINGS_MENU = "<b>欢迎进入设置菜单</b>\n\n请选择你想要设置的选项"
    TIDAL_AUTH_PANEL = "<b>成功完成Tidal的授权\n\n授权状态 : </b>{}"
    AUTH_SUCCESFULL_MSG = "授权成功\n\n有效期至 {}"
    WARN_REMOVE_AUTH = "<b>你即将要移除一个授权</b>\n\n请再次确认"
    AUTH_NEXT_STEP = "Go to {} within the next {} to complete setup." #语言表达顺序改变
#
#
# INDEXING
#
#
    INIT_INDEX = "正在初始化索引引擎\n请耐心等候"
    INDEX_DONE = "检索成功"
#
#
# BUTTONS
#
#
    JOIN_MUSIC_STORAGE = "加入音乐库"
    GET_FILE = "获取文件"
    LOGIN_TIDAL = "点击登录"
#
#
# ERRORS
#
#
    ERR_VARS = "必要的变量缺失...\n请检查你的配置(.env)是否正确"
    ERR_AUTH_CHECK = "因为 {} 无法下载"
    ERR_NO_LINK = "未找到链接"
    ERR_INDEX = "在索引时发生错误 \n\n{}"
