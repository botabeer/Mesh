from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from config import Config


class UI:
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
                     "contents": [self._btn("الصدارة", "الصدارة"), self._btn("تغيير الاسم", "تغيير")]}
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
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )
