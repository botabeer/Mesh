"""
Bot Mesh - UI Builder v8.5 FIXED
Created by: Abeer Aldosari © 2025
✅ إصلاح backgroundColor issue
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
# Quick Reply System
# ============================================================================

def create_games_quick_reply() -> QuickReply:
    """إنشاء Quick Reply للألعاب"""
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
    """الصفحة الرئيسية"""
    colors = _safe_get_colors(theme)

    header = create_glass_header(
        colors, f"مرحباً {username}", f"النقاط: {points}", "🎮"
    )

    buttons = [
        {"type": "button", "action": {"type": "message", "label": "🎮 ألعاب", "text": "ألعاب"}, "style": "primary", "height": "sm"},
        {"type": "button", "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"}, "style": "link", "height": "sm"},
        {"type": "button", "action": {"type": "message", "label": "🏆 صدارة", "text": "صدارة"}, "style": "link", "height": "sm"},
        {"type": "button", "action": {"type": "message", "label": "🎨 ثيمات", "text": "ثيمات"}, "style": "link", "height": "sm"},
    ]

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + buttons,
            "paddingAll": "20px"
        }
    }

    return attach_quick_reply_to_message(
        FlexMessage(alt_text="الرئيسية", contents=FlexContainer.from_dict(bubble))
    )


def build_games_menu(theme: str = DEFAULT_THEME) -> FlexMessage:
    """قائمة الألعاب"""
    colors = _safe_get_colors(theme)

    header = create_glass_header(colors, "🎮 قائمة الألعاب")

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
            "height": "sm"
        })

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + buttons,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(
        alt_text="الألعاب",
        contents=FlexContainer.from_dict(bubble)
    )


def build_my_points(username: str, total_points: int, stats: Dict, theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(theme)

    contents = [
        {"type": "text", "text": "⭐ نقاطي", "weight": "bold", "size": "xl", "align": "center", "color": colors["primary"]},
        {"type": "separator", "margin": "md"},
        {"type": "text", "text": f"اللاعب: {username}", "size": "md", "margin": "md"},
        {"type": "text", "text": f"النقاط الإجمالية: {total_points}", "size": "lg", "weight": "bold", "margin": "sm", "color": colors["success"]}
    ]

    if stats:
        contents.append({"type": "separator", "margin": "lg"})
        contents.append({"type": "text", "text": "إحصائيات الألعاب:", "weight": "bold", "margin": "md"})
        
        for game_name, data in list(stats.items())[:5]:
            contents.append({
                "type": "text",
                "text": f"{game_name}: {data.get('plays', 0)} لعبة - {data.get('total_score', 0)} نقطة",
                "size": "sm",
                "margin": "xs"
            })

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(bubble))


def build_leaderboard(top_users: List[Tuple[str, int]], theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(theme)

    contents = [
        {"type": "text", "text": "🏆 الصدارة", "weight": "bold", "size": "xl", "align": "center", "color": colors["primary"]},
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
            "weight": "bold" if i < 3 else "regular"
        })

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble))


def build_theme_selector(current_theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(current_theme)

    header = [
        {"type": "text", "text": "🎨 اختر الثيم", "weight": "bold", "size": "xl", "align": "center"},
        {"type": "separator", "margin": "md"}
    ]

    buttons = []
    for name in THEMES.keys():
        marker = "✓" if name == current_theme else ""
        buttons.append({
            "type": "button",
            "action": {"type": "message", "label": f"{marker} {name}", "text": f"ثيم {name}"},
            "style": "primary" if name == current_theme else "link",
            "height": "sm"
        })

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + buttons,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="الثيمات", contents=FlexContainer.from_dict(bubble))


def build_registration_required(theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "⚠️", "size": "xxl", "align": "center"},
                {"type": "text", "text": "يجب التسجيل أولاً", "weight": "bold", "size": "lg", "align": "center", "margin": "md"},
                {"type": "text", "text": "للعب الألعاب وكسب النقاط", "size": "sm", "align": "center", "margin": "sm", "wrap": True},
                {"type": "button", "action": {"type": "message", "label": "✅ انضم الآن", "text": "انضم"}, "style": "primary", "margin": "lg"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="تسجيل", contents=FlexContainer.from_dict(bubble))


def build_winner_announcement(username: str, game_name: str, points: int, total_points: int, theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🏆", "size": "xxl", "align": "center"},
                {"type": "text", "text": "انتهت اللعبة", "weight": "bold", "size": "xl", "align": "center", "margin": "sm"},
                {"type": "separator", "margin": "lg"},
                {"type": "text", "text": f"الفائز: {username}", "size": "lg", "weight": "bold", "align": "center", "margin": "md"},
                {"type": "text", "text": f"اللعبة: {game_name}", "size": "md", "align": "center", "margin": "sm"},
                {"type": "text", "text": f"النقاط المكتسبة: +{points}", "size": "lg", "color": colors["success"], "align": "center", "margin": "md"},
                {"type": "text", "text": f"الإجمالي: {total_points} نقطة", "size": "sm", "align": "center", "margin": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="الفائز", contents=FlexContainer.from_dict(bubble))


def build_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(theme)

    commands = [
        ("🎮 ألعاب", "عرض قائمة الألعاب"),
        ("⭐ نقاطي", "عرض نقاطك وإحصائياتك"),
        ("🏆 صدارة", "عرض أفضل اللاعبين"),
        ("🎨 ثيمات", "تغيير مظهر البوت"),
        ("✅ انضم", "التسجيل في البوت"),
        ("⛔ إيقاف", "إيقاف اللعبة الحالية"),
        ("❓ مساعدة", "عرض هذه القائمة")
    ]

    contents = [
        {"type": "text", "text": "📚 دليل الأوامر", "weight": "bold", "size": "xl", "align": "center"},
        {"type": "separator", "margin": "md"}
    ]

    for cmd, desc in commands:
        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": cmd, "weight": "bold", "size": "md"},
                {"type": "text", "text": desc, "size": "xs", "color": colors["text2"], "wrap": True}
            ],
            "margin": "md"
        })

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="مساعدة", contents=FlexContainer.from_dict(bubble))


def build_multiplayer_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(theme)

    steps = [
        {"type": "text", "text": "👥 وضع الفريقين", "weight": "bold", "size": "xl", "align": "center"},
        {"type": "separator", "margin": "md"},
        {"type": "text", "text": "1️⃣ اكتب: فريقين", "size": "md", "margin": "md"},
        {"type": "text", "text": "لبدء مرحلة الانضمام", "size": "xs", "color": colors["text2"], "margin": "xs"},
        {"type": "text", "text": "2️⃣ اكتب: انضم", "size": "md", "margin": "md"},
        {"type": "text", "text": "للانضمام للعبة الجماعية", "size": "xs", "color": colors["text2"], "margin": "xs"},
        {"type": "text", "text": "3️⃣ اختر اللعبة", "size": "md", "margin": "md"},
        {"type": "text", "text": "سيتم تقسيم الفرق تلقائياً", "size": "xs", "color": colors["text2"], "margin": "xs"}
    ]

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": steps,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="فريقين", contents=FlexContainer.from_dict(bubble))


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
