"""
Bot Mesh - UI Builder v9.1 FULL FLEX FIXED
Created by: Abeer Aldosari © 2025
✅ كل شيء نوافذ Flex + أزرار
✅ Quick Reply دائم للألعاب فقط
✅ جميع الدوال المطلوبة موجودة
✅ إصلاح مشكلة backgroundColor
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


def create_glass_box(contents: List[Dict], colors: Dict, padding: str = "15px") -> Dict:
    """إنشاء صندوق زجاجي بدون backgroundColor"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "cornerRadius": "15px",
        "paddingAll": padding,
        "margin": "md",
        "borderWidth": "1px",
        "borderColor": colors.get("border", "#E2E8F0")
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
                "cornerRadius": "10px",
                "paddingAll": "10px",
                "margin": "md",
                "borderWidth": "1px",
                "borderColor": colors.get("warning", "#F59E0B")
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
                "cornerRadius": "15px",
                "paddingAll": "15px",
                "margin": "md",
                "borderWidth": "2px",
                "borderColor": colors.get("primary", "#3B82F6")
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
            "margin": "lg",
            "color": colors["text"]
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
                "cornerRadius": "8px",
                "paddingAll": "10px",
                "margin": "sm",
                "borderWidth": "1px",
                "borderColor": colors.get("border", "#E2E8F0")
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
                    "cornerRadius": "15px",
                    "paddingAll": "20px",
                    "margin": "lg",
                    "borderWidth": "2px",
                    "borderColor": colors.get("success", "#10B981")
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
                    "margin": "md",
                    "color": colors["text"]
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
            "cornerRadius": "8px" if i < 3 else "0px",
            "paddingAll": "10px" if i < 3 else "5px",
            "margin": "sm",
            "borderWidth": "1px" if i < 3 else "0px",
            "borderColor": colors.get("border", "#E2E8F0") if i < 3 else "#000000"
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
# نافذة نجاح التسجيل
# ============================================================================

def build_registration_success(username: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة نجاح التسجيل"""
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
                    "text": "✅",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "تم التسجيل بنجاح",
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["success"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": f"مرحباً بك {username}",
                    "size": "lg",
                    "color": colors["text"],
                    "align": "center",
                    "margin": "lg",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "يمكنك الآن اللعب وكسب النقاط",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center",
                    "wrap": True,
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                create_glass_button("🎮 ابدأ اللعب", "ألعاب", "primary"),
                create_glass_button("🏠 الرئيسية", "بداية", "link")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="التسجيل", contents=FlexContainer.from_dict(bubble))
    )


# ============================================================================
# نوافذ إضافية
# ============================================================================

def build_join_confirmation(username: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة تأكيد الانضمام"""
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
                    "text": "👥",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "تم الانضمام",
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["success"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": f"{username} انضم للعبة الجماعية",
                    "size": "md",
                    "color": colors["text"],
                    "align": "center",
                    "margin": "lg",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "انتظر الآخرين واختر اللعبة",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center",
                    "wrap": True,
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                create_glass_button("🎮 اختر لعبة", "ألعاب", "primary")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="انضمام", contents=FlexContainer.from_dict(bubble))
    )


def build_error_message(message: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة رسالة خطأ"""
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
                    "text": message,
                    "size": "md",
                    "color": colors["text"],
                    "align": "center",
                    "wrap": True,
                    "margin": "lg"
                },
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
        FlexMessage(alt_text="خطأ", contents=FlexContainer.from_dict(bubble))
    )


def build_theme_change_success(theme_name: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة تأكيد تغيير الثيم"""
    colors = _safe_get_colors(theme_name)

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
                    "text": "تم تغيير الثيم",
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["success"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": f"الثيم الجديد: {theme_name}",
                    "size": "lg",
                    "color": colors["text"],
                    "align": "center",
                    "margin": "lg"
                },
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
        FlexMessage(alt_text="تغيير الثيم", contents=FlexContainer.from_dict(bubble))
    )


