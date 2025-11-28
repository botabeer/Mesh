"""
Bot Mesh - UI Builder v3.2 (UPDATED)
Created by: Abeer Aldosari © 2025

Features:
- نافذة إعلان الفائز مع زر إعادة
- عرض السؤال والإجابة السابقة في كل سؤال
- أزرار ألعاب واضحة
- أزرار ثابتة مفعلة
"""

from linebot.v3.messaging import FlexMessage, FlexContainer
from constants import (
    BOT_NAME, BOT_RIGHTS, THEMES, DEFAULT_THEME,
    GAME_LIST, FIXED_BUTTONS
)


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
        row_themes = theme_list[i:i + 3]
        rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": t, "text": f"ثيم {t}"},
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
    status_color = "#48BB78" if is_registered else "#CBD5E0"

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
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {"type": "text", "text": username, "size": "lg", "weight": "bold"},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": status, "size": "sm", "color": status_color},
                        {"type": "text", "text": f"{points} نقطة", "size": "sm", "align": "end"}
                    ]
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "20px",
            "paddingAll": "20px"
        },
        {"type": "text", "text": "اختر الثيم:", "weight": "bold"}
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
        {"type": "separator", "color": colors["shadow1"]},
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "align": "center"}
    ]

    return FlexMessage(
        alt_text="الرئيسية",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


def build_games_menu(theme="أبيض"):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])

    games = list(GAME_LIST.items())
    game_rows = []

    for i in range(0, len(games), 3):
        row_games = games[i:i + 3]
        game_rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": f"{game[1]['icon']} {game[1]['label']}",
                        "text": game[1]['label']   # ✅ بدون كلمة "لعبة"
                    },
                    "style": "secondary",
                    "height": "sm",
                    "color": colors["primary"]
                }
                for game in row_games
            ]
        })

    contents = [
        {"type": "text", "text": "الألعاب المتاحة", "weight": "bold", "size": "xl", "align": "center"},
        {"type": "separator"}
    ] + game_rows + [
        {"type": "separator"},
        {
            "type": "text",
            "text": "أوامر اللعب: لمح – جاوب – إيقاف",
            "size": "sm",
            "align": "center"
        }
    ]

    footer = [
        create_button_row([
            FIXED_BUTTONS["home"],
            FIXED_BUTTONS["stop"]
        ], colors),
        {"type": "separator"},
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "align": "center"}
    ]

    return FlexMessage(
        alt_text="الألعاب",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


def build_winner_announcement(username, game_name, total_score, final_points, theme="أبيض"):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])

    contents = [
        {"type": "text", "text": "تهانينا", "size": "xxl", "weight": "bold", "align": "center"},
        {"type": "separator"},
        {"type": "text", "text": username, "align": "center"},
        {"type": "text", "text": f"+{total_score} نقاط", "align": "center"},
        {"type": "text", "text": f"الإجمالي: {final_points}", "align": "center"}
    ]

    footer = [
        {
            "type": "button",
            "action": {"type": "message", "label": "إعادة", "text": game_name},
            "style": "primary"
        },
        create_button_row([
            FIXED_BUTTONS["games"],
            FIXED_BUTTONS["home"]
        ], colors),
        {"type": "separator"},
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "align": "center"}
    ]

    return FlexMessage(
        alt_text="فائز",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


def build_help_menu(theme="أبيض"):
    return build_games_menu(theme)


def build_game_stats(theme="أبيض"):
    return build_games_menu(theme)


def build_detailed_game_info(theme="أبيض"):
    return build_games_menu(theme)
