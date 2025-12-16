import random
import logging
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config

logger = logging.getLogger(__name__)


class TextManager:
    """مدير المحتوى النصي التفاعلي"""
    
    def __init__(self):
        self.challenges = self._load_file("games/challenges.txt")
        self.confessions = self._load_file("games/confessions.txt")
        self.mentions = self._load_file("games/mentions.txt")
        self.personality = self._load_file("games/personality.txt")
        self.questions = self._load_file("games/questions.txt")
        self.quotes = self._load_file("games/quotes.txt")
        self.situations = self._load_file("games/situations.txt")

    def _load_file(self, path: str):
        """تحميل ملف نصي"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                return lines
        except Exception as e:
            logger.error(f"Load {path} error: {e}")
            return []

    def _quick_reply(self):
        """الأزرار الثابتة"""
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="البداية", text="بداية")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف"))
        ])

    def _create_text_card(self, title: str, content: str, theme: str = "light"):
        """إنشاء بطاقة نصية بسيطة"""
        c = Config.get_theme(theme)

        contents = [
            {"type": "text", "text": title, "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "text", "text": content, "size": "sm", "color": c["text"], "wrap": True, "margin": "lg"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": title, "text": title}, "style": "secondary", "height": "sm", "margin": "sm"}
        ]

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px",
                "backgroundColor": c["bg"]
            }
        }

        return FlexMessage(
            alt_text=title,
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    def handle(self, cmd: str, theme: str = "light"):
        """معالجة الأوامر النصية"""
        cmd = cmd.strip().lower()
        
        mapping = {
            "تحدي": (self.challenges, "تحدي"),
            "اعتراف": (self.confessions, "اعتراف"),
            "منشن": (self.mentions, "منشن"),
            "شخصيه": (self.personality, "شخصية"),
            "شخصية": (self.personality, "شخصية"),
            "سؤال": (self.questions, "سؤال"),
            "سوال": (self.questions, "سؤال"),
            "حكمه": (self.quotes, "حكمة"),
            "حكمة": (self.quotes, "حكمة"),
            "موقف": (self.situations, "موقف")
        }
        
        if cmd in mapping:
            data, title = mapping[cmd]
            if data:
                return self._create_text_card(title, random.choice(data), theme)

        return None
