from typing import List, Dict
from config import Config

class UIBuilder:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self) -> Dict[str, str]:
        return Config.get_theme(self.theme)

    def _btn(self, label: str, action: str, style: str = "secondary") -> Dict:
        return {
            "type": "button",
            "style": style,
            "height": "sm",
            "action": {"type": "message", "label": label, "text": action},
            "color": self._c()["primary" if style == "primary" else "secondary"]
        }

    def _header(self, text: str) -> Dict:
        return {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": self._c()["card"],
            "cornerRadius": "16px",
            "paddingAll": "16px",
            "contents": [{
                "type": "text",
                "text": text,
                "align": "center",
                "weight": "bold",
                "size": "xl",
                "color": self._c()["primary"]
            }]
        }

    def _bubble(self, contents: List[Dict]) -> Dict:
        return {
            "type": "bubble",
            "styles": {"body": {"backgroundColor": self._c()["bg"]}},
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": contents
            }
        }

    def welcome_card(self, name: str, registered: bool):
        c = self._c()
        status = f"{name} مسجل" if registered else f"{name} غير مسجل"
        status_color = c["success"] if registered else c["warning"]

        contents = [
            self._header("Bot Mesh"),
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
                {"type": "text", "text": "الحساب", "weight": "bold", "size": "md", "margin": "md", "color": c["primary"]},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        self._btn("تغيير الاسم", "تغيير"),
                        self._btn("نقاطي", "نقاطي")
                    ]
                },
                {"type": "text", "text": "الاعدادات", "weight": "bold", "size": "md", "margin": "md", "color": c["primary"]},
                self._btn("الوضع " + ("الفاتح" if self.theme == "dark" else "الداكن"), "تغيير_الثيم"),
                {"type": "text", "text": "الاحصائيات", "weight": "bold", "size": "md", "margin": "md", "color": c["primary"]},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        self._btn("الصدارة", "الصدارة"),
                        self._btn("مساعدة", "مساعدة")
                    ]
                },
                {"type": "text", "text": "القوائم", "weight": "bold", "size": "md", "margin": "md", "color": c["primary"]},
                self._btn("الالعاب", "العاب", "primary")
            ])
        else:
            contents.extend([
                {"type": "text", "text": "ابدأ الآن", "weight": "bold", "size": "md", "margin": "md", "color": c["primary"]},
                self._btn("تسجيل", "تسجيل", "primary")
            ])

        contents.append({
            "type": "text",
            "text": "عبير الدوسري 2025",
            "align": "center",
            "size": "xs",
            "color": c["text3"],
            "margin": "lg"
        })

        return self._bubble(contents)

    def games_menu_card(self):
        games = [
            ["ذكاء", "خمن", "ضد"],
            ["ترتيب", "رياضيات", "اغنيه"],
            ["لون", "تكوين", "لعبة"],
            ["سلسلة", "اسرع", "توافق"],
            ["مافيا", "سؤال", "منشن"]
        ]

        contents = [self._header("الالعاب")]

        for row in games:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm",
                "contents": [self._btn(g, g) for g in row]
            })

        contents.append(self._btn("رجوع", "بداية", "primary"))
        contents[-1]["margin"] = "md"

        return self._bubble(contents)

    def leaderboard_card(self, leaders: List[tuple]):
        c = self._c()
        contents = [self._header("لوحة الصدارة")]

        items = []
        for i, (name, pts) in enumerate(leaders[:10]):
            items.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "backgroundColor": c["card"],
                "cornerRadius": "8px",
                "paddingAll": "8px",
                "contents": [
                    {"type": "text", "text": str(i + 1), "size": "sm", "color": c["text"], "flex": 0, "weight": "bold"},
                    {"type": "text", "text": name, "size": "sm", "color": c["text"], "flex": 3, "margin": "sm"},
                    {"type": "text", "text": str(pts), "size": "sm", "color": c["primary"], "weight": "bold", "flex": 1, "align": "end"}
                ]
            })

        contents.append({"type": "box", "layout": "vertical", "spacing": "sm", "contents": items})
        contents.append(self._btn("رجوع", "بداية", "primary"))
        contents[-1]["margin"] = "md"

        return self._bubble(contents)

    def stats_card(self, name: str, user_data: dict):
        c = self._c()
        points = user_data.get("total_points", 0)
        games = user_data.get("games_played", 0)
        wins = user_data.get("wins", 0)

        contents = [
            self._header("احصائياتي"),
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "paddingAll": "16px",
                "spacing": "sm",
                "contents": [
                    {"type": "text", "text": f"الاسم: {name}", "size": "md", "color": c["text"]},
                    {"type": "text", "text": f"النقاط: {points}", "size": "lg", "color": c["primary"], "weight": "bold"},
                    {"type": "text", "text": f"الالعاب: {games}", "size": "sm", "color": c["text2"]},
                    {"type": "text", "text": f"الفوز: {wins}", "size": "sm", "color": c["text2"]}
                ]
            },
            self._btn("رجوع", "بداية", "primary")
        ]
        contents[-1]["margin"] = "md"

        return self._bubble(contents)

    def help_card(self):
        c = self._c()
        help_texts = [
            ("بداية", "القائمة الرئيسية"),
            ("العاب", "عرض الالعاب"),
            ("نقاطي", "عرض النقاط"),
            ("الصدارة", "المتصدرين"),
            ("تسجيل", "انشاء حساب")
        ]

        help_items = [
            {"type": "text", "text": "الاوامر المتاحة:", "size": "md", "color": c["text"], "weight": "bold"}
        ] + [
            {"type": "text", "text": f"{cmd} - {desc}", "size": "sm", "color": c["text2"], "wrap": True}
            for cmd, desc in help_texts
        ]

        contents = [
            self._header("المساعدة"),
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "paddingAll": "16px",
                "spacing": "sm",
                "contents": help_items
            },
            self._btn("رجوع", "بداية", "primary")
        ]
        contents[-1]["margin"] = "md"

        return self._bubble(contents)
