"""
Bot Mesh - UI Builder v9.0 PROFESSIONAL GLASS DESIGN
Created by: Abeer Aldosari © 2025
✅ تصميم زجاجي ثلاثي الأبعاد احترافي
✅ نوافذ شاملة ومتكاملة (مساعدة + بداية)
✅ دعم الفردي والمجموعة مع تقسيم فريقين
✅ 9 ثيمات قابلة للتبديل
✅ أزرار ذكية وسهلة الاستخدام
✅ بدون كاروسيل - Flex + Buttons فقط
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from constants import BOT_RIGHTS, THEMES, DEFAULT_THEME, GAME_LIST

# ============================================================================
# CORE GLASS COMPONENTS
# ============================================================================

def create_glass_card(colors, content, highlight=False):
    """إنشاء كارت زجاجي ثلاثي الأبعاد"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": content,
        "backgroundColor": colors["glass"],
        "cornerRadius": "20px",
        "paddingAll": "20px",
        "margin": "md",
        "borderWidth": "2px" if highlight else "1px",
        "borderColor": colors["primary"] if highlight else colors["border"]
    }

def create_separator(color="#E5E7EB"):
    """فاصل أنيق"""
    return {
        "type": "separator",
        "color": color,
        "margin": "lg"
    }

def create_button(label, text, color, style="primary"):
    """زر أنيق"""
    return {
        "type": "button",
        "action": {
            "type": "message",
            "label": label,
            "text": text
        },
        "style": style,
        "height": "sm",
        "color": color,
        "margin": "sm"
    }

def create_button_row(buttons):
    """صف من الأزرار"""
    return {
        "type": "box",
        "layout": "horizontal",
        "spacing": "sm",
        "contents": buttons,
        "margin": "sm"
    }

def create_glass_bubble(colors, header_content, body_content, footer_content=None):
    """إنشاء bubble زجاجية احترافية"""
    bubble = {
        "type": "bubble",
        "size": "giga",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header_content + [create_separator(colors["border"])] + body_content,
            "paddingAll": "24px",
            "spacing": "md",
            "backgroundColor": colors["bg"]
        }
    }
    
    if footer_content:
        bubble["footer"] = {
            "type": "box",
            "layout": "vertical",
            "contents": footer_content,
            "paddingAll": "20px",
            "spacing": "sm",
            "backgroundColor": colors["bg"]
        }
    
    bubble["styles"] = {
        "body": {"backgroundColor": colors["bg"]},
        "footer": {"backgroundColor": colors["bg"]}
    }
    
    return bubble

# ============================================================================
# نافذة البداية - HOME (شاملة كل شيء)
# ============================================================================

