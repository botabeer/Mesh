"""
Bot Mesh - UI Builder v10.1 UNIFIED GAME WINDOWS
Created by: Abeer Aldosari © 2025
✅ نوافذ موحدة للعبة (بداية، مساعدة، أثناء اللعب)
✅ عرض السؤال السابق والإجابة
✅ نظام التوافق المستقل
✅ تصميم زجاجي احترافي
"""

from typing import List, Optional, Dict, Any, Tuple
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction
from constants import BOT_NAME, BOT_VERSION, BOT_RIGHTS, THEMES, DEFAULT_THEME, GAME_LIST

# ============================================================================
# GLASS THEMES (نفس الثيمات السابقة)
# ============================================================================

GLASS_THEMES = {
    "أبيض": {
        "bg": "#F8FAFC", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_alpha": "#F8FAFC",
        "primary": "#3B82F6", "secondary": "#60A5FA", "accent": "#2563EB",
        "text": "#1E293B", "text2": "#64748B", "text3": "#94A3B8",
        "border": "#E2E8F0", "shadow": "#CBD5E1",
        "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "info": "#3B82F6"
    },
    "أسود": {
        "bg": "#0F172A", "card": "#1E293B", "glass": "#1E293B", "glass_alpha": "#0F172A",
        "primary": "#60A5FA", "secondary": "#93C5FD", "accent": "#3B82F6",
        "text": "#F1F5F9", "text2": "#CBD5E1", "text3": "#94A3B8",
        "border": "#334155", "shadow": "#0F172A",
        "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "info": "#60A5FA"
    },
    "رمادي": {
        "bg": "#F9FAFB", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_alpha": "#F3F4F6",
        "primary": "#6B7280", "secondary": "#9CA3AF", "accent": "#4B5563",
        "text": "#111827", "text2": "#6B7280", "text3": "#9CA3AF",
        "border": "#E5E7EB", "shadow": "#D1D5DB",
        "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "info": "#6B7280"
    },
    "أزرق": {
        "bg": "#EFF6FF", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_alpha": "#DBEAFE",
        "primary": "#2563EB", "secondary": "#3B82F6", "accent": "#1D4ED8",
        "text": "#1E3A8A", "text2": "#3B82F6", "text3": "#60A5FA",
        "border": "#BFDBFE", "shadow": "#93C5FD",
        "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "info": "#3B82F6"
    },
    "بنفسجي": {
        "bg": "#F5F3FF", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_alpha": "#EDE9FE",
        "primary": "#8B5CF6", "secondary": "#A78BFA", "accent": "#7C3AED",
        "text": "#4C1D95", "text2": "#7C3AED", "text3": "#A78BFA",
        "border": "#DDD6FE", "shadow": "#C4B5FD",
        "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "info": "#8B5CF6"
    },
    "وردي": {
        "bg": "#FDF2F8", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_alpha": "#FCE7F3",
        "primary": "#EC4899", "secondary": "#F472B6", "accent": "#DB2777",
        "text": "#831843", "text2": "#DB2777", "text3": "#F472B6",
        "border": "#FBCFE8", "shadow": "#F9A8D4",
        "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "info": "#EC4899"
    },
    "أخضر": {
        "bg": "#F0FDF4", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_alpha": "#DCFCE7",
        "primary": "#10B981", "secondary": "#34D399", "accent": "#059669",
        "text": "#064E3B", "text2": "#059669", "text3": "#34D399",
        "border": "#BBF7D0", "shadow": "#86EFAC",
        "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "info": "#10B981"
    },
    "برتقالي": {
        "bg": "#FFF7ED", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_alpha": "#FFEDD5",
        "primary": "#F97316", "secondary": "#FB923C", "accent": "#EA580C",
        "text": "#7C2D12", "text2": "#EA580C", "text3": "#FB923C",
        "border": "#FED7AA", "shadow": "#FDBA74",
        "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "info": "#F97316"
    },
    "بني": {
        "bg": "#FEFCF9", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_alpha": "#F5E6D8",
        "primary": "#92400E", "secondary": "#B45309", "accent": "#78350F",
        "text": "#451A03", "text2": "#92400E", "text3": "#B45309",
        "border": "#E7D4C3", "shadow": "#D4B8A0",
        "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "info": "#92400E"
    }
}

