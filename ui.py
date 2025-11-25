"""
Bot Mesh v6.1 - UI Module
نوافذ Flex احترافية وسهلة الاستخدام
"""

from linebot.v3.messaging import FlexMessage, FlexContainer

# ============================================================================
# الثيمات الجميلة - 9 ثيمات
# ============================================================================
THEMES = {
    "🖤": {"name": "أسود أنيق", "primary": "#667EEA", "bg": "#1A202C", "text": "#F7FAFC"},
    "🤎": {"name": "بني ترابي", "primary": "#8B4513", "bg": "#FEFCF9", "text": "#5C2E00"},
    "🩷": {"name": "وردي زهري", "primary": "#D53F8C", "bg": "#FFF5F7", "text": "#702459"},
    "💚": {"name": "أخضر طبيعي", "primary": "#38A169", "bg": "#F0FDF4", "text": "#1C4532"},
    "🧡": {"name": "برتقالي دافئ", "primary": "#DD6B20", "bg": "#FFFAF0", "text": "#7C2D12"},
    "🩶": {"name": "رمادي فضي", "primary": "#718096", "bg": "#F7FAFC", "text": "#2D3748"},
    "💜": {"name": "بنفسجي حالم", "primary": "#805AD5", "bg": "#EDF2F7", "text": "#2D3748"},
    "💙": {"name": "أزرق المحيط", "primary": "#3182CE", "bg": "#EBF8FF", "text": "#2C5282"},
    "🤍": {"name": "أبيض نظيف", "primary": "#4299E1", "bg": "#FFFFFF", "text": "#2D3748"}
}

def get_theme(emoji="💜"):
    return THEMES.get(emoji, THEMES["💜"])

# ============================================================================
# الشاشة الرئيسية
# ============================================================================
def home_screen(username, points, theme="💜"):
    t = get_theme(theme)
    
    return FlexMessage(alt_text="🎮 Bot Mesh", contents=FlexContainer.from_dict({
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎮 Bot Mesh", "size": "xxl", "weight": "bold", "color": "#FFFFFF", "align": "center"},
                {"type": "text", "text": "بوت الألعاب الذكي", "size": "sm", "color": "#FFFFFF", "align": "center", "margin": "sm"}
            ],
            "backgroundColor": t["primary"],
            "paddingAll": "25px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "👤 اللاعب", "size": "xs", "color": "#718096", "align": "center"},
                                {"type": "text", "text": username, "size": "xl", "weight": "bold", "color": t["primary"], "align": "center", "wrap": True}
                            ],
                            "flex": 1
                        },
                        {"type": "separator", "margin": "md"},
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "⭐ النقاط", "size": "xs", "color": "#718096", "align": "center"},
                                {"type": "text", "text": str(points), "size": "xl", "weight": "bold", "color": "#48BB78", "align": "center"}
                            ],
                            "flex": 1
                        }
                    ],
                    "backgroundColor": "#FFFFFF",
                    "cornerRadius": "15px",
                    "paddingAll": "20px"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": t["bg"]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {"type": "button", "action": {"type": "message", "label": "🎮 ابدأ اللعب", "text": "العاب"}, "style": "primary", "color": t["primary"], "height": "sm"},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {"type": "button", "action": {"type": "message", "label": "🎨 الثيمات", "text": "ثيمات"}, "style": "secondary", "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "🏆 الصدارة", "text": "صدارة"}, "style": "secondary", "height": "sm"}
                    ]
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": t["bg"]
        }
    }))

