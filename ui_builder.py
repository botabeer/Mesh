"""
Bot Mesh - UI Builder v10.0 GLASS DESIGN
Created by: Abeer Aldosari © 2025
✅ تصميم زجاجي احترافي 100%
✅ جميع النوافذ Flex
✅ Quick Reply للألعاب فقط
✅ متوافق تماماً مع LINE Flex Message
"""

from typing import List, Optional, Dict, Any, Tuple

from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    MessageAction
)

from constants import (
    BOT_NAME,
    BOT_VERSION,
    BOT_RIGHTS,
    THEMES,
    DEFAULT_THEME,
    GAME_LIST
)

# ============================================================================
# GLASS THEME SYSTEM - 9 ثيمات زجاجية احترافية
# ============================================================================

GLASS_THEMES = {
    "أبيض": {
        "bg": "#F8FAFC",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_alpha": "#F8FAFC",
        "primary": "#3B82F6",
        "secondary": "#60A5FA",
        "accent": "#2563EB",
        "text": "#1E293B",
        "text2": "#64748B",
        "text3": "#94A3B8",
        "border": "#E2E8F0",
        "shadow": "#CBD5E1",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "info": "#3B82F6"
    },
    "أسود": {
        "bg": "#0F172A",
        "card": "#1E293B",
        "glass": "#1E293B",
        "glass_alpha": "#0F172A",
        "primary": "#60A5FA",
        "secondary": "#93C5FD",
        "accent": "#3B82F6",
        "text": "#F1F5F9",
        "text2": "#CBD5E1",
        "text3": "#94A3B8",
        "border": "#334155",
        "shadow": "#0F172A",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "info": "#60A5FA"
    },
    "رمادي": {
        "bg": "#F9FAFB",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_alpha": "#F3F4F6",
        "primary": "#6B7280",
        "secondary": "#9CA3AF",
        "accent": "#4B5563",
        "text": "#111827",
        "text2": "#6B7280",
        "text3": "#9CA3AF",
        "border": "#E5E7EB",
        "shadow": "#D1D5DB",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "info": "#6B7280"
    },
    "أزرق": {
        "bg": "#EFF6FF",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_alpha": "#DBEAFE",
        "primary": "#2563EB",
        "secondary": "#3B82F6",
        "accent": "#1D4ED8",
        "text": "#1E3A8A",
        "text2": "#3B82F6",
        "text3": "#60A5FA",
        "border": "#BFDBFE",
        "shadow": "#93C5FD",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "info": "#3B82F6"
    },
    "بنفسجي": {
        "bg": "#F5F3FF",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_alpha": "#EDE9FE",
        "primary": "#8B5CF6",
        "secondary": "#A78BFA",
        "accent": "#7C3AED",
        "text": "#4C1D95",
        "text2": "#7C3AED",
        "text3": "#A78BFA",
        "border": "#DDD6FE",
        "shadow": "#C4B5FD",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "info": "#8B5CF6"
    },
    "وردي": {
        "bg": "#FDF2F8",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_alpha": "#FCE7F3",
        "primary": "#EC4899",
        "secondary": "#F472B6",
        "accent": "#DB2777",
        "text": "#831843",
        "text2": "#DB2777",
        "text3": "#F472B6",
        "border": "#FBCFE8",
        "shadow": "#F9A8D4",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "info": "#EC4899"
    },
    "أخضر": {
        "bg": "#F0FDF4",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_alpha": "#DCFCE7",
        "primary": "#10B981",
        "secondary": "#34D399",
        "accent": "#059669",
        "text": "#064E3B",
        "text2": "#059669",
        "text3": "#34D399",
        "border": "#BBF7D0",
        "shadow": "#86EFAC",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "info": "#10B981"
    },
    "برتقالي": {
        "bg": "#FFF7ED",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_alpha": "#FFEDD5",
        "primary": "#F97316",
        "secondary": "#FB923C",
        "accent": "#EA580C",
        "text": "#7C2D12",
        "text2": "#EA580C",
        "text3": "#FB923C",
        "border": "#FED7AA",
        "shadow": "#FDBA74",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "info": "#F97316"
    },
    "بني": {
        "bg": "#FEFCF9",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_alpha": "#F5E6D8",
        "primary": "#92400E",
        "secondary": "#B45309",
        "accent": "#78350F",
        "text": "#451A03",
        "text2": "#92400E",
        "text3": "#B45309",
        "border": "#E7D4C3",
        "shadow": "#D4B8A0",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "info": "#92400E"
    }
}