def get_theme(theme_name: str = DEFAULT_THEME) -> Dict[str, str]:
    """الحصول على ألوان الثيم"""
    return GLASS_THEMES.get(theme_name, GLASS_THEMES[DEFAULT_THEME])

# ============================================================================
# QUICK REPLY SYSTEM
# ============================================================================

def create_games_quick_reply() -> QuickReply:
    """إنشاء Quick Reply للألعاب"""
    try:
        items = []
        for _, display_name, icon in GAME_LIST[:13]:
            items.append(QuickReplyItem(action=MessageAction(label=f"{icon} {display_name}", text=display_name)))
        return QuickReply(items=items)
    except:
        return QuickReply(items=[])

def attach_quick_reply(message):
    """إضافة Quick Reply لأي رسالة"""
    try:
        message.quick_reply = create_games_quick_reply()
    except:
        pass
    return message

# ============================================================================
# UNIFIED GAME WINDOW - نافذة موحدة للعبة
# ============================================================================

def build_game_window(
    game_name: str,
    game_icon: str,
    question_number: int,
    total_questions: int,
    question_text: str,
    additional_info: Optional[str] = None,
    previous_question: Optional[str] = None,
    previous_answer: Optional[str] = None,
    show_hints: bool = True,
    theme: str = DEFAULT_THEME
) -> FlexMessage:
    """
    🎮 نافذة اللعبة الموحدة - تصميم احترافي
    
    Parameters:
    - game_name: اسم اللعبة
    - game_icon: أيقونة اللعبة
    - question_number: رقم السؤال الحالي
    - total_questions: إجمالي الأسئلة
    - question_text: نص السؤال
    - additional_info: معلومات إضافية (وقت، تعليمات)
    - previous_question: السؤال السابق
    - previous_answer: إجابة السؤال السابق
    - show_hints: إظهار أزرار لمح/جاوب
    - theme: الثيم
    """
    colors = get_theme(theme)
    contents = []
    
    # ==================== HEADER ====================
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": game_icon,
                "size": "xxl",
                "align": "center"
            },
            {
                "type": "text",
                "text": game_name,
                "size": "md",
                "weight": "bold",
                "color": colors["primary"],
                "align": "center",
                "margin": "sm"
            },
            {
                "type": "text",
                "text": f"سؤال {question_number} من {total_questions}",
                "size": "xs",
                "color": colors["text3"],
                "align": "center",
                "margin": "xs"
            }
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "15px"
    })
    
    contents.append({
        "type": "separator",
        "margin": "lg",
        "color": colors["border"]
    })
    
    # ==================== السؤال السابق (إن وجد) ====================
    if previous_question and previous_answer:
        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "📋 السؤال السابق",
                    "size": "xs",
                    "color": colors["text3"],
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": previous_question[:50] + "..." if len(previous_question) > 50 else previous_question,
                    "size": "xs",
                    "color": colors["text2"],
                    "wrap": True,
                    "margin": "xs"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "✅",
                            "size": "xs",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": previous_answer,
                            "size": "xs",
                            "color": colors["success"],
                            "weight": "bold",
                            "wrap": True,
                            "margin": "xs"
                        }
                    ],
                    "margin": "xs"
                }
            ],
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "12px",
            "paddingAll": "12px",
            "margin": "lg",
            "borderWidth": "1px",
            "borderColor": colors["border"]
        })
        
        contents.append({
            "type": "separator",
            "margin": "md",
            "color": colors["border"]
        })
    
    # ==================== السؤال الحالي ====================
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": question_text,
                "size": "lg",
                "color": colors["text"],
                "align": "center",
                "wrap": True,
                "weight": "bold"
            }
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "15px",
        "paddingAll": "20px",
        "margin": "lg"
    })
    
    # ==================== معلومات إضافية ====================
    if additional_info:
        contents.append({
            "type": "text",
            "text": additional_info,
            "size": "xs",
            "color": colors["text2"],
            "align": "center",
            "wrap": True,
            "margin": "md"
        })
    
    # ==================== أزرار لمح/جاوب ====================
    if show_hints:
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "💡 لمح",
                        "text": "لمح"
                    },
                    "style": "link",
                    "color": colors["info"],
                    "height": "sm",
                    "flex": 1
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "🔍 جاوب",
                        "text": "جاوب"
                    },
                    "style": "link",
                    "color": colors["secondary"],
                    "height": "sm",
                    "flex": 1
                }
            ],
            "spacing": "sm",
            "margin": "lg"
        })
    
    # ==================== زر إيقاف ====================
    contents.append({
        "type": "button",
        "action": {
            "type": "message",
            "label": "⛔ إيقاف",
            "text": "إيقاف"
        },
        "style": "link",
        "color": colors["error"],
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
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text=f"{game_icon} {game_name}", contents=FlexContainer.from_dict(bubble))
    )

