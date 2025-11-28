"""
Bot Mesh - UI Builder v11.0 FLAT DESIGN (LINE Style)
Created by: Abeer Aldosari © 2025
✅ تصميم مسطح يطابق الصور تماماً
✅ أزرار دائرية ناعمة
✅ شبكات منظمة
✅ ألوان LINE الأصلية
"""

from typing import List, Optional, Dict, Any, Tuple
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction
from constants import BOT_NAME, BOT_VERSION, BOT_RIGHTS, GAME_LIST, DEFAULT_THEME

# ============================================================================
# FLAT THEMES - ألوان مسطحة ناعمة كالصور
# ============================================================================

FLAT_THEMES = {
    "رمادي": {
        "bg": "#F5F5F5",           # خلفية رمادية فاتحة جداً
        "card": "#FFFFFF",          # بطاقات بيضاء
        "primary": "#6B7C93",       # رمادي-أزرق للعناوين
        "secondary": "#8B9BAE",     # رمادي فاتح
        "text": "#2C3E50",          # نص داكن
        "text2": "#7F8C8D",         # نص ثانوي
        "text3": "#95A5A6",         # نص باهت
        "button": "#F0F2F5",        # خلفية أزرار
        "button_text": "#6B7C93",   # نص الأزرار
        "border": "#E8EAED",        # حدود خفيفة
        "success": "#27AE60",       # أخضر
        "error": "#E74C3C",         # أحمر
        "warning": "#F39C12",       # برتقالي
        "info": "#3498DB"           # أزرق
    },
    "أبيض": {
        "bg": "#FFFFFF",
        "card": "#F8F9FA",
        "primary": "#5B6B7A",
        "secondary": "#8B9BAE",
        "text": "#212529",
        "text2": "#6C757D",
        "text3": "#ADB5BD",
        "button": "#F0F2F5",
        "button_text": "#5B6B7A",
        "border": "#DEE2E6",
        "success": "#28A745",
        "error": "#DC3545",
        "warning": "#FFC107",
        "info": "#17A2B8"
    },
    "أسود": {
        "bg": "#1C1E21",
        "card": "#242527",
        "primary": "#7B8FA3",
        "secondary": "#9BABBE",
        "text": "#E4E6EB",
        "text2": "#B0B3B8",
        "text3": "#8A8D91",
        "button": "#3A3B3C",
        "button_text": "#B0B3B8",
        "border": "#3E4042",
        "success": "#2ECC71",
        "error": "#E74C3C",
        "warning": "#F39C12",
        "info": "#3498DB"
    }
}

def get_theme(theme_name: str = "رمادي") -> Dict[str, str]:
    """الحصول على ألوان الثيم"""
    return FLAT_THEMES.get(theme_name, FLAT_THEMES["رمادي"])

# ============================================================================
# QUICK REPLY - كما في الصور
# ============================================================================

def create_games_quick_reply() -> QuickReply:
    """Quick Reply للألعاب (12 لعبة)"""
    try:
        items = []
        for _, display_name, icon in GAME_LIST[:12]:  # 12 لعبة فقط
            items.append(QuickReplyItem(
                action=MessageAction(
                    label=f"{icon} {display_name}",
                    text=display_name
                )
            ))
        return QuickReply(items=items)
    except:
        return QuickReply(items=[])

def attach_quick_reply(message):
    """إضافة Quick Reply دائماً"""
    try:
        message.quick_reply = create_games_quick_reply()
    except:
        pass
    return message

# ============================================================================
# HOME SCREEN - الشاشة الرئيسية (الصورة 1 و 2)
# ============================================================================

