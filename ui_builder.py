"""
Bot Mesh - Enhanced UI Builder v5.0
Created by: Abeer Aldosari © 2025

التحسينات:
✅ نصوص مختصرة وواضحة
✅ أزرار ثابتة محسّنة
✅ تصميم موحد
✅ ألوان متناسقة
"""

from linebot.v3.messaging import FlexMessage, FlexContainer
from constants import (
    BOT_NAME, BOT_RIGHTS, THEMES, DEFAULT_THEME, GAME_LIST
)


def build_home(theme="💜", username="مستخدم", points=0, is_registered=False):
    """بناء الصفحة الرئيسية المحسّنة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    status = "✅ مسجل" if is_registered else "⚪ غير مسجل"
    status_color = colors["success"] if is_registered else colors["text2"]
    
    # بطاقة المستخدم
    user_card = {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {
                "type": "text",
                "text": f"👤 {username}",
                "size": "xl",
                "color": colors["text"],
                "weight": "bold",
                "align": "center"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": status,
                        "size": "xs",
                        "color": status_color,
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"⭐ {points} نقطة",
                        "size": "xs",
                        "color": colors["primary"],
                        "align": "end",
                        "flex": 1
                    }
                ]
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "15px",
        "paddingAll": "15px"
    }
    
    # محدد الثيمات (صف واحد)
    theme_list = list(THEMES.keys())
    theme_row1 = theme_list[:5]
    theme_row2 = theme_list[5:]
    
    theme_buttons_row1 = {
        "type": "box",
        "layout": "horizontal",
        "spacing": "xs",
        "contents": [
            {
                "type": "button",
                "action": {"type": "message", "label": t, "text": f"ثيم {t}"},
                "style": "primary" if t == theme else "secondary",
                "height": "sm",
                "color": colors["primary"] if t == theme else None
            }
            for t in theme_row1
        ]
    }
    
    theme_buttons_row2 = {
        "type": "box",
        "layout": "horizontal",
        "spacing": "xs",
        "contents": [
            {
                "type": "button",
                "action": {"type": "message", "label": t, "text": f"ثيم {t}"},
                "style": "primary" if t == theme else "secondary",
                "height": "sm",
                "color": colors["primary"] if t == theme else None
            }
            for t in theme_row2
        ]
    }
    
    # المحتوى
    contents = [
        {
            "type": "text",
            "text": f"🎮 {BOT_NAME}",
            "size": "xxl",
            "weight": "bold",
            "color": colors["primary"],
            "align": "center"
        },
        {
            "type": "text",
            "text": "بوت الألعاب الترفيهية",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"], "margin": "md"},
        user_card,
        {
            "type": "text",
            "text": "🎨 اختر ثيمك:",
            "size": "sm",
            "weight": "bold",
            "color": colors["text"],
            "margin": "md"
        },
        theme_buttons_row1,
        theme_buttons_row2
    ]
    
    # التذييل
    footer_buttons = [
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "📝 انضم" if not is_registered else "🚪 انسحب",
                        "text": "انضم" if not is_registered else "انسحب"
                    },
                    "style": "primary",
                    "height": "sm",
                    "color": colors["button"]
                },
                {
                    "type": "button",
                    "action": {"type": "message", "label": "🎮 ألعاب", "text": "مساعدة"},
                    "style": "secondary",
                    "height": "sm"
                }
            ]
        },
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"},
                    "style": "secondary",
                    "height": "sm"
                },
                {
                    "type": "button",
                    "action": {"type": "message", "label": "🏆 صدارة", "text": "صدارة"},
                    "style": "secondary",
                    "height": "sm"
                }
            ]
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    flex_content = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_buttons,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text=f"{BOT_NAME} - البداية",
        contents=FlexContainer.from_dict(flex_content)
    )


def build_games_menu(theme="💜"):
    """بناء قائمة الألعاب المحسّنة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # إنشاء أزرار الألعاب (3 في كل صف)
    games = list(GAME_LIST.items())
    game_buttons = []
    
    for i in range(0, len(games), 3):
        row_games = games[i:i+3]
        buttons = [
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
        game_buttons.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "xs",
            "contents": buttons
        })
    
    # المحتوى
    contents = [
        {
            "type": "text",
            "text": "🎮 الألعاب",
            "size": "xxl",
            "weight": "bold",
            "color": colors["primary"],
            "align": "center"
        },
        {
            "type": "text",
            "text": f"{len(GAME_LIST)} لعبة ممتعة",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"], "margin": "md"}
    ] + game_buttons
    
    # التذييل
    footer_buttons = [
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": "🏠 بداية", "text": "بداية"},
                    "style": "primary",
                    "height": "sm",
                    "color": colors["button"]
                },
                {
                    "type": "button",
                    "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                    "style": "secondary",
                    "height": "sm",
                    "color": colors["error"]
                }
            ]
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    flex_content = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_buttons,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text=f"{BOT_NAME} - الألعاب",
        contents=FlexContainer.from_dict(flex_content)
    )