# ============================================================================
# GAME START WINDOW - نافذة بداية اللعبة
# ============================================================================

def build_game_start_window(
    game_name: str,
    game_icon: str,
    game_description: str,
    total_questions: int,
    game_features: List[str],
    theme: str = DEFAULT_THEME
) -> FlexMessage:
    """
    🎯 نافذة بداية اللعبة - ترحيب وتعليمات
    """
    colors = get_theme(theme)
    contents = []
    
    # Header
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": game_icon,
                "size": "xxl",
                "align": "center"
            },
            {
                "type": "text",
                "text": game_name,
                "size": "xl",
                "weight": "bold",
                "color": colors["primary"],
                "align": "center",
                "margin": "md"
            },
            {
                "type": "text",
                "text": game_description,
                "size": "sm",
                "color": colors["text2"],
                "align": "center",
                "wrap": True,
                "margin": "sm"
            }
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "20px"
    })
    
    contents.append({
        "type": "separator",
        "margin": "lg",
        "color": colors["border"]
    })
    
    # تفاصيل اللعبة
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "📊 تفاصيل اللعبة",
                "size": "md",
                "weight": "bold",
                "color": colors["text"],
                "margin": "lg"
            },
            {
                "type": "text",
                "text": f"🎮 عدد الأسئلة: {total_questions}",
                "size": "sm",
                "color": colors["text2"],
                "margin": "md"
            }
        ]
    })
    
    # المميزات
    if game_features:
        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "✨ المميزات",
                    "size": "md",
                    "weight": "bold",
                    "color": colors["text"],
                    "margin": "lg"
                }
            ] + [
                {
                    "type": "text",
                    "text": f"• {feature}",
                    "size": "sm",
                    "color": colors["text2"],
                    "wrap": True,
                    "margin": "sm"
                } for feature in game_features
            ]
        })
    
    # زر البدء
    contents.append({
        "type": "button",
        "action": {
            "type": "message",
            "label": "🚀 ابدأ اللعب",
            "text": game_name
        },
        "style": "primary",
        "color": colors["primary"],
        "height": "sm",
        "margin": "xl"
    })
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text=f"🎯 {game_name}", contents=FlexContainer.from_dict(bubble))
    )

# ============================================================================
# GAME HELP WINDOW - نافذة مساعدة اللعبة
# ============================================================================

def build_game_help_window(
    game_name: str,
    game_icon: str,
    instructions: List[Dict[str, str]],
    tips: List[str],
    theme: str = DEFAULT_THEME
) -> FlexMessage:
    """
    ❓ نافذة مساعدة اللعبة - تعليمات ونصائح
    
    instructions: [{"title": "...", "description": "..."}]
    tips: ["نصيحة 1", "نصيحة 2"]
    """
    colors = get_theme(theme)
    contents = []
    
    # Header
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": game_icon,
                "size": "xxl",
                "align": "center"
            },
            {
                "type": "text",
                "text": f"مساعدة {game_name}",
                "size": "lg",
                "weight": "bold",
                "color": colors["primary"],
                "align": "center",
                "margin": "md"
            }
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "15px"
    })
    
    contents.append({
        "type": "separator",
        "margin": "lg",
        "color": colors["border"]
    })
    
    # التعليمات
    if instructions:
        contents.append({
            "type": "text",
            "text": "📖 كيفية اللعب",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "lg"
        })
        
        for i, instruction in enumerate(instructions, 1):
            contents.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"{i}",
                                "size": "xs",
                                "color": colors["primary"],
                                "weight": "bold",
                                "flex": 0,
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": instruction.get("title", ""),
                                "size": "sm",
                                "color": colors["text"],
                                "weight": "bold",
                                "margin": "sm",
                                "wrap": True
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": instruction.get("description", ""),
                        "size": "xs",
                        "color": colors["text2"],
                        "wrap": True,
                        "margin": "xs"
                    }
                ],
                "backgroundColor": colors["glass_alpha"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "margin": "sm"
            })
    
    # النصائح
    if tips:
        contents.append({
            "type": "separator",
            "margin": "lg",
            "color": colors["border"]
        })
        
        contents.append({
            "type": "text",
            "text": "💡 نصائح",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "lg"
        })
        
        for tip in tips:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "•",
                        "size": "sm",
                        "color": colors["primary"],
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": tip,
                        "size": "xs",
                        "color": colors["text2"],
                        "wrap": True,
                        "margin": "sm"
                    }
                ],
                "margin": "sm"
            })
    
    # زر البدء
    contents.append({
        "type": "button",
        "action": {
            "type": "message",
            "label": "🎮 ابدأ اللعب",
            "text": game_name
        },
        "style": "primary",
        "color": colors["primary"],
        "height": "sm",
        "margin": "xl"
    })
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text=f"❓ مساعدة {game_name}", contents=FlexContainer.from_dict(bubble))
    )

