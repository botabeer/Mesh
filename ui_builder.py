"""
Bot Mesh - Enhanced UI Builder with Perfect LINE Compatibility
Created by: Abeer Aldosari © 2025

Features:
✅ Perfect Arabic encoding
✅ Professional Neumorphism design
✅ LINE-optimized Flex Messages
✅ Smooth animations
✅ Accessibility-friendly colors
"""

from linebot.v3.messaging import FlexMessage, FlexContainer
from constants import (
    BOT_NAME, BOT_RIGHTS, THEMES, DEFAULT_THEME,
    GAME_LIST, FIXED_BUTTONS
)


def create_neumorphic_card(colors, contents, footer_contents=None, size="mega"):
    """
    إنشاء بطاقة Neumorphic محسنة
    
    Args:
        colors: ألوان الثيم
        contents: محتويات البطاقة
        footer_contents: محتويات التذييل (اختياري)
        size: حجم البطاقة (kilo/mega/giga)
    
    Returns:
        dict: بطاقة Flex Message
    """
    card = {
        "type": "bubble",
        "size": size,
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "styles": {
            "body": {"backgroundColor": colors["bg"]}
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
        card["styles"]["footer"] = {"backgroundColor": colors["bg"]}
    
    return card


def create_button(label, text, style="secondary", color=None):
    """
    إنشاء زر محسن
    
    Args:
        label: نص الزر
        text: الرسالة المرسلة عند الضغط
        style: نمط الزر (primary/secondary)
        color: لون مخصص (اختياري)
    
    Returns:
        dict: زر
    """
    button = {
        "type": "button",
        "action": {
            "type": "message",
            "label": label,
            "text": text
        },
        "style": style,
        "height": "sm"
    }
    
    if color:
        button["color"] = color
    
    return button


def create_button_row(buttons, spacing="sm"):
    """
    إنشاء صف أزرار
    
    Args:
        buttons: قائمة الأزرار
        spacing: المسافة بين الأزرار
    
    Returns:
        dict: صف أزرار أفقي
    """
    return {
        "type": "box",
        "layout": "horizontal",
        "spacing": spacing,
        "contents": buttons
    }


def create_separator(color="#E2E8F0", margin="md"):
    """
    إنشاء خط فاصل
    
    Args:
        color: لون الخط
        margin: الهامش
    
    Returns:
        dict: خط فاصل
    """
    return {
        "type": "separator",
        "color": color,
        "margin": margin
    }


def create_header(title, subtitle=None, colors=None):
    """
    إنشاء رأس احترافي
    
    Args:
        title: العنوان الرئيسي
        subtitle: العنوان الفرعي (اختياري)
        colors: ألوان الثيم
    
    Returns:
        dict: رأس البطاقة
    """
    if not colors:
        colors = THEMES[DEFAULT_THEME]
    
    contents = [
        {
            "type": "text",
            "text": title,
            "weight": "bold",
            "size": "xxl",
            "color": colors["primary"],
            "align": "center"
        }
    ]
    
    if subtitle:
        contents.append({
            "type": "text",
            "text": subtitle,
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "margin": "sm"
        })
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "spacing": "xs"
    }


def create_info_card(icon, title, value, colors):
    """
    إنشاء بطاقة معلومات
    
    Args:
        icon: أيقونة
        title: عنوان
        value: قيمة
        colors: ألوان الثيم
    
    Returns:
        dict: بطاقة معلومات
    """
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": icon,
                "size": "xl",
                "align": "center"
            },
            {
                "type": "text",
                "text": title,
                "size": "xs",
                "color": colors["text2"],
                "align": "center",
                "margin": "sm"
            },
            {
                "type": "text",
                "text": str(value),
                "size": "lg",
                "weight": "bold",
                "color": colors["primary"],
                "align": "center",
                "margin": "xs"
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "20px",
        "paddingAll": "20px",
        "spacing": "xs"
    }


