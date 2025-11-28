"""
Bot Mesh - UI Builder v8.0 PROFESSIONAL
Created by: Abeer Aldosari © 2025
✅ تصميم زجاجي ثلاثي الأبعاد
✅ نافذتان رئيسيتان: مساعدة وبداية
✅ بدون كاروسيل - أزرار فقط
✅ بدون إيموجي إلا للضرورة
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from constants import BOT_RIGHTS, THEMES, DEFAULT_THEME, GAME_LIST

# ============================================================================
# Core Components
# ============================================================================

def create_glass_card(colors, content):
    """إنشاء كارت زجاجي ثلاثي الأبعاد"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": content,
        "backgroundColor": colors["glass"],
        "cornerRadius": "20px",
        "paddingAll": "20px",
        "margin": "md",
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }

def create_separator(color):
    """فاصل"""
    return {"type": "separator", "color": color, "margin": "lg"}

def create_button(label, text, color, style="primary"):
    """زر"""
    return {
        "type": "button",
        "action": {"type": "message", "label": label, "text": text},
        "style": style,
        "height": "sm",
        "color": color,
        "margin": "sm"
    }

def create_glass_bubble(colors, header_content, body_content, footer_content=None):
    """إنشاء bubble زجاجية"""
    bubble = {
        "type": "bubble",
        "size": "giga",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header_content + [create_separator(colors["border"])] + body_content,
            "paddingAll": "24px",
            "spacing": "md"
        }
    }
    
    if footer_content:
        bubble["footer"] = {
            "type": "box",
            "layout": "vertical",
            "contents": footer_content,
            "paddingAll": "20px",
            "spacing": "sm"
        }
    
    return bubble

# ============================================================================
# نافذة البداية - HOME
# ============================================================================

def build_home_window(username, points, is_registered, theme="أبيض"):
    """نافذة البداية الرئيسية"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    status = "مسجل" if is_registered else "غير مسجل"
    status_color = colors["success"] if is_registered else colors["error"]
    
    # HEADER
    header = [
        {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", 
         "color": colors["primary"], "align": "center"},
        {"type": "text", "text": "منصة الألعاب الذكية", "size": "sm", 
         "color": colors["text2"], "align": "center", "margin": "sm"}
    ]
    
    # BODY
    body = [
        create_glass_card(colors, [
            {"type": "text", "text": username, "size": "lg", "weight": "bold", 
             "color": colors["text"], "align": "center"},
            {"type": "text", "text": f"{status} • {points} نقطة", "size": "md", 
             "color": status_color, "align": "center", "margin": "sm"}
        ]),
        
        {"type": "text", "text": "القائمة الرئيسية", "size": "md", 
         "color": colors["text"], "weight": "bold", "margin": "xl"},
        
        create_button("الألعاب", "ألعاب", colors["primary"]),
        create_button("نقاطي", "نقاطي", colors["secondary"], "secondary"),
        create_button("الصدارة", "صدارة", colors["secondary"], "secondary"),
        create_button("الثيمات", "ثيمات", colors["secondary"], "secondary"),
        create_button("المساعدة", "مساعدة", colors["secondary"], "secondary"),
        
        create_separator(colors["border"]),
        
        {"type": "text", "text": "التسجيل", "size": "md", 
         "color": colors["text"], "weight": "bold", "margin": "lg"},
        
        {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
            {
                "type": "button",
                "action": {"type": "message", "label": "انضم", "text": "انضم"},
                "style": "primary", "height": "sm", "color": colors["success"], "flex": 1
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "انسحب", "text": "انسحب"},
                "style": "secondary", "height": "sm", "color": colors["error"], "flex": 1
            }
        ]}
    ]
    
    # FOOTER
    footer = [
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
         "color": colors["text2"], "align": "center"}
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="البداية", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# نافذة المساعدة - HELP
# ============================================================================

def build_help_window(theme="أبيض"):
    """نافذة المساعدة الرئيسية"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # HEADER
    header = [
        {"type": "text", "text": "المساعدة", "size": "xxl", "weight": "bold", 
         "color": colors["primary"], "align": "center"},
        {"type": "text", "text": "دليل استخدام البوت", "size": "sm", 
         "color": colors["text2"], "align": "center", "margin": "sm"}
    ]
    
    # BODY
    body = [
        create_glass_card(colors, [
            {"type": "text", "text": "كيفية اللعب", "size": "md", 
             "color": colors["text"], "weight": "bold"},
            {"type": "text", 
             "text": "• اضغط على 'الألعاب' لعرض القائمة\n• اختر اللعبة المفضلة\n• أجب على الأسئلة بسرعة\n• اكسب النقاط وتنافس", 
             "size": "sm", "color": colors["text2"], "wrap": True, "margin": "sm"}
        ]),
        
        create_glass_card(colors, [
            {"type": "text", "text": "الأوامر المتاحة", "size": "md", 
             "color": colors["text"], "weight": "bold"},
            {"type": "text", 
             "text": "• لمح: للحصول على تلميح\n• جاوب: لكشف الإجابة\n• إيقاف: لإنهاء اللعبة", 
             "size": "sm", "color": colors["text2"], "wrap": True, "margin": "sm"}
        ]),
        
        create_glass_card(colors, [
            {"type": "text", "text": "اللعب الجماعي", "size": "md", 
             "color": colors["text"], "weight": "bold"},
            {"type": "text", 
             "text": "• أضف البوت للمجموعة\n• منشن البوت @Bot\n• اختر اللعبة\n• أول إجابة صحيحة تفوز", 
             "size": "sm", "color": colors["text2"], "wrap": True, "margin": "sm"}
        ]),
        
        create_separator(colors["border"]),
        
        create_button("العودة للرئيسية", "home", colors["primary"])
    ]
    
    # FOOTER
    footer = [
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
         "color": colors["text2"], "align": "center"}
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="المساعدة", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# قائمة الألعاب
# ============================================================================

