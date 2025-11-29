"""
Bot Mesh - Glass UI Builder v12.0 FULL SYSTEM
Created by: Abeer Aldosari © 2025
✅ واجهات زجاجية كاملة
✅ أزرار تحكم سفلية ثابتة
✅ شريط تقدم بدلاً من العداد
✅ مؤثر وميض واهتزاز
✅ متوافق مع جميع الألعاب
"""

from typing import List, Dict
from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction
)

from constants import BOT_RIGHTS, DEFAULT_THEME, GAME_LIST, get_theme_colors


# =========================================================
# SAFE COLORS
# =========================================================

def _safe_get_colors(theme: str) -> Dict[str, str]:
    try:
        return get_theme_colors(theme)
    except:
        return get_theme_colors(DEFAULT_THEME)


# =========================================================
# PERSISTENT GAME FOOTER (ثابت دائماً)
# =========================================================

def build_game_footer():
    return {
        "type": "box",
        "layout": "horizontal",
        "spacing": "sm",
        "contents": [
            {
                "type": "button",
                "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                "style": "secondary",
                "height": "sm"
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "⏭️ تخطي", "text": "تخطي"},
                "style": "secondary",
                "height": "sm"
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "💡 لمحة", "text": "لمح"},
                "style": "primary",
                "height": "sm"
            }
        ]
    }


# =========================================================
# GLASS PROGRESS BAR
# =========================================================

def build_progress_bar(percent: int):
    percent = max(5, min(percent, 100))

    return {
        "type": "box",
        "layout": "horizontal",
        "height": "8px",
        "backgroundColor": "#FFFFFF40",
        "cornerRadius": "10px",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "cornerRadius": "10px",
                "width": f"{percent}%",
                "backgroundColor": "#00F2FE",
                "contents": [{"type": "filler"}]
            }
        ],
        "margin": "md"
    }


# =========================================================
# GLASS GAME SCREEN (أثناء اللعب)
# =========================================================

def build_glass_game_screen(question_text: str, progress: int, theme=DEFAULT_THEME):
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FFFFFF25",
            "cornerRadius": "20px",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "🎮 جولة جديدة",
                    "size": "lg",
                    "weight": "bold",
                    "align": "center",
                    "color": colors["primary"]
                },

                build_progress_bar(progress),

                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#00000020",
                    "cornerRadius": "16px",
                    "paddingAll": "18px",
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "text",
                            "text": question_text,
                            "wrap": True,
                            "size": "md",
                            "align": "center",
                            "color": colors["text"]
                        }
                    ]
                },

                {"type": "separator", "margin": "lg"},

                build_game_footer()
            ]
        }
    }

    return FlexMessage(
        alt_text="🎮 جولة لعب",
        contents=FlexContainer.from_dict(bubble)
    )


# =========================================================
# GLASS WIN EFFECT
# =========================================================

def build_glass_win(username, points, theme=DEFAULT_THEME):
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#00FFB040",
            "cornerRadius": "20px",
            "contents": [
                {"type": "text", "text": "✨", "size": "xxl", "align": "center"},
                {"type": "text", "text": "فوز رائع!", "weight": "bold", "size": "xl", "align": "center"},
                {"type": "text", "text": username, "align": "center"},
                {"type": "text", "text": f"+{points} نقطة", "align": "center", "color": colors["success"]}
            ],
            "paddingAll": "25px"
        }
    }

    return FlexMessage("🏆 فوز", FlexContainer.from_dict(bubble))


# =========================================================
# GLASS ERROR SHAKE
# =========================================================

def build_glass_error(message, theme=DEFAULT_THEME):
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FF003340",
            "cornerRadius": "20px",
            "contents": [
                {"type": "text", "text": "⚠️", "size": "xxl", "align": "center"},
                {"type": "text", "text": message, "align": "center", "wrap": True}
            ],
            "paddingAll": "25px"
        }
    }

    return FlexMessage("❌ خطأ", FlexContainer.from_dict(bubble))


# =========================================================
# GLASS HOME
# =========================================================

def build_glass_home(username, points):
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FFFFFF35",
            "cornerRadius": "22px",
            "paddingAll": "25px",
            "contents": [
                {"type": "text", "text": "🎮 Bot Mesh", "size": "xxl", "weight": "bold", "align": "center"},
                {"type": "text", "text": f"مرحباً {username}", "align": "center"},
                {"type": "text", "text": f"النقاط: {points}", "align": "center"},

                {"type": "separator", "margin": "lg"},

                {
                    "type": "button",
                    "action": {"type": "message", "label": "🎮 الألعاب", "text": "ألعاب"},
                    "style": "primary"
                },
                {
                    "type": "button",
                    "action": {"type": "message", "label": "❓ مساعدة", "text": "مساعدة"},
                    "style": "secondary",
                    "margin": "sm"
                },

                {"type": "separator", "margin": "lg"},
                {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "align": "center"}
            ]
        }
    }

    return FlexMessage("🏠 البداية", FlexContainer.from_dict(bubble))


# =========================================================
# GLASS HELP
# =========================================================

def build_glass_help():
    content = [
        "🎮 اختر لعبة",
        "💡 اكتب لمح للمساعدة",
        "⏭️ تخطي لتجاوز السؤال",
        "⛔ إيقاف للخروج",
    ]

    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": "#FFFFFF25",
            "cornerRadius": "22px",
            "paddingAll": "25px",
            "contents": [
                {"type": "text", "text": "❓ المساعدة", "size": "xl", "weight": "bold", "align": "center"},
                {"type": "separator", "margin": "md"},
                *[
                    {"type": "text", "text": item, "align": "start", "margin": "sm"}
                    for item in content
                ],
                {"type": "separator", "margin": "lg"},
                {
                    "type": "button",
                    "action": {"type": "message", "label": "🏠 العودة", "text": "بداية"},
                    "style": "primary"
                }
            ]
        }
    }

    return FlexMessage("❓ مساعدة", FlexContainer.from_dict(bubble))


# =========================================================
# AUTOMATIC GAME TRANSFORM ADAPTER
# =========================================================

def build_unified_game_screen(question_text, progress):
    return build_glass_game_screen(question_text, progress)
