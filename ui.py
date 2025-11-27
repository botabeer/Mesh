"""
🎨 Bot Mesh v8.0 - Complete UI System (All-in-One)
نظام واجهات شامل مع 9 ثيمات ثلاثية الأبعاد - ملف واحد
Created by: Abeer Aldosari © 2025

Features:
✅ 9 Neumorphic Themes
✅ 3D Effects (Shadows & Gradients)
✅ Quick Reply Buttons (Always Visible)
✅ All Windows: Start, Help, Games, Playing, End, Winner, Compatibility
✅ Theme Storage per User in SQLite
✅ Full LINE Flex + Quick Reply Support
✅ Bot Name & Rights in Every Window
✅ Perfect Arabic Encoding
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "8.0"
BOT_RIGHTS = "Bot Mesh © 2025 by Abeer Aldosari"
BOT_DESCRIPTION = "بوت الألعاب الترفيهية الذكي"

# ============================================================================
# 9 Neumorphic Themes (3D Design)
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
        "border": "#7C3AED"
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
        "border": "#10B981"
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
        "border": "#3B82F6"
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
        "border": "#475569"
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
        "border": "#EC4899"
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
        "border": "#F97316"
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
        "border": "#E5E7EB"
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
        "border": "#D97706"
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
        "border": "#EAB308"
    }
}

DEFAULT_THEME = "💜"

# ============================================================================
# Quick Reply Buttons (Always Visible - Games)
# ============================================================================
QUICK_REPLY_BUTTONS = [
    {"label": "▫️ أسرع", "text": "لعبة سرعة"},
    {"label": "▫️ ذكاء", "text": "لعبة ذكاء"},
    {"label": "▫️ لعبة", "text": "لعبة لعبة"},
    {"label": "▫️ أغنية", "text": "لعبة أغنية"},
    {"label": "▫️ خمن", "text": "لعبة تخمين"},
    {"label": "▫️ سلسلة", "text": "لعبة سلسلة"},
    {"label": "▫️ ترتيب", "text": "لعبة كلمات"},
    {"label": "▫️ تكوين", "text": "لعبة تكوين"},
    {"label": "▫️ ضد", "text": "لعبة أضداد"},
    {"label": "▫️ لون", "text": "لعبة ألوان"},
    {"label": "▫️ رياضيات", "text": "لعبة رياضيات"},
    {"label": "▫️ توافق", "text": "لعبة توافق"}
]

# ============================================================================
# Game List
# ============================================================================
GAME_LIST = {
    "سرعة": {"icon": "⚡", "label": "أسرع"},
    "ذكاء": {"icon": "🧠", "label": "ذكاء"},
    "لعبة": {"icon": "🎯", "label": "لعبة"},
    "أغنية": {"icon": "🎵", "label": "أغنية"},
    "تخمين": {"icon": "🔮", "label": "خمن"},
    "سلسلة": {"icon": "🔗", "label": "سلسلة"},
    "كلمات": {"icon": "🔤", "label": "ترتيب"},
    "تكوين": {"icon": "📝", "label": "تكوين"},
    "أضداد": {"icon": "↔️", "label": "ضد"},
    "ألوان": {"icon": "🎨", "label": "لون"},
    "رياضيات": {"icon": "🔢", "label": "رياضيات"},
    "توافق": {"icon": "💖", "label": "توافق"}
}

# ============================================================================
# User Level System
# ============================================================================
LEVEL_SYSTEM = {
    "ranges": [
        {"min": 0, "max": 49, "name": "🌱 مبتدئ", "color": "#10B981"},
        {"min": 50, "max": 149, "name": "⭐ متوسط", "color": "#667EEA"},
        {"min": 150, "max": 299, "name": "🔥 متقدم", "color": "#DD6B20"},
        {"min": 300, "max": 499, "name": "👑 محترف", "color": "#D53F8C"},
        {"min": 500, "max": 999999, "name": "💎 أسطوري", "color": "#8B5CF6"}
    ]
}

def get_user_level(points):
    """تحديد مستوى المستخدم بناءً على النقاط"""
    for level in LEVEL_SYSTEM["ranges"]:
        if level["min"] <= points <= level["max"]:
            progress = int(((points - level["min"]) / (level["max"] - level["min"] + 1)) * 100)
            return {
                "name": level["name"],
                "color": level["color"],
                "progress": min(progress, 100),
                "next_level_points": level["max"] + 1
            }
    
    return {
        "name": "💎 أسطوري",
        "color": "#8B5CF6",
        "progress": 100,
        "next_level_points": None
    }

# ============================================================================
# Rank Colors (Leaderboard)
# ============================================================================
RANK_COLORS = {
    1: {"medal": "🥇", "color": "#FFD700"},
    2: {"medal": "🥈", "color": "#C0C0C0"},
    3: {"medal": "🥉", "color": "#CD7F32"},
}

# ============================================================================
# Error & Success Messages
# ============================================================================
ERROR_MESSAGES = {
    "not_registered": "⚠️ يجب التسجيل أولاً للعب",
    "already_registered": "ℹ️ أنت مسجل بالفعل",
    "game_not_found": "❌ اللعبة غير موجودة",
    "no_active_game": "ℹ️ لا توجد لعبة نشطة",
    "database_error": "❌ حدث خطأ في قاعدة البيانات",
    "invalid_input": "❌ إدخال غير صحيح"
}

SUCCESS_MESSAGES = {
    "registration": "✅ تم تسجيلك بنجاح!",
    "deactivation": "👋 تم إلغاء تسجيلك",
    "game_started": "🎮 بدأت اللعبة!",
    "game_ended": "⛔ تم إيقاف اللعبة",
    "correct_answer": "✅ إجابة صحيحة!",
    "theme_changed": "🎨 تم تغيير الثيم"
}

# ============================================================================
# Security Settings
# ============================================================================
RATE_LIMITS = {
    "max_games_per_hour": 20,
    "max_messages_per_minute": 10,
    "cooldown_seconds": 2
}

# ============================================================================
# Helper Functions - UI Components
# ============================================================================
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

def create_3d_card(colors, corner_radius="20px", padding="20px"):
    """إنشاء بطاقة ثلاثية الأبعاد"""
    return {
        "backgroundColor": colors["card"],
        "cornerRadius": corner_radius,
        "paddingAll": padding,
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }

def create_info_card(icon, title, value, colors):
    """إنشاء بطاقة معلومات ثلاثية الأبعاد"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
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
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "20px",
        "paddingAll": "20px",
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }

