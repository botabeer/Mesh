from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config


class UI:
    """واجهة مستخدم محسّنة - أبيض وأسود ورمادي"""
    
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
        """القائمة الرئيسية المحسّنة"""
        c = self._c()
        theme_name = "فاتح" if self.theme == "light" else "داكن"

        contents = [
            {"type": "text", "text": Config.BOT_NAME, "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "text", "text": f"v{Config.VERSION}", "size": "xs", "color": c["text_tertiary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]

        if user:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": user['name'], "size": "sm", "weight": "bold", "color": c["text"], "flex": 3},
                    {"type": "text", "text": str(user['points']), "size": "sm", "weight": "bold", "color": c["primary"], "align": "end", "flex": 1}
                ],
                "margin": "lg",
                "paddingAll": "12px",
                "cornerRadius": "8px",
                "backgroundColor": c["glass"],
                "borderWidth": "1px",
                "borderColor": c["border"]
            })

        # الأزرار الرئيسية
        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "العاب", "text": "العاب"}, "style": "primary", "color": c["primary"], "margin": "md", "height": "sm"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                {"type": "button", "action": {"type": "message", "label": "نقاطي" if user else "تسجيل", "text": "نقاطي" if user else "تسجيل"}, "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "الصدارة", "text": "الصدارة"}, "style": "secondary", "height": "sm", "flex": 1}
            ]},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                {"type": "button", "action": {"type": "message", "label": f"وضع {theme_name}", "text": "ثيم"}, "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "مساعدة", "text": "مساعدة"}, "style": "secondary", "height": "sm", "flex": 1}
            ]}
        ])

        if user:
            contents.extend([
                {"type": "separator", "margin": "lg", "color": c["border"]},
                {"type": "button", "action": {"type": "message", "label": "تغيير الاسم", "text": "تغيير الاسم"}, "style": "secondary", "height": "sm", "margin": "sm"}
            ])

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="البداية", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def games_menu(self):
        """قائمة الألعاب المنظمة"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "الألعاب المتاحة", "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "text", "text": "ألعاب ذهنية", "size": "sm", "weight": "bold", "color": c["text"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                {"type": "button", "action": {"type": "message", "label": "ذكاء", "text": "ذكاء"}, "style": "primary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "خمن", "text": "خمن"}, "style": "primary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "رياضيات", "text": "رياضيات"}, "style": "primary", "height": "sm", "flex": 1}
            ]},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                {"type": "button", "action": {"type": "message", "label": "ترتيب", "text": "ترتيب"}, "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "ضد", "text": "ضد"}, "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "اسرع", "text": "اسرع"}, "style": "secondary", "height": "sm", "flex": 1}
            ]},
            {"type": "text", "text": "ألعاب كلمات", "size": "sm", "weight": "bold", "color": c["text"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                {"type": "button", "action": {"type": "message", "label": "سلسلة", "text": "سلسله"}, "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "انسان حيوان", "text": "انسان حيوان"}, "style": "secondary", "height": "sm", "flex": 2}
            ]},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                {"type": "button", "action": {"type": "message", "label": "كون كلمات", "text": "كون كلمات"}, "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "اغاني", "text": "اغاني"}, "style": "secondary", "height": "sm", "flex": 1}
            ]},
            {"type": "text", "text": "ألعاب اخرى", "size": "sm", "weight": "bold", "color": c["text"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                {"type": "button", "action": {"type": "message", "label": "الوان", "text": "الوان"}, "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "توافق", "text": "توافق"}, "style": "secondary", "height": "sm", "flex": 1}
            ]},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "sm"}
        ]

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="الألعاب", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def help_menu(self):
        """دليل الاستخدام المبسط"""
        c = self._c()
        
        sections = [
            ("الأوامر الأساسية", "بداية - العاب - نقاطي - الصدارة - تسجيل - انسحب - ثيم"),
            ("ألعاب ذهنية", "ذكاء - خمن - رياضيات - ترتيب - ضد - اسرع"),
            ("ألعاب كلمات", "سلسله - انسان حيوان - كون كلمات - اغاني"),
            ("محتوى تفاعلي", "تحدي - سؤال - اعتراف - منشن - موقف - حكمة - شخصية")
        ]
        
        contents = [
            {"type": "text", "text": "المساعدة", "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]
        
        for title, items in sections:
            contents.extend([
                {"type": "text", "text": title, "size": "sm", "weight": "bold", "color": c["text"], "margin": "lg"},
                {"type": "text", "text": items, "size": "xs", "color": c["text_secondary"], "wrap": True, "margin": "xs"}
            ])
        
        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "sm"}
        ])

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="المساعدة", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def stats_card(self, user):
        """بطاقة الإحصائيات"""
        c = self._c()
        win_rate = round((user['wins'] / user['games'] * 100)) if user['games'] > 0 else 0

        stats = [
            ("الاسم", user['name']),
            ("النقاط", str(user['points'])),
            ("الألعاب", str(user['games'])),
            ("الفوز", str(user['wins'])),
            ("نسبة الفوز", f"{win_rate}%")
        ]

        contents = [
            {"type": "text", "text": "إحصائياتي", "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]

        for label, value in stats:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": label, "size": "sm", "color": c["text_secondary"], "flex": 2},
                    {"type": "text", "text": value, "size": "sm", "weight": "bold", "color": c["text"], "align": "end", "flex": 3}
                ],
                "margin": "md",
                "paddingAll": "10px",
                "cornerRadius": "8px",
                "backgroundColor": c["glass"]
            })

        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "sm"}
        ])

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="إحصائياتي", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def leaderboard_card(self, top_users):
        """لوحة الصدارة"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "لوحة الصدارة", "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]

        for i, u in enumerate(top_users, 1):
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": str(i), "size": "sm", "weight": "bold", "color": c["text"], "flex": 1, "align": "center"},
                    {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": u['name'], "size": "sm", "weight": "bold", "color": c["text"]},
                        {"type": "text", "text": f"{u['wins']} فوز", "size": "xs", "color": c["text_tertiary"]}
                    ], "flex": 4},
                    {"type": "text", "text": str(u['points']), "size": "sm", "weight": "bold", "color": c["primary"], "flex": 2, "align": "end"}
                ],
                "margin": "md",
                "paddingAll": "10px",
                "cornerRadius": "8px",
                "backgroundColor": c["glass"]
            })

        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "sm"}
        ])

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def ask_name(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "التسجيل", "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "text", "text": "أدخل اسمك للبدء", "size": "sm", "color": c["text"], "align": "center", "margin": "lg"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="تسجيل", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def ask_name_invalid(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "اسم غير صحيح", "size": "lg", "weight": "bold", "color": c["danger"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "text", "text": "الاسم يجب أن يكون 2-50 حرف", "size": "sm", "color": c["text"], "align": "center", "margin": "lg", "wrap": True}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="خطأ", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def ask_new_name(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "تغيير الاسم", "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "text", "text": "أدخل اسمك الجديد", "size": "sm", "color": c["text"], "align": "center", "margin": "lg"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="تغيير الاسم", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def ask_new_name_invalid(self):
        return self.ask_name_invalid()

    def game_stopped(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "تم إيقاف اللعبة", "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "lg"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="إيقاف", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def registration_required(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "التسجيل مطلوب", "size": "lg", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "تسجيل", "text": "تسجيل"}, "style": "primary", "color": c["primary"], "height": "sm", "margin": "lg"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="تسجيل مطلوب", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())
