from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config

class UI:
    def __init__(self, theme="light"):
        self.theme = theme
    def _c(self): return Config.get_theme(self.theme)
    def _qr(self): return QuickReply(items=[
        QuickReplyItem(action=MessageAction(label="القائمة", text="بداية")),
        QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
        QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
        QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
        QuickReplyItem(action=MessageAction(label="ايقاف", text="ايقاف")),
        QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
    ])
    def main_menu(self,user=None):
        c=self._c()
        contents=[{"type":"box","layout":"vertical","contents":[{"type":"text","text":Config.BOT_NAME,"size":"xxl","weight":"bold","color":c["primary"],"align":"center"},{"type":"text","text":f"الإصدار {Config.VERSION}","size":"xs","color":c["text_tertiary"],"align":"center","margin":"xs"}],"paddingAll":"md","backgroundColor":c["card"],"cornerRadius":"md"},{"type":"separator","margin":"xl","color":c["border"]}]
        if user: contents.append({"type":"box","layout":"horizontal","contents":[{"type":"box","layout":"vertical","contents":[{"type":"text","text":"اللاعب","size":"xs","color":c["text_tertiary"]},{"type":"text","text":user['name'],"size":"md","weight":"bold","color":c["text"],"margin":"xs"}],"flex":3},{"type":"box","layout":"vertical","contents":[{"type":"text","text":"النقاط","size":"xs","color":c["text_tertiary"],"align":"end"},{"type":"text","text":str(user['points']),"size":"xl","weight":"bold","color":c["primary"],"align":"end","margin":"xs"}],"flex":2}],"margin":"xl","paddingAll":"md","cornerRadius":"md","backgroundColor":c["glass"],"borderWidth":"1px","borderColor":c["border"]})
        contents.extend([{"type":"separator","margin":"xl","color":c["border"]},{"type":"button","action":{"type":"message","label":"الالعاب","text":"العاب"},"style":"primary","color":c["primary"],"margin":"md","height":"md"},{"type":"box","layout":"horizontal","spacing":"md","margin":"md","contents":[{"type":"button","action":{"type":"message","label":"نقاطي" if user else "تسجيل","text":"نقاطي" if user else "تسجيل"},"style":"secondary","height":"sm","flex":1},{"type":"button","action":{"type":"message","label":"الصدارة","text":"الصدارة"},"style":"secondary","height":"sm","flex":1}]}])
        if user: contents.append({"type":"box","layout":"horizontal","spacing":"md","margin":"sm","contents":[{"type":"button","action":{"type":"message","label":"تغيير الاسم","text":"تغيير الاسم"},"style":"secondary","height":"sm","flex":1},{"type":"button","action":{"type":"message","label":"تبديل الثيم","text":"ثيم"},"style":"secondary","height":"sm","flex":1}]})
        else: contents.append({"type":"button","action":{"type":"message","label":"تجاهل البوت","text":"انسحب"},"style":"secondary","height":"sm","margin":"sm"})
        contents.extend([{"type":"separator","margin":"xl","color":c["border"]},{"type":"text","text":Config.COPYRIGHT,"size":"xxs","color":c["text_tertiary"],"align":"center","wrap":True,"margin":"md"}])
        bubble={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        return FlexMessage(alt_text="البداية",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    def games_menu(self):
        c=self._c()
        games_registered=["ذكاء","خمن","رياضيات","ترتيب","ضد","اسرع","سلسله","انسان حيوان","كون كلمات","اغاني","الوان"]
        games_no_register=["توافق","مافيا"]
        interactive=["تحدي","سؤال","اعتراف","منشن","موقف","حكمة","شخصية"]
        def make_rows(items,style="primary"):
            rows=[]
            for i in range(0,len(items),2):
                row={"type":"box","layout":"horizontal","spacing":"sm","contents":[]}
                for j in range(2):
                    if i+j<len(items):
                        row["contents"].append({"type":"button","action":{"type":"message","label":items[i+j],"text":items[i+j]},"style":style,"height":"sm","flex":1,"color":c["primary"] if style=="primary" else None})
                rows.append(row)
            return rows
        contents=[{"type":"box","layout":"vertical","contents":[{"type":"text","text":"الألعاب المتاحة","size":"xl","weight":"bold","color":c["primary"],"align":"center"}],"paddingAll":"md","backgroundColor":c["card"],"cornerRadius":"md"},{"type":"separator","margin":"lg","color":c["border"]},{"type":"text","text":"ألعاب تحتاج تسجيل","size":"sm","weight":"bold","color":c["text"],"margin":"lg"}]
        contents.extend(make_rows(games_registered,"primary"))
        contents.append({"type":"separator","margin":"lg","color":c["border"]})
        contents.append({"type":"text","text":"ألعاب بدون تسجيل","size":"sm","weight":"bold","color":c["text"],"margin":"lg"})
        contents.extend(make_rows(games_no_register,"secondary"))
        contents.append({"type":"separator","margin":"lg","color":c["border"]})
        contents.append({"type":"text","text":"محتوى تفاعلي","size":"sm","weight":"bold","color":c["secondary"],"margin":"lg"})
        contents.extend(make_rows(interactive,"secondary"))
        contents.append({"type":"separator","margin":"xl","color":c["border"]})
        contents.append({"type":"button","action":{"type":"message","label":"البداية","text":"بداية"},"style":"secondary","height":"sm","margin":"md"})
        bubble={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        return FlexMessage(alt_text="الالعاب",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    def help_menu(self):
        c=self._c()
        contents=[{"type":"text","text":"دليل الاستخدام","size":"xl","weight":"bold","color":c["primary"],"align":"center"},{"type":"separator","margin":"lg","color":c["border"]},{"type":"text","text":"الاوامر الاساسية","size":"md","weight":"bold","color":c["text"],"margin":"lg"},{"type":"text","text":"بداية - العاب - نقاطي - الصدارة - ثيم - مساعدة","size":"sm","color":c["text_secondary"],"wrap":True,"margin":"sm"},{"type":"text","text":"التسجيل","size":"md","weight":"bold","color":c["text"],"margin":"lg"},{"type":"text","text":"تسجيل: للعب وحساب النقاط\nانسحب: تجاهل كامل (لن يرد البوت)","size":"sm","color":c["text_secondary"],"wrap":True,"margin":"sm"},{"type":"text","text":"المحتوى التفاعلي","size":"md","weight":"bold","color":c["text"],"margin":"lg"},{"type":"text","text":"تحدي - سؤال - اعتراف - منشن - موقف - حكمة - شخصية","size":"sm","color":c["text_secondary"],"wrap":True,"margin":"sm"},{"type":"text","text":"ملاحظات","size":"md","weight":"bold","color":c["text"],"margin":"lg"},{"type":"text","text":"ايقاف: يوقف اللعبة مؤقتاً\nانسحب: يتجاهلك البوت حتى تسجل","size":"xs","color":c["text_tertiary"],"wrap":True,"margin":"sm"},{"type":"separator","margin":"xl","color":c["border"]},{"type":"text","text":Config.COPYRIGHT,"size":"xxs","color":c["text_tertiary"],"align":"center","wrap":True,"margin":"md"},{"type":"button","action":{"type":"message","label":"البداية","text":"بداية"},"style":"secondary","height":"sm","margin":"md"}]
        bubble={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        return FlexMessage(alt_text="المساعدة",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    def stats_card(self,user):
        c=self._c()
        win_rate=round((user['wins']/user['games']*100)) if user['games']>0 else 0
        contents=[{"type":"text","text":"احصائياتي","size":"xl","weight":"bold","color":c["primary"],"align":"center"},{"type":"separator","margin":"lg","color":c["border"]},{"type":"box","layout":"vertical","spacing":"sm","margin":"lg","contents":[self._stat_row("الاسم",user['name'],c),self._stat_row("النقاط",str(user['points']),c,True),self._stat_row("الالعاب",str(user['games']),c),self._stat_row("الفوز",str(user['wins']),c),self._stat_row("نسبة الفوز",f"{win_rate}%",c)]},{"type":"separator","margin":"xl","color":c["border"]},{"type":"button","action":{"type":"message","label":"البداية","text":"بداية"},"style":"secondary","height":"sm","margin":"md"}]
        bubble={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        return FlexMessage(alt_text="احصائياتي",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    def _stat_row(self,label,value,c,highlight=False): return {"type":"box","layout":"horizontal","contents":[{"type":"text","text":label,"size":"sm","color":c["text_secondary"],"flex":2},{"type":"text","text":value,"size":"md","weight":"bold","color":c["primary"] if highlight else c["text"],"align":"end","flex":3}],"paddingAll":"sm","cornerRadius":"sm","backgroundColor":c["glass"]}

    def leaderboard_card(self,top_users):
        c=self._c()
        contents=[{"type":"text","text":"لوحة الصدارة","size":"xl","weight":"bold","color":c["primary"],"align":"center"},{"type":"separator","margin":"lg","color":c["border"]}]
        for i,u in enumerate(top_users,1):
            contents.append({"type":"box","layout":"horizontal","contents":[{"type":"text","text":f"{i}","size":"lg","weight":"bold","color":c["primary"],"flex":1,"align":"center"},{"type":"box","layout":"vertical","contents":[{"type":"text","text":u['name'],"size":"md","weight":"bold","color":c["text"]},{"type":"text","text":f"{u['wins']} فوز","size":"xs","color":c["text_tertiary"]}],"flex":4},{"type":"text","text":str(u['points']),"size":"lg","weight":"bold","color":c["primary"],"flex":2,"align":"end"}],"margin":"md","paddingAll":"sm","cornerRadius":"sm","backgroundColor":c["glass"]})
        contents.extend([{"type":"separator","margin":"xl","color":c["border"]},{"type":"button","action":{"type":"message","label":"البداية","text":"بداية"},"style":"secondary","height":"sm","margin":"md"}])
        bubble={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        return FlexMessage(alt_text="الصدارة",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    def ask_name(self):
        c=self._c()
        contents=[{"type":"text","text":"التسجيل","size":"xl","weight":"bold","color":c["primary"],"align":"center"},{"type":"separator","margin":"lg","color":c["border"]},{"type":"text","text":"ادخل اسمك للبدء","size":"md","color":c["text"],"align":"center","margin":"xl","wrap":True},{"type":"text","text":"حرف واحد على الاقل","size":"xs","color":c["text_tertiary"],"align":"center","margin":"sm"},{"type":"button","action":{"type":"message","label":"تجاهلني","text":"انسحب"},"style":"secondary","height":"sm","margin":"lg"}]
        bubble={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        return FlexMessage(alt_text="تسجيل",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    def ask_name_invalid(self): return self.ask_name()
    def ask_new_name(self): return self.ask_name()
    def ask_new_name_invalid(self): return self.ask_name()
    def game_stopped(self): return self.ask_name()
    def registration_choice(self): return self.ask_name()
