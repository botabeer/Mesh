"""
Bot Mesh - UI Builder v9.0 FULL FLEX
Created by: Abeer Aldosari © 2025
✅ كل شيء نوافذ Flex + أزرار
✅ Quick Reply دائم للألعاب فقط
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
    GAME_LIST,
    get_theme_colors
)

# ============================================================================
# Utility Functions
# ============================================================================

def _safe_get_colors(theme: str) -> Dict[str, str]:
    """الحصول على الألوان بأمان"""
    try:
        return get_theme_colors(theme)
    except Exception:
        return get_theme_colors(DEFAULT_THEME)


# ============================================================================
# Quick Reply System - GAMES ONLY
# ============================================================================

def create_games_quick_reply() -> QuickReply:
    """إنشاء Quick Reply للألعاب فقط"""
    try:
        items = []
        for game_data in GAME_LIST:
            if len(game_data) >= 3:
                _, display_name, icon = game_data[:3]
                items.append(
                    QuickReplyItem(
                        action=MessageAction(
                            label=f"{icon} {display_name}",
                            text=display_name
                        )
                    )
                )
        return QuickReply(items=items[:13])
    except Exception:
        return QuickReply(items=[])


def attach_quick_reply_to_message(message):
    """إضافة Quick Reply للألعاب فقط إلى أي رسالة"""
    try:
        qr = create_games_quick_reply()
        message.quick_reply = qr
    except Exception:
        pass
    return message


# Alias for compatibility
attach_quick_reply = attach_quick_reply_to_message


# ============================================================================
# Glass Components
# ============================================================================

def create_glass_button(label: str, text: str, style: str = "primary") -> Dict:
    """إنشاء زر"""
    return {
        "type": "button",
        "action": {
            "type": "message",
            "label": label,
            "text": text
        },
        "style": style,
        "height": "sm",
        "margin": "sm"
    }


# ============================================================================
# نافذة البداية الرئيسية
# ============================================================================

def build_enhanced_home(username: str, points: int, is_registered: bool, theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة البداية - كل شيء أزرار"""
    colors = _safe_get_colors(theme)

    # التسجيل أو معلومات المستخدم
    status_section = []
    if not is_registered:
        status_section = [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "⚠️ غير مسجل",
                        "size": "sm",
                        "color": colors["warning"],
                        "align": "center",
                        "weight": "bold"
                    }
                ],
                "backgroundColor": colors["glass"],
                "cornerRadius": "10px",
                "paddingAll": "10px",
                "margin": "md"
            },
            create_glass_button("✅ انضم للبوت", "انضم", "primary")
        ]
    else:
        status_section = [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"⭐ {points}",
                        "size": "xxl",
                        "color": colors["primary"],
                        "align": "center",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": "نقاطك الحالية",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "xs"
                    }
                ],
                "backgroundColor": colors["glass"],
                "cornerRadius": "15px",
                "paddingAll": "15px",
                "margin": "md"
            }
        ]

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # العنوان
                {
                    "type": "text",
                    "text": "🎮",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": BOT_NAME,
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": f"مرحباً {username}",
                    "size": "md",
                    "color": colors["text"],
                    "align": "center",
                    "margin": "xs"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                
                # حالة المستخدم
                *status_section,
                
                {
                    "type": "separator",
                    "margin": "lg"
                },
                
                # الأزرار الرئيسية
                create_glass_button("🎮 الألعاب", "ألعاب", "primary"),
                create_glass_button("📊 نقاطي", "نقاطي", "link"),
                create_glass_button("🏆 الصدارة", "صدارة", "link"),
                create_glass_button("🎨 الثيمات", "ثيمات", "link"),
                create_glass_button("❓ مساعدة", "مساعدة", "link"),
                
                # حقوق النشر
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "color": colors["text2"],
                    "align": "center",
                    "margin": "lg",
                    "wrap": True
                }
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="البداية", contents=FlexContainer.from_dict(bubble))
    )


# ============================================================================
# نافذة الألعاب
# ============================================================================

