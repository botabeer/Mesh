import random
import logging
import os
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

    def _create_text_bubble(self, title, content, theme="light"):
        """إنشاء Bubble مخصص للمحتوى النصي"""
        c = Config.get_theme(theme)
        
        contents = [
            {
                "type": "text",
                "text": title,
                "size": "xl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg"},
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": content,
                        "size": "md",
                        "color": c["text"],
                        "wrap": True,
                        "align": "center"
                    }
                ],
                "backgroundColor": c["card_secondary"],
                "cornerRadius": "16px",
                "paddingAll": "20px",
                "margin": "lg"
            },
            {"type": "separator", "margin": "lg"},
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "مرة اخرى", "text": title},
                        "style": "primary",
                        "color": c["primary"],
                        "height": "sm",
                        "flex": 1
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "البداية", "text": "بداية"},
                        "style": "secondary",
                        "height": "sm",
                        "flex": 1
                    }
                ],
                "spacing": "sm",
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
                "backgroundColor": c["card"],
                "paddingAll": "24px"
            }
        }
        
        qr_items = ["تحدي", "سؤال", "اعتراف", "منشن", "موقف", "حكمة", "شخصية", "بداية"]
        qr = QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in qr_items])
        
        return FlexMessage(alt_text=title, contents=FlexContainer.from_dict(bubble), quickReply=qr)

    def handle(self, cmd, theme="light"):
        cmd = cmd.strip().lower()
        
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
                return self._create_text_bubble(title, content, theme)
            else:
                logger.warning(f"No data for command: {cmd}")

        return None
