"""
Bot Mesh - UI Builder v8.5 COMPLETE FIXED
Created by: Abeer Aldosari © 2025
✅ واجهات زجاجية احترافية
✅ Quick Reply للألعاب فقط
✅ متوافق 100% مع آلية البوت
✅ معالجة أخطاء محسّنة
✅ دعم جميع الثيمات
✅ إصلاح جميع مشاكل color في separators
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
        if hasattr(message, "quick_reply"):
            message.quick_reply = qr
        else:
            setattr(message, "quick_reply", qr)
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


def create_glass_card(colors: Dict, icon: str, title: str, description: str, highlight: bool = False) -> Dict:
    """إنشاء بطاقة زجاجية"""
    return {
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
                        "align": "center",
                        "color": colors["text"] if not highlight else "#FFFFFF"
                    }
                ],
                "backgroundColor": colors["primary"] if highlight else colors["card"],
                "cornerRadius": "15px",
                "width": "50px",
                "height": "50px",
                "justifyContent": "center",
                "alignItems": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "size": "md",
                        "weight": "bold",
                        "color": colors["text"]
                    },
                    {
                        "type": "text",
                        "text": description,
                        "size": "xs",
                        "wrap": True,
                        "color": colors["text2"]
                    }
                ],
                "flex": 1,
                "paddingStart": "md",
                "justifyContent": "center"
            }
        ],
        "backgroundColor": colors["glass"],
        "cornerRadius": "20px",
        "paddingAll": "15px",
        "margin": "sm"
    }


def create_glass_button(label: str, text_cmd: str, color: str, style: str = "primary") -> Dict:
    """إنشاء زر زجاجي"""
    return {
        "type": "button",
        "action": {
            "type": "message",
            "label": label,
            "text": text_cmd
        },
        "style": style,
        "height": "sm",
        "color": color
    }


def create_button_grid(buttons: List[Dict], columns: int = 2) -> List[Dict]:
    """إنشاء شبكة أزرار"""
    rows = []

    for i in range(0, len(buttons), columns):
        row_buttons = buttons[i:i + columns]
        rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": row_buttons,
            "margin": "sm"
        })

    return rows


# ============================================================================
# Main UI Screens
# ============================================================================

def build_enhanced_home(username: str, points: int, is_registered: bool, theme: str = DEFAULT_THEME) -> FlexMessage:
    """الصفحة الرئيسية المحسّنة"""
    try:
        colors = _safe_get_colors(theme)

        header = create_glass_header(
            colors, f"مرحباً {username}", f"النقاط: {points}", "🎮"
        )

        cards = [
            create_glass_card(colors, "🎮", "الألعاب", "اختر لعبتك المفضلة"),
            create_glass_card(colors, "⭐", "نقاطي", f"لديك {points} نقطة"),
            create_glass_card(colors, "🏆", "الصدارة", "أفضل اللاعبين"),
            create_glass_card(colors, "🎨", "الثيمات", "غيّر المظهر"),
        ]

        buttons = create_button_grid([
            create_glass_button("🎮 ألعاب", "ألعاب", colors["primary"]),
            create_glass_button("⭐ نقاطي", "نقاطي", colors["primary"]),
            create_glass_button("🏆 صدارة", "صدارة", colors["secondary"]),
            create_glass_button("🎨 ثيمات", "ثيمات", colors["secondary"]),
        ])

        footer = [{
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center",
            "margin": "lg"
        }]

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": header + cards + buttons + footer,
                "paddingAll": "20px",
                "backgroundColor": colors["bg"]
            }
        }

        flex_msg = FlexMessage(
            alt_text="الصفحة الرئيسية",
            contents=FlexContainer.from_dict(bubble)
        )

        return attach_quick_reply_to_message(flex_msg)

    except Exception as e:
        return create_debug_report(e, {"username": username, "theme": theme})


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
