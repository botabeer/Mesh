"""
🎨 Bot Mesh v6.0 - Glassmorphic UI Builder
Created by: Abeer Aldosari © 2025

✨ تصميم Glass Morphism ثلاثي الأبعاد:
- شفافية وانعكاسات زجاجية
- ظلال وإضاءات متدرجة
- ألوان متناسقة مع تدرجات
- أزرار بارزة وسهلة اللمس
"""

from linebot.v3.messaging import FlexMessage, FlexContainer

class UIBuilder:
    """بناء واجهات Flex احترافية"""
    
    # الثيمات التسعة المحسّنة مع Glass Effect
    THEMES = {
        "🖤": {
            "name": "Dark Elegance",
            "primary": "#8B5CF6",
            "secondary": "#A78BFA",
            "bg": "#1F2937",
            "card": "#374151",
            "text": "#F9FAFB",
            "text_light": "#D1D5DB",
            "glass": "rgba(167, 139, 250, 0.1)",
            "shadow": "rgba(139, 92, 246, 0.3)"
        },
        "🤍": {
            "name": "Pure White",
            "primary": "#3B82F6",
            "secondary": "#60A5FA",
            "bg": "#FFFFFF",
            "card": "#F3F4F6",
            "text": "#1F2937",
            "text_light": "#6B7280",
            "glass": "rgba(96, 165, 250, 0.1)",
            "shadow": "rgba(59, 130, 246, 0.2)"
        },
        "🩶": {
            "name": "Silver Gray",
            "primary": "#6B7280",
            "secondary": "#9CA3AF",
            "bg": "#F9FAFB",
            "card": "#E5E7EB",
            "text": "#1F2937",
            "text_light": "#6B7280",
            "glass": "rgba(156, 163, 175, 0.1)",
            "shadow": "rgba(107, 114, 128, 0.2)"
        },
        "🩷": {
            "name": "Pink Blossom",
            "primary": "#EC4899",
            "secondary": "#F472B6",
            "bg": "#FDF2F8",
            "card": "#FCE7F3",
            "text": "#831843",
            "text_light": "#9D174D",
            "glass": "rgba(244, 114, 182, 0.1)",
            "shadow": "rgba(236, 72, 153, 0.2)"
        },
        "💙": {
            "name": "Ocean Blue",
            "primary": "#0EA5E9",
            "secondary": "#38BDF8",
            "bg": "#F0F9FF",
            "card": "#E0F2FE",
            "text": "#0C4A6E",
            "text_light": "#075985",
            "glass": "rgba(56, 189, 248, 0.1)",
            "shadow": "rgba(14, 165, 233, 0.2)"
        },
        "🤎": {
            "name": "Earth Brown",
            "primary": "#92400E",
            "secondary": "#B45309",
            "bg": "#FFFBEB",
            "card": "#FEF3C7",
            "text": "#451A03",
            "text_light": "#78350F",
            "glass": "rgba(180, 83, 9, 0.1)",
            "shadow": "rgba(146, 64, 14, 0.2)"
        },
        "💜": {
            "name": "Purple Dream",
            "primary": "#7C3AED",
            "secondary": "#A78BFA",
            "bg": "#FAF5FF",
            "card": "#F3E8FF",
            "text": "#1F2937",
            "text_light": "#6B7280",
            "glass": "rgba(167, 139, 250, 0.1)",
            "shadow": "rgba(124, 58, 237, 0.2)"
        },
        "💚": {
            "name": "Green Nature",
            "primary": "#10B981",
            "secondary": "#34D399",
            "bg": "#F0FDF4",
            "card": "#D1FAE5",
            "text": "#1F2937",
            "text_light": "#6B7280",
            "glass": "rgba(52, 211, 153, 0.1)",
            "shadow": "rgba(16, 185, 129, 0.2)"
        },
        "💛": {
            "name": "Sunny Yellow",
            "primary": "#EAB308",
            "secondary": "#FCD34D",
            "bg": "#FEFCE8",
            "card": "#FEF9C3",
            "text": "#713F12",
            "text_light": "#854D0E",
            "glass": "rgba(252, 211, 77, 0.1)",
            "shadow": "rgba(234, 179, 8, 0.2)"
        }
    }
    
    DEFAULT_THEME = "💜"
    
    def __init__(self):
        """تهيئة البناء"""
        self.current_theme = self.DEFAULT_THEME
    
    def get_theme(self, emoji: str = None) -> dict:
        """الحصول على ألوان الثيم"""
        if emoji:
            self.current_theme = emoji
        return self.THEMES.get(self.current_theme, self.THEMES[self.DEFAULT_THEME])
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def create_glass_card(self, contents: list, theme: dict) -> dict:
        """إنشاء بطاقة زجاجية ثلاثية الأبعاد"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": theme["card"],
            "cornerRadius": "25px",
            "paddingAll": "25px",
            "spacing": "md"
        }
    
    def create_button(self, label: str, text: str, theme: dict, primary: bool = False) -> dict:
        """إنشاء زر زجاجي محسّن"""
        return {
            "type": "button",
            "action": {
                "type": "message",
                "label": label,
                "text": text
            },
            "style": "primary" if primary else "secondary",
            "color": theme["primary"] if primary else theme["secondary"],
            "height": "md",
            "adjustMode": "shrink-to-fit"
        }
    
    def create_header(self, title: str, subtitle: str = None, theme: dict = None) -> dict:
        """إنشاء رأس زجاجي"""
        if not theme:
            theme = self.get_theme()
        
        contents = [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "size": "xxl",
                "color": theme["primary"],
                "align": "center"
            }
        ]
        
        if subtitle:
            contents.append({
                "type": "text",
                "text": subtitle,
                "size": "sm",
                "color": theme["text_light"],
                "align": "center",
                "margin": "sm"
            })
        
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "spacing": "xs"
        }
    
    def create_separator(self, theme: dict) -> dict:
        """إنشاء خط فاصل"""
        return {
            "type": "separator",
            "color": theme["text_light"],
            "margin": "lg"
        }
    
    # ========================================================================
    # Main Pages
    # ========================================================================
    
    def build_home(self, username: str, points: int, theme_emoji: str = None) -> FlexMessage:
        """بناء الصفحة الرئيسية"""
        theme = self.get_theme(theme_emoji)
        
        # بطاقة المستخدم
        user_card = self.create_glass_card([
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
                                "text": "👤 اللاعب",
                                "size": "xs",
                                "color": theme["text_light"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": username,
                                "size": "xl",
                                "weight": "bold",
                                "color": theme["text"],
                                "align": "center",
                                "wrap": True
                            }
                        ],
                        "flex": 1
                    },
                    {
                        "type": "separator",
                        "color": theme["text_light"]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "⭐ النقاط",
                                "size": "xs",
                                "color": theme["text_light"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": str(points),
                                "size": "xl",
                                "weight": "bold",
                                "color": theme["primary"],
                                "align": "center"
                            }
                        ],
                        "flex": 1
                    }
                ],
                "spacing": "lg"
            }
        ], theme)
        
        # اختيار الثيم - الثيمات التسعة
        theme_selector = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎨 اختر ثيمك المفضل",
                    "size": "md",
                    "weight": "bold",
                    "color": theme["text"],
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        self.create_button(emoji, f"ثيم {emoji}", theme, emoji == self.current_theme)
                        for emoji in ["🖤", "🤍", "🩶"]
                    ],
                    "spacing": "sm",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        self.create_button(emoji, f"ثيم {emoji}", theme, emoji == self.current_theme)
                        for emoji in ["🩷", "💙", "🤎"]
                    ],
                    "spacing": "sm",
                    "margin": "sm"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        self.create_button(emoji, f"ثيم {emoji}", theme, emoji == self.current_theme)
                        for emoji in ["💜", "💚", "💛"]
                    ],
                    "spacing": "sm",
                    "margin": "sm"
                }
            ],
            "spacing": "md"
        }
        
        # المحتوى الرئيسي
        body_contents = [
            self.create_header("🎮 Bot Mesh", "بوت الألعاب الترفيهية", theme),
            self.create_separator(theme),
            user_card,
            theme_selector
        ]
        
        # الأزرار السفلية
        footer_contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self.create_button("🎮 ابدأ اللعب", "العاب", theme, True),
                    self.create_button("📊 نقاطي", "نقاطي", theme)
                ],
                "spacing": "sm"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self.create_button("🏆 الصدارة", "صدارة", theme),
                    self.create_button("ℹ️ المساعدة", "مساعدة", theme)
                ],
                "spacing": "sm",
                "margin": "sm"
            },
            self.create_separator(theme),
            {
                "type": "text",
                "text": "© 2025 by Abeer Aldosari",
                "size": "xs",
                "color": theme["text_light"],
                "align": "center"
            }
        ]
        
        # بناء البطاقة النهائية
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": body_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "25px",
                "spacing": "lg"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": footer_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "20px",
                "spacing": "sm"
            }
        }
        
        return FlexMessage(
            alt_text="🎮 Bot Mesh - البداية",
            contents=FlexContainer.from_dict(bubble)
        )
    
    def build_games_menu(self, theme_emoji: str = None) -> FlexMessage:
        """بناء قائمة الألعاب"""
        theme = self.get_theme(theme_emoji)
        
        # قائمة الألعاب
        games = [
            {"icon": "🧠", "name": "ذكاء", "desc": "ألغاز وأحاجي"},
            {"icon": "🔢", "name": "رياضيات", "desc": "حساب سريع"},
            {"icon": "⚡", "name": "سرعة", "desc": "كتابة سريعة"},
            {"icon": "🔤", "name": "كلمات", "desc": "ترتيب حروف"},
            {"icon": "🎨", "name": "ألوان", "desc": "تحدي الألوان"},
            {"icon": "↔️", "name": "أضداد", "desc": "عكس الكلمة"}
        ]
        
        # بناء أزرار الألعاب
        game_buttons = []
        for i in range(0, len(games), 2):
            row_games = games[i:i+2]
            buttons = [
                self.create_button(
                    f"{g['icon']} {g['name']}",
                    f"لعبة {g['name']}",
                    theme,
                    True
                )
                for g in row_games
            ]
            
            game_buttons.append({
                "type": "box",
                "layout": "horizontal",
                "contents": buttons,
                "spacing": "sm",
                "margin": "sm"
            })
        
        # المحتوى
        body_contents = [
            self.create_header("🎮 الألعاب المتاحة", f"{len(games)} لعبة مختلفة", theme),
            self.create_separator(theme)
        ] + game_buttons
        
        # الأزرار السفلية
        footer_contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self.create_button("🏠 الرئيسية", "بداية", theme, True),
                    self.create_button("⛔ إيقاف", "ايقاف", theme)
                ],
                "spacing": "sm"
            }
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": body_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "25px",
                "spacing": "md"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": footer_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "20px"
            }
        }
        
        return FlexMessage(
            alt_text="🎮 الألعاب",
            contents=FlexContainer.from_dict(bubble)
        )
    
    def build_user_stats(self, username: str, stats: dict, rank: int, theme_emoji: str = None) -> FlexMessage:
        """بناء صفحة الإحصائيات"""
        theme = self.get_theme(theme_emoji)
        
        # بطاقة النقاط الكبرى
        points_card = self.create_glass_card([
            {
                "type": "text",
                "text": "⭐ النقاط الكلية",
                "size": "sm",
                "color": theme["text_light"],
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
        ], theme)
        
        # إحصائيات إضافية
        stats_grid = self.create_glass_card([
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
                            {"type": "text", "text": "ألعاب", "size": "xs", "color": theme["text_light"], "align": "center"}
                        ],
                        "flex": 1
                    },
                    {"type": "separator", "color": theme["text_light"]},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "🏆", "size": "lg", "align": "center"},
                            {"type": "text", "text": str(stats['wins']), "size": "lg", "weight": "bold", "color": theme["text"], "align": "center"},
                            {"type": "text", "text": "فوز", "size": "xs", "color": theme["text_light"], "align": "center"}
                        ],
                        "flex": 1
                    },
                    {"type": "separator", "color": theme["text_light"]},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "🎖️", "size": "lg", "align": "center"},
                            {"type": "text", "text": f"#{rank}", "size": "lg", "weight": "bold", "color": theme["text"], "align": "center"},
                            {"type": "text", "text": "ترتيب", "size": "xs", "color": theme["text_light"], "align": "center"}
                        ],
                        "flex": 1
                    }
                ],
                "spacing": "md"
            }
        ], theme)
        
        body_contents = [
            self.create_header("📊 إحصائياتك", username, theme),
            self.create_separator(theme),
            points_card,
            stats_grid
        ]
        
        footer_contents = [
            self.create_button("🏠 الرئيسية", "بداية", theme, True)
        ]
        
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": body_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "25px",
                "spacing": "lg"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": footer_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "20px"
            }
        }
        
        return FlexMessage(
            alt_text="📊 نقاطي",
            contents=FlexContainer.from_dict(bubble)
        )
    
    def build_leaderboard(self, top_users: list, theme_emoji: str = None) -> FlexMessage:
        """بناء لوحة الصدارة"""
        theme = self.get_theme(theme_emoji)
        medals = ["🥇", "🥈", "🥉"]
        
        # بناء قائمة اللاعبين
        players_list = []
        for i, user in enumerate(top_users[:10], 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            bg_color = theme["card"] if i <= 3 else "transparent"
            
            players_list.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": medal, "size": "xl", "flex": 0, "color": theme["primary"]},
                    {"type": "text", "text": user['name'], "size": "md", "color": theme["text"], "flex": 2, "wrap": True},
                    {"type": "text", "text": str(user['points']), "size": "md", "weight": "bold", "color": theme["primary"], "align": "end", "flex": 1}
                ],
                "spacing": "md",
                "paddingAll": "15px",
                "backgroundColor": bg_color,
                "cornerRadius": "15px",
                "margin": "sm"
            })
        
        body_contents = [
            self.create_header("🏆 لوحة الصدارة", "أفضل 10 لاعبين", theme),
            self.create_separator(theme)
        ] + players_list
        
        footer_contents = [
            self.create_button("🏠 الرئيسية", "بداية", theme, True)
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": body_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "25px",
                "spacing": "none"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": footer_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "20px"
            }
        }
        
        return FlexMessage(
            alt_text="🏆 الصدارة",
            contents=FlexContainer.from_dict(bubble)
        )
    
    def build_game_question(self, game_name: str, question: str, round_num: int, total_rounds: int, theme_emoji: str = None) -> FlexMessage:
        """بناء نافذة السؤال"""
        theme = self.get_theme(theme_emoji)
        
        # بطاقة السؤال
        question_card = self.create_glass_card([
            {
                "type": "text",
                "text": question,
                "size": "xl",
                "weight": "bold",
                "color": theme["text"],
                "align": "center",
                "wrap": True
            }
        ], theme)
        
        body_contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": f"🎮 {game_name}", "size": "xl", "weight": "bold", "color": theme["primary"], "flex": 2},
                    {"type": "text", "text": f"{round_num}/{total_rounds}", "size": "md", "color": theme["text_light"], "align": "end", "flex": 1}
                ]
            },
            self.create_separator(theme),
            question_card
        ]
        
        footer_contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self.create_button("💡 تلميح", "لمح", theme),
                    self.create_button("⛔ إيقاف", "ايقاف", theme)
                ],
                "spacing": "sm"
            }
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": body_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "25px",
                "spacing": "lg"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": footer_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "20px"
            }
        }
        
        return FlexMessage(
            alt_text=f"🎮 {game_name}",
            contents=FlexContainer.from_dict(bubble)
        )
    
    def build_game_result(self, game_name: str, total_points: int, theme_emoji: str = None) -> FlexMessage:
        """بناء نتيجة اللعبة"""
        theme = self.get_theme(theme_emoji)
        
        result_card = self.create_glass_card([
            {"type": "text", "text": "🎉", "size": "xxl", "align": "center"},
            {"type": "text", "text": "انتهت اللعبة!", "size": "xl", "weight": "bold", "color": theme["primary"], "align": "center"},
            self.create_separator(theme),
            {"type": "text", "text": "مجموع نقاطك", "size": "sm", "color": theme["text_light"], "align": "center"},
            {"type": "text", "text": f"⭐ {total_points}", "size": "xxl", "weight": "bold", "color": theme["primary"], "align": "center"}
        ], theme)
        
        body_contents = [
            result_card
        ]
        
        footer_contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self.create_button(f"🔄 {game_name}", f"لعبة {game_name}", theme, True),
                    self.create_button("🎮 الألعاب", "العاب", theme)
                ],
                "spacing": "sm"
            }
        ]
        
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": body_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "25px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": footer_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "20px"
            }
        }
        
        return FlexMessage(
            alt_text="🎉 نتيجة اللعبة",
            contents=FlexContainer.from_dict(bubble)
        )
    
    def build_correct_answer(self, points_earned: int, next_question: dict, theme_emoji: str = None) -> FlexMessage:
        """بناء نافذة الإجابة الصحيحة"""
        theme = self.get_theme(theme_emoji)
        
        success_card = self.create_glass_card([
            {"type": "text", "text": "✅", "size": "xxl", "align": "center"},
            {"type": "text", "text": "إجابة صحيحة!", "size": "xl", "weight": "bold", "color": theme["primary"], "align": "center"},
            {"type": "text", "text": f"+{points_earned} نقطة", "size": "lg", "color": theme["primary"], "weight": "bold", "align": "center"}
        ], theme)
        
        next_q_card = self.create_glass_card([
            {"type": "text", "text": "السؤال التالي", "size": "sm", "color": theme["text_light"], "align": "center"},
            {"type": "text", "text": next_question['question'], "size": "lg", "weight": "bold", "color": theme["text"], "align": "center", "wrap": True}
        ], theme)
        
        body_contents = [
            success_card,
            next_q_card
        ]
        
        bubble = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": body_contents,
                "backgroundColor": theme["bg"],
                "paddingAll": "25px",
                "spacing": "lg"
            }
        }
        
        return FlexMessage(
            alt_text="✅ إجابة صحيحة",
            contents=FlexContainer.from_dict(bubble)
        )
