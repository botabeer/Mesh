# -*- coding: utf-8 -*-
"""
Bot Mesh - Theme & UI Styles
Created by: Abeer Aldosari © 2025
"""

from linebot.v3.messaging import TextMessage, FlexMessage, FlexContainer

# ===================== ثيمات البوت =====================
THEMES = {
    "💜": {
        "bg": "#F3E8FF",
        "card": "#FAF5FF",
        "primary": "#9F7AEA",
        "text": "#44337A",
        "text2": "#6B46C1"
    },
    "💚": {
        "bg": "#E6FFFA",
        "card": "#F0FFF4",
        "primary": "#38B2AC",
        "text": "#234E52",
        "text2": "#2C7A7B"
    },
    "🤍": {
        "bg": "#F8F9FA",
        "card": "#FFFFFF",
        "primary": "#667EEA",
        "text": "#2D3748",
        "text2": "#718096"
    },
    "🖤": {
        "bg": "#1A202C",
        "card": "#2D3748",
        "primary": "#667EEA",
        "text": "#E2E8F0",
        "text2": "#CBD5E0"
    },
    "💙": {
        "bg": "#EBF8FF",
        "card": "#BEE3F8",
        "primary": "#3182CE",
        "text": "#2C5282",
        "text2": "#2B6CB0"
    },
    "🩶": {
        "bg": "#F7FAFC",
        "card": "#EDF2F7",
        "primary": "#718096",
        "text": "#2D3748",
        "text2": "#4A5568"
    },
    "🩷": {
        "bg": "#FFF5F7",
        "card": "#FED7E2",
        "primary": "#D53F8C",
        "text": "#702459",
        "text2": "#97266D"
    },
    "🧡": {
        "bg": "#FFFAF0",
        "card": "#FEEBC8",
        "primary": "#DD6B20",
        "text": "#7C2D12",
        "text2": "#C05621"
    },
    "🤎": {
        "bg": "#F7F3EF",
        "card": "#EDE0D4",
        "primary": "#8B4513",
        "text": "#5C2E00",
        "text2": "#7A4F1D"
    }
}

DEFAULT_THEME = "💜"

# ===================== الأزرار الثابتة =====================
FIXED_BUTTONS = {
    "home": "Home",
    "games": "Games",
    "info": "Info",
    "stop": "إيقاف"
}

# ===================== Flex Builders =====================
class UIBuilder:
    """بناء الرسائل والواجهات Flex Messages"""

    @staticmethod
    def build_home(theme, username, points, is_registered):
        colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
        content = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {"type": "text", "text": f"مرحباً {username}", "size": "lg", "weight": "bold", "color": colors["primary"], "align": "center"},
                    {"type": "text", "text": f"نقاطك: {points}", "size": "md", "color": colors["text"], "align": "center"},
                    {"type": "text", "text": "اختر لعبة أو زر من الأسفل", "size": "sm", "color": colors["text2"], "align": "center"}
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "20px"
            }
        }
        return FlexMessage(alt_text="Home", contents=FlexContainer.from_dict(content))

    @staticmethod
    def build_games_menu(theme):
        colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
        content = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {"type": "text", "text": "🎮 قائمة الألعاب", "size": "lg", "weight": "bold", "color": colors["primary"], "align": "center"},
                    {"type": "text", "text": "اختر اللعبة التي تريدها من القائمة", "size": "sm", "color": colors["text2"], "align": "center"}
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "20px"
            }
        }
        return FlexMessage(alt_text="Games Menu", contents=FlexContainer.from_dict(content))

    @staticmethod
    def build_info(theme):
        colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
        content = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "ℹ️ معلومات البوت", "size": "lg", "weight": "bold", "color": colors["primary"], "align": "center"},
                    {"type": "text", "text": "تم تطوير البوت بواسطة عبير الدوسري\n© 2025", "size": "sm", "color": colors["text2"], "align": "center"}
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "20px"
            }
        }
        return FlexMessage(alt_text="Info", contents=FlexContainer.from_dict(content))

    @staticmethod
    def build_my_points(username, points, theme):
        colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
        return TextMessage(text=f"🏅 {username}, لديك {points} نقطة")

    @staticmethod
    def build_leaderboard(sorted_users, theme):
        colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
        text = "🏆 الصدارة:\n" + "\n".join([f"{i+1}. {name}: {pts}" for i, (name, pts) in enumerate(sorted_users)])
        return TextMessage(text=text)
