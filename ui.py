"""
🎨 Bot Mesh v8.0 - Complete UI System (Enhanced 3D Design)
نظام واجهات شامل مع 9 ثيمات ثلاثية الأبعاد - محسّن ومُحدّث
Created by: Abeer Aldosari © 2025

Features:
✅ 9 Neumorphic Themes with 3D Effects
✅ Advanced Shadow & Gradient System
✅ Quick Reply Buttons (Always Visible)
✅ All Windows: Start, Help, Games, My Points, Leaderboard, Registration
✅ Theme Storage per User in SQLite
✅ Full LINE Flex + Quick Reply Support
✅ Bot Name & Rights in Every Window
✅ Perfect Arabic Encoding
✅ Error-Free & Production-Ready
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "8.0"
BOT_RIGHTS = "Bot Mesh © 2025 by Abeer Aldosari"
BOT_DESCRIPTION = "بوت الألعاب الترفيهية الذكي"

# ============================================================================
# 9 Neumorphic Themes (Enhanced 3D Design)
# ============================================================================
THEMES = {
    "💜": {
        "name": "حلم بنفسجي",
        "primary": "#A78BFA",
        "secondary": "#C4B5FD",
        "accent": "#8B5CF6",
        "bg": "#1E1B4B",
        "card": "#2E2558",
        "text": "#F3F4F6",
        "text2": "#C4B5FD",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow1": "#6D28D9",
        "shadow2": "#1E1B4B",
        "border": "#7C3AED",
        "gradient": "linear-gradient(135deg, #667EEA 0%, #764BA2 100%)"
    },
    "💚": {
        "name": "غابة زمردية",
        "primary": "#10B981",
        "secondary": "#34D399",
        "accent": "#059669",
        "bg": "#064E3B",
        "card": "#065F46",
        "text": "#F0FDF4",
        "text2": "#6EE7B7",
        "success": "#34D399",
        "error": "#F87171",
        "warning": "#FBBF24",
        "shadow1": "#047857",
        "shadow2": "#022C22",
        "border": "#10B981",
        "gradient": "linear-gradient(135deg, #11998E 0%, #38EF7D 100%)"
    },
    "💙": {
        "name": "أزرق المحيط",
        "primary": "#3B82F6",
        "secondary": "#60A5FA",
        "accent": "#2563EB",
        "bg": "#1E3A8A",
        "card": "#1E40AF",
        "text": "#EFF6FF",
        "text2": "#93C5FD",
        "success": "#22C55E",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow1": "#1D4ED8",
        "shadow2": "#172554",
        "border": "#3B82F6",
        "gradient": "linear-gradient(135deg, #667EEA 0%, #5FCFFC 100%)"
    },
    "🖤": {
        "name": "المادة المظلمة",
        "primary": "#60A5FA",
        "secondary": "#93C5FD",
        "accent": "#3B82F6",
        "bg": "#0F172A",
        "card": "#1E293B",
        "text": "#F1F5F9",
        "text2": "#CBD5E1",
        "success": "#34D399",
        "error": "#F87171",
        "warning": "#FBBF24",
        "shadow1": "#334155",
        "shadow2": "#020617",
        "border": "#475569",
        "gradient": "linear-gradient(135deg, #232526 0%, #414345 100%)"
    },
    "🩷": {
        "name": "زهر وردي",
        "primary": "#EC4899",
        "secondary": "#F472B6",
        "accent": "#DB2777",
        "bg": "#831843",
        "card": "#9D174D",
        "text": "#FFF1F2",
        "text2": "#FBCFE8",
        "success": "#22C55E",
        "error": "#DC2626",
        "warning": "#F59E0B",
        "shadow1": "#BE185D",
        "shadow2": "#500724",
        "border": "#EC4899",
        "gradient": "linear-gradient(135deg, #F857A6 0%, #FF5858 100%)"
    },
    "🧡": {
        "name": "برتقالي الغروب",
        "primary": "#F97316",
        "secondary": "#FB923C",
        "accent": "#EA580C",
        "bg": "#7C2D12",
        "card": "#9A3412",
        "text": "#FFF7ED",
        "text2": "#FED7AA",
        "success": "#22C55E",
        "error": "#DC2626",
        "warning": "#FBBF24",
        "shadow1": "#C2410C",
        "shadow2": "#431407",
        "border": "#F97316",
        "gradient": "linear-gradient(135deg, #FFB75E 0%, #ED8F03 100%)"
    },
    "🤍": {
        "name": "نور نقي",
        "primary": "#8B5CF6",
        "secondary": "#A78BFA",
        "accent": "#7C3AED",
        "bg": "#F9FAFB",
        "card": "#FFFFFF",
        "text": "#111827",
        "text2": "#6B7280",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow1": "#E5E7EB",
        "shadow2": "#D1D5DB",
        "border": "#E5E7EB",
        "gradient": "linear-gradient(135deg, #FDFBFB 0%, #EBEDEE 100%)"
    },
    "🤎": {
        "name": "بني الأرض",
        "primary": "#D97706",
        "secondary": "#F59E0B",
        "accent": "#B45309",
        "bg": "#451A03",
        "card": "#78350F",
        "text": "#FEF3C7",
        "text2": "#FCD34D",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow1": "#92400E",
        "shadow2": "#1C0A00",
        "border": "#D97706",
        "gradient": "linear-gradient(135deg, #BC5F04 0%, #D67900 100%)"
    },
    "💛": {
        "name": "شمس ذهبية",
        "primary": "#EAB308",
        "secondary": "#FDE047",
        "accent": "#CA8A04",
        "bg": "#713F12",
        "card": "#854D0E",
        "text": "#FEFCE8",
        "text2": "#FEF08A",
        "success": "#22C55E",
        "error": "#DC2626",
        "warning": "#F97316",
        "shadow1": "#A16207",
        "shadow2": "#422006",
        "border": "#EAB308",
        "gradient": "linear-gradient(135deg, #FFD89B 0%, #19547B 100%)"
    }
}

DEFAULT_THEME = "💜"

# ============================================================================
# Quick Reply Buttons (Always Visible - 12 Games)
# ============================================================================
QUICK_REPLY_BUTTONS = [
    {"label": "⚡ سرعة", "text": "لعبة سرعة"},
    {"label": "🧠 ذكاء", "text": "لعبة ذكاء"},
    {"label": "🎯 لعبة", "text": "لعبة لعبة"},
    {"label": "🎵 أغنية", "text": "لعبة أغنية"},
    {"label": "🔮 تخمين", "text": "لعبة تخمين"},
    {"label": "🔗 سلسلة", "text": "لعبة سلسلة"},
    {"label": "🔤 كلمات", "text": "لعبة كلمات"},
    {"label": "📝 تكوين", "text": "لعبة تكوين"},
    {"label": "↔️ أضداد", "text": "لعبة أضداد"},
    {"label": "🎨 ألوان", "text": "لعبة ألوان"},
    {"label": "🔢 رياضيات", "text": "لعبة رياضيات"},
    {"label": "💖 توافق", "text": "لعبة توافق"}
]

# ============================================================================
# Game List (Complete Information)
# ============================================================================
GAME_LIST = {
    "سرعة": {"icon": "⚡", "label": "سرعة", "description": "اختبار سرعة الكتابة"},
    "ذكاء": {"icon": "🧠", "label": "ذكاء", "description": "ألغاز ذكية وممتعة"},
    "لعبة": {"icon": "🎯", "label": "لعبة", "description": "إنسان حيوان نبات"},
    "أغنية": {"icon": "🎵", "label": "أغنية", "description": "خمن المغني من الأغنية"},
    "تخمين": {"icon": "🔮", "label": "تخمين", "description": "خمن الكلمة من الفئة"},
    "سلسلة": {"icon": "🔗", "label": "سلسلة", "description": "سلسلة الكلمات"},
    "كلمات": {"icon": "🔤", "label": "كلمات", "description": "رتب الحروف المبعثرة"},
    "تكوين": {"icon": "📝", "label": "تكوين", "description": "كوّن كلمات من الحروف"},
    "أضداد": {"icon": "↔️", "label": "أضداد", "description": "اكتشف عكس الكلمة"},
    "ألوان": {"icon": "🎨", "label": "ألوان", "description": "لعبة تحدي الألوان"},
    "رياضيات": {"icon": "🔢", "label": "رياضيات", "description": "أسئلة حسابية ذكية"},
    "توافق": {"icon": "💖", "label": "توافق", "description": "احسب نسبة التوافق"}
}

# ============================================================================
# Constants
# ============================================================================
ERROR_MESSAGES = {
    "not_registered": "⚠️ يجب التسجيل أولاً للعب",
    "already_registered": "ℹ️ أنت مسجل بالفعل",
    "game_not_found": "❌ اللعبة غير موجودة",
    "no_active_game": "ℹ️ لا توجد لعبة نشطة",
}

SUCCESS_MESSAGES = {
    "registration": "✅ تم تسجيلك بنجاح!",
    "deactivation": "👋 تم إلغاء تسجيلك",
    "game_started": "🎮 بدأت اللعبة!",
    "theme_changed": "🎨 تم تغيير الثيم"
}

RATE_LIMITS = {
    "max_games_per_hour": 20,
    "max_messages_per_minute": 10,
    "cooldown_seconds": 2
}

# ============================================================================
# Helper Functions - 3D Components
# ============================================================================
def create_3d_button(label, text, colors, style="secondary", color=None):
    """إنشاء زر ثلاثي الأبعاد"""
    return {
        "type": "button",
        "action": {
            "type": "message",
            "label": label,
            "text": text
        },
        "style": style,
        "height": "sm",
        "color": color if color else (colors["primary"] if style == "primary" else colors["card"])
    }

def create_button_row(buttons, spacing="sm"):
    """إنشاء صف أزرار"""
    return {
        "type": "box",
        "layout": "horizontal",
        "spacing": spacing,
        "contents": buttons
    }

def create_separator(colors, margin="md"):
    """إنشاء خط فاصل"""
    return {
        "type": "separator",
        "color": colors["shadow1"],
        "margin": margin
    }

def create_3d_card(contents, colors, corner_radius="20px", padding="20px"):
    """إنشاء بطاقة ثلاثية الأبعاد"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "backgroundColor": colors["card"],
        "cornerRadius": corner_radius,
        "paddingAll": padding,
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }

def create_header(title, subtitle, colors):
    """إنشاء رأس احترافي"""
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

def create_info_box(icon, title, value, colors):
    """إنشاء صندوق معلومات ثلاثي الأبعاد"""
    return create_3d_card([
        {
            "type": "text",
            "text": icon,
            "size": "xxl",
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
            "size": "xl",
            "weight": "bold",
            "color": colors["primary"],
            "align": "center",
            "margin": "xs"
        }
    ], colors, "15px", "15px")

def create_footer_with_rights(buttons, colors):
    """إنشاء تذييل مع حقوق النشر"""
    contents = buttons + [
        create_separator(colors),
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": contents,
        "backgroundColor": colors["bg"],
        "paddingAll": "15px"
    }

# ============================================================================
# Build Home Window
# ============================================================================
def build_home(theme="💜", username="مستخدم", points=0, is_registered=False):
    """بناء الصفحة الرئيسية المحسّنة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    status = "✅ مسجل" if is_registered else "⚪ غير مسجل"
    status_color = colors["success"] if is_registered else colors["text2"]
    
    # بطاقة المستخدم الثلاثية الأبعاد
    user_card = create_3d_card([
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
            "spacing": "md",
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
                    "text": f"⭐ {points}",
                    "size": "sm",
                    "color": colors["primary"],
                    "align": "end",
                    "flex": 1,
                    "weight": "bold"
                }
            ],
            "margin": "md"
        }
    ], colors)
    
    # محدد الثيمات (3 في كل صف)
    theme_buttons = []
    theme_list = list(THEMES.keys())
    
    for i in range(0, len(theme_list), 3):
        row_themes = theme_list[i:i+3]
        buttons = []
        for t in row_themes:
            buttons.append(create_3d_button(
                t,
                f"ثيم {t}",
                colors,
                "primary" if t == theme else "secondary",
                colors["primary"] if t == theme else None
            ))
        theme_buttons.append(create_button_row(buttons))
    
    # المحتوى الرئيسي
    body_contents = [
        create_header(f"🎮 {BOT_NAME}", BOT_DESCRIPTION, colors),
        create_separator(colors),
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
    
    # أزرار التذييل
    footer_buttons = [
        create_button_row([
            create_3d_button(
                "📝 انضم" if not is_registered else "🚪 انسحب",
                "انضم" if not is_registered else "انسحب",
                colors,
                "primary",
                colors["success" if not is_registered else "error"]
            ),
            create_3d_button("🎮 ألعاب", "العاب", colors)
        ]),
        create_button_row([
            create_3d_button("⭐ نقاطي", "نقاطي", colors),
            create_3d_button("🏆 صدارة", "صدارة", colors)
        ])
    ]
    
    card = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": body_contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "footer": create_footer_with_rights(footer_buttons, colors),
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text=f"{BOT_NAME} - البداية",
        contents=FlexContainer.from_dict(card)
    )

# ============================================================================
# Build Help Window
# ============================================================================
def build_help(theme="💜"):
    """بناء نافذة المساعدة المحسّنة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # الأوامر الأساسية
    basic_commands = create_3d_card([
        {
            "type": "text",
            "text": "📌 الأوامر الأساسية:",
            "size": "md",
            "color": colors["text"],
            "weight": "bold"
        },
        {
            "type": "text",
            "text": "• بداية - العودة للقائمة الرئيسية\n• العاب - عرض جميع الألعاب\n• نقاطي - عرض نقاطك\n• صدارة - لوحة الصدارة\n• انضم - التسجيل في البوت\n• انسحب - إلغاء التسجيل",
            "size": "xs",
            "color": colors["text2"],
            "wrap": True,
            "margin": "sm"
        }
    ], colors, "15px", "15px")
    
    # أوامر اللعب
    game_commands = create_3d_card([
        {
            "type": "text",
            "text": "🎮 أوامر اللعب:",
            "size": "md",
            "color": colors["text"],
            "weight": "bold"
        },
        {
            "type": "text",
            "text": "• لعبة [اسم] - بدء لعبة\n• لمح - طلب تلميح (في بعض الألعاب)\n• جاوب - كشف الإجابة\n• إيقاف - إنهاء اللعبة الحالية",
            "size": "xs",
            "color": colors["text2"],
            "wrap": True,
            "margin": "sm"
        }
    ], colors, "15px", "15px")
    
    # معلومات الألعاب
    games_info = create_3d_card([
        {
            "type": "text",
            "text": "🎯 الألعاب المتاحة:",
            "size": "md",
            "color": colors["text"],
            "weight": "bold"
        },
        {
            "type": "text",
            "text": f"✨ {len(GAME_LIST)} لعبة مختلفة\n💡 استخدم الأزرار السريعة في الأسفل!",
            "size": "xs",
            "color": colors["primary"],
            "wrap": True,
            "margin": "sm"
        }
    ], colors, "15px", "15px")
    
    # المحتوى
    body_contents = [
        create_header("❓ مساعدة", "دليل استخدام البوت", colors),
        create_separator(colors),
        basic_commands,
        game_commands,
        games_info
    ]
    
    # التذييل
    footer_buttons = [
        create_button_row([
            create_3d_button("🏠 البداية", "بداية", colors, "primary", colors["primary"]),
            create_3d_button("🎮 ألعاب", "العاب", colors)
        ])
    ]
    
    card = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": body_contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "footer": create_footer_with_rights(footer_buttons, colors),
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text="مساعدة",
        contents=FlexContainer.from_dict(card)
    )