def get_theme(theme_name: str = DEFAULT_THEME) -> Dict[str, str]:
    """الحصول على ألوان الثيم بشكل آمن"""
    return GLASS_THEMES.get(theme_name, GLASS_THEMES[DEFAULT_THEME])


# ============================================================================
# QUICK REPLY SYSTEM - للألعاب فقط
# ============================================================================

def create_games_quick_reply() -> QuickReply:
    """إنشاء Quick Reply للألعاب فقط (13 لعبة)"""
    try:
        items = []
        for _, display_name, icon in GAME_LIST[:13]:
            items.append(
                QuickReplyItem(
                    action=MessageAction(
                        label=f"{icon} {display_name}",
                        text=display_name
                    )
                )
            )
        return QuickReply(items=items)
    except Exception:
        return QuickReply(items=[])


def attach_quick_reply(message):
    """إضافة Quick Reply لأي رسالة"""
    try:
        message.quick_reply = create_games_quick_reply()
    except:
        pass
    return message


# ============================================================================
# GLASS COMPONENTS - مكونات زجاجية قابلة لإعادة الاستخدام
# ============================================================================

def create_glass_card(contents: List[Dict], colors: Dict, with_shadow: bool = True) -> Dict:
    """إنشاء بطاقة زجاجية احترافية"""
    card = {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "backgroundColor": colors["glass"],
        "cornerRadius": "20px",
        "paddingAll": "20px",
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }
    return card


def create_header_section(title: str, subtitle: str, icon: str, colors: Dict) -> List[Dict]:
    """إنشاء header احترافي"""
    return [
        # الأيقونة
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": icon,
                    "size": "xxl",
                    "align": "center",
                    "color": colors["primary"]
                }
            ],
            "paddingAll": "10px",
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "20px",
            "margin": "none"
        },
        # العنوان
        {
            "type": "text",
            "text": title,
            "size": "xl",
            "weight": "bold",
            "color": colors["text"],
            "align": "center",
            "margin": "md"
        },
        # العنوان الفرعي
        {
            "type": "text",
            "text": subtitle,
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "margin": "xs",
            "wrap": True
        },
        # فاصل أنيق
        {
            "type": "separator",
            "margin": "lg",
            "color": colors["border"]
        }
    ]


