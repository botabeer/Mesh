from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config

class UI:
    def __init__(self, theme="light"):
        self.theme = theme

    def _c(self):
        """ارجاع ألوان الثيم الحالي"""
        return Config.get_theme(self.theme)

    def _qr(self):
        """الاختصارات السريعة لكل النوافذ"""
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="القائمة", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
            QuickReplyItem(action=MessageAction(label="ايقاف", text="ايقاف")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
        ])

    ### ==================== النوافذ الرئيسية ====================

    def main_menu(self, user=None):
        c = self._c()
        contents = [
            {"type":"text","text":Config.BOT_NAME,"size":"xxl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"text","text":f"الإصدار {Config.VERSION}","size":"xs","color":c["text_tertiary"],"align":"center","margin":"xs"},
            {"type":"separator","margin":"md","color":c["border"]}
        ]

        if user:
            contents.append({
                "type":"box","layout":"horizontal","spacing":"md","margin":"md","contents":[
                    {"type":"box","layout":"vertical","contents":[
                        {"type":"text","text":"اللاعب","size":"xs","color":c["text_tertiary"]},
                        {"type":"text","text":user['name'],"size":"md","weight":"bold","color":c["text"],"margin":"xs"}
                    ],"flex":3},
                    {"type":"box","layout":"vertical","contents":[
                        {"type":"text","text":"النقاط","size":"xs","color":c["text_tertiary"],"align":"end"},
                        {"type":"text","text":str(user['points']),"size":"xl","weight":"bold","color":c["primary"],"align":"end","margin":"xs"}
                    ],"flex":2}
                ],"paddingAll":"md","cornerRadius":"md","backgroundColor":c["glass"],"borderWidth":"1px","borderColor":c["border"]}
            )

        contents.extend([
            {"type":"separator","margin":"lg","color":c["border"]},
            {"type":"button","action":{"type":"message","label":"الالعاب","text":"العاب"},"style":"primary","color":c["primary"],"margin":"md","height":"md"},
            {"type":"box","layout":"horizontal","spacing":"md","margin":"md","contents":[
                {"type":"button","action":{"type":"message","label":"نقاطي" if user else "تسجيل","text":"نقاطي" if user else "تسجيل"},"style":"secondary","height":"sm","flex":1},
                {"type":"button","action":{"type":"message","label":"الصدارة","text":"الصدارة"},"style":"secondary","height":"sm","flex":1}
            ]}
        ])

        if user:
            contents.append({
                "type":"box","layout":"horizontal","spacing":"md","margin":"sm","contents":[
                    {"type":"button","action":{"type":"message","label":"تغيير الاسم","text":"تغيير الاسم"},"style":"secondary","height":"sm","flex":1},
                    {"type":"button","action":{"type":"message","label":"تبديل الثيم","text":"ثيم"},"style":"secondary","height":"sm","flex":1}
                ]
            })
        else:
            contents.append({"type":"button","action":{"type":"message","label":"انسحب","text":"انسحب"},"style":"secondary","height":"sm","margin":"sm"})

        contents.extend([
            {"type":"separator","margin":"xl","color":c["border"]},
            {"type":"text","text":Config.COPYRIGHT,"size":"xxs","color":c["text_tertiary"],"align":"center","wrap":True,"margin":"md"}
        ])

        bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        return FlexMessage(alt_text="البداية",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    def help_menu(self):
        c = self._c()
        contents = [
            {"type":"text","text":"دليل الاستخدام","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"lg","color":c["border"]},
            {"type":"text","text":"الأوامر الأساسية","size":"md","weight":"bold","color":c["text"],"margin":"lg"},
            {"type":"text","text":"بداية - العاب - نقاطي - الصدارة - ثيم - مساعدة","size":"sm","color":c["text_secondary"],"wrap":True,"margin":"sm"},
            {"type":"text","text":"التسجيل","size":"md","weight":"bold","color":c["text"],"margin":"lg"},
            {"type":"text","text":"تسجيل: للعب وحساب النقاط\nانسحب: تجاهل كامل (لن يرد البوت)","size":"sm","color":c["text_secondary"],"wrap":True,"margin":"sm"},
            {"type":"text","text":"المحتوى التفاعلي","size":"md","weight":"bold","color":c["text"],"margin":"lg"},
            {"type":"text","text":"تحدي - سؤال - اعتراف - منشن - موقف - حكمة - شخصية","size":"sm","color":c["text_secondary"],"wrap":True,"margin":"sm"},
            {"type":"text","text":"ملاحظات","size":"md","weight":"bold","color":c["text"],"margin":"lg"},
            {"type":"text","text":"ايقاف: يوقف اللعبة مؤقتاً\nانسحب: يتجاهلك البوت حتى تسجل","size":"xs","color":c["text_tertiary"],"wrap":True,"margin":"sm"},
            {"type":"separator","margin":"xl","color":c["border"]},
            {"type":"button","action":{"type":"message","label":"البداية","text":"بداية"},"style":"secondary","height":"sm","margin":"md"}
        ]
        bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        return FlexMessage(alt_text="المساعدة",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    ### ==================== ألعاب ====================

    def games_menu(self, user=None):
        c = self._c()
        games_list = ["ذكاء","خمن","رياضيات","ترتيب","ضد","اسرع","تكوين","انسان حيوان","اغاني","الوان"]
        contents = [{"type":"text","text":"الألعاب المتاحة","size":"xl","weight":"bold","color":c["primary"],"align":"center"}]

        for i in range(0,len(games_list),2):
            row = {"type":"box","layout":"horizontal","spacing":"sm","contents":[]}
            for j in range(2):
                if i+j < len(games_list):
                    row["contents"].append({
                        "type":"button",
                        "action":{"type":"message","label":games_list[i+j],"text":games_list[i+j]},
                        "style":"primary",
                        "height":"sm",
                        "flex":1,
                        "color":c["primary"]
                    })
            contents.append(row)

        contents.append({"type":"separator","margin":"lg","color":c["border"]})
        contents.append({"type":"button","action":{"type":"message","label":"البداية","text":"بداية"},"style":"secondary","height":"sm","margin":"md"})

        bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        return FlexMessage(alt_text="الالعاب",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    ### ==================== نافذة سؤال اللعبة ====================

    def game_question(self, question_text, round_num, total_rounds):
        c = self._c()
        contents = [
            {"type":"text","text":f"السؤال {round_num}/{total_rounds}","size":"md","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"md","color":c["border"]},
            {"type":"text","text":question_text,"size":"lg","weight":"bold","color":c["text"],"align":"center","margin":"lg","wrap":True},
            {"type":"box","layout":"horizontal","spacing":"md","margin":"xl","contents":[
                {"type":"button","action":{"type":"message","label":"لمح","text":"لمح"},"style":"primary","height":"md","flex":1,"color":c["primary"]},
                {"type":"button","action":{"type":"message","label":"جاوب","text":"جاوب"},"style":"secondary","height":"md","flex":1}
            ]}
        ]

        bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        return FlexMessage(alt_text=f"السؤال {round_num}/{total_rounds}",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    ### ==================== إعلان الفائز ====================

    def game_result(self, winner_name):
        c = self._c()
        contents = [
            {"type":"text","text":"انتهت اللعبة!","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"md","color":c["border"]},
            {"type":"text","text":f"الفائز: {winner_name}","size":"lg","weight":"bold","color":c["primary"],"align":"center","margin":"lg"},
            {"type":"button","action":{"type":"message","label":"البداية","text":"بداية"},"style":"secondary","height":"sm","margin":"xl"}
        ]
        bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        return FlexMessage(alt_text="انتهت اللعبة",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())
