"""
🎨 Bot Mesh v7.0 - UI Builder
بناء واجهات المستخدم الاحترافية
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage

class UI:
    """بناء واجهات Flex Messages احترافية"""
    
    # الثيمات التسعة
    THEMES = {
        "💜": {
            "name": "Purple Dream",
            "primary": "#8B5CF6",
            "secondary": "#A78BFA",
            "bg": "#FAF5FF",
            "card": "#F3E8FF",
            "text": "#1F2937",
            "text2": "#6B7280"
        },
        "💚": {
            "name": "Green Nature",
            "primary": "#10B981",
            "secondary": "#34D399",
            "bg": "#F0FDF4",
            "card": "#D1FAE5",
            "text": "#1F2937",
            "text2": "#6B7280"
        },
        "🤍": {
            "name": "Clean White",
            "primary": "#3B82F6",
            "secondary": "#60A5FA",
            "bg": "#FFFFFF",
            "card": "#F3F4F6",
            "text": "#1F2937",
            "text2": "#6B7280"
        },
        "🖤": {
            "name": "Dark Elegance",
            "primary": "#8B5CF6",
            "secondary": "#A78BFA",
            "bg": "#1F2937",
            "card": "#374151",
            "text": "#F9FAFB",
            "text2": "#D1D5DB"
        },
        "💙": {
            "name": "Ocean Blue",
            "primary": "#0EA5E9",
            "secondary": "#38BDF8",
    "bg": "#F0F9FF",
        "card": "#E0F2FE",
        "text": "#0C4A6E",
        "text2": "#075985"
    },
    "🩶": {
        "name": "Silver Gray",
        "primary": "#6B7280",
        "secondary": "#9CA3AF",
        "bg": "#F9FAFB",
        "card": "#E5E7EB",
        "text": "#1F2937",
        "text2": "#6B7280"
    },
    "🩷": {
        "name": "Pink Blossom",
        "primary": "#EC4899",
        "secondary": "#F472B6",
        "bg": "#FDF2F8",
        "card": "#FCE7F3",
        "text": "#831843",
        "text2": "#9D174D"
    },
    "🧡": {
        "name": "Warm Sunset",
        "primary": "#F97316",
        "secondary": "#FB923C",
        "bg": "#FFF7ED",
        "card": "#FFEDD5",
        "text": "#7C2D12",
        "text2": "#9A3412"
    },
    "🤎": {
        "name": "Earth Brown",
        "primary": "#92400E",
        "secondary": "#B45309",
        "bg": "#FFFBEB",
        "card": "#FEF3C7",
        "text": "#451A03",
        "text2": "#78350F"
    }
}

def get_theme(self, emoji: str = "💜") -> dict:
    """الحصول على ألوان الثيم"""
    return self.THEMES.get(emoji, self.THEMES["💜"])

# ========================================================================
# Helper Methods
# ========================================================================

def _create_button(self, label: str, text: str, color: str = None) -> dict:
    """إنشاء زر"""
    button = {
        "type": "button",
        "action": {
            "type": "message",
            "label": label,
            "text": text
        },
        "style": "primary",
        "height": "sm"
    }
    
    if color:
        button["color"] = color
    
    return button

def _create_separator(self, theme: dict) -> dict:
    """إنشاء خط فاصل"""
    return {
        "type": "separator",
        "margin": "lg",
        "color": theme["text2"]
    }

# ========================================================================
# Main Pages
# ========================================================================

def build_home(self, username: str, points: int, theme_emoji: str = "💜") -> FlexMessage:
    """بناء الصفحة الرئيسية"""
    theme = self.get_theme(theme_emoji)
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎮 Bot Mesh",
                    "size": "xxl",
                    "weight": "bold",
                    "color": theme["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "بوت الألعاب الترفيهية",
                    "size": "sm",
                    "color": theme["text2"],
                    "align": "center",
                    "margin": "sm"
                },
                self._create_separator(theme),
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "👤",
                                    "size": "xl",
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": username,
                                    "size": "md",
                                    "weight": "bold",
                                    "color": theme["text"],
                                    "align": "center",
                                    "wrap": True
                                }
                            ],
                            "flex": 1
                        },
                        {
                            "type": "separator"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "⭐",
                                    "size": "xl",
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": str(points),
                                    "size": "md",
                                    "weight": "bold",
                                    "color": theme["primary"],
                                    "align": "center"
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "backgroundColor": theme["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "20px",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "🎨 اختر ثيمك المفضل",
                    "size": "md",
                    "weight": "bold",
                    "color": theme["text"],
                    "align": "center",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        self._create_button(emoji, f"ثيم {emoji}", theme["primary"])
                        for emoji in ["💜", "💚", "🤍"]
                    ],
                    "spacing": "sm",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        self._create_button(emoji, f"ثيم {emoji}", theme["primary"])
                        for emoji in ["🖤", "💙", "🩶"]
                    ],
                    "spacing": "sm",
                    "margin": "sm"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        self._create_button(emoji, f"ثيم {emoji}", theme["primary"])
                        for emoji in ["🩷", "🧡", "🤎"]
                    ],
                    "spacing": "sm",
                    "margin": "sm"
                }
            ],
            "backgroundColor": theme["bg"],
            "paddingAll": "25px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        self._create_button("🎮 الألعاب", "العاب", theme["primary"]),
                        self._create_button("📊 نقاطي", "نقاطي", theme["secondary"])
                    ],
                    "spacing": "sm"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        self._create_button("🏆 الصدارة", "صدارة", theme["secondary"]),
                        self._create_button("ℹ️ مساعدة", "مساعدة", theme["secondary"])
                    ],
                    "spacing": "sm",
                    "margin": "sm"
                },
                self._create_separator(theme),
                {
                    "type": "text",
                    "text": "© 2025 by Abeer Aldosari",
                    "size": "xs",
                    "color": theme["text2"],
                    "align": "center"
                }
            ],
            "backgroundColor": theme["bg"],
            "paddingAll": "20px"
        }
    }
    
    return FlexMessage(
        alt_text="🎮 Bot Mesh - البداية",
        contents=FlexContainer.from_dict(bubble)
    )

def build_games_menu(self, theme_emoji: str = "💜") -> FlexMessage:
    """بناء قائمة الألعاب"""
    theme = self.get_theme(theme_emoji)
    
    games = [
        {"emoji": "🧠", "name": "ذكاء"},
        {"emoji": "🔢", "name": "رياضيات"},
        {"emoji": "⚡", "name": "سرعة"},
        {"emoji": "🔤", "name": "كلمات"},
        {"emoji": "🎨", "name": "ألوان"},
        {"emoji": "↔️", "name": "أضداد"},
        {"emoji": "🔗", "name": "سلسلة"},
        {"emoji": "🔮", "name": "تخمين"},
        {"emoji": "🎵", "name": "أغنية"},
        {"emoji": "🎯", "name": "إنسان حيوان"},
        {"emoji": "💕", "name": "توافق"},
        {"emoji": "📝", "name": "تكوين"}
    ]
    
    game_buttons = []
    for i in range(0, len(games), 2):
        row = games[i:i+2]
        game_buttons.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                self._create_button(
                    f"{g['emoji']} {g['name']}",
                    f"لعبة {g['name']}",
                    theme["primary"]
                )
                for g in row
            ],
            "spacing": "sm",
            "margin": "sm"
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎮 الألعاب المتاحة",
                    "size": "xl",
                    "weight": "bold",
                    "color": theme["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"{len(games)} لعبة مختلفة",
                    "size": "sm",
                    "color": theme["text2"],
                    "align": "center",
                    "margin": "sm"
                },
                self._create_separator(theme)
            ] + game_buttons,
            "backgroundColor": theme["bg"],
            "paddingAll": "25px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        self._create_button("🏠 البداية", "بداية", theme["primary"]),
                        self._create_button("⛔ إيقاف", "ايقاف", theme["secondary"])
                    ],
                    "spacing": "sm"
                }
            ],
            "backgroundColor": theme["bg"],
            "paddingAll": "20px"
        }
    }
    
    return FlexMessage(
        alt_text="🎮 الألعاب المتاحة",
        contents=FlexContainer.from_dict(bubble)
    )

def build_user_stats(self, username: str, stats: dict, rank: int, theme_emoji: str = "💜") -> FlexMessage:
    """بناء صفحة الإحصائيات"""
    theme = self.get_theme(theme_emoji)
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "📊 إحصائياتك",
                    "size": "xl",
                    "weight": "bold",
                    "color": theme["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": username,
                    "size": "md",
                    "color": theme["text2"],
                    "align": "center",
                    "margin": "sm"
                },
                self._create_separator(theme),
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "⭐ النقاط",
                            "size": "sm",
                            "color": theme["text2"],
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": str(stats['points']),
                            "size": "xxl",
                            "weight": "bold",
                            "color": theme["primary"],
                            "align": "center"
                        }
                    ],
                    "backgroundColor": theme["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "20px",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "🎮", "size": "lg", "align": "center"},
                                {"type": "text", "text": str(stats['games_played']), "size": "lg", "weight": "bold", "color": theme["text"], "align": "center"},
                                {"type": "text", "text": "ألعاب", "size": "xs", "color": theme["text2"], "align": "center"}
                            ],
                            "flex": 1
                        },
                        {"type": "separator"},
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "🏆", "size": "lg", "align": "center"},
                                {"type": "text", "text": str(stats['wins']), "size": "lg", "weight": "bold", "color": theme["text"], "align": "center"},
                                {"type": "text", "text": "فوز", "size": "xs", "color": theme["text2"], "align": "center"}
                            ],
                            "flex": 1
                        },
                        {"type": "separator"},
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "🎖️", "size": "lg", "align": "center"},
                                {"type": "text", "text": f"#{rank}", "size": "lg", "weight": "bold", "color": theme["text"], "align": "center"},
                                {"type": "text", "text": "ترتيب", "size": "xs", "color": theme["text2"], "align": "center"}
                            ],
                            "flex": 1
                        }
                    ],
                    "backgroundColor": theme["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "15px",
                    "margin": "md"
                }
            ],
            "backgroundColor": theme["bg"],
            "paddingAll": "25px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                self._create_button("🏠 البداية", "بداية", theme["primary"])
            ],
            "backgroundColor": theme["bg"],
            "paddingAll": "20px"
        }
    }
    
    return FlexMessage(
        alt_text="📊 إحصائياتك",
        contents=FlexContainer.from_dict(bubble)
    )

def build_leaderboard(self, top_users: list, theme_emoji: str = "💜") -> FlexMessage:
    """بناء لوحة الصدارة"""
    theme = self.get_theme(theme_emoji)
    medals = ["🥇", "🥈", "🥉"]
    
    players_list = []
    for i, user in enumerate(top_users[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        
        players_list.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": medal, "size": "md", "flex": 0, "color": theme["primary"]},
                {"type": "text", "text": user['name'], "size": "sm", "color": theme["text"], "flex": 2, "wrap": True},
                {"type": "text", "text": str(user['points']), "size": "sm", "weight": "bold", "color": theme["primary"], "align": "end", "flex": 1}
            ],
            "spacing": "md",
            "paddingAll": "12px",
            "backgroundColor": theme["card"] if i <= 3 else "transparent",
            "cornerRadius": "15px",
            "margin": "sm"
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🏆 لوحة الصدارة",
                    "size": "xl",
                    "weight": "bold",
                    "color": theme["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "أفضل 10 لاعبين",
                    "size": "sm",
                    "color": theme["text2"],
                    "align": "center",
                    "margin": "sm"
                },
                self._create_separator(theme)
            ] + players_list,
            "backgroundColor": theme["bg"],
            "paddingAll": "25px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                self._create_button("🏠 البداية", "بداية", theme["primary"])
            ],
            "backgroundColor": theme["bg"],
            "paddingAll": "20px"
        }
    }
    
    return FlexMessage(
        alt_text="🏆 لوحة الصدارة",
        contents=FlexContainer.from_dict(bubble)
    )

def build_game_question(self, game_name: str, question: str, round_num: int, total_rounds: int, theme_emoji: str = "💜", message: str = None) -> FlexMessage:
    """بناء نافذة السؤال"""
    theme = self.get_theme(theme_emoji)
    
    contents = []
    
    # إضافة رسالة إضافية إن وجدت
    if message:
        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": message,
                    "size": "sm",
                    "color": theme["primary"],
                    "weight": "bold",
                    "align": "center",
                    "wrap": True
                }
            ],
            "backgroundColor": theme["card"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "margin": "md"
        })
    
    contents.extend([
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": f"🎮 {game_name}", "size": "lg", "weight": "bold", "color": theme["primary"], "flex": 2},
                {"type": "text", "text": f"{round_num}/{total_rounds}", "size": "md", "color": theme["text2"], "align": "end", "flex": 1}
            ]
        },
        self._create_separator(theme),
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": question,
                    "size": "lg",
                    "weight": "bold",
                    "color": theme["text"],
                    "align": "center",
                    "wrap": True
                }
            ],
            "backgroundColor": theme["card"],
            "cornerRadius": "20px",
            "paddingAll": "20px",
            "margin": "lg"
        }
    ])
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": theme["bg"],
            "paddingAll": "25px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        self._create_button("💡 تلميح", "لمح", theme["secondary"]),
                        self._create_button("⛔ إيقاف", "ايقاف", theme["secondary"])
                    ],
                    "spacing": "sm"
                }
            ],
            "backgroundColor": theme["bg"],
            "paddingAll": "20px"
        }
    }
    
    return FlexMessage(
        alt_text=f"🎮 {game_name}",
        contents=FlexContainer.from_dict(bubble)
    )

def build_game_result(self, game_name: str, total_points: int, theme_emoji: str = "💜") -> FlexMessage:
    """بناء نتيجة اللعبة"""
    theme = self.get_theme(theme_emoji)
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "🎉", "size": "xxl", "align": "center"},
                        {"type": "text", "text": "انتهت اللعبة!", "size": "xl", "weight": "bold", "color": theme["primary"], "align": "center", "margin": "md"},
                        self._create_separator(theme),
                        {"type": "text", "text": "مجموع نقاطك", "size": "sm", "color": theme["text2"], "align": "center", "margin": "md"},
                        {"type": "text", "text": f"⭐ {total_points}", "size": "xxl", "weight": "bold", "color": theme["primary"], "align": "center"}
                    ],
                    "backgroundColor": theme["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "25px"
                }
            ],
            "backgroundColor": theme["bg"],
            "paddingAll": "25px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        self._create_button(f"🔄 {game_name}", f"لعبة {game_name}", theme["primary"]),
                        self._create_button("🎮 الألعاب", "العاب", theme["secondary"])
                    ],
                    "spacing": "sm"
                }
            ],
            "backgroundColor": theme["bg"],
            "paddingAll": "20px"
        }
    }
    
    return FlexMessage(
        alt_text="🎉 نتيجة اللعبة",
        contents=FlexContainer.from_dict(bubble)
    )
