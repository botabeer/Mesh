"""
Bot Mesh - Glass UI Builder v13.0 FINAL
Created by: Abeer Aldosari © 2025
✅ واجهات نظيفة احترافية
✅ ترتيب رسمي للألعاب
✅ Quick Reply للألعاب فقط
✅ تصميم موحد Header/Body/Footer
"""

from typing import List, Dict
from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction
)

from constants import DEFAULT_THEME, get_theme_colors

# معلومات البوت الرسمية
BOT_NAME = "Bot Mesh"
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

# الترتيب الرسمي النهائي للألعاب
OFFICIAL_GAMES = [
    "ذكاء", "سرعة", "رياضيات", "تحدي",
    "ألوان", "تكوين", "سلسلة", "خمن",
    "أغنية", "حروف", "لعبة", "توافق"
]


# =========================================================
# SAFE COLORS
# =========================================================

def _safe_get_colors(theme: str) -> Dict[str, str]:
    try:
        return get_theme_colors(theme)
    except:
        return get_theme_colors(DEFAULT_THEME)


# =========================================================
# QUICK REPLY FOR GAMES (ثابت للألعاب فقط)
# =========================================================

def build_games_quick_reply():
    """Quick Reply ثابت يظهر مع نافذة الألعاب المتاحة فقط"""
    return QuickReply(
        items=[
            QuickReplyItem(
                action=MessageAction(label=game, text=game)
            )
            for game in OFFICIAL_GAMES
        ]
    )


def attach_quick_reply(message):
    """إضافة Quick Reply للألعاب إلى أي رسالة"""
    if hasattr(message, 'quick_reply'):
        message.quick_reply = build_games_quick_reply()
    return message


# =========================================================
# HOME SCREEN (نافذة البداية)
# =========================================================

def build_enhanced_home(username, points, is_registered=True, theme=DEFAULT_THEME):
    """نافذة البداية الرئيسية"""
    
    status_indicator = "✅" if is_registered else "⭕"
    status_text = f"نقطة | {status_indicator} مسجل {points}"
    
    theme_buttons = [
        {"name": "رمادي", "style": "primary"},
        {"name": "أسود", "style": "secondary"},
        {"name": "أبيض", "style": "secondary"},
        {"name": "وردي", "style": "secondary"},
        {"name": "بنفسجي", "style": "secondary"},
        {"name": "أزرق", "style": "secondary"},
        {"name": "بني", "style": "secondary"},
        {"name": "برتقالي", "style": "secondary"},
        {"name": "أخضر", "style": "secondary"}
    ]
    
    theme_rows = []
    for i in range(0, len(theme_buttons), 3):
        row_buttons = theme_buttons[i:i+3]
        theme_rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": btn["name"], "text": btn["name"]},
                    "style": btn["style"],
                    "height": "sm"
                }
                for btn in row_buttons
            ]
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"🎮 {BOT_NAME}",
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#4A5568"
                }
            ],
            "backgroundColor": "#F7FAFC",
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": status_text,
                            "align": "center",
                            "size": "md",
                            "color": "#2D3748"
                        }
                    ],
                    "backgroundColor": "#EDF2F7",
                    "cornerRadius": "10px",
                    "paddingAll": "12px",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": "🎨 :اختر الثيم",
                    "size": "lg",
                    "weight": "bold",
                    "margin": "xl",
                    "color": "#2D3748"
                },
                *theme_rows,
                {"type": "separator", "margin": "xl"},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "lg",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "✅ انضم", "text": "انضم"},
                            "style": "primary",
                            "height": "sm",
                            "color": "#48BB78"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🎮 الألعاب", "text": "الألعاب"},
                            "style": "primary",
                            "height": "sm"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"},
                            "style": "secondary",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🏆 الصدارة", "text": "الصدارة"},
                            "style": "secondary",
                            "height": "sm"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "فريقين", "text": "فريقين"},
                            "style": "secondary",
                            "height": "sm",
                            "color": "#A0AEC0"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "❓ مساعدة", "text": "مساعدة"},
                            "style": "secondary",
                            "height": "sm"
                        }
                    ]
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#FFFFFF"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "align": "center",
                    "color": "#A0AEC0"
                }
            ],
            "backgroundColor": "#F7FAFC",
            "paddingAll": "10px"
        }
    }

    return FlexMessage("البداية", FlexContainer.from_dict(bubble))


# =========================================================
# GAMES MENU (نافذة الألعاب المتاحة)
# =========================================================

def build_games_menu(theme=DEFAULT_THEME):
    """نافذة الألعاب المتاحة - مع Quick Reply للألعاب"""
    
    game_count = len(OFFICIAL_GAMES)
    
    # بناء صفوف الألعاب (3 ألعاب في كل صف)
    game_rows = []
    for i in range(0, len(OFFICIAL_GAMES), 3):
        row_games = OFFICIAL_GAMES[i:i+3]
        game_rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": game, "text": game},
                    "style": "primary",
                    "height": "sm",
                    "color": "#4299E1"
                }
                for game in row_games
            ]
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"🎮 {BOT_NAME}",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#2B6CB0"
                },
                {
                    "type": "text",
                    "text": "الألعاب المتاحة",
                    "size": "sm",
                    "align": "center",
                    "color": "#4A5568",
                    "margin": "sm"
                }
            ],
            "backgroundColor": "#EBF8FF",
            "paddingAll": "18px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"عدد الألعاب: {game_count}",
                    "align": "center",
                    "size": "md",
                    "color": "#4A5568",
                    "margin": "md"
                },
                
                {"type": "separator", "margin": "lg"},
                
                # صفوف الألعاب
                *game_rows,
                
                {"type": "separator", "margin": "xl"},
                
                # أمر المساعدة
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "اضغط على اسم اللعبة للبدء",
                            "size": "sm",
                            "color": "#718096",
                            "align": "center",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "أو اختر من القائمة السريعة أسفل الشاشة",
                            "size": "xs",
                            "color": "#A0AEC0",
                            "align": "center",
                            "margin": "xs",
                            "wrap": True
                        }
                    ],
                    "backgroundColor": "#F7FAFC",
                    "cornerRadius": "8px",
                    "paddingAll": "12px",
                    "margin": "lg"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#FFFFFF"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🏠 البداية", "text": "بداية"},
                            "style": "secondary",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "❓ مساعدة", "text": "مساعدة"},
                            "style": "secondary",
                            "height": "sm"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "align": "center",
                    "color": "#A0AEC0",
                    "margin": "md"
                }
            ],
            "paddingAll": "15px",
            "backgroundColor": "#F7FAFC"
        }
    }

    return FlexMessage(
        alt_text="الألعاب المتاحة",
        contents=FlexContainer.from_dict(bubble),
        quick_reply=build_games_quick_reply()
    )


# =========================================================
# MY POINTS SCREEN (نقاطي)
# =========================================================

def build_my_points(username, total_points, stats, theme=DEFAULT_THEME):
    """نافذة نقاطي"""
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "⭐ نقاطي",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#2B6CB0"
                }
            ],
            "backgroundColor": "#FFF5F7",
            "paddingAll": "18px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # أيقونة المستخدم
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "80px",
                    "height": "80px",
                    "cornerRadius": "100px",
                    "backgroundColor": "#E2E8F0",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "margin": "lg"
                },
                
                {"type": "separator", "margin": "xl"},
                
                # النقاط الكلية
                {
                    "type": "text",
                    "text": "النقاط الكلية",
                    "size": "md",
                    "align": "center",
                    "color": "#718096",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": str(total_points),
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#2D3748",
                    "margin": "sm"
                },
                
                {"type": "separator", "margin": "xl"},
                
                # المستوى الحالي
                {
                    "type": "text",
                    "text": "المستوى الحالي",
                    "size": "md",
                    "align": "center",
                    "color": "#718096",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "🔥 متقدم",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#F56565",
                    "margin": "sm"
                },
                
                {"type": "separator", "margin": "xl"},
                
                # تحذير حذف البيانات
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "⚠️ سيتم حذف بياناتك بعد 7 أيام من عدم النشاط",
                            "size": "xs",
                            "color": "#E53E3E",
                            "wrap": True,
                            "align": "center"
                        }
                    ],
                    "backgroundColor": "#FFF5F5",
                    "cornerRadius": "8px",
                    "paddingAll": "12px",
                    "margin": "lg"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#FFFFFF",
            "alignItems": "center"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🏠 البداية", "text": "بداية"},
                            "style": "secondary",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🎮 الألعاب", "text": "الألعاب"},
                            "style": "primary",
                            "height": "sm",
                            "color": "#4299E1"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "align": "center",
                    "color": "#A0AEC0",
                    "margin": "md"
                }
            ],
            "paddingAll": "15px",
            "backgroundColor": "#F7FAFC"
        }
    }

    return FlexMessage("نقاطي", FlexContainer.from_dict(bubble))


# =========================================================
# LEADERBOARD SCREEN (لوحة الصدارة)
# =========================================================