def build_games_menu(theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة الألعاب - كل لعبة زر"""
    colors = _safe_get_colors(theme)

    game_buttons = []
    for _, display_name, icon in GAME_LIST:
        game_buttons.append(
            create_glass_button(f"{icon} {display_name}", display_name, "link")
        )

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎮 قائمة الألعاب",
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"عدد الألعاب: {len(GAME_LIST)}",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center",
                    "margin": "xs"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                
                *game_buttons,
                
                {
                    "type": "separator",
                    "margin": "lg"
                },
                create_glass_button("🏠 الرئيسية", "بداية", "primary")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="الألعاب", contents=FlexContainer.from_dict(bubble))
    )


# ============================================================================
# نافذة النقاط
# ============================================================================

def build_my_points(username: str, total_points: int, stats: Dict, theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة النقاط"""
    colors = _safe_get_colors(theme)

    # إحصائيات الألعاب
    stats_content = []
    if stats:
        stats_content.append({
            "type": "text",
            "text": "📊 إحصائيات الألعاب",
            "weight": "bold",
            "size": "md",
            "margin": "lg"
        })
        
        for game_name, data in list(stats.items())[:5]:
            stats_content.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": game_name,
                        "size": "sm",
                        "weight": "bold",
                        "color": colors["text"]
                    },
                    {
                        "type": "text",
                        "text": f"مرات اللعب: {data.get('plays', 0)} | النقاط: {data.get('total_score', 0)}",
                        "size": "xs",
                        "color": colors["text2"],
                        "wrap": True
                    }
                ],
                "backgroundColor": colors["glass"],
                "cornerRadius": "8px",
                "paddingAll": "10px",
                "margin": "sm"
            })

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "⭐",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "نقاطي",
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                
                # بطاقة النقاط
                {
                    "type": "box",
                    "layout": "vertical",
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
                            "text": f"{total_points}",
                            "size": "xxl",
                            "weight": "bold",
                            "color": colors["success"],
                            "align": "center",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "النقاط الإجمالية",
                            "size": "xs",
                            "color": colors["text2"],
                            "align": "center",
                            "margin": "xs"
                        }
                    ],
                    "backgroundColor": colors["glass"],
                    "cornerRadius": "15px",
                    "paddingAll": "20px",
                    "margin": "lg"
                },
                
                *stats_content,
                
                {
                    "type": "separator",
                    "margin": "lg"
                },
                create_glass_button("🏠 الرئيسية", "بداية", "primary")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(bubble))
    )


# ============================================================================
# نافذة الصدارة
# ============================================================================

def build_leaderboard(top_users: List[Tuple[str, int]], theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة الصدارة"""
    colors = _safe_get_colors(theme)

    medals = ["🥇", "🥈", "🥉"]
    
    leaderboard_items = []
    for i, (name, pts) in enumerate(top_users[:10]):
        medal = medals[i] if i < 3 else f"{i+1}."
        
        leaderboard_items.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": medal,
                    "size": "lg" if i < 3 else "md",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": name,
                    "size": "md" if i < 3 else "sm",
                    "weight": "bold" if i < 3 else "regular",
                    "flex": 1,
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": str(pts),
                    "size": "md" if i < 3 else "sm",
                    "color": colors["primary"],
                    "align": "end",
                    "flex": 0
                }
            ],
            "backgroundColor": colors["glass"] if i < 3 else "transparent",
            "cornerRadius": "8px",
            "paddingAll": "10px" if i < 3 else "5px",
            "margin": "sm"
        })

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
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
                    "text": "لوحة الصدارة",
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": f"أفضل {len(top_users)} لاعب",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center",
                    "margin": "xs"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                
                *leaderboard_items,
                
                {
                    "type": "separator",
                    "margin": "lg"
                },
                create_glass_button("🏠 الرئيسية", "بداية", "primary")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble))
    )


# ============================================================================
# نافذة الثيمات
# ============================================================================

def build_theme_selector(current_theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة اختيار الثيم"""
    colors = _safe_get_colors(current_theme)

    theme_buttons = []
    for theme_name in THEMES.keys():
        marker = "✓ " if theme_name == current_theme else ""
        style = "primary" if theme_name == current_theme else "link"
        theme_buttons.append(
            create_glass_button(f"{marker}{theme_name}", f"ثيم {theme_name}", style)
        )

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎨",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "اختر الثيم",
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": f"الثيم الحالي: {current_theme}",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center",
                    "margin": "xs"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                
                *theme_buttons,
                
                {
                    "type": "separator",
                    "margin": "lg"
                },
                create_glass_button("🏠 الرئيسية", "بداية", "primary")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="الثيمات", contents=FlexContainer.from_dict(bubble))
    )


# ============================================================================
# نافذة طلب التسجيل
# ============================================================================

def build_registration_required(theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة طلب التسجيل"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
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
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": "للعب الألعاب وكسب النقاط يجب عليك التسجيل في البوت أولاً",
                    "size": "sm",
                    "color": colors["text"],
                    "align": "center",
                    "wrap": True,
                    "margin": "lg"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                create_glass_button("✅ انضم الآن", "انضم", "primary"),
                create_glass_button("🏠 الرئيسية", "بداية", "link")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="التسجيل", contents=FlexContainer.from_dict(bubble))
    )


