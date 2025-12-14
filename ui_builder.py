from typing import List, Dict
from config import Config


class UIBuilder:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _colors(self) -> Dict[str, str]:
        return Config.get_theme(self.theme)

    def _section_title(self, text: str) -> Dict:
        return {
            "type": "text",
            "text": text,
            "weight": "bold",
            "size": "md",
            "margin": "md",
            "color": self._colors()["primary"]
        }

    def _two_buttons(self, text1: str, action1: str, text2: str, action2: str) -> Dict:
        c = self._colors()
        return {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {"type": "message", "label": text1, "text": action1},
                    "color": c["secondary"]
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {"type": "message", "label": text2, "text": action2},
                    "color": c["secondary"]
                }
            ]
        }

    def _theme_toggle_button(self) -> Dict:
        c = self._colors()
        label = "الوضع الداكن" if self.theme != "dark" else "الوضع الفاتح"
        return {
            "type": "button",
            "style": "secondary",
            "height": "sm",
            "action": {"type": "message", "label": label, "text": "تغيير_الثيم"},
            "color": c["secondary"],
            "margin": "sm"
        }

    def _footer(self) -> Dict:
        c = self._colors()
        return {
            "type": "text",
            "text": "تم انشاء هذا البوت بواسطة\nعبير الدوسري 2025",
            "align": "center",
            "size": "xs",
            "color": c["text3"],
            "margin": "lg"
        }

    def welcome_card(self, name: str, registered: bool):
        c = self._colors()
        status = f"{name} مسجل" if registered else f"{name} غير مسجل"
        status_color = c["success"] if registered else c["warning"]

        contents = [
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "cornerRadius": "16px",
                "paddingAll": "16px",
                "contents": [
                    {"type": "text", "text": "Bot Mesh", "align": "center", "weight": "bold", "size": "xl", "color": c["primary"]}
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "8px",
                "contents": [
                    {"type": "text", "text": "مرحبا", "align": "center", "weight": "bold", "size": "lg", "color": c["primary"]},
                    {"type": "text", "text": status, "align": "center", "color": status_color, "size": "sm"}
                ]
            }
        ]

        if registered:
            contents.extend([
                self._section_title("الحساب"),
                self._two_buttons("تغيير الاسم", "تغيير", "نقاطي", "نقاطي"),
                self._section_title("الاعدادات"),
                self._theme_toggle_button(),
                self._section_title("الاحصائيات"),
                self._two_buttons("الصدارة", "الصدارة", "مساعدة", "مساعدة"),
                self._section_title("القوائم"),
                {"type": "button", "style": "primary", "height": "sm",
                 "action": {"type": "message", "label": "الالعاب", "text": "العاب"},
                 "color": c["primary"], "margin": "sm"}
            ])
        else:
            contents.extend([
                self._section_title("ابدأ الآن"),
                {"type": "button", "style": "primary", "height": "sm",
                 "action": {"type": "message", "label": "تسجيل", "text": "تسجيل"},
                 "color": c["primary"], "margin": "sm"}
            ])

        contents.append(self._footer())

        return {"type": "bubble", "styles": {"body": {"backgroundColor": c["bg"]}},
                "body": {"type": "box", "layout": "vertical", "spacing": "md", "contents": contents}}

    def games_menu_card(self):
        c = self._colors()
        games = [
            ["ذكاء", "خمن", "ضد"],
            ["ترتيب", "رياضيات", "اغنيه"],
            ["لون", "تكوين", "لعبة"],
            ["سلسلة", "اسرع", "توافق"],
            ["مافيا", "سؤال", "منشن"]
        ]

        buttons = []
        for row in games:
            row_buttons = {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": []}
            for game in row:
                row_buttons["contents"].append({"type": "button", "style": "secondary", "height": "sm",
                                                "action": {"type": "message", "label": game, "text": game},
                                                "color": c["secondary"]})
            buttons.append(row_buttons)

        contents = [{"type": "box", "layout": "vertical", "backgroundColor": c["card"], "cornerRadius": "16px",
                     "paddingAll": "16px", "contents": [{"type": "text", "text": "الالعاب",
                                                          "align": "center", "weight": "bold", "size": "xl",
                                                          "color": c["primary"]}]}] + buttons + [
                       {"type": "button", "style": "primary", "height": "sm",
                        "action": {"type": "message", "label": "رجوع", "text": "بداية"},
                        "color": c["primary"], "margin": "md"}]

        return {"type": "bubble", "styles": {"body": {"backgroundColor": c["bg"]}},
                "body": {"type": "box", "layout": "vertical", "spacing": "md", "contents": contents}}

    def leaderboard_card(self, leaders: List[tuple]):
        c = self._colors()
        items = []
        for i, (name, pts) in enumerate(leaders[:10]):
            items.append({"type": "box", "layout": "horizontal", "margin": "sm", "backgroundColor": c["card"],
                          "cornerRadius": "8px", "paddingAll": "8px",
                          "contents": [
                              {"type": "text", "text": str(i + 1), "size": "sm", "color": c["text"], "flex": 0,
                               "weight": "bold"},
                              {"type": "text", "text": name, "size": "sm", "color": c["text"], "flex": 3, "margin": "sm"},
                              {"type": "text", "text": str(pts), "size": "sm", "color": c["primary"], "weight": "bold",
                               "flex": 1, "align": "end"}
                          ]})

        contents = [{"type": "box", "layout": "vertical", "backgroundColor": c["card"], "cornerRadius": "16px",
                     "paddingAll": "16px", "contents": [{"type": "text", "text": "لوحة الصدارة",
                                                          "align": "center", "weight": "bold", "size": "xl",
                                                          "color": c["primary"]}]}] + \
                   [{"type": "box", "layout": "vertical", "spacing": "sm", "contents": items}] + \
                   [{"type": "button", "style": "primary", "height": "sm",
                     "action": {"type": "message", "label": "رجوع", "text": "بداية"},
                     "color": c["primary"], "margin": "md"}]

        return {"type": "bubble", "styles": {"body": {"backgroundColor": c["bg"]}},
                "body": {"type": "box", "layout": "vertical", "spacing": "md", "contents": contents}}

    def stats_card(self, name: str, user_data: dict):
        c = self._colors()
        points = user_data.get("total_points", 0)
        games = user_data.get("games_played", 0)
        wins = user_data.get("wins", 0)

        contents = [
            {"type": "box", "layout": "vertical", "backgroundColor": c["card"], "cornerRadius": "16px",
             "paddingAll": "16px",
             "contents": [{"type": "text", "text": "احصائياتي", "align": "center", "weight": "bold", "size": "xl",
                           "color": c["primary"]}]},
            {"type": "box", "layout": "vertical", "backgroundColor": c["card"], "cornerRadius": "12px",
             "paddingAll": "16px", "spacing": "sm",
             "contents": [
                 {"type": "text", "text": f"الاسم: {name}", "size": "md", "color": c["text"]},
                 {"type": "text", "text": f"النقاط: {points}", "size": "lg", "color": c["primary"], "weight": "bold"},
                 {"type": "text", "text": f"الالعاب: {games}", "size": "sm", "color": c["text2"]},
                 {"type": "text", "text": f"الفوز: {wins}", "size": "sm", "color": c["text2"]}
             ]},
            {"type": "button", "style": "primary", "height": "sm",
             "action": {"type": "message", "label": "رجوع", "text": "بداية"},
             "color": c["primary"], "margin": "md"}
        ]

        return {"type": "bubble", "styles": {"body": {"backgroundColor": c["bg"]}},
                "body": {"type": "box", "layout": "vertical", "spacing": "md", "contents": contents}}

    def help_card(self):
        c = self._colors()
        contents = [
            {"type": "box", "layout": "vertical", "backgroundColor": c["card"], "cornerRadius": "16px",
             "paddingAll": "16px",
             "contents": [{"type": "text", "text": "المساعدة", "align": "center", "weight": "bold", "size": "xl",
                           "color": c["primary"]}]}]
        help_texts = [
            ("بداية", "القائمة الرئيسية"),
            ("العاب", "عرض الالعاب"),
            ("نقاطي", "عرض النقاط"),
            ("الصدارة", "المتصدرين"),
            ("تسجيل", "انشاء حساب")
        ]
        help_contents = [{"type": "text", "text": f"{cmd} - {desc}", "size": "sm", "color": c["text2"], "wrap": True}
                         for cmd, desc in help_texts]
        contents.append({"type": "box", "layout": "vertical", "backgroundColor": c["card"], "cornerRadius": "12px",
                         "paddingAll": "16px", "spacing": "sm", "contents": [{"type": "text", "text": "الاوامر المتاحة:",
                                                                             "size": "md", "color": c["text"],
                                                                             "weight": "bold"}] + help_contents})
        contents.append({"type": "button", "style": "primary", "height": "sm",
                         "action": {"type": "message", "label": "رجوع", "text": "بداية"},
                         "color": c["primary"], "margin": "md"})

        return {"type": "bubble", "styles": {"body": {"backgroundColor": c["bg"]}},
                "body": {"type": "box", "layout": "vertical", "spacing": "md", "contents": contents}}