# ============================================================================
# Build Games Menu
# ============================================================================
def build_games_menu(theme="💜"):
    """بناء قائمة الألعاب المحسّنة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # أزرار الألعاب (3 في كل صف)
    games = list(GAME_LIST.items())
    game_buttons = []
    
    for i in range(0, len(games), 3):
        row_games = games[i:i+3]
        buttons = []
        for game_key, game_info in row_games:
            buttons.append(create_3d_button(
                f"{game_info['icon']} {game_info['label']}",
                f"لعبة {game_key}",
                colors
            ))
        game_buttons.append(create_button_row(buttons))
    
    # بطاقة التعليمات
    instructions = create_3d_card([
        {
            "type": "text",
            "text": "💡 كيفية اللعب:",
            "size": "sm",
            "color": colors["text"],
            "weight": "bold"
        },
        {
            "type": "text",
            "text": "اضغط على اسم اللعبة للبدء فوراً!\nاستخدم الأزرار السريعة في الأسفل للوصول السريع.",
            "size": "xs",
            "color": colors["text2"],
            "wrap": True,
            "margin": "sm"
        }
    ], colors, "15px", "15px")
    
    # المحتوى
    body_contents = [
        create_header("🎮 الألعاب المتاحة", f"{len(GAME_LIST)} لعبة مختلفة", colors),
        create_separator(colors)
    ] + game_buttons + [
        create_separator(colors),
        instructions
    ]
    
    # التذييل
    footer_buttons = [
        create_button_row([
            create_3d_button("🏠 البداية", "بداية", colors, "primary", colors["primary"]),
            create_3d_button("❓ مساعدة", "مساعدة", colors)
        ])
    ]
    
    card = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": body_contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "footer": create_footer_with_rights(footer_buttons, colors),
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text="قائمة الألعاب",
        contents=FlexContainer.from_dict(card)
    )

# ============================================================================
# Build My Points Window
# ============================================================================
def build_my_points(username, points, theme="💜"):
    """بناء نافذة نقاطي المحسّنة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # بطاقة النقاط الكبيرة
    points_card = create_3d_card([
        {
            "type": "text",
            "text": "⭐",
            "size": "xxl",
            "align": "center"
        },
        {
            "type": "text",
            "text": str(points),
            "size": "xxl",
            "weight": "bold",
            "color": colors["primary"],
            "align": "center",
            "margin": "md"
        },
        {
            "type": "text",
            "text": "نقطة",
            "size": "md",
            "color": colors["text2"],
            "align": "center",
            "margin": "sm"
        }
    ], colors, "25px", "30px")
    
    # معلومات إضافية
    info_boxes = {
        "type": "box",
        "layout": "horizontal",
        "spacing": "md",
        "contents": [
            create_info_box("🎮", "ألعاب", len(GAME_LIST), colors),
            create_info_box("👤", "اللاعب", username[:8] + "..." if len(username) > 8 else username, colors)
        ]
    }
    
    # نصيحة
    tip = create_3d_card([
        {
            "type": "text",
            "text": "💡 نصيحة:",
            "size": "sm",
            "color": colors["text"],
            "weight": "bold"
        },
        {
            "type": "text",
            "text": "العب المزيد من الألعاب لزيادة نقاطك والوصول للصدارة!",
            "size": "xs",
            "color": colors["text2"],
            "wrap": True,
            "margin": "sm"
        }
    ], colors, "15px", "15px")
    
    # المحتوى
    body_contents = [
        create_header("⭐ نقاطي", f"مرحباً {username}", colors),
        create_separator(colors),
        points_card,
        info_boxes,
        create_separator(colors),
        tip
    ]
    
    # التذييل
    footer_buttons = [
        create_button_row([
            create_3d_button("🏆 الصدارة", "صدارة", colors, "primary", colors["primary"]),
            create_3d_button("🎮 ألعاب", "العاب", colors)
        ]),
        create_button_row([
            create_3d_button("🏠 البداية", "بداية", colors)
        ])
    ]
    
    card = {
        "type": "bubble",
        "
    size": "mega",
"body": {
"type": "box",
"layout": "vertical",
"spacing": "lg",
"contents": body_contents,
"backgroundColor": colors["bg"],
"paddingAll": "20px"
},
"footer": create_footer_with_rights(footer_buttons, colors),
"styles": {
"body": {"backgroundColor": colors["bg"]},
"footer": {"backgroundColor": colors["bg"]}
}
}
return FlexMessage(
    alt_text="نقاطي",
    contents=FlexContainer.from_dict(card)
)
============================================================================
Build Leaderboard Window
============================================================================
def build_leaderboard(top_players, theme="💜"):
"""بناء لوحة الصدارة المحسّنة"""
colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
# قائمة اللاعبين
players_list = []