def create_stat_box(label: str, value: str, icon: str, colors: Dict) -> Dict:
    """صندوق إحصائيات زجاجي"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": icon,
                "size": "lg",
                "align": "center",
                "color": colors["primary"]
            },
            {
                "type": "text",
                "text": value,
                "size": "xl",
                "weight": "bold",
                "align": "center",
                "color": colors["text"],
                "margin": "xs"
            },
            {
                "type": "text",
                "text": label,
                "size": "xs",
                "align": "center",
                "color": colors["text3"],
                "margin": "xs"
            }
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "15px",
        "paddingAll": "15px",
        "flex": 1
    }


def create_button(label: str, text: str, style: str, colors: Dict, icon: str = None) -> Dict:
    """زر زجاجي احترافي"""
    if icon:
        label = f"{icon} {label}"
    
    button = {
        "type": "button",
        "action": {
            "type": "message",
            "label": label,
            "text": text
        },
        "height": "sm",
        "style": style
    }
    
    if style == "primary":
        button["color"] = colors["primary"]
    elif style == "secondary":
        button["color"] = colors["secondary"]
    
    return button


def create_info_row(label: str, value: str, colors: Dict) -> Dict:
    """صف معلومات أنيق"""
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": label,
                "size": "sm",
                "color": colors["text2"],
                "flex": 0
            },
            {
                "type": "text",
                "text": value,
                "size": "sm",
                "color": colors["text"],
                "align": "end",
                "weight": "bold"
            }
        ],
        "margin": "md"
    }


# ============================================================================
# MAIN SCREENS - الشاشات الرئيسية
# ============================================================================

def build_enhanced_home(username: str, points: int, is_registered: bool, theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏠 الصفحة الرئيسية - تصميم زجاجي فاخر"""
    colors = get_theme(theme)
    
    # محتوى البطاقة
    contents = []
    
    # Header
    contents.extend(create_header_section(
        title=f"مرحباً {username}",
        subtitle=f"🎮 {BOT_NAME} v{BOT_VERSION}",
        icon="👋",
        colors=colors
    ))
    
    # صندوق النقاط البارز
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "⭐",
                "size": "xl",
                "align": "center",
                "color": colors["warning"]
            },
            {
                "type": "text",
                "text": str(points),
                "size": "xxl",
                "weight": "bold",
                "align": "center",
                "color": colors["primary"],
                "margin": "xs"
            },
            {
                "type": "text",
                "text": "نقاطك الإجمالية",
                "size": "xs",
                "align": "center",
                "color": colors["text3"],
                "margin": "xs"
            }
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "20px",
        "margin": "lg"
    })
    
    # الأزرار
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            create_button("الألعاب", "ألعاب", "primary", colors, "🎮"),
            create_button("نقاطي", "نقاطي", "link", colors, "⭐"),
            create_button("الصدارة", "صدارة", "link", colors, "🏆"),
            create_button("الثيمات", "ثيمات", "link", colors, "🎨")
        ],
        "spacing": "sm",
        "margin": "lg"
    })
    
    # Footer
    contents.append({
        "type": "text",
        "text": BOT_RIGHTS,
        "size": "xxs",
        "color": colors["text3"],
        "align": "center",
        "margin": "lg",
        "wrap": True
    })
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "0px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="🏠 الصفحة الرئيسية", contents=FlexContainer.from_dict(bubble))
    )


def build_games_menu(theme: str = DEFAULT_THEME) -> FlexMessage:
    """🎮 قائمة الألعاب - شبكة احترافية"""
    colors = get_theme(theme)
    
    contents = []
    
    # Header
    contents.extend(create_header_section(
        title="الألعاب المتاحة",
        subtitle=f"اختر لعبتك المفضلة",
        icon="🎮",
        colors=colors
    ))
    
    # الألعاب في شبكة 2×2
    row_contents = []
    for i, (_, display_name, icon) in enumerate(GAME_LIST):
        game_box = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": icon,
                    "size": "xxl",
                    "align": "center",
                    "color": colors["primary"]
                },
                {
                    "type": "text",
                    "text": display_name,
                    "size": "xs",
                    "align": "center",
                    "color": colors["text"],
                    "margin": "sm",
                    "wrap": True,
                    "weight": "bold"
                }
            ],
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "action": {
                "type": "message",
                "text": display_name
            },
            "flex": 1,
            "spacing": "xs"
        }
        
        row_contents.append(game_box)
        
        # كل صفين نضيف row
        if (i + 1) % 2 == 0 or i == len(GAME_LIST) - 1:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": row_contents.copy(),
                "spacing": "sm",
                "margin": "md"
            })
            row_contents.clear()
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="🎮 الألعاب", contents=FlexContainer.from_dict(bubble))
    )


