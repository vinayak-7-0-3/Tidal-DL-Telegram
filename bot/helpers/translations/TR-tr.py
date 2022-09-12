class EN(object):
    INIT_MSG = "<b>Merhaba {} </b>"

    START_TEXT = """
<b>Merhaba {} </b>,
Ben bir Tidal DL Botuyum. Tidal'dan şarkı indirmek için kullanılır.
"""

    HELP_MSG = """
<b>Merhaba {} </b>,
Ben bir Tidal DL Botuyum. tidal.com'dan şarkı indirmek için kullanılır.
Tüm şarkıları master kalitesinde indirebilirsiniz.
<code>/{}</code>
"""

    CMD_LIST = """
<b>Merhaba {0} </b>,
Bot için komutlar aşağıda açıklanmıştır:
<code>/{1}</code> - Yardım mesajını gösterir.
<code>/{2}</code> - Komutların listesini gösterir.
<code>/{3}</code> - Şarkıyı Tidal Link'ten indirir.
<code>/{4}</code> - Botun kimliğini doğrular <b> [ ADMIN ] </b>.
<code>/{5}</code> - Bir kabuk komutu çalıştırır <b> [ ADMIN ] </b>.
<code>/{6}</code> - Bot'un Ayarlar Panelini Açın. <b> [ ADMIN ] </b>.
Komutu yazdığınızda, her komut için yardım gösterilir.
Tartışma Grubunda şüphelerinizi sormaktan çekinmeyin.
"""

    INIT_DOWNLOAD = "İndirmeyi başlatmaya çalışıyorum..."
    ERR_NO_LINK = "Mesajda bağlantı bulunamadı."

    ALREADY_AUTH = "Kimlik doğrulamanız zaten yapıldı.\nBunun için geçerlidir: {}"
    AUTH_DISABLED = "Kimlik doğrulama devre dışı bırakıldığından indirilemiyor."
#
#
# INLINE MODE TEXTS..............................................................
#
#
    INLINE_SEARCH_HELP = """
Bu botu her yerde doğrudan şarkı aramak için kullanabilirsiniz.
Sonuçları almak için arama sorgusu ile birlikte bayrakları kullanın.
Bayraklar :
<code>-s</code> Tidal izi için
<code>-a</code> Tidal albümü için
<code>-d</code> Arşiv kanalından şarkı
"""
    INLINE_PLACEHOLDER = "Arama ile ilgili yardım için buraya tıklayın."
    INLINE_NO_RESULT = "Sonuç bulunamadı"

    INPUT_MESSAGE_TRACK = """
💽 <b>Başlık :</b> {0}
👤 <b>Sanatçı :</b> {1}
💿 <b>Album :</b> {2}
🕒 <b>Süre :</b> {3}
"""

    INPUT_MESSAGE_ALBUM = """
💽 <b>Başlık :</b> {0}
👤 <b>Sanatçı :</b> {1}
📀 <b>Şarkı :</b> {2}
📅 <b>Yayın tarihi :</b> {3}
"""

    INLINE_MEDIA_SEARCH = """
💽 <b>Başlık :</b> {0}
👤 <b>Sanatçı :</b> {1}
"""
#
#
# ALBUM TEXT FORMAT...............................................................
#
#
    ALBUM_DETAILS = """
💽 <b>Başlık :</b> {0}
👤 <b>Sanatçı :</b> {1}
📅 <b>Yayın tarihi :</b> {2}
📀 <b>Şarkı Sayısı :</b> {3}
🕒 <b>Süre :</b> {4}
🔢 <b>Cilt Sayısı :</b> {5}
"""
#
#
# CHATS AUTH MSGS
#
#
    CHAT_AUTH = "Sohbeti başarıyla yetkilendirdi : {} "
    ADD_ADMIN = "{} Eklendi."
#
#
# SETTINGS PANEL
#
#
    INIT_SETTINGS_MENU = "<b>Bot Ayarları Menüsüne Hoş Geldiniz.</b>\n\nAyarlarını açma seçeneğini seçin."
    TIDAL_AUTH_PANEL = "<b>Tidal Kimlik Doğrulamasını Yapılandırın</b>\n\n"
    AUTH_SUCCESFULL_MSG = "Kimlik doğrulama başarılı.\n\n"
    WARN_REMOVE_AUTH = "<b>Kimlik doğrulamasını kaldırmak üzeresiniz.</b>\n\nOnaylamak için tekrar basın."
