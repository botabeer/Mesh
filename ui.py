from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config


class UI:
    """واجهة مستخدم أنيقة ومريحة"""
    
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    def _qr(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="القائمة", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
            QuickReplyItem(action=MessageAction(label="ايقاف", text="ايقاف")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
        ])

    def main_menu(self, user=None):
        """القائمة الرئيسية"""
        c = self._c()

        contents = [
            {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": Config.BOT_NAME, "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "text", "text": f"الإصدار {Config.VERSION}", "size": "xs", "color": c["text_tertiary"], "align": "center", "margin": "xs"}
                ],
                "paddingAll": "md", "backgroundColor": c["card"], "cornerRadius": "md"
            },
            {"type": "separator", "margin": "xl", "color": c["border"]}
        ]

        if user:
            contents.append({
                "type": "box", "layout": "horizontal",
                "contents": [
                    {
                        "type": "box", "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "اللاعب", "size": "xs", "color": c["text_tertiary"]},
                            {"type": "text", "text": user['name'], "size": "md", "weight": "bold", "color": c["text"], "margin": "xs"}
                        ],
                        "flex": 3
                    },
                    {
                        "type": "box", "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "النقاط", "size": "xs", "color": c["text_tertiary"], "align": "end"},
                            {"type": "text", "text": str(user['points']), "size": "xl", "weight": "bold", "color": c["primary"], "align": "end", "margin": "xs"}
                        ],
                        "flex": 2
                    }
                ],
                "margin": "xl", "paddingAll": "md", "cornerRadius": "md",
                "backgroundColor": c["glass"], "borderWidth": "1px", "borderColor": c["border"]
            })

        contents.extend([
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "الالعاب", "text": "العاب"}, 
             "style": "primary", "color": c["primary"], "margin": "md", "height": "md"},
            {
                "type": "box", "layout": "horizontal", "spacing": "md", "margin": "md",
                "contents": [
                    {"type": "button", "action": {"type": "message", "label": "نقاطي" if user else "تسجيل", "text": "نقاطي" if user else "تسجيل"}, 
                     "style": "secondary", "height": "sm", "flex": 1},
                    {"type": "button", "action": {"type": "message", "label": "الصدارة", "text": "الصدارة"}, 
                     "style": "secondary", "height": "sm", "flex": 1}
                ]
            }
        ])

        if user:
            contents.append({
                "type": "box", "layout": "horizontal", "spacing": "md", "margin": "sm",
                "contents": [
                    {"type": "button", "action": {"type": "message", "label": "تغيير الاسم", "text": "تغيير الاسم"}, 
                     "style": "secondary", "height": "sm", "flex": 1},
                    {"type": "button", "action": {"type": "message", "label": "تبديل الثيم", "text": "ثيم"}, 
                     "style": "secondary", "height": "sm", "flex": 1}
                ]
            })
        else:
            contents.append({
                "type": "button", "action": {"type": "message", "label": "تجاهل البوت", "text": "انسحب"},
                "style": "secondary", "height": "sm", "margin": "sm"
            })

        contents.extend([
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "text", "text": Config.COPYRIGHT, "size": "xxs", "color": c["text_tertiary"], "align": "center", "wrap": True, "margin": "md"}
        ])

        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg", "backgroundColor": c["bg"], "spacing": "none"
            }
        }
        return FlexMessage(alt_text="البداية", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def games_menu(self):
        """قائمة الالعاب"""
        c = self._c()
        
        contents = [
            {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "الالعاب المتاحة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"}
                ],
                "paddingAll": "md", "backgroundColor": c["card"], "cornerRadius": "md"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            {"type": "text", "text": "العاب تحتاج تسجيل", "size": "sm", "weight": "bold", "color": c["text"], "margin": "lg"},
            {
                "type": "box", "layout": "vertical", "spacing": "xs", "margin": "sm",
                "contents": [
                    {"type": "button", "action": {"type": "message", "label": "ذكاء", "text": "ذكاء"}, "style": "primary", "color": c["primary"], "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "خمن", "text": "خمن"}, "style": "primary", "color": c["primary"], "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "رياضيات", "text": "رياضيات"}, "style": "primary", "color": c["primary"], "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "ترتيب", "text": "ترتيب"}, "style": "primary", "color": c["primary"], "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "ضد", "text": "ضد"}, "style": "primary", "color": c["primary"], "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "اسرع", "text": "اسرع"}, "style": "primary", "color": c["primary"], "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "سلسلة", "text": "سلسله"}, "style": "primary", "color": c["primary"], "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "انسان حيوان", "text": "انسان حيوان"}, "style": "primary", "color": c["primary"], "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "كون كلمات", "text": "كون كلمات"}, "style": "primary", "color": c["primary"], "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "اغاني", "text": "اغاني"}, "style": "primary", "color": c["primary"], "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "الوان", "text": "الوان"}, "style": "primary", "color": c["primary"], "height": "sm"}
                ]
            },
            
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            {"type": "text", "text": "العاب بدون تسجيل", "size": "sm", "weight": "bold", "color": c["text"], "margin": "lg"},
            {
                "type": "box", "layout": "vertical", "spacing": "xs", "margin": "sm",
                "contents": [
                    {"type": "button", "action": {"type": "message", "label": "توافق", "text": "توافق"}, "style": "secondary", "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "مافيا", "text": "مافيا"}, "style": "secondary", "height": "sm"}
                ]
            },
            
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            {"type": "text", "text": "محتوى تفاعلي", "size": "sm", "weight": "bold", "color": c["secondary"], "margin": "lg"},
            {
                "type": "box", "layout": "vertical", "spacing": "xs", "margin": "sm",
                "contents": [
                    {"type": "button", "action": {"type": "message", "label": "تحدي", "text": "تحدي"}, "style": "secondary", "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "سؤال", "text": "سؤال"}, "style": "secondary", "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "اعتراف", "text": "اعتراف"}, "style": "secondary", "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "منشن", "text": "منشن"}, "style": "secondary", "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "موقف", "text": "موقف"}, "style": "secondary", "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "حكمة", "text": "حكمة"}, "style": "secondary", "height": "sm"},
                    {"type": "button", "action": {"type": "message", "label": "شخصية", "text": "شخصية"}, "style": "secondary", "height": "sm"}
                ]
            },
            
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "md"}
        ]

        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg", "backgroundColor": c["bg"], "spacing": "none"
            }
        }
        return FlexMessage(alt_text="الالعاب", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def help_menu(self):
        """دليل الاستخدام"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "دليل الاستخدام", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            {"type": "text", "text": "الاوامر الاساسية", "size": "md", "weight": "bold", "color": c["text"], "margin": "lg"},
            {"type": "text", "text": "بداية - العاب - نقاطي - الصدارة - ثيم - مساعدة", "size": "sm", "color": c["text_secondary"], "wrap": True, "margin": "sm"},
            
            {"type": "text", "text": "التسجيل", "size": "md", "weight": "bold", "color": c["text"], "margin": "lg"},
            {"type": "text", "text": "تسجيل: للعب وحساب النقاط\nانسحب: تجاهل كامل (لن يرد البوت)", "size": "sm", "color": c["text_secondary"], "wrap": True, "margin": "sm"},
            
            {"type": "text", "text": "المحتوى التفاعلي", "size": "md", "weight": "bold", "color": c["text"], "margin": "lg"},
            {"type": "text", "text": "تحدي - سؤال - اعتراف - منشن - موقف - حكمة - شخصية", "size": "sm", "color": c["text_secondary"], "wrap": True, "margin": "sm"},
            
            {"type": "text", "text": "ملاحظات", "size": "md", "weight": "bold", "color": c["text"], "margin": "lg"},
            {"type": "text", "text": "ايقاف: يوقف اللعبة مؤقتاً\nانسحب: يتجاهلك البوت حتى تسجل", "size": "xs", "color": c["text_tertiary"], "wrap": True, "margin": "sm"},
            
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "text", "text": Config.COPYRIGHT, "size": "xxs", "color": c["text_tertiary"], "align": "center", "wrap": True, "margin": "md"},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "md"}
        ]

        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg", "backgroundColor": c["bg"], "spacing": "none"
            }
        }
        return FlexMessage(alt_text="المساعدة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def stats_card(self, user):
        """بطاقة الاحصائيات"""
        c = self._c()
        win_rate = round((user['wins'] / user['games'] * 100)) if user['games'] > 0 else 0

        contents = [
            {"type": "text", "text": "احصائياتي", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box", "layout": "vertical", "spacing": "sm", "margin": "lg",
                "contents": [
                    self._stat_row("الاسم", user['name'], c),
                    self._stat_row("النقاط", str(user['points']), c, True),
                    self._stat_row("الالعاب", str(user['games']), c),
                    self._stat_row("الفوز", str(user['wins']), c),
                    self._stat_row("نسبة الفوز", f"{win_rate}%", c)
                ]
            },
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "md"}
        ]

        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg", "backgroundColor": c["bg"], "spacing": "none"
            }
        }
        return FlexMessage(alt_text="احصائياتي", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def _stat_row(self, label, value, c, highlight=False):
        return {
            "type": "box", "layout": "horizontal",
            "contents": [
                {"type": "text", "text": label, "size": "sm", "color": c["text_secondary"], "flex": 2},
                {"type": "text", "text": value, "size": "md", "weight": "bold", 
                 "color": c["primary"] if highlight else c["text"], "align": "end", "flex": 3}
            ],
            "paddingAll": "sm", "cornerRadius": "sm", "backgroundColor": c["glass"]
        }

    def leaderboard_card(self, top_users):
        """لوحة الصدارة"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "لوحة الصدارة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        for i, u in enumerate(top_users, 1):
            contents.append({
                "type": "box", "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": f"{i}", "size": "lg", "weight": "bold", "color": c["primary"], "flex": 1, "align": "center"},
                    {
                        "type": "box", "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": u['name'], "size": "md", "weight": "bold", "color": c["text"]},
                            {"type": "text", "text": f"{u['wins']} فوز", "size": "xs", "color": c["text_tertiary"]}
                        ],
                        "flex": 4
                    },
                    {"type": "text", "text": str(u['points']), "size": "lg", "weight": "bold", "color": c["primary"], "flex": 2, "align": "end"}
                ],
                "margin": "md", "paddingAll": "sm", "cornerRadius": "sm", "backgroundColor": c["glass"]
            })

        contents.extend([
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "md"}
        ])

        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg", "backgroundColor": c["bg"], "spacing": "none"
            }
        }
        return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def ask_name(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "التسجيل", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "ادخل اسمك للبدء", "size": "md", "color": c["text"], "align": "center", "margin": "xl", "wrap": True},
            {"type": "text", "text": "حرف واحد على الاقل", "size": "xs", "color": c["text_tertiary"], "align": "center", "margin": "sm"},
            {"type": "button", "action": {"type": "message", "label": "تجاهلني", "text": "انسحب"}, "style": "secondary", "height": "sm", "margin": "lg"}
        ]
        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg", "backgroundColor": c["bg"], "spacing": "none"
            }
        }
        return FlexMessage(alt_text="تسجيل", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def ask_name_invalid(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "اسم غير صحيح", "size": "xl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "الاسم يجب ان يكون 1-50 حرف", "size": "md", "color": c["text"], "align": "center", "margin": "xl", "wrap": True}
        ]
        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg", "backgroundColor": c["bg"], "spacing": "none"
            }
        }
        return FlexMessage(alt_text="خطأ", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def ask_new_name(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "تغيير الاسم", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "ادخل اسمك الجديد", "size": "md", "color": c["text"], "align": "center", "margin": "xl"}
        ]
        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg", "backgroundColor": c["bg"], "spacing": "none"
            }
        }
        return FlexMessage(alt_text="تغيير الاسم", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def ask_new_name_invalid(self):
        return self.ask_name_invalid()

    def game_stopped(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "تم ايقاف اللعبة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "xl"}
        ]
        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg", "backgroundColor": c["bg"], "spacing": "none"
            }
        }
        return FlexMessage(alt_text="ايقاف", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def registration_choice(self):
        """خيار التسجيل أو التجاهل"""
        c = self._c()
        contents = [
            {"type": "text", "text": "اهلا بك", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "للعب مع حفظ النقاط، اختر تسجيل\nللتجاهل التام، اختر انسحب", "size": "sm", "color": c["text"], "align": "center", "margin": "xl", "wrap": True},
            {
                "type": "box", "layout": "vertical", "spacing": "sm", "margin": "xl",
                "contents": [
                    {"type": "button", "action": {"type": "message", "label": "تسجيل", "text": "تسجيل"}, "style": "primary", "color": c["primary"], "height": "md"},
                    {"type": "button", "action": {"type": "message", "label": "انسحب - تجاهل", "text": "انسحب"}, "style": "secondary", "height": "sm"}
                ]
            },
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "text", "text": "انسحب = لن يرد البوت على رسائلك حتى تسجل", "size": "xxs", "color": c["text_tertiary"], "align": "center", "margin": "md", "wrap": True}
        ]
        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg", "backgroundColor": c["bg"], "spacing": "none"
            }
        }
        return FlexMessage(alt_text="التسجيل", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())
