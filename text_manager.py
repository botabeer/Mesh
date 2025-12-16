import random
import logging
from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction
)
from config import Config

logger = logging.getLogger(__name__)


class TextManager:
    def __init__(self):
        self._data = {
            "تحدي": self._load_file("games/challenges.txt"),
            "اعتراف": self._load_file("games/confessions.txt"),
            "منشن": self._load_file("games/mentions.txt"),
            "شخصية": self._load_file("games/personality.txt"),
            "سؤال": self._load_file("games/questions.txt"),
            "حكمة": self._load_file("games/quotes.txt"),
            "موقف": self._load_file("games/situations.txt"),
        }

    # ===============================
    # Load
    # ===============================
    def _load_file(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
                logger.info(f"Loaded {len(lines)} lines from {path}")
                return lines
        except Exception as e:
            logger.error(f"Load {path} error: {e}")
            return []

    # ===============================
    # Quick Reply
    # ===============================
    def _quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(
                action=MessageAction(label="البداية", text="بداية")
            ),
            QuickReplyItem(
                action=MessageAction(label="العاب", text="العاب")
            ),
            QuickReplyItem(
                action=MessageAction(label="تحدي", text="تحدي")
            ),
            QuickReplyItem(
                action=MessageAction(label="اعتراف", text="اعتراف")
            ),
            QuickReplyItem(
                action=MessageAction(label="سؤال", text="سؤال")
            ),
        ])

    # ===============================
    # Flex Builder
    # ===============================
    def _create_flex(self, title: str, content: str, theme: str):
        c = Config.get_theme(theme)

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["bg"],
                "paddingAll": "20px",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "weight": "bold",
                        "size": "lg",
                        "align": "center",
                        "color": c["primary"]
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": c["border"]
                    },
                    {
                        "type": "text",
                        "text": content,
                        "wrap": True,
                        "size": "md",
                        "color": c["text"],
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": c["border"]
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "البداية",
                            "text": "بداية"
                        },
                        "style": "secondary",
                        "height": "sm",
                        "margin": "md"
                    }
                ]
            }
        }

        return FlexMessage(
            alt_text=title,
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    # ===============================
    # Public API
    # ===============================
    def handle(self, cmd: str, theme: str = "light"):
        if cmd not in self._data:
            return None

        items = self._data.get(cmd)
        if not items:
            return None

        text = random.choice(items)
        logger.info(f"Text command executed: {cmd}")

        return self._create_flex(cmd, text, theme)
