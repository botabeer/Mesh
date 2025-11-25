"""
Bot Mesh v6.0 - UI Module
Simple & Beautiful Flex Messages
"""

from linebot.v3.messaging import FlexMessage, FlexContainer

# ============================================================================
# الألوان والثيمات
# ============================================================================
THEME = {
    "primary": "#667EEA",
    "secondary": "#764BA2",
    "success": "#48BB78",
    "error": "#F56565",
    "bg": "#F7FAFC",
    "card": "#FFFFFF",
    "text": "#2D3748",
    "text2": "#718096",
    "shadow": "#E2E8F0"
}

# ============================================================================
# مكونات مساعدة
# ============================================================================

def button(label, text, color=None):
    """إنشاء زر"""
    return {
        "type": "button",
        "action": {"type": "message", "label": label, "text": text},
        "style": "primary" if color else "secondary",
        "height": "sm",
        "color": color or THEME["shadow"]
    }

def separator():
    """خط فاصل"""
    return {"type": "separator", "margin": "lg", "color": THEME["shadow"]}

def text_box(text, size="md", color=None, bold=False):
    """صندوق نص"""
    return {
        "type": "text",
        "text": text,
        "size": size,
        "color": color or THEME["text"],
        "weight": "bold" if bold else "regular",
        "wrap": True,
        "align": "center"
    }

# ============================================================================
# الشاشات الرئيسية
# ============================================================================

def home_screen(username, points):
    """🏠 الشاشة الرئيسية"""
    content = {
        "type": "bubble",
        "hero": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎮 Bot Mesh",
                    "size": "xxl",
                    "weight": "bold",
                    "color": "#FFFFFF",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "بوت الألعاب الجماعية",
                    "size": "sm",
                    "color": "#FFFFFF",
                    "align": "center",
                    "margin": "sm"
                }
            ],
            "backgroundColor": THEME["primary"],
            "paddingAll": "30px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                text_box("👤 اللاعب", "xs", THEME["text2"]),
                                text_box(username, "lg", THEME["primary"], True)
                            ],
                            "flex": 1
                        },
                        {"type": "separator"},
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                text_box("⭐ النقاط", "xs", THEME["text2"]),
                                text_box(str(points), "lg", THEME["success"], True)
                            ],
                            "flex": 1
                        }
                    ],
                    "backgroundColor": THEME["card"],
                    "cornerRadius": "15px",
                    "paddingAll": "15px"
                },
                separator(),
                text_box("اختر وضع اللعب:", "md", THEME["text"], True)
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                button("👥 لعب جماعي", "جماعي", THEME["primary"]),
                button("👤 لعب فردي", "فردي", THEME["secondary"]),
                separator(),
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        button("🎮 الألعاب", "العاب"),
                        button("🏆 الصدارة", "صدارة")
                    ]
                }
            ],
            "paddingAll": "20px"
        }
    }
    
    return FlexMessage(alt_text="الشاشة الرئيسية", contents=FlexContainer.from_dict(content))


def games_menu(mode="فردي"):
    """🎮 قائمة الألعاب"""
    games = [
        {"icon": "🧠", "name": "ذكاء", "cmd": "لعبة ذكاء"},
        {"icon": "🔢", "name": "رياضيات", "cmd": "لعبة رياضيات"},
        {"icon": "🎨", "name": "ألوان", "cmd": "لعبة ألوان"},
        {"icon": "⚡", "name": "سرعة", "cmd": "لعبة سرعة"},
        {"icon": "🔤", "name": "كلمات", "cmd": "لعبة كلمات"},
        {"icon": "🎵", "name": "أغاني", "cmd": "لعبة أغاني"}
    ]
    
    # بناء أزرار الألعاب
    game_buttons = []
    for i in range(0, len(games), 2):
        row = {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": []
        }
        for game in games[i:i+2]:
            row["contents"].append(button(f"{game['icon']} {game['name']}", game['cmd']))
        game_buttons.append(row)
    
    content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                text_box(f"🎮 الألعاب - {mode}", "xl", "#FFFFFF", True)
            ],
            "backgroundColor": THEME["primary"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": game_buttons + [
                separator(),
                text_box(f"وضع اللعب: {mode}", "xs", THEME["text2"])
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                button("🏠 الرئيسية", "بداية", THEME["primary"]),
                button("🔄 تغيير الوضع", "جماعي" if mode == "فردي" else "فردي")
            ],
            "paddingAll": "15px"
        }
    }
    
    return FlexMessage(alt_text="قائمة الألعاب", contents=FlexContainer.from_dict(content))


