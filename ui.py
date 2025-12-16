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

    def _create_bubble(self, contents):
        c = self._c()
        return {
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

    def _create_button(self, label, text, style="secondary", color=None):
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": style,
            "color": color,
            "height": "sm"
        }

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
                "type": "box", "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": f"مرحبا {user['name']}", "size": "lg",
                     "weight": "bold", "color": c["text"], "flex": 3},
                    {"type": "text", "text": f"{user['points']} نقطة", "size": "md",
                     "weight": "bold", "color": c["success"], "align": "end", "flex": 2}
                ],
                "margin": "lg", "paddingAll": "12px", "cornerRadius": "12px",
                "borderWidth": "1px", "borderColor": c["border"]
            })

        contents.extend([
            {"type": "text", "text": "الالعاب", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                self._create_button("العاب", "العاب", "primary", c["primary"]),
                self._create_button("انسحب", "انسحب"),
                self._create_button("ايقاف", "ايقاف")
            ]},
            {"type": "text", "text": "محتوى تفاعلي", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                self._create_button("تحدي", "تحدي"),
                self._create_button("سؤال", "سؤال"),
                self._create_button("اعتراف", "اعتراف")
            ]},
            {"type": "text", "text": "الملف الشخصي", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                self._create_button("نقاطي" if user else "تسجيل",
                                  "نقاطي" if user else "تسجيل",
                                  "primary" if not user else "secondary",
                                  c["primary"] if not user else None),
                self._create_button("الصدارة", "الصدارة")
            ]}
        ])

        if user:
            contents.extend([
                {"type": "text", "text": "الإعدادات", "size": "md", "weight": "bold",
                 "color": c["text_secondary"], "margin": "lg"},
                {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                    self._create_button(f"الوضع {theme_name}", "ثيم"),
                    self._create_button("تغيير الاسم", "تغيير الاسم")
                ]}
            ])

        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": f"v{Config.VERSION}", "size": "xxs",
             "color": c["text_tertiary"], "align": "center", "margin": "md"}
        ])

        return FlexMessage(
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def games_menu(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "الالعاب المتاحة", "size": "xxl",
             "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "العاب ذهنية", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                self._create_button("ذكاء", "ذكاء", "primary", c["primary"]),
                self._create_button("خمن", "خمن", "primary", c["secondary"]),
                self._create_button("رياضيات", "رياضيات", "primary", c["success"])
            ]},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                self._create_button("ترتيب", "ترتيب"),
                self._create_button("ضد", "ضد"),
                self._create_button("اسرع", "اسرع")
            ]},
            {"type": "text", "text": "العاب كلمات", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                self._create_button("سلسلة", "سلسله"),
                self._create_button("انسان حيوان", "انسان حيوان")
            ]},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                self._create_button("كون كلمات", "كون كلمات"),
                self._create_button("اغاني", "اغاني")
            ]},
            {"type": "text", "text": "العاب اخرى", "size": "md", "weight": "bold",
             "color": c["text_secondary"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                self._create_button("الوان", "الوان"),
                self._create_button("مافيا", "مافيا"),
                self._create_button("توافق", "توافق")
            ]},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            self._create_button("العودة", "بداية", "primary", c["primary"])
        ]
        contents[-1]["margin"] = "md"

        return FlexMessage(
            alt_text="الالعاب",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
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
            ("اوامر اللعبة", "انسحب - ايقاف")
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
            self._create_button("العودة", "بداية", "primary", c["primary"])
        ])
        contents[-1]["margin"] = "md"

        return FlexMessage(
            alt_text="المساعدة",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def stats_card(self, user):
        c = self._c()
        win_rate = round((user['wins'] / user['games'] * 100)) if user['games'] > 0 else 0
        stats = [
            ("الاسم", user['name'], c["text"]),
            ("النقاط", str(user['points']), c["success"]),
            ("الالعاب", str(user['games']), c["text"]),
            ("الفوز", str(user['wins']), c["text"]),
            ("نسبة الفوز", f"{win_rate}%", c["info"])
        ]

        contents = [
            {"type": "text", "text": "احصائياتي", "size": "xxl", "weight": "bold",
             "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        for i, (label, value, color) in enumerate(stats):
            contents.append({
                "type": "box", "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": label, "size": "sm", "color": c["text_secondary"], "flex": 2},
                    {"type": "text", "text": value, "size": "sm", "weight": "bold",
                     "color": color, "align": "end", "flex": 3}
                ],
                "margin": "lg" if i == 0 else "md"
            })

        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            self._create_button("العودة", "بداية", "primary", c["primary"])
        ])
        contents[-1]["margin"] = "md"

        return FlexMessage(
            alt_text="احصائياتي",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def leaderboard_card(self, top_users):
        c = self._c()
        contents = [
            {"type": "text", "text": "الصدارة", "size": "xxl", "weight": "bold",
             "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        for i, u in enumerate(top_users, 1):
            contents.append({
                "type": "text", "text": f"{i}. {u['name']} - {u['points']} نقطة",
                "size": "sm", "color": c["text"], "margin": "sm"
            })

        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            self._create_button("العودة", "بداية", "primary", c["primary"])
        ])
        contents[-1]["margin"] = "md"

        return FlexMessage(
            alt_text="الصدارة",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def ask_name(self):
        c = self._c()
        return FlexMessage(
            alt_text="تسجيل الاسم",
            contents=FlexContainer.from_dict(self._create_bubble([
                {"type": "text", "text": "أدخل اسمك للبدء", "size": "lg",
                 "weight": "bold", "color": c["primary"], "align": "center"},
                {"type": "separator", "margin": "lg", "color": c["border"]}
            ])),
            quickReply=self._quick_reply()
        )

    def ask_name_invalid(self):
        c = self._c()
        return FlexMessage(
            alt_text="اسم غير صالح",
            contents=FlexContainer.from_dict(self._create_bubble([
                {"type": "text", "text": "اسم غير صالح", "size": "lg",
                 "weight": "bold", "color": c["error"], "align": "center"},
                {"type": "text", "text": "يرجى إدخال اسم صحيح", "size": "sm",
                 "color": c["text_secondary"], "align": "center", "margin": "md"}
            ])),
            quickReply=self._quick_reply()
        )

    def ask_new_name(self):
        c = self._c()
        return FlexMessage(
            alt_text="تغيير الاسم",
            contents=FlexContainer.from_dict(self._create_bubble([
                {"type": "text", "text": "أدخل اسمك الجديد", "size": "lg",
                 "weight": "bold", "color": c["primary"], "align": "center"},
                {"type": "separator", "margin": "lg", "color": c["border"]}
            ])),
            quickReply=self._quick_reply()
        )

    def ask_new_name_invalid(self):
        c = self._c()
        return FlexMessage(
            alt_text="اسم جديد غير صالح",
            contents=FlexContainer.from_dict(self._create_bubble([
                {"type": "text", "text": "اسم غير صالح", "size": "lg",
                 "weight": "bold", "color": c["error"], "align": "center"},
                {"type": "text", "text": "يرجى إدخال اسم صحيح", "size": "sm",
                 "color": c["text_secondary"], "align": "center", "margin": "md"}
            ])),
            quickReply=self._quick_reply()
        )

    def game_stopped(self):
        c = self._c()
        return FlexMessage(
            alt_text="تم ايقاف اللعبة",
            contents=FlexContainer.from_dict(self._create_bubble([
                {"type": "text", "text": "تم ايقاف اللعبة", "size": "lg",
                 "weight": "bold", "color": c["error"], "align": "center"},
                {"type": "separator", "margin": "lg", "color": c["border"]}
            ])),
            quickReply=self._quick_reply()
        )

    def registration_required(self):
        c = self._c()
        return FlexMessage(
            alt_text="التسجيل مطلوب",
            contents=FlexContainer.from_dict(self._create_bubble([
                {"type": "text", "text": "يرجى التسجيل أولاً", "size": "lg",
                 "weight": "bold", "color": c["warning"], "align": "center"},
                {"type": "separator", "margin": "lg", "color": c["border"]}
            ])),
            quickReply=self._quick_reply()
        )
