from linebot.v3.messaging import (
    FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
)
from config import Config


class UI:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    def _qr(self, items=None):
        if items is None:
            items = ["بداية", "العاب", "نقاطي", "الصدارة", "ثيم", "مساعدة"]
        return QuickReply(
            items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items[:13]]
        )

    def _separator(self, margin="md"):
        """فاصل بسيط بدون أي ألوان"""
        return {
            "type": "separator",
            "margin": margin
        }

    def _glass_box(self, contents, padding="16px", margin="none"):
        c = self._c()
        # استخدام لون صلب بدلاً من الشفاف
        bg_color = c["card_secondary"] if self.theme == "light" else "#1A202C"
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": bg_color,
            "cornerRadius": "16px",
            "paddingAll": padding,
            "spacing": "sm",
            "margin": margin
        }

    def _icon_badge(self, text, color):
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": text,
                    "size": "xs",
                    "color": "#FFFFFF",
                    "align": "center",
                    "weight": "bold"
                }
            ],
            "backgroundColor": color,
            "cornerRadius": "12px",
            "paddingAll": "8px",
            "width": "48px",
            "height": "48px",
            "justifyContent": "center"
        }

    # ================= Main Menu =================
    
    def main_menu(self, user: dict):
        c = self._c()
        name = user.get('name', 'مستخدم') if user else 'مستخدم'
        points = user.get('points', 0) if user else 0
        
        contents = [
            # Header
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
                                "color": c["success"],
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
                "spacing": "none"
            },
            self._separator("lg"),
            
            # Main Actions - Row 1
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._main_button("العاب", c["primary"], "🎮"),
                    self._main_button("نقاطي", c["secondary"], "📊")
                ],
                "spacing": "md",
                "margin": "lg"
            },
            
            # Main Actions - Row 2
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._main_button("الصدارة", c["success"], "🏆"),
                    self._main_button("تحديات", c["accent"], "⚡")
                ],
                "spacing": "md",
                "margin": "sm"
            },
            
            self._separator("lg"),
            
            # Secondary Actions
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._secondary_button("ثيم", c["text_tertiary"]),
                    self._secondary_button("مساعدة", c["text_tertiary"]),
                    self._secondary_button("انسحب", c["danger"])
                ],
                "spacing": "sm",
                "margin": "md"
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
        
        qr_items = ["العاب", "نقاطي", "الصدارة", "تحديات", "ثيم", "مساعدة"]
        return FlexMessage(
            alt_text="البداية", 
            contents=FlexContainer.from_dict(bubble), 
            quickReply=self._qr(qr_items)
        )

    def _main_button(self, text, color, icon):
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
                            "text": icon,
                            "size": "xl",
                            "align": "center"
                        }
                    ],
                    "backgroundColor": color,
                    "cornerRadius": "16px",
                    "paddingAll": "16px",
                    "height": "64px",
                    "justifyContent": "center"
                },
                {
                    "type": "text",
                    "text": text,
                    "size": "sm",
                    "color": c["text"],
                    "align": "center",
                    "weight": "bold",
                    "margin": "md"
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

    # ================= Games Menu =================
    
    def games_menu(self):
        c = self._c()
        
        games = [
            {"name": "ذكاء", "icon": "🧠", "color": c["primary"]},
            {"name": "خمن", "icon": "🤔", "color": c["secondary"]},
            {"name": "رياضيات", "icon": "🔢", "color": c["success"]},
            {"name": "ترتيب", "icon": "🔤", "color": c["accent"]},
            {"name": "ضد", "icon": "⚖️", "color": c["warning"]},
            {"name": "اسرع", "icon": "⚡", "color": c["danger"]},
            {"name": "سلسله", "icon": "🔗", "color": c["primary"]},
            {"name": "انسان حيوان", "icon": "🦁", "color": c["secondary"]},
            {"name": "تكوين", "icon": "🔠", "color": c["success"]},
            {"name": "اغاني", "icon": "🎵", "color": c["accent"]},
            {"name": "الوان", "icon": "🎨", "color": c["warning"]},
            {"name": "توافق", "icon": "❤️", "color": c["danger"]}
        ]
        
        contents = [
            {
                "type": "text",
                "text": "الالعاب المتاحة",
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
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
        
        # Create game grid (3 per row)
        for i in range(0, len(games), 3):
            row_games = games[i:i+3]
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._game_card(game["name"], game["icon"], game["color"])
                    for game in row_games
                ],
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
        
        qr_items = ["بداية", "نقاطي", "الصدارة", "ثيم", "مساعدة"]
        return FlexMessage(
            alt_text="الالعاب", 
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr(qr_items)
        )

    def _game_card(self, name, icon, color):
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
                            "text": icon,
                            "size": "lg",
                            "align": "center"
                        }
                    ],
                    "backgroundColor": color,
                    "cornerRadius": "12px",
                    "paddingAll": "12px",
                    "height": "48px",
                    "justifyContent": "center"
                },
                {
                    "type": "text",
                    "text": name,
                    "size": "xs",
                    "color": c["text"],
                    "align": "center",
                    "weight": "bold",
                    "margin": "sm"
                }
            ],
            "action": {
                "type": "message",
                "text": name
            },
            "flex": 1
        }

    # ================= Help Menu =================
    
    def help_menu(self):
        c = self._c()
        
        commands = [
            {"cmd": "بداية", "desc": "العودة للقائمة الرئيسية"},
            {"cmd": "العاب", "desc": "عرض جميع الالعاب المتاحة"},
            {"cmd": "نقاطي", "desc": "عرض احصائياتك"},
            {"cmd": "الصدارة", "desc": "عرض لوحة المتصدرين"},
            {"cmd": "ثيم", "desc": "تبديل بين الفاتح والداكن"},
            {"cmd": "ايقاف", "desc": "ايقاف اللعبة الحالية"},
            {"cmd": "لمح", "desc": "الحصول على تلميح"},
            {"cmd": "جاوب", "desc": "عرض الاجابة والانتقال"}
        ]
        
        contents = [
            {
                "type": "text",
                "text": "دليل الاستخدام",
                "size": "xl",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
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
                                "color": c["primary"],
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
        contents.append(self._glass_box([
            {
                "type": "text",
                "text": "استخدم الازرار او اكتب الاوامر مباشرة",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center",
                "wrap": True
            }
        ], "12px", "md"))
        
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
        
        qr_items = ["بداية", "العاب", "نقاطي", "الصدارة", "ثيم"]
        return FlexMessage(
            alt_text="المساعدة", 
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr(qr_items)
        )

    # ================= Registration =================
    
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

    # ================= Stats =================
    
    def stats_card(self, user: dict):
        c = self._c()
        
        stats = [
            {"label": "النقاط", "value": str(user.get('points', 0)), "color": c["success"], "icon": "💎"},
            {"label": "الالعاب", "value": str(user.get('games', 0)), "color": c["primary"], "icon": "🎮"},
            {"label": "الفوز", "value": str(user.get('wins', 0)), "color": c["accent"], "icon": "🏆"}
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
        
        # Stats grid
        for stat in stats:
            contents.append(
                self._glass_box([
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": stat["icon"],
                                "size": "xl",
                                "flex": 0
                            },
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
                                "flex": 1,
                                "margin": "md"
                            }
                        ]
                    }
                ], "16px", "sm")
            )
        
        contents.append(self._separator("lg"))
        
        # Win rate badge
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
                            "color": c["success"],
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
        
        qr_items = ["بداية", "العاب", "الصدارة", "ثيم", "مساعدة"]
        return FlexMessage(
            alt_text="احصائياتي", 
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr(qr_items)
        )

    # ================= Leaderboard =================
    
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
        
        medal_colors = {1: "#FFD700", 2: "#C0C0C0", 3: "#CD7F32"}
        medal_icons = {1: "🥇", 2: "🥈", 3: "🥉"}
        
        for i, leader in enumerate(leaders[:10], 1):
            medal_color = medal_colors.get(i, c["accent"])
            medal_icon = medal_icons.get(i, "🏅")
            
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
                                        "text": medal_icon,
                                        "size": "lg",
                                        "align": "center"
                                    }
                                ],
                                "backgroundColor": medal_color,
                                "cornerRadius": "50%",
                                "width": "40px",
                                "height": "40px",
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
                                "color": c["primary"],
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
        
        qr_items = ["بداية", "العاب", "نقاطي", "ثيم", "مساعدة"]
        return FlexMessage(
            alt_text="الصدارة", 
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr(qr_items)
        )

    # ================= Simple Messages =================
    
    def ask_name(self):
        return TextMessage(text="ادخل اسمك عربي او انجليزي")

    def ask_name_invalid(self):
        return TextMessage(text="الاسم غير صالح حاول مرة اخرى")

    def theme_changed(self, theme_name):
        return TextMessage(text=f"تم التغيير الى {theme_name}")

    def game_stopped(self):
        return TextMessage(text="تم ايقاف اللعبة وحفظ تقدمك")