def build_my_points(username: str, total_points: int, stats: Dict, theme: str = DEFAULT_THEME) -> FlexMessage:
    """⭐ نقاطي - لوحة إحصائيات شاملة"""
    colors = get_theme(theme)
    
    contents = []
    
    # Header
    contents.extend(create_header_section(
        title="نقاطي",
        subtitle=f"ملف {username}",
        icon="⭐",
        colors=colors
    ))
    
    # صندوق النقاط الكبير
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "🏆",
                "size": "xxl",
                "align": "center"
            },
            {
                "type": "text",
                "text": str(total_points),
                "size": "xxl",
                "weight": "bold",
                "align": "center",
                "color": colors["primary"],
                "margin": "sm"
            },
            {
                "type": "text",
                "text": "النقاط الإجمالية",
                "size": "sm",
                "align": "center",
                "color": colors["text2"],
                "margin": "xs"
            }
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "25px",
        "margin": "lg"
    })
    
    # إحصائيات الألعاب
    if stats:
        contents.append({
            "type": "text",
            "text": "📊 إحصائيات الألعاب",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "xl"
        })
        
        for game_name, data in list(stats.items())[:5]:
            contents.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": game_name,
                                "size": "sm",
                                "weight": "bold",
                                "color": colors["text"],
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": f"{data.get('total_score', 0)} نقطة",
                                "size": "sm",
                                "color": colors["primary"],
                                "align": "end",
                                "weight": "bold"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"🎮 {data.get('plays', 0)} لعبة",
                                "size": "xs",
                                "color": colors["text3"]
                            },
                            {
                                "type": "text",
                                "text": f"🏆 {data.get('wins', 0)} فوز",
                                "size": "xs",
                                "color": colors["success"],
                                "align": "end"
                            }
                        ],
                        "margin": "xs"
                    }
                ],
                "backgroundColor": colors["glass_alpha"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "margin": "sm"
            })
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="⭐ نقاطي", contents=FlexContainer.from_dict(bubble))
    )


