"""
Bot Mesh - UI Builder v7.3 COMPLETE
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

✅ Glass iOS Style
✅ Complete Theme System
✅ Help Window (5 cards)
✅ Fixed backgroundColor error
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from constants import BOT_RIGHTS, THEMES, DEFAULT_THEME, GAME_LIST

# ============================================================================
# Core Components
# ============================================================================

def create_glass_bubble(colors, header, body, footer=None):
    """Create glass bubble (FIXED - no backgroundColor in boxes)"""
    bubble = {
        "type": "bubble", "size": "mega",
        "header": {
            "type": "box", "layout": "vertical", "contents": header,
            "paddingAll": "20px"
        },
        "body": {
            "type": "box", "layout": "vertical", "contents": body,
            "paddingAll": "20px", "spacing": "md"
        }
    }
    if footer:
        bubble["footer"] = {
            "type": "box", "layout": "vertical", "contents": footer,
            "paddingAll": "15px", "spacing": "sm"
        }
    return bubble

def create_separator(color):
    return {"type": "separator", "color": color, "margin": "md"}

def create_button(label, text, color, style="primary"):
    return {
        "type": "button",
        "action": {"type": "message", "label": label, "text": text},
        "style": style, "height": "sm", "color": color
    }

# ============================================================================
# Games Menu
# ============================================================================

def build_games_menu(theme="أبيض"):
    """Games menu"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    games_order = ["أسرع", "ذكاء", "لعبة", "أغنية", "خمن", "سلسلة",
                   "ترتيب", "تكوين", "ضد", "لون", "رياضيات", "توافق"]
    
    header = [
        {"type": "text", "text": "🎮 الألعاب المتاحة", "size": "xl", "weight": "bold", 
         "color": colors["primary"], "align": "center"},
        {"type": "text", "text": f"اختر من {len(games_order)} لعبة", "size": "sm", 
         "color": colors["text2"], "align": "center", "margin": "sm"}
    ]
    
    game_buttons = []
    for i in range(0, len(games_order), 3):
        row = {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": []}
        for game in games_order[i:i+3]:
            row["contents"].append(create_button(game, game, colors["shadow1"], "secondary"))
        game_buttons.append(row)
    
    body = [create_separator(colors["shadow1"])] + game_buttons + [
        create_separator(colors["shadow1"]),
        {
            "type": "text",
            "text": "5 جولات • نقطة لكل إجابة • أول إجابة صحيحة فقط",
            "size": "xs", "color": colors["text2"], "align": "center", "wrap": True,
            "margin": "md"
        }
    ]
    
    footer = [
        create_separator(colors["shadow1"]),
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
         "color": colors["text2"], "align": "center"}
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="الألعاب", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# My Points
# ============================================================================

def build_my_points(username, points, game_stats, theme="أبيض"):
    """Points page"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    total_games = sum(game_stats.values())
    
    header = [
        {"type": "text", "text": "⭐ نقاطي", "size": "xl", "weight": "bold", 
         "color": colors["primary"], "align": "center"}
    ]
    
    body = [{
        "type": "box", "layout": "vertical",
        "contents": [
            {"type": "text", "text": username, "size": "lg", "weight": "bold", 
             "color": colors["text"], "align": "center"},
            {"type": "text", "text": str(points), "size": "xxl", "weight": "bold", 
             "color": colors["primary"], "align": "center", "margin": "sm"},
            {"type": "text", "text": f"إجمالي الألعاب: {total_games}", "size": "sm", 
             "color": colors["text2"], "align": "center", "margin": "sm"}
        ],
        "cornerRadius": "15px", "paddingAll": "20px"
    }]
    
    if game_stats:
        body.append(create_separator(colors["shadow1"]))
        body.append({"type": "text", "text": "🎯 أكثر الألعاب", "size": "md", 
                    "color": colors["text"], "weight": "bold", "margin": "md"})
        
        for game_name, plays in sorted(game_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
            body.append({
                "type": "box", "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": game_name, "size": "sm", 
                     "color": colors["text"], "flex": 3},
                    {"type": "text", "text": str(plays), "size": "sm", 
                     "color": colors["primary"], "align": "end", "flex": 1, "weight": "bold"}
                ],
                "cornerRadius": "8px", "paddingAll": "10px", "margin": "xs"
            })
    
    footer = [
        {"type": "box", "layout": "horizontal", "spacing": "sm",
         "contents": [
             create_button("🏆 الصدارة", "صدارة", colors["primary"]),
             create_button("🎮 الألعاب", "ألعاب", colors["shadow1"], "secondary")
         ]},
        create_separator(colors["shadow1"]),
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
         "color": colors["text2"], "align": "center"}
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# Leaderboard
# ============================================================================

def build_leaderboard(leaderboard, theme="أبيض"):
    """Leaderboard"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    header = [
        {"type": "text", "text": "🏆 الصدارة", "size": "xl", "weight": "bold", 
         "color": colors["primary"], "align": "center"},
        {"type": "text", "text": f"أفضل {len(leaderboard)} لاعبين", "size": "sm", 
         "color": colors["text2"], "align": "center", "margin": "sm"}
    ]
    
    body = [create_separator(colors["shadow1"])]
    
    if leaderboard:
        medals = ["🥇", "🥈", "🥉"]
        for i, (name, points) in enumerate(leaderboard):
            medal = medals[i] if i < 3 else f"{i+1}."
            body.append({
                "type": "box", "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": medal, "size": "sm", 
                     "color": colors["text"], "flex": 1},
                    {"type": "text", "text": name[:20], "size": "sm", 
                     "color": colors["text"], "flex": 4},
                    {"type": "text", "text": str(points), "size": "sm", 
                     "color": colors["primary"], "weight": "bold", "align": "end", "flex": 1}
                ],
                "cornerRadius": "10px", "paddingAll": "12px", "margin": "xs"
            })
    else:
        body.append({"type": "text", "text": "لا يوجد لاعبين بعد", "size": "sm", 
                    "color": colors["text2"], "align": "center", "margin": "md"})
    
    footer = [
        {"type": "box", "layout": "horizontal", "spacing": "sm",
         "contents": [
             create_button("⭐ نقاطي", "نقاطي", colors["primary"]),
             create_button("🎮 الألعاب", "ألعاب", colors["shadow1"], "secondary")
         ]},
        create_separator(colors["shadow1"]),
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
         "color": colors["text2"], "align": "center"}
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# Registration Required
# ============================================================================

