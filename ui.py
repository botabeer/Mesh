from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction
)
from config import Config


class UI:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    # ===============================
    # Theme
    # ===============================
    def _c(self):
        return Config.get_theme(self.theme)

    # ===============================
    # Global Quick Reply
    # ===============================
    def _global_quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="القائمة", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة")),
        ])

    # ===============================
    # UI Helpers
    # ===============================
    def _glass_box(self, contents):
        c = self._c()
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": c["glass"],
            "cornerRadius": "16px",
            "paddingAll": "16px",
            "spacing": "sm",
            "margin": "md",
            "borderWidth": "1px",
            "borderColor": c["glass_border"]
        }

    def _button(self, label, text, style="secondary", color=None):
        c = self._c()
        btn = {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": style,
            "height": "sm",
            "margin": "xs"
        }
        if color:
            btn["color"] = color
        elif style == "primary":
            btn["color"] = c["primary"]
        return btn

    def _bubble(self, contents, hero=None):
        c = self._c()
        bubble = {
            "type": "bubble",
            "size": "giga",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"],
                "paddingAll": "20px",
                "spacing": "md"
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
            "paddingAll": "20px",
            "backgroundColor": c["glass"],
            "contents": [
                {
                    "type": "text",
                    "text": Config.BOT_NAME,
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": c["primary"]
                },
                {
                    "type": "text",
                    "text": "منصة الالعاب التفاعلية",
                    "size": "xs",
                    "align": "center",
                    "color": c["text_tertiary"],
                    "margin": "xs"
                }
            ]
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
                            "flex": 3
                        },
                        {
                            "type": "text",
                            "text": f"{user['points']} نقطة",
                            "size": "md",
                            "weight": "bold",
                            "align": "end",
                            "color": c["success"],
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
                "align": "center",
                "color": c["text_tertiary"]
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
    def games_menu(self, games: list):
        c = self._c()

        rows = []
        row = []

        for i, game in enumerate(games, 1):
            row.append(self._button(game, game, "primary"))
            if i % 3 == 0:
                rows.append({
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": row
                })
                row = []

        if row:
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": row
            })

        contents = [
            {
                "type": "text",
                "text": "الالعاب المتاحة",
                "size": "xxl",
                "weight": "bold",
                "align": "center",
                "color": c["primary"]
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            self._glass_box(rows),
            self._button("العودة", "بداية")
        ]

        return FlexMessage(
            alt_text="الالعاب",
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._global_quick_reply()
        )

    # ===============================
    # Help
    # ===============================
    def help_menu(self):
        c = self._c()

        items = [
            "بداية - تسجيل - العاب - نقاطي - الصدارة",
            "انسحب لإيقاف اللعبة الحالية",
            "كل لعبة تتكون من 5 اسئلة",
            "يتم حفظ التقدم تلقائيا"
        ]

        contents = [
            {
                "type": "text",
                "text": "المساعدة",
                "size": "xxl",
                "weight": "bold",
                "align": "center",
                "color": c["primary"]
            },
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        for item in items:
            contents.append({
                "type": "text",
                "text": item,
                "size": "sm",
                "wrap": True
            })

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
            {
                "type": "text",
                "text": "التسجيل",
                "size": "xxl",
                "weight": "bold",
                "align": "center",
                "color": c["primary"]
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            self._glass_box([
                {
                    "type": "text",
                    "text": "ارسل اسمك للتسجيل",
                    "align": "center"
                }
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
            {
                "type": "text",
                "text": "تم ايقاف اللعبة",
                "size": "xl",
                "weight": "bold",
                "align": "center",
                "color": c["warning"]
            },
            self._button("العودة", "بداية", "primary")
        ]

        return FlexMessage(
            alt_text="تم ايقاف اللعبة",
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._global_quick_reply()
        )