def build_home(theme="💜", username="مستخدم", points=0, is_registered=False):
    """
    بناء الصفحة الرئيسية المحسنة
    
    Args:
        theme: رمز الثيم
        username: اسم المستخدم
        points: نقاط المستخدم
        is_registered: حالة التسجيل
    
    Returns:
        FlexMessage: رسالة الصفحة الرئيسية
    """
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    status = "✅ مسجل" if is_registered else "⚪ غير مسجل"
    status_color = colors["success"] if is_registered else colors["text2"]
    
    # بطاقة معلومات المستخدم
    user_card = {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
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
                        "size": "sm",
                        "color": status_color,
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"⭐ {points} نقطة",
                        "size": "sm",
                        "color": colors["primary"],
                        "align": "end",
                        "flex": 1
                    }
                ]
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "20px",
        "paddingAll": "20px"
    }
    
    # محدد الثيمات (3 في كل صف)
    theme_buttons = []
    theme_list = list(THEMES.keys())
    
    for i in range(0, len(theme_list), 3):
        row_themes = theme_list[i:i+3]
        buttons = [
            create_button(
                t,
                f"ثيم {t}",
                "primary" if t == theme else "secondary",
                colors["primary"] if t == theme else None
            )
            for t in row_themes
        ]
        theme_buttons.append(create_button_row(buttons))
    
    # بناء المحتوى
    contents = [
        create_header(f"🎮 {BOT_NAME}", "بوت الألعاب الترفيهية الذكي", colors),
        create_separator(colors["shadow1"]),
        user_card,
        {
            "type": "text",
            "text": "🎨 اختر ثيمك المفضل:",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "lg"
        }
    ] + theme_buttons
    
    # التذييل
    footer_buttons = [
        create_button_row([
            create_button(
                "📝 انضم" if not is_registered else "🚪 انسحب",
                "انضم" if not is_registered else "انسحب",
                "primary",
                colors["button"]
            ),
            create_button(
                FIXED_BUTTONS["games"]["label"],
                FIXED_BUTTONS["games"]["text"],
                "secondary"
            )
        ]),
        create_button_row([
            create_button(
                FIXED_BUTTONS["points"]["label"],
                FIXED_BUTTONS["points"]["text"]
            ),
            create_button(
                FIXED_BUTTONS["leaderboard"]["label"],
                FIXED_BUTTONS["leaderboard"]["text"]
            )
        ]),
        create_separator(colors["shadow1"]),
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    card = create_neumorphic_card(colors, contents, footer_buttons)
    return FlexMessage(
        alt_text=f"{BOT_NAME} - البداية",
        contents=FlexContainer.from_dict(card)
    )


def build_games_menu(theme="💜"):
    """
    بناء قائمة الألعاب المحسنة
    
    Args:
        theme: رمز الثيم
    
    Returns:
        FlexMessage: رسالة قائمة الألعاب
    """
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # إنشاء أزرار الألعاب (3 في كل صف)
    games = list(GAME_LIST.items())
    game_buttons = []
    
    for i in range(0, len(games), 3):
        row_games = games[i:i+3]
        buttons = [
            create_button(
                f"{game[1]['icon']} {game[1]['label']}",
                f"لعبة {game[0]}",
                "secondary",
                colors["primary"]
            )
            for game in row_games
        ]
        game_buttons.append(create_button_row(buttons))
    
    # بطاقة التعليمات
    instructions_card = {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
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
                "wrap": True,
                "margin": "sm"
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "15px",
        "paddingAll": "15px"
    }
    
    # بناء المحتوى
    contents = [
        create_header("🎮 الألعاب المتاحة", f"اختر من {len(GAME_LIST)} لعبة مختلفة", colors),
        create_separator(colors["shadow1"])
    ] + game_buttons + [
        create_separator(colors["shadow1"], "lg"),
        instructions_card
    ]
    
    # التذييل
    footer_buttons = [
        create_button_row([
            create_button(
                FIXED_BUTTONS["home"]["label"],
                FIXED_BUTTONS["home"]["text"],
                "primary",
                colors["button"]
            ),
            create_button(
                FIXED_BUTTONS["stop"]["label"],
                FIXED_BUTTONS["stop"]["text"],
                "secondary",
                colors["error"]
            )
        ]),
        create_separator(colors["shadow1"]),
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    card = create_neumorphic_card(colors, contents, footer_buttons)
    return FlexMessage(
        alt_text=f"{BOT_NAME} - الألعاب",
        contents=FlexContainer.from_dict(card)
    )


def build_my_points(username, points, theme="💜"):
    """
    بناء صفحة النقاط المحسنة
    
    Args:
        username: اسم المستخدم
        points: النقاط
        theme: رمز الثيم
    
    Returns:
        FlexMessage: رسالة النقاط
    """
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
    
    # بطاقة النقاط الرئيسية
    points_card = {
        "type": "box",
        "layout": "vertical",
        "spacing": "lg",
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
                "text": str(points),
                "size": "xxl",
                "weight": "bold",
                "color": colors["primary"],
                "align": "center"
            },
            {
                "type": "text",
                "text": "نقطة",
                "size": "md",
                "color": colors["text2"],
                "align": "center"
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "25px",
        "paddingAll": "30px"
    }
    
    # بطاقة المستوى
    level_card = {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
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
                "size": "xl",
                "weight": "bold",
                "color": level_color,
                "align": "center"
            },
            # شريط التقدم
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
                        "height": "6px"
                    }
                ],
                "backgroundColor": colors["shadow1"],
                "height": "6px",
                "cornerRadius": "3px"
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
        "cornerRadius": "20px",
        "paddingAll": "20px"
    }
    
    # بناء المحتوى
    contents = [
        create_header("⭐ نقاطي", None, colors),
        create_separator(colors["shadow1"]),
        {
            "type": "text",
            "text": f"👤 {username}",
            "size": "lg",
            "color": colors["text"],
            "weight": "bold",
            "align": "center"
        },
        points_card,
        level_card,
        create_separator(colors["shadow1"], "lg"),
        {
            "type": "text",
            "text": "⚠️ سيتم حذف بياناتك بعد 7 أيام من عدم النشاط",
            "size": "xs",
            "color": colors["error"],
            "wrap": True,
            "align": "center"
        }
    ]
    
    # التذييل
    footer_buttons = [
        create_button_row([
            create_button(
                FIXED_BUTTONS["home"]["label"],
                FIXED_BUTTONS["home"]["text"],
                "primary",
                colors["button"]
            ),
            create_button(
                FIXED_BUTTONS["games"]["label"],
                FIXED_BUTTONS["games"]["text"]
            )
        ]),
        create_separator(colors["shadow1"]),
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    card = create_neumorphic_card(colors, contents, footer_buttons, "kilo")
    return FlexMessage(
        alt_text="نقاطي",
        contents=FlexContainer.from_dict(card)
    )


def build_leaderboard(top_users, theme="💜"):
    """
    بناء لوحة الصدارة المحسنة
    
    Args:
        top_users: قائمة أفضل المستخدمين [(name, points), ...]
        theme: رمز الثيم
    
    Returns:
        FlexMessage: رسالة لوحة الصدارة
    """
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    medals = ["🥇", "🥈", "🥉"]
    
    # إنشاء قائمة اللاعبين
    leaderboard_items = []
    
    for i, (name, points) in enumerate(top_users[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        item_color = colors["primary"] if i <= 3 else colors["text"]
        bg_color = colors["card"] if i <= 3 else "transparent"
        
        leaderboard_items.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": medal,
                    "size": "lg" if i <= 3 else "md",
                    "flex": 0,
                    "color": item_color,
                    "weight": "bold" if i <= 3 else "regular"
                },
                {
                    "type": "text",
                    "text": name,
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
            "paddingAll": "md",
            "backgroundColor": bg_color,
            "cornerRadius": "10px" if i <= 3 else "0px"
        })
        
        if i < len(top_users[:10]):
            leaderboard_items.append(create_separator(colors["shadow1"], "sm"))
    
    if not leaderboard_items:
        leaderboard_items = [{
            "type": "text",
            "text": "لا يوجد لاعبين مسجلين بعد",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        }]
    
    # حاوية اللوحة
    leaderboard_container = {
        "type": "box",
        "layout": "vertical",
        "spacing": "none",
        "contents": leaderboard_items,
        "backgroundColor": colors["card"],
        "cornerRadius": "20px",
        "paddingAll": "15px"
    }
    
    # بناء المحتوى
    contents = [
        create_header("🏆 لوحة الصدارة", "أفضل 10 لاعبين", colors),
        create_separator(colors["shadow1"]),
        leaderboard_container
    ]
    
    # التذييل
    footer_buttons = [
        create_button_row([
            create_button(
                FIXED_BUTTONS["home"]["label"],
                FIXED_BUTTONS["home"]["text"],
                "primary",
                colors["button"]
            ),
            create_button(
                FIXED_BUTTONS["points"]["label"],
                FIXED_BUTTONS["points"]["text"]
            )
        ]),
        create_separator(colors["shadow1"]),
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    card = create_neumorphic_card(colors, contents, footer_buttons, "kilo")
    return FlexMessage(
        alt_text="الصدارة",
        contents=FlexContainer.from_dict(card)
    )


def build_registration_required(theme="💜"):
    """
    بناء رسالة التسجيل المطلوب
    
    Args:
        theme: رمز الثيم
    
    Returns:
        FlexMessage: رسالة التسجيل
    """
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
            "margin": "md"
        },
        create_separator(colors["shadow1"]),
        {
            "type": "text",
            "text": "اضغط 'انضم' للتسجيل والبدء باللعب",
            "size": "md",
            "color": colors["text2"],
            "align": "center",
            "wrap": True
        }
    ]
    
    footer_buttons = [
        create_button_row([
            create_button(
                "📝 انضم",
                "انضم",
                "primary",
                colors["button"]
            ),
            create_button(
                FIXED_BUTTONS["home"]["label"],
                FIXED_BUTTONS["home"]["text"]
            )
        ])
    ]
    
    card = create_neumorphic_card(colors, contents, footer_buttons, "kilo")
    return FlexMessage(
        alt_text="تسجيل مطلوب",
        contents=FlexContainer.from_dict(card)
    )