def build_registration_required(theme="أبيض"):
    """Registration required"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    header = [
        {"type": "text", "text": "⭕ تسجيل مطلوب", "size": "xl", "weight": "bold", 
         "color": colors["error"], "align": "center"}
    ]
    
    body = [{
        "type": "text", "text": "يجب التسجيل للمشاركة في الألعاب",
        "size": "md", "color": colors["text"], "align": "center", "wrap": True,
        "margin": "lg"
    }]
    
    footer = [
        create_button("✅ انضم الآن", "انضم", colors["success"]),
        create_separator(colors["shadow1"]),
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
         "color": colors["text2"], "align": "center"}
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="تسجيل مطلوب", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# Winner Announcement
# ============================================================================

def build_winner_announcement(username, game_name, total_score, final_points, theme="أبيض"):
    """Winner announcement"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    header = [
        {"type": "text", "text": "🎉 تهانينا", "size": "xxl", "weight": "bold", 
         "color": colors["success"], "align": "center"}
    ]
    
    body = [{
        "type": "box", "layout": "vertical",
        "contents": [
            {"type": "text", "text": username, "size": "xl", "weight": "bold", 
             "color": colors["text"], "align": "center"},
            {"type": "text", "text": f"أنهيت لعبة {game_name}", "size": "md", 
             "color": colors["text2"], "align": "center", "wrap": True, "margin": "sm"},
            create_separator(colors["shadow1"]),
            {"type": "text", "text": f"+{total_score}", "size": "xxl", "weight": "bold", 
             "color": colors["primary"], "align": "center", "margin": "md"},
            {"type": "text", "text": f"الإجمالي: {final_points}", "size": "md", 
             "color": colors["text2"], "align": "center", "margin": "sm"}
        ],
        "cornerRadius": "15px", "paddingAll": "20px"
    }]
    
    footer = [
        {"type": "box", "layout": "horizontal", "spacing": "sm",
         "contents": [
             create_button("🔄 إعادة", f"إعادة {game_name}", colors["primary"]),
             create_button("🎮 الألعاب", "ألعاب", colors["shadow1"], "secondary")
         ]},
        create_separator(colors["shadow1"]),
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
         "color": colors["text2"], "align": "center"}
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="الفائز", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# Help Window (5 Cards)
# ============================================================================