def create_progress_bar(percentage, colors, height="6px"):
    """إنشاء شريط تقدم"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": f"{min(max(percentage, 0), 100)}%",
                "backgroundColor": colors["primary"],
                "height": height,
                "cornerRadius": "3px"
            }
        ],
        "backgroundColor": colors["shadow1"],
        "height": height,
        "cornerRadius": "3px"
    }

# ============================================================================
# Build Home Window
# ============================================================================
def build_home(theme="💜", username="مستخدم", points=0, is_registered=False):
    """بناء الصفحة الرئيسية"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    status = "✅ مسجل" if is_registered else "⚪ غير مسجل"
    status_color = colors["success"] if is_registered else colors["text2"]
    
    # بطاقة المستخدم
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
        "paddingAll": "20px",
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }
    
    # محدد الثيمات
    theme_buttons = []
    theme_list = list(THEMES.keys())
    
    for i in range(0, len(theme_list), 3):
        row_themes = theme_list[i:i+3]
        buttons = []
        for t in row_themes:
            buttons.append({
                "type": "button",
                "action": {
                    "type": "message",
                    "label": t,
                    "text": f"ثيم {t}"
                },
                "style": "primary" if t == theme else "secondary",
                "height": "sm",
                "color": colors["primary"] if t == theme else colors["card"]
            })
        theme_buttons.append(create_button_row(buttons))
    
    # المحتوى
    contents = [
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
    
    # التذييل
    footer_buttons = [
        create_button_row([
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "📝 انضم" if not is_registered else "🚪 انسحب",
                    "text": "انضم" if not is_registered else "انسحب"
                },
                "style": "primary",
                "height": "sm",
                "color": colors["primary"]
            },
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "🎮 ألعاب",
                    "text": "العاب"
                },
                "style": "secondary",
                "height": "sm"
            }
        ]),
        create_button_row([
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "⭐ نقاطي",
                    "text": "نقاطي"
                },
                "style": "secondary",
                "height": "sm"
            },
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "🏆 صدارة",
                    "text": "صدارة"
                },
                "style": "secondary",
                "height": "sm"
            }
        ]),
        create_separator(colors),
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    card = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
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
        alt_text=f"{BOT_NAME} - البداية",
        contents=FlexContainer.from_dict(card)
    )

