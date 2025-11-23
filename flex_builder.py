"""
Bot Mesh - Flex Builder
"""
from linebot.models import QuickReply, QuickReplyButton, MessageAction

from config import THEMES

class FlexBuilder:
    def __init__(self, theme):
        self.theme = THEMES.get(theme, THEMES["white"])

    def welcome(self):
        return {
            "type": "bubble",
            "body": {"type": "box","layout":"vertical","contents":[
                {"type":"text","text":"مرحباً بك في Bot Mesh!","weight":"bold","size":"lg"}
            ]},
            "styles":{"header":{"backgroundColor":self.theme["primary"]}}
        }

    def get_games_quick_reply(self):
        buttons = ["ذكاء","لون","ترتيب","رياضيات","أسرع","ضد","تكوين","أغنية","لعبة","سلسلة","خمن","توافق","إيقاف"]
        return QuickReply(items=[QuickReplyButton(action=MessageAction(label=btn,text=btn)) for btn in buttons])
