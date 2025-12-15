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

    def _create_quick_reply(self, items):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label=label, text=text))
            for label, text in items
        ])

    def handle(self, cmd: str, ui):
        # ازرار ثابتة
        quick_items = [
            ("تحدي", "تحدي"),
            ("اعتراف", "اعتراف"),
            ("منشن", "منشن"),
            ("شخصيه", "شخصيه"),
            ("سؤال", "سؤال"),
            ("حكمه", "حكمه"),
            ("موقف", "موقف")
        ]

        if cmd == "تحدي" and self.challenges:
            text = random.choice(self.challenges)
            return TextMessage(text=text, quickReply=self._create_quick_reply(quick_items))

        if cmd == "اعتراف" and self.confessions:
            text = random.choice(self.confessions)
            return TextMessage(text=text, quickReply=self._create_quick_reply(quick_items))

        if cmd == "منشن" and self.mentions:
            text = random.choice(self.mentions)
            return TextMessage(text=text, quickReply=self._create_quick_reply(quick_items))

        if cmd == "شخصيه" and self.personality:
            text = random.choice(self.personality)
            return TextMessage(text=text, quickReply=self._create_quick_reply(quick_items))

        if cmd == "سؤال" and self.questions:
            text = random.choice(self.questions)
            return TextMessage(text=text, quickReply=self._create_quick_reply(quick_items))

        if cmd == "حكمه" and self.quotes:
            text = random.choice(self.quotes)
            return TextMessage(text=text, quickReply=self._create_quick_reply(quick_items))

        if cmd == "موقف" and self.situations:
            text = random.choice(self.situations)
            return TextMessage(text=text, quickReply=self._create_quick_reply(quick_items))

        return None
