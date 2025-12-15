from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from config import Config


class UI:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    def _btn(self, label: str, action: str, style: str = "secondary"):
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": action},
            "style": style,
            "height": "sm"
        }

    def _glass_box(self, contents, padding: str = "16px"):
        c = self._c()
        return {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": c["glass"],
            "cornerRadius": "16px",
            "paddingAll": padding,
            "contents": contents
        }

    def _header(self, text: str):
        c = self._c()
        return {
            "type": "text",
            "text": text,
            "size": "xl",
            "weight": "bold",
            "color": c["primary"],
            "align": "center"
        }

    def _bubble(self, contents):
        c = self._c()
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["bg"],
                "paddingAll": "20px",
                "spacing": "md",
                "contents": contents
            }
        }

    def main_menu(self, user):
        c = self._c()

        if not user:
            contents = [
                self._header(Config.BOT_NAME),
                self._glass_box([
                    {"type": "text", "text": "مرحبا", "align": "center", "size": "lg", "color": c["text"]},
                    {"type": "text", "text": "غير مسجل", "align": "center", "size": "sm",
                     "color": c["warning"], "margin": "sm"}
                ]),
                {"type": "separator", "margin": "lg"},
                self._glass_box([
                    {"type": "text", "text": "النصوص", "size": "sm", "color": c["text_tertiary"]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                     "contents": [self._btn("تحدي", "تحدي"), self._btn("اعتراف", "اعتراف")]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                     "contents": [self._btn("منشن", "منشن"), self._btn("سؤال", "سؤال")]}
                ], "12px"),
                {"type": "separator", "margin": "md"},
                self._btn("تسجيل", "تسجيل", "primary")
            ]
        else:
            contents = [
                self._header(Config.BOT_NAME),
                self._glass_box([
                    {"type": "text", "text": f"مرحبا {user['name']}", "align": "center",
                     "size": "lg", "color": c["text"], "weight": "bold"},
                    {"type": "text", "text": f"النقاط {user['points']}", "align": "center",
                     "size": "md", "color": c["primary"], "margin": "sm"}
                ]),
                {"type": "separator", "margin": "lg"},
                self._glass_box([
                    {"type": "text", "text": "القوائم", "size": "sm", "color": c["text_tertiary"]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                     "contents": [self._btn("الالعاب", "العاب"), self._btn("نقاطي", "نقاطي")]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                     "contents": [self._btn("الصداره", "الصداره"), self._btn("تغيير الاسم", "تغيير")]}
                ], "12px"),
                {"type": "separator", "margin": "md"},
                self._glass_box([
                    {"type": "text", "text": "النصوص", "size": "sm", "color": c["text_tertiary"]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                     "contents": [self._btn("تحدي", "تحدي"), self._btn("اعتراف", "اعتراف")]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                     "contents": [self._btn("منشن", "منشن"), self._btn("سؤال", "سؤال")]}
                ], "12px"),
                {"type": "separator", "margin": "md"},
                self._btn(f"الوضع {'الفاتح' if self.theme == 'dark' else 'الداكن'}", "تغيير_الثيم")
            ]

        contents.append({
            "type": "text",
            "text": f"{Config.BOT_NAME} v{Config.VERSION}",
            "size": "xxs",
            "color": c["text_tertiary"],
            "align": "center",
            "margin": "lg"
        })

        return FlexMessage(
            alt_text="القائمه الرئيسيه",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )

    def games_menu(self):
        c = self._c()

        games = [
            ("ذكاء", "الغاز ذكاء"),
            ("خمن", "خمن الكلمه"),
            ("رياضيات", "عمليات حسابيه"),
            ("ترتيب", "رتب الحروف"),
            ("ضد", "عكس الكلمه"),
            ("اسرع", "اكتب بسرعه"),
            ("انسان", "انسان حيوان نبات"),
            ("سلسله", "سلسلة الكلمات"),
            ("تكوين", "كون كلمات"),
            ("لون", "لون الكلمه"),
            ("اغنيه", "من المغني")
        ]

        cards = []
        for title, desc in games:
            cards.append({
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["glass"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "margin": "sm",
                "action": {"type": "message", "label": title, "text": title},
                "contents": [
                    {"type": "text", "text": title, "weight": "bold", "color": c["primary"], "size": "md"},
                    {"type": "text", "text": desc, "color": c["text_secondary"], "size": "xs", "margin": "xs"}
                ]
            })

        contents = [
            self._header("الالعاب"),
            {"type": "separator", "margin": "md"}
        ] + cards + [
            {"type": "separator", "margin": "md"},
            self._btn("رجوع", "بدايه")
        ]

        return FlexMessage(
            alt_text="قائمه الالعاب",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )

    def stats_card(self, user):
        c = self._c()

        win_rate = int((user['wins'] / user['games'] * 100)) if user['games'] > 0 else 0

        contents = [
            self._header("احصائياتي"),
            {"type": "separator", "margin": "md"},
            self._glass_box([
                {"type": "text", "text": user['name'], "weight": "bold",
                 "size": "lg", "color": c["text"], "align": "center"},
                {"type": "box", "layout": "horizontal", "margin": "md",
                 "contents": [
                     self._stat("النقاط", user['points'], c["primary"]),
                     {"type": "separator"},
                     self._stat("الالعاب", user['games'], c["text"]),
                     {"type": "separator"},
                     self._stat("الفوز", user['wins'], c["success"])
                 ]},
                {"type": "box", "layout": "vertical", "margin": "md",
                 "contents": [
                     {"type": "text", "text": "نسبة الفوز", "size": "xs",
                      "color": c["text_tertiary"], "align": "center"},
                     {"type": "text", "text": f"{win_rate}%", "size": "xl", "weight": "bold",
                      "color": c["primary"], "align": "center"}
                 ]}
            ]),
            {"type": "separator", "margin": "md"},
            self._btn("رجوع", "بدايه")
        ]

        return FlexMessage(
            alt_text="احصائياتي",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )

    def _stat(self, label, value, color):
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": label, "size": "xs", "color": self._c()["text_tertiary"], "align": "center"},
                {"type": "text", "text": str(value), "size": "xl", "weight": "bold",
                 "color": color, "align": "center"}
            ]
        }

    def leaderboard_card(self, leaders):
        c = self._c()

        if not leaders:
            contents = [
                self._header("الصداره"),
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": "لا يوجد لاعبون بعد",
                 "align": "center", "color": c["text_secondary"], "margin": "md"},
                {"type": "separator", "margin": "md"},
                self._btn("رجوع", "بدايه")
            ]
        else:
            rows = []
            for i, (name, points) in enumerate(leaders[:10], 1):
                medal = "1" if i == 1 else "2" if i == 2 else "3" if i == 3 else f"{i}."
                rows.append({
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "sm",
                    "contents": [
                        {"type": "text", "text": medal, "flex": 1, "size": "sm", "color": c["text"]},
                        {"type": "text", "text": name, "flex": 4, "size": "sm", "color": c["text"]},
                        {"type": "text", "text": str(points), "flex": 2,
                         "align": "end", "size": "sm", "weight": "bold", "color": c["primary"]}
                    ]
                })

            contents = [
                self._header("الصداره"),
                {"type": "separator", "margin": "md"},
                self._glass_box(rows, "12px"),
                {"type": "separator", "margin": "md"},
                self._btn("رجوع", "بدايه")
            ]

        return FlexMessage(
            alt_text="لوحه الصداره",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )

    def ask_name(self):
        return TextMessage(text="اكتب اسمك")

    def game_stopped(self):
        return TextMessage(text="تم الانسحاب من اللعبه")