def game_question(game_name, question, round_num, total_rounds, mode="فردي"):
    """❓ سؤال اللعبة"""
    content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        text_box(f"🎮 {game_name}", "lg", "#FFFFFF", True),
                        text_box(f"{round_num}/{total_rounds}", "md", "#FFFFFF")
                    ]
                },
                text_box(f"وضع: {mode}", "xs", "#FFFFFF")
            ],
            "backgroundColor": THEME["primary"],
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
                        text_box("❓ السؤال:", "sm", THEME["text2"], True),
                        text_box(question, "xl", THEME["primary"], True)
                    ],
                    "backgroundColor": THEME["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "25px"
                },
                text_box("💡 اكتب إجابتك في الدردشة", "xs", THEME["text2"])
            ],
            "paddingAll": "20px"
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
                        button("💡 تلميح", "تلميح"),
                        button("👁️ إجابة", "اجابة")
                    ]
                },
                button("⛔ إيقاف", "ايقاف", THEME["error"])
            ],
            "paddingAll": "15px"
        }
    }
    
    return FlexMessage(alt_text=f"{game_name} - سؤال {round_num}", contents=FlexContainer.from_dict(content))


def game_result(winner_name, winner_points, all_players, mode="فردي"):
    """🏆 نتيجة اللعبة"""
    # قائمة اللاعبين
    players_list = []
    for i, (name, points) in enumerate(all_players[:5], 1):
        medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
        players_list.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                text_box(f"{medal} {name}", "sm", THEME["text"]),
                text_box(f"{points} نقطة", "sm", THEME["primary"], True)
            ],
            "backgroundColor": THEME["card"] if i == 1 else "transparent",
            "cornerRadius": "10px",
            "paddingAll": "10px"
        })
    
    content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                text_box("🎉 انتهت اللعبة!", "xxl", "#FFFFFF", True)
            ],
            "backgroundColor": THEME["success"],
            "paddingAll": "30px"
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
                        text_box("🏆 الفائز", "sm", THEME["text2"]),
                        text_box(winner_name, "xxl", THEME["primary"], True),
                        text_box(f"{winner_points} نقطة", "lg", THEME["success"], True)
                    ],
                    "backgroundColor": THEME["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "25px"
                },
                separator(),
                text_box("📊 جميع اللاعبين:", "sm", THEME["text"], True)
            ] + players_list,
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                button("🔄 لعب مرة أخرى", "العاب", THEME["primary"]),
                button("🏠 الرئيسية", "بداية")
            ],
            "paddingAll": "15px"
        }
    }
    
    return FlexMessage(alt_text="نتيجة اللعبة", contents=FlexContainer.from_dict(content))


def leaderboard(top_players):
    """🏆 لوحة الصدارة"""
    medals = ["🥇", "🥈", "🥉"]
    
    # قائمة اللاعبين
    players_list = []
    for i, (name, points) in enumerate(top_players[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        bg = THEME["card"] if i <= 3 else "transparent"
        
        players_list.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                text_box(medal, "lg", THEME["primary"], True),
                text_box(name, "md", THEME["text"]),
                text_box(str(points), "md", THEME["success"], True)
            ],
            "spacing": "md",
            "backgroundColor": bg,
            "cornerRadius": "15px",
            "paddingAll": "15px"
        })
    
    content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                text_box("🏆 لوحة الصدارة", "xxl", "#FFFFFF", True),
                text_box("أفضل 10 لاعبين", "sm", "#FFFFFF")
            ],
            "backgroundColor": THEME["primary"],
            "paddingAll": "25px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": players_list if players_list else [
                text_box("لا يوجد لاعبون بعد", "md", THEME["text2"])
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                button("🏠 الرئيسية", "بداية", THEME["primary"])
            ],
            "paddingAll": "15px"
        }
    }
    
    return FlexMessage(alt_text="لوحة الصدارة", contents=FlexContainer.from_dict(content))
