from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction
from config import Config

class UI:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    def _quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="البداية", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
        ])

    def _btn(self, label: str, action: str, style: str = "secondary"):
        c = self._c()
        btn = {
            "type": "button",
            "action": {"type": "message", "label": label, "text": action},
            "style": style,
            "height": "sm"
        }
        if style == "primary":
            btn["color"] = c["primary"]
        return btn

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
        contents = [
            {
                "type": "text",
                "text": "القائمة الرئيسية",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        if user:
            contents.extend([
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": c["glass"],
                    "cornerRadius": "12px",
                    "paddingAll": "12px",
                    "margin": "md",
                    "contents": [
                        {"type": "text", "text": f"مرحبا {user['name']}", "size": "md", "color": c["text"], "weight": "bold"},
                        {"type": "text", "text": f"النقاط: {user['points']}", "size": "sm", "color": c["text_secondary"], "margin": "xs"}
                    ]
                },
                {"type": "separator", "margin": "lg", "color": c["border"]}
            ])

        contents.extend([
            self._btn("العاب", "العاب", "primary"),
            self._btn("نقاطي", "نقاطي") if user else self._btn("تسجيل", "تسجيل", "primary"),
            self._btn("الصدارة", "الصدارة"),
            self._btn("تغيير الثيم", "تغيير_الثيم"),
            self._btn("مساعدة", "مساعدة")
        ])

        return FlexMessage(
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._quick_reply()
        )

    def help_menu(self):
        help_text = """الاوامر المتاحة:

- بداية: العودة للقائمة الرئيسية
- تسجيل: تسجيل حساب جديد
- العاب: عرض قائمة الالعاب
- نقاطي: عرض احصائياتك
- الصدارة: عرض لوحة الصدارة
- تغيير_الثيم: التبديل بين الثيم الفاتح والداكن
- انسحب: الانسحاب من اللعبة الحالية

محتوى تفاعلي:
- تحدي: تحدي عشوائي
- اعتراف: اعتراف عشوائي
- منشن: منشن عشوائي
- سؤال: سؤال عشوائي
- شخصية: سؤال شخصية
- حكمة: حكمة عشوائية
- موقف: موقف عشوائي

الالعاب المتاحة:
ذكاء - خمن - رياضيات - ترتيب - ضد - اسرع - مافيا - توافق

ملاحظة: كل لعبة مكونة من 5 جولات ويتم احتساب النقاط لاول اجابة صحيحة فقط"""

        return TextMessage(text=help_text, quickReply=self._quick_reply())

    def games_menu(self):
        c = self._c()
        contents = [
            {
                "type": "text",
                "text": "اختر اللعبة",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "text",
                "text": "العاب ذهنية",
                "size": "md",
                "weight": "bold",
                "color": c["text_secondary"],
                "margin": "md"
            },
            self._btn("ذكاء", "ذكاء", "primary"),
            self._btn("خمن", "خمن", "primary"),
            self._btn("رياضيات", "رياضيات", "primary"),
            self._btn("ترتيب", "ترتيب", "primary"),
            self._btn("ضد", "ضد", "primary"),
            self._btn("اسرع", "اسرع", "primary"),
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "text",
                "text": "العاب جماعية",
                "size": "md",
                "weight": "bold",
                "color": c["text_secondary"],
                "margin": "md"
            },
            self._btn("مافيا", "مافيا"),
            self._btn("توافق", "توافق")
        ]

        return FlexMessage(
            alt_text="الالعاب",
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._quick_reply()
        )

    def stats_card(self, user):
        c = self._c()
        win_rate = round((user['wins'] / user['games'] * 100) if user['games'] > 0 else 0, 1)
        
        contents = [
            {
                "type": "text",
                "text": "احصائياتك",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["glass"],
                "cornerRadius": "12px",
                "paddingAll": "16px",
                "margin": "md",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "الاسم", "flex": 1, "color": c["text_secondary"], "size": "sm"},
                            {"type": "text", "text": user['name'], "flex": 2, "color": c["text"], "weight": "bold", "align": "end"}
                        ]
                    },
                    {"type": "separator", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "النقاط", "flex": 1, "color": c["text_secondary"], "size": "sm"},
                            {"type": "text", "text": str(user['points']), "flex": 2, "color": c["success"], "weight": "bold", "size": "lg", "align": "end"}
                        ]
                    },
                    {"type": "separator", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "عدد الالعاب", "flex": 1, "color": c["text_secondary"], "size": "sm"},
                            {"type": "text", "text": str(user['games']), "flex": 2, "color": c["text"], "align": "end"}
                        ]
                    },
                    {"type": "separator", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "عدد الفوز", "flex": 1, "color": c["text_secondary"], "size": "sm"},
                            {"type": "text", "text": str(user['wins']), "flex": 2, "color": c["primary"], "align": "end"}
                        ]
                    },
                    {"type": "separator", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "text", "text": "نسبة الفوز", "flex": 1, "color": c["text_secondary"], "size": "sm"},
                            {"type": "text", "text": f"{win_rate}%", "flex": 2, "color": c["warning"], "align": "end"}
                        ]
                    }
                ]
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            self._btn("البداية", "بداية")
        ]

        return FlexMessage(
            alt_text="احصائياتك",
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._quick_reply()
        )

    def leaderboard_card(self, leaderboard):
        c = self._c()
        contents = [
            {
                "type": "text",
                "text": "لوحة الصدارة",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        if not leaderboard:
            contents.append({
                "type": "text",
                "text": "لا يوجد لاعبين مسجلين بعد",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "md"
            })
        else:
            for i, player in enumerate(leaderboard, 1):
                rank_color = c["primary"] if i == 1 else c["success"] if i == 2 else c["warning"] if i == 3 else c["text_secondary"]
                
                contents.append({
                    "type": "box",
                    "layout": "horizontal",
                    "backgroundColor": c["glass"],
                    "cornerRadius": "8px",
                    "paddingAll": "10px",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(i),
                            "flex": 0,
                            "color": rank_color,
                            "weight": "bold",
                            "size": "lg",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": player['name'],
                            "flex": 3,
                            "color": c["text"],
                            "weight": "bold",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": str(player['points']),
                            "flex": 1,
                            "color": c["success"],
                            "weight": "bold",
                            "align": "end"
                        }
                    ]
                })

        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            self._btn("البداية", "بداية")
        ])

        return FlexMessage(
            alt_text="لوحة الصدارة",
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._quick_reply()
        )

    def ask_name(self):
        return TextMessage(
            text="ارسل اسمك للتسجيل:",
            quickReply=QuickReply(items=[
                QuickReplyItem(action=MessageAction(label="البداية", text="بداية"))
            ])
        )

    def game_stopped(self):
        return TextMessage(text="تم ايقاف اللعبة بنجاح", quickReply=self._quick_reply())
