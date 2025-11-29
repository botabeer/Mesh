"""
Bot Mesh - UI Builder v10.0 COMPLETE FIXED
Created by: Abeer Aldosari © 2025
✅ إصلاح جميع الأخطاء
✅ Quick Reply للألعاب فقط
✅ نوافذ Flex كاملة
"""

from linebot.v3.messaging import (
    FlexMessage, FlexContainer, TextMessage,
    QuickReply, QuickReplyItem, MessageAction
)
from constants import GAME_LIST, DEFAULT_THEME, THEMES, BOT_NAME, BOT_RIGHTS

# ============================================================================
# Quick Reply - للألعاب فقط
# ============================================================================

def build_games_quick_reply():
    """بناء Quick Reply للألعاب فقط"""
    items = []
    for internal, display, icon in GAME_LIST:
        items.append(
            QuickReplyItem(
                action=MessageAction(
                    label=f"{icon} {display}",
                    text=display
                )
            )
        )
    return QuickReply(items=items)


def attach_quick_reply(message):
    """إضافة Quick Reply لأي رسالة"""
    if message and hasattr(message, 'quick_reply'):
        message.quick_reply = build_games_quick_reply()
    return message


# ============================================================================
# Helper Functions
# ============================================================================

def get_theme_colors(theme_name=None):
    """الحصول على ألوان الثيم"""
    if theme_name is None:
        theme_name = DEFAULT_THEME
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])


def _btn(label, text, style="primary", color=None):
    """زر سريع"""
    btn = {
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
        btn["color"] = color
    return btn


# ============================================================================
# Main Windows
# ============================================================================

def build_enhanced_home(username, points, is_registered=True, theme=DEFAULT_THEME):
    """نافذة البداية المحسّنة"""
    colors = get_theme_colors(theme)
    
    # أزرار الثيمات
    theme_names = list(THEMES.keys())
    theme_rows = []
    for i in range(0, len(theme_names), 3):
        row_themes = theme_names[i:i+3]
        theme_rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [
                _btn(t, f"ثيم {t}", "primary" if t == theme else "secondary")
                for t in row_themes
            ]
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["primary"],
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": f"🎮 {BOT_NAME}",
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#FFFFFF"
                },
                {
                    "type": "text",
                    "text": f"مرحباً {username}",
                    "size": "md",
                    "align": "center",
                    "color": "#FFFFFF",
                    "margin": "md"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": colors["glass"],
                    "cornerRadius": "10px",
                    "paddingAll": "15px",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"⭐ {points} نقطة",
                            "size": "xl",
                            "weight": "bold",
                            "align": "center",
                            "color": colors["text"]
                        },
                        {
                            "type": "text",
                            "text": "✅ مسجل" if is_registered else "⭕ غير مسجل",
                            "size": "sm",
                            "align": "center",
                            "color": colors["success"] if is_registered else colors["error"],
                            "margin": "sm"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": "🎨 اختر الثيم:",
                    "size": "lg",
                    "weight": "bold",
                    "margin": "xl",
                    "color": colors["text"]
                },
                *theme_rows,
                {
                    "type": "separator",
                    "margin": "xl"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "lg",
                    "contents": [
                        _btn("🎮 الألعاب", "ألعاب", "primary"),
                        _btn("⭐ نقاطي", "نقاطي", "secondary")
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "sm",
                    "contents": [
                        _btn("🏆 الصدارة", "صدارة", "secondary"),
                        _btn("❓ مساعدة", "مساعدة", "secondary")
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "15px",
            "contents": [
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "align": "center",
                    "color": colors["text2"]
                }
            ]
        }
    }
    
    msg = FlexMessage(alt_text="البداية", contents=FlexContainer.from_dict(bubble))
    return attach_quick_reply(msg)