# ============================================================================
# Build Help Window
# ============================================================================
def build_help(theme="💜"):
    """بناء نافذة المساعدة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # قسم الأوامر الأساسية
    basic_commands = {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
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
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "15px",
        "paddingAll": "15px",
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }
    
    # قسم أوامر اللعب
    game_commands = {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {
                "type": "text",
                "text": "🎮 أوامر اللعب:",
                "size": "md",
                "color": colors["text"],
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "• لعبة [اسم] - بدء لعبة\n• لمح - طلب تلميح\n• جاوب - كشف الإجابة\n• إيقاف - إنهاء اللعبة الحالية",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True,
                "margin": "sm"
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "15px",
        "paddingAll": "15px",
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }
    
    # قسم الألعاب المتاحة
    games_info = {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {
                "type": "text",
                "text": "🎯 الألعاب المتاحة (12):",
                "size": "md",
                "color": colors["text"],
                "weight": "bold"
            },
            {
                "type": "text",
                "text": "استخدم الأزرار السريعة في الأسفل للوصول السريع للألعاب!",
                "size": "xs",
                "color": colors["primary"],
                "wrap": True,
                "margin": "sm"
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "15px",
        "paddingAll": "15px",
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }
    
    # المحتوى
    contents = [
        create_header("❓ مساعدة", "دليل استخدام البوت", colors),
        create_separator(colors),
        basic_commands,
        game_commands,
        games_info,
        create_separator(colors),
        {
            "type": "text",
            "text": "💡 نصيحة: استخدم الأزرار السريعة الدائمة في الأسفل للوصول السريع!",
            "size": "xs",
            "color": colors["warning"],
            "wrap": True,
            "align": "center"
        }
    ]
    
    # التذييل
    footer_buttons = [
        create_button_row([
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "🏠 البداية",
                    "text": "بداية"
                },
                "style": "primary",
                "height": "sm",
                "color": colors["primary"]
            },
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "🎮 ألعاب",
                    "text": "العاب"
                },
                "style": "secondary",
                "height": "sm"
            }
        ]),
        create_separator(colors),
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    card = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
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
        alt_text="مساعدة",
        contents=FlexContainer.from_dict(card)
    )

# ============================================================================
# Build Games Menu
# ============================================================================
def build_games_menu(theme="💜"):
    """بناء قائمة الألعاب"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # أزرار الألعاب (3 في كل صف)
    games = list(GAME_LIST.items())
    game_buttons = []
    
    for i in range(0, len(games), 3):
        row_games = games[i:i+3]
        buttons = []
        for game_key, game_info in row_games:
            buttons.append({
                "type": "button",
                "action": {
                    "type": "message",
                    "label": f"{game_info['icon']} {game_info['label']}",
                    "text": f"لعبة {game_key}"
                },
                "style": "secondary",
                "height": "sm",
                "color": colors["primary"]
            })
        game_buttons.append(create_button_row(buttons))
    
    # بطاقة التعليمات
    instructions = {
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
        "paddingAll": "15px",
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }
    
    # المحتوى
    contents = [
        create_header("🎮 الألعاب المتاحة", f"{len(GAME_LIST)} لعبة مختلفة", colors),
        create_separator(colors)
    ] + game_buttons + [
        create_separator(colors, "
