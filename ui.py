from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction
from config import Config


class UI:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    def _btn(self, label: str, action: str, style: str = "secondary", height: str = "sm"):
        c = self._c()
        btn = {
            "type": "button",
            "action": {"type": "message", "label": label, "text": action},
            "style": style,
            "height": height
        }
        if style == "primary":
            btn["color"] = c["primary"]
        return btn

    def _glass_box(self, contents, padding: str = "16px", margin: str = "md"):
        c = self._c()
        return {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": c["glass"],
            "cornerRadius": "16px",
            "paddingAll": padding,
            "margin": margin,
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

    def _text_buttons_quick_reply(self):
        """أزرار النصوص الثابتة بدون إيموجي"""
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="منشن", text="منشن")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="شخصيه", text="شخصيه")),
            QuickReplyItem(action=MessageAction(label="حكمه", text="حكمه")),
            QuickReplyItem(action=MessageAction(label="موقف", text="موقف")),
            QuickReplyItem(action=MessageAction(label="البداية", text="بدايه"))
        ])

    def main_menu(self, user):
        c = self._c()

        if not user:
            contents = [
                self._header(f"{Config.BOT_NAME}", "xxl"),
                {"type": "text", "text": "مرحباً بك في البوت!", 
                 "align": "center", "size": "md", "color": c["text"], "margin": "md"},
                {"type": "separator", "margin": "lg", "color": c["border"]},
                self._glass_box([
                    {"type": "text", "text": "غير مسجل", "align": "center", 
                     "size": "lg", "color": c["warning"], "weight": "bold"},
                    {"type": "text", "text": "سجل الآن للحصول على نقاط", 
                     "align": "center", "size": "sm", "color": c["text_secondary"], "margin": "sm", "wrap": True}
                ], "16px", "md"),
                {"type": "separator", "margin": "md", "color": c["border"]},
                self._glass_box([
                    {"type": "text", "text": "النصوص التفاعلية", "size": "sm", 
                     "color": c["text_tertiary"], "weight": "bold"},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                     "contents": [
                         self._btn("تحدي", "تحدي"),
                         self._btn("اعتراف", "اعتراف")
                     ]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "xs",
                     "contents": [
                         self._btn("منشن", "منشن"),
                         self._btn("سؤال", "سؤال")
                     ]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "xs",
                     "contents": [
                         self._btn("شخصيه", "شخصيه"),
                         self._btn("حكمه", "حكمه")
                     ]},
                    {"type": "button", "action": {"type": "message", "label": "موقف", "text": "موقف"},
                     "style": "secondary", "height": "sm", "margin": "xs"}
                ], "12px", "md"),
                {"type": "separator", "margin": "md", "color": c["border"]},
                self._btn("تسجيل", "تسجيل", "primary", "md"),
                self._btn("المساعدة", "مساعده", "secondary", "sm")
            ]
        else:
            win_rate = int((user['wins'] / user['games'] * 100)) if user['games'] > 0 else 0
            
            contents = [
                self._header(f"{Config.BOT_NAME}", "xxl"),
                self._glass_box([
                    {"type": "text", "text": f"{user['name']}", "align": "center",
                     "size": "xl", "color": c["text"], "weight": "bold"},
                    {"type": "box", "layout": "horizontal", "spacing": "md", "margin": "md",
                     "contents": [
                         {"type": "box", "layout": "vertical", "contents": [
                             {"type": "text", "text": "النقاط", "size": "xs", 
                              "color": c["text_tertiary"], "align": "center"},
                             {"type": "text", "text": str(user['points']), "size": "xxl", 
                              "weight": "bold", "color": c["primary"], "align": "center"}
                         ]},
                         {"type": "separator"},
                         {"type": "box", "layout": "vertical", "contents": [
                             {"type": "text", "text": "الفوز", "size": "xs", 
                              "color": c["text_tertiary"], "align": "center"},
                             {"type": "text", "text": f"{win_rate}%", "size": "xxl", 
                              "weight": "bold", "color": c["success"], "align": "center"}
                         ]}
                     ]}
                ], "16px", "md"),
                {"type": "separator", "margin": "lg", "color": c["border"]},
                self._glass_box([
                    {"type": "text", "text": "القوائم الرئيسية", "size": "sm", 
                     "color": c["text_tertiary"], "weight": "bold"},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                     "contents": [
                         self._btn("الالعاب", "العاب", "primary"),
                         self._btn("احصائياتي", "نقاطي")
                     ]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "xs",
                     "contents": [
                         self._btn("الصداره", "الصداره"),
                         self._btn("تغيير الاسم", "تغيير")
                     ]}
                ], "12px", "md"),
                {"type": "separator", "margin": "md", "color": c["border"]},
                self._glass_box([
                    {"type": "text", "text": "النصوص التفاعلية", "size": "sm", 
                     "color": c["text_tertiary"], "weight": "bold"},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                     "contents": [
                         self._btn("تحدي", "تحدي"),
                         self._btn("اعتراف", "اعتراف")
                     ]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "xs",
                     "contents": [
                         self._btn("منشن", "منشن"),
                         self._btn("سؤال", "سؤال")
                     ]},
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "xs",
                     "contents": [
                         self._btn("شخصيه", "شخصيه"),
                         self._btn("حكمه", "حكمه")
                     ]},
                    {"type": "button", "action": {"type": "message", "label": "موقف", "text": "موقف"},
                     "style": "secondary", "height": "sm", "margin": "xs"}
                ], "12px", "md"),
                {"type": "separator", "margin": "md", "color": c["border"]},
                {"type": "box", "layout": "horizontal", "spacing": "sm",
                 "contents": [
                     self._btn(f"الوضع {'الفاتح' if self.theme == 'dark' else 'الداكن'}", "تغيير_الثيم"),
                     self._btn("المساعدة", "مساعده")
                 ]}
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
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._text_buttons_quick_reply()
        )