def build_enhanced_home(username: str, points: int, is_registered: bool, theme: str = "رمادي") -> FlexMessage:
    """
    🏠 الشاشة الرئيسية - نفس تصميم الصور تماماً
    - أيقونة اللعبة أعلى
    - اختيار الثيم (grid 3x3)
    - حالة التسجيل
    - الأزرار الرئيسية
    """
    colors = get_theme(theme)
    
    contents = []
    
    # ==================== HEADER - الأيقونة والعنوان ====================
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "image",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",  # placeholder
                "size": "md",
                "aspectRatio": "1:1",
                "aspectMode": "cover"
            },
            {
                "type": "text",
                "text": "Bot Mesh",
                "size": "xl",
                "weight": "bold",
                "color": colors["text"],
                "align": "center",
                "margin": "md"
            }
        ],
        "spacing": "none"
    })
    
    # ==================== REGISTRATION STATUS ====================
    status_text = "✅ مسجل" if is_registered else "⚪ غير مسجل"
    status_color = colors["success"] if is_registered else colors["text3"]
    
    contents.append({
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": "نقطة | ",
                "size": "sm",
                "color": colors["text2"],
                "flex": 0
            },
            {
                "type": "text",
                "text": status_text,
                "size": "sm",
                "color": status_color,
                "flex": 0
            },
            {
                "type": "text",
                "text": f" {points}",
                "size": "sm",
                "color": colors["text"],
                "align": "end"
            }
        ],
        "margin": "lg"
    })
    
    # ==================== THEME SELECTOR - شبكة 3x3 ====================
    contents.append({
        "type": "text",
        "text": "🎨 :اختر الثيم",
        "size": "sm",
        "color": colors["text2"],
        "margin": "xl",
        "align": "start"
    })
    
    # الثيمات في شبكة 3x3
    theme_names = ["رمادي", "أسود", "أبيض", "وردي", "بنفسجي", "أزرق", "أخضر", "برتقالي", "بني"]
    theme_colors_map = {
        "رمادي": "#95A5A6",
        "أسود": "#34495E",
        "أبيض": "#ECF0F1",
        "وردي": "#FFC0CB",
        "بنفسجي": "#9B59B6",
        "أزرق": "#3498DB",
        "أخضر": "#2ECC71",
        "برتقالي": "#E67E22",
        "بني": "#8B4513"
    }
    
    for row_start in range(0, 9, 3):
        row_contents = []
        for i in range(row_start, min(row_start + 3, 9)):
            if i < len(theme_names):
                theme_name = theme_names[i]
                theme_color = theme_colors_map.get(theme_name, "#95A5A6")
                
                row_contents.append({
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                }
                            ],
                            "backgroundColor": theme_color,
                            "cornerRadius": "15px",
                            "height": "60px"
                        },
                        {
                            "type": "text",
                            "text": theme_name,
                            "size": "xs",
                            "color": colors["text2"],
                            "align": "center",
                            "margin": "sm"
                        }
                    ],
                    "action": {
                        "type": "message",
                        "text": theme_name
                    },
                    "flex": 1
                })
        
        if row_contents:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": row_contents,
                "spacing": "sm",
                "margin": "md"
            })
    
    # ==================== MAIN BUTTONS - الأزرار الرئيسية ====================
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            # زر انضم
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "انضم  ✅",
                    "text": "انضم"
                },
                "style": "primary",
                "color": colors["success"],
                "height": "sm"
            },
            # زر انسحب
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "انسحب  ❌",
                    "text": "انسحب"
                },
                "style": "secondary",
                "height": "sm",
                "margin": "sm"
            }
        ],
        "margin": "xl"
    })
    
    # ==================== BOTTOM BUTTONS - أزرار سفلية ====================
    contents.append({
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "الألعاب  🎮",
                    "text": "ألعاب"
                },
                "style": "link",
                "color": colors["primary"],
                "height": "sm",
                "flex": 1
            },
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "نقاطي  ⭐",
                    "text": "نقاطي"
                },
                "style": "link",
                "color": colors["primary"],
                "height": "sm",
                "flex": 1
            }
        ],
        "spacing": "sm",
        "margin": "md"
    })
    
    contents.append({
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "الصدارة  🏆",
                    "text": "صدارة"
                },
                "style": "link",
                "color": colors["primary"],
                "height": "sm",
                "flex": 1
            },
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "فريقين",
                    "text": "فريقين"
                },
                "style": "link",
                "color": colors["secondary"],
                "height": "sm",
                "flex": 1
            }
        ],
        "spacing": "sm",
        "margin": "sm"
    })
    
    # ==================== COPYRIGHT ====================
    contents.append({
        "type": "text",
        "text": BOT_RIGHTS,
        "size": "xxs",
        "color": colors["text3"],
        "align": "center",
        "wrap": True,
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
        FlexMessage(
            alt_text="🏠 Bot Mesh",
            contents=FlexContainer.from_dict(bubble)
        )
    )

# ============================================================================
# GAMES MENU - قائمة الألعاب (الصورة 3)
# ============================================================================

def build_games_menu(theme: str = "رمادي") -> FlexMessage:
    """
    🎮 قائمة الألعاب - شبكة 3 أعمدة
    كما في الصورة 3 بالضبط
    """
    colors = get_theme(theme)
    
    contents = []
    
    # ==================== HEADER ====================
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "image",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
                "size": "md",
                "aspectRatio": "1:1",
                "aspectMode": "cover"
            },
            {
                "type": "text",
                "text": "🎮 الألعاب المتاحة",
                "size": "lg",
                "weight": "bold",
                "color": colors["text"],
                "align": "center",
                "margin": "md"
            }
        ]
    })
    
    contents.append({
        "type": "text",
        "text": f"عدد الألعاب: {len(GAME_LIST)}",
        "size": "sm",
        "color": colors["text2"],
        "align": "center",
        "margin": "sm"
    })
    
    contents.append({
        "type": "separator",
        "margin": "lg",
        "color": colors["border"]
    })
    
    # ==================== GAMES GRID - 3 أعمدة ====================
    # تقسيم الألعاب إلى صفوف (كل صف 3 ألعاب)
    for row_start in range(0, len(GAME_LIST), 3):
        row_contents = []
        
        for i in range(row_start, min(row_start + 3, len(GAME_LIST))):
            _, display_name, icon = GAME_LIST[i]
            
            row_contents.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # الأيقونة في دائرة
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": icon,
                                "size": "xxl",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": colors["button"],
                        "cornerRadius": "20px",
                        "paddingAll": "15px",
                        "height": "70px",
                        "justifyContent": "center"
                    },
                    # اسم اللعبة
                    {
                        "type": "text",
                        "text": display_name,
                        "size": "xs",
                        "color": colors["text"],
                        "align": "center",
                        "wrap": True,
                        "margin": "sm",
                        "weight": "bold"
                    }
                ],
                "action": {
                    "type": "message",
                    "text": display_name
                },
                "flex": 1
            })
        
        # إضافة الصف
        if row_contents:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": row_contents,
                "spacing": "sm",
                "margin": "md"
            })
    
    # ==================== BOTTOM BUTTONS ====================
    contents.append({
        "type": "separator",
        "margin": "xl",
        "color": colors["border"]
    })
    
    contents.append({
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "⛔ إيقاف",
                    "text": "إيقاف"
                },
                "style": "link",
                "color": colors["error"],
                "height": "sm",
                "flex": 1
            },
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "🏠 البداية",
                    "text": "بداية"
                },
                "style": "link",
                "color": colors["primary"],
                "height": "sm",
                "flex": 1
            }
        ],
        "spacing": "sm",
        "margin": "lg"
    })
    
    # ==================== COPYRIGHT ====================
    contents.append({
        "type": "text",
        "text": BOT_RIGHTS,
        "size": "xxs",
        "color": colors["text3"],
        "align": "center",
        "wrap": True,
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
        FlexMessage(
            alt_text="🎮 الألعاب",
            contents=FlexContainer.from_dict(bubble)
        )
    )

# ============================================================================
# MY POINTS - نقاطي (الصورة 4 أعلى)
# ============================================================================

def build_my_points(username: str, total_points: int, stats: Dict, theme: str = "رمادي") -> FlexMessage:
    """
    ⭐ لوحة النقاط - كما في الصورة 4 أعلى
    """
    colors = get_theme(theme)
    
    contents = []
    
    # ==================== HEADER ====================
    contents.append({
        "type": "text",
        "text": "🏆 لوحة الصدارة",
        "size": "lg",
        "weight": "bold",
        "color": colors["text"],
        "align": "center"
    })
    
    contents.append({
        "type": "separator",
        "margin": "lg",
        "color": colors["border"]
    })
    
    # ==================== USER INFO BOX ====================
    contents.append({
        "type": "box",
        "layout": "horizontal",
        "contents": [
            # الأيقونة
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "👤",
                        "size": "xxl"
                    }
                ],
                "flex": 0,
                "paddingAll": "10px",
                "backgroundColor": colors["button"],
                "cornerRadius": "15px"
            },
            # المعلومات
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "النقاط الكلية",
                        "size": "xs",
                        "color": colors["text3"]
                    },
                    {
                        "type": "text",
                        "text": str(total_points),
                        "size": "xxl",
                        "weight": "bold",
                        "color": colors["text"]
                    }
                ],
                "margin": "md"
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "15px",
        "paddingAll": "15px",
        "margin": "lg"
    })
    
    # ==================== LEVEL ====================
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "المستوى الحالي",
                "size": "xs",
                "color": colors["text3"],
                "align": "center"
            },
            {
                "type": "text",
                "text": "🔥 متقدم",
                "size": "lg",
                "weight": "bold",
                "color": colors["warning"],
                "align": "center",
                "margin": "sm"
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "15px",
        "paddingAll": "15px",
        "margin": "md"
    })
    
    # ==================== WARNING ====================
    contents.append({
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": "⚠️",
                "size": "sm",
                "flex": 0
            },
            {
                "type": "text",
                "text": "سيتم حذف بياناتك بعد 7 أيام من عدم النشاط",
                "size": "xs",
                "color": colors["warning"],
                "wrap": True,
                "margin": "sm"
            }
        ],
        "backgroundColor": "#FFF3CD",
        "cornerRadius": "12px",
        "paddingAll": "12px",
        "margin": "lg"
    })
    
    # ==================== BOTTOM BUTTONS ====================
    contents.append({
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "🏠 البداية",
                    "text": "بداية"
                },
                "style": "link",
                "color": colors["primary"],
                "height": "sm",
                "flex": 1
            },
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "الألعاب  🎮",
                    "text": "ألعاب"
                },
                "style": "link",
                "color": colors["primary"],
                "height": "sm",
                "flex": 1
            }
        ],
        "spacing": "sm",
        "margin": "xl"
    })
    
    # ==================== COPYRIGHT ====================
    contents.append({
        "type": "text",
        "text": BOT_RIGHTS,
        "size": "xxs",
        "color": colors["text3"],
        "align": "center",
        "wrap": True,
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
        FlexMessage(
            alt_text="⭐ نقاطي",
            contents=FlexContainer.from_dict(bubble)
        )
    )

# ============================================================================
# LEADERBOARD - لوحة الصدارة (الصورة 4 أسفل)
# ============================================================================

def build_leaderboard(top_users: List[Tuple[str, int]], theme: str = "رمادي") -> FlexMessage:
    """
    🏆 لوحة الصدارة - تصميم بسيط وواضح
    """
    colors = get_theme(theme)
    
    contents = []
    
    # ==================== HEADER ====================
    contents.append({
        "type": "text",
        "text": "⭐ نقاطي",
        "size": "lg",
        "weight": "bold",
        "color": colors["text"],
        "align": "center"
    })
    
    contents.append({
        "type": "separator",
        "margin": "lg",
        "color": colors["border"]
    })
    
    # ==================== USER ICON ====================
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "👤",
                "size": "xxl",
                "align": "center"
            }
        ],
        "margin": "lg"
    })
    
    # ==================== TOP USERS ====================
    medals = ["🥇", "🥈", "🥉"]
    
    if not top_users:
        contents.append({
            "type": "text",
            "text": "لا يوجد متصدرين بعد",
            "size": "sm",
            "color": colors["text3"],
            "align": "center",
            "margin": "lg"
        })
    else:
        for i, (name, pts) in enumerate(top_users[:3]):
            medal = medals[i] if i < 3 else f"{i+1}."
            
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": medal,
                        "size": "lg",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": name,
                        "size": "sm",
                        "color": colors["text"],
                        "margin": "md",
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": str(pts),
                        "size": "sm",
                        "color": colors["primary"],
                        "weight": "bold",
                        "align": "end",
                        "flex": 1
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "margin": "sm"
            })
    
    # ==================== BUTTONS ====================
    contents.append({
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "🏠 البداية",
                    "text": "بداية"
                },
                "style": "link",
                "color": colors["primary"],
                "height": "sm",
                "flex": 1
            },
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "الألعاب  🎮",
                    "text": "ألعاب"
                },
                "style": "link",
                "color": colors["primary"],
                "height": "sm",
                "flex": 1
            }
        ],
        "spacing": "sm",
        "margin": "xl"
    })
    
    contents.append({
        "type": "text",
        "text": BOT_RIGHTS,
        "size": "xxs",
        "color": colors["text3"],
        "align": "center",
        "wrap": True,
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
        FlexMessage(
            alt_text="🏆 الصدارة",
            contents=FlexContainer.from_dict(bubble)
        )
    )

# ============================================================================
# GAME SCREEN - شاشة اللعبة (الصورة 5 و 6)
# ============================================================================

def build_game_window(
    game_name: str,
    game_icon: str,
    question_number: int,
    total_questions: int,
    ques