# ============================================================================
# نافذة إعلان الفائز
# ============================================================================

def build_winner_announcement(username: str, game_name: str, points: int, total_points: int, theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة إعلان الفائز"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
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
                    "text": "مبروك!",
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                
                # بطاقة الفائز
                {
                    "type": "box",
                    "layout": "vertical",
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
                            "text": game_name,
                            "size": "md",
                            "color": colors["text2"],
                            "align": "center",
                            "margin": "sm"
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": f"+{points}",
                            "size": "xxl",
                            "weight": "bold",
                            "color": colors["success"],
                            "align": "center",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "نقطة مكتسبة",
                            "size": "xs",
                            "color": colors["text2"],
                            "align": "center",
                            "margin": "xs"
                        },
                        {
                            "type": "text",
                            "text": f"الإجمالي: {total_points} نقطة",
                            "size": "sm",
                            "color": colors["text"],
                            "align": "center",
                            "margin": "md"
                        }
                    ],
                    "backgroundColor": colors["glass"],
                    "cornerRadius": "15px",
                    "paddingAll": "20px",
                    "margin": "lg"
                },
                
                {
                    "type": "separator",
                    "margin": "lg"
                },
                create_glass_button("🎮 العب مرة أخرى", "ألعاب", "primary"),
                create_glass_button("🏠 الرئيسية", "بداية", "link")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="الفائز", contents=FlexContainer.from_dict(bubble))
    )


# ============================================================================
# نافذة المساعدة
# ============================================================================

def build_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة المساعدة"""
    colors = _safe_get_colors(theme)

    commands = [
        ("🎮 ألعاب", "عرض قائمة الألعاب المتاحة"),
        ("📊 نقاطي", "عرض نقاطك وإحصائياتك"),
        ("🏆 صدارة", "عرض أفضل اللاعبين"),
        ("🎨 ثيمات", "تغيير مظهر البوت"),
        ("✅ انضم", "التسجيل في البوت"),
        ("⛔ إيقاف", "إيقاف اللعبة الحالية"),
        ("🏠 بداية", "العودة للصفحة الرئيسية"),
    ]

    command_items = []
    for cmd, desc in commands:
        command_items.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": cmd,
                    "size": "md",
                    "weight": "bold",
                    "color": colors["primary"]
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
            "backgroundColor": colors["glass"],
            "cornerRadius": "8px",
            "paddingAll": "10px",
            "margin": "sm"
        })

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "❓",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "دليل الأوامر",
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                
                *command_items,
                
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "💡 نصيحة: استخدم Quick Reply أسفل الشاشة لاختيار الألعاب بسرعة",
                    "size": "xs",
                    "color": colors["text2"],
                    "align": "center",
                    "wrap": True,
                    "margin": "md"
                },
                create_glass_button("🏠 الرئيسية", "بداية", "primary")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="المساعدة", contents=FlexContainer.from_dict(bubble))
    )


# ============================================================================
# نافذة مساعدة الفريقين
# ============================================================================

def build_multiplayer_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة مساعدة وضع الفريقين"""
    colors = _safe_get_colors(theme)

    steps = [
        ("1️⃣", "اكتب: فريقين", "لبدء مرحلة الانضمام"),
        ("2️⃣", "اكتب: انضم", "للانضمام للعبة الجماعية"),
        ("3️⃣", "اختر اللعبة", "سيتم تقسيم الفرق تلقائياً"),
    ]

    step_items = []
    for num, title, desc in steps:
        step_items.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"{num} {title}",
                    "size": "md",
                    "weight": "bold",
                    "color": colors["primary"]
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
            "backgroundColor": colors["glass"],
            "cornerRadius": "8px",
            "paddingAll": "10px",
            "margin": "sm"
        })

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "👥",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "وضع الفريقين",
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": "للعب جماعي في المجموعات",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center",
                    "margin": "xs"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                
                *step_items,
                
                {
                    "type": "separator",
                    "margin": "lg"
                },
                create_glass_button("✅ ابدأ الآن", "فريقين", "primary"),
                create_glass_button("🏠 الرئيسية", "بداية", "link")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="وضع الفريقين", contents=FlexContainer.from_dict(bubble))
    )


# ============================================================================
# Export All
# ============================================================================

__all__ = [
    "build_enhanced_home",
    "build_games_menu",
    "build_my_points",
    "build_leaderboard",
    "build_theme_selector",
    "build_registration_required",
    "build_winner_announcement",
    "build_help_window",
    "build_multiplayer_help_window",
    "attach_quick_reply_to_message",
    "create_games_quick_reply"
]
