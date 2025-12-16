from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config


class UI:
    """واجهة مستخدم محسّنة ومرتبة"""
    
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
        """القائمة الرئيسية الأنيقة"""
        c = self._c()

        contents = [
            {"type": "text", "text": Config.BOT_NAME, "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "text", "text": f"v{Config.VERSION}", "size": "xs", "color": c["text_tertiary"], "align": "center", "margin": "xs"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        if user:
            contents.append({
                "type": "box", "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": user['name'], "size": "md", "weight": "bold", "color": c["text"], "flex": 2},
                    {"type": "text", "text": f"{user['points']}", "size": "lg", "weight": "bold", "color": c["success"], "align": "end", "flex": 1}
                ],
                "margin": "lg", "paddingAll": "14px", "cornerRadius": "10px",
                "backgroundColor": c["glass"], "borderWidth": "2px", "borderColor": c["border"]
            })

        contents.extend([
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "الألعاب", "text": "العاب"}, 
             "style": "primary", "color": c["primary"], "margin": "md", "height": "md"},
            {"type": "box", "layout": "horizontal", "spacing": "md", "margin": "md", "contents": [
                {"type": "button", "action": {"type": "message", "label": "نقاطي" if user else "تسجيل", "text": "نقاطي" if user else "تسجيل"}, 
                 "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "الصدارة", "text": "الصدارة"}, 
                 "style": "secondary", "height": "sm", "flex": 1}
            ]}
        ])

        if user:
            contents.append({"type": "button", "action": {"type": "message", "label": "تغيير الاسم", "text": "تغيير الاسم"}, 
                           "style": "secondary", "height": "sm", "margin": "sm"})

        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": Config.COPYRIGHT, "size": "xxs", "color": c["text_tertiary"], "align": "center", "wrap": True, "margin": "md"}
        ])

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="البداية", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def games_menu(self):
        """قائمة الألعاب المرتبة"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "الألعاب المتاحة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            {"type": "text", "text": "ألعاب بتسجيل", "size": "md", "weight": "bold", "color": c["success"], "margin": "lg"},
            {"type": "box", "layout": "vertical", "spacing": "sm", "margin": "sm", "contents": [
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
            ]},
            
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            {"type": "text", "text": "ألعاب بدون تسجيل", "size": "md", "weight": "bold", "color": c["info"], "margin": "lg"},
            {"type": "box", "layout": "vertical", "spacing": "sm", "margin": "sm", "contents": [
                {"type": "button", "action": {"type": "message", "label": "توافق", "text": "توافق"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "مافيا", "text": "مافيا"}, "style": "secondary", "height": "sm"}
            ]},
            
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "md"}
        ]

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="الألعاب", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def help_menu(self):
        """دليل الاستخدام"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "المساعدة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "الأوامر الأساسية", "size": "md", "weight": "bold", "color": c["text"], "margin": "lg"},
            {"type": "text", "text": "بداية - العاب - نقاطي - الصدارة - تسجيل - انسحب", "size": "sm", "color": c["text_secondary"], "wrap": True, "margin": "sm"},
            {"type": "text", "text": "المحتوى التفاعلي", "size": "md", "weight": "bold", "color": c["text"], "margin": "lg"},
            {"type": "text", "text": "تحدي - سؤال - اعتراف - منشن - موقف - حكمة - شخصية", "size": "sm", "color": c["text_secondary"], "wrap": True, "margin": "sm"},
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "text", "text": Config.COPYRIGHT, "size": "xxs", "color": c["text_tertiary"], "align": "center", "wrap": True, "margin": "md"},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "md"}
        ]

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="المساعدة", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def stats_card(self, user):
        """بطاقة الإحصائيات الأنيقة"""
        c = self._c()
        win_rate = round((user['wins'] / user['games'] * 100)) if user['games'] > 0 else 0

        contents = [
            {"type": "text", "text": "إحصائياتي", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "box", "layout": "vertical", "spacing": "md", "margin": "lg", "contents": [
                self._stat_row("الاسم", user['name'], c),
                self._stat_row("النقاط", str(user['points']), c, True),
                self._stat_row("الألعاب", str(user['games']), c),
                self._stat_row("الفوز", str(user['wins']), c),
                self._stat_row("نسبة الفوز", f"{win_rate}%", c)
            ]},
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "md"}
        ]

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="إحصائياتي", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def _stat_row(self, label, value, c, highlight=False):
        """صف إحصائي أنيق"""
        return {
            "type": "box", "layout": "horizontal",
            "contents": [
                {"type": "text", "text": label, "size": "sm", "color": c["text_secondary"], "flex": 2},
                {"type": "text", "text": value, "size": "md", "weight": "bold", 
                 "color": c["success"] if highlight else c["text"], "align": "end", "flex": 3}
            ],
            "paddingAll": "12px", "cornerRadius": "8px", "backgroundColor": c["glass"]
        }

    def leaderboard_card(self, top_users):
        """لوحة الصدارة الأنيقة"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "لوحة الصدارة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        for i, u in enumerate(top_users, 1):
            medal = "" if i > 3 else ""
            contents.append({
                "type": "box", "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": f"{i}", "size": "lg", "weight": "bold", "color": c["primary"], "flex": 1, "align": "center"},
                    {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": u['name'], "size": "md", "weight": "bold", "color": c["text"]},
                        {"type": "text", "text": f"{u['wins']} فوز", "size": "xs", "color": c["text_tertiary"]}
                    ], "flex": 4},
                    {"type": "text", "text": str(u['points']), "size": "lg", "weight": "bold", "color": c["success"], "flex": 2, "align": "end"}
                ],
                "margin": "md", "paddingAll": "12px", "cornerRadius": "8px", "backgroundColor": c["glass"]
            })

        contents.extend([
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "md"}
        ])

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def ask_name(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "التسجيل", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "أدخل اسمك للبدء", "size": "md", "color": c["text"], "align": "center", "margin": "xl", "wrap": True},
            {"type": "text", "text": "حرف واحد على الأقل", "size": "xs", "color": c["text_tertiary"], "align": "center", "margin": "sm"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="تسجيل", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def ask_name_invalid(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "اسم غير صحيح", "size": "xl", "weight": "bold", "color": c["danger"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "الاسم يجب أن يكون 1-50 حرف", "size": "md", "color": c["text"], "align": "center", "margin": "xl", "wrap": True}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="خطأ", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def ask_new_name(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "تغيير الاسم", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "أدخل اسمك الجديد", "size": "md", "color": c["text"], "align": "center", "margin": "xl"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="تغيير الاسم", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def ask_new_name_invalid(self):
        return self.ask_name_invalid()

    def game_stopped(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "تم إيقاف اللعبة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "البداية", "text": "بداية"}, "style": "secondary", "height": "sm", "margin": "xl"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="إيقاف", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())

    def registration_required(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "التسجيل مطلوب", "size": "xl", "weight": "bold", "color": c["warning"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "يجب التسجيل أولا للعب", "size": "md", "color": c["text"], "align": "center", "margin": "lg"},
            {"type": "button", "action": {"type": "message", "label": "تسجيل", "text": "تسجيل"}, "style": "primary", "color": c["primary"], "height": "md", "margin": "xl"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "24px", "backgroundColor": c["bg"]}}
        return FlexMessage(alt_text="تسجيل مطلوب", contents=FlexContainer.from_dict(bubble), quickReply=self._quick_reply())
