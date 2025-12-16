import random
import logging
from linebot.v3.messaging import TextMessage
from config import Config

logger = logging.getLogger(__name__)


class TextManager:
    """مدير المحتوى النصي - يرسل نص عادي بدون Flex"""
    
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

    def handle(self, cmd: str, theme: str = "light"):
        """معالجة الاوامر النصية - يرجع TextMessage"""
        cmd = cmd.strip().lower()
        
        mapping = {
            "تحدي": (self.challenges, ""),
            "اعتراف": (self.confessions, ""),
            "منشن": (self.mentions, ""),
            "شخصيه": (self.personality, ""),
            "شخصية": (self.personality, ""),
            "سؤال": (self.questions, ""),
            "سوال": (self.questions, ""),
            "حكمه": (self.quotes, ""),
            "حكمة": (self.quotes, ""),
            "موقف": (self.situations, "")
        }
        
        if cmd in mapping:
            data, _ = mapping[cmd]
            if data:
                content = random.choice(data)
                return TextMessage(text=content)

        return None
