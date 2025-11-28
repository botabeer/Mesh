"""
Bot Mesh - UI Builder v3.2
Created by: Abeer Aldosari © 2025

Features:
- نافذة إعلان الفائز مع زر إعادة
- عرض السؤال والإجابة السابقة في كل سؤال
"""

from linebot.v3.messaging import FlexMessage, FlexContainer
from constants import (
    BOT_NAME, BOT_RIGHTS, THEMES, DEFAULT_THEME,
    FIXED_BUTTONS
)

# ✅ قائمة الألعاب النهائية الواضحة المرتبة
GAME_LIST_ORDERED = [
    "أسرع",
    "ذكاء",
    "لعبة",
    "أغنية",
    "خمن",
    "سلسلة",
    "ترتيب",
    "تكوين",
    "ضد",
    "لون",
    "رياضيات",
    "توافق"
]


def create_neumorphic_card(colors, contents, footer_contents=None):
    card = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xl",
            "contents": contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    if footer_contents:
        card["footer"] = {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        }
    return card


def create_button_row(buttons, colors, style="secondary"):
    return {
        "type": "box",
        "layout": "horizontal",
        "spacing": "sm",
        "contents": [
            {
                "type": "button",
                "action": {"type": "message", "label": btn["label"], "text": btn["text"]},
                "style": "primary" if style == "primary" else "secondary",
                "height": "sm",
                "color": colors["button"] if style == "primary" else colors["shadow1"]
            }
            for btn in buttons
        ]
    }


def create_theme_selector(current_theme, colors):
    theme_list = list(THEMES.keys())
    rows = []
    for i in range(0, len(theme_list), 3):
        row_themes = theme_list[i:i+3]
        rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": f"{t}", "text": f"ثيم {t}"},
                    "style": "primary" if t == current_theme else "secondary",
                    "height": "sm",
                    "color": colors["primary"] if t == current_theme else colors["shadow1"]
                }
                for t in row_themes
            ]
        })
    return rows


def build_home(theme="أبيض", username="مستخدم", points=0, is_registered=False):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    status = "مسجل" if is_registered else "غير مسجل"
    theme_rows = create_theme_selector(theme, colors)

    contents = [
        {
            "type": "text",
            "text": BOT_NAME,
            "weight": "bold",
            "size": "xxl",
            "color": colors["primary"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": f"{username} | {points} نقطة | {status}",
            "size": "sm",
            "align": "center",
            "color": colors["text"]
        },
        {
            "type": "text",
            "text": "اختر الثيم:",
            "size": "md",
            "weight": "bold",
            "color": colors["text"]
        }
    ] + theme_rows

    footer = [
        create_button_row([
            {"label": "انضم", "text": "انضم"} if not is_registered else {"label": "انسحب", "text": "انسحب"},
            FIXED_BUTTONS["games"]
        ], colors),
        create_button_row([
            FIXED_BUTTONS["points"],
            FIXED_BUTTONS["leaderboard"]
        ], colors),
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "align": "center"
        }
    ]

    return FlexMessage(
        alt_text="البداية",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


def build_games_menu(theme="أبيض"):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])

    game_rows = []
    for i in range(0, len(GAME_LIST_ORDERED), 3):
        row_games = GAME_LIST_ORDERED[i:i+3]
        game_rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": game,
                        "text": game
                    },
                    "style": "secondary",
                    "height": "sm",
                    "color": colors["primary"]
                }
                for game in row_games
            ]
        })

    contents = [
        {
            "type": "text",
            "text": "الألعاب المتاحة",
            "weight": "bold",
            "size": "xl",
            "color": colors["primary"],
            "align": "center"
        },
        {
            "type": "text",
            "text": f"عدد الألعاب: {len(GAME_LIST_ORDERED)}",
            "size": "sm",
            "align": "center"
        }
    ] + game_rows + [
        {
            "type": "text",
            "text": "الأوامر أثناء اللعب:\nلمح – جاوب – إيقاف",
            "size": "xs",
            "align": "center",
            "wrap": True
        }
    ]

    footer = [
        create_button_row([
            FIXED_BUTTONS["home"],
            FIXED_BUTTONS["stop"]
        ], colors),
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "align": "center"
        }
    ]

    return FlexMessage(
        alt_text="الألعاب",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


def build_winner_announcement(username, game_name, total_score, final_points, theme="أبيض"):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])

    contents = [
        {"type": "text", "text": "تهانينا", "size": "xxl", "weight": "bold", "align": "center"},
        {"type": "text", "text": f"{username}", "align": "center"},
        {"type": "text", "text": f"أنهيت لعبة {game_name}", "align": "center"},
        {"type": "text", "text": f"+{total_score} نقاط", "align": "center"},
        {"type": "text", "text": f"الإجمالي: {final_points}", "align": "center"}
    ]

    footer = [
        {
            "type": "button",
            "action": {
                "type": "message",
                "label": "إعادة نفس اللعبة",
                "text": f"إعادة {game_name}"
            },
            "style": "primary",
            "height": "sm",
            "color": colors["primary"]
        },
        create_button_row([
            FIXED_BUTTONS["games"],
            FIXED_BUTTONS["home"]
        ], colors)
    ]

    return FlexMessage(
        alt_text="الفائز",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


# Dummy aliases
def build_help_menu(theme="أبيض"):
    return build_games_menu(theme)

def build_game_stats(theme="أبيض"):
    return build_games_menu(theme)

def build_detailed_game_info(theme="أبيض"):
    return build_games_menu(theme)
