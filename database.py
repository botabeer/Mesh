from typing import Dict, List, Optional
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction
from config import Config


class UIBuilder:
    def __init__(self):
        self.config = Config

    def _get_quick_reply(self) -> QuickReply:
        """أزرار سريعة ثابتة أسفل الشاشة"""
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="بداية", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="توافق", text="توافق"))
        ])

    def _create_flex(self, alt_text: str, flex_dict: dict) -> FlexMessage:
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_dict),
            quick_reply=self._get_quick_reply()
        )

    def _create_text(self, text: str) -> TextMessage:
        return TextMessage(text=text, quick_reply=self._get_quick_reply())

    def _get_colors(self, theme: str = None) -> Dict[str, str]:
        return self.config.get_theme(theme)

    def home_screen(self, username: str, points: int, is_registered: bool, theme: str) -> FlexMessage:
        """شاشة البداية مع اختيار الثيم"""
        c = self._get_colors(theme)
        
        return self._create_flex("البداية", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "0px",
                "backgroundColor": c["bg"],
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "paddingAll": "24px",
                        "backgroundColor": c["glass"],
                        "contents": [
                            {
                                "type": "text",
                                "text": self.config.BOT_NAME,
                                "size": "xxl",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": f"v{self.config.VERSION}",
                                "size": "xs",
                                "color": c["text3"],
                                "align": "center",
                                "margin": "xs"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "paddingAll": "20px",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": c["card"],
                                "cornerRadius": "16px",
                                "paddingAll": "20px",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": username[:30],
                                        "size": "lg",
                                        "weight": "bold",
                                        "color": c["text"],
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": "مسجل" if is_registered else "زائر",
                                        "size": "sm",
                                        "color": c["success"] if is_registered else c["text3"],
                                        "align": "center",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "spacing": "sm",
                                        "margin": "md",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "النقاط",
                                                "size": "sm",
                                                "color": c["text2"],
                                                "flex": 0
                                            },
                                            {
                                                "type": "text",
                                                "text": str(points),
                                                "size": "xl",
                                                "weight": "bold",
                                                "color": c["primary"],
                                                "align": "end",
                                                "flex": 1
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": c["card"],
                                "cornerRadius": "16px",
                                "paddingAll": "16px",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "المظهر",
                                        "size": "sm",
                                        "color": c["text2"],
                                        "align": "center",
                                        "margin": "none"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "spacing": "sm",
                                        "margin": "sm",
                                        "contents": [
                                            {
                                                "type": "button",
                                                "style": "primary" if theme == "فاتح" else "secondary",
                                                "height": "sm",
                                                "color": c["primary"] if theme == "فاتح" else c["text3"],
                                                "action": {"type": "message", "label": "فاتح", "text": "ثيم فاتح"}
                                            },
                                            {
                                                "type": "button",
                                                "style": "primary" if theme == "داكن" else "secondary",
                                                "height": "sm",
                                                "color": c["primary"] if theme == "داكن" else c["text3"],
                                                "action": {"type": "message", "label": "داكن", "text": "ثيم داكن"}
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "button",
                                        "style": "primary",
                                        "height": "sm",
                                        "color": c["primary"],
                                        "action": {"type": "message", "label": "مساعدة", "text": "مساعدة"}
                                    },
                                    {
                                        "type": "button",
                                        "style": "primary",
                                        "height": "sm",
                                        "color": c["success"],
                                        "action": {"type": "message", "label": "العاب", "text": "العاب"}
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "paddingAll": "16px",
                        "contents": [
                            {
                                "type": "text",
                                "text": self.config.RIGHTS,
                                "size": "xxs",
                                "color": c["text3"],
                                "align": "center",
                                "wrap": True
                            }
                        ]
                    }
                ]
            }
        })

    def help_screen(self, theme: str) -> FlexMessage:
        """شاشة المساعدة"""
        c = self._get_colors(theme)
        
        return self._create_flex("المساعدة", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "24px",
                "backgroundColor": c["bg"],
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["glass"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "contents": [
                            {
                                "type": "text",
                                "text": "دليل الاستخدام",
                                "size": "xl",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "spacing": "sm",
                        "contents": [
                            {"type": "text", "text": "الاوامر الاساسية", "size": "sm", "weight": "bold", "color": c["text"]},
                            {"type": "text", "text": "بداية - العاب - مساعدة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "spacing": "sm",
                        "contents": [
                            {"type": "text", "text": "الحساب", "size": "sm", "weight": "bold", "color": c["text"]},
                            {"type": "text", "text": "انضم - انسحب - نقاطي - صدارة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "spacing": "sm",
                        "contents": [
                            {"type": "text", "text": "اثناء اللعب", "size": "sm", "weight": "bold", "color": c["text"]},
                            {"type": "text", "text": "لمح - جاوب - ايقاف", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "spacing": "sm",
                        "contents": [
                            {"type": "text", "text": "الالعاب الترفيهية", "size": "sm", "weight": "bold", "color": c["text"]},
                            {"type": "text", "text": "سؤال - تحدي - اعتراف - منشن - توافق", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "height": "sm",
                                "color": c["primary"],
                                "action": {"type": "message", "label": "بداية", "text": "بداية"}
                            },
                            {
                                "type": "button",
                                "style": "primary",
                                "height": "sm",
                                "color": c["success"],
                                "action": {"type": "message", "label": "العاب", "text": "العاب"}
                            }
                        ]
                    }
                ]
            }
        })

    def games_menu(self, theme: str) -> FlexMessage:
        """قائمة الالعاب الشاملة"""
        c = self._get_colors(theme)
        
        point_games = self.config.get_all_point_games()
        fun_games = self.config.get_all_fun_games()
        
        point_buttons = []
        for i in range(0, len(point_games), 3):
            row = {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm" if i > 0 else "md",
                "contents": []
            }
            for g in point_games[i:i+3]:
                row["contents"].append({
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "color": c["primary"],
                    "action": {"type": "message", "label": self.config.POINT_GAMES[g]["name"], "text": g}
                })
            point_buttons.append(row)
        
        fun_buttons = []
        for i in range(0, len(fun_games), 3):
            row = {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm" if i > 0 else "md",
                "contents": []
            }
            for g in fun_games[i:i+3]:
                row["contents"].append({
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {"type": "message", "label": self.config.FUN_GAMES[g]["name"], "text": g}
                })
            fun_buttons.append(row)
        
        return self._create_flex("الالعاب", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "24px",
                "backgroundColor": c["bg"],
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["glass"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الالعاب المتاحة",
                                "size": "xl",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "contents": [
                            {
                                "type": "text",
                                "text": "العاب النقاط",
                                "size": "sm",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            },
                            *point_buttons
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "contents": [
                            {
                                "type": "text",
                                "text": "العاب ترفيهية",
                                "size": "sm",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            },
                            *fun_buttons
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "height": "sm",
                                "color": c["secondary"],
                                "action": {"type": "message", "label": "تسجيل", "text": "انضم"}
                            },
                            {
                                "type": "button",
                                "style": "primary",
                                "height": "sm",
                                "color": c["primary"],
                                "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"}
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "صدارة", "text": "صدارة"}
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "انسحب", "text": "انسحب"}
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "ايقاف", "text": "ايقاف"}
                            },
                            {
                                "type": "button",
                                "style": "primary",
                                "height": "sm",
                                "color": c["success"],
                                "action": {"type": "message", "label": "بداية", "text": "بداية"}
                            }
                        ]
                    }
                ]
            }
        })

    def my_points(self, username: str, points: int, stats: Optional[Dict], theme: str) -> FlexMessage:
        """شاشة النقاط"""
        c = self._get_colors(theme)
        
        stats_content = []
        if stats:
            for game, data in stats.items():
                stats_content.append({
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "sm",
                    "contents": [
                        {"type": "text", "text": game, "size": "sm", "color": c["text"], "flex": 2},
                        {"type": "text", "text": f"{data['plays']} مرة", "size": "xs", "color": c["text3"], "flex": 1, "align": "end"}
                    ]
                })
        else:
            stats_content.append({
                "type": "text",
                "text": "لا توجد احصائيات",
                "size": "sm",
                "color": c["text3"],
                "align": "center"
            })
        
        return self._create_flex("نقاطي", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "24px",
                "backgroundColor": c["bg"],
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["glass"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "contents": [
                            {"type": "text", "text": "احصائياتي", "size": "xl", "weight": "bold", "color": c["text"], "align": "center"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "20px",
                        "contents": [
                            {"type": "text", "text": username[:30], "size": "lg", "weight": "bold", "color": c["text"], "align": "center"},
                            {"type": "text", "text": "اجمالي النقاط", "size": "sm", "color": c["text2"], "align": "center", "margin": "md"},
                            {"type": "text", "text": str(points), "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center", "margin": "xs"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "contents": [
                            {"type": "text", "text": "الالعاب الاكثر لعبا", "size": "sm", "weight": "bold", "color": c["text"], "align": "center"},
                            *stats_content
                        ]
                    }
                ]
            }
        })

    def leaderboard(self, top_users: List[tuple], theme: str) -> FlexMessage:
        """لوحة الصدارة"""
        c = self._get_colors(theme)
        
        rows = []
        for i, (name, pts) in enumerate(top_users[:20], start=1):
            rank_color = c["primary"] if i <= 3 else c["text2"]
            
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "paddingAll": "12px",
                "margin": "xs",
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "contents": [
                    {"type": "text", "text": str(i), "size": "md", "weight": "bold", "color": rank_color, "flex": 0},
                    {"type": "text", "text": name[:20], "size": "sm", "color": c["text"], "flex": 3, "margin": "md"},
                    {"type": "text", "text": str(pts), "size": "sm", "weight": "bold", "color": c["primary"], "flex": 1, "align": "end"}
                ]
            })
        
        return self._create_flex("الصدارة", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "24px",
                "backgroundColor": c["bg"],
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["glass"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "contents": [
                            {"type": "text", "text": "لوحة الصدارة", "size": "xl", "weight": "bold", "color": c["text"], "align": "center"}
                        ]
                    },
                    {"type": "box", "layout": "vertical", "contents": rows}
                ]
            }
        })

    def registration_prompt(self, theme: str) -> TextMessage:
        return self._create_text("ارسل اسمك للتسجيل")

    def registration_success(self, username: str, points: int, theme: str) -> TextMessage:
        return self._create_text(f"تم التسجيل بنجاح\n\nالاسم: {username}\nالنقاط: {points}")

    def unregister_confirm(self, username: str, points: int, theme: str) -> TextMessage:
        return self._create_text(f"تم الانسحاب\n\nالاسم: {username}\nالنقاط: {points}")

    def game_stopped(self, game_name: str, theme: str) -> TextMessage:
        return self._create_text(f"تم ايقاف لعبة {game_name}")
