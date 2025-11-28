# Bot Mesh - UI Builder v8.5 COMPLETE FIXED
# Created by: Abeer Aldosari © 2025

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


def create_debug_report(exc: Exception, context: Optional[Dict[str, Any]] = None) -> TextMessage:
    """إنشاء تقرير خطأ مفصل"""
    try:
        tb = traceback.format_exc()
        ctx_lines = []

        if context:
            for k, v in context.items():
                ctx_lines.append(f"{k}: {str(v)[:100]}")

        ctx_text = "\n".join(ctx_lines) if ctx_lines else "لا توجد معلومات إضافية"

        text = (
            "⚠️ تقرير خطأ\n\n"
            f"الخطأ: {str(exc)[:200]}\n\n"
            f"التفاصيل:\n{tb[:800]}\n\n"
            f"السياق:\n{ctx_text}"
        )

        if len(text) > 1800:
            text = text[:900] + "\n\n...[مقتطع]...\n\n" + text[-800:]

        return TextMessage(text=text)

    except Exception:
        return TextMessage(text="⚠️ حدث خطأ غير متوقع")


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
        {"type": "button", "action": {"type": "message", "label": "🎮 ألعاب", "text": "ألعاب"}},
        {"type": "button", "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"}},
        {"type": "button", "action": {"type": "message", "label": "🏆 صدارة", "text": "صدارة"}},
        {"type": "button", "action": {"type": "message", "label": "🎨 ثيمات", "text": "ثيمات"}},
    ]

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + buttons,
            "backgroundColor": colors["bg"],
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
            }
        })

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + buttons,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(
        alt_text="الألعاب",
        contents=FlexContainer.from_dict(bubble)
    )


def build_my_points(username: str, total_points: int, stats: Dict, theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"{username}", "weight": "bold"},
                {"type": "text", "text": f"النقاط: {total_points}"}
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(bubble))


def build_leaderboard(top_users: List[Tuple[str, int]], theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(theme)

    items = []
    for name, pts in top_users:
        items.append({"type": "text", "text": f"{name} - {pts}"})

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": items,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble))


def build_theme_selector(current_theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(current_theme)

    buttons = []
    for name in THEMES.keys():
        buttons.append({
            "type": "button",
            "action": {"type": "message", "label": name, "text": f"ثيم {name}"}
        })

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": buttons,
            "backgroundColor": colors["bg"],
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
                {"type": "text", "text": "يجب التسجيل أولاً"},
                {"type": "button", "action": {"type": "message", "label": "انضم", "text": "انضم"}}
            ],
            "backgroundColor": colors["bg"],
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
                {"type": "text", "text": "🏆 الفائز"},
                {"type": "text", "text": username},
                {"type": "text", "text": f"{game_name}"},
                {"type": "text", "text": f"+{points}"},
                {"type": "text", "text": f"الإجمالي: {total_points}"}
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="الفائز", contents=FlexContainer.from_dict(bubble))


def build_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(theme)

    items = [
        {"type": "text", "text": "ألعاب"},
        {"type": "text", "text": "نقاطي"},
        {"type": "text", "text": "صدارة"},
        {"type": "text", "text": "ثيمات"},
        {"type": "text", "text": "انضم"},
        {"type": "text", "text": "إيقاف"}
    ]

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": items,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="مساعدة", contents=FlexContainer.from_dict(bubble))


def build_multiplayer_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _safe_get_colors(theme)

    steps = [
        {"type": "text", "text": "1 اكتب فريقين"},
        {"type": "text", "text": "2 اكتب انضم"},
        {"type": "text", "text": "3 ابدأ اللعبة"}
    ]

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": steps,
            "backgroundColor": colors["bg"],
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
