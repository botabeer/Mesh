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
    GAME_LIST, FIXED_BUTTONS
)


def create_neumorphic_card(colors, contents, footer_contents=None):
    """Create a neumorphic card with soft 3D shadows"""
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
    """Create horizontal button row with neumorphic style"""
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
    """Create theme selector with 3 themes per row"""
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
    """Build home window with neumorphic design"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    status = "✅ مسجل" if is_registered else "⚪ غير مسجل"
    status_color = "#48BB78" if is_registered else "#CBD5E0"
    
    # Theme selector rows
    theme_rows = create_theme_selector(theme, colors)
    
    contents = [
        # Header
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"🎮 {BOT_NAME}",
                    "weight": "bold",
                    "size": "xxl",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "بوت الألعاب الترفيهية الذكي",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center"
                }
            ],
            "spacing": "xs"
        },
        {"type": "separator", "color": colors["shadow1"]},
        
        # User Info Card
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": f"👤 {username}",
                    "size": "lg",
                    "color": colors["text"],
                    "weight": "bold"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": status,
                            "size": "sm",
                            "color": status_color,
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"⭐ {points} نقطة",
                            "size": "sm",
                            "color": colors["primary"],
                            "align": "end"
                        }
                    ]
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "20px",
            "paddingAll": "20px"
        },
        
        # Theme Selector
        {
            "type": "text",
            "text": "🎨 اختر ثيمك المفضل:",
            "size": "md",
            "weight": "bold",
            "color": colors["text"]
        }
    ] + theme_rows
    
    # Footer with fixed buttons
    footer = [
        create_button_row([
            {"label": "📝 انضم", "text": "انضم"} if not is_registered else {"label": "🚪 انسحب", "text": "انسحب"},
            FIXED_BUTTONS["games"]
        ], colors),
        create_button_row([
            FIXED_BUTTONS["points"],
            FIXED_BUTTONS["leaderboard"]
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
    
    card = create_neumorphic_card(colors, contents, footer)
    return FlexMessage(alt_text=f"{BOT_NAME} - البداية", contents=FlexContainer.from_dict(card))


def build_games_menu(theme="أبيض"):
    """Build games menu with all 12 games"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # Create game buttons (3 per row)
    games = list(GAME_LIST.items())
    game_rows = []
    
    for i in range(0, len(games), 3):
        row_games = games[i:i+3]
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
                        "text": f"لعبة {game[0]}"
                    },
                    "style": "secondary",
                    "height": "sm",
                    "color": colors["primary"]
                }
                for game in row_games
            ]
        })
    
    contents = [
        # Header
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
            "text": f"اختر من {len(GAME_LIST)} لعبة مختلفة",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"]}
    ] + game_rows + [
        {"type": "separator", "color": colors["shadow1"]},
        
        # Game Instructions
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
                {
                    "type": "text",
                    "text": "💡 الأوامر أثناء اللعب:",
                    "size": "sm",
                    "color": colors["text"],
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "• لمح - للحصول على تلميح\n• جاوب - لكشف الإجابة\n• إيقاف - لإنهاء اللعبة",
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
    
    # Footer
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
    
    card = create_neumorphic_card(colors, contents, footer)
    return FlexMessage(alt_text=f"{BOT_NAME} - الألعاب", contents=FlexContainer.from_dict(card))


def build_my_points(username, points, user_game_stats=None, theme="أبيض"):
    """Build my points window with level system"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # Determine level based on points
    if points < 50:
        level = "🌱 مبتدئ"
        level_color = "#48BB78"
    elif points < 150:
        level = "⭐ متوسط"
        level_color = "#667EEA"
    elif points < 300:
        level = "🔥 متقدم"
        level_color = "#DD6B20"
    else:
        level = "👑 محترف"
        level_color = "#D53F8C"
    
    contents = [
        # Header
        {
            "type": "text",
            "text": "⭐ نقاطي",
            "weight": "bold",
            "size": "xl",
            "color": colors["primary"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"]},
        
        # User Info
        {
            "type": "text",
            "text": f"👤 {username}",
            "size": "lg",
            "color": colors["text"],
            "weight": "bold",
            "align": "center"
        },
        
        # Points Card
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "النقاط الكلية",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"{points}",
                    "size": "xxl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center"
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "20px",
            "paddingAll": "25px"
        },
        
        # Level Card
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": "المستوى الحالي",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": level,
                    "size": "lg",
                    "weight": "bold",
                    "color": level_color,
                    "align": "center"
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "15px"
        },
        
        {"type": "separator", "color": colors["shadow1"]},
        
        # Warning
        {
            "type": "text",
            "text": "⚠️ سيتم حذف بياناتك بعد 7 أيام من عدم النشاط",
            "size": "xs",
            "color": "#FF5555",
            "wrap": True,
            "align": "center"
        }
    ]
    
    # Footer
    footer = [
        create_button_row([
            FIXED_BUTTONS["home"],
            FIXED_BUTTONS["games"]
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
    
    card = create_neumorphic_card(colors, contents, footer)
    return FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(card))


def build_leaderboard(top_users, theme="أبيض"):
    """Build leaderboard window"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    leaderboard_contents = []
    medals = ["🥇", "🥈", "🥉"]
    
    for i, (name, points) in enumerate(top_users[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        medal_color = colors["primary"] if i <= 3 else colors["text"]
        
        leaderboard_contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": medal,
                    "size": "lg",
                    "flex": 0,
                    "color": medal_color
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
                    "align": "end",
                    "flex": 1
                }
            ],
            "spacing": "md",
            "paddingAll": "sm"
        })
    
    if not leaderboard_contents:
        leaderboard_contents.append({
            "type": "text",
            "text": "لا يوجد لاعبين مسجلين بعد",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        })
    
    contents = [
        # Header
        {
            "type": "text",
            "text": "🏆 لوحة الصدارة",
            "weight": "bold",
            "size": "xl",
            "color": colors["primary"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"]},
        
        # Leaderboard List
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": leaderboard_contents,
            "backgroundColor": colors["card"],
            "cornerRadius": "20px",
            "paddingAll": "20px"
        }
    ]
    
    # Footer
    footer = [
        create_button_row([
            FIXED_BUTTONS["home"],
            FIXED_BUTTONS["points"]
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
    
    card = create_neumorphic_card(colors, contents, footer)
    return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(card))


def build_registration_required(theme="أبيض"):
    """Build registration required message"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    contents = [
        {
            "type": "text",
            "text": "⚠️ يجب التسجيل أولاً",
            "weight": "bold",
            "size": "lg",
            "color": colors["primary"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": "اضغط 'انضم' للتسجيل والبدء باللعب",
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "wrap": True
        }
    ]
    
    footer = [
        create_button_row([
            {"label": "📝 انضم", "text": "انضم"},
            FIXED_BUTTONS["home"]
        ], colors)
    ]
    
    card = create_neumorphic_card(colors, contents, footer)
    return FlexMessage(alt_text="تسجيل مطلوب", contents=FlexContainer.from_dict(card))


def build_winner_announcement(username, game_name, total_score, final_points, theme="أبيض"):
    """Build winner announcement window with replay button"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    contents = [
        # Celebration Header
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎉",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "تهانينا!",
                    "size": "xxl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"أنهيت لعبة {game_name}",
                    "size": "md",
                    "color": colors["text2"],
                    "align": "center"
                }
            ],
            "spacing": "sm"
        },
        
        {"type": "separator", "color": colors["shadow1"]},
        
        # Player Info
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"👤 {username}",
                    "size": "lg",
                    "weight": "bold",
                    "color": colors["text"],
                    "align": "center"
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "15px"
        },
        
        # Score Card
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "النقاط المكتسبة",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"+{total_score}",
                    "size": "xxl",
                    "weight": "bold",
                    "color": colors["success"],
                    "align": "center"
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "20px",
            "paddingAll": "25px"
        },
        
        # Total Points
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "⭐ إجمالي النقاط:",
                    "size": "md",
                    "color": colors["text"],
                    "flex": 2
                },
                {
                    "type": "text",
                    "text": f"{final_points}",
                    "size": "md",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "end",
                    "flex": 1
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "15px"
        }
    ]
    
    # Footer with Replay Button
    footer = [
        {
            "type": "button",
            "action": {
                "type": "message",
                "label": "🔄 إعادة نفس اللعبة",
                "text": f"إعادة {game_name}"
            },
            "style": "primary",
            "height": "sm",
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
    
    card = create_neumorphic_card(colors, contents, footer)
    return FlexMessage(alt_text="🎉 تهانينا!", contents=FlexContainer.from_dict(card))


# Dummy functions to satisfy imports (not used)
def build_help_menu(theme="أبيض"):
    """Alias for build_games_menu"""
    return build_games_menu(theme)


def build_game_stats(theme="أبيض"):
    """Placeholder for game stats"""
    return build_games_menu(theme)


def build_detailed_game_info(theme="أبيض"):
    """Placeholder for detailed game info"""
    return build_games_menu(theme)
