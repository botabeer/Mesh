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

    def _create_quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="منشن", text="منشن")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="شخصية", text="شخصيه")),
            QuickReplyItem(action=MessageAction(label="حكمة", text="حكمه")),
            QuickReplyItem(action=MessageAction(label="موقف", text="موقف")),
            QuickReplyItem(action=MessageAction(label="البداية", text="بدايه"))
        ])

    def handle(self, cmd: str):
        quick_reply = self._create_quick_reply()

        if cmd == "تحدي" and self.challenges:
            text = random.choice(self.challenges)
            return TextMessage(text=text, quickReply=quick_reply)

        if cmd == "اعتراف" and self.confessions:
            text = random.choice(self.confessions)
            return TextMessage(text=text, quickReply=quick_reply)

        if cmd == "منشن" and self.mentions:
            text = random.choice(self.mentions)
            return TextMessage(text=text, quickReply=quick_reply)

        if cmd in ("شخصيه", "شخصية") and self.personality:
            text = random.choice(self.personality)
            return TextMessage(text=text, quickReply=quick_reply)

        if cmd == "سؤال" and self.questions:
            text = random.choice(self.questions)
            return TextMessage(text=text, quickReply=quick_reply)

        if cmd in ("حكمه", "حكمة") and self.quotes:
            text = random.choice(self.quotes)
            return TextMessage(text=text, quickReply=quick_reply)

        if cmd == "موقف" and self.situations:
            text = random.choice(self.situations)
            return TextMessage(text=text, quickReply=quick_reply)

        return None