def build_my_points(username, points, theme="💜"):
    """بناء صفحة النقاط المحسّنة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # تحديد المستوى
    if points < 50:
        level = "🌱 مبتدئ"
        level_color = colors["success"]
        progress = int((points / 50) * 100)
    elif points < 150:
        level = "⭐ متوسط"
        level_color = "#667EEA"
        progress = int(((points - 50) / 100) * 100)
    elif points < 300:
        level = "🔥 متقدم"
        level_color = "#DD6B20"
        progress = int(((points - 150) / 150) * 100)
    else:
        level = "👑 محترف"
        level_color = "#D53F8C"
        progress = 100
    
    # بطاقة النقاط
    points_card = {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {
                "type": "text",
                "text": str(points),
                "size": "xxl",
                "weight": "bold",
                "color": colors["primary"],
                "align": "center"
            },
            {
                "type": "text",
                "text": "نقطة",
                "size": "sm",
                "color": colors["text2"],
                "align": "center"
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "20px",
        "paddingAll": "20px"
    }
    
    # بطاقة المستوى
    level_card = {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {
                "type": "text",
                "text": level,
                "size": "lg",
                "weight": "bold",
                "color": level_color,
                "align": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": f"{progress}%",
                        "backgroundColor": level_color,
                        "height": "4px"
                    }
                ],
                "backgroundColor": colors["shadow1"],
                "height": "4px",
                "cornerRadius": "2px"
            },
            {
                "type": "text",
                "text": f"{progress}% للمستوى التالي",
                "size": "xs",
                "color": colors["text2"],
                "align": "center"
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "15px",
        "paddingAll": "15px"
    }
    
    # المحتوى
    contents = [
        {
            "type": "text",
            "text": "⭐ نقاطي",
            "size": "xxl",
            "weight": "bold",
            "color": colors["primary"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"], "margin": "sm"},
        {
            "type": "text",
            "text": f"👤 {username}",
            "size": "md",
            "color": colors["text"],
            "weight": "bold",
            "align": "center"
        },
        points_card,
        level_card
    ]
    
    # التذييل
    footer_buttons = [
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": "🏠 بداية", "text": "بداية"},
                    "style": "primary",
                    "height": "sm",
                    "color": colors["button"]
                },
                {
                    "type": "button",
                    "action": {"type": "message", "label": "🎮 ألعاب", "text": "مساعدة"},
                    "style": "secondary",
                    "height": "sm"
                }
            ]
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    flex_content = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_buttons,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text="نقاطي",
        contents=FlexContainer.from_dict(flex_content)
    )


def build_leaderboard(top_users, theme="💜"):
    """بناء لوحة الصدارة المحسّنة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    medals = ["🥇", "🥈", "🥉"]
    
    # قائمة اللاعبين
    leaderboard_items = []
    
    for i, (name, points) in enumerate(top_users[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        item_color = colors["primary"] if i <= 3 else colors["text"]
        
        leaderboard_items.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": medal,
                    "size": "md" if i <= 3 else "sm",
                    "flex": 0,
                    "color": item_color,
                    "weight": "bold" if i <= 3 else "regular"
                },
                {
                    "type": "text",
                    "text": name[:15] + "..." if len(name) > 15 else name,
                    "size": "sm",
                    "color": colors["text"],
                    "flex": 3,
                    "weight": "bold" if i <= 3 else "regular"
                },
                {
                    "type": "text",
                    "text": str(points),
                    "size": "sm",
                    "color": item_color,
                    "align": "end",
                    "flex": 1,
                    "weight": "bold"
                }
            ],
            "spacing": "md",
            "paddingAll": "sm"
        })
        
        if i < len(top_users[:10]):
            leaderboard_items.append({"type": "separator", "color": colors["shadow1"]})
    
    if not leaderboard_items:
        leaderboard_items = [{
            "type": "text",
            "text": "لا يوجد لاعبين",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        }]
    
    # المحتوى
    contents = [
        {
            "type": "text",
            "text": "🏆 الصدارة",
            "size": "xxl",
            "weight": "bold",
            "color": colors["primary"],
            "align": "center"
        },
        {
            "type": "text",
            "text": "أفضل 10 لاعبين",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        },
        {"type": "separator", "color": colors["shadow1"], "margin": "md"},
        {
            "type": "box",
            "layout": "vertical",
            "spacing": "none",
            "contents": leaderboard_items,
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "10px"
        }
    ]
    
    # التذييل
    footer_buttons = [
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": "🏠 بداية", "text": "بداية"},
                    "style": "primary",
                    "height": "sm",
                    "color": colors["button"]
                },
                {
                    "type": "button",
                    "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"},
                    "style": "secondary",
                    "height": "sm"
                }
            ]
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    flex_content = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_buttons,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text="الصدارة",
        contents=FlexContainer.from_dict(flex_content)
    )


def build_registration_required(theme="💜"):
    """بناء رسالة التسجيل المطلوب"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    contents = [
        {
            "type": "text",
            "text": "⚠️",
            "size": "xxl",
            "align": "center",
            "color": colors["error"]
        },
        {
            "type": "text",
            "text": "يجب التسجيل أولاً",
            "weight": "bold",
            "size": "xl",
            "color": colors["text"],
            "align": "center",
            "margin": "sm"
        },
        {"type": "separator", "color": colors["shadow1"], "margin": "sm"},
        {
            "type": "text",
            "text": "اضغط 'انضم' للتسجيل والبدء",
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "wrap": True
        }
    ]
    
    footer_buttons = [
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": "📝 انضم", "text": "انضم"},
                    "style": "primary",
                    "height": "sm",
                    "color": colors["button"]
                },
                {
                    "type": "button",
                    "action": {"type": "message", "label": "🏠 بداية", "text": "بداية"},
                    "style": "secondary",
                    "height": "sm"
                }
            ]
        }
    ]
    
    flex_content = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_buttons,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text="تسجيل مطلوب",
        contents=FlexContainer.from_dict(flex_content)
    )