# ============================================================================
# COMPATIBILITY RESULT - نتيجة التوافق (بدون نقاط)
# ============================================================================

def build_compatibility_result(
    name1: str,
    name2: str,
    percentage: int,
    message: str,
    theme: str = DEFAULT_THEME
) -> FlexMessage:
    """
    💕 نافذة نتيجة التوافق - نظام مستقل بدون نقاط
    """
    colors = get_theme(theme)
    
    # تحديد اللون حسب النسبة
    if percentage >= 90:
        bar_color = colors["success"]
        icon = "💖"
    elif percentage >= 75:
        bar_color = colors["primary"]
        icon = "💗"
    elif percentage >= 60:
        bar_color = colors["warning"]
        icon = "💛"
    elif percentage >= 45:
        bar_color = colors["info"]
        icon = "💙"
    else:
        bar_color = colors["error"]
        icon = "💔"
    
    contents = []
    
    # Header
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "💕",
                "size": "xxl",
                "align": "center"
            },
            {
                "type": "text",
                "text": "نتيجة التوافق",
                "size": "lg",
                "weight": "bold",
                "color": colors["primary"],
                "align": "center",
                "margin": "md"
            }
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "15px"
    })
    
    contents.append({
        "type": "separator",
        "margin": "lg",
        "color": colors["border"]
    })
    
    # الأسماء
    contents.append({
        "type": "text",
        "text": f"{name1}  ×  {name2}",
        "size": "md",
        "weight": "bold",
        "color": colors["text"],
        "align": "center",
        "wrap": True,
        "margin": "lg"
    })
    
    # النسبة الكبيرة
    contents.append({
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
                "text": f"{percentage}%",
                "size": "xxl",
                "weight": "bold",
                "color": bar_color,
                "align": "center",
                "margin": "sm"
            }
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "25px",
        "margin": "lg"
    })
    
    # شريط التقدم
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "backgroundColor": bar_color,
                        "width": f"{percentage}%",
                        "height": "8px",
                        "cornerRadius": "4px"
                    }
                ],
                "backgroundColor": colors["border"],
                "height": "8px",
                "cornerRadius": "4px"
            }
        ],
        "margin": "md"
    })
    
    # الرسالة
    contents.append({
        "type": "text",
        "text": message,
        "size": "md",
        "color": colors["text"],
        "align": "center",
        "wrap": True,
        "weight": "bold",
        "margin": "lg"
    })
    
    # ملاحظة
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "💡 نفس النتيجة لو كتبت:",
                "size": "xs",
                "color": colors["text3"],
                "align": "center"
            },
            {
                "type": "text",
                "text": f"{name2} و {name1}",
                "size": "xs",
                "color": colors["text2"],
                "align": "center",
                "margin": "xs"
            }
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "12px",
        "paddingAll": "12px",
        "margin": "lg"
    })
    
    # زر إعادة
    contents.append({
        "type": "button",
        "action": {
            "type": "message",
            "label": "🔄 حساب جديد",
            "text": "توافق"
        },
        "style": "link",
        "color": colors["primary"],
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
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return attach_quick_reply(
        FlexMessage(alt_text="💕 نتيجة التوافق", contents=FlexContainer.from_dict(bubble))
    )

# ============================================================================
# LEGACY FUNCTIONS - الدوال القديمة للتوافق
# ============================================================================

def build_enhanced_home(username: str, points: int, is_registered: bool, theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏠 الصفحة الرئيسية"""
    colors = get_theme(theme)
    contents = []
    
    # Header
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": "👋", "size": "xxl", "align": "center"},
            {"type": "text", "text": f"مرحباً {username}", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center", "margin": "md"},
            {"type": "text", "text": f"🎮 {BOT_NAME} v{BOT_VERSION}", "size": "sm", "color": colors["text2"], "align": "center", "margin": "xs"}
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "15px"
    })
    
    contents.append({"type": "separator", "margin": "lg", "color": colors["border"]})
    
    # النقاط
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": "⭐", "size": "xl", "align": "center", "color": colors["warning"]},
            {"type": "text", "text": str(points), "size": "xxl", "weight": "bold", "align": "center", "color": colors["primary"], "margin": "xs"},
            {"type": "text", "text": "نقاطك الإجمالية", "size": "xs", "align": "center", "color": colors["text3"], "margin": "xs"}
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "20px",
        "margin": "lg"
    })
    
    # الأزرار
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "button", "action": {"type": "message", "label": "🎮 الألعاب", "text": "ألعاب"}, "height": "sm", "style": "primary", "color": colors["primary"]},
            {"type": "button", "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"}, "height": "sm", "style": "link"},
            {"type": "button", "action": {"type": "message", "label": "🏆 الصدارة", "text": "صدارة"}, "height": "sm", "style": "link"},
            {"type": "button", "action": {"type": "message", "label": "🎨 الثيمات", "text": "ثيمات"}, "height": "sm", "style": "link"}
        ],
        "spacing": "sm",
        "margin": "lg"
    })
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": colors["bg"]}
    }
    
    return attach_quick_reply(FlexMessage(alt_text="🏠 الرئيسية", contents=FlexContainer.from_dict(bubble)))


def build_games_menu(theme: str = DEFAULT_THEME) -> FlexMessage:
    """🎮 قائمة الألعاب"""
    colors = get_theme(theme)
    contents = []
    
    # Header
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": "🎮", "size": "xxl", "align": "center"},
            {"type": "text", "text": "الألعاب المتاحة", "size": "lg", "weight": "bold", "color": colors["primary"], "align": "center", "margin": "md"}
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "15px"
    })
    
    contents.append({"type": "separator", "margin": "lg", "color": colors["border"]})
    
    # الألعاب في شبكة
    row_contents = []
    for i, (_, display_name, icon) in enumerate(GAME_LIST):
        game_box = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": icon, "size": "xxl", "align": "center", "color": colors["primary"]},
                {"type": "text", "text": display_name, "size": "xs", "align": "center", "color": colors["text"], "margin": "sm", "wrap": True, "weight": "bold"}
            ],
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "action": {"type": "message", "text": display_name},
            "flex": 1
        }
        
        row_contents.append(game_box)
        
        if (i + 1) % 2 == 0 or i == len(GAME_LIST) - 1:
            contents.append({"type": "box", "layout": "horizontal", "contents": row_contents.copy(), "spacing": "sm", "margin": "md"})
            row_contents.clear()
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": colors["bg"]}
    }
    
    return attach_quick_reply(FlexMessage(alt_text="🎮 الألعاب", contents=FlexContainer.from_dict(bubble)))


def build_my_points(username: str, total_points: int, stats: Dict, theme: str = DEFAULT_THEME) -> FlexMessage:
    """⭐ نقاطي"""
    colors = get_theme(theme)
    contents = []
    
    # Header
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": "⭐", "size": "xxl", "align": "center"},
            {"type": "text", "text": "نقاطي", "size": "lg", "weight": "bold", "color": colors["primary"], "align": "center", "margin": "md"}
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "15px"
    })
    
    contents.append({"type": "separator", "margin": "lg", "color": colors["border"]})
    
    # النقاط
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": "🏆", "size": "xxl", "align": "center"},
            {"type": "text", "text": str(total_points), "size": "xxl", "weight": "bold", "align": "center", "color": colors["primary"], "margin": "sm"},
            {"type": "text", "text": "النقاط الإجمالية", "size": "sm", "align": "center", "color": colors["text2"], "margin": "xs"}
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "25px",
        "margin": "lg"
    })
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": colors["bg"]}
    }
    
    return attach_quick_reply(FlexMessage(alt_text="⭐ نقاطي", contents=FlexContainer.from_dict(bubble)))


def build_leaderboard(top_users: List[Tuple[str, int]], theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏆 الصدارة"""
    colors = get_theme(theme)
    contents = []
    
    # Header
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": "🏆", "size": "xxl", "align": "center"},
            {"type": "text", "text": "لوحة الصدارة", "size": "lg", "weight": "bold", "color": colors["primary"], "align": "center", "margin": "md"}
        ],
        "backgroundColor": colors["glass_alpha"],
        "cornerRadius": "20px",
        "paddingAll": "15px"
    })
    
    contents.append({"type": "separator", "margin": "lg", "color": colors["border"]})
    
    # أفضل 3
    medals = ["🥇", "🥈", "🥉"]
    for i in range(min(3, len(top_users))):
        name, pts = top_users[i]
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": medals[i], "size": "xl", "flex": 0},
                {"type": "text", "text": name, "size": "md", "color": colors["text"], "margin": "md"},
                {"type": "text", "text": str(pts), "size": "md", "color": colors["primary"], "align": "end", "weight": "bold"}
            ],
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "margin": "md"
        })
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": colors["bg"]}
    }
    
    return attach_quick_reply(FlexMessage(alt_text="🏆 الصدارة", contents=FlexContainer.from_dict(bubble)))