def build_leaderboard(top_users: List[Tuple[str, int]], theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏆 الصدارة - لوحة المتصدرين"""
    colors = get_theme(theme)
    
    contents = []
    
    # Header
    contents.extend(create_header_section(
        title="لوحة الصدارة",
        subtitle="أفضل اللاعبين",
        icon="🏆",
        colors=colors
    ))
    
    # أفضل 3 لاعبين - تصميم خاص
    medals = ["🥇", "🥈", "🥉"]
    medal_colors = [colors["warning"], colors["text3"], colors["secondary"]]
    
    for i in range(min(3, len(top_users))):
        name, pts = top_users[i]
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": medals[i],
                            "size": "xl",
                            "align": "center"
                        }
                    ],
                    "backgroundColor": colors["glass_alpha"],
                    "cornerRadius": "12px",
                    "paddingAll": "10px",
                    "flex": 0,
                    "width": "50px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": name,
                            "size": "md",
                            "weight": "bold",
                            "color": colors["text"]
                        },
                        {
                            "type": "text",
                            "text": f"{pts} نقطة",
                            "size": "sm",
                            "color": medal_colors[i],
                            "weight": "bold"
                        }
                    ],
                    "margin": "md"
                }
            ],
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "margin": "md"
        })
    
    # باقي اللاعبين
    if len(top_users) > 3:
        contents.append({
            "type": "separator",
            "margin": "lg",
            "color": colors["border"]
        })
        
        for i in range(3, min(10, len(top_users))):
            name, pts = top_users[i]
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{i + 1}.",
                        "size": "sm",
                        "color": colors["text2"],
                        "flex": 0,
                        "width": "30px"
                    },
                    {
                        "type": "text",
                        "text": name,
                        "size": "sm",
                        "color": colors["text"]
                    },
                    {
                        "type": "text",
                        "text": f"{pts}",
                        "size": "sm",
                        "color": colors["primary"],
                        "align": "end",
                        "weight": "bold"
                    }
                ],
                "margin": "md"
            })
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="🏆 الصدارة", contents=FlexContainer.from_dict(bubble))
    )


def build_theme_selector(current_theme: str = DEFAULT_THEME) -> FlexMessage:
    """🎨 اختيار الثيم - معرض الثيمات"""
    colors = get_theme(current_theme)
    
    contents = []
    
    # Header
    contents.extend(create_header_section(
        title="اختر الثيم",
        subtitle="غيّر مظهر البوت",
        icon="🎨",
        colors=colors
    ))
    
    # الثيمات في شبكة 3×3
    row_contents = []
    for i, (theme_name, theme_colors) in enumerate(GLASS_THEMES.items()):
        is_selected = theme_name == current_theme
        
        theme_box = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "filler"
                        }
                    ],
                    "backgroundColor": theme_colors["primary"],
                    "cornerRadius": "8px",
                    "height": "30px"
                },
                {
                    "type": "text",
                    "text": "✓" if is_selected else theme_name,
                    "size": "xs",
                    "align": "center",
                    "color": colors["text"],
                    "margin": "sm",
                    "weight": "bold" if is_selected else "regular"
                }
            ],
            "backgroundColor": theme_colors["glass_alpha"] if is_selected else colors["glass_alpha"],
            "cornerRadius": "12px",
            "paddingAll": "10px",
            "action": {
                "type": "message",
                "text": f"ثيم {theme_name}"
            },
            "flex": 1,
            "borderWidth": "2px" if is_selected else "0px",
            "borderColor": colors["primary"] if is_selected else colors["border"]
        }
        
        row_contents.append(theme_box)
        
        # كل 3 ثيمات نضيف row
        if (i + 1) % 3 == 0 or i == len(GLASS_THEMES) - 1:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": row_contents.copy(),
                "spacing": "sm",
                "margin": "md"
            })
            row_contents.clear()
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="🎨 الثيمات", contents=FlexContainer.from_dict(bubble))
    )


def build_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """❓ المساعدة - دليل شامل"""
    colors = get_theme(theme)
    
    contents = []
    
    # Header
    contents.extend(create_header_section(
        title="المساعدة",
        subtitle="دليل استخدام البوت",
        icon="❓",
        colors=colors
    ))
    
    # الأوامر
    commands = [
        ("🎮", "ألعاب", "عرض قائمة الألعاب"),
        ("⭐", "نقاطي", "عرض نقاطك وإحصائياتك"),
        ("🏆", "صدارة", "عرض لوحة المتصدرين"),
        ("🎨", "ثيمات", "تغيير مظهر البوت"),
        ("✅", "انضم", "التسجيل في البوت"),
        ("👥", "فريقين", "بدء لعبة جماعية"),
        ("⛔", "إيقاف", "إيقاف اللعبة الحالية"),
        ("🏠", "بداية", "العودة للصفحة الرئيسية")
    ]
    
    for icon, cmd, desc in commands:
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": icon,
                            "size": "xl",
                            "align": "center"
                        }
                    ],
                    "backgroundColor": colors["glass_alpha"],
                    "cornerRadius": "10px",
                    "paddingAll": "8px",
                    "flex": 0,
                    "width": "45px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": cmd,
                            "size": "md",
                            "weight": "bold",
                            "color": colors["text"]
                        },
                        {
                            "type": "text",
                            "text": desc,
                            "size": "xs",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "xs"
                        }
                    ],
                    "margin": "md"
                }
            ],
            "margin": "md"
        })
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="❓ المساعدة", contents=FlexContainer.from_dict(bubble))
    )


def build_multiplayer_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """👥 مساعدة الفرق - شرح وضع الفريقين"""
    colors = get_theme(theme)
    
    contents = []
    
    # Header
    contents.extend(create_header_section(
        title="وضع الفريقين",
        subtitle="العب مع أصدقائك",
        icon="👥",
        colors=colors
    ))
    
    # الخطوات
    steps = [
        {
            "number": "1",
            "title": "اكتب: فريقين",
            "desc": "لبدء مرحلة الانضمام في المجموعة",
            "icon": "🎯"
        },
        {
            "number": "2",
            "title": "اكتب: انضم",
            "desc": "كل شخص يكتب انضم للمشاركة",
            "icon": "✅"
        },
        {
            "number": "3",
            "title": "اختر اللعبة",
            "desc": "سيتم تقسيم الفرق تلقائياً",
            "icon": "🎮"
        }
    ]
    
    for step in steps:
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": step["icon"],
                            "size": "xl",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": step["number"],
                            "size": "xs",
                            "align": "center",
                            "color": colors["text3"],
                            "margin": "xs"
                        }
                    ],
                    "backgroundColor": colors["glass_alpha"],
                    "cornerRadius": "12px",
                    "paddingAll": "12px",
                    "flex": 0,
                    "width": "55px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": step["title"],
                            "size": "md",
                            "weight": "bold",
                            "color": colors["text"]
                        },
                        {
                            "type": "text",
                            "text": step["desc"],
                            "size": "xs",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "xs"
                        }
                    ],
                    "margin": "md"
                }
            ],
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "margin": "md"
        })
    
    # ملاحظة مهمة
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "💡 ملاحظة",
                "size": "sm",
                "weight": "bold",
                "color": colors["info"]
            },
            {
                "type": "text",
                "text": "وضع الفريقين متاح في المجموعات فقط",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True,
                "margin": "xs"
            }
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "12px",
        "paddingAll": "12px",
        "margin": "lg",
        "borderWidth": "1px",
        "borderColor": colors["info"]
    })
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="👥 وضع الفريقين", contents=FlexContainer.from_dict(bubble))
    )


def build_registration_required(theme: str = DEFAULT_THEME) -> FlexMessage:
    """⚠️ تطلب التسجيل"""
    colors = get_theme(theme)
    
    contents = [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "⚠️",
                    "size": "xxl",
                    "align": "center",
                    "color": colors["warning"]
                }
            ],
            "paddingAll": "15px",
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "20px"
        },
        {
            "type": "text",
            "text": "يجب التسجيل أولاً",
            "size": "xl",
            "weight": "bold",
            "color": colors["text"],
            "align": "center",
            "margin": "lg"
        },
        {
            "type": "text",
            "text": "سجّل الآن للعب الألعاب وكسب النقاط",
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "wrap": True,
            "margin": "md"
        },
        {
            "type": "separator",
            "margin": "lg",
            "color": colors["border"]
        },
        create_button("انضم الآن", "انضم", "primary", colors, "✅")
    ]
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "25px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="⚠️ تسجيل مطلوب", contents=FlexContainer.from_dict(bubble))
    )


def build_registration_success(username: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """✅ نجح التسجيل"""
    colors = get_theme(theme)
    
    contents = [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎉",
                    "size": "xxl",
                    "align": "center"
                }
            ],
            "paddingAll": "15px",
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "20px"
        },
        {
            "type": "text",
            "text": "مرحباً بك!",
            "size": "xl",
            "weight": "bold",
            "color": colors["success"],
            "align": "center",
            "margin": "lg"
        },
        {
            "type": "text",
            "text": f"تم تسجيل {username} بنجاح",
            "size": "md",
            "color": colors["text"],
            "align": "center",
            "wrap": True,
            "margin": "md"
        },
        {
            "type": "separator",
            "margin": "lg",
            "color": colors["border"]
        },
        {
            "type": "text",
            "text": "الآن يمكنك:",
            "size": "sm",
            "color": colors["text2"],
            "margin": "lg"
        },
        {
            "type": "text",
            "text": "🎮 لعب جميع الألعاب\n⭐ كسب النقاط\n🏆 المنافسة في الصدارة",
            "size": "sm",
            "color": colors["text"],
            "wrap": True,
            "margin": "md"
        },
        create_button("ابدأ اللعب", "ألعاب", "primary", colors, "🎮")
    ]
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "25px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="✅ تم التسجيل", contents=FlexContainer.from_dict(bubble))
    )


def build_join_confirmation(username: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """✅ تأكيد الانضمام للفريق"""
    colors = get_theme(theme)
    
    contents = [
        {
            "type": "text",
            "text": "✅",
            "size": "xxl",
            "align": "center",
            "color": colors["success"]
        },
        {
            "type": "text",
            "text": "انضممت للعبة",
            "size": "lg",
            "weight": "bold",
            "color": colors["text"],
            "align": "center",
            "margin": "md"
        },
        {
            "type": "text",
            "text": f"{username} جاهز للعب",
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "margin": "sm"
        }
    ]
    
    bubble = {
        "type": "bubble",
        "size": "nano",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="✅ انضممت", contents=FlexContainer.from_dict(bubble))
    )


def build_winner_announcement(username: str, game_name: str, points: int, total_points: int, theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏆 إعلان الفائز - تصميم احتفالي"""
    colors = get_theme(theme)
    
    contents = [
        # التاج
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "👑",
                    "size": "xxl",
                    "align": "center"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "25px"
        },
        {
            "type": "text",
            "text": "مبروك!",
            "size": "xxl",
            "weight": "bold",
            "color": colors["success"],
            "align": "center",
            "margin": "lg"
        },
        {
            "type": "separator",
            "margin": "lg",
            "color": colors["border"]
        },
        # بطاقة الفائز
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🏆 الفائز",
                    "size": "sm",
                    "color": colors["text3"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": username,
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["text"],
                    "align": "center",
                    "margin": "sm"
                }
            ],
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "margin": "lg"
        },
        # تفاصيل اللعبة
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                create_stat_box("اللعبة", game_name, "🎮", colors),
                create_stat_box("النقاط", f"+{points}", "⭐", colors)
            ],
            "spacing": "sm",
            "margin": "lg"
        },
        # الإجمالي
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "إجمالي النقاط",
                    "size": "xs",
                    "color": colors["text3"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": str(total_points),
                    "size": "xxl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center",
                    "margin": "xs"
                }
            ],
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "margin": "lg"
        },
        create_button("لعبة جديدة", "ألعاب", "primary", colors, "🎮")
    ]
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "25px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="🏆 مبروك الفوز", contents=FlexContainer.from_dict(bubble))
    )