def build_games_menu(theme="أبيض"):
    """قائمة الألعاب"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    games = ["أسرع", "ذكاء", "لعبة", "أغنية", "خمن", "سلسلة",
             "ترتيب", "تكوين", "ضد", "لون", "رياضيات", "توافق"]
    
    # HEADER
    header = [
        {"type": "text", "text": "الألعاب المتاحة", "size": "xxl", "weight": "bold", 
         "color": colors["primary"], "align": "center"},
        {"type": "text", "text": f"{len(games)} لعبة متنوعة", "size": "sm", 
         "color": colors["text2"], "align": "center", "margin": "sm"}
    ]
    
    # BODY
    game_buttons = []
    for i in range(0, len(games), 3):
        row_games = games[i:i+3]
        row = {
            "type": "box", "layout": "horizontal", "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": game, "text": game},
                    "style": "secondary", "height": "sm", "color": colors["secondary"], "flex": 1
                }
                for game in row_games
            ],
            "margin": "sm"
        }
        game_buttons.append(row)
    
    body = [
        create_separator(colors["border"]),
        {"type": "text", "text": "اختر اللعبة", "size": "md", 
         "color": colors["text"], "weight": "bold", "margin": "md"}
    ] + game_buttons + [
        create_separator(colors["border"]),
        {"type": "text", "text": "5 جولات لكل لعبة • نقطة لكل إجابة صحيحة", 
         "size": "xs", "color": colors["text2"], "align": "center", "wrap": True, "margin": "md"},
        create_button("العودة للرئيسية", "home", colors["primary"])
    ]
    
    # FOOTER
    footer = [
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
         "color": colors["text2"], "align": "center"}
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="الألعاب", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# نقاطي
# ============================================================================

def build_my_points(username, points, game_stats, theme="أبيض"):
    """صفحة النقاط"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    total_games = sum(game_stats.values())
    
    # HEADER
    header = [
        {"type": "text", "text": "نقاطي", "size": "xxl", "weight": "bold", 
         "color": colors["primary"], "align": "center"}
    ]
    
    # BODY
    stats_content = [
        {"type": "text", "text": username, "size": "lg", "weight": "bold", 
         "color": colors["text"], "align": "center"},
        {"type": "text", "text": str(points), "size": "xxl", "weight": "bold", 
         "color": colors["primary"], "align": "center", "margin": "md"},
        {"type": "text", "text": f"إجمالي الألعاب: {total_games}", "size": "sm", 
         "color": colors["text2"], "align": "center", "margin": "sm"}
    ]
    
    body = [create_glass_card(colors, stats_content)]
    
    if game_stats:
        body.append({"type": "text", "text": "أكثر الألعاب", "size": "md", 
                    "color": colors["text"], "weight": "bold", "margin": "xl"})
        
        for game_name, plays in sorted(game_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
            body.append(create_glass_card(colors, [{
                "type": "box", "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": game_name, "size": "sm", 
                     "color": colors["text"], "flex": 3},
                    {"type": "text", "text": str(plays), "size": "sm", 
                     "color": colors["primary"], "align": "end", "flex": 1, "weight": "bold"}
                ]
            }]))
    
    body.extend([
        create_separator(colors["border"]),
        {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
            {
                "type": "button",
                "action": {"type": "message", "label": "الصدارة", "text": "صدارة"},
                "style": "primary", "height": "sm", "color": colors["primary"], "flex": 1
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "الرئيسية", "text": "home"},
                "style": "secondary", "height": "sm", "color": colors["secondary"], "flex": 1
            }
        ]}
    ])
    
    # FOOTER
    footer = [
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
         "color": colors["text2"], "align": "center"}
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# الصدارة
# ============================================================================

