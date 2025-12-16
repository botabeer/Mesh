from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
from config import Config


class UI:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        """الحصول على ألوان الثيم الحالي"""
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

    # ------------------- القائمة الرئيسية -------------------
    def main_menu(self, user=None):
        c = self._c()
        theme_name = "فاتح" if self.theme == "light" else "داكن"

        contents = [
            {"type": "text", "text": Config.BOT_NAME, "size": "xxl", "weight": "bold",
             "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        if user:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": f"مرحبا {user['name']}", "size": "lg",
                     "weight": "bold", "color": c["text"], "flex": 3},
                    {"type": "text", "text": f"{user['points']} نقطة", "size": "md",
                     "weight": "bold", "color": c["success"], "align": "end", "flex": 2}
                ],
                "margin": "lg", "paddingAll": "12px", "cornerRadius": "12px",
                "borderWidth": "1px", "borderColor": c["border"]
            })

        # الألعاب
        contents.extend([
            {"type": "text", "text": "الالعاب", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm",
             "contents": [
                 {"type": "button", "action": {"type": "message", "label": "العاب", "text": "العاب"},
                  "style": "primary", "color": c["primary"], "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "انسحب", "text": "انسحب"},
                  "style": "secondary", "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "ايقاف", "text": "ايقاف"},
                  "style": "secondary", "height": "sm"}
             ]}
        ])

        # محتوى تفاعلي
        contents.extend([
            {"type": "text", "text": "محتوى تفاعلي", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm",
             "contents": [
                 {"type": "button", "action": {"type": "message", "label": "تحدي", "text": "تحدي"},
                  "style": "secondary", "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "سؤال", "text": "سؤال"},
                  "style": "secondary", "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "اعتراف", "text": "اعتراف"},
                  "style": "secondary", "height": "sm"}
             ]}
        ])

        # الملف الشخصي
        contents.extend([
            {"type": "text", "text": "الملف الشخصي", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm",
             "contents": [
                 {"type": "button", "action": {"type": "message",
                                               "label": "نقاطي" if user else "تسجيل",
                                               "text": "نقاطي" if user else "تسجيل"},
                  "style": "primary" if not user else "secondary",
                  "color": c["primary"] if not user else None, "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "الصدارة", "text": "الصدارة"},
                  "style": "secondary", "height": "sm"}
             ]}
        ])

        # الإعدادات
        if user:
            contents.extend([
                {"type": "text", "text": "الإعدادات", "size": "md", "weight": "bold",
                 "color": c["text_secondary"], "margin": "lg"},
                {"type": "box", "layout": "horizontal", "spacing": "sm",
                 "contents": [
                     {"type": "button", "action": {"type": "message", "label": f"الوضع {theme_name}", "text": "ثيم"},
                      "style": "secondary", "height": "sm"},
                     {"type": "button", "action": {"type": "message", "label": "تغيير الاسم", "text": "تغيير الاسم"},
                      "style": "secondary", "height": "sm"}
                 ]}
            ])

        # نسخة + separator
        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": f"v{Config.VERSION}", "size": "xxs",
             "color": c["text_tertiary"], "align": "center", "margin": "md"}
        ])

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {"type": "box", "layout": "vertical", "contents": contents,
                     "paddingAll": "20px", "spacing": "md", "backgroundColor": c["bg"]}
        }

        return FlexMessage(
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    # ------------------- قائمة الألعاب -------------------
    def games_menu(self):
        c = self._c()

        contents = [
            {"type": "text", "text": "الالعاب المتاحة", "size": "xxl",
             "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "العاب ذهنية", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm",
             "contents": [
                 {"type": "button", "action": {"type": "message", "label": "ذكاء", "text": "ذكاء"},
                  "style": "primary", "color": c["primary"], "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "خمن", "text": "خمن"},
                  "style": "primary", "color": c["secondary"], "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "رياضيات", "text": "رياضيات"},
                  "style": "primary", "color": c["success"], "height": "sm"}
             ]},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
             "contents": [
                 {"type": "button", "action": {"type": "message", "label": "ترتيب", "text": "ترتيب"},
                  "style": "secondary", "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "ضد", "text": "ضد"},
                  "style": "secondary", "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "اسرع", "text": "اسرع"},
                  "style": "secondary", "height": "sm"}
             ]},
            {"type": "text", "text": "العاب كلمات", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm",
             "contents": [
                 {"type": "button", "action": {"type": "message", "label": "سلسلة", "text": "سلسله"},
                  "style": "secondary", "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "انسان حيوان", "text": "انسان حيوان"},
                  "style": "secondary", "height": "sm"}
             ]},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
             "contents": [
                 {"type": "button", "action": {"type": "message", "label": "كون كلمات", "text": "كون كلمات"},
                  "style": "secondary", "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "اغاني", "text": "اغاني"},
                  "style": "secondary", "height": "sm"}
             ]},
            {"type": "text", "text": "العاب اخرى", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm",
             "contents": [
                 {"type": "button", "action": {"type": "message", "label": "الوان", "text": "الوان"},
                  "style": "secondary", "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "مافيا", "text": "مافيا"},
                  "style": "secondary", "height": "sm"},
                 {"type": "button", "action": {"type": "message", "label": "توافق", "text": "توافق"},
                  "style": "secondary", "height": "sm"}
             ]},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "العودة", "text": "بداية"},
             "style": "primary", "color": c["primary"], "height": "sm", "margin": "md"}
        ]

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {"type": "box", "layout": "vertical", "contents": contents,
                     "paddingAll": "20px", "spacing": "md", "backgroundColor": c["bg"]}
        }

        return FlexMessage(
            alt_text="الالعاب",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    # ------------------- مساعدة -------------------
    def help_menu(self):
        c = self._c()
        sections = [
            ("الاوامر الرئيسية", "بداية - تسجيل - العاب - نقاطي - الصدارة - انسحب - ثيم"),
            ("العاب ذهنية", "ذكاء - خمن - رياضيات - ترتيب - ضد - اسرع"),
            ("العاب كلمات", "سلسله - انسان حيوان - كون كلمات - اغاني"),
            ("العاب اخرى", "الوان - مافيا - توافق"),
            ("محتوى تفاعلي", "تحدي - سؤال - اعتراف - منشن - موقف - حكمة - شخصية"),
            ("اوامر اللعبة", "انسحب - ايقاف"),
        ]

        contents = [
            {"type": "text", "text": "المساعدة", "size": "xxl", "weight": "bold",
             "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        for title, items in sections:
            contents.extend([
                {"type": "text", "text": title, "size": "md", "weight": "bold",
                 "color": c["text_secondary"], "margin": "lg"},
                {"type": "text", "text": items, "size": "sm", "color": c["text"], "wrap": True}
            ])

        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "العودة", "text": "بداية"},
             "style": "primary", "color": c["primary"], "height": "sm", "margin": "md"}
        ])

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {"type": "box", "layout": "vertical", "contents": contents,
                     "paddingAll": "20px", "spacing": "md", "backgroundColor": c["bg"]}
        }

        return FlexMessage(
            alt_text="المساعدة",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    # ------------------- احصائيات -------------------
    def stats_card(self, user):
        c = self._c()
        win_rate = round((user['wins'] / user['games'] * 100)) if user['games'] > 0 else 0

        contents = [
            {"type": "text", "text": "احصائياتي", "size": "xxl", "weight": "bold",
             "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": "الاسم", "size": "sm", "color": c["text_secondary"], "flex": 2},
                {"type": "text", "text": user['name'], "size": "sm", "weight": "bold", "color": c["text"],
                 "align": "end", "flex": 3}
            ], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": "النقاط", "size": "sm", "color": c["text_secondary"], "flex": 2},
                {"type": "text", "text": str(user['points']), "size": "sm", "weight": "bold",
                 "color": c["success"], "align": "end", "flex": 3}
            ], "margin": "md"},
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": "الالعاب", "size": "sm", "color": c["text_secondary"], "flex": 2},
                {"type": "text", "text": str(user['games']), "size": "sm", "weight": "bold",
                 "color": c["text"], "align": "end", "flex": 3}
            ], "margin": "md"},
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": "الفوز", "size": "sm", "color": c["text_secondary"], "flex": 2},
                {"type": "text", "text": str(user['wins']), "size": "sm", "weight": "bold",
                 "color": c["text"], "align": "end", "flex": 3}
            ], "margin": "md"},
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": "نسبة الفوز", "size": "sm", "color": c["text_secondary"], "flex": 2},
                {"type": "text", "text": f"{win_rate}%", "size": "sm", "weight": "bold",
                 "color": c["info"], "align": "end", "flex": 3}
            ], "margin": "md"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "button", "action": {"type": "message", "label": "العودة", "text": "بداية"},
             "style": "primary", "color": c["primary"], "height": "sm", "margin": "md"}
        ]

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical",
                                                            "contents": contents, "paddingAll": "20px",
                                                            "spacing": "md", "backgroundColor": c["bg"]}}

        return FlexMessage(
            alt_text="احصائياتي",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    # ------------------- لوحة الصدارة -------------------
    def leaderboard_card(self, top_users):
        c = self._c()
        contents = [
            {"type": "text", "text": "الصدارة", "size": "xxl", "weight": "bold",
             "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        for i, u in enumerate(top_users, 1):
            contents.append({
                "type": "text", "text": f"{i}. {u['name']} - {u['points']} نقطة", "size": "sm",
                "color": c["text"], "margin": "sm"
            })

        contents.append({"type": "separator", "margin": "lg", "color": c["border"]})
        contents.append({"type": "button", "action": {"type": "message", "label": "العودة", "text": "بداية"},
                         "style": "primary", "color": c["primary"], "height": "sm", "margin": "md"})

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical",
                                                            "contents": contents, "paddingAll": "20px",
                                                            "spacing": "md", "backgroundColor": c["bg"]}}

        return FlexMessage(
            alt_text="الصدارة",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._quick_reply()
        )

    # ------------------- تسجيل الاسم -------------------
    def ask_name(self):
        c = self._c()
        return FlexMessage(
            alt_text="تسجيل الاسم",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "size": "mega",
                "body": {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "أدخل اسمك للبدء", "size": "lg", "weight": "bold",
                     "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]}
                ], "paddingAll": "20px", "spacing": "md", "backgroundColor": c["bg"]}
            }),
            quickReply=self._quick_reply()
        )

    def ask_new_name(self):
        c = self._c()
        return FlexMessage(
            alt_text="تغيير الاسم",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "size": "mega",
                "body": {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "أدخل اسمك الجديد", "size": "lg", "weight": "bold",
                     "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]}
                ], "paddingAll": "20px", "spacing": "md", "backgroundColor": c["bg"]}
            }),
            quickReply=self._quick_reply()
        )

    # ------------------- اللعبة أوقفت -------------------
    def game_stopped(self):
        c = self._c()
        return FlexMessage(
            alt_text="تم ايقاف اللعبة",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "size": "mega",
                "body": {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "تم ايقاف اللعبة", "size": "lg", "weight": "bold",
                     "color": c["error"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]}
                ], "paddingAll": "20px", "spacing": "md", "backgroundColor": c["bg"]}
            }),
            quickReply=self._quick_reply()
        )

    def registration_required(self):
        c = self._c()
        return FlexMessage(
            alt_text="التسجيل مطلوب",
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "size": "mega",
                "body": {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "يرجى التسجيل أولاً", "size": "lg", "weight": "bold",
                     "color": c["warning"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]}
                ], "paddingAll": "20px", "spacing": "md", "backgroundColor": c["bg"]}
            }),
            quickReply=self._quick_reply()
        )