def build_leaderboard(top_users, theme=DEFAULT_THEME):
    """نافذة لوحة الصدارة"""
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🏆 لوحة الصدارة",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#2B6CB0"
                }
            ],
            "backgroundColor": "#FFF9E6",
            "paddingAll": "18px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # موقعك الحالي
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
                                    "text": "🥇",
                                    "size": "xl",
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": "7",
                                    "size": "sm",
                                    "align": "center",
                                    "color": "#718096"
                                }
                            ],
                            "width": "50px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "215",
                                    "size": "xxl",
                                    "weight": "bold",
                                    "align": "end",
                                    "color": "#2D3748"
                                }
                            ],
                            "flex": 1,
                            "justifyContent": "center"
                        }
                    ],
                    "backgroundColor": "#E6FFFA",
                    "cornerRadius": "12px",
                    "paddingAll": "15px",
                    "margin": "md"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#FFFFFF"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🏠 البداية", "text": "بداية"},
                            "style": "secondary",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"},
                            "style": "primary",
                            "height": "sm",
                            "color": "#F6AD55"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "align": "center",
                    "color": "#A0AEC0",
                    "margin": "md"
                }
            ],
            "paddingAll": "15px",
            "backgroundColor": "#F7FAFC"
        }
    }

    return FlexMessage("لوحة الصدارة", FlexContainer.from_dict(bubble))


# =========================================================
# WINNER ANNOUNCEMENT (إعلان الفائز)
# =========================================================

def build_winner_announcement(username, game_name, points, total_points, theme=DEFAULT_THEME):
    """نافذة الفوز"""
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
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
                    "text": "!إتهانينا",
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#2B6CB0",
                    "margin": "sm"
                },
                {
                    "type": "text",
                    "text": f"أنهيت {game_name}",
                    "size": "sm",
                    "align": "center",
                    "color": "#4A5568",
                    "margin": "sm",
                    "wrap": True
                }
            ],
            "backgroundColor": "#FFF5F7",
            "paddingAll": "25px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "النقاط المكتسبة",
                    "size": "sm",
                    "align": "center",
                    "color": "#718096",
                    "margin": "xl"
                },
                {
                    "type": "text",
                    "text": f"+{points}",
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#48BB78",
                    "margin": "sm"
                },
                
                {"type": "separator", "margin": "xl"},
                
                {
                    "type": "text",
                    "text": f"⭐ إجمالي النقاط                {total_points}",
                    "size": "md",
                    "color": "#2D3748",
                    "margin": "lg"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#FFFFFF",
            "alignItems": "center"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": "🔄 إعادة نفس اللعبة", "text": game_name},
                    "style": "primary",
                    "height": "sm",
                    "color": "#4299E1"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🎮 الألعاب", "text": "الألعاب"},
                            "style": "secondary",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🏠 البداية", "text": "بداية"},
                            "style": "secondary",
                            "height": "sm"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "align": "center",
                    "color": "#A0AEC0",
                    "margin": "md"
                }
            ],
            "paddingAll": "15px",
            "backgroundColor": "#F7FAFC"
        }
    }

    return FlexMessage("فوز", FlexContainer.from_dict(bubble))


# =========================================================
# HELP WINDOW (المساعدة)
# =========================================================

def build_help_window(theme=DEFAULT_THEME):
    """نافذة المساعدة"""
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "❓ المساعدة",
                    "size": "xl",
                    "weight": "bold",
                    "align": "center",
                    "color": "#2B6CB0"
                }
            ],
            "backgroundColor": "#EBF8FF",
            "paddingAll": "18px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "كيفية اللعب:",
                    "weight": "bold",
                    "margin": "md",
                    "color": "#2D3748"
                },
                {
                    "type": "text",
                    "text": "• اختر لعبة من قائمة الألعاب",
                    "size": "sm",
                    "color": "#718096",
                    "margin": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "• اكتب إجابتك مباشرة",
                    "size": "sm",
                    "color": "#718096",
                    "margin": "xs",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "• استخدم 'لمح' للحصول على تلميح",
                    "size": "sm",
                    "color": "#718096",
                    "margin": "xs",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "• استخدم 'جاوب' لمعرفة الحل",
                    "size": "sm",
                    "color": "#718096",
                    "margin": "xs",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "• استخدم 'إيقاف' لإنهاء اللعبة",
                    "size": "sm",
                    "color": "#718096",
                    "margin": "xs",
                    "wrap": True
                },
                
                {"type": "separator", "margin": "lg"},
                
                {
                    "type": "text",
                    "text": "نظام النقاط:",
                    "weight": "bold",
                    "margin": "lg",
                    "color": "#2D3748"
                },
                {
                    "type": "text",
                    "text": "• +10 نقاط للإجابة الصحيحة",
                    "size": "sm",
                    "color": "#718096",
                    "margin": "sm",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "• +5 نقاط بعد استخدام لمحة",
                    "size": "sm",
                    "color": "#718096",
                    "margin": "xs",
                    "wrap": True
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#FFFFFF"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": "🏠 البداية", "text": "بداية"},
                    "style": "primary",
                    "height": "sm"
                }
            ],
            "paddingAll": "15px",
            "backgroundColor": "#F7FAFC"
        }
    }

    return FlexMessage("المساعدة", FlexContainer.from_dict(bubble))


# =========================================================
# ADDITIONAL HELPERS
# =========================================================

def build_registration_required(theme=DEFAULT_THEME):
    """نافذة تطلب التسجيل"""
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "⚠️", "size": "xxl
