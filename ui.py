"""
Bot Mesh v6.0 - UI Module
Simple & Beautiful Flex Messages
"""

from linebot.v3.messaging import FlexMessage, FlexContainer

# ============================================================================
# 9 ثيمات جميلة
# ============================================================================
THEMES = {
    "💜": {  # Purple Dream
        "name": "أرجواني حالم",
        "primary": "#805AD5",
        "secondary": "#9F7AEA",
        "success": "#48BB78",
        "error": "#F56565",
        "bg": "#EDF2F7",
        "card": "#FFFFFF",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow": "#CBD5E0"
    },
    "💚": {  # Green Nature
        "name": "أخضر طبيعي",
        "primary": "#38A169",
        "secondary": "#48BB78",
        "success": "#48BB78",
        "error": "#F56565",
        "bg": "#F0FDF4",
        "card": "#FFFFFF",
        "text": "#1C4532",
        "text2": "#276749",
        "shadow": "#C6F6D5"
    },
    "🤍": {  # Clean White
        "name": "أبيض نظيف",
        "primary": "#4299E1",
        "secondary": "#63B3ED",
        "success": "#48BB78",
        "error": "#F56565",
        "bg": "#F7FAFC",
        "card": "#FFFFFF",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow": "#E2E8F0"
    },
    "🖤": {  # Dark Elegant
        "name": "أسود أنيق",
        "primary": "#667EEA",
        "secondary": "#7F9CF5",
        "success": "#48BB78",
        "error": "#FC8181",
        "bg": "#1A202C",
        "card": "#2D3748",
        "text": "#F7FAFC",
        "text2": "#CBD5E0",
        "shadow": "#4A5568"
    },
    "💙": {  # Ocean Blue
        "name": "أزرق المحيط",
        "primary": "#2B6CB0",
        "secondary": "#3182CE",
        "success": "#48BB78",
        "error": "#F56565",
        "bg": "#EBF8FF",
        "card": "#FFFFFF",
        "text": "#2C5282",
        "text2": "#2B6CB0",
        "shadow": "#BEE3F8"
    },
    "🩶": {  # Silver Gray
        "name": "رمادي فضي",
        "primary": "#4A5568",
        "secondary": "#718096",
        "success": "#48BB78",
        "error": "#F56565",
        "bg": "#F7FAFC",
        "card": "#FFFFFF",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow": "#E2E8F0"
    },
    "🩷": {  # Pink Blossom
        "name": "وردي زهري",
        "primary": "#B83280",
        "secondary": "#D53F8C",
        "success": "#48BB78",
        "error": "#F56565",
        "bg": "#FFF5F7",
        "card": "#FFFFFF",
        "text": "#702459",
        "text2": "#97266D",
        "shadow": "#FED7E2"
    },
    "🧡": {  # Warm Sunset
        "name": "برتقالي دافئ",
        "primary": "#C05621",
        "secondary": "#DD6B20",
        "success": "#48BB78",
        "error": "#F56565",
        "bg": "#FFFAF0",
        "card": "#FFFFFF",
        "text": "#7C2D12",
        "text2": "#9C4221",
        "shadow": "#FEEBC8"
    },
    "🤎": {  # Earth Brown
        "name": "بني ترابي",
        "primary": "#744210",
        "secondary": "#8B4513",
        "success": "#48BB78",
        "error": "#F56565",
        "bg": "#FEFCF9",
        "card": "#FFFFFF",
        "text": "#5C2E00",
        "text2": "#7A4F1D",
        "shadow": "#E6D5C3"
    }
}

DEFAULT_THEME = "💜"

def get_theme(theme_emoji="💜"):
    """الحصول على ألوان الثيم"""
    return THEMES.get(theme_emoji, THEMES[DEFAULT_THEME])

# ============================================================================
# مكونات مساعدة
# ============================================================================

def button(label, text, color=None, theme=None):
    """إنشاء زر"""
    if theme is None:
        theme = get_theme()
    return {
        "type": "button",
        "action": {"type": "message", "label": label, "text": text},
        "style": "primary" if color else "secondary",
        "height": "sm",
        "color": color or theme["shadow"]
    }