def build_team_game_end(team_points: Dict[str, int], theme: str = DEFAULT_THEME) -> FlexMessage:
    """👥 نهاية لعبة الفريقين"""
    colors = get_theme(theme)
    
    team1_pts = team_points.get("team1", 0)
    team2_pts = team_points.get("team2", 0)
    
    if team1_pts > team2_pts:
        winner = "الفريق الأول 🥇"
        winner_color = colors["success"]
    elif team2_pts > team1_pts:
        winner = "الفريق الثاني 🥈"
        winner_color = colors["info"]
    else:
        winner = "تعادل ⚖️"
        winner_color = colors["warning"]
    
    contents = [
        {
            "type": "text",
            "text": "🏁",
            "size": "xxl",
            "align": "center"
        },
        {
            "type": "text",
            "text": "انتهت اللعبة",
            "size": "xl",
            "weight": "bold",
            "color": colors["text"],
            "align": "center",
            "margin": "md"
        },
        {
            "type": "separator",
            "margin": "lg",
            "color": colors["border"]
        },
        # النتيجة
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔵",
                            "size": "xl",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "الفريق الأول",
                            "size": "xs",
                            "align": "center",
                            "color": colors["text3"],
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": str(team1_pts),
                            "size": "xxl",
                            "weight": "bold",
                            "align": "center",
                            "color": colors["primary"],
                            "margin": "xs"
                        }
                    ],
                    "backgroundColor": colors["glass_alpha"],
                    "cornerRadius": "15px",
                    "paddingAll": "15px",
                    "flex": 1
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🔴",
                            "size": "xl",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "الفريق الثاني",
                            "size": "xs",
                            "align": "center",
                            "color": colors["text3"],
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": str(team2_pts),
                            "size": "xxl",
                            "weight": "bold",
                            "align": "center",
                            "color": colors["error"],
                            "margin": "xs"
                        }
                    ],
                    "backgroundColor": colors["glass_alpha"],
                    "cornerRadius": "15px",
                    "paddingAll": "15px",
                    "flex": 1
                }
            ],
            "spacing": "sm",
            "margin": "lg"
        },
        # الفائز
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "الفائز",
                    "size": "sm",
                    "color": colors["text3"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": winner,
                    "size": "lg",
                    "weight": "bold",
                    "color": winner_color,
                    "align": "center",
                    "margin": "sm"
                }
            ],
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "margin": "lg"
        }
    ]
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "25px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="🏁 نهاية اللعبة", contents=FlexContainer.from_dict(bubble))
    )