def build_game_stopped(game_name: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة إيقاف اللعبة"""
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
                    "text": "⏹️",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "تم إيقاف اللعبة",
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["text"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": f"اللعبة: {game_name}",
                    "size": "md",
                    "color": colors["text2"],
                    "align": "center",
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
        FlexMessage(alt_text="إيقاف", contents=FlexContainer.from_dict(bubble))
    )

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
                    "color": colors["success"],
                    "align": "center",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": username,
                    "size": "lg",
                    "weight": "bold",
                    "color": colors["text"],
                    "align": "center",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": f"فاز في لعبة {game_name}",
                    "size": "md",
                    "color": colors["text2"],
                    "align": "center",
                    "wrap": True,
                    "margin": "sm"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"+{points}",
                            "size": "xxl",
                            "weight": "bold",
                            "color": colors["primary"],
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": f"المجموع: {total_points}",
                            "size": "sm",
                            "color": colors["text2"],
                            "align": "center",
                            "margin": "xs"
                        }
                    ],
                    "cornerRadius": "15px",
                    "paddingAll": "15px",
                    "margin": "lg",
                    "borderWidth": "2px",
                    "borderColor": colors.get("primary", "#3B82F6")
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                create_glass_button("🎮 العب مرة أخرى", "ألعاب", "primary"),
                create_glass_button("📊 نقاطي", "نقاطي", "link"),
                create_glass_button("🏆 الصدارة", "صدارة", "link")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="فوز", contents=FlexContainer.from_dict(bubble))
    )


def build_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة المساعدة"""
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
                    "text": "❓",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "المساعدة",
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
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 الأوامر الأساسية:",
                            "size": "md",
                            "weight": "bold",
                            "color": colors["text"],
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "• بداية - الصفحة الرئيسية\n• ألعاب - قائمة الألعاب\n• نقاطي - نقاطك وإحصائياتك\n• صدارة - لوحة الصدارة\n• ثيمات - تغيير المظهر\n• انضم - التسجيل في البوت",
                            "size": "sm",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "md"
                        }
                    ],
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "margin": "md",
                    "borderWidth": "1px",
                    "borderColor": colors.get("border", "#E2E8F0")
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎮 أوامر اللعب:",
                            "size": "md",
                            "weight": "bold",
                            "color": colors["text"],
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "• لمح - تلميح للإجابة\n• جاوب - كشف الإجابة\n• إيقاف - إيقاف اللعبة\n• فريقين - لعبة جماعية",
                            "size": "sm",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "md"
                        }
                    ],
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "margin": "md",
                    "borderWidth": "1px",
                    "borderColor": colors.get("border", "#E2E8F0")
                },
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
        FlexMessage(alt_text="مساعدة", contents=FlexContainer.from_dict(bubble))
    )


def build_multiplayer_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة مساعدة المجموعة"""
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
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "تم بدء وضع المجموعة !",
                    "size": "md",
                    "color": colors["text"],
                    "align": "center",
                    "wrap": True,
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "الخطوات:",
                            "size": "md",
                            "weight": "bold",
                            "color": colors["text"]
                        },
                        {
                            "type": "text",
                            "text": "1️⃣ اكتب 'انضم' للانضمام\n2️⃣ انتظر اللاعبين\n3️⃣ اختر اللعبة لبدء المنافسة\n4️⃣ سيتم تقسيمكم لفريقين",
                            "size": "sm",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "md"
                        }
                    ],
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "margin": "md",
                    "borderWidth": "1px",
                    "borderColor": colors.get("border", "#E2E8F0")
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                create_glass_button("✅ انضم", "انضم", "primary"),
                create_glass_button("🎮 اختر لعبة", "ألعاب", "link")
            ],
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="فريقين", contents=FlexContainer.from_dict(bubble))
    )


def build_team_game_end(team_points: Dict[str, int], theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة نهاية لعبة الفرق"""
    colors = _safe_get_colors(theme)

    team1_pts = team_points.get("team1", 0)
    team2_pts = team_points.get("team2", 0)

    if team1_pts > team2_pts:
        winner = "🥇 الفريق الأول"
        winner_color = colors["success"]
    elif team2_pts > team1_pts:
        winner = "🥈 الفريق الثاني"
        winner_color = colors["success"]
    else:
        winner = "⚖️ تعادل"
        winner_color = colors["warning"]

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
                    "text": "انتهت اللعبة",
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
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "النتيجة النهائية",
                            "size": "md",
                            "weight": "bold",
                            "color": colors["text"],
                            "align": "center"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "الفريق الأول",
                                    "size": "sm",
                                    "color": colors["text2"],
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": str(team1_pts),
                                    "size": "md",
                                    "weight": "bold",
                                    "color": colors["primary"],
                                    "align": "end",
                                    "flex": 0
                                }
                            ],
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "الفريق الثاني",
                                    "size": "sm",
                                    "color": colors["text2"],
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": str(team2_pts),
                                    "size": "md",
                                    "weight": "bold",
                                    "color": colors["primary"],
                                    "align": "end",
                                    "flex": 0
                                }
                            ],
                            "margin": "sm"
                        }
                    ],
                    "cornerRadius": "10px",
                    "paddingAll": "10px",
                    "margin": "md",
                    "borderWidth": "1px",
                    "borderColor": colors.get("border", "#E2E8F0")
                },
                {
                    "type": "text",
                    "text": winner,
                    "size": "lg",
                    "weight": "bold",
                    "color": winner_color,
                    "align": "center",
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
        FlexMessage(alt_text="نهاية اللعبة", contents=FlexContainer.from_dict(bubble))
    )


def build_answer_feedback(message: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """نافذة ردود فعل الإجابات"""
    colors = _safe_get_colors(theme)
    
    is_correct = "✅" in message or "صحيح" in message
    icon = "✅" if is_correct else "❌"
    title_color = colors["success"] if is_correct else colors["error"]

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
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
                    "text": message,
                    "size": "md",
                    "color": title_color,
                    "align": "center",
                    "wrap": True,
                    "margin": "lg"
                }
            ],
            "paddingAll": "15px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="نتيجة", contents=FlexContainer.from_dict(bubble))
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
    "build_registration_success",
    "build_join_confirmation",
    "build_error_message",
    "build_theme_change_success",
    "build_game_stopped",
    "build_winner_announcement",
    "build_help_window",
    "build_multiplayer_help_window",
    "build_team_game_end",
    "build_answer_feedback",
    "attach_quick_reply_to_message",
    "attach_quick_reply",
    "create_games_quick_reply"
]