def separator(theme=None):
    """خط فاصل"""
    if theme is None:
        theme = get_theme()
    return {"type": "separator", "margin": "lg", "color": theme["shadow"]}

def text_box(text, size="md", color=None, bold=False, theme=None):
    """صندوق نص"""
    if theme is None:
        theme = get_theme()
    return {
        "type": "text",
        "text": text,
        "size": size,
        "color": color or theme["text"],
        "weight": "bold" if bold else "regular",
        "wrap": True,
        "align": "center"
    }

# ============================================================================
# الشاشات الرئيسية
# ============================================================================

def home_screen(username, points, current_theme="💜"):
    """🏠 الشاشة الرئيسية"""
    theme = get_theme(current_theme)
    
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
            "backgroundColor": theme["primary"],
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
                                text_box("👤 اللاعب", "xs", theme["text2"], theme=theme),
                                text_box(username, "lg", theme["primary"], True, theme)
                            ],
                            "flex": 1
                        },
                        {"type": "separator"},
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                text_box("⭐ النقاط", "xs", theme["text2"], theme=theme),
                                text_box(str(points), "lg", theme["success"], True, theme)
                            ],
                            "flex": 1
                        }
                    ],
                    "backgroundColor": theme["card"],
                    "cornerRadius": "15px",
                    "paddingAll": "15px"
                },
                separator(theme),
                text_box("اختر وضع اللعب:", "md", theme["text"], True, theme)
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                button("👥 لعب جماعي", "جماعي", theme["primary"], theme),
                button("👤 لعب فردي", "فردي", theme["secondary"], theme),
                separator(theme),
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        button("🎮 الألعاب", "العاب", theme=theme),
                        button("🎨 الثيمات", "ثيمات", theme=theme)
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        button("🏆 الصدارة", "صدارة", theme=theme),
                        button("ℹ️ المساعدة", "مساعدة", theme=theme)
                    ]
                }
            ],
            "paddingAll": "20px"
        }
    }
    
    return FlexMessage(alt_text="الشاشة الرئيسية", contents=FlexContainer.from_dict(content))


def themes_selector(current_theme="💜"):
    """🎨 شاشة اختيار الثيمات"""
    theme = get_theme(current_theme)
    
    # بناء أزرار الثيمات (3 في كل صف)
    theme_buttons = []
    theme_items = list(THEMES.items())
    
    for i in range(0, len(theme_items), 3):
        row_themes = theme_items[i:i+3]
        buttons = []
        
        for emoji, t_data in row_themes:
            is_current = (emoji == current_theme)
            btn = button(
                f"{emoji} {t_data['name']}" + (" ✓" if is_current else ""),
                f"ثيم {emoji}",
                t_data["primary"] if is_current else None,
                theme
            )
            buttons.append(btn)
        
        theme_buttons.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": buttons
        })
    
    content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                text_box("🎨 اختر الثيم المفضل", "xl", "#FFFFFF", True, theme)
            ],
            "backgroundColor": theme["primary"],
            "paddingAll": "25px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                text_box(f"الثيم الحالي: {THEMES[current_theme]['name']}", "sm", theme["text2"], theme=theme),
                separator(theme)
            ] + theme_buttons,
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                button("🏠 الرئيسية", "بداية", theme["primary"], theme)
            ],
            "paddingAll": "15px"
        }
    }
    
    return FlexMessage(alt_text="اختيار الثيم", contents=FlexContainer.from_dict(content))


def games_menu(mode="فردي", current_theme="💜"):
def games_menu(mode="فردي", current_theme="💜"):
    """🎮 قائمة الألعاب"""
    theme = get_theme(current_theme)
    
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
            row["contents"].append(button(f"{game['icon']} {game['name']}", game['cmd'], theme=theme))
        game_buttons.append(row)
    
    content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                text_box(f"🎮 الألعاب - {mode}", "xl", "#FFFFFF", True, theme)
            ],
            "backgroundColor": theme["primary"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": game_buttons + [
                separator(theme),
                text_box(f"وضع اللعب: {mode}", "xs", theme["text2"], theme=theme)
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                button("🏠 الرئيسية", "بداية", theme["primary"], theme),
                button("🔄 تغيير الوضع", "جماعي" if mode == "فردي" else "فردي", theme=theme)
            ],
            "paddingAll": "15px"
        }
    }
    
    return FlexMessage(alt_text="قائمة الألعاب", contents=FlexContainer.from_dict(content))


