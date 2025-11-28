"""
Bot Mesh - UI Builder v10.0 GLASS MORPHISM PRO
Created by: Abeer Aldosari © 2025
✨ تصميم زجاجي ثلاثي الأبعاد احترافي
🎨 نظام بطاقات ذكي مع أيقونات
🚀 تجربة مستخدم سلسة ومتكاملة
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from constants import BOT_RIGHTS, THEMES, DEFAULT_THEME, GAME_LIST

# ============================================================================
# ADVANCED GLASS COMPONENTS
# ============================================================================

def create_glass_header(colors, title, subtitle=None, icon=None):
    """رأس زجاجي مع أيقونة اختيارية"""
    header_content = []
    
    if icon:
        header_content.append({
            "type": "text",
            "text": icon,
            "size": "xxl",
            "align": "center"
        })
    
    header_content.append({
        "type": "text",
        "text": title,
        "size": "xxl",
        "weight": "bold",
        "color": colors["primary"],
        "align": "center",
        "margin": "xs" if icon else "none"
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

def create_glass_card(colors, icon, title, description, highlight=False):
    """بطاقة زجاجية ثلاثية الأبعاد مع أيقونة"""
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            # أيقونة
            {
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": icon,
                    "size": "xl",
                    "align": "center",
                    "gravity": "center"
                }],
                "backgroundColor": colors["primary"] if highlight else colors["card"],
                "cornerRadius": "15px",
                "width": "50px",
                "height": "50px",
                "justifyContent": "center",
                "alignItems": "center"
            },
            # محتوى
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
        "backgroundColor": colors["glass"],
        "cornerRadius": "20px",
        "paddingAll": "15px",
        "margin": "sm",
        "borderWidth": "2px" if highlight else "1px",
        "borderColor": colors["primary"] if highlight else colors["border"],
        "spacing": "md"
    }

def create_info_card(colors, title, points, highlight=False):
    """بطاقة معلومات مع عنوان وقيمة"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": title,
                "size": "xs",
                "color": colors["text2"],
                "align": "center"
            },
            {
                "type": "text",
                "text": str(points),
                "size": "xxl",
                "weight": "bold",
                "color": colors["primary"] if highlight else colors["text"],
                "align": "center",
                "margin": "xs"
            }
        ],
        "backgroundColor": colors["glass"],
        "cornerRadius": "20px",
        "paddingAll": "15px",
        "flex": 1,
        "borderWidth": "2px" if highlight else "1px",
        "borderColor": colors["primary"] if highlight else colors["border"]
    }

def create_section_title(colors, title, icon=None):
    """عنوان قسم مع خط فاصل"""
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
                "color": colors["primary"],
                "margin": "sm"
            }
        ],
        "margin": "xl"
    }

def create_glass_button(label, text, color, icon=None, style="primary"):
    """زر زجاجي مع أيقونة اختيارية"""
    button_text = f"{icon} {label}" if icon else label
    return {
        "type": "button",
        "action": {
            "type": "message",
            "label": button_text,
            "text": text
        },
        "style": style,
        "height": "sm",
        "color": color
    }

def create_button_grid(buttons, columns=2):
    """شبكة أزرار ذكية"""
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

def create_feature_list(colors, features):
    """قائمة ميزات بتصميم أنيق"""
    feature_items = []
    for feature in features:
        feature_items.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": "✓",
                    "size": "sm",
                    "color": colors["success"],
                    "flex": 0,
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": feature,
                    "size": "xs",
                    "color": colors["text2"],
                    "wrap": True,
                    "flex": 1,
                    "margin": "sm"
                }
            ],
            "spacing": "sm",
            "margin": "xs"
        })
    
    return {
        "type": "box",
        "layout": "vertical",
        "contents": feature_items,
        "backgroundColor": colors["glass"],
        "cornerRadius": "15px",
        "paddingAll": "15px",
        "margin": "sm",
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }

# ============================================================================
# نافذة البداية - HOME (تصميم احترافي متكامل)
# ============================================================================