for i, (name, points) in enumerate(top_players[:10], 1):
    # ميدالية للمراكز الثلاثة الأولى
    medal = ""
    rank_color = colors["text"]
    
    if i == 1:
        medal = "🥇"
        rank_color = "#FFD700"
    elif i == 2:
        medal = "🥈"
        rank_color = "#C0C0C0"
    elif i == 3:
        medal = "🥉"
        rank_color = "#CD7F32"
    else:
        medal = f"{i}."
    
    player_row = create_3d_card([
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": medal,
                    "size": "lg",
                    "color": rank_color,
                    "weight": "bold",
                    "flex": 0,
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": name[:15] + "..." if len(name) > 15 else name,
                    "size": "sm",
                    "color": colors["text"],
                    "flex": 3,
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": f"⭐ {points}",
                    "size": "sm",
                    "color": colors["primary"],
                    "align": "end",
                    "weight": "bold",
                    "flex": 2
                }
            ]
        }
    ], colors, "15px", "15px")
    
    players_list.append(player_row)

# رسالة إذا لم يكن هناك لاعبين
if not top_players:
    players_list = [
        create_3d_card([
            {
                "type": "text",
                "text": "لا يوجد لاعبون بعد",
                "size": "md",
                "color": colors["text2"],
                "align": "center"
            }
        ], colors, "15px", "15px")
    ]

