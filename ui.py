"""
UI Builder - Bot Mesh v7.0 - FIXED VERSION
واجهة رسائل LINE (Flex Messages)
اللغة: العربية فقط
"""

from linebot.v3.messaging import (
    FlexMessage, FlexContainer, TextMessage
)

class UI:
    """
    UI builder لبوت Bot Mesh
    يوفر واجهات Flex Messages احترافية
    """

    # ثيمات (أسماء عربية، ألوان HEX)
    THEMES = {
        "أسود":    {"primary": "#60A5FA", "secondary": "#818CF8", "bg": "#0F172A", "card": "#1E293B", "text": "#F1F5F9", "text2": "#CBD5E1", "success": "#34D399", "error": "#F87171"},
        "أبيض":    {"primary": "#0EA5E9", "secondary": "#38BDF8", "bg": "#FFFFFF", "card": "#F8FAFC", "text": "#0F172A", "text2": "#64748B", "success": "#10B981", "error": "#EF4444"},
        "رمادي":   {"primary": "#6B7280", "secondary": "#9CA3AF", "bg": "#F9FAFB", "card": "#E5E7EB", "text": "#111827", "text2": "#4B5563", "success": "#10B981", "error": "#EF4444"},
        "أزرق":    {"primary": "#0EA5E9", "secondary": "#38BDF8", "bg": "#F0F9FF", "card": "#E0F2FE", "text": "#0C4A6E", "text2": "#075985", "success": "#10B981", "error": "#EF4444"},
        "بنفسجي":  {"primary": "#A78BFA", "secondary": "#C4B5FD", "bg": "#FAF5FF", "card": "#F3E8FF", "text": "#5B21B6", "text2": "#7C3AED", "success": "#10B981", "error": "#EF4444"},
        "وردي":    {"primary": "#EC4899", "secondary": "#F472B6", "bg": "#FFF1F2", "card": "#FFE4EC", "text": "#831843", "text2": "#9D174D", "success": "#10B981", "error": "#EF4444"},
        "أصفر":    {"primary": "#F59E0B", "secondary": "#FBBF24", "bg": "#FFFBEB", "card": "#FEF3C7", "text": "#92400E", "text2": "#B45309", "success": "#10B981", "error": "#EF4444"},
        "أخضر":    {"primary": "#10B981", "secondary": "#34D399", "bg": "#F0FDF4", "card": "#D1FAE5", "text": "#064E3B", "text2": "#065F46", "success": "#059669", "error": "#EF4444"},
        "بني":     {"primary": "#7C2D12", "secondary": "#B45309", "bg": "#FFFBEB", "card": "#FEF3C7", "text": "#3B1F0F", "text2": "#7C2D12", "success": "#10B981", "error": "#EF4444"}
    }

    # ترتيب الألعاب
    GAMES_ORDERED = [
        "ذكاء", "رياضيات", "سرعة", "كلمات", "ألوان", "أضداد",
        "سلسلة", "تخمين", "أغنية", "ترتيب", "تكوين", "إنسان حيوان", "توافق"
    ]

    def _separator(self, color):
        return {"type": "separator", "margin": "lg", "color": color}

    def _create_button(self, label, text, color):
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": "primary",
            "color": color,
            "height": "sm"
        }

    # الصفحة الرئيسية
    def build_home(self, username: str, points: int, theme_name: str = "أزرق") -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "paddingAll": "20px",
                "contents": [
                    {
                        "type": "text",
                        "text": "🎮 Bot Mesh",
                        "size": "xl",
                        "weight": "bold",
                        "color": theme["primary"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"مرحباً {username}",
                        "size": "md",
                        "color": theme["text"],
                        "align": "center",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"⭐ النقاط: {points}",
                        "size": "sm",
                        "color": theme["text2"],
                        "align": "center",
                        "margin": "sm"
                    },
                    self._separator(theme["text2"]),
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._create_button("🎯 ألعاب", "العاب", theme["primary"]),
                            self._create_button("📊 نقاطي", "نقاطي", theme["secondary"])
                        ],
                        "spacing": "sm",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._create_button("🏆 صدارة", "صدارة", theme["secondary"]),
                            self._create_button("❓ مساعدة", "مساعدة", theme["secondary"])
                        ],
                        "spacing": "sm",
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": "© 2025 Abeer Aldosari",
                        "size": "xxs",
                        "color": theme["text2"],
                        "align": "center",
                        "margin": "lg"
                    }
                ]
            }
        }
        return FlexMessage(
            alt_text="البداية - Bot Mesh",
            contents=FlexContainer.from_dict(bubble)
        )

    # قائمة الألعاب
    def build_games_menu(self, theme_name: str = "أزرق") -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        
        contents = [
            {
                "type": "text",
                "text": "🎯 قائمة الألعاب",
                "size": "xl",
                "weight": "bold",
                "color": theme["primary"],
                "align": "center"
            },
            self._separator(theme["text2"])
        ]

        # إضافة أزرار الألعاب (صفين في كل صف)
        for i in range(0, len(self.GAMES_ORDERED), 2):
            row_games = self.GAMES_ORDERED[i:i+2]
            row_contents = []
            for game in row_games:
                row_contents.append(
                    self._create_button(game, f"لعبة {game}", theme["primary"])
                )
            
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": row_contents,
                "spacing": "sm",
                "margin": "sm"
            })

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "paddingAll": "20px",
                "contents": contents
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💡 اختر لعبة للبدء",
                        "size": "xs",
                        "color": theme["text2"],
                        "align": "center"
                    }
                ],
                "paddingAll": "12px",
                "backgroundColor": theme["bg"]
            }
        }
        
        return FlexMessage(
            alt_text="قائمة الألعاب - Bot Mesh",
            contents=FlexContainer.from_dict(bubble)
        )

    # إحصائيات المستخدم
    def build_user_stats(self, username: str, stats: dict, rank: int, theme_name: str = "أزرق") -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "paddingAll": "20px",
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
                        "color": theme["text"],
                        "align": "center",
                        "margin": "sm"
                    },
                    self._separator(theme["text2"]),
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"⭐ {stats.get('points', 0)}",
                                "size": "xxl",
                                "weight": "bold",
                                "color": theme["primary"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": "النقاط الإجمالية",
                                "size": "xs",
                                "color": theme["text2"],
                                "align": "center"
                            }
                        ],
                        "backgroundColor": theme["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "20px",
                        "margin": "md"
                    },
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
                                        "text": str(stats.get('games_played', 0)),
                                        "size": "lg",
                                        "weight": "bold",
                                        "color": theme["text"],
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "ألعاب",
                                        "size": "xs",
                                        "color": theme["text2"],
                                        "align": "center"
                                    }
                                ],
                                "flex": 1
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": str(stats.get('wins', 0)),
                                        "size": "lg",
                                        "weight": "bold",
                                        "color": theme["success"],
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "فوز",
                                        "size": "xs",
                                        "color": theme["text2"],
                                        "align": "center"
                                    }
                                ],
                                "flex": 1
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"#{rank}",
                                        "size": "lg",
                                        "weight": "bold",
                                        "color": theme["primary"],
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "ترتيب",
                                        "size": "xs",
                                        "color": theme["text2"],
                                        "align": "center"
                                    }
                                ],
                                "flex": 1
                            }
                        ],
                        "spacing": "md",
                        "margin": "lg"
                    }
                ]
            }
        }
        
        return FlexMessage(
            alt_text="نقاطي - Bot Mesh",
            contents=FlexContainer.from_dict(bubble)
        )

    # لوحة الصدارة
    def build_leaderboard(self, top_users: list, theme_name: str = "أزرق") -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        
        contents = [
            {
                "type": "text",
                "text": "🏆 لوحة الصدارة",
                "size": "xl",
                "weight": "bold",
                "color": theme["primary"],
                "align": "center"
            },
            self._separator(theme["text2"])
        ]
        
        medals = ["🥇", "🥈", "🥉"]
        
        for i, user in enumerate(top_users[:10], 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": medal,
                        "size": "md",
                        "color": theme["primary"],
                        "flex": 0,
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": user.get("display_name", "مستخدم"),
                        "size": "sm",
                        "color": theme["text"],
                        "flex": 3,
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": str(user.get("points", 0)),
                        "size": "sm",
                        "color": theme["primary"],
                        "flex": 1,
                        "align": "end",
                        "weight": "bold"
                    }
                ],
                "paddingAll": "12px",
                "margin": "sm",
                "backgroundColor": theme["card"] if i <= 3 else "transparent",
                "cornerRadius": "12px"
            })
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "paddingAll": "20px",
                "contents": contents
            }
        }
        
        return FlexMessage(
            alt_text="لوحة الصدارة - Bot Mesh",
            contents=FlexContainer.from_dict(bubble)
        )

    # سؤال اللعبة
    def build_game_question(
        self,
        game_name: str,
        question: str,
        round_num: int,
        total_rounds: int,
        theme_name: str = "أزرق"
    ) -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        
        bubble = {
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
                            {
                                "type": "text",
                                "text": f"🎮 {game_name}",
                                "size": "lg",
                                "weight": "bold",
                                "color": theme["text"],
                                "flex": 3
                            },
                            {
                                "type": "text",
                                "text": f"{round_num}/{total_rounds}",
                                "size": "sm",
                                "color": theme["text2"],
                                "align": "end",
                                "flex": 1
                            }
                        ]
                    }
                ],
                "backgroundColor": theme["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
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
                        "cornerRadius": "15px",
                        "paddingAll": "20px"
                    }
                ],
                "backgroundColor": theme["bg"],
                "paddingAll": "15px"
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
                            self._create_button("💡 تلميح", "لمح", theme["secondary"]),
                            self._create_button("⛔ إيقاف", "إيقاف", theme["error"])
                        ]
                    }
                ],
                "backgroundColor": theme["bg"],
                "paddingAll": "15px"
            }
        }
        
        return FlexMessage(
            alt_text=f"{game_name} - سؤال {round_num}",
            contents=FlexContainer.from_dict(bubble)
        )

    # نتيجة اللعبة
    def build_game_result(
        self,
        game_name: str,
        total_points: int,
        theme_name: str = "أزرق"
    ) -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "paddingAll": "20px",
                "contents": [
                    {
                        "type": "text",
                        "text": "🎉 انتهت اللعبة",
                        "size": "xl",
                        "weight": "bold",
                        "color": theme["primary"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": game_name,
                        "size": "md",
                        "color": theme["text"],
                        "align": "center",
                        "margin": "sm"
                    },
                    self._separator(theme["text2"]),
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"⭐ {total_points}",
                                "size": "xxl",
                                "weight": "bold",
                                "color": theme["success"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": "نقطة",
                                "size": "sm",
                                "color": theme["text2"],
                                "align": "center"
                            }
                        ],
                        "backgroundColor": theme["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "25px",
                        "margin": "lg"
                    }
                ]
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
                            self._create_button("🔄 إعادة", f"لعبة {game_name}", theme["primary"]),
                            self._create_button("🎯 ألعاب", "العاب", theme["secondary"])
                        ]
                    }
                ],
                "backgroundColor": theme["bg"],
                "paddingAll": "15px"
            }
        }
        
        return FlexMessage(
            alt_text="النتيجة - Bot Mesh",
            contents=FlexContainer.from_dict(bubble)
        )

    # المساعدة
    def build_help(self, theme_name: str = "أزرق") -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "paddingAll": "20px",
                "contents": [
                    {
                        "type": "text",
                        "text": "❓ دليل الاستخدام",
                        "size": "xl",
                        "weight": "bold",
                        "color": theme["primary"],
                        "align": "center"
                    },
                    self._separator(theme["text2"]),
                    {
                        "type": "text",
                        "text": "الأوامر الأساسية:",
                        "size": "md",
                        "weight": "bold",
                        "color": theme["text"],
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "• بداية - الصفحة الرئيسية\n• العاب - قائمة الألعاب\n• نقاطي - إحصائياتك\n• صدارة - لوحة الصدارة\n• لعبة [اسم] - بدء لعبة",
                        "size": "sm",
                        "wrap": True,
                        "color": theme["text2"],
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": "أثناء اللعب:",
                        "size": "md",
                        "weight": "bold",
                        "color": theme["text"],
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "• لمح - الحصول على تلميح\n• إيقاف - إيقاف اللعبة الحالية",
                        "size": "sm",
                        "wrap": True,
                        "color": theme["text2"],
                        "margin": "sm"
                    }
                ]
            }
        }
        
        return FlexMessage(
            alt_text="مساعدة - Bot Mesh",
            contents=FlexContainer.from_dict(bubble)
        )