def build_registration_required(theme: str = DEFAULT_THEME) -> FlexMessage:
    """⚠️ تطلب التسجيل"""
    colors = get_theme(theme)
    contents = [
        {"type": "text", "text": "⚠️", "size": "xxl", "align": "center", "color": colors["warning"]},
        {"type": "text", "text": "يجب التسجيل أولاً", "size": "lg", "weight": "bold", "color": colors["text"], "align": "center", "margin": "lg"},
        {"type": "button", "action": {"type": "message", "label": "✅ انضم الآن", "text": "انضم"}, "style": "primary", "height": "sm", "margin": "lg"}
    ]
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "25px", "backgroundColor": colors["bg"]}
    }
    
    return attach_quick_reply(FlexMessage(alt_text="⚠️ تسجيل مطلوب", contents=FlexContainer.from_dict(bubble)))


def build_winner_announcement(username: str, game_name: str, points: int, total_points: int, theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏆 إعلان الفائز"""
    colors = get_theme(theme)
    contents = [
        {"type": "text", "text": "👑", "size": "xxl", "align": "center"},
        {"type": "text", "text": "مبروك!", "size": "xxl", "weight": "bold", "color": colors["success"], "align": "center", "margin": "lg"},
        {"type": "separator", "margin": "lg", "color": colors["border"]},
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🏆 الفائز", "size": "sm", "color": colors["text3"], "align": "center"},
                {"type": "text", "text": username, "size": "xl", "weight": "bold", "color": colors["text"], "align": "center", "margin": "sm"}
            ],
            "backgroundColor": colors["glass_alpha"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "margin": "lg"
        },
        {"type": "button", "action": {"type": "message", "label": "🎮 لعبة جديدة", "text": "ألعاب"}, "style": "primary", "height": "sm", "margin": "lg"}
    ]
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "25px", "backgroundColor": colors["bg"]}
    }
    
    return attach_quick_reply(FlexMessage(alt_text="🏆 مبروك", contents=FlexContainer.from_dict(bubble)))


def build_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """❓ المساعدة"""
    colors = get_theme(theme)
    contents = [
        {"type": "text", "text": "❓", "size": "xxl", "align": "center"},
        {"type": "text", "text": "المساعدة", "size": "lg", "weight": "bold", "color": colors["primary"], "align": "center", "margin": "md"},
        {"type": "separator", "margin": "lg", "color": colors["border"]},
        {"type": "text", "text": "🎮 ألعاب - عرض الألعاب", "size": "sm", "color": colors["text"], "margin": "lg", "wrap": True},
        {"type": "text", "text": "⭐ نقاطي - نقاطك", "size": "sm", "color": colors["text"], "margin": "sm", "wrap": True},
        {"type": "text", "text": "🏆 صدارة - المتصدرين", "size": "sm", "color": colors["text"], "margin": "sm", "wrap": True}
    ]
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": colors["bg"]}
    }
    
    return attach_quick_reply(FlexMessage(alt_text="❓ المساعدة", contents=FlexContainer.from_dict(bubble)))


def build_theme_selector(current_theme: str = DEFAULT_THEME) -> FlexMessage:
    """🎨 اختيار الثيم"""
    colors = get_theme(current_theme)
    contents = [
        {"type": "text", "text": "🎨", "size": "xxl", "align": "center"},
        {"type": "text", "text": "اختر الثيم", "size": "lg", "weight": "bold", "color": colors["primary"], "align": "center", "margin": "md"},
        {"type": "separator", "margin": "lg", "color": colors["border"]}
    ]
    
    row_contents = []
    for i, (theme_name, theme_colors) in enumerate(GLASS_THEMES.items()):
        is_selected = theme_name == current_theme
        theme_box = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "box", "layout": "vertical", "contents": [{"type": "filler"}], "backgroundColor": theme_colors["primary"], "cornerRadius": "8px", "height": "30px"},
                {"type": "text", "text": "✓" if is_selected else theme_name, "size": "xs", "align": "center", "color": colors["text"], "margin": "sm", "weight": "bold" if is_selected else "regular"}
            ],
            "backgroundColor": theme_colors["glass_alpha"] if is_selected else colors["glass_alpha"],
            "cornerRadius": "12px",
            "paddingAll": "10px",
            "action": {"type": "message", "text": f"ثيم {theme_name}"},
            "flex": 1
        }
        
        row_contents.append(theme_box)
        
        if (i + 1) % 3 == 0 or i == len(GLASS_THEMES) - 1:
            contents.append({"type": "box", "layout": "horizontal", "contents": row_contents.copy(), "spacing": "sm", "margin": "md"})
            row_contents.clear()
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": colors["bg"]}
    }
    
    return attach_quick_reply(FlexMessage(alt_text="🎨 الثيمات", contents=FlexContainer.from_dict(bubble)))


def build_multiplayer_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """👥 مساعدة الفرق"""
    colors = get_theme(theme)
    contents = [
        {"type": "text", "text": "👥", "size": "xxl", "align": "center"},
        {"type": "text", "text": "وضع الفريقين", "size": "lg", "weight": "bold", "color": colors["primary"], "align": "center", "margin": "md"},
        {"type": "separator", "margin": "lg", "color": colors["border"]},
        {"type": "text", "text": "1️⃣ اكتب: فريقين", "size": "sm", "color": colors["text"], "margin": "lg"},
        {"type": "text", "text": "2️⃣ اكتب: انضم", "size": "sm", "color": colors["text"], "margin": "sm"},
        {"type": "text", "text": "3️⃣ اختر اللعبة", "size": "sm", "color": colors["text"], "margin": "sm"}
    ]
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": colors["bg"]}
    }
    
    return attach_quick_reply(FlexMessage(alt_text="👥 الفرق", contents=FlexContainer.from_dict(bubble)))


# دوال إضافية مطلوبة
def build_registration_success(username: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = get_theme(theme)
    return TextMessage(text=f"✅ مرحباً {username}! تم التسجيل بنجاح")

def build_join_confirmation(username: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    return TextMessage(text=f"✅ {username} انضم للعبة")

def build_team_game_end(team_points: Dict[str, int], theme: str = DEFAULT_THEME) -> FlexMessage:
    return TextMessage(text=f"🏁 انتهت اللعبة")

def build_theme_change_success(theme_name: str, theme: str) -> FlexMessage:
    return TextMessage(text=f"✅ تم تغيير الثيم إلى {theme_name}")

def build_game_stopped(game_name: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    return TextMessage(text=f"⛔ تم إيقاف {game_name}")

def build_error_message(message: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    return TextMessage(text=f"❌ {message}")

def build_answer_feedback(message: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    return TextMessage(text=message)


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "get_theme",
    "attach_quick_reply",
    "build_game_window",
    "build_game_start_window",
    "build_game_help_window",
    "build_compatibility_result",
    "build_enhanced_home",
    "build_games_menu",
    "build_my_points",
    "build_leaderboard",
    "build_registration_required",
    "build_winner_announcement",
    "build_help_window",
    "build_theme_selector",
    "build_multiplayer_help_window",
    "build_registration_success",
    "build_join_confirmation",
    "build_team_game_end",
    "build_theme_change_success",
    "build_game_stopped",
    "build_error_message",
    "build_answer_feedback"
]