# المحتوى
body_contents = [
    create_header("🏆 لوحة الصدارة", f"أفضل {len(top_players)} لاعب", colors),
    create_separator(colors)
] + players_list

# التذييل
footer_buttons = [
    create_button_row([
        create_3d_button("⭐ نقاطي", "نقاطي", colors, "primary", colors["primary"]),
        create_3d_button("🎮 ألعاب", "العاب", colors)
    ]),
    create_button_row([
        create_3d_button("🏠 البداية", "بداية", colors)
    ])
]

card = {
    "type": "bubble",
    "size": "mega",
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": body_contents,
        "backgroundColor": colors["bg"],
        "paddingAll": "20px"
    },
    "footer": create_footer_with_rights(footer_buttons, colors),
    "styles": {
        "body": {"backgroundColor": colors["bg"]},
        "footer": {"backgroundColor": colors["bg"]}
    }
}

return FlexMessage(
    alt_text="لوحة الصدارة",
    contents=FlexContainer.from_dict(card)
)
============================================================================
Build Registration Required Window
============================================================================
def build_registration_required(theme="💜"):
"""بناء نافذة طلب التسجيل"""
colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
# رسالة التنبيه
alert_card = create_3d_card([
    {
        "type": "text",
        "text": "⚠️",
        "size": "xxl",
        "align": "center"
    },
    {
        "type": "text",
        "text": "يجب التسجيل أولاً",
        "size": "xl",
        "weight": "bold",
        "color": colors["warning"],
        "align": "center",
        "margin": "md"
    },
    {
        "type": "text",
        "text": "للعب الألعاب وجمع النقاط، يرجى التسجيل أولاً",
        "size": "sm",
        "color": colors["text2"],
        "align": "center",
        "wrap": True,
        "margin": "md"
    }
], colors, "25px", "30px")

# المحتوى
body_contents = [
    create_header("📝 تسجيل مطلوب", "انضم إلينا الآن!", colors),
    create_separator(colors),
    alert_card
]

# التذييل
footer_buttons = [
    create_button_row([
        create_3d_button("✅ انضم الآن", "انضم", colors, "primary", colors["success"])
    ]),
    create_button_row([
        create_3d_button("🏠 البداية", "بداية", colors)
    ])
]

card = {
    "type": "bubble",
    "size": "mega",
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "lg",
        "contents": body_contents,
        "backgroundColor": colors["bg"],
        "paddingAll": "20px"
    },
    "footer": create_footer_with_rights(footer_buttons, colors),
    "styles": {
        "body": {"backgroundColor": colors["bg"]},
        "footer": {"backgroundColor": colors["bg"]}
    }
}

return FlexMessage(
    alt_text="تسجيل مطلوب",
    contents=FlexContainer.from_dict(card)
)
