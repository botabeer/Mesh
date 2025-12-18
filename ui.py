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
        """QuickReply ثابت في كل مكان"""
        items = ["سؤال", "منشن", "تحدي", "اعتراف", "شخصية", "حكمة", "موقف", "بداية", "العاب", "مساعدة"]
        return QuickReply(
            items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items]
        )

    def _separator(self, margin="md"):
        return {"type": "separator", "margin": margin, "color": self._c()["border"]}

    def _glass_box(self, contents, padding="16px", margin="none"):
        c = self._c()
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": c["card_secondary"],
            "cornerRadius": "12px",
            "paddingAll": padding,
            "spacing": "sm",
            "margin": margin
        }

    def text_content(self, title, content):
        """عرض محتوى نصي (سؤال، منشن، تحدي، إلخ)"""
        c = self._c()
        
        contents = [
            {
                "type": "text",
                "text": title,
                "size": "lg",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
            },
            self._separator("lg"),
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": content,
                        "size": "md",
                        "color": c["text"],
                        "wrap": True,
                        "align": "center"
                    }
                ],
                "backgroundColor": c["card_secondary"],
                "cornerRadius": "12px",
                "paddingAll": "24px",
                "margin": "lg"
            }
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text=title, 
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def main_menu(self, user: dict):
        c = self._c()
        name = user.get('name', 'مستخدم') if user else 'مستخدم'
        points = user.get('points', 0) if user else 0
        
        contents = [
            {
                "type": "text",
                "text": "Bot Mesh",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "مرحبا بك",
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
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"{points}",
                                "size": "md",
                                "color": c["text"],
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "نقطة",
                                "size": "sm",
                                "color": c["text_secondary"],
                                "margin": "xs"
                            }
                        ],
                        "justifyContent": "center",
                        "margin": "md"
                    }
                ],
                "spacing": "none",
                "margin": "sm"
            },
            self._separator("lg"),
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._main_button("العاب", c["primary"]),
                    self._main_button("نقاطي", c["secondary"]),
                    self._main_button("الصدارة", c["primary"])
                ],
                "spacing": "sm",
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._main_button("سؤال", c["secondary"]),
                    self._main_button("منشن", c["primary"]),
                    self._main_button("تحدي", c["secondary"])
                ],
                "spacing": "sm",
                "margin": "sm"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._main_button("اعتراف", c["primary"]),
                    self._main_button("موقف", c["secondary"]),
                    self._main_button("حكمة", c["primary"])
                ],
                "spacing": "sm",
                "margin": "sm"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._main_button("شخصية", c["secondary"]),
                    self._main_button("ثيم", c["primary"]),
                    self._main_button("مساعدة", c["secondary"])
                ],
                "spacing": "sm",
                "margin": "sm"
            },
            self._separator("lg"),
            {
                "type": "text",
                "text": "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025",
                "size": "xxs",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "md",
                "wrap": True
            }
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px",
                "spacing": "none"
            }
        }
        
        return FlexMessage(
            alt_text="البداية", 
            contents=FlexContainer.from_dict(bubble), 
            quickReply=self._qr()
        )

    def _main_button(self, text, color):
        c = self._c()
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": text,
                            "size": "md",
                            "align": "center",
                            "color": "#000000",
                            "weight": "bold"
                        }
                    ],
                    "backgroundColor": color,
                    "cornerRadius": "12px",
                    "paddingAll": "16px",
                    "height": "56px",
                    "justifyContent": "center"
                }
            ],
            "action": {
                "type": "message",
                "text": text
            },
            "flex": 1
        }

    def _secondary_button(self, text, color):
        return {
            "type": "button",
            "action": {
                "type": "message",
                "label": text,
                "text": text
            },
            "style": "secondary",
            "color": color,
            "height": "sm",
            "flex": 1
        }

    def challenges_menu(self):
        c = self._c()
        
        contents = [
            {
                "type": "text",
                "text": "Bot Mesh",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center"
            },
            {
                "type": "text",
                "text": "التحديات",
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center",
                "margin": "sm"
            },
            {
                "type": "text",
                "text": "اختر نوع التحدي",
                "size": "xs",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "sm"
            },
            self._separator("lg")
        ]
        
        rows = [
            ["سؤال", "منشن", "تحدي"],
            ["اعتراف", "موقف", "حكمة"],
            ["شخصية", "", ""]
        ]
        
        for row in rows:
            buttons = []
            for item in row:
                if item:
                    buttons.append(self._challenge_button(item, c["primary"] if len(buttons) % 2 == 0 else c["secondary"]))
            
            if buttons:
                contents.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": buttons,
                    "spacing": "sm",
                    "margin": "md"
                })
        
        contents.append(self._separator("lg"))
        contents.append({
            "type": "button",
            "action": {
                "type": "message",
                "label": "رجوع للبداية",
                "text": "بداية"
            },
            "style": "secondary",
            "height": "sm",
            "margin": "md"
        })
        
        contents.append({
            "type": "text",
            "text": "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025",
            "size": "xxs",
            "color": c["text_tertiary"],
            "align": "center",
            "margin": "md",
            "wrap": True
        })
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text="التحديات", 
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def _challenge_button(self, text, color):
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": text,
                            "size": "md",
                            "align": "center",
                            "color": "#000000",
                            "weight": "bold"
                        }
                    ],
                    "backgroundColor": color,
                    "cornerRadius": "12px",
                    "paddingAll": "16px",
                    "height": "56px",
                    "justifyContent": "center"
                }
            ],
            "action": {
                "type": "message",
                "text": text
            },
            "flex": 1
        }

    def games_menu(self):
        c = self._c()
        
        games = [
            "ذكاء", "خمن", "رياضيات",
            "ترتيب", "ضد", "اسرع",
            "سلسله", "لعبه", "تكوين",
            "اغاني", "الوان", "توافق",
            "مافيا"
        ]
        
        contents = [
            {
                "type": "text",
                "text": "Bot Mesh",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center"
            },
            {
                "type": "text",
                "text": "الالعاب المتاحة",
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center",
                "margin": "sm"
            },
            {
                "type": "text",
                "text": "اختر لعبتك المفضلة",
                "size": "xs",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "sm"
            },
            self._separator("lg")
        ]
        
        for i in range(0, len(games), 3):
            row_games = games[i:i+3]
            buttons = []
            for idx, game in enumerate(row_games):
                color = c["primary"] if idx % 2 == 0 else c["secondary"]
                buttons.append(self._game_card(game, color))
            
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": buttons,
                "spacing": "sm",
                "margin": "md"
            })
        
        contents.append(self._separator("lg"))
        contents.append({
            "type": "button",
            "action": {
                "type": "message",
                "label": "رجوع للبداية",
                "text": "بداية"
            },
            "style": "secondary",
            "height": "sm",
            "margin": "md"
        })
        
        contents.append({
            "type": "text",
            "text": "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025",
            "size": "xxs",
            "color": c["text_tertiary"],
            "align": "center",
            "margin": "md",
            "wrap": True
        })
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text="الالعاب", 
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def _game_card(self, name, color):
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": name,
                            "size": "md",
                            "align": "center",
                            "color": "#000000",
                            "weight": "bold"
                        }
                    ],
                    "backgroundColor": color,
                    "cornerRadius": "12px",
                    "paddingAll": "16px",
                    "height": "56px",
                    "justifyContent": "center"
                }
            ],
            "action": {
                "type": "message",
                "text": name
            },
            "flex": 1
        }

    def help_menu(self):
        c = self._c()
        
        commands = [
            {"cmd": "بداية", "desc": "القائمة الرئيسية"},
            {"cmd": "العاب", "desc": "جميع الالعاب"},
            {"cmd": "نقاطي", "desc": "احصائياتك"},
            {"cmd": "الصدارة", "desc": "المتصدرين"},
            {"cmd": "سؤال", "desc": "أسئلة عميقة"},
            {"cmd": "منشن", "desc": "منشن أصدقائك"},
            {"cmd": "تحدي", "desc": "تحديات ممتعة"},
            {"cmd": "اعتراف", "desc": "اعترافات صريحة"},
            {"cmd": "موقف", "desc": "مواقف افتراضية"},
            {"cmd": "حكمة", "desc": "حكم وأقوال"},
            {"cmd": "شخصية", "desc": "اكتشف شخصيتك"},
            {"cmd": "ثيم", "desc": "تبديل الثيم"},
            {"cmd": "ايقاف", "desc": "ايقاف اللعبة"},
            {"cmd": "لمح", "desc": "تلميح"},
            {"cmd": "جاوب", "desc": "عرض الاجابة"}
        ]
        
        contents = [
            {
                "type": "text",
                "text": "Bot Mesh",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center"
            },
            {
                "type": "text",
                "text": "دليل الاستخدام",
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center",
                "margin": "sm"
            },
            {
                "type": "text",
                "text": "اوامر البوت الاساسية",
                "size": "xs",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "sm"
            },
            self._separator("lg")
        ]
        
        for cmd in commands:
            contents.append(
                self._glass_box([
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": cmd["cmd"],
                                "size": "sm",
                                "color": c["text"],
                                "weight": "bold",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": cmd["desc"],
                                "size": "xs",
                                "color": c["text_secondary"],
                                "wrap": True,
                                "flex": 1,
                                "margin": "md"
                            }
                        ]
                    }
                ], "12px", "sm")
            )
        
        contents.append(self._separator("lg"))
        contents.append({
            "type": "button",
            "action": {
                "type": "message",
                "label": "رجوع للبداية",
                "text": "بداية"
            },
            "style": "primary",
            "color": c["primary"],
            "height": "sm",
            "margin": "lg"
        })
        
        contents.append({
            "type": "text",
            "text": "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025",
            "size": "xxs",
            "color": c["text_tertiary"],
            "align": "center",
            "margin": "md",
            "wrap": True
        })
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text="المساعدة", 
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

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
            {
                "type": "text",
                "text": "في بوت ميش",
                "size": "md",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "sm"
            },
            self._separator("lg"),
            self._glass_box([
                {
                    "type": "text",
                    "text": "للبدء يرجى التسجيل اولا",
                    "size": "md",
                    "color": c["text"],
                    "align": "center",
                    "wrap": True,
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": "سنحتاج الى اسمك فقط",
                    "size": "xs",
                    "color": c["text_secondary"],
                    "align": "center",
                    "margin": "md"
                }
            ], "20px", "lg"),
            {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "تسجيل الان",
                    "text": "تسجيل"
                },
                "style": "primary",
                "color": c["primary"],
                "height": "md",
                "margin": "lg"
            }
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(alt_text="التسجيل", contents=FlexContainer.from_dict(bubble))

    def stats_card(self, user: dict):
        c = self._c()
        
        stats = [
            {"label": "النقاط", "value": str(user.get('points', 0)), "color": c["text"]},
            {"label": "الالعاب", "value": str(user.get('games', 0)), "color": c["text"]},
            {"label": "الفوز", "value": str(user.get('wins', 0)), "color": c["text"]}
        ]
        
        win_rate = round((user.get('wins', 0) / user.get('games', 1)) * 100) if user.get('games', 0) > 0 else 0
        
        contents = [
            {
                "type": "text",
                "text": "احصائياتي",
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
            },
            {
                "type": "text",
                "text": user.get('name', 'مستخدم'),
                "size": "sm",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "sm"
            },
            self._separator("lg")
        ]
        
        for stat in stats:
            contents.append(
                self._glass_box([
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
                                        "text": stat["value"],
                                        "size": "xl",
                                        "weight": "bold",
                                        "color": stat["color"]
                                    },
                                    {
                                        "type": "text",
                                        "text": stat["label"],
                                        "size": "xs",
                                        "color": c["text_secondary"]
                                    }
                                ],
                                "flex": 1
                            }
                        ]
                    }
                ], "16px", "sm")
            )
        
        contents.append(self._separator("lg"))
        contents.append(
            self._glass_box([
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "نسبة الفوز",
                            "size": "sm",
                            "color": c["text_secondary"],
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": f"{win_rate}%",
                            "size": "lg",
                            "weight": "bold",
                            "color": c["text"],
                            "flex": 0
                        }
                    ]
                }
            ], "16px", "md")
        )
        
        contents.append({
            "type": "button",
            "action": {
                "type": "message",
                "label": "رجوع للبداية",
                "text": "بداية"
            },
            "style": "secondary",
            "height": "sm",
            "margin": "lg"
        })
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text="احصائياتي", 
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

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
            {
                "type": "text",
                "text": "افضل اللاعبين",
                "size": "xs",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "sm"
            },
            self._separator("lg")
        ]
        
        for i, leader in enumerate(leaders[:10], 1):
            medal_color = c["text"] if i <= 3 else c["text_secondary"]
            
            contents.append(
                self._glass_box([
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
                                        "text": str(i),
                                        "size": "md",
                                        "align": "center",
                                        "color": "#000000",
                                        "weight": "bold"
                                    }
                                ],
                                "backgroundColor": medal_color,
                                "cornerRadius": "50%",
                                "width": "36px",
                                "height": "36px",
                                "justifyContent": "center",
                                "flex": 0
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": leader.get('name', 'مجهول'),
                                        "size": "md",
                                        "color": c["text"],
                                        "weight": "bold"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"الالعاب {leader.get('games', 0)}",
                                        "size": "xs",
                                        "color": c["text_tertiary"]
                                    }
                                ],
                                "flex": 1,
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": str(leader.get('points', 0)),
                                "size": "xl",
                                "color": c["text"],
                                "weight": "bold",
                                "flex": 0
                            }
                        ]
                    }
                ], "12px", "sm")
            )
        
        contents.append(self._separator("lg"))
        contents.append({
            "type": "button",
            "action": {
                "type": "message",
                "label": "رجوع للبداية",
                "text": "بداية"
            },
            "style": "secondary",
            "height": "sm",
            "margin": "md"
        })
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["card"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text="الصدارة", 
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def ask_name(self):
        return TextMessage(text="ادخل اسمك عربي او انجليزي")

    def ask_name_invalid(self):
        return TextMessage(text="الاسم غير صالح حاول مرة اخرى")

    def theme_changed(self, theme_name):
        return TextMessage(text=f"تم التغيير الى {theme_name}")

    def game_stopped(self):
        return TextMessage(text="تم ايقاف اللعبة وحفظ تقدمك")
