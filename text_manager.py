import random
import logging
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config

logger = logging.getLogger(__name__)


class TextManager:
    def __init__(self):
        self.challenges = self._load_file("games/challenges.txt")
        self.confessions = self._load_file("games/confessions.txt")
        self.mentions = self._load_file("games/mentions.txt")
        self.personality = self._load_file("games/personality.txt")
        self.questions = self._load_file("games/questions.txt")
        self.quotes = self._load_file("games/quotes.txt")
        self.situations = self._load_file("games/situations.txt")

    def _load_file(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                return lines
        except Exception as e:
            logger.error(f"Load {path} error: {e}")
            return []

    def _quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="القائمة", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="منشن", text="منشن")),
            QuickReplyItem(action=MessageAction(label="موقف", text="موقف")),
            QuickReplyItem(action=MessageAction(label="حكمة", text="حكمة")),
            QuickReplyItem(action=MessageAction(label="شخصية", text="شخصية")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
        ])

    def _create_flex_message(self, title: str, content: str, theme: str = "light"):
        c = Config.get_theme(theme)

        contents = [
            {
                "type": "text",
                "text": title,
                "size": "lg",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "md", "color": c["border"]},
            {
                "type": "text",
                "text": content,
                "size": "md",
                "color": c["text"],
                "wrap": True,
                "margin": "md"
            },
            {"type": "separator", "margin": "md", "color": c["border"]},
            {
                "type": "button",
                "action": {"type": "message", "label": "البداية", "text": "بداية"},
                "style": "secondary",
                "height": "sm",
                "margin": "md"
            }
        ]

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px",
                "spacing": "md",
                "backgroundColor": c["bg"]
            }
        }

        return FlexMessage(
            alt_text=title,
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    def handle(self, cmd: str, theme: str = "light"):
        cmd = cmd.strip().lower()
        
        if cmd == "تحدي" and self.challenges:
            return self._create_flex_message("تحدي", random.choice(self.challenges), theme)
        
        if cmd == "اعتراف" and self.confessions:
            return self._create_flex_message("اعتراف", random.choice(self.confessions), theme)
        
        if cmd == "منشن" and self.mentions:
            return self._create_flex_message("منشن", random.choice(self.mentions), theme)
        
        if cmd in ("شخصيه", "شخصية") and self.personality:
            return self._create_flex_message("سؤال شخصية", random.choice(self.personality), theme)
        
        if cmd in ("سؤال", "سوال") and self.questions:
            return self._create_flex_message("سؤال", random.choice(self.questions), theme)
        
        if cmd in ("حكمه", "حكمة") and self.quotes:
            return self._create_flex_message("حكمة", random.choice(self.quotes), theme)
        
        if cmd == "موقف" and self.situations:
            return self._create_flex_message("موقف", random.choice(self.situations), theme)

        return None
