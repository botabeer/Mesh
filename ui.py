from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from config import Config


class UI:
    """واجهة المستخدم"""
    
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def set_theme(self, theme: str):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    def _btn(self, label: str, action: str, style: str = "secondary"):
        c = self._c()
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": action},
            "style": style,
            "height": "sm",
            "color": c["primary"] if style == "primary" else c["secondary"]
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

    def main_menu(self, user):
        """القائمة الرئيسية"""
        c = self._c()

        if not user:
            contents = [
                self._header(Config.BOT_NAME),
                self._glass_box([
                    {"type": "text", "text": "مرحبا", "align": "center", "size": "lg", "color": c["text"]},
                    {"type": "text", "text": "غير مسجل", "align": "center", "size": "sm", "color": c["warning"], "margin": "sm"}
                ]),
                {"type": "separator", "margin": "lg", "color": c["border"]},
                self._btn("تسجيل", "تسجيل", "primary")
            ]
        else:
            contents = [
                self._header(Config.BOT_NAME),
                self._glass_box([
                    {"type": "text", "text": f"مرحبا {user['name']}", "align": "center", "size": "lg", "color": c["text"], "weight": "bold"},
                    {"type": "text", "text": f"النقاط: {user['points']}", "align": "center", "size": "md", "color": c["primary"], "margin": "sm"}
                ]),
                {"type": "separator", "margin": "lg", "color": c["border"]},
                self._glass_box([
                    {"type": "text", "text": "القوائم", "size": "sm", "color": c["text_tertiary"]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                     "contents": [self._btn("الالعاب", "العاب"), self._btn("نقاطي", "نقاطي")]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                     "contents": [self._btn("الصداره", "الصداره"), self._btn("تغيير الاسم", "تغيير")]}
                ], "12px"),
                {"type": "separator", "margin": "md", "color": c["border"]},
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
        """قائمة الالعاب"""
        c = self._c()
        
        games = [
            ("ذكاء", "الغاز ذكاء"),
            ("خمن", "حزر الكلمه"),
            ("رياضيات", "عمليات حسابيه")
        ]
        
        buttons = []
        for cmd, desc in games:
            buttons.append({
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["glass"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "margin": "sm",
                "action": {"type": "message", "label": cmd, "text": cmd},
                "contents": [
                    {"type": "text", "text": cmd, "weight": "bold", "color": c["primary"], "size": "md"},
                    {"type": "text", "text": desc, "color": c["text_secondary"], "size": "xs", "margin": "xs"}
                ]
            })
        
        contents = [
            self._header("الالعاب"),
            {"type": "separator", "margin": "md", "color": c["border"]}
        ] + buttons + [
            {"type": "separator", "margin": "md", "color": c["border"]},
            self._btn("رجوع", "بداية")
        ]
        
        return FlexMessage(
            alt_text="قائمه الالعاب",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )

    def stats_card(self, user):
        """بطاقة الاحصائيات"""
        c = self._c()
        
        contents = [
            self._header("احصائياتي"),
            {"type": "separator", "margin": "md", "color": c["border"]},
            self._glass_box([
                {"type": "text", "text": user['name'], "weight": "bold", "size": "lg", "color": c["text"], "align": "center"},
                {"type": "box", "layout": "horizontal", "margin": "md", "contents": [
                    {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": "النقاط", "size": "xs", "color": c["text_tertiary"], "align": "center"},
                        {"type": "text", "text": str(user['points']), "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"}
                    ]},
                    {"type": "separator", "color": c["border"]},
                    {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": "الالعاب", "size": "xs", "color": c["text_tertiary"], "align": "center"},
                        {"type": "text", "text": str(user['games']), "size": "xl", "weight": "bold", "color": c["text"], "align": "center"}
                    ]},
                    {"type": "separator", "color": c["border"]},
                    {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": "الفوز", "size": "xs", "color": c["text_tertiary"], "align": "center"},
                        {"type": "text", "text": str(user['wins']), "size": "xl", "weight": "bold", "color": c["success"], "align": "center"}
                    ]}
                ]}
            ]),
            {"type": "separator", "margin": "md", "color": c["border"]},
            self._btn("رجوع", "بداية")
        ]
        
        return FlexMessage(
            alt_text="احصائياتي",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )

    def leaderboard_card(self, leaders):
        """لوحة الصداره"""
        c = self._c()
        
        if not leaders:
            contents = [
                self._header("الصداره"),
                {"type": "separator", "margin": "md", "color": c["border"]},
                {"type": "text", "text": "لا يوجد لاعبون بعد", "align": "center", "color": c["text_secondary"], "margin": "md"},
                {"type": "separator", "margin": "md", "color": c["border"]},
                self._btn("رجوع", "بداية")
            ]
        else:
            rank_items = []
            for i, (name, points) in enumerate(leaders[:10], 1):
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                rank_items.append({
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "sm",
                    "contents": [
                        {"type": "text", "text": emoji, "size": "sm", "flex": 1, "color": c["text"]},
                        {"type": "text", "text": name, "size": "sm", "flex": 4, "color": c["text"]},
                        {"type": "text", "text": str(points), "size": "sm", "flex": 2, "align": "end", "color": c["primary"], "weight": "bold"}
                    ]
                })
            
            contents = [
                self._header("الصداره"),
                {"type": "separator", "margin": "md", "color": c["border"]},
                self._glass_box(rank_items, "12px"),
                {"type": "separator", "margin": "md", "color": c["border"]},
                self._btn("رجوع", "بداية")
            ]
        
        return FlexMessage(
            alt_text="لوحه الصداره",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )
