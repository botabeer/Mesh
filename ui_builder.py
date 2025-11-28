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
    """Get theme colors safely"""
    try:
        return get_theme_colors(theme)
    except Exception:
        return get_theme_colors(DEFAULT_THEME)


def create_debug_report(exc: Exception, context: Optional[Dict[str, Any]] = None) -> TextMessage:
    """Create detailed debug report for troubleshooting"""
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
        
        # Truncate if too long
        if len(text) > 1800:
            text = text[:900] + "\n\n...[مقتطع]...\n\n" + text[-800:]
        
        return TextMessage(text=text)
    except Exception:
        return TextMessage(text="⚠️ حدث خطأ غير متوقع")


# ============================================================================
# Quick Reply System (Games Only)
# ============================================================================

def create_games_quick_reply() -> QuickReply:
    """Create Quick Reply with game items only"""
    try:
        items = []
        
        # Build from GAME_LIST (list of tuples: internal, display, icon)
        for game_data in GAME_LIST:
            if len(game_data) >= 3:
                internal_name, display_name, icon = game_data[:3]
                items.append(
                    QuickReplyItem(
                        action=MessageAction(
                            label=f"{icon} {display_name}",
                            text=display_name
                        )
                    )
                )
        
        return QuickReply(items=items[:13])  # LINE limit: 13 items
    
    except Exception as e:
        # Fallback: return empty quick reply
        return QuickReply(items=[])


def attach_quick_reply_to_message(message):
    """Attach games quick reply to any message"""
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
# Glass UI Components
# ============================================================================

def create_glass_header(
    colors: Dict[str, str], 
    title: str, 
    subtitle: Optional[str] = None, 
    icon: Optional[str] = None
) -> List[Dict]:
    """Create glass-style header"""
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


def create_glass_card(
    colors: Dict[str, str], 
    icon: str, 
    title: str, 
    description: str, 
    highlight: bool = False
) -> Dict:
    """Create glass-style card"""
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
                        "color": "#FFFFFF" if highlight else colors["primary"]
                    }
                ],
                "backgroundColor": colors.get("primary", "#000000") if highlight else colors.get("card", "#FFFFFF"),
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
                        "color": colors["text2"],
                        "wrap": True,
                        "margin": "xs"
                    }
                ],
                "flex": 1,
                "spacing": "xs",
                "paddingStart": "md"
            }
        ],
        "backgroundColor": colors.get("glass", colors.get("card", "#FFFFFF")),
        "cornerRadius": "20px",
        "paddingAll": "15px",
        "margin": "sm",
        "borderWidth": "2px" if highlight else "1px",
        "borderColor": colors.get("primary", "#000000") if highlight else colors.get("border", colors.get("shadow1", "#E2E8F0"))
    }


def create_glass_button(
    label: str, 
    text_cmd: str, 
    color: str, 
    icon: Optional[str] = None, 
    style: str = "primary"
) -> Dict:
    """Create glass-style button"""
    button_text = f"{icon} {label}" if icon else label
    return {
        "type": "button",
        "action": {
            "type": "message",
            "label": button_text,
            "text": text_cmd
        },
        "style": style,
        "height": "sm",
        "color": color
    }


def create_button_grid(buttons: List[Dict], columns: int = 2) -> List[Dict]:
    """Create grid layout for buttons"""
    rows = []
    for i in range(0, len(buttons), columns):
        row_buttons = buttons[i:i+columns]
        rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": row_buttons,
            "margin": "sm"
        })
    return rows


def create_section_title(
    colors: Dict[str, str], 
    title: str, 
    icon: Optional[str] = None
) -> Dict:
    """Create section title with separator"""
    title_text = f"{icon} {title}" if icon else title
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": title_text,
                "size": "lg",
                "weight": "bold",
                "color": colors["text"]
            },
            {
                "type": "separator",
                "color": colors.get("primary", "#3B82F6"),
                "margin": "sm"
            }
        ],
        "margin": "xl"
    }


# ============================================================================
# Main UI Windows
# ============================================================================

