from linebot.v3.messaging import (
    FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
)
from config import Config


class UI:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        """الحصول على ألوان الثيم الحالي"""
        return Config.get_theme(self.theme)

    def _qr(self):
        """إنشاء قائمة QuickReply مع الحد الأقصى 13 زر"""
        commands = [
            "بداية", "العاب", "نقاطي", "الصدارة", "ثيم", "ايقاف", "مساعدة",
            "تحدي", "سؤال", "اعتراف", "منشن", "موقف", "حكمة", "شخصية"
        ]
        commands = commands[:13]  # الحد الأقصى 13 زر
        return QuickReply(
            items=[QuickReplyItem(action=MessageAction(label=c, text=c)) for c in commands]
        )

    # ================= Main Menus =================

    def main_menu(self, user: dict):
        c = self._c()
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"مرحباً {user.get('name', '')}!", "weight": "bold", "size": "lg", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "text", "text": "اختر ما تريد فعله من الأزرار أدناه:", "size": "md", "color": c["text"], "align": "center", "margin": "md"}
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        return FlexMessage(
            alt_text="البداية", 
            contents=FlexContainer.from_dict(bubble), 
            quickReply=self._qr()
        )

    def help_menu(self):
        c = self._c()
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "قائمة المساعدة", "weight": "bold", "size": "lg", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "text", "text": "يمكنك استخدام الأزرار التالية للتفاعل مع البوت.", "size": "md", "color": c["text"], "align": "center", "margin": "md"}
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        return FlexMessage(
            alt_text="المساعدة", 
            contents=FlexContainer.from_dict(bubble), 
            quickReply=self._qr()
        )

    def registration_choice(self):
        c = self._c()
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "مرحباً! يرجى اختيار:", "weight": "bold", "size": "lg", "color": c["primary"], "align": "center"}
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        return FlexMessage(
            alt_text="مرحباً", 
            contents=FlexContainer.from_dict(bubble), 
            quickReply=self._qr()
        )

    def ask_name(self, title="أدخل اسمك"):
        c = self._c()
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": title, "weight": "bold", "size": "lg", "color": c["primary"], "align": "center"}
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        return FlexMessage(
            alt_text=title, 
            contents=FlexContainer.from_dict(bubble), 
            quickReply=self._qr()
        )

    # ================= Game Question Builder =================

    def build_question_flex(self, question_text, game_name="لعبة", current_q=0, total_q=5, hint=None):
        c = self._c()
        contents = [
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": game_name, "weight": "bold", "size": "lg", "color": c["primary"]}
                ], "flex": 1},
                {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": f"{current_q+1}/{total_q}", "size": "sm", "align": "end", "color": c["text_secondary"]}
                ], "flex": 0}
            ]},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]

        if hint:
            contents.append({
                "type": "text", "text": hint, "size": "xs", "color": c["text_tertiary"], "align": "center", "margin": "md"
            })

        contents.append({
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": question_text, "wrap": True, "align": "center", "size": "md", "color": c["text"], "weight": "bold"}
            ],
            "backgroundColor": c["glass"], "cornerRadius": "12px", "paddingAll": "16px", "margin": "lg"
        })

        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text=game_name, contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    # ================= Pause / Game Over =================

    def pause_message(self, score=0, current_q=0, total_q=5):
        c = self._c()
        contents = [
            {"type": "text", "text": "تم حفظ تقدمك", "size": "lg", "weight": "bold", "color": c["warning"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": f"النقاط: {score}", "size": "md", "color": c["text"], "align": "center"},
                {"type": "text", "text": f"{current_q}/{total_q}", "size": "sm", "color": c["text_secondary"], "align": "center", "margin": "xs"}
            ], "backgroundColor": c["glass"], "cornerRadius": "12px", "paddingAll": "16px", "margin": "lg"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text="تم الإيقاف", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def game_over_message(self, score=0, total_q=5):
        c = self._c()
        won = score == total_q
        contents = [
            {"type": "text", "text": "انتهت اللعبة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": "فوز كامل" if won else f"النتيجة: {score}/{total_q}", "size": "lg", "color": c["success"] if won else c["text"], "align": "center", "weight": "bold"}
            ], "backgroundColor": c["glass"], "cornerRadius": "12px", "paddingAll": "20px", "margin": "lg"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text="النتيجة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())