def build_help_window(theme="أبيض"):
    """Help window - matches design exactly"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    cards = [
        # Card 1: البداية (matches image 1)
        {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", 
                     "color": colors["text"], "align": "center"},
                    create_separator(colors["shadow1"]),
                    {"type": "text", "text": "نقطة | مسجل 520", "size": "md",
                     "color": colors["text"], "align": "center", "margin": "lg"},
                    create_separator(colors["shadow1"]),
                    {"type": "text", "text": "اختر الثيم:", "size": "md", "color": colors["text"], 
                     "weight": "bold", "align": "center", "margin": "lg"},
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm",
                        "contents": [
                            create_button("أبيض", "ثيم أبيض", colors["shadow1"], "secondary"),
                            create_button("أسود", "ثيم أسود", colors["shadow1"], "secondary"),
                            create_button("رمادي", "ثيم رمادي", colors["primary"])
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm",
                        "contents": [
                            create_button("أزرق", "ثيم أزرق", colors["shadow1"], "secondary"),
                            create_button("بنفسجي", "ثيم بنفسجي", colors["shadow1"], "secondary"),
                            create_button("وردي", "ثيم وردي", colors["shadow1"], "secondary")
                        ],
                        "margin": "xs"
                    },
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm",
                        "contents": [
                            create_button("بني", "ثيم ذهبي", colors["shadow1"], "secondary"),
                            create_button("برتقالي", "ثيم برتقالي", colors["shadow1"], "secondary"),
                            create_button("أخضر", "ثيم أخضر", colors["shadow1"], "secondary")
                        ],
                        "margin": "xs"
                    },
                    create_separator(colors["shadow1"]),
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm",
                        "contents": [
                            create_button("انسحب", "انسحب", colors["error"]),
                            create_button("الألعاب", "ألعاب", colors["primary"])
                        ],
                        "margin": "lg"
                    },
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm",
                        "contents": [
                            create_button("نقاطي", "نقاطي", colors["shadow1"], "secondary"),
                            create_button("الصدارة", "صدارة", colors["shadow1"], "secondary")
                        ],
                        "margin": "sm"
                    },
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm",
                        "contents": [
                            create_button("اللعب فردي", "help", colors["shadow1"], "secondary"),
                            create_button("مساعدة", "مساعدة", colors["shadow1"], "secondary")
                        ],
                        "margin": "sm"
                    },
                    create_separator(colors["shadow1"]),
                    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
                     "color": colors["text2"], "align": "center", "margin": "md"}
                ],
                "paddingAll": "24px", "spacing": "none"
            }
        },
        
        # Card 2: الألعاب المتاحة (matches image 2)
        {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "الألعاب المتاحة", "size": "xl", "weight": "bold", 
                     "color": colors["text"], "align": "center"},
                    {"type": "text", "text": "عدد الألعاب: 12", "size": "sm", 
                     "color": colors["text2"], "align": "center", "margin": "sm"},
                    create_separator(colors["shadow1"]),
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm",
                        "contents": [
                            create_button("أسرع", "أسرع", colors["shadow1"], "secondary"),
                            create_button("ذكاء", "ذكاء", colors["shadow1"], "secondary"),
                            create_button("لعبة", "لعبة", colors["shadow1"], "secondary")
                        ],
                        "margin": "lg"
                    },
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm",
                        "contents": [
                            create_button("أغنية", "أغنية", colors["shadow1"], "secondary"),
                            create_button("خمن", "خمن", colors["shadow1"], "secondary"),
                            create_button("سلسلة", "سلسلة", colors["shadow1"], "secondary")
                        ],
                        "margin": "xs"
                    },
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm",
                        "contents": [
                            create_button("ترتيب", "ترتيب", colors["shadow1"], "secondary"),
                            create_button("تكوين", "تكوين", colors["shadow1"], "secondary"),
                            create_button("ضد", "ضد", colors["shadow1"], "secondary")
                        ],
                        "margin": "xs"
                    },
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm",
                        "contents": [
                            create_button("لون", "لون", colors["shadow1"], "secondary"),
                            create_button("رياضيات", "رياضيات", colors["shadow1"], "secondary"),
                            create_button("توافق", "توافق", colors["shadow1"], "secondary")
                        ],
                        "margin": "xs"
                    },
                    create_separator(colors["shadow1"]),
                    {"type": "text", "text": "أوامر اللعب", "size": "md", "color": colors["text"], 
                     "weight": "bold", "align": "center", "margin": "lg"},
                    {"type": "text", "text": "• اضغط على اسم اللعبة لبدء اللعب\n• اكتب 'لمح' للتلميح\n• اكتب 'جاوب' لكشف الإجابة\n• اكتب 'إيقاف' لإنهاء اللعبة", 
                     "size": "xs", "color": colors["text2"], "wrap": True, "margin": "sm"},
                    create_separator(colors["shadow1"]),
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm",
                        "contents": [
                            create_button("البداية", "home", colors["shadow1"], "secondary"),
                            create_button("إيقاف", "إيقاف", colors["error"])
                        ],
                        "margin": "lg"
                    },
                    create_separator(colors["shadow1"]),
                    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
                     "color": colors["text2"], "align": "center", "margin": "md"}
                ],
                "paddingAll": "24px", "spacing": "none"
            }
        },
        
        # Card 3: اللعب الجماعي
        {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "اللعب الجماعي", "size": "xl", "weight": "bold", 
                     "color": colors["text"], "align": "center"},
                    {"type": "text", "text": "نافس أصدقاءك في المجموعات", "size": "sm", 
                     "color": colors["text2"], "align": "center", "margin": "sm"},
                    create_separator(colors["shadow1"]),
                    {"type": "text", "text": "المميزات:", "size": "md", "color": colors["text"], 
                     "weight": "bold", "margin": "lg"},
                    {"type": "text", "text": "• المنافسة الحية بين الأعضاء\n• أول إجابة صحيحة تفوز\n• 5 جولات للمنافسة\n• نقاط تراكمية للصدارة", 
                     "size": "sm", "color": colors["text2"], "wrap": True, "margin": "sm"},
                    create_separator(colors["shadow1"]),
                    {"type": "text", "text": "كيفية البدء:", "size": "md", "color": colors["text"], 
                     "weight": "bold", "margin": "lg"},
                    {"type": "text", "text": "منشن البوت @Bot ثم اختر اللعبة", 
                     "size": "sm", "color": colors["text2"], "wrap": True, "margin": "sm"},
                    create_separator(colors["shadow1"]),
                    create_button("الألعاب", "ألعاب", colors["primary"]),
                    create_separator(colors["shadow1"]),
                    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
                     "color": colors["text2"], "align": "center", "margin": "md"}
                ],
                "paddingAll": "24px", "spacing": "none"
            }
        },
        
        # Card 4: اللعب الفردي
        {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "اللعب الفردي", "size": "xl", "weight": "bold", 
                     "color": colors["text"], "align": "center"},
                    {"type": "text", "text": "تدرب وطور مهاراتك", "size": "sm", 
                     "color": colors["text2"], "align": "center", "margin": "sm"},
                    create_separator(colors["shadow1"]),
                    {"type": "text", "text": "المميزات:", "size": "md", "color": colors["text"], 
                     "weight": "bold", "margin": "lg"},
                    {"type": "text", "text": "• تدرب بدون ضغط الوقت\n• تلميحات ومساعدة متاحة\n• تتبع تقدمك ونقاطك\n• جاهز للمنافسة الجماعية", 
                     "size": "sm", "color": colors["text2"], "wrap": True, "margin": "sm"},
                    create_separator(colors["shadow1"]),
                    {"type": "text", "text": "كيفية البدء:", "size": "md", "color": colors["text"], 
                     "weight": "bold", "margin": "lg"},
                    {"type": "text", "text": "راسل البوت مباشرة واختر اللعبة", 
                     "size": "sm", "color": colors["text2"], "wrap": True, "margin": "sm"},
                    create_separator(colors["shadow1"]),
                    create_button("الألعاب", "ألعاب", colors["primary"]),
                    create_separator(colors["shadow1"]),
                    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
                     "color": colors["text2"], "align": "center", "margin": "md"}
                ],
                "paddingAll": "24px", "spacing": "none"
            }
        }
    ]
    
    return FlexMessage(
        alt_text="المساعدة",
        contents=FlexContainer.from_dict({"type": "carousel", "contents": cards})
    )

# ============================================================================
# Theme Selector
# ============================================================================

def build_theme_selector(current_theme="أبيض"):
    """Theme selector"""
    colors = THEMES.get(current_theme, THEMES[DEFAULT_THEME])
    
    theme_buttons = []
    theme_names = list(THEMES.keys())
    
    for i in range(0, len(theme_names), 3):
        row = {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": []}
        for theme_name in theme_names[i:i+3]:
            theme_colors = THEMES[theme_name]
            is_selected = (theme_name == current_theme)
            row["contents"].append({
                "type": "button",
                "action": {"type": "message", "label": f"{'✓ ' if is_selected else ''}{theme_name}", 
                          "text": f"ثيم {theme_name}"},
                "style": "primary" if is_selected else "secondary",
                "height": "sm",
                "color": theme_colors["primary"]
            })
        theme_buttons.append(row)
    
    header = [
        {"type": "text", "text": "🎨", "size": "xxl", "align": "center"},
        {"type": "text", "text": "اختر الثيم", "size": "xl", "weight": "bold", 
         "color": colors["text"], "align": "center", "margin": "md"},
        {"type": "text", "text": f"الثيم الحالي: {current_theme}", "size": "sm", 
         "color": colors["text2"], "align": "center", "margin": "sm"}
    ]
    
    body = [
        create_separator(colors["shadow1"]),
        {"type": "text", "text": "اختر ثيمك المفضل", "size": "md", 
         "color": colors["text"], "weight": "bold", "align": "center", "margin": "lg"}
    ] + theme_buttons + [{
        "type": "text",
        "text": "الثيم سيُطبق على جميع القوائم والأزرار",
        "size": "xs", "color": colors["text2"], "align": "center", "wrap": True,
        "margin": "lg"
    }]
    
    bubble = create_glass_bubble(colors, header, body)
    return FlexMessage(alt_text="اختيار الثيم", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# Enhanced Home
# ============================================================================

def build_enhanced_home(username, points, is_registered, theme="أبيض"):
    """Enhanced home page"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    registration_emoji = "✅" if is_registered else "⭕"
    registration_text = f"مسجل • {points} نقطة" if is_registered else "غير مسجل"
    
    # Theme buttons
    theme_buttons = []
    theme_names = list(THEMES.keys())
    for i in range(0, len(theme_names), 3):
        row = {"type": "box", "layout": "horizontal", "spacing": "xs", "contents": []}
        for theme_name in theme_names[i:i+3]:
            row["contents"].append(create_button(theme_name, f"ثيم {theme_name}", 
                                                colors["shadow1"], "secondary"))
        theme_buttons.append(row)
        if i > 0:
            theme_buttons[-1]["margin"] = "xs"
    
    header = [
        {"type": "text", "text": "🎮", "size": "xxl", "align": "center"},
        {"type": "text", "text": "Bot Mesh", "size": "xl", "weight": "bold", 
         "color": colors["text"], "align": "center", "margin": "md"}
    ]
    
    body = [
        create_separator(colors["shadow1"]),
        {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": username, "size": "lg", "weight": "bold", 
                 "color": colors["text"], "align": "center"},
                {"type": "text", "text": f"{registration_emoji} {registration_text}", 
                 "size": "sm", "color": colors["success"] if is_registered else colors["text2"], 
                 "align": "center", "margin": "sm"}
            ],
            "cornerRadius": "20px", "paddingAll": "20px", "margin": "lg"
        },
        {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎨 اختر الثيم", "size": "sm", 
                 "color": colors["text"], "weight": "bold"}
            ] + theme_buttons,
            "cornerRadius": "15px", "paddingAll": "12px", "margin": "lg"
        },
        {
            "type": "box", "layout": "vertical", "spacing": "sm",
            "contents": [
                create_button("🎮 الألعاب", "ألعاب", colors["primary"]),
                create_button("⭐ نقاطي", "نقاطي", colors["shadow1"], "secondary"),
                create_button("🏆 الصدارة", "صدارة", colors["shadow1"], "secondary"),
                create_button("❓ مساعدة", "مساعدة", colors["shadow1"], "secondary")
            ],
            "margin": "lg"
        }
    ]
    
    footer = [
        create_separator(colors["shadow1"]),
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", 
         "color": colors["text2"], "align": "center", "margin": "md"}
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="البداية", contents=FlexContainer.from_dict(bubble))