def build_theme_change_success(theme_name: str, theme: str) -> FlexMessage:
    """✅ تغيير الثيم بنجاح"""
    colors = get_theme(theme)
    
    contents = [
        {
            "type": "text",
            "text": "🎨",
            "size": "xxl",
            "align": "center"
        },
        {
            "type": "text",
            "text": "تم تغيير الثيم",
            "size": "lg",
            "weight": "bold",
            "color": colors["success"],
            "align": "center",
            "margin": "md"
        },
        {
            "type": "text",
            "text": f"الثيم الجديد: {theme_name}",
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "margin": "sm"
        }
    ]
    
    bubble = {
        "type": "bubble",
        "size": "nano",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="✅ تم التغيير", contents=FlexContainer.from_dict(bubble))
    )


def build_game_stopped(game_name: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """⛔ إيقاف اللعبة"""
    colors = get_theme(theme)
    
    contents = [
        {
            "type": "text",
            "text": "⛔",
            "size": "xxl",
            "align": "center",
            "color": colors["error"]
        },
        {
            "type": "text",
            "text": "تم إيقاف اللعبة",
            "size": "lg",
            "weight": "bold",
            "color": colors["text"],
            "align": "center",
            "margin": "md"
        },
        {
            "type": "text",
            "text": f"تم إيقاف: {game_name}",
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "margin": "sm"
        }
    ]
    
    bubble = {
        "type": "bubble",
        "size": "nano",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="⛔ تم الإيقاف", contents=FlexContainer.from_dict(bubble))
    )