def build_enhanced_home(
    username: str, 
    points: int, 
    is_registered: bool, 
    theme: str = DEFAULT_THEME
) -> FlexMessage:
    """Build enhanced home screen"""
    try:
        colors = _safe_get_colors(theme)
        status_icon = "✅" if is_registered else "⚠️"
        status_text = "مسجل" if is_registered else "غير مسجل"
        
        # Header
        header = create_glass_header(
            colors, 
            f"{BOT_NAME} v{BOT_VERSION}", 
            "منصة الألعاب الذكية الشاملة",
            "🎮"
        )
        
        # Profile Card
        profile_card = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "👤",
                    "size": "xxl",
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
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{status_icon} {status_text}",
                            "size": "sm",
                            "color": colors["text2"],
                            "flex": 2
                        },
                        {
                            "type": "text",
                            "text": f"⭐ {points}",
                            "size": "sm",
                            "color": colors.get("primary", "#3B82F6"),
                            "align": "end",
                            "flex": 1,
                            "weight": "bold"
                        }
                    ],
                    "margin": "md"
                }
            ],
            "backgroundColor": colors.get("glass", colors.get("card", "#FFFFFF")),
            "cornerRadius": "20px",
            "paddingAll": "20px",
            "borderWidth": "2px",
            "borderColor": colors.get("primary", "#3B82F6")
        }
        
        # Body content
        body = [
            profile_card,
            create_section_title(colors, "الأقسام الرئيسية", "📋"),
            create_glass_card(colors, "🎮", "الألعاب", "اختر من مجموعة ألعاب متنوعة"),
            create_glass_card(colors, "⭐", "نقاطي", "راجع رصيد نقاطك وإحصائياتك"),
            create_glass_card(colors, "🏆", "الصدارة", "تنافس مع اللاعبين الآخرين"),
            create_glass_card(colors, "🎨", "الثيمات", "غيّر مظهر التطبيق"),
            create_glass_card(colors, "🎯", "الأهداف", "اربح النقاط وتصدر القائمة"),
        ]

        # أزرار الإجراءات السريعة
        action_buttons = []
        
        # زر الألعاب
        action_buttons.append(
            create_glass_button("الألعاب", "ألعاب", colors.get("primary", "#3B82F6"), "🎮")
        )
        
        # زر نقاطي
        action_buttons.append(
            create_glass_button("نقاطي", "نقاطي", colors.get("secondary", colors.get("primary", "#3B82F6")), "⭐", style="secondary")
        )
        
        # زر الصدارة
        action_buttons.append(
            create_glass_button("الصدارة", "صدارة", colors.get("secondary", colors.get("primary", "#3B82F6")), "🏆", style="secondary")
        )
        
        # زر الثيمات
        action_buttons.append(
            create_glass_button("الثيمات", "ثيمات", colors.get("secondary", colors.get("primary", "#3B82F6")), "🎨", style="secondary")
        )

        # إضافة الأزرار للواجهة
        button_grids = create_button_grid(action_buttons, columns=2)
        body.extend(button_grids)

        # معلومات إضافية
        body.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "💡 نصيحة: استخدم Quick Reply أسفل الشاشة للوصول السريع للألعاب",
                    "size": "xs",
                    "color": colors["text2"],
                    "wrap": True,
                    "align": "center"
                }
            ],
            "backgroundColor": colors.get("card", "#FFFFFF"),
            "cornerRadius": "15px",
            "paddingAll": "12px",
            "margin": "lg"
        })

        # Footer
        footer = [
            {
                "type": "separator",
                "color": colors.get("border", colors.get("shadow1", "#E2E8F0")),
                "margin": "md"
            },
            {
                "type": "text",
                "text": BOT_RIGHTS,
                "size": "xxs",
                "color": colors["text2"],
                "align": "center",
                "margin": "sm"
            }
        ]

        # بناء Bubble النهائي
        bubble = {
            "type": "bubble",
            "size": "giga",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": header + [
                    {
                        "type": "separator",
                        "color": colors.get("border", colors.get("shadow1", "#E2E8F0")),
                        "margin": "lg"
                    }
                ] + body,
                "paddingAll": "24px",
                "spacing": "md",
                "backgroundColor": colors["bg"]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": footer,
                "paddingAll": "15px",
                "backgroundColor": colors["bg"]
            },
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                },
                "footer": {
                    "backgroundColor": colors["bg"]
                }
            }
        }

        try:
            flex_msg = FlexMessage(
                alt_text="🏠 الصفحة الرئيسية",
                contents=FlexContainer.from_dict(bubble)
            )
            
            # إضافة Quick Reply
            flex_msg = attach_quick_reply_to_message(flex_msg)
            
            return flex_msg
            
        except Exception as e:
            # في حالة الفشل، إرجاع رسالة نصية بسيطة مع تقرير الخطأ
            return create_debug_report(e, {
                "function": "build_enhanced_home",
                "username": username,
                "points": points,
                "theme": theme
            })
