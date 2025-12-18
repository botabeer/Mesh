import random
import logging
import os
from ui import UI

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
        logger.info(f"TextManager loaded {sum(len(v) for v in [self.challenges, self.confessions, self.mentions, self.personality, self.questions, self.quotes, self.situations])} items")

    def _load_file(self, path):
        try:
            if not os.path.exists(path):
                logger.warning(f"File not found: {path}")
                return []
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                logger.info(f"Loaded {len(lines)} items from {path}")
                return lines
        except Exception as e:
            logger.error(f"Load {path} error: {e}")
            return []

    def handle(self, cmd, theme="light"):
        cmd = cmd.strip().lower()
        ui = UI(theme)
        
        mapping = {
            "تحدي": ("تحدي", self.challenges),
            "اعتراف": ("اعتراف", self.confessions),
            "منشن": ("منشن", self.mentions),
            "شخصيه": ("شخصية", self.personality),
            "شخصية": ("شخصية", self.personality),
            "سؤال": ("سؤال", self.questions),
            "سوال": ("سؤال", self.questions),
            "حكمه": ("حكمة", self.quotes),
            "حكمة": ("حكمة", self.quotes),
            "موقف": ("موقف", self.situations)
        }
        
        if cmd in mapping:
            title, data = mapping[cmd]
            if data:
                content = random.choice(data)
                return ui.text_content(title, content)
            else:
                logger.warning(f"No data for command: {cmd}")

        return None