def build_error_message(message: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """❌ رسالة خطأ"""
    colors = get_theme(theme)
    
    contents = [
        {
            "type": "text",
            "text": "❌",
            "size": "xl",
            "align": "center",
            "color": colors["error"]
        },
        {
            "type": "text",
            "text": message,
            "size": "md",
            "color": colors["text"],
            "align": "center",
            "wrap": True,
            "margin": "md"
        }
    ]
    
    bubble = {
        "type": "bubble",
        "size": "nano",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="❌ خطأ", contents=FlexContainer.from_dict(bubble))
    )


def build_answer_feedback(message: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """💬 رد على الإجابة"""
    colors = get_theme(theme)
    
    is_correct = "✅" in message or "صحيح" in message
    icon = "✅" if is_correct else "❌"
    icon_color = colors["success"] if is_correct else colors["error"]
    
    contents = [
        {
            "type": "text",
            "text": icon,
            "size": "xl",
            "align": "center",
            "color": icon_color
        },
        {
            "type": "text",
            "text": message,
            "size": "md",
            "color": colors["text"],
            "align": "center",
            "wrap": True,
            "margin": "md"
        }
    ]
    
    bubble = {
        "type": "bubble",
        "size": "nano",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text=message, contents=FlexContainer.from_dict(bubble))
    )


# ============================================================================
# التصدير
# ============================================================================

__all__ = [
    "get_theme",
    "attach_quick_reply",
    "create_games_quick_reply",
    "build_enhanced_home",
    "build_games_menu",
    "build_my_points",
    "build_leaderboard",
    "build_theme_selector",
    "build_help_window",
    "build_multiplayer_help_window",
    "build_registration_required",
    "build_registration_success",
    "build_join_confirmation",
    "build_winner_announcement",
    "build_team_game_end",
    "build_theme_change_success",
    "build_game_stopped",
    "build_error_message",
    "build_answer_feedback"
]