def build_leaderboard(leaderboard, theme="أبيض"):
    """لوحة الصدارة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # HEADER
    header = [
        {"type": "text", "text": "الصدارة", "size": "xxl", "weight": "bold", 
         "color": colors["primary"], "align": "center"},
        {"type": "text", "text": f"أفضل {len(leaderboard)} لاعبين", "size": "sm", 
         "color": colors["text2"], "align": "center", "margin": "sm"}
    ]
    
    # BODY
    body = [create_separator(colors["border"])]
    
    if leaderboard:
        for i, (name, points) in enumerate(leaderboard):
            rank = f"{i+1}."
            body.append(create_glass_card(colors, [{
                "type": "box", "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": rank, "size": "sm", 
                     "color": colors["text"], "flex": 1, "weight": "bold"},
                    {"type": "text", "text": name[:20], "size": "sm", 
                     "color": colors["text"], "flex": 5},
                    {"type": "text", "text": str(points), "size": "sm", 
                     "color": colors["primary"], "weight": "bold", "align": "end", "flex": 2}
                ]
            }]))
    else:
        body.append({"type": "text", "text": "لا يوجد لاعبين بعد", "size": "md", 
                    "color": colors["text2"], "align": "center", "margin": "xl"})
    
    body.extend([
        create_separator(colors["border"]),
        {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
            {
                "type": "button",
                "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"},
                "style": "primary", "height": "sm", "color": colors["primary"], "flex": 1
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "الرئيسية", "text": "home"},
                "style": "secondary", "height": "sm", "color": colors["secondary"], "flex": 1
            }
        ]}
    ])
    
    # FOOTER
    footer = [
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
         "color": colors["text2"], "align": "center"}
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# اختيار الثيم
# ============================================================================

def build_theme_selector(current_theme="أبيض"):
    """اختيار الثيم"""
    colors = THEMES.get(current_theme, THEMES[DEFAULT_THEME])
    theme_names = list(THEMES.keys())
    
    # HEADER
    header = [
        {"type": "text", "text": "الثيمات", "size": "xxl", "weight": "bold", 
         "color": colors["primary"], "align": "center"},
        {"type": "text", "text": f"الثيم الحالي: {current
    _theme}", "size": "sm",
"color": colors["text2"], "align": "center", "margin": "sm"}
]
# BODY
theme_buttons = []
for i in range(0, len(theme_names), 3):
    row_themes = theme_names[i:i+3]
    row = {
        "type": "box", "layout": "horizontal", "spacing": "sm",
        "contents": [
            {
                "type": "button",
                "action": {"type": "message", "label": theme, "text": f"ثيم {theme}"},
                "style": "primary" if theme == current_theme else "secondary",
                "height": "sm",
                "color": THEMES[theme]["primary"],
                "flex": 1
            }
            for theme in row_themes
        ],
        "margin": "sm"
    }
    theme_buttons.append(row)

body = [
    create_separator(colors["border"]),
    {"type": "text", "text": "اختر ثيمك المفضل", "size": "md", 
     "color": colors["text"], "weight": "bold", "margin": "md"}
] + theme_buttons + [
    create_separator(colors["border"]),
    create_button("العودة للرئيسية", "home", colors["primary"])
]

# FOOTER
footer = [
    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
     "color": colors["text2"], "align": "center"}
]

bubble = create_glass_bubble(colors, header, body, footer)
return FlexMessage(alt_text="الثيمات", contents=FlexContainer.from_dict(bubble))
============================================================================
تسجيل مطلوب
============================================================================
def build_registration_required(theme="أبيض"):
"""تسجيل مطلوب"""
colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
# HEADER
header = [
    {"type": "text", "text": "تسجيل مطلوب", "size": "xxl", "weight": "bold", 
     "color": colors["error"], "align": "center"}
]

# BODY
body = [
    create_glass_card(colors, [
        {"type": "text", "text": "يجب التسجيل للمشاركة في الألعاب وجمع النقاط", 
         "size": "md", "color": colors["text"], "align": "center", "wrap": True}
    ]),
    create_separator(colors["border"]),
    create_button("انضم الآن", "انضم", colors["success"]),
    create_button("العودة للرئيسية", "home", colors["secondary"], "secondary")
]

# FOOTER
footer = [
    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
     "color": colors["text2"], "align": "center"}
]

bubble = create_glass_bubble(colors, header, body, footer)
return FlexMessage(alt_text="تسجيل مطلوب", contents=FlexContainer.from_dict(bubble))
============================================================================
إعلان الفائز
============================================================================
def build_winner_announcement(username, game_name, total_score, final_points, theme="أبيض"):
"""إعلان الفائز"""
colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
# HEADER
header = [
    {"type": "text", "text": "تهانينا", "size": "xxl", "weight": "bold", 
     "color": colors["success"], "align": "center"}
]

# BODY
body = [
    create_glass_card(colors, [
        {"type": "text", "text": username, "size": "xl", "weight": "bold", 
         "color": colors["text"], "align": "center"},
        {"type": "text", "text": f"أنهيت لعبة {game_name}", "size": "md", 
         "color": colors["text2"], "align": "center", "wrap": True, "margin": "sm"}
    ]),
    create_glass_card(colors, [
        {"type": "text", "text": f"+{total_score}", "size": "xxl", "weight": "bold", 
         "color": colors["primary"], "align": "center"},
        {"type": "text", "text": f"الإجمالي: {final_points}", "size": "md", 
         "color": colors["text2"], "align": "center", "margin": "sm"}
    ]),
    create_separator(colors["border"]),
    {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
        {
            "type": "button",
            "action": {"type": "message", "label": "إعادة", "text": f"إعادة {game_name}"},
            "style": "primary", "height": "sm", "color": colors["primary"], "flex": 1
        },
        {
            "type": "button",
            "action": {"type": "message", "label": "الرئيسية", "text": "home"},
            "style": "secondary", "height": "sm", "color": colors["secondary"], "flex": 1
        }
    ]}
]

# FOOTER
footer = [
    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
     "color": colors["text2"], "align": "center"}
]

bubble = create_glass_bubble(colors, header, body, footer)
return FlexMessage(alt_text="الفائز", contents=FlexContainer.from_dict(bubble))