def build_enhanced_home(username, points, is_registered, theme="أبيض"):
    """نافذة البداية الرئيسية الشاملة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    status = "مسجل" if is_registered else "غير مسجل"
    status_color = colors["success"] if is_registered else colors["error"]
    
    # HEADER
    header = [
        {
            "type": "text",
            "text": "Bot Mesh",
            "size": "xxl",
            "weight": "bold",
            "color": colors["primary"],
            "align": "center"
        },
        {
            "type": "text",
            "text": "منصة الألعاب الذكية الشاملة",
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "margin": "xs"
        }
    ]
    
    # BODY
    body = [
        # بطاقة الملف الشخصي
        create_glass_card(colors, [
            {
                "type": "text",
                "text": username,
                "size": "xl",
                "weight": "bold",
                "color": colors["text"],
                "align": "center"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": status,
                        "size": "sm",
                        "color": status_color,
                        "flex": 1,
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "•",
                        "size": "sm",
                        "color": colors["text2"],
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": f"{points} نقطة",
                        "size": "sm",
                        "color": colors["primary"],
                        "weight": "bold",
                        "flex": 1,
                        "align": "center"
                    }
                ],
                "spacing": "sm",
                "margin": "sm"
            }
        ], highlight=True),
        
        # أقسام رئيسية
        {
            "type": "text",
            "text": "الأقسام الرئيسية",
            "size": "md",
            "color": colors["text"],
            "weight": "bold",
            "margin": "xl"
        },
        
        # صف الألعاب والإحصائيات
        create_button_row([
            {
                "type": "button",
                "action": {"type": "message", "label": "الألعاب", "text": "ألعاب"},
                "style": "primary",
                "height": "sm",
                "color": colors["primary"],
                "flex": 1
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"},
                "style": "secondary",
                "height": "sm",
                "color": colors["secondary"],
                "flex": 1
            }
        ]),
        
        # صف الصدارة والثيمات
        create_button_row([
            {
                "type": "button",
                "action": {"type": "message", "label": "الصدارة", "text": "صدارة"},
                "style": "secondary",
                "height": "sm",
                "color": colors["secondary"],
                "flex": 1
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "الثيمات", "text": "ثيمات"},
                "style": "secondary",
                "height": "sm",
                "color": colors["secondary"],
                "flex": 1
            }
        ]),
        
        create_separator(colors["border"]),
        
        # طرق اللعب
        {
            "type": "text",
            "text": "طرق اللعب",
            "size": "md",
            "color": colors["text"],
            "weight": "bold",
            "margin": "lg"
        },
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "فردي",
                "size": "sm",
                "weight": "bold",
                "color": colors["text"]
            },
            {
                "type": "text",
                "text": "العب بمفردك وتنافس مع نفسك",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True,
                "margin": "xs"
            }
        ]),
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "مجموعة",
                "size": "sm",
                "weight": "bold",
                "color": colors["text"]
            },
            {
                "type": "text",
                "text": "أضف البوت للمجموعة واستمتع مع أصدقائك",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True,
                "margin": "xs"
            }
        ]),
        
        create_separator(colors["border"]),
        
        # التسجيل والمساعدة
        {
            "type": "text",
            "text": "الحساب والدعم",
            "size": "md",
            "color": colors["text"],
            "weight": "bold",
            "margin": "lg"
        },
        
        create_button_row([
            {
                "type": "button",
                "action": {"type": "message", "label": "انضم", "text": "انضم"},
                "style": "primary",
                "height": "sm",
                "color": colors["success"],
                "flex": 1
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "انسحب", "text": "انسحب"},
                "style": "secondary",
                "height": "sm",
                "color": colors["error"],
                "flex": 1
            }
        ]),
        
        create_button(
            "المساعدة الشاملة",
            "مساعدة",
            colors["primary"]
        )
    ]
    
    # FOOTER
    footer = [
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center",
            "wrap": True
        }
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="البداية", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# نافذة المساعدة الشاملة - HELP (كل شيء)
# ============================================================================

def build_help_window(theme="أبيض"):
    """نافذة المساعدة الشاملة والمتكاملة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # HEADER
    header = [
        {
            "type": "text",
            "text": "دليل الاستخدام الشامل",
            "size": "xxl",
            "weight": "bold",
            "color": colors["primary"],
            "align": "center"
        },
        {
            "type": "text",
            "text": "كل ما تحتاج معرفته",
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "margin": "xs"
        }
    ]
    
    # BODY
    body = [
        # البدء السريع
        {
            "type": "text",
            "text": "البدء السريع",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "md"
        },
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "1. اضغط 'انضم' للتسجيل",
                "size": "sm",
                "color": colors["text"],
                "wrap": True
            },
            {
                "type": "text",
                "text": "2. اختر 'الألعاب' من القائمة",
                "size": "sm",
                "color": colors["text"],
                "wrap": True,
                "margin": "xs"
            },
            {
                "type": "text",
                "text": "3. اختر اللعبة المفضلة",
                "size": "sm",
                "color": colors["text"],
                "wrap": True,
                "margin": "xs"
            },
            {
                "type": "text",
                "text": "4. أجب بسرعة واكسب النقاط",
                "size": "sm",
                "color": colors["text"],
                "wrap": True,
                "margin": "xs"
            }
        ]),
        
        create_separator(colors["border"]),
        
        # اللعب الفردي
        {
            "type": "text",
            "text": "اللعب الفردي",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "lg"
        },
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "العب بمفردك",
                "size": "sm",
                "weight": "bold",
                "color": colors["primary"]
            },
            {
                "type": "text",
                "text": "• افتح المحادثة الخاصة مع البوت\n• اختر اللعبة\n• أجب على 5 أسئلة\n• اكسب نقطة لكل إجابة صحيحة",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True,
                "margin": "sm"
            }
        ]),
        
        create_separator(colors["border"]),
        
        # اللعب الجماعي
        {
            "type": "text",
            "text": "اللعب في مجموعة",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "lg"
        },
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "استمتع مع أصدقائك",
                "size": "sm",
                "weight": "bold",
                "color": colors["primary"]
            },
            {
                "type": "text",
                "text": "• أضف البوت للمجموعة\n• اكتب '@' لمنشن البوت\n• اختر اللعبة\n• أول إجابة صحيحة تفوز\n• تنافسوا في الصدارة",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True,
                "margin": "sm"
            }
        ]),
        
        create_separator(colors["border"]),
        
        # تقسيم الفرق
        {
            "type": "text",
            "text": "تقسيم الفرق",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "lg"
        },
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "العب فريق ضد فريق",
                "size": "sm",
                "weight": "bold",
                "color": colors["primary"]
            },
            {
                "type": "text",
                "text": "• اكتب 'انضم' للانضمام للعبة\n• البوت يقسم اللاعبين تلقائياً\n• فريق 1 vs فريق 2\n• كل إجابة صحيحة = نقطة للفريق",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True,
                "margin": "sm"
            }
        ]),
        
        create_separator(colors["border"]),
        
        # الأوامر المتاحة
        {
            "type": "text",
            "text": "الأوامر المتاحة",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "lg"
        },
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "لمح",
                "size": "sm",
                "weight": "bold",
                "color": colors["primary"]
            },
            {
                "type": "text",
                "text": "احصل على تلميح للسؤال الحالي",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True,
                "margin": "xs"
            }
        ]),
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "جاوب",
                "size": "sm",
                "weight": "bold",
                "color": colors["primary"]
            },
            {
                "type": "text",
                "text": "اكشف الإجابة الصحيحة وانتقل للسؤال التالي",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True,
                "margin": "xs"
            }
        ]),
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "إيقاف",
                "size": "sm",
                "weight": "bold",
                "color": colors["error"]
            },
            {
                "type": "text",
                "text": "أنهِ اللعبة الحالية",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True,
                "margin": "xs"
            }
        ]),
        
        create_separator(colors["border"]),
        
        # نصائح وحيل
        {
            "type": "text",
            "text": "نصائح للفوز",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "lg"
        },
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "• اقرأ السؤال بتركيز\n• استخدم 'لمح' عند الحاجة\n• السرعة مهمة في المجموعات\n• تدرب على جميع الألعاب\n• تابع نقاطك في 'نقاطي'",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True
            }
        ]),
        
        create_separator(colors["border"]),
        
        # أزرار العودة
        create_button_row([
            {
                "type": "button",
                "action": {"type": "message", "label": "الألعاب", "text": "ألعاب"},
                "style": "primary",
                "height": "sm",
                "color": colors["primary"],
                "flex": 1
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "الرئيسية", "text": "home"},
                "style": "secondary",
                "height": "sm",
                "color": colors["secondary"],
                "flex": 1
            }
        ])
    ]
    
    # FOOTER
    footer = [
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center",
            "wrap": True
        }
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="المساعدة", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# نافذة مساعدة مجموعة متعددة اللاعبين
# ============================================================================