# ============================================================================
# قائمة الألعاب
# ============================================================================
def games_menu(mode="فردي", theme="💜"):
    t = get_theme(theme)
    
    games = [
        {"icon": "🧠", "name": "ذكاء", "desc": "ألغاز وأحاجي", "cmd": "لعبة ذكاء"},
        {"icon": "🔢", "name": "رياضيات", "desc": "حساب سريع", "cmd": "لعبة رياضيات"},
        {"icon": "🎨", "name": "ألوان", "desc": "تحدي الألوان", "cmd": "لعبة ألوان"},
        {"icon": "⚡", "name": "سرعة", "desc": "كتابة سريعة", "cmd": "لعبة سرعة"},
        {"icon": "🔤", "name": "كلمات", "desc": "ترتيب حروف", "cmd": "لعبة كلمات"},
        {"icon": "🎵", "name": "أغاني", "desc": "خمن المغني", "cmd": "لعبة أغاني"},
        {"icon": "↔️", "name": "أضداد", "desc": "عكس الكلمة", "cmd": "لعبة أضداد"},
        {"icon": "🔮", "name": "تخمين", "desc": "خمن الكلمة", "cmd": "لعبة تخمين"},
        {"icon": "🔗", "name": "سلسلة", "desc": "سلسلة كلمات", "cmd": "لعبة سلسلة"},
        {"icon": "🎯", "name": "إنسان حيوان", "desc": "إنسان حيوان نبات", "cmd": "لعبة إنسان حيوان"},
        {"icon": "🖤", "name": "توافق", "desc": "نسبة التوافق", "cmd": "لعبة توافق"},
        {"icon": "🔡", "name": "تكوين", "desc": "تكوين كلمات", "cmd": "لعبة تكوين"}
    ]
    
    game_boxes = []
    for game in games:
        game_boxes.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": game["icon"],
                    "size": "xl",
                    "flex": 0,
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": game["name"], "size": "md", "weight": "bold", "color": t["text"]},
                        {"type": "text", "text": game["desc"], "size": "xs", "color": "#718096", "margin": "xs"}
                    ],
                    "flex": 1
                }
            ],
            "backgroundColor": "#FFFFFF",
            "cornerRadius": "12px",
            "paddingAll": "15px",
            "action": {"type": "message", "text": game["cmd"]},
            "margin": "sm"
        })
    
    return FlexMessage(alt_text="🎮 الألعاب", contents=FlexContainer.from_dict({
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎮 اختر لعبتك", "size": "xl", "weight": "bold", "color": "#FFFFFF", "align": "center"},
                {"type": "text", "text": f"وضع اللعب: {mode}", "size": "sm", "color": "#FFFFFF", "align": "center", "margin": "sm"}
            ],
            "backgroundColor": t["primary"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "none",
            "contents": game_boxes,
            "paddingAll": "15px",
            "backgroundColor": t["bg"]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {"type": "button", "action": {"type": "message", "label": "🔄 وضع " + ("مجموعة" if mode == "فردي" else "فردي"), "text": "مجموعة" if mode == "فردي" else "فردي"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "secondary", "height": "sm"}
            ],
            "paddingAll": "15px",
            "backgroundColor": t["bg"]
        }
    }))

# ============================================================================
# سؤال اللعبة
# ============================================================================
def game_question(game_name, question, round_num, total_rounds, mode="فردي", theme="💜"):
    t = get_theme(theme)
    
    return FlexMessage(alt_text=f"❓ {game_name}", contents=FlexContainer.from_dict({
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": f"🎮 {game_name}", "size": "lg", "weight": "bold", "color": "#FFFFFF", "flex": 2},
                        {"type": "text", "text": f"سؤال {round_num}/{total_rounds}", "size": "md", "color": "#FFFFFF", "align": "end", "flex": 1}
                    ]
                }
            ],
            "backgroundColor": t["primary"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "❓ السؤال", "size": "sm", "color": "#718096", "weight": "bold"},
                        {"type": "text", "text": question, "size": "xl", "color": t["text"], "weight": "bold", "wrap": True, "margin": "md"}
                    ],
                    "backgroundColor": "#FFFFFF",
                    "cornerRadius": "15px",
                    "paddingAll": "20px"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "💡 اكتب إجابتك في الدردشة", "size": "xs", "color": "#718096", "align": "center"}
                    ]
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": t["bg"]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {"type": "button", "action": {"type": "message", "label": "💡 تلميح", "text": "تلميح"}, "style": "secondary", "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "👁 الإجابة", "text": "اجابة"}, "style": "secondary", "height": "sm"}
                    ]
                },
                {"type": "button", "action": {"type": "message", "label": "⛔ إيقاف اللعبة", "text": "ايقاف"}, "style": "primary", "color": "#F56565", "height": "sm"}
            ],
            "paddingAll": "15px",
            "backgroundColor": t["bg"]
        }
    }))