def game_question(game_name, question, round_num, total_rounds, mode="فردي", current_theme="💜"):
    """❓ سؤال اللعبة"""
    theme = get_theme(current_theme)
    
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
                        text_box(f"🎮 {game_name}", "lg", "#FFFFFF", True, theme),
                        text_box(f"{round_num}/{total_rounds}", "md", "#FFFFFF", theme=theme)
                    ]
                },
                text_box(f"وضع: {mode}", "xs", "#FFFFFF", theme=theme)
            ],
            "backgroundColor": theme["primary"],
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
                        text_box("❓ السؤال:", "sm", theme["text2"], True, theme),
                        text_box(question, "xl", theme["primary"], True, theme)
                    ],
                    "backgroundColor": theme["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "25px"
                },
                text_box("💡 اكتب إجابتك في الدردشة", "xs", theme["text2"], theme=theme)
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
                        button("💡 تلميح", "تلميح", theme=theme),
                        button("👁️ إجابة", "اجابة", theme=theme)
                    ]
                },
                button("⛔ إيقاف", "ايقاف", theme["error"], theme)
            ],
            "paddingAll": "15px"
        }
    }
    
    return FlexMessage(alt_text=f"{game_name} - سؤال {round_num}", contents=FlexContainer.from_dict(content))


def game_result(winner_name, winner_points, all_players, mode="فردي", current_theme="💜"):
    """🏆 نتيجة اللعبة"""
    theme = get_theme(current_theme)
    
    # قائمة اللاعبين
    players_list = []
    for i, (name, points) in enumerate(all_players[:5], 1):
        medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i-1]
        players_list.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                text_box(f"{medal} {name}", "sm", theme["text"], theme=theme),
                text_box(f"{points} نقطة", "sm", theme["primary"], True, theme)
            ],
            "backgroundColor": theme["card"] if i == 1 else "transparent",
            "cornerRadius": "10px",
            "paddingAll": "10px"
        })
    
    content = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                text_box("🎉 انتهت اللعبة!", "xxl", "#FFFFFF", True, theme)
            ],
            "backgroundColor": theme["success"],
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
                        text_box("🏆 الفائز", "sm", theme["text2"], theme=theme),
                        text_box(winner_name, "xxl", theme["primary"], True, theme),
                        text_box(f"{winner_points} نقطة", "lg", theme["success"], True, theme)
                    ],
                    "backgroundColor": theme["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "25px"
                },
                separator(theme),
                text_box("📊 جميع اللاعبين:", "sm", theme["text"], True, theme)
            ] + players_list,
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                button("🔄 لعب مرة أخرى", "العاب", theme["primary"], theme),
                button("🏠 الرئيسية", "بداية", theme=theme)
            ],
            "paddingAll": "15px"
        }
    }
    
    return FlexMessage(alt_text="نتيجة اللعبة", contents=FlexContainer.from_dict(content))


def leaderboard(top_players, current_theme="💜"):
    """🏆 لوحة الصدارة"""
    theme = get_theme(current_theme)
    medals = ["🥇", "🥈", "🥉"]
    
    # قائمة اللاعبين
    players_list = []
    for i, (name, points) in enumerate(top_players[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        bg = theme["card"] if i <= 3 else "transparent"
        
        players_list.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                text_box(medal, "lg", theme["primary"], True, theme),
                text_box(name, "md", theme["text"], theme=theme),
                text_box(str(points), "md", theme["success"], True, theme)
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
                text_box("🏆 لوحة الصدارة", "xxl", "#FFFFFF", True, theme),
                text_box("أفضل 10 لاعبين", "sm", "#FFFFFF", theme=theme)
            ],
            "backgroundColor": theme["primary"],
            "paddingAll": "25px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": players_list if players_list else [
                text_box("لا يوجد لاعبون بعد", "md", theme["text2"], theme=theme)
            ],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                button("🏠 الرئيسية", "بداية", theme["primary"], theme)
            ],
            "paddingAll": "15px"
        }
    }
    
    return FlexMessage(alt_text="لوحة الصدارة", contents=FlexContainer.from_dict(content))
