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

    # ====== الدوال الرئيسية ======
    def main_menu(self, user):
        # نفس الكود الموجود عندك سابقًا
        pass  # احتفظ بالكود القديم لـ main_menu كما هو

    def help_menu(self):
        text = (
            "أوامر البوت:\n"
            "• بداية: عرض القائمة الرئيسية\n"
            "• تسجيل: لتسجيل اسمك\n"
            "• تغيير_الثيم: لتغيير الثيم\n"
            "• العاب: عرض الألعاب\n"
            "• نقاطي: عرض نقاطك\n"
            "• الصدارة: عرض قائمة الصدارة\n"
            "• انسحب: لإيقاف اللعبة الحالية\n"
        )
        return TextMessage(text=text)

    def ask_name(self):
        return TextMessage(text="من فضلك اكتب اسمك:")

    def games_menu(self):
        contents = [
            {"type": "text", "text": "هذه قائمة الألعاب المتاحة:"},
            {"type": "separator", "margin": "md", "color": self._c()["border"]},
            self._btn("ذكاء", "ذكاء", "primary"),
            self._btn("خمن", "خمن"),
            self._btn("رياضيات", "رياضيات"),
            self._btn("ترتيب", "ترتيب"),
            self._btn("ضد", "ضد"),
            self._btn("اسرع", "اسرع"),
            self._btn("انسان", "انسان"),
            self._btn("سلسله", "سلسله"),
            self._btn("تكوين", "تكوين"),
            self._btn("لون", "لون"),
            self._btn("اغنيه", "اغنيه"),
            self._btn("مافيا", "مافيا"),
            self._btn("توافق", "توافق"),
        ]
        return FlexMessage(
            alt_text="قائمة الألعاب",
            contents=FlexContainer.from_dict(self._bubble(contents)),
            quickReply=self._text_buttons_quick_reply()
        )

    def stats_card(self, user):
        contents = [
            {"type": "text", "text": f"اسمك: {user['name']}"},
            {"type": "text", "text": f"النقاط: {user['points']}"},
            {"type": "text", "text": f"عدد الألعاب: {user['games']}"},
            {"type": "text", "text": f"عدد الفوز: {user['wins']}"}
        ]
        return FlexMessage(
            alt_text="احصائياتك",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )

    def leaderboard_card(self, leaderboard):
        contents = [{"type": "text", "text": "الصدارة:"}]
        for i, user in enumerate(leaderboard, 1):
            contents.append({"type": "text", "text": f"{i}. {user['name']} - {user['points']} نقاط"})
        return FlexMessage(
            alt_text="الصدارة",
            contents=FlexContainer.from_dict(self._bubble(contents))
        )

    def game_stopped(self):
        return TextMessage(text="تم إيقاف اللعبة بنجاح")
