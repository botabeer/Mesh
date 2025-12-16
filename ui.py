from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
from config import Config


class UI:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    def _quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="القائمة", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="منشن", text="منشن")),
            QuickReplyItem(action=MessageAction(label="موقف", text="موقف")),
            QuickReplyItem(action=MessageAction(label="حكمة", text="حكمة")),
            QuickReplyItem(action=MessageAction(label="شخصية", text="شخصية")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
        ])

    def main_menu(self, user=None):
        c = self._c()
        
        contents = [
            {
                "type": "text",
                "text": Config.BOT_NAME,
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            }
        ]

        if user:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"مرحبا {user['name']}",
                        "size": "lg",
                        "weight": "bold",
                        "color": c["text"],
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": f"{user['points']} نقطة",
                        "size": "md",
                        "weight": "bold",
                        "color": c["success"],
                        "align": "end",
                        "flex": 2
                    }
                ],
                "margin": "lg",
                "paddingAll": "12px",
                "cornerRadius": "12px",
                "borderWidth": "1px",
                "borderColor": c["border"]
            })

        contents.extend([
            {
                "type": "text",
                "text": "الالعاب",
                "size": "md",
                "weight": "bold",
                "color": c["text_secondary"],
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "العاب", "text": "العاب"},
                        "style": "primary",
                        "color": c["primary"],
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "انسحب", "text": "انسحب"},
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "ايقاف", "text": "ايقاف"},
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
            },
            {
                "type": "text",
                "text": "محتوى تفاعلي",
                "size": "md",
                "weight": "bold",
                "color": c["text_secondary"],
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "تحدي", "text": "تحدي"},
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "سؤال", "text": "سؤال"},
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "اعتراف", "text": "اعتراف"},
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
            },
            {
                "type": "text",
                "text": "الملف الشخصي",
                "size": "md",
                "weight": "bold",
                "color": c["text_secondary"],
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "نقاطي" if user else "تسجيل",
                            "text": "نقاطي" if user else "تسجيل"
                        },
                        "style": "primary" if not user else "secondary",
                        "color": c["primary"] if not user else None,
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "الصدارة", "text": "الصدارة"},
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
            }
        ])

        if user:
            theme_icon = "الليلي" if self.theme == "light" else "النهاري"
            
            contents.extend([
                {
                    "type": "text",
                    "text": "الإعدادات",
                    "size": "md",
                    "weight": "bold",
                    "color": c["text_secondary"],
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": f"الوضع {theme_icon}",
                                "text": "ثيم"
                            },
                            "style": "secondary",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "تغيير الاسم",
                                "text": "تغيير الاسم"
                            },
                            "style": "secondary",
                            "height": "sm"
                        }
                    ]
                }
            ])

        contents.extend([
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            },
            {
                "type": "text",
                "text": f"v{Config.VERSION}",
                "size": "xxs",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "md"
            }
        ])

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px",
                "spacing": "md",
                "backgroundColor": c["bg"]
            }
        }

        return FlexMessage(
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    def ask_name(self):
        c = self._c()
        
        contents = [
            {
                "type": "text",
                "text": "التسجيل",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            },
            {
                "type": "text",
                "text": "ارسل اسمك للتسجيل",
                "size": "md",
                "color": c["text"],
                "align": "center",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "من 2 الى 50 حرف",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "sm"
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "الغاء", "text": "بداية"},
                "style": "secondary",
                "height": "sm",
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
                "paddingAll": "20px",
                "spacing": "md",
                "backgroundColor": c["bg"]
            }
        }

        return FlexMessage(
            alt_text="التسجيل",
            contents=FlexContainer.from_dict(bubble)
        )

    def ask_name_invalid(self):
        """رسالة عند استخدام اسم محجوز"""
        c = self._c()
        
        return TextMessage(
            text="عذرا، هذا الاسم محجوز.\nارجو اختيار اسم مختلف."
        )

    def ask_new_name(self):
        """طلب اسم جديد"""
        c = self._c()
        
        contents = [
            {
                "type": "text",
                "text": "تغيير الاسم",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            },
            {
                "type": "text",
                "text": "ارسل الاسم الجديد",
                "size": "md",
                "color": c["text"],
                "align": "center",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "من 2 الى 50 حرف",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "sm"
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "الغاء", "text": "بداية"},
                "style": "secondary",
                "height": "sm",
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
                "paddingAll": "20px",
                "spacing": "md",
                "backgroundColor": c["bg"]
            }
        }

        return FlexMessage(
            alt_text="تغيير الاسم",
            contents=FlexContainer.from_dict(bubble)
        )

    def ask_new_name_invalid(self):
        """رسالة عند استخدام اسم محجوز للتغيير"""
        return TextMessage(
            text="عذرا، هذا الاسم محجوز.\nارجو اختيار اسم مختلف."
        )

    def registration_required(self):
        """رسالة طلب التسجيل"""
        return TextMessage(
            text="يجب التسجيل اولا\nارسل: تسجيل"
        )

    def game_stopped(self):
        """رسالة إيقاف اللعبة"""
        c = self._c()
        
        contents = [
            {
                "type": "text",
                "text": "تم ايقاف اللعبة",
                "size": "xl",
                "weight": "bold",
                "color": c["warning"],
                "align": "center"
            },
            {
                "type": "text",
                "text": "تم حفظ تقدمك",
                "size": "sm",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "md"
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "العودة", "text": "بداية"},
                "style": "primary",
                "color": c["primary"],
                "height": "sm",
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
                "paddingAll": "20px",
                "spacing": "md",
                "backgroundColor": c["bg"]
            }
        }

        return FlexMessage(
            alt_text="تم ايقاف اللعبة",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    # باقي الدوال من ui.py السابق...
    # (games_menu, help_menu, stats_card, leaderboard_card)
