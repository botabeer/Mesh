from linebot.v3.messaging import (
    FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
)
from config import Config


class UI:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    def _qr(self):
        commands = [
            "بداية", "العاب", "نقاطي", "الصدارة", "ثيم", "ايقاف", "مساعدة",
            "تحدي", "سؤال", "اعتراف", "منشن", "موقف", "حكمة"
        ]
        return QuickReply(
            items=[QuickReplyItem(action=MessageAction(label=c, text=c)) for c in commands[:13]]
        )

    def _create_glass_card(self, contents, with_shadow=True):
        c = self._c()
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px",
                "spacing": "md"
            },
            "styles": {
                "body": {
                    "separator": False
                }
            }
        }

    def _separator(self, margin="md"):
        c = self._c()
        return {
            "type": "separator",
            "margin": margin,
            "color": c["border"]
        }

    def _glass_box(self, contents, padding="16px"):
        c = self._c()
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": c["glass"],
            "cornerRadius": "16px",
            "paddingAll": padding,
            "spacing": "sm"
        }

    def main_menu(self, user: dict):
        c = self._c()
        name = user.get('name', 'مستخدم') if user else 'مستخدم'
        
        contents = [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "مرحبا",
                        "size": "sm",
                        "color": c["text_secondary"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": name,
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center",
                        "margin": "xs"
                    }
                ],
                "spacing": "none",
                "margin": "none"
            },
            self._separator("lg"),
            self._glass_box([
                {
                    "type": "text",
                    "text": "اختر ما تريد",
                    "size": "md",
                    "color": c["text"],
                    "align": "center",
                    "weight": "bold"
                }
            ]),
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._menu_button("العاب", c["primary"]),
                            self._menu_button("نقاطي", c["secondary"])
                        ],
                        "spacing": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._menu_button("الصدارة", c["success"]),
                            self._menu_button("تحديات", c["accent"])
                        ],
                        "spacing": "sm",
                        "margin": "sm"
                    }
                ],
                "margin": "lg"
            }
        ]
        
        bubble = self._create_glass_card(contents)
        return FlexMessage(alt_text="البداية", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def _menu_button(self, text, color):
        return {
            "type": "button",
            "action": {
                "type": "message",
                "label": text,
                "text": text
            },
            "style": "primary",
            "color": color,
            "height": "md",
            "flex": 1
        }

    def help_menu(self):
        c = self._c()
        contents = [
            {
                "type": "text",
                "text": "المساعدة",
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
            },
            self._separator(),
            self._glass_box([
                {
                    "type": "text",
                    "text": "استخدم الازرار للتفاعل مع البوت",
                    "size": "sm",
                    "color": c["text_secondary"],
                    "align": "center",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "اكتب الاوامر او اختر من القائمة السريعة",
                    "size": "xs",
                    "color": c["text_tertiary"],
                    "align": "center",
                    "wrap": True,
                    "margin": "md"
                }
            ])
        ]
        
        bubble = self._create_glass_card(contents)
        return FlexMessage(alt_text="المساعدة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def registration_choice(self):
        c = self._c()
        contents = [
            {
                "type": "text",
                "text": "مرحبا بك",
                "size": "xxl",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
            },
            self._separator(),
            self._glass_box([
                {
                    "type": "text",
                    "text": "للبدء يرجى التسجيل اولا",
                    "size": "md",
                    "color": c["text_secondary"],
                    "align": "center",
                    "wrap": True
                }
            ]),
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "تسجيل",
                    "text": "تسجيل"
                },
                "style": "primary",
                "color": c["primary"],
                "height": "md",
                "margin": "lg"
            }
        ]
        
        bubble = self._create_glass_card(contents)
        return FlexMessage(alt_text="التسجيل", contents=FlexContainer.from_dict(bubble))

    def ask_name(self):
        return TextMessage(text="ادخل اسمك عربي او انجليزي")

    def ask_name_invalid(self):
        return TextMessage(text="الاسم غير صالح حاول مرة اخرى")

    def theme_changed(self, theme_name):
        return TextMessage(text=f"تم التغيير الى {theme_name}")

    def stats_card(self, user: dict):
        c = self._c()
        
        stats = [
            {"label": "النقاط", "value": str(user.get('points', 0)), "color": c["success"]},
            {"label": "الالعاب", "value": str(user.get('games', 0)), "color": c["primary"]},
            {"label": "الفوز", "value": str(user.get('wins', 0)), "color": c["accent"]}
        ]
        
        contents = [
            {
                "type": "text",
                "text": "احصائياتي",
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
            },
            self._separator(),
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._stat_item(stat["label"], stat["value"], stat["color"])
                    for stat in stats
                ],
                "spacing": "md",
                "margin": "lg"
            }
        ]
        
        bubble = self._create_glass_card(contents)
        return FlexMessage(alt_text="احصائياتي", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def _stat_item(self, label, value, color):
        c = self._c()
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": value,
                    "size": "xxl",
                    "weight": "bold",
                    "color": color,
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": label,
                    "size": "xs",
                    "color": c["text_secondary"],
                    "align": "center",
                    "margin": "sm"
                }
            ],
            "backgroundColor": c["glass"],
            "cornerRadius": "12px",
            "paddingAll": "16px",
            "flex": 1
        }

    def leaderboard_card(self, leaders: list):
        c = self._c()
        
        contents = [
            {
                "type": "text",
                "text": "لوحة الصدارة",
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
            },
            self._separator()
        ]
        
        for i, leader in enumerate(leaders[:10], 1):
            medal_colors = {1: "#FFD700", 2: "#C0C0C0", 3: "#CD7F32"}
            medal_color = medal_colors.get(i, c["accent"])
            
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": str(i),
                        "size": "md",
                        "weight": "bold",
                        "color": "#FFFFFF",
                        "align": "center",
                        "flex": 0,
                        "backgroundColor": medal_color,
                        "cornerRadius": "50%",
                        "paddingAll": "8px",
                        "width": "32px",
                        "height": "32px"
                    },
                    {
                        "type": "text",
                        "text": leader.get('name', 'مجهول'),
                        "size": "md",
                        "color": c["text"],
                        "flex": 3,
                        "margin": "md",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f"{leader.get('points', 0)}",
                        "size": "md",
                        "color": c["primary"],
                        "align": "end",
                        "flex": 1,
                        "weight": "bold"
                    }
                ],
                "spacing": "md",
                "backgroundColor": c["glass"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "margin": "sm"
            })
        
        bubble = self._create_glass_card(contents)
        return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def games_menu(self):
        c = self._c()
        games = ["ذكاء", "خمن", "رياضيات", "ترتيب", "ضد", "اسرع", "سلسله", "انسان حيوان", "تكوين", "اغاني", "الوان", "توافق"]
        
        contents = [
            {
                "type": "text",
                "text": "الالعاب المتاحة",
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
            },
            self._separator()
        ]
        
        for i in range(0, len(games), 2):
            row_games = games[i:i+2]
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": game,
                            "text": game
                        },
                        "style": "primary",
                        "color": c["primary"],
                        "height": "sm",
                        "flex": 1
                    } for game in row_games
                ],
                "spacing": "sm",
                "margin": "sm"
            })
        
        bubble = self._create_glass_card(contents)
        return FlexMessage(alt_text="الالعاب", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def game_stopped(self):
        return TextMessage(text="تم ايقاف اللعبة")
