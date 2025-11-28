"""
Bot Mesh - UI Builder v8.5 ENHANCED
Created by: Abeer Aldosari © 2025
✅ واجهات زجاجية احترافية
✅ Quick Reply للألعاب فقط
✅ متوافق 100% مع آلية البوت
✅ معالجة أخطاء محسّنة
✅ دعم جميع الثيمات
"""

import traceback
from typing import List, Optional, Dict, Any

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
    try:
        return get_theme_colors(theme)
    except Exception:
        return get_theme_colors(DEFAULT_THEME)


def create_debug_report(exc: Exception, context: Optional[Dict[str, Any]] = None) -> TextMessage:
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
    try:
        qr = create_games_quick_reply()
        if hasattr(message, 'quick_reply'):
            message.quick_reply = qr
        else:
            setattr(message, 'quick_reply', qr)
    except Exception:
        pass
    return message


# ============================================================================
# Glass Components
# ============================================================================

def create_glass_header(colors, title, subtitle=None, icon=None) -> List[Dict]:
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
    
    return header_content


def create_glass_card(colors, icon, title, description, highlight=False) -> Dict:
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": icon, "size": "xl", "align": "center"}
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
                    {"type": "text", "text": title, "size": "md", "weight": "bold"},
                    {"type": "text", "text": description, "size": "xs", "wrap": True}
                ],
                "flex": 1,
                "paddingStart": "md"
            }
        ],
        "backgroundColor": colors["bg"],
        "cornerRadius": "20px",
        "paddingAll": "15px",
        "margin": "sm"
    }


def create_glass_button(label, text_cmd, color, icon=None, style="primary") -> Dict:
    return {
        "type": "button",
        "action": {"type": "message", "label": label, "text": text_cmd},
        "style": style,
        "height": "sm",
        "color": color
    }


def create_button_grid(buttons: List[Dict], columns: int = 2) -> List[Dict]:
    rows = []
    for i in range(0, len(buttons), columns):
        rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": buttons[i:i+columns]
        })
    return rows


# ============================================================================
# Main UI
# ============================================================================

def build_enhanced_home(username, points, is_registered, theme=DEFAULT_THEME) -> FlexMessage:
    try:
        colors = _safe_get_colors(theme)

        header = create_glass_header(
            colors, f"{BOT_NAME} v{BOT_VERSION}", "منصة الألعاب الذكية", "🎮"
        )

        body = [
            create_glass_card(colors, "🎮", "الألعاب", "اختر لعبتك"),
            create_glass_card(colors, "⭐", "نقاطي", "عرض نقاطك"),
            create_glass_card(colors, "🏆", "الصدارة", "أفضل اللاعبين"),
            create_glass_card(colors, "🎨", "الثيمات", "غيّر شكل البوت"),
            create_glass_card(colors, "🎯", "الأهداف", "حقق الإنجازات")
        ]

        buttons = create_button_grid([
            create_glass_button("الألعاب", "ألعاب", colors["primary"]),
            create_glass_button("نقاطي", "نقاطي", colors["primary"]),
            create_glass_button("الصدارة", "صدارة", colors["primary"]),
            create_glass_button("الثيمات", "ثيمات", colors["primary"]),
        ])

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": header + body + buttons,
                "paddingAll": "20px"
            }
        }

        flex_msg = FlexMessage(
            alt_text="الصفحة الرئيسية",
            contents=FlexContainer.from_dict(bubble)
        )

        return attach_quick_reply_to_message(flex_msg)

    except Exception as e:
        return create_debug_report(e, {"username": username})
