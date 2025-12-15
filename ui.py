from linebot.v3.messaging import FlexMessage, FlexContainer
from config import Config


class UI:
    """واجهة المستخدم (Flex Safe v3)"""

    def __init__(self, theme: str = "light"):
        self.theme = theme

    def set_theme(self, theme: str):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    # ---------- Components ----------

    def _btn(self, label: str, action: str, style: str = "secondary"):
        return {
            "type": "button",
            "action": {
                "type": "message",
                "label": label,
                "text": action
            },
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

    def _header(self, text: str, size: str = "xl"):
        c = self._c()
        return {
            "type": "text",
            "text": text,
            "size": size,
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

    # ---------- Screens ----------

    def main_menu(self, user):
        c = self._c()

        if not user:
            contents = [
                self._header(Config.BOT_NAME),
                self._glass_box([
                    {"type": "text", "text": "مرحبًا", "align": "center", "size": "lg", "color": c["text"]},
                    {"type": "text", "text": "غير مسجل", "align": "center", "size": "sm",
                     "color": c["warning"], "margin": "sm"}
                ]),
                {"type": "separator", "margin": "lg"},
                self._btn("تسجيل", "تسجيل", "primary")
            ]
        else:
            contents = [
                self._header(Config.BOT_NAME),
                self._glass_box([
                    {"type": "text", "text": f"مرحبًا {user['name']}", "align": "center",
                     "size": "lg", "color": c["text"], "weight": "bold"},
                    {"type": "text", "text": f"النقاط: {user['points']}", "align": "center",
                     "size": "md", "color": c["primary"], "margin": "sm"}
                ]),
                {"type": "separator", "margin": "lg"},
                self._glass_box([
                    {"type": "text", "text": "القوائم", "size": "sm", "color": c["text_tertiary"]},
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                        "contents": [self._btn("الألعاب", "العاب"), self._btn("نقاطي", "نقاطي")]
                    },
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                        "contents": [self._btn("الصدارة", "الصداره"), self._btn("تغيير الاسم", "تغيير")]
                    }
                ], "12px"),
                {"type": "separator", "margin": "md"},
                self._btn(
                    f"الوضع {'الفاتح' if self.theme == 'dark' else 'الداكن'}",
                    "تغيير_الثيم"
                )
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
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )

    def games_menu(self):
        c = self._c()

        games = [
            ("ذكاء", "ألغاز ذكاء"),
            ("خمن", "خمن الكلمة"),
            ("رياضيات", "عمليات حسابية")
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
            self._header("الألعاب"),
            {"type": "separator", "margin": "md"}
        ] + cards + [
            {"type": "separator", "margin": "md"},
            self._btn("رجوع", "بداية")
        ]

        return FlexMessage(
            alt_text="قائمة الألعاب",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )

    def stats_card(self, user):
        c = self._c()

        contents = [
            self._header("إحصائياتي"),
            {"type": "separator", "margin": "md"},
            self._glass_box([
                {"type": "text", "text": user['name'], "weight": "bold",
                 "size": "lg", "color": c["text"], "align": "center"},
                {
                    "type": "box", "layout": "horizontal", "margin": "md",
                    "contents": [
                        self._stat("النقاط", user['points'], c["primary"]),
                        {"type": "separator"},
                        self._stat("الألعاب", user['games'], c["text"]),
                        {"type": "separator"},
                        self._stat("الفوز", user['wins'], c["success"])
                    ]
                }
            ]),
            {"type": "separator", "margin": "md"},
            self._btn("رجوع", "بداية")
        ]

        return FlexMessage(
            alt_text="إحصائياتي",
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
                self._header("الصدارة"),
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": "لا يوجد لاعبون بعد",
                 "align": "center", "color": c["text_secondary"], "margin": "md"},
                {"type": "separator", "margin": "md"},
                self._btn("رجوع", "بداية")
            ]
        else:
            rows = []
            for i, (name, points) in enumerate(leaders[:10], 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
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
                self._header("الصدارة"),
                {"type": "separator", "margin": "md"},
                self._glass_box(rows, "12px"),
                {"type": "separator", "margin": "md"},
                self._btn("رجوع", "بداية")
            ]

        return FlexMessage(
            alt_text="لوحة الصدارة",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )
