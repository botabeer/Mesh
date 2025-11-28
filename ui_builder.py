"""
Bot Mesh - UI Builder v10.0 FULL FLEX
Created by: Abeer Aldosari © 2025
✅ كل شيء نوافذ فلكس وأزرار
✅ Quick Reply دائم للألعاب فقط
"""

import traceback
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
# Quick Reply System - الألعاب فقط
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
    """إضافة Quick Reply للرسالة"""
    try:
        qr = create_games_quick_reply()
        message.quick_reply = qr
    except Exception:
        pass
    return message


# ============================================================================
# Glass Components
# ============================================================================

def create_glass_header(colors: Dict, title: str, subtitle: str = None, icon: str = None) -> List[Dict]:
    """إنشاء Header زجاجي"""
    header_content = []

    if icon:
        header_content.append({
            "type": "text",
            "text": icon,
            "size": "xxl",
            "align": "center",
            "color": colors["primary"]
        })

    header_content.append({
        "type": "text",
        "text": title,
        "size": "xxl",
        "weight": "bold",
        "color": colors["primary"],
        "align": "center",
        "margin": "sm" if icon else "none"
    })

    if subtitle:
        header_content.append({
            "type": "text",
            "text": subtitle,
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "margin": "xs"
        })

    header_content.append({
        "type": "separator",
        "margin": "lg"
    })

    return header_content


# ============================================================================
# Main UI Screens
# ============================================================================

def build_enhanced_home(username: str, points: int, is_registered: bool, theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏠 نافذة البداية الرئيسية"""
    colors = _safe_get_colors(theme)

    header = create_glass_header(
        colors, 
        f"مرحباً {username}", 
        f"النقاط: {points}", 
        "🎮"
    )

    buttons = [
        {
            "type": "button",
            "action": {"type": "message", "label": "🎮 الألعاب", "text": "ألعاب"},
            "style": "primary",
            "height": "sm",
            "margin": "md"
        },
        {
            "type": "button",
            "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"},
            "style": "link",
            "height": "sm",
            "margin": "sm"
        },
        {
            "type": "button",
            "action": {"type": "message", "label": "🏆 الصدارة", "text": "صدارة"},
            "style": "link",
            "height": "sm",
            "margin": "sm"
        },
        {
            "type": "button",
            "action": {"type": "message", "label": "🎨 الثيمات", "text": "ثيمات"},
            "style": "link",
            "height": "sm",
            "margin": "sm"
        },
        {
            "type": "button",
            "action": {"type": "message", "label": "❓ مساعدة", "text": "مساعدة"},
            "style": "link",
            "height": "sm",
            "margin": "sm"
        }
    ]

    if not is_registered:
        buttons.insert(1, {
            "type": "button",
            "action": {"type": "message", "label": "✅ انضم الآن", "text": "انضم"},
            "style": "primary",
            "color": colors["success"],
            "height": "sm",
            "margin": "md"
        })

    # إضافة حقوق
    footer = [
        {
            "type": "separator",
            "margin": "lg"
        },
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center",
            "margin": "md",
            "wrap": True
        }
    ]

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + buttons + footer,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🏠 البداية", contents=FlexContainer.from_dict(bubble))


def build_games_menu(theme: str = DEFAULT_THEME) -> FlexMessage:
    """🎮 نافذة قائمة الألعاب"""
    colors = _safe_get_colors(theme)

    header = create_glass_header(colors, "قائمة الألعاب", icon="🎮")

    buttons = []

    for _, display_name, icon in GAME_LIST:
        buttons.append({
            "type": "button",
            "action": {
                "type": "message",
                "label": f"{icon} {display_name}",
                "text": display_name
            },
            "style": "link",
            "height": "sm",
            "margin": "sm"
        })

    # زر العودة
    buttons.append({
        "type": "separator",
        "margin": "lg"
    })
    buttons.append({
        "type": "button",
        "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"},
        "style": "link",
        "height": "sm",
        "margin": "md"
    })

    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + buttons,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🎮 الألعاب", contents=FlexContainer.from_dict(bubble))


def build_my_points(username: str, total_points: int, stats: Dict, theme: str = DEFAULT_THEME) -> FlexMessage:
    """⭐ نافذة النقاط"""
    colors = _safe_get_colors(theme)

    contents = [
        {"type": "text", "text": "⭐", "size": "xxl", "align": "center", "color": colors["primary"]},
        {"type": "text", "text": "نقاطي", "weight": "bold", "size": "xl", "align": "center", "color": colors["primary"], "margin": "sm"},
        {"type": "separator", "margin": "md"},
        {"type": "text", "text": f"اللاعب: {username}", "size": "md", "margin": "md", "color": colors["text"]},
        {"type": "text", "text": f"النقاط الإجمالية: {total_points}", "size": "lg", "weight": "bold", "margin": "sm", "color": colors["success"]}
    ]

    if stats:
        contents.append({"type": "separator", "margin": "lg"})
        contents.append({"type": "text", "text": "📊 إحصائيات الألعاب:", "weight": "bold", "margin": "md", "color": colors["text"]})
        
        for game_name, data in list(stats.items())[:5]:
            contents.append({
                "type": "text",
                "text": f"• {game_name}: {data.get('plays', 0)} لعبة - {data.get('total_score', 0)} نقطة",
                "size": "sm",
                "margin": "xs",
                "color": colors["text2"],
                "wrap": True
            })

    # زر العودة
    contents.append({"type": "separator", "margin": "lg"})
    contents.append({
        "type": "button",
        "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"},
        "style": "link",
        "height": "sm",
        "margin": "md"
    })

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="⭐ نقاطي", contents=FlexContainer.from_dict(bubble))


def build_leaderboard(top_users: List[Tuple[str, int]], theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏆 نافذة الصدارة"""
    colors = _safe_get_colors(theme)

    contents = [
        {"type": "text", "text": "🏆", "size": "xxl", "align": "center", "color": colors["primary"]},
        {"type": "text", "text": "الصدارة", "weight": "bold", "size": "xl", "align": "center", "color": colors["primary"], "margin": "sm"},
        {"type": "separator", "margin": "md"}
    ]

    medals = ["🥇", "🥈", "🥉"]
    
    for i, (name, pts) in enumerate(top_users[:10]):
        medal = medals[i] if i < 3 else f"{i+1}."
        contents.append({
            "type": "text",
            "text": f"{medal} {name} - {pts} نقطة",
            "size": "md" if i < 3 else "sm",
            "margin": "sm",
            "weight": "bold" if i < 3 else "regular",
            "color": colors["primary"] if i < 3 else colors["text"]
        })

    # زر العودة
    contents.append({"type": "separator", "margin": "lg"})
    contents.append({
        "type": "button",
        "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"},
        "style": "link",
        "height": "sm",
        "margin": "md"
    })

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🏆 الصدارة", contents=FlexContainer.from_dict(bubble))


def build_theme_selector(current_theme: str = DEFAULT_THEME) -> FlexMessage:
    """🎨 نافذة اختيار الثيم"""
    colors = _safe_get_colors(current_theme)

    header = [
        {"type": "text", "text": "🎨", "size": "xxl", "align": "center", "color": colors["primary"]},
        {"type": "text", "text": "اختر الثيم", "weight": "bold", "size": "xl", "align": "center", "color": colors["primary"], "margin": "sm"},
        {"type": "separator", "margin": "md"}
    ]

    buttons = []
    for name in THEMES.keys():
        marker = "✓ " if name == current_theme else ""
        buttons.append({
            "type": "button",
            "action": {"type": "message", "label": f"{marker}{name}", "text": f"ثيم {name}"},
            "style": "primary" if name == current_theme else "link",
            "height": "sm",
            "margin": "sm"
        })

    # زر العودة
    buttons.append({"type": "separator", "margin": "lg"})
    buttons.append({
        "type": "button",
        "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"},
        "style": "link",
        "height": "sm",
        "margin": "md"
    })

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + buttons,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🎨 الثيمات", contents=FlexContainer.from_dict(bubble))


def build_registration_required(theme: str = DEFAULT_THEME) -> FlexMessage:
    """⚠️ نافذة التسجيل المطلوب"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"اللعبة: {game_name}", "size": "md", "align": "center", "margin": "md", "color": colors["text2"]},
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "🎮 ألعاب أخرى", "text": "ألعاب"}, "style": "primary", "margin": "md", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "margin": "sm", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="⛔ إيقاف", contents=FlexContainer.from_dict(bubble))


def build_team_game_end(team_points: Dict[str, int], theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏆 نافذة نهاية لعبة الفريقين"""
    colors = _safe_get_colors(theme)

    t1 = team_points.get("team1", 0)
    t2 = team_points.get("team2", 0)
    
    if t1 > t2:
        winner = "الفريق الأول 🥇"
        winner_color = colors["success"]
    elif t2 > t1:
        winner = "الفريق الثاني 🥈"
        winner_color = colors["primary"]
    else:
        winner = "تعادل ⚖️"
        winner_color = colors["warning"]

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🏆", "size": "xxl", "align": "center", "color": colors["primary"]},
                {"type": "text", "text": "انتهت اللعبة", "weight": "bold", "size": "xl", "align": "center", "margin": "sm", "color": colors["primary"]},
                {"type": "separator", "margin": "lg"},
                {"type": "text", "text": "النتيجة النهائية", "weight": "bold", "size": "lg", "align": "center", "margin": "md", "color": colors["text"]},
                {"type": "text", "text": f"▫️ الفريق الأول: {t1}", "size": "md", "align": "center", "margin": "sm", "color": colors["text2"]},
                {"type": "text", "text": f"▫️ الفريق الثاني: {t2}", "size": "md", "align": "center", "margin": "xs", "color": colors["text2"]},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": f"الفائز: {winner}", "size": "lg", "weight": "bold", "align": "center", "margin": "md", "color": winner_color},
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "🎮 لعب مرة أخرى", "text": "ألعاب"}, "style": "primary", "margin": "md", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "margin": "sm", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🏆 نهاية اللعبة", contents=FlexContainer.from_dict(bubble))


def build_answer_feedback(message: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """💬 نافذة ردود الإجابات"""
    colors = _safe_get_colors(theme)
    
    # تحديد الأيقونة واللون حسب الرسالة
    if "✅" in message or "صحيح" in message:
        icon = "✅"
        color = colors["success"]
    elif "❌" in message or "خطأ" in message:
        icon = "❌"
        color = colors["error"]
    else:
        icon = "💬"
        color = colors["primary"]

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": icon, "size": "xxl", "align": "center", "color": color},
                {"type": "text", "text": message, "size": "md", "align": "center", "margin": "md", "color": colors["text"], "wrap": True}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text=message, contents=FlexContainer.from_dict(bubble))


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
    "build_join_confirmation",
    "build_registration_success",
    "build_theme_change_success",
    "build_error_message",
    "build_game_stopped",
    "build_team_game_end",
    "build_answer_feedback",
    "attach_quick_reply_to_message",
    "create_games_quick_reply"
]text", "text": "⚠️", "size": "xxl", "align": "center", "color": colors["warning"]},
                {"type": "text", "text": "يجب التسجيل أولاً", "weight": "bold", "size": "lg", "align": "center", "margin": "md", "color": colors["text"]},
                {"type": "text", "text": "للعب الألعاب وكسب النقاط", "size": "sm", "align": "center", "margin": "sm", "wrap": True, "color": colors["text2"]},
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "✅ انضم الآن", "text": "انضم"}, "style": "primary", "margin": "md", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "margin": "sm", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="⚠️ التسجيل مطلوب", contents=FlexContainer.from_dict(bubble))


def build_winner_announcement(username: str, game_name: str, points: int, total_points: int, theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏆 نافذة إعلان الفائز"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🏆", "size": "xxl", "align": "center", "color": colors["primary"]},
                {"type": "text", "text": "انتهت اللعبة", "weight": "bold", "size": "xl", "align": "center", "margin": "sm", "color": colors["primary"]},
                {"type": "separator", "margin": "lg"},
                {"type": "text", "text": f"الفائز: {username}", "size": "lg", "weight": "bold", "align": "center", "margin": "md", "color": colors["text"]},
                {"type": "text", "text": f"اللعبة: {game_name}", "size": "md", "align": "center", "margin": "sm", "color": colors["text2"]},
                {"type": "text", "text": f"النقاط المكتسبة: +{points}", "size": "lg", "color": colors["success"], "align": "center", "margin": "md", "weight": "bold"},
                {"type": "text", "text": f"الإجمالي: {total_points} نقطة", "size": "sm", "align": "center", "margin": "sm", "color": colors["text2"]},
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "🎮 لعب مرة أخرى", "text": "ألعاب"}, "style": "primary", "margin": "md", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "margin": "sm", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🏆 الفائز", contents=FlexContainer.from_dict(bubble))


def build_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """❓ نافذة المساعدة"""
    colors = _safe_get_colors(theme)

    commands = [
        ("🏠 بداية", "العودة للصفحة الرئيسية"),
        ("🎮 ألعاب", "عرض قائمة الألعاب"),
        ("⭐ نقاطي", "عرض نقاطك وإحصائياتك"),
        ("🏆 صدارة", "عرض أفضل اللاعبين"),
        ("🎨 ثيمات", "تغيير مظهر البوت"),
        ("✅ انضم", "التسجيل في البوت"),
        ("⛔ إيقاف", "إيقاف اللعبة الحالية")
    ]

    contents = [
        {"type": "text", "text": "❓", "size": "xxl", "align": "center", "color": colors["primary"]},
        {"type": "text", "text": "دليل الأوامر", "weight": "bold", "size": "xl", "align": "center", "color": colors["primary"], "margin": "sm"},
        {"type": "separator", "margin": "md"}
    ]

    for cmd, desc in commands:
        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": cmd, "weight": "bold", "size": "md", "color": colors["text"]},
                {"type": "text", "text": desc, "size": "xs", "color": colors["text2"], "wrap": True}
            ],
            "margin": "md"
        })

    # أزرار
    contents.append({"type": "separator", "margin": "lg"})
    contents.append({
        "type": "button",
        "action": {"type": "message", "label": "🎮 ابدأ اللعب", "text": "ألعاب"},
        "style": "primary",
        "margin": "md",
        "height": "sm"
    })
    contents.append({
        "type": "button",
        "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"},
        "style": "link",
        "margin": "sm",
        "height": "sm"
    })

    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="❓ مساعدة", contents=FlexContainer.from_dict(bubble))


