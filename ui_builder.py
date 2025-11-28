"""
Bot Mesh - UI Builder v6.0
Created by: Abeer Aldosari © 2025

✅ Glassmorphism + Soft Neumorphism Style
✅ Quick Reply: Games Only (Permanent)
✅ Fixed: Import Issues
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from constants import (
    BOT_NAME, BOT_RIGHTS, THEMES, DEFAULT_THEME,
    GAME_LIST, FIXED_BUTTONS
)


def create_neumorphic_card(colors, contents, footer_contents=None):
    """Create Glassmorphism card with soft neumorphism"""
    card = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
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
    """Create horizontal button row"""
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
    """Create theme selection buttons"""
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
    """Build home screen"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    status = "✅ مسجل" if is_registered else "⚪ غير مسجل"
    
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
                {
                    "type": "text",
                    "text": username,
                    "size": "lg",
                    "weight": "bold",
                    "color": colors["text"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"{points} نقطة | {status}",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center"
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "20px",
            "paddingAll": "20px",
            "margin": "md"
        },
        {
            "type": "text",
            "text": "🎨 اختر الثيم:",
            "weight": "bold",
            "size": "md",
            "color": colors["text"],
            "margin": "lg"
        }
    ] + theme_rows
    
    footer = [
        create_button_row([
            {"label": "✅ انضم", "text": "انضم"} if not is_registered else {"label": "❌ انسحب", "text": "انسحب"},
            FIXED_BUTTONS["games"]
        ], colors),
        create_button_row([
            FIXED_BUTTONS["points"],
            FIXED_BUTTONS["leaderboard"]
        ], colors),
        create_button_row([
            FIXED_BUTTONS["achievements"],
            FIXED_BUTTONS["help"]
        ], colors),
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return FlexMessage(
        alt_text="البداية",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


def build_games_menu(theme="أبيض"):
    """Build games menu with Quick Reply buttons for games only"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # Games ordered list
    games_ordered = [
        "أسرع", "ذكاء", "لعبة", "أغنية", "خمن", "سلسلة",
        "ترتيب", "تكوين", "ضد", "لون", "رياضيات", "توافق"
    ]
    
    game_rows = []
    for i in range(0, len(games_ordered), 3):
        row_games = games_ordered[i:i+3]
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
            "text": "🎮 الألعاب المتاحة",
            "weight": "bold",
            "size": "xl",
            "color": colors["primary"],
            "align": "center"
        },
        {
            "type": "text",
            "text": f"عدد الألعاب: {len(games_ordered)}",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"], "margin": "md"}
    ] + game_rows + [
        {"type": "separator", "color": colors["shadow1"], "margin": "md"},
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
                {
                    "type": "text",
                    "text": "💡 أوامر اللعب:",
                    "size": "sm",
                    "weight": "bold",
                    "color": colors["text"]
                },
                {
                    "type": "text",
                    "text": "• اضغط على اسم اللعبة لبدء اللعب\n• اكتب 'لمح' للتلميح\n• اكتب 'جاوب' لكشف الإجابة\n• اكتب 'إيقاف' لإنهاء اللعبة",
                    "size": "xs",
                    "color": colors["text2"],
                    "wrap": True
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "15px"
        }
    ]
    
    footer = [
        create_button_row([
            FIXED_BUTTONS["home"],
            FIXED_BUTTONS["stop"]
        ], colors),
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return FlexMessage(
        alt_text="الألعاب",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


def build_my_points(username, points, game_stats, theme="أبيض"):
    """Build my points screen"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    total_games = sum(game_stats.values())
    
    stats_rows = []
    for game_name, plays in sorted(game_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
        stats_rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": game_name,
                    "size": "sm",
                    "color": colors["text"],
                    "flex": 3
                },
                {
                    "type": "text",
                    "text": f"{plays} مرة",
                    "size": "sm",
                    "color": colors["primary"],
                    "align": "end",
                    "flex": 1
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "10px",
            "margin": "sm"
        })
    
    contents = [
        {
            "type": "text",
            "text": "⭐ نقاطي",
            "weight": "bold",
            "size": "xl",
            "color": colors["primary"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": username,
                    "size": "lg",
                    "weight": "bold",
                    "color": colors["text"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"{points} نقطة",
                    "size": "xxl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"عدد الألعاب: {total_games}",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center"
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "20px",
            "paddingAll": "25px",
            "margin": "md"
        },
        {
            "type": "text",
            "text": "🎮 أكثر الألعاب لعباً:",
            "weight": "bold",
            "size": "md",
            "color": colors["text"],
            "margin": "lg"
        }
    ] + (stats_rows if stats_rows else [{
        "type": "text",
        "text": "لم تلعب أي لعبة بعد",
        "size": "sm",
        "color": colors["text2"],
        "align": "center"
    }])
    
    footer = [
        create_button_row([
            FIXED_BUTTONS["leaderboard"],
            FIXED_BUTTONS["achievements"]
        ], colors),
        create_button_row([
            FIXED_BUTTONS["games"],
            FIXED_BUTTONS["home"]
        ], colors),
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return FlexMessage(
        alt_text="نقاطي",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


def build_leaderboard(leaderboard, theme="أبيض"):
    """Build leaderboard screen"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    rank_emojis = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    
    leaderboard_rows = []
    for i, (name, points) in enumerate(leaderboard):
        leaderboard_rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": f"{rank_emojis[i]} {i+1}",
                    "size": "sm",
                    "color": colors["text"],
                    "flex": 1
                },
                {
                    "type": "text",
                    "text": name,
                    "size": "sm",
                    "color": colors["text"],
                    "flex": 3
                },
                {
                    "type": "text",
                    "text": f"{points}",
                    "size": "sm",
                    "color": colors["primary"],
                    "weight": "bold",
                    "align": "end",
                    "flex": 1
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "12px",
            "margin": "sm"
        })
    
    contents = [
        {
            "type": "text",
            "text": "🏆 الصدارة",
            "weight": "bold",
            "size": "xl",
            "color": colors["primary"],
            "align": "center"
        },
        {
            "type": "text",
            "text": f"أفضل {len(leaderboard)} لاعبين",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"], "margin": "md"}
    ] + (leaderboard_rows if leaderboard_rows else [{
        "type": "text",
        "text": "لا يوجد لاعبين مسجلين بعد",
        "size": "sm",
        "color": colors["text2"],
        "align": "center"
    }])
    
    footer = [
        create_button_row([
            FIXED_BUTTONS["points"],
            FIXED_BUTTONS["achievements"]
        ], colors),
        create_button_row([
            FIXED_BUTTONS["games"],
            FIXED_BUTTONS["home"]
        ], colors),
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return FlexMessage(
        alt_text="الصدارة",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


def build_registration_required(theme="أبيض"):
    """Build registration required screen"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    contents = [
        {
            "type": "text",
            "text": "⚠️ تسجيل مطلوب",
            "weight": "bold",
            "size": "xl",
            "color": colors["error"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "يجب التسجيل أولاً للعب الألعاب وكسب النقاط!",
                    "size": "md",
                    "color": colors["text"],
                    "wrap": True,
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "✅ احصل على نقاط\n🏆 شارك في الصدارة\n🎖️ افتح الإنجازات",
                    "size": "sm",
                    "color": colors["text2"],
                    "wrap": True,
                    "align": "center"
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "20px",
            "paddingAll": "25px",
            "margin": "md"
        }
    ]
    
    footer = [
        {
            "type": "button",
            "action": {"type": "message", "label": "✅ انضم الآن", "text": "انضم"},
            "style": "primary",
            "height": "md",
            "color": colors["success"]
        },
        create_button_row([
            FIXED_BUTTONS["home"]
        ], colors),
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return FlexMessage(
        alt_text="تسجيل مطلوب",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


def build_winner_announcement(username, game_name, total_score, final_points, theme="أبيض"):
    """Build winner announcement with replay button"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    contents = [
        {
            "type": "text",
            "text": "🎉 تهانينا!",
            "size": "xxl",
            "weight": "bold",
            "color": colors["success"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": username,
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["text"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"أنهيت لعبة {game_name}",
                    "size": "md",
                    "color": colors["text2"],
                    "align": "center",
                    "wrap": True
                },
                {"type": "separator", "color": colors["shadow1"]},
                {
                    "type": "text",
                    "text": f"+{total_score} نقاط",
                    "size": "xxl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"الإجمالي: {final_points} نقطة",
                    "size": "md",
                    "color": colors["text2"],
                    "align": "center"
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "20px",
            "paddingAll": "25px",
            "margin": "md"
        }
    ]
    
    footer = [
        {
            "type": "button",
            "action": {
                "type": "message",
                "label": "🔄 إعادة نفس اللعبة",
                "text": f"إعادة {game_name}"
            },
            "style": "primary",
            "height": "md",
            "color": colors["primary"]
        },
        create_button_row([
            FIXED_BUTTONS["games"],
            FIXED_BUTTONS["home"]
        ], colors),
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return FlexMessage(
        alt_text="الفائز",
        contents=FlexContainer.from_dict(create_neumorphic_card(colors, contents, footer))
    )


# Dummy aliases for compatibility
def build_help_menu(theme="أبيض"):
    return build_games_menu(theme)

def build_game_stats(theme="أبيض"):
    return build_games_menu(theme)

def build_detailed_game_info(theme="أبيض"):
    return build_games_menu(theme)
