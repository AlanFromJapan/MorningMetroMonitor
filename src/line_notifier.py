
from linebot import (
    LineBotApi
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from config import conf

lba = LineBotApi(conf["channelAccessToken"])

def send_line_message(message):
    lba.push_message(conf["targetID"], TextSendMessage(text=message))
    