def build_games_menu(theme=DEFAULT_THEME):
    """قائمة الألعاب"""
    colors = get_theme_colors(theme)
    
    # تقسيم الألعاب إلى صفوف
    game_rows = []
    for i in range(0, len(GAME_LIST), 3):
        row_games = GAME_LIST[i:i+3]
        game_rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [
                _btn(f"{icon} {display}", display, "primary")
                for internal, display, icon in row_games
            ]
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["primary"],
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "🎮 الألعاب المتاحة",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#FFFFFF"
                },
                {
                    "type": "text",
                    "text": f"عدد الألعاب: {len(GAME_LIST)}",
                    "size": "sm",
                    "align": "center",
                    "color": "#FFFFFF",
                    "margin": "sm"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                *game_rows,
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": colors["glass"],
                    "cornerRadius": "8px",
                    "paddingAll": "12px",
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "text",
                            "text": "💡 اضغط على اسم اللعبة للبدء",
                            "size": "sm",
                            "color": colors["text"],
                            "align": "center",
                            "wrap": True
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "15px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        _btn("🏠 البداية", "بداية", "secondary"),
                        _btn("❓ مساعدة", "مساعدة", "secondary")
                    ]
                }
            ]
        }
    }
    
    msg = FlexMessage(alt_text="الألعاب", contents=FlexContainer.from_dict(bubble))
    return attach_quick_reply(msg)


def build_my_points(username, points, stats=None, theme=DEFAULT_THEME):
    """نافذة نقاطي"""
    colors = get_theme_colors(theme)
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["primary"],
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "⭐ نقاطي",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#FFFFFF"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "النقاط الكلية",
                    "size": "md",
                    "align": "center",
                    "color": colors["text2"],
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": str(points),
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": colors["text"],
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": colors["glass"],
                    "cornerRadius": "8px",
                    "paddingAll": "15px",
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "text",
                            "text": "استمر باللعب لكسب المزيد!",
                            "size": "sm",
                            "color": colors["text"],
                            "align": "center",
                            "wrap": True
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "15px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        _btn("🎮 الألعاب", "ألعاب", "primary"),
                        _btn("🏠 البداية", "بداية", "secondary")
                    ]
                }
            ]
        }
    }
    
    msg = FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(bubble))
    return attach_quick_reply(msg)


def build_leaderboard(top_users, theme=DEFAULT_THEME):
    """لوحة الصدارة"""
    colors = get_theme_colors(theme)
    
    leaderboard_items = []
    for idx, (name, pts) in enumerate(top_users[:10], 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
        leaderboard_items.append({
            "type": "box",
            "layout": "horizontal",
            "margin": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": medal,
                    "size": "md",
                    "flex": 0,
                    "margin": "none"
                },
                {
                    "type": "text",
                    "text": name,
                    "size": "sm",
                    "color": colors["text"],
                    "flex": 2,
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": str(pts),
                    "size": "sm",
                    "color": colors["primary"],
                    "align": "end",
                    "flex": 1
                }
            ]
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["primary"],
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "🏆 لوحة الصدارة",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#FFFFFF"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": leaderboard_items if leaderboard_items else [
                {
                    "type": "text",
                    "text": "لا توجد بيانات بعد",
                    "align": "center",
                    "color": colors["text2"]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "15px",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        _btn("⭐ نقاطي", "نقاطي", "primary"),
                        _btn("🏠 البداية", "بداية", "secondary")
                    ]
                }
            ]
        }
    }
    
    msg = FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble))
    return attach_quick_reply(msg)


def build_help_window(theme=DEFAULT_THEME):
    """نافذة المساعدة"""
    colors = get_theme_colors(theme)
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["primary"],
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "❓ المساعدة",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#FFFFFF"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "🎮 الأوامر الأساسية:",
                    "weight": "bold",
                    "color": colors["text"],
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "• بداية - العودة للصفحة الرئيسية\n• ألعاب - عرض جميع الألعاب\n• نقاطي - عرض نقاطك\n• صدارة - لوحة المتصدرين\n• انضم - التسجيل في البوت",
                    "size": "sm",
                    "color": colors["text2"],
                    "margin": "sm",
                    "wrap": True
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "🎯 أثناء اللعب:",
                    "weight": "bold",
                    "color": colors["text"],
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "• لمح - الحصول على تلميح\n• جاوب - كشف الإجابة\n• إيقاف - إنهاء اللعبة",
                    "size": "sm",
                    "color": colors["text2"],
                    "margin": "sm",
                    "wrap": True
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "👥 وضع الفريقين:",
                    "weight": "bold",
                    "color": colors["text"],
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "• فريقين - بدء وضع الفرق (للمجموعات)\n• انضم - الانضمام للفريق",
                    "size": "sm",
                    "color": colors["text2"],
                    "margin": "sm",
                    "wrap": True
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "15px",
            "contents": [
                _btn("🏠 البداية", "بداية", "primary")
            ]
        }
    }
    
    msg = FlexMessage(alt_text="المساعدة", contents=FlexContainer.from_dict(bubble))
    return attach_quick_reply(msg)