# ============================================================================
# نتيجة اللعبة
# ============================================================================
def game_result(winner_name, winner_points, all_players, mode="فردي", theme="💜"):
    t = get_theme(theme)
    
    medals = ["🥇", "🥈", "🥉"]
    players_list = []
    
    for i, (name, points) in enumerate(all_players[:5], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        players_list.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": medal, "size": "lg", "flex": 0},
                {"type": "text", "text": name, "size": "md", "color": t["text"], "flex": 2, "margin": "md"},
                {"type": "text", "text": f"{points} نقطة", "size": "sm", "color": "#48BB78", "weight": "bold", "align": "end", "flex": 1}
            ],
            "backgroundColor": "#FFFFFF" if i <= 3 else "transparent",
            "cornerRadius": "10px",
            "paddingAll": "12px",
            "margin": "xs"
        })
    
    return FlexMessage(alt_text="🏆 النتيجة", contents=FlexContainer.from_dict({
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎉", "size": "xxl", "align": "center"},
                {"type": "text", "text": "انتهت اللعبة!", "size": "xl", "weight": "bold", "color": "#FFFFFF", "align": "center", "margin": "md"}
            ],
            "backgroundColor": "#48BB78",
            "paddingAll": "25px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "🏆 الفائز", "size": "sm", "color": "#718096", "align": "center"},
                        {"type": "text", "text": winner_name, "size": "xxl", "weight": "bold", "color": t["primary"], "align": "center", "margin": "sm", "wrap": True},
                        {"type": "text", "text": f"{winner_points} نقطة", "size": "lg", "color": "#48BB78", "weight": "bold", "align": "center", "margin": "sm"}
                    ],
                    "backgroundColor": "#FFFFFF",
                    "cornerRadius": "15px",
                    "paddingAll": "20px"
                },
                {"type": "separator", "margin": "lg"},
                {"type": "text", "text": "📊 جميع اللاعبين", "size": "md", "weight": "bold", "color": t["text"], "margin": "md"}
            ] + players_list,
            "paddingAll": "20px",
            "backgroundColor": t["bg"]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {"type": "button", "action": {"type": "message", "label": "🔄 لعب مرة أخرى", "text": "العاب"}, "style": "primary", "color": t["primary"], "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "secondary", "height": "sm"}
            ],
            "paddingAll": "15px",
            "backgroundColor": t["bg"]
        }
    }))

# ============================================================================
# لوحة الصدارة
# ============================================================================
def leaderboard(top_players, theme="💜"):
    t = get_theme(theme)
    
    medals = ["🥇", "🥈", "🥉"]
    players_list = []
    
    if not top_players:
        players_list.append({
            "type": "text",
            "text": "لا يوجد لاعبون بعد 😊",
            "size": "md",
            "color": "#718096",
            "align": "center"
        })
    else:
        for i, (name, points) in enumerate(top_players[:10], 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            players_list.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": medal, "size": "xl", "flex": 0, "weight": "bold", "color": t["primary"]},
                    {"type": "text", "text": name, "size": "md", "color": t["text"], "flex": 2, "margin": "md", "wrap": True},
                    {"type": "text", "text": str(points), "size": "md", "color": "#48BB78", "weight": "bold", "align": "end", "flex": 1}
                ],
                "backgroundColor": "#FFFFFF" if i <= 3 else "transparent",
                "cornerRadius": "12px",
                "paddingAll": "15px",
                "margin": "xs"
            })
    
    return FlexMessage(alt_text="🏆 الصدارة", contents=FlexContainer.from_dict({
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🏆 لوحة الصدارة", "size": "xl", "weight": "bold", "color": "#FFFFFF", "align": "center"},
                {"type": "text", "text": "أفضل 10 لاعبين", "size": "sm", "color": "#FFFFFF", "align": "center", "margin": "sm"}
            ],
            "backgroundColor": t["primary"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "none",
            "contents": players_list,
            "paddingAll": "20px",
            "backgroundColor": t["bg"]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "primary", "color": t["primary"], "height": "sm"}
            ],
            "paddingAll": "15px",
            "backgroundColor": t["bg"]
        }
    }))

# ============================================================================
# اختيار الثيمات
# ============================================================================
def themes_selector(current_theme="💜"):
    t = get_theme(current_theme)
    
    theme_buttons = []
    for emoji, data in THEMES.items():
        is_current = (emoji == current_theme)
        theme_buttons.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": emoji, "size": "xl", "flex": 0},
                {"type": "text", "text": data["name"], "size": "md", "color": t["text"], "flex": 1, "margin": "md"},
                {"type": "text", "text": "✓" if is_current else "", "size": "lg", "color": "#48BB78", "flex": 0}
            ],
            "backgroundColor": "#FFFFFF",
            "cornerRadius": "12px",
            "paddingAll": "15px",
            "action": {"type": "message", "text": f"ثيم {emoji}"},
            "margin": "sm"
        })
    
    return FlexMessage(alt_text="🎨 الثيمات", contents=FlexContainer.from_dict({
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎨 اختر الثيم المفضل", "size": "xl", "weight": "bold", "color": "#FFFFFF", "align": "center"},
                {"type": "text", "text": f"الثيم الحالي: {THEMES[current_theme]['name']}", "size": "sm", "color": "#FFFFFF", "align": "center", "margin": "sm"}
            ],
            "backgroundColor": t["primary"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "none",
            "contents": theme_buttons,
            "paddingAll": "15px",
            "backgroundColor": t["bg"]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "secondary", "height": "sm"}
            ],
            "paddingAll": "15px",
            "backgroundColor": t["bg"]
        }
    }))
