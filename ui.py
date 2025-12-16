from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
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
                "type": "text",
                "text": "منصة الالعاب التفاعلية",
                "size": "xs",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "sm"
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            }
        ]

        if user:
            # عرض معلومات المستخدم
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

        # زر تغيير الثيم (فقط للمستخدمين المسجلين)
        if user:
            theme_icon = "🌙" if self.theme == "light" else "☀️"
            theme_label = "الوضع الليلي" if self.theme == "light" else "الوضع النهاري"
            
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
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": f"{theme_icon} {theme_label}",
                        "text": "ثيم"
                    },
                    "style": "secondary",
                    "height": "sm"
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
                "text": f"{Config.BOT_NAME} v{Config.VERSION}",
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

    def games_menu(self):
        c = self._c()
        
        contents = [
            {
                "type": "text",
                "text": "الالعاب المتاحة",
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
                "text": "العاب ذهنية",
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
                        "action": {"type": "message", "label": "ذكاء", "text": "ذكاء"},
                        "style": "primary",
                        "color": c["primary"],
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "خمن", "text": "خمن"},
                        "style": "primary",
                        "color": c["secondary"],
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "رياضيات", "text": "رياضيات"},
                        "style": "primary",
                        "color": c["success"],
                        "height": "sm"
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
                        "action": {"type": "message", "label": "ترتيب", "text": "ترتيب"},
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "ضد", "text": "ضد"},
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "اسرع", "text": "اسرع"},
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
            },
            {
                "type": "text",
                "text": "العاب كلمات",
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
                        "action": {"type": "message", "label": "سلسلة", "text": "سلسله"},
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "انسان حيوان", "text": "انسان حيوان"},
                        "style": "secondary",
                        "height": "sm"
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
                        "action": {"type": "message", "label": "كون كلمات", "text": "كون كلمات"},
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "اغاني", "text": "اغاني"},
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
            },
            {
                "type": "text",
                "text": "العاب اخرى",
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
                        "action": {"type": "message", "label": "الوان", "text": "الوان"},
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "مافيا", "text": "مافيا"},
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "توافق", "text": "توافق"},
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
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
            alt_text="الالعاب",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    def help_menu(self):
        c = self._c()
        
        sections = [
            ("الاوامر الرئيسية", "بداية - تسجيل - العاب - نقاطي - الصدارة - انسحب - ثيم"),
            ("العاب ذهنية", "ذكاء - خمن - رياضيات - ترتيب - ضد - اسرع"),
            ("العاب كلمات", "سلسله - انسان حيوان - كون كلمات - اغاني"),
            ("العاب اخرى", "الوان - مافيا - توافق"),
            ("محتوى تفاعلي", "تحدي - سؤال - اعتراف - منشن - موقف - حكمة - شخصية"),
            ("اوامر اللعبة", "لمح - جاوب - انسحب"),
        ]

        contents = [
            {
                "type": "text",
                "text": "المساعدة",
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

        for title, items in sections:
            contents.extend([
                {
                    "type": "text",
                    "text": title,
                    "size": "md",
                    "weight": "bold",
                    "color": c["text_secondary"],
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": items,
                    "size": "sm",
                    "color": c["text"],
                    "wrap": True
                }
            ])

        contents.extend([
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
            alt_text="المساعدة",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    def stats_card(self, user):
        c = self._c()
        
        win_rate = round((user['wins'] / user['games'] * 100)) if user['games'] > 0 else 0
        
        contents = [
            {
                "type": "text",
                "text": "احصائياتي",
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
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "الاسم",
                        "size": "sm",
                        "color": c["text_secondary"],
                        "flex": 2
                    },
                    {
                        "type": "text",
                        "text": user['name'],
                        "size": "sm",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "end",
                        "flex": 3
                    }
                ],
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "النقاط",
                        "size": "sm",
                        "color": c["text_secondary"],
                        "flex": 2
                    },
                    {
                        "type": "text",
                        "text": str(user['points']),
                        "size": "sm",
                        "weight": "bold",
                        "color": c["success"],
                        "align": "end",
                        "flex": 3
                    }
                ],
                "margin": "md"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "الالعاب",
                        "size": "sm",
                        "color": c["text_secondary"],
                        "flex": 2
                    },
                    {
                        "type": "text",
                        "text": str(user['games']),
                        "size": "sm",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "end",
                        "flex": 3
                    }
                ],
                "margin": "md"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "الفوز",
                        "size": "sm",
                        "color": c["text_secondary"],
                        "flex": 2
                    },
                    {
                        "type": "text",
                        "text": str(user['wins']),
                        "size": "sm",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "end",
                        "flex": 3
                    }
                ],
                "margin": "md"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "نسبة الفوز",
                        "size": "sm",
                        "color": c["text_secondary"],
                        "flex": 2
                    },
                    {
                        "type": "text",
                        "text": f"{win_rate}%",
                        "size": "sm",
                        "weight": "bold",
                        "color": c["info"],
                        "align": "end",
                        "flex": 3
                    }
                ],
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
            alt_text="احصائياتي",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    def leaderboard_card(self, leaders):
        c = self._c()
        
        contents = [
            {
                "type": "text",
                "text": "لوحة الصدارة",
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

        if not leaders:
            contents.append({
                "type": "text",
                "text": "لا يوجد لاعبين بعد",
                "size": "md",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "lg"
            })
        else:
            for idx, leader in enumerate(leaders[:10], 1):
                medal = ""
                if idx == 1:
                    medal = "🥇 "
                elif idx == 2:
                    medal = "🥈 "
                elif idx == 3:
                    medal = "🥉 "
                
                contents.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{medal}{leader['name']}",
                            "size": "sm",
                            "weight": "bold" if idx <= 3 else "regular",
                            "color": c["text"],
                            "flex": 3
                        },
                        {
                            "type": "text",
                            "text": str(leader['points']),
                            "size": "sm",
                            "weight": "bold",
                            "color": c["success"],
                            "align": "end",
                            "flex": 1
                        }
                    ],
                    "margin": "md",
                    "paddingAll": "8px",
                    "cornerRadius": "8px",
                    "borderWidth": "1px" if idx <= 3 else "0px",
                    "borderColor": c["border"]
                })

        contents.extend([
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
            alt_text="لوحة الصدارة",
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
                "text": "الحد الادنى حرفين والاقصى 50 حرف",
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
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    def game_stopped(self):
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
