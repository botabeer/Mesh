from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config

class UI:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    # ===============================
    # Quick Reply ثابت
    # ===============================
    def _global_quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="القائمة", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="منشن", text="منشن")),
            QuickReplyItem(action=MessageAction(label="موقف", text="موقف")),
            QuickReplyItem(action=MessageAction(label="حكمة", text="حكمة")),
            QuickReplyItem(action=MessageAction(label="شخصية", text="شخصية")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة")),
        ])

    # ===============================
    # Helpers
    # ===============================
    def _button(self, label, action, style="secondary", color=None):
        c = self._c()
        btn = {
            "type": "button",
            "action": {"type": "message", "label": label, "text": action},
            "style": style,
            "height": "sm",
            "margin": "xs"
        }
        if color:
            btn["color"] = color
        elif style == "primary":
            btn["color"] = c["primary"]
        return btn

    def _glass_box(self, contents):
        c = self._c()
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "16px",
            "margin": "md",
            "spacing": "sm",
            "cornerRadius": "16px",
            "borderWidth": "1px",
            "borderColor": c["glass_border"]
        }

    def _bubble(self, contents, hero=None):
        c = self._c()
        bubble = {
            "type": "bubble",
            "size": "giga",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px",
                "spacing": "md",
                "backgroundColor": c["bg"]
            }
        }
        if hero:
            bubble["hero"] = hero
        return bubble

    # ===============================
    # Main Menu
    # ===============================
    def main_menu(self, user=None):
        c = self._c()
        hero = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "paddingAll": "16px",
                    "cornerRadius": "16px",
                    "contents": [
                        {
                            "type": "text",
                            "text": Config.BOT_NAME,
                            "size": "xxl",
                            "weight": "bold",
                            "color": c["primary"],
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "منصة الالعاب التفاعلية",
                            "size": "xs",
                            "color": c["text_tertiary"],
                            "align": "center"
                        }
                    ]
                }
            ],
            "paddingAll": "20px"
        }

        contents = []
        if user:
            contents.append(self._glass_box([
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"مرحبا {user['name']}",
                            "size": "lg",
                            "weight": "bold",
                            "color": c["text"],
                            "flex": 3
                        },
                        {
                            "type": "text",
                            "text": f"{user['points']} نقطة",
                            "size": "md",
                            "weight": "bold",
                            "color": c["success"],
                            "align": "end",
                            "flex": 2
                        }
                    ]
                }
            ]))

        contents.extend([
            {
                "type": "text",
                "text": "الالعاب",
                "size": "md",
                "weight": "bold",
                "color": c["text_secondary"],
                "margin": "md"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    self._button("العاب", "العاب", "primary"),
                    self._button("انسحب", "انسحب")
                ]
            },
            {
                "type": "text",
                "text": "محتوى تفاعلي",
                "size": "md",
                "weight": "bold",
                "color": c["text_secondary"],
                "margin": "md"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    self._button("تحدي", "تحدي"),
                    self._button("سؤال", "سؤال"),
                    self._button("اعتراف", "اعتراف")
                ]
            },
            {
                "type": "text",
                "text": "الملف الشخصي",
                "size": "md",
                "weight": "bold",
                "color": c["text_secondary"],
                "margin": "md"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    self._button("نقاطي", "نقاطي") if user else self._button("تسجيل", "تسجيل", "primary"),
                    self._button("الصدارة", "الصدارة")
                ]
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "text",
                "text": f"{Config.BOT_NAME} v{Config.VERSION}",
                "size": "xxs",
                "color": c["text_tertiary"],
                "align": "center"
            }
        ])

        return FlexMessage(
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(self._bubble(contents, hero)),
            quickReply=self._global_quick_reply()
        )

    # ===============================
    # Games Menu
    # ===============================
    def games_menu(self):
        c = self._c()
        contents = [
            {
                "type": "text",
                "text": "الالعاب المتاحة",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            self._glass_box([
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        self._button("ذكاء", "ذكاء", "primary"),
                        self._button("خمن", "خمن", "primary"),
                        self._button("رياضيات", "رياضيات", "primary")
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "xs",
                    "contents": [
                        self._button("ترتيب", "ترتيب"),
                        self._button("ضد", "ضد"),
                        self._button("اسرع", "اسرع")
                    ]
                }
            ]),
            self._button("العودة", "بداية")
        ]

        return FlexMessage(
            alt_text="الالعاب",
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._global_quick_reply()
        )

    # ===============================
    # Help Menu
    # ===============================
    def help_menu(self):
        c = self._c()
        sections = [
            ("الاوامر الرئيسية", "بداية - تسجيل - العاب - نقاطي - الصدارة - انسحب"),
            ("العاب ذهنية", "ذكاء - خمن - رياضيات - ترتيب - ضد - اسرع"),
            ("العاب كلمات", "سلسلة - انسان حيوان - اغاني"),
            ("اوامر اللعبة", "لمح - جاوب - انسحب"),
        ]

        contents = [
            {"type": "text", "text": "المساعدة", "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        for title, items in sections:
            contents.append({"type": "text", "text": title, "size": "md", "weight": "bold", "color": c["text_secondary"], "margin": "md"})
            contents.append({"type": "text", "text": items, "size": "sm", "wrap": True})

        contents.append(self._button("العودة", "بداية"))

        return FlexMessage(
            alt_text="المساعدة",
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._global_quick_reply()
        )

    # ===============================
    # Register
    # ===============================
    def ask_name(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "التسجيل", "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            self._glass_box([
                {"type": "text", "text": "ارسل اسمك للتسجيل", "align": "center"}
            ]),
            self._button("الغاء", "بداية")
        ]
        return FlexMessage(
            alt_text="التسجيل",
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._global_quick_reply()
        )

    # ===============================
    # Game Stopped
    # ===============================
    def game_stopped(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "تم ايقاف اللعبة", "size": "xl", "weight": "bold", "color": c["warning"], "align": "center"},
            self._button("العودة", "بداية", "primary")
        ]
        return FlexMessage(
            alt_text="تم ايقاف اللعبة",
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._global_quick_reply()
        )
