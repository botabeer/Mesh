import random
import logging
from linebot.v3.messaging import TextMessage, QuickReply, QuickReplyItem, MessageAction

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
            QuickReplyItem(action=MessageAction(label="البداية", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="منشن", text="منشن")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="شخصية", text="شخصية")),
            QuickReplyItem(action=MessageAction(label="حكمة", text="حكمة")),
            QuickReplyItem(action=MessageAction(label="موقف", text="موقف"))
        ])

    def handle(self, cmd: str):
        qr = self._quick_reply()

        if cmd == "تحدي" and self.challenges:
            return TextMessage(text=random.choice(self.challenges), quickReply=qr)
        if cmd == "اعتراف" and self.confessions:
            return TextMessage(text=random.choice(self.confessions), quickReply=qr)
        if cmd == "منشن" and self.mentions:
            return TextMessage(text=random.choice(self.mentions), quickReply=qr)
        if cmd in ("شخصيه", "شخصية") and self.personality:
            return TextMessage(text=random.choice(self.personality), quickReply=qr)
        if cmd == "سؤال" and self.questions:
            return TextMessage(text=random.choice(self.questions), quickReply=qr)
        if cmd in ("حكمه", "حكمة") and self.quotes:
            return TextMessage(text=random.choice(self.quotes), quickReply=qr)
        if cmd == "موقف" and self.situations:
            return TextMessage(text=random.choice(self.situations), quickReply=qr)

        return None