def build_multiplayer_help_window(theme="أبيض"):
    """نافذة مساعدة خاصة باللعب الجماعي"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    header = [
        {
            "type": "text",
            "text": "دليل اللعب الجماعي",
            "size": "xxl",
            "weight": "bold",
            "color": colors["primary"],
            "align": "center"
        },
        {
            "type": "text",
            "text": "تعلم كيف تلعب في المجموعة",
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "margin": "xs"
        }
    ]
    
    body = [
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "إضافة البوت للمجموعة",
                "size": "md",
                "weight": "bold",
                "color": colors["primary"]
            },
            {
                "type": "text",
                "text": "1. افتح إعدادات المجموعة\n2. اضغط على 'دعوة'\n3. ابحث عن 'Bot Mesh'\n4. أضف البوت",
                "size": "sm",
                "color": colors["text2"],
                "wrap": True,
                "margin": "sm"
            }
        ]),
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "بدء اللعبة",
                "size": "md",
                "weight": "bold",
                "color": colors["primary"]
            },
            {
                "type": "text",
                "text": "• اكتب '@' لمنشن البوت\n• اختر اللعبة من القائمة\n• أول لاعب يجيب يفوز بالنقطة",
                "size": "sm",
                "color": colors["text2"],
                "wrap": True,
                "margin": "sm"
            }
        ]),
        
        create_separator(colors["border"]),
        
        {
            "type": "text",
            "text": "تقسيم الفرق (تلقائي)",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "lg"
        },
        
        create_glass_card(colors, [
            {
                "type": "text",
                "text": "كيف يعمل التقسيم؟",
                "size": "sm",
                "weight": "bold",
                "color": colors["primary"]
            },
            {
                "type": "text",
                "text": "• اكتب 'انضم' للانضمام\n• البوت يقسم تلقائياً:\n  - فريق 1: اللاعبون الفرديون (1، 3، 5...)\n  - فريق 2: اللاعبون الزوجيون (2، 4، 6...)\n• كل إجابة صحيحة = نقطة للفريق",
                "size": "xs",
                "color": colors["text2"],
                "wrap": True,
                "margin": "sm"
            }
        ]),
        
        create_separator(colors["border"]),
        
        create_button_row([
            {
                "type": "button",
                "action": {"type": "message", "label": "جرب الآن", "text": "ألعاب"},
                "style": "primary",
                "height": "sm",
                "color": colors["primary"],
                "flex": 1
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "الرئيسية", "text": "home"},
                "style": "secondary",
                "height": "sm",
                "color": colors["secondary"],
                "flex": 1
            }
        ])
    ]
    
    footer = [
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center",
            "wrap": True
        }
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="مساعدة المجموعة", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# قائمة الألعاب
# ============================================================================

def build_games_menu(theme="أبيض"):
    """قائمة الألعاب الشاملة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    games = ["أسرع", "ذكاء", "لعبة", "أغنية", "خمن", "سلسلة",
             "ترتيب", "تكوين", "ضد", "لون", "رياضيات", "