def build_multiplayer_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """👥 نافذة شرح وضع الفريقين"""
    colors = _safe_get_colors(theme)

    steps = [
        {"type": "text", "text": "👥", "size": "xxl", "align": "center", "color": colors["primary"]},
        {"type": "text", "text": "وضع الفريقين", "weight": "bold", "size": "xl", "align": "center", "color": colors["primary"], "margin": "sm"},
        {"type": "separator", "margin": "md"},
        {"type": "text", "text": "1️⃣ اكتب: فريقين", "size": "md", "margin": "md", "color": colors["text"], "weight": "bold"},
        {"type": "text", "text": "لبدء مرحلة الانضمام", "size": "xs", "color": colors["text2"], "margin": "xs"},
        {"type": "text", "text": "2️⃣ اكتب: انضم", "size": "md", "margin": "md", "color": colors["text"], "weight": "bold"},
        {"type": "text", "text": "للانضمام للعبة الجماعية", "size": "xs", "color": colors["text2"], "margin": "xs"},
        {"type": "text", "text": "3️⃣ اختر اللعبة", "size": "md", "margin": "md", "color": colors["text"], "weight": "bold"},
        {"type": "text", "text": "سيتم تقسيم الفرق تلقائياً", "size": "xs", "color": colors["text2"], "margin": "xs"},
        {"type": "separator", "margin": "lg"},
        {"type": "button", "action": {"type": "message", "label": "🎮 اختر اللعبة", "text": "ألعاب"}, "style": "primary", "margin": "md", "height": "sm"}
    ]

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": steps,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="👥 فريقين", contents=FlexContainer.from_dict(bubble))


# ============================================================================
# Additional Flex Windows
# ============================================================================

def build_join_confirmation(username: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """✅ نافذة تأكيد الانضمام"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "✅", "size": "xxl", "align": "center", "color": colors["success"]},
                {"type": "text", "text": "تم الانضمام", "weight": "bold", "size": "xl", "align": "center", "margin": "sm", "color": colors["text"]},
                {"type": "text", "text": f"{username} انضم للعبة", "size": "md", "align": "center", "margin": "md", "color": colors["text2"]},
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "🎮 اختر اللعبة", "text": "ألعاب"}, "style": "primary", "margin": "md", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="✅ انضمام", contents=FlexContainer.from_dict(bubble))


def build_registration_success(username: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """✅ نافذة نجاح التسجيل"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "✅", "size": "xxl", "align": "center", "color": colors["success"]},
                {"type": "text", "text": "تم التسجيل بنجاح", "weight": "bold", "size": "xl", "align": "center", "margin": "sm", "color": colors["text"]},
                {"type": "text", "text": f"مرحباً {username}!", "size": "md", "align": "center", "margin": "md", "color": colors["text2"]},
                {"type": "text", "text": "الآن يمكنك اللعب وكسب النقاط", "size": "sm", "align": "center", "margin": "sm", "color": colors["text2"], "wrap": True},
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "🎮 ابدأ اللعب", "text": "ألعاب"}, "style": "primary", "margin": "md", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "margin": "sm", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="✅ التسجيل", contents=FlexContainer.from_dict(bubble))


def build_theme_change_success(theme_name: str, current_theme: str = DEFAULT_THEME) -> FlexMessage:
    """🎨 نافذة نجاح تغيير الثيم"""
    colors = _safe_get_colors(theme_name)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎨", "size": "xxl", "align": "center", "color": colors["primary"]},
                {"type": "text", "text": "تم التغيير", "weight": "bold", "size": "xl", "align": "center", "margin": "sm", "color": colors["text"]},
                {"type": "text", "text": f"الثيم: {theme_name}", "size": "md", "align": "center", "margin": "md", "color": colors["text2"]},
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "primary", "margin": "md", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🎨 تغيير الثيم", contents=FlexContainer.from_dict(bubble))


def build_error_message(error_text: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """❌ نافذة رسالة خطأ"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "❌", "size": "xxl", "align": "center", "color": colors["error"]},
                {"type": "text", "text": error_text, "weight": "bold", "size": "lg", "align": "center", "margin": "md", "color": colors["text"], "wrap": True},
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "margin": "md", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="❌ خطأ", contents=FlexContainer.from_dict(bubble))


def build_game_stopped(game_name: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """⛔ نافذة إيقاف اللعبة"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "⛔", "size": "xxl", "align": "center", "color": colors["error"]},
                {"type": "text", "text": "تم إيقاف اللعبة", "weight": "bold", "size": "xl", "align": "center", "margin": "sm", "color": colors["text"]},
                {"type": "
