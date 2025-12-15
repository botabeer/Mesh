from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction
from config import Config

class UI:
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    def _btn(self, label: str, action: str, style: str = "secondary", height: str = "sm"):
        btn = {"type":"button","action":{"type":"message","label":label,"text":action},"style":style,"height":height}
        if style=="primary": btn["color"]=self._c()["primary"]
        return btn

    def _bubble(self, contents):
        return {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","backgroundColor":self._c()["bg"],"paddingAll":"20px","spacing":"md","contents":contents}}

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

    def main_menu(self, user):
        contents = [
            {"type":"text","text":"القائمة الرئيسية","size":"xl","weight":"bold","color":self._c()["primary"],"align":"center"},
            {"type":"separator","margin":"md","color":self._c()["border"]},
            self._btn("العاب","العاب","primary"),
            self._btn("نقاطي","نقاطي"),
            self._btn("تغيير الثيم","تغيير_الثيم"),
            self._btn("مساعدة","مساعدة")
        ]
        return FlexMessage(alt_text="القائمة الرئيسية", contents=FlexContainer.from_dict(self._bubble(contents)), quickReply=self._text_buttons_quick_reply())

    def help_menu(self):
        text="أوامر البوت:\n• بداية\n• تسجيل\n• تغيير_الثيم\n• العاب\n• نقاطي\n• الصدارة\n• انسحب"
        return TextMessage(text=text)

    def games_menu(self):
        contents=[{"type":"text","text":"اختر اللعبة:"}]
        games=["ذكاء","خمن","رياضيات","ترتيب","ضد","اسرع","انسان","سلسله","تكوين","لون","اغنيه","مافيا","توافق"]
        for g in games:
            contents.append(self._btn(g,g))
        return FlexMessage(alt_text="الألعاب", contents=FlexContainer.from_dict(self._bubble(contents)), quickReply=self._text_buttons_quick_reply())

    def stats_card(self, user):
        contents=[{"type":"text","text":f"اسمك: {user['name']}"},
                  {"type":"text","text":f"النقاط: {user['points']}"},
                  {"type":"text","text":f"عدد الألعاب: {user['games']}"},
                  {"type":"text","text":f"عدد الفوز: {user['wins']}"}]
        return FlexMessage(alt_text="احصائياتك", contents=FlexContainer.from_dict(self._bubble(contents)))

    def leaderboard_card(self, leaderboard):
        contents=[{"type":"text","text":"الصدارة:"}]
        for i,user in enumerate(leaderboard,1):
            contents.append({"type":"text","text":f"{i}. {user['name']} - {user['points']} نقاط"})
        return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(self._bubble(contents)))

    def game_stopped(self):
        return TextMessage(text="تم إيقاف اللعبة بنجاح")