def build_enhanced_home(username, points, is_registered, theme="أبيض"):
    """نافذة البداية بتصميم Glass Morphism Pro"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    status_icon = "✅" if is_registered else "⚠️"
    status_text = "مسجل" if is_registered else "غير مسجل"
    status_color = colors["success"] if is_registered else colors["error"]
    
    # HEADER
    header = create_glass_header(
        colors,
        "Bot Mesh",
        "منصة الألعاب الذكية الشاملة",
        "🎮"
    )
    
    # BODY
    body = [
        # بطاقة الملف الشخصي
        {
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
                        create_info_card(colors, "الحالة", f"{status_icon}\n{status_text}"),
                        create_info_card(colors, "النقاط", f"⭐\n{points}", highlight=True)
                    ],
                    "spacing": "sm",
                    "margin": "md"
                }
            ],
            "backgroundColor": colors["glass"],
            "cornerRadius": "25px",
            "paddingAll": "20px",
            "borderWidth": "2px",
            "borderColor": colors["primary"]
        },
        
        # الأقسام الرئيسية
        create_section_title(colors, "الأقسام الرئيسية", "📂"),
        
        create_glass_card(
            colors, "🎯", "الألعاب",
            "اختر من 12+ لعبة ذكية ومسلية"
        ),
        
        create_glass_card(
            colors, "📊", "إحصائياتي",
            "تتبع نقاطك وتقدمك"
        ),
        
        create_glass_card(
            colors, "🏆", "لوحة الصدارة",
            "تنافس مع اللاعبين الآخرين"
        ),
        
        create_glass_card(
            colors, "🎨", "الثيمات",
            "غيّر مظهر البوت (9 ثيمات)"
        ),
        
        # طرق اللعب
        create_section_title(colors, "طرق اللعب", "🎮"),
        
        create_glass_card(
            colors, "👤", "وضع فردي",
            "العب بمفردك • 5 أسئلة • نقطة لكل إجابة صحيحة",
            highlight=True
        ),
        
        create_glass_card(
            colors, "👥", "وضع مجموعة",
            "أضف البوت للمجموعة • تنافس مع الأصدقاء • فرق تلقائية"
        ),
        
        # أزرار سريعة
        create_section_title(colors, "أدوات سريعة", "⚡"),
    ]
    
    # شبكة الأزرار
    buttons = [
        create_glass_button("🎯 الألعاب", "ألعاب", colors["primary"]),
        create_glass_button("📊 نقاطي", "نقاطي", colors["secondary"], style="secondary"),
        create_glass_button("🏆 الصدارة", "صدارة", colors["secondary"], style="secondary"),
        create_glass_button("🎨 الثيمات", "ثيمات", colors["secondary"], style="secondary"),
        create_glass_button("✅ انضم", "انضم", colors["success"]),
        create_glass_button("❓ المساعدة", "مساعدة", colors["primary"])
    ]
    
    body.extend(create_button_grid(buttons, columns=2))
    
    # FOOTER
    footer = [
        {
            "type": "separator",
            "color": colors["border"]
        },
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center",
            "wrap": True,
            "margin": "md"
        }
    ]
    
    bubble = {
        "type": "bubble",
        "size": "giga",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + [{"type": "separator", "color": colors["border"], "margin": "lg"}] + body,
            "paddingAll": "24px",
            "spacing": "none",
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
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(alt_text="🏠 البداية", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# نافذة المساعدة الشاملة - HELP (تصميم متكامل)
# ============================================================================

def build_help_window(theme="أبيض"):
    """نافذة المساعدة بتصميم Glass Morphism Pro"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # HEADER
    header = create_glass_header(
        colors,
        "دليل الاستخدام",
        "كل ما تحتاج معرفته عن Bot Mesh",
        "📚"
    )
    
    # BODY
    body = [
        # البدء السريع
        create_section_title(colors, "البدء السريع", "🚀"),
        
        create_feature_list(colors, [
            "اضغط 'انضم' للتسجيل في النظام",
            "اختر 'الألعاب' من القائمة الرئيسية",
            "اختر اللعبة المفضلة لديك",
            "أجب على الأسئلة واكسب النقاط"
        ]),
        
        # اللعب الفردي
        create_section_title(colors, "اللعب الفردي", "👤"),
        
        create_glass_card(
            colors, "🎯", "كيف تلعب؟",
            "افتح المحادثة الخاصة • اختر لعبة • أجب على 5 أسئلة • اكسب نقطة لكل إجابة صحيحة"
        ),
        
        # اللعب الجماعي
        create_section_title(colors, "اللعب في مجموعة", "👥"),
        
        create_glass_card(
            colors, "➕", "إضافة البوت",
            "إعدادات المجموعة → دعوة → ابحث عن Bot Mesh → أضف"
        ),
        
        create_glass_card(
            colors, "🎮", "بدء اللعبة",
            "اكتب '@' لمنشن البوت • اختر اللعبة • أول إجابة صحيحة تفوز"
        ),
        
        create_glass_card(
            colors, "👥", "تقسيم تلقائي",
            "اكتب 'انضم' → البوت يقسم اللاعبين لفريقين → تنافس جماعي"
        ),
        
        # الأوامر المتاحة
        create_section_title(colors, "الأوامر المتاحة", "⌨️"),
        
        create_glass_card(
            colors, "💡", "لمح",
            "احصل على تلميح للسؤال الحالي (حرف أول + عدد)"
        ),
        
        create_glass_card(
            colors, "🔍", "جاوب",
            "اكشف الإجابة الصحيحة وانتقل للسؤال التالي"
        ),
        
        create_glass_card(
            colors, "⛔", "إيقاف",
            "أنهِ اللعبة الحالية وأوقف الجلسة"
        ),
        
        # نصائح للفوز
        create_section_title(colors, "نصائح للفوز", "🏆"),
        
        create_feature_list(colors, [
            "اقرأ السؤال بتركيز قبل الإجابة",
            "استخدم 'لمح' عندما تحتاج مساعدة",
            "السرعة مهمة في المجموعات",
            "تدرب على جميع الألعاب للتحسين",
            "تابع تقدمك في 'نقاطي'"
        ]),
        
        # أزرار التنقل
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "separator",
                    "color": colors["border"],
                    "margin": "xl"
                }
            ] + create_button_grid([
                create_glass_button("🎯 الألعاب", "ألعاب", colors["primary"]),
                create_glass_button("🏠 الرئيسية", "home", colors["secondary"], style="secondary")
            ], columns=2)
        }
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
    
    bubble = {
        "type": "bubble",
        "size": "giga",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + [{"type": "separator", "color": colors["border"], "margin": "lg"}] + body,
            "paddingAll": "24px",
            "spacing": "none",
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
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(alt_text="📚 المساعدة", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# نافذة مساعدة المجموعة (متعددة اللاعبين)
# ============================================================================

def build_multiplayer_help_window(theme="أبيض"):
    """نافذة مساعدة خاصة باللعب الجماعي"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    header = create_glass_header(
        colors,
        "دليل اللعب الجماعي",
        "تعلم كيف تلعب مع أصدقائك",
        "👥"
    )
    
    body = [
        create_section_title(colors, "إضافة البوت", "➕"),
        
        create_feature_list(colors, [
            "افتح إعدادات المجموعة",
            "اضغط على 'دعوة'",
            "ابحث عن 'Bot Mesh'",
            "أضف البوت للمجموعة"
        ]),
        
        create_section_title(colors, "بدء اللعبة", "🎮"),
        
        create_glass_card(
            colors, "@", "منشن البوت",
            "اكتب '@' لاستدعاء البوت في المجموعة"
        ),
        
        create_glass_card(
            colors, "🎯", "اختر اللعبة",
            "اختر من قائمة الألعاب المتاحة"
        ),
        
        create_glass_card(
            colors, "⚡", "أجب أولاً",
            "أول لاعب يجيب بشكل صحيح يفوز بالنقطة"
        ),
        
        create_section_title(colors, "تقسيم الفرق", "⚔️"),
        
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "التقسيم التلقائي",
                    "size": "md",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "فريق 1", "size": "sm", "weight": "bold", "color": colors["text"], "align": "center"},
                                {"type": "text", "text": "اللاعبون\nالفرديون", "size": "xs", "color": colors["text2"], "align": "center", "wrap": True, "margin": "xs"},
                                {"type": "text", "text": "1, 3, 5...", "size": "xs", "color": colors["primary"], "align": "center", "margin": "xs"}
                            ],
                            "backgroundColor": colors["card"],
                            "cornerRadius": "15px",
                            "paddingAll": "10px",
                            "flex": 1
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "فريق 2", "size": "sm", "weight": "bold", "color": colors["text"], "align": "center"},
                                {"type": "text", "text": "اللاعبون\nالزوجيون", "size": "xs", "color": colors["text2"], "align": "center", "wrap": True, "margin": "xs"},
                                {"type": "text", "text": "2, 4, 6...", "size": "xs", "color": colors["secondary"], "align": "center", "margin": "xs"}
                            ],
                            "backgroundColor": colors["card"],
                            "cornerRadius": "15px",
                            "paddingAll": "10px",
                            "flex": 1
                        }
                    ],
                    "spacing": "sm",
                    "margin": "md"
                }
            ],
            "backgroundColor": colors["glass"],
            "cornerRadius": "20px",
            "paddingAll": "15px",
            "borderWidth": "2px",
            "borderColor": colors["primary"],
            "margin": "sm"
        },
        
        create_feature_list(colors, [
            "اكتب 'انضم' للانضمام للعبة",
            "البوت يقسم اللاعبين تلقائياً",
            "كل إجابة صحيحة = نقطة للفريق",
            "الفريق صاحب النقاط الأكثر يفوز"
        ]),
        
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "separator", "color": colors["border"], "margin": "xl"}
            ] + create_button_grid([
                create_glass_button("🎮 جرب الآن", "ألعاب", colors["primary"]),
                create_glass_button("🏠 الرئيسية", "home", colors["secondary"], style="secondary")
            ], columns=2)
        }
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
    
    bubble = {
        "type": "bubble",
        "size": "giga",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + [{"type": "separator", "color": colors["border"], "margin": "lg"}] + body,
            "paddingAll": "24px",
            "spacing": "none",
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
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(alt_text="👥 مساعدة المجموعة", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# النوافذ الأخرى (يتم استيرادها من الملف الأصلي)
# ============================================================================

# يتم الاحتفاظ بجميع الدوال الأخرى كما هي:
# - build_games_menu()
# - build_my_points()
# - build_leaderboard()
# - build_registration_required()
# - build_winner_announcement()
# - build_theme_selector()
# - build_percentage_result()

# (ضع باقي الدوال من الملف الأصلي هنا)