# ============================================================================
# Game-Specific Windows
# ============================================================================

def build_registration_required(theme=DEFAULT_THEME):
    """نافذة طلب التسجيل"""
    colors = get_theme_colors(theme)
    
    bubble = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["warning"],
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "⚠️ تسجيل مطلوب",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#FFFFFF"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "يجب التسجيل أولاً للعب",
                    "align": "center",
                    "color": colors["text"],
                    "wrap": True
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "15px",
            "contents": [
                _btn("✅ انضم الآن", "انضم", "primary")
            ]
        }
    }
    
    msg = FlexMessage(alt_text="تسجيل مطلوب", contents=FlexContainer.from_dict(bubble))
    return attach_quick_reply(msg)


def build_winner_announcement(username, game_name, round_points, total_points, theme=DEFAULT_THEME):
    """إعلان الفائز"""
    colors = get_theme_colors(theme)
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["success"],
            "paddingAll": "25px",
            "contents": [
                {
                    "type": "text",
                    "text": "🎉",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "مبروك!",
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#FFFFFF",
                    "margin": "sm"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": f"أنهيت لعبة {game_name}",
                    "size": "md",
                    "align": "center",
                    "color": colors["text"],
                    "wrap": True
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "النقاط المكتسبة",
                    "size": "sm",
                    "align": "center",
                    "color": colors["text2"],
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": f"+{round_points}",
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": colors["success"],
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": f"⭐ إجمالي النقاط: {total_points}",
                    "size": "md",
                    "align": "center",
                    "color": colors["text"],
                    "margin": "lg"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "paddingAll": "15px",
            "contents": [
                _btn(f"🔄 {game_name}", game_name, "primary"),
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        _btn("🎮 الألعاب", "ألعاب", "secondary"),
                        _btn("🏠 البداية", "بداية", "secondary")
                    ]
                }
            ]
        }
    }
    
    msg = FlexMessage(alt_text="فوز", contents=FlexContainer.from_dict(bubble))
    return attach_quick_reply(msg)


def build_theme_selector(theme=DEFAULT_THEME):
    """محدد الثيمات"""
    colors = get_theme_colors(theme)
    theme_names = list(THEMES.keys())
    
    theme_buttons = []
    for i in range(0, len(theme_names), 3):
        row = theme_names[i:i+3]
        theme_buttons.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [_btn(t, f"ثيم {t}") for t in row]
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["primary"],
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "🎨 اختر الثيم",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#FFFFFF"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": theme_buttons
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "15px",
            "contents": [_btn("🏠 البداية", "بداية", "secondary")]
        }
    }
    
    msg = FlexMessage(alt_text="الثيمات", contents=FlexContainer.from_dict(bubble))
    return attach_quick_reply(msg)


def build_multiplayer_help_window(theme=DEFAULT_THEME):
    """نافذة مساعدة الفريقين"""
    colors = get_theme_colors(theme)
    
    bubble = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": colors["primary"],
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "👥 وضع الفريقين",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#FFFFFF"
                }
            ]
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "تم بدء مرحلة الانضمام!",
                    "size": "md",
                    "color": colors["text"],
                    "wrap": True
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "الخطوات:",
                    "weight": "bold",
                    "color": colors["text"],
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "1. اكتب 'انضم' للانضمام\n2. اختر اللعبة من القائمة\n3. سيتم تقسيم الفرق تلقائياً",
                    "size": "sm",
                    "color": colors["text2"],
                    "margin": "sm",
                    "wrap": True
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "15px",
            "contents": [_btn("✅ انضم", "انضم", "primary")]
        }
    }
    
    msg = FlexMessage(alt_text="وضع الفريقين", contents=FlexContainer.from_dict(bubble))
    return attach_quick_reply(msg)


# ============================================================================
# Export
# ============================================================================

__all__ = [
    'build_enhanced_home',
    'build_games_menu',
    'build_my_points',
    'build_leaderboard',
    'build_help_window',
    'build_registration_required',
    'build_winner_announcement',
    'build_theme_selector',
    'build_multiplayer_help_window',
    'attach_quick_reply',
    'build_games_quick_reply'
]
