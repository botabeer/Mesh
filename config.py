import os
import re
from dotenv import load_dotenv

load_dotenv()


class Config:
    LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    DB_PATH = os.getenv("DB_PATH", "botmesh.db")
    PORT = int(os.getenv("PORT", 5000))
    WORKERS = int(os.getenv("WORKERS", 4))
    ENV = os.getenv("ENV", "production")

    QUESTIONS_PER_GAME = 5
    MAX_NAME_LENGTH = 50
    MIN_NAME_LENGTH = 2

    DAILY_REWARD_POINTS = 10
    DAILY_REWARD_HOURS = 24
    INACTIVE_DAYS = 30

    ACHIEVEMENTS = {
        "first_game": {
            "name": "اللعبة الاولى",
            "desc": "اكمل اول لعبة",
            "points": 5
        },
        "ten_games": {
            "name": "محترف",
            "desc": "اكمل 10 العاب",
            "points": 20
        },
        "fifty_games": {
            "name": "خبير",
            "desc": "اكمل 50 لعبة",
            "points": 50
        },
        "hundred_games": {
            "name": "اسطورة",
            "desc": "اكمل 100 لعبة",
            "points": 100
        },
        "first_win": {
            "name": "الفوز الاول",
            "desc": "احصل على فوز مثالي",
            "points": 10
        },
        "ten_wins": {
            "name": "فائز متميز",
            "desc": "احصل على 10 انتصارات",
            "points": 30
        },
        "hundred_points": {
            "name": "جامع النقاط",
            "desc": "اجمع 100 نقطة",
            "points": 25
        },
        "streak_3": {
            "name": "سلسلة قوية",
            "desc": "فز ب 3 العاب متتالية",
            "points": 15
        },
        "streak_5": {
            "name": "سلسلة ذهبية",
            "desc": "فز ب 5 العاب متتالية",
            "points": 35
        },
        "all_games": {
            "name": "المستكشف",
            "desc": "جرب جميع الالعاب",
            "points": 40
        }
    }

    @staticmethod
    def normalize(text):
        if not text:
            return ""

        # إزالة التشكيل
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)

        # توحيد الحروف
        replacements = {
            "أ": "ا",
            "إ": "ا",
            "آ": "ا",
            "ى": "ي",
            "ة": "ه",
            "ؤ": "و",
            "ئ": "ي"
        }
        for old, new in replacements.items():
            text = text.replace(old, new)

        # إزالة الرموز
        text = re.sub(r"[^\w\sء-ي]", "", text)

        return text.strip().lower()

    @staticmethod
    def get_theme(theme):
        # ثيم بدون خلفية زرقاء وكل الازرار نفس اللون
        if theme == "dark":
            return {
                "bg": "#0F0F0F",

                "card": "#1C1C1C",
                "card_secondary": "#262626",

                "text": "#FFFFFF",
                "text_secondary": "#CFCFCF",
                "text_tertiary": "#9A9A9A",

                "border": "#2F2F2F",

                "primary": "#FFFFFF",

                # جميع الازرار نفس اللون
                "button_primary": "#E5E5E5",
                "button_secondary": "#E5E5E5",
                "button_text": "#000000"
            }

        else:
            return {
                "bg": "#FFFFFF",

                "card": "#F2F2F2",
                "card_secondary": "#EAEAEA",

                "text": "#111111",
                "text_secondary": "#555555",
                "text_tertiary": "#888888",

                "border": "#DDDDDD",

                "primary": "#111111",

                # جميع الازرار نفس اللون
                "button_primary": "#E3E3E3",
                "button_secondary": "#E3E3E3",
                "button_text": "#111111"
            }
