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
            "تحدي", "سؤال", "اعتراف", "منشن", "موقف", "حكمة"
        ]
        commands = commands[:13]  # الحد الأقصى 13 زر
        return QuickReply(
            items=[QuickReplyItem(action=MessageAction(label=c, text=c)) for c in commands]
        )

    # ================= Main Menus =================

    def main_menu(self, user: dict):
        c = self._c()
        name = user.get('name', 'مستخدم') if user else 'مستخدم'
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"مرحباً {name}!", "weight": "bold", "size": "lg", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "text", "text": "اختر ما تريد فعله:", "size": "md", "color": c["text"], "align": "center", "margin": "md"}
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
                    {"type": "text", "text": "استخدم الأزرار للتفاعل مع البوت", "size": "sm", "color": c["text"], "align": "center", "margin": "md", "wrap": True}
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
                    {"type": "text", "text": "مرحباً بك!", "weight": "bold", "size": "xl", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "text", "text": "للبدء، يرجى التسجيل أولاً", "size": "md", "color": c["text"], "align": "center", "margin": "lg", "wrap": True},
                    {"type": "button", "action": {"type": "message", "label": "تسجيل", "text": "تسجيل"}, "style": "primary", "margin": "lg"}
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        return FlexMessage(
            alt_text="التسجيل", 
            contents=FlexContainer.from_dict(bubble)
        )

    def ask_name(self):
        return TextMessage(text="أدخل اسمك (عربي أو إنجليزي)")

    def ask_name_invalid(self):
        return TextMessage(text="الاسم غير صالح. حاول مرة أخرى")

    def theme_changed(self, theme_name):
        return TextMessage(text=f"تم التغيير إلى {theme_name}")

    def stats_card(self, user: dict):
        c = self._c()
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "إحصائياتي", "weight": "bold", "size": "lg", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": f"النقاط: {user.get('points', 0)}", "size": "md", "color": c["text"]},
                        {"type": "text", "text": f"الألعاب: {user.get('games', 0)}", "size": "md", "color": c["text"], "margin": "sm"},
                        {"type": "text", "text": f"الفوز: {user.get('wins', 0)}", "size": "md", "color": c["text"], "margin": "sm"}
                    ], "margin": "lg"}
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        return FlexMessage(alt_text="إحصائياتي", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def leaderboard_card(self, leaders: list):
        c = self._c()
        contents = [
            {"type": "text", "text": "لوحة الصدارة", "weight": "bold", "size": "lg", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]
        
        for i, leader in enumerate(leaders[:10], 1):
            contents.append({
                "type": "box", "layout": "horizontal", "contents": [
                    {"type": "text", "text": f"{i}. {leader.get('name', 'مجهول')}", "size": "sm", "color": c["text"], "flex": 3},
                    {"type": "text", "text": f"{leader.get('points', 0)} نقطة", "size": "sm", "color": c["text_secondary"], "align": "end", "flex": 2}
                ], "margin": "md"
            })
        
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def games_menu(self):
        c = self._c()
        games = ["ذكاء", "خمن", "رياضيات", "ترتيب", "ضد", "اسرع", "سلسله", "انسان حيوان", "تكوين", "اغاني", "الوان", "توافق", "مافيا"]
        contents = [
            {"type": "text", "text": "الألعاب المتاحة", "weight": "bold", "size": "lg", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]
        
        for game in games[:13]:
            contents.append({
                "type": "button",
                "action": {"type": "message", "label": game, "text": game},
                "style": "secondary",
                "margin": "xs"
            })
        
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text="الألعاب", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    def game_stopped(self):
        return TextMessage(text="تم إيقاف اللعبة")
