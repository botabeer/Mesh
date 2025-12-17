from linebot.v3.messaging import FlexSendMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config

class UI:
    """واجهة المستخدم Flex UI للبوت مع دعم الثيمات والظلال"""
    
    def __init__(self, theme="light"):
        self.theme = theme

    def _c(self):
        """الحصول على ألوان الثيم الحالي"""
        return Config.get_theme(self.theme)

    def _qr(self):
        """Quick Reply جاهزة لجميع الأوامر الشائعة"""
        commands = [
            "العاب","نقاطي","الصدارة","تحدي","سؤال","اعتراف",
            "منشن","موقف","حكمة","شخصية","توافق","مافيا","مساعدة"
        ]
        return QuickReply(
            items=[QuickReplyItem(action=MessageAction(label=cmd, text=cmd)) for cmd in commands]
        )

    # =============================
    # القائمة الرئيسية
    # =============================
    def main_menu(self, user=None):
        c = self._c()
        contents = [
            {"type":"text","text":Config.BOT_NAME,"size":"xxl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"lg","color":c["border"]}
        ]

        if user:
            contents.append({
                "type":"box","layout":"horizontal","spacing":"md","margin":"lg","contents":[
                    {"type":"box","layout":"vertical","contents":[
                        {"type":"text","text":"اللاعب","size":"xs","color":c["text_tertiary"]},
                        {"type":"text","text":user['name'],"size":"md","weight":"bold","color":c["text"],"margin":"xs"}
                    ],"flex":3},
                    {"type":"box","layout":"vertical","contents":[
                        {"type":"text","text":"النقاط","size":"xs","color":c["text_tertiary"],"align":"end"},
                        {"type":"text","text":str(user['points']),"size":"xl","weight":"bold","color":c["primary"],"align":"end","margin":"xs"}
                    ],"flex":2}
                ],"paddingAll":"md","cornerRadius":"md","backgroundColor":c["glass"],"borderWidth":"1px","borderColor":c["border"],"shadow":c.get("shadow", "none")}
            )

        # أزرار أساسية
        contents.append({
            "type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[
                {"type":"button","action":{"type":"message","label":"العاب","text":"العاب"},"style":"primary","color":c["primary"],"flex":1,"height":"sm"},
                {"type":"button","action":{"type":"message","label":"نقاطي" if user else "تسجيل","text":"نقاطي" if user else "تسجيل"},"style":"secondary","flex":1,"height":"sm"}
            ]
        })

        # أزرار إضافية
        if user:
            contents.append({
                "type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[
                    {"type":"button","action":{"type":"message","label":"تغيير الاسم","text":"تغيير الاسم"},"style":"secondary","flex":1,"height":"sm"},
                    {"type":"button","action":{"type":"message","label":"تبديل الثيم","text":"ثيم"},"style":"secondary","flex":1,"height":"sm"}
                ]
            })
        else:
            contents.append({
                "type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[
                    {"type":"button","action":{"type":"message","label":"انسحب","text":"انسحب"},"style":"secondary","flex":1,"height":"sm"},
                    {"type":"button","action":{"type":"message","label":"مساعدة","text":"مساعدة"},"style":"secondary","flex":1,"height":"sm"}
                ]
            })

        # الحقوق
        contents.extend([
            {"type":"separator","margin":"xl","color":c["border"]},
            {"type":"text","text":Config.COPYRIGHT,"size":"xxs","color":c["text_tertiary"],"align":"center","wrap":True,"margin":"md"}
        ])

        bubble = {"type":"bubble","size":"mega","body":{
            "type":"box","layout":"vertical","contents":contents,
            "paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"
        }}

        return FlexSendMessage(alt_text="البداية",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    # =============================
    # قائمة المساعدة
    # =============================
    def help_menu(self):
        c = self._c()
        contents = [
            {"type":"text","text":"دليل الاستخدام","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"lg","color":c["border"]},
            {"type":"text","text":"الأوامر الأساسية: بداية - العاب - نقاطي - الصدارة - ثيم - مساعدة","size":"sm","color":c["text_secondary"],"wrap":True,"margin":"md"}
        ]
        bubble = {"type":"bubble","size":"mega","body":{
            "type":"box","layout":"vertical","contents":contents,
            "paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"
        }}
        return FlexSendMessage(alt_text="المساعدة",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    # =============================
    # قائمة الألعاب
    # =============================
    def games_menu(self, user=None):
        c = self._c()
        games_list = [
            ["ذكاء", "خمن"],["رياضيات", "ترتيب"],["ضد", "اسرع"],
            ["سلسله", "انسان حيوان"],["تكوين", "اغاني"],["الوان", "توافق"],["مافيا",""]
        ]
        contents = [
            {"type":"text","text":"الألعاب المتاحة","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"lg","color":c["border"]}
        ]

        for row in games_list:
            if row[1]:
                contents.append({
                    "type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[
                        {"type":"button","action":{"type":"message","label":row[0],"text":row[0]},"style":"primary","color":c["primary"],"flex":1,"height":"sm"},
                        {"type":"button","action":{"type":"message","label":row[1],"text":row[1]},"style":"primary","color":c["primary"],"flex":1,"height":"sm"}
                    ]
                })
            else:
                contents.append({
                    "type":"button","action":{"type":"message","label":row[0],"text":row[0]},"style":"primary","color":c["primary"],"margin":"sm","height":"sm"}
                })

        bubble = {"type":"bubble","size":"mega","body":{
            "type":"box","layout":"vertical","contents":contents,
            "paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"
        }}
        return FlexSendMessage(alt_text="الالعاب",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    # =============================
    # بطاقة الإحصائيات
    # =============================
    def stats_card(self, user):
        c = self._c()
        win_rate = round((user['wins'] / user['games']) * 100) if user['games'] > 0 else 0

        contents = [
            {"type":"text","text":"إحصائياتي","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"lg","color":c["border"]},
            {"type":"box","layout":"horizontal","spacing":"md","margin":"lg","contents":[
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":"النقاط","size":"xs","color":c["text_tertiary"],"align":"center"},
                    {"type":"text","text":str(user['points']),"size":"xxl","weight":"bold","color":c["success"],"align":"center"}
                ],"flex":1,"paddingAll":"md","cornerRadius":"md","backgroundColor":c["card"],"borderWidth":"1px","borderColor":c["border"]},
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":"الألعاب","size":"xs","color":c["text_tertiary"],"align":"center"},
                    {"type":"text","text":str(user['games']),"size":"xxl","weight":"bold","color":c["info"],"align":"center"}
                ],"flex":1,"paddingAll":"md","cornerRadius":"md","backgroundColor":c["card"],"borderWidth":"1px","borderColor":c["border"]}
            ]},
            {"type":"box","layout":"horizontal","spacing":"md","margin":"md","contents":[
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":"الانتصارات","size":"xs","color":c["text_tertiary"],"align":"center"},
                    {"type":"text","text":str(user['wins']),"size":"xl","weight":"bold","color":c["primary"],"align":"center"}
                ],"flex":1,"paddingAll":"md","cornerRadius":"md","backgroundColor":c["card"],"borderWidth":"1px","borderColor":c["border"]},
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":"نسبة الفوز","size":"xs","color":c["text_tertiary"],"align":"center"},
                    {"type":"text","text":f"{win_rate}%","size":"xl","weight":"bold","color":c["warning"],"align":"center"}
                ],"flex":1,"paddingAll":"md","cornerRadius":"md","backgroundColor":c["card"],"borderWidth":"1px","borderColor":c["border"]}
            ]}
        ]

        bubble = {"type":"bubble","size":"mega","body":{
            "type":"box","layout":"vertical","contents":contents,
            "paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"
        }}
        return FlexSendMessage(alt_text="إحصائياتي",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())
        
    # =============================
    # لوحة الصدارة
    # =============================
    def leaderboard_card(self, leaderboard):
        c = self._c()
        contents = [
            {"type":"text","text":"لوحة الصدارة","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"text","text":"أفضل 10 لاعبين","size":"xs","color":c["text_tertiary"],"align":"center","margin":"xs"},
            {"type":"separator","margin":"lg","color":c["border"]}
        ]

        if not leaderboard:
            contents.append({
                "type":"box","layout":"vertical","contents":[
                    {"type":"text","text":"لا توجد بيانات بعد","size":"md","color":c["text_secondary"],"align":"center","wrap":True}
                ],"paddingAll":"xl","cornerRadius":"md","backgroundColor":c["glass"],"margin":"lg","shadow":c.get("shadow","none")}
            })
        else:
            for idx, player in enumerate(leaderboard[:10]):
                rank = idx + 1
                border_width = "3px" if rank == 1 else "2px" if rank <= 3 else "1px"
                bg_color = c["glass"] if rank <= 3 else c["card"]
                contents.append({
                    "type":"box","layout":"horizontal","spacing":"md","contents":[
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":str(rank),"size":"xl","weight":"bold","align":"center","color":c["primary"]}
                        ],"flex":0,"width":"40px","justifyContent":"center"},
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":player['name'],"size":"md","weight":"bold","color":c["text"],"wrap":True},
                            {"type":"box","layout":"horizontal","spacing":"md","margin":"xs","contents":[
                                {"type":"text","text":f"النقاط: {player['points']}","size":"xs","color":c["text_secondary"],"flex":0},
                                {"type":"text","text":f"الفوز: {player['wins']}","size":"xs","color":c["text_secondary"],"flex":0}
                            ]}
                        ],"flex":1}
                    ],"paddingAll":"md","cornerRadius":"md","backgroundColor":bg_color,"borderWidth":border_width,"borderColor":c["border"],"margin":"sm","shadow":c.get("shadow","none")}
                })

        contents.append({
            "type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[
                {"type":"button","action":{"type":"message","label":"البداية","text":"بداية"},"style":"secondary","height":"sm","flex":1},
                {"type":"button","action":{"type":"message","label":"نقاطي","text":"نقاطي"},"style":"primary","color":c["primary"],"height":"sm","flex":1}
            ]
        })

        bubble = {"type":"bubble","size":"mega","body":{
            "type":"box","layout":"vertical","contents":contents,
            "paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"
        }}
        return FlexSendMessage(alt_text="لوحة الصدارة",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    # =============================
    # اختيار التسجيل
    # =============================
    def registration_choice(self):
        c = self._c()
        contents = [
            {"type":"text","text":"مرحباً بك","size":"xxl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"lg","color":c["border"]},
            {"type":"box","layout":"vertical","contents":[
                {"type":"text","text":"للعب وكسب النقاط","size":"md","color":c["text"],"wrap":True,"align":"center","weight":"bold"},
                {"type":"text","text":"سجل حسابك الآن","size":"sm","color":c["text_secondary"],"wrap":True,"align":"center","margin":"sm"}
            ],"paddingAll":"md","cornerRadius":"md","backgroundColor":c["glass"],"margin":"lg","shadow":c.get("shadow","none")},
            {"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[
                {"type":"button","action":{"type":"message","label":"تسجيل","text":"تسجيل"},"style":"primary","color":c["success"],"height":"sm","flex":1},
                {"type":"button","action":{"type":"message","label":"انسحب","text":"انسحب"},"style":"secondary","height":"sm","flex":1}
            ]}
        ]
        bubble = {"type":"bubble","size":"mega","body":{
            "type":"box","layout":"vertical","contents":contents,
            "paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"
        }}
        return FlexSendMessage(alt_text="مرحباً",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    # =============================
    # إدخال الاسم
    # =============================
    def ask_name(self):
        c = self._c()
        contents = [
            {"type":"text","text":"التسجيل","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"md","color":c["border"]},
            {"type":"box","layout":"vertical","contents":[
                {"type":"text","text":"يرجى إدخال اسمك","size":"md","color":c["text"],"wrap":True,"align":"center","weight":"bold"},
                {"type":"text","text":"من 1 إلى 50 حرف","size":"xs","color":c["text_tertiary"],"align":"center","margin":"sm"}
            ],"paddingAll":"lg","cornerRadius":"md","backgroundColor":c["glass"],"margin":"lg","shadow":c.get("shadow","none")}
        ]
        bubble = {"type":"bubble","size":"mega","body":{
            "type":"box","layout":"vertical","contents":contents,
            "paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"
        }}
        return FlexSendMessage(alt_text="إدخال الاسم",contents=FlexContainer.from_dict(bubble))

    # =============================
    # اسم غير صالح
    # =============================
    def ask_name_invalid(self):
        c = self._c()
        contents = [
            {"type":"text","text":"اسم غير صالح","size":"lg","weight":"bold","color":c["danger"],"align":"center"},
            {"type":"separator","margin":"md","color":c["border"]},
            {"type":"box","layout":"vertical","contents":[
                {"type":"text","text":"يرجى إدخال اسم صحيح","size":"sm","color":c["text"],"wrap":True},
                {"type":"text","text":"من 1 إلى 50 حرف","size":"xs","color":c["text_secondary"],"margin":"sm"},
                {"type":"text","text":"حروف عربية أو إنجليزية فقط","size":"xs","color":c["text_secondary"],"margin":"xs"},
                {"type":"text","text":"لا يمكن استخدام أوامر البوت كاسم","size":"xs","color":c["text_secondary"],"margin":"xs"}
            ],"paddingAll":"md","cornerRadius":"md","backgroundColor":c["glass"],"margin":"lg","shadow":c.get("shadow","none")}
        ]
        bubble = {"type":"bubble","size":"mega","body":{
            "type":"box","layout":"vertical","contents":contents,
            "paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"
        }}
        return FlexSendMessage(alt_text="اسم غير صالح",contents=FlexContainer.from_dict(bubble))

    # =============================
    # إيقاف اللعبة
    # =============================
    def game_stopped(self):
        c = self._c()
        contents = [
            {"type":"text","text":"تم إيقاف اللعبة","size":"xl","weight":"bold","color":c["warning"],"align":"center"},
            {"type":"separator","margin":"md","color":c["border"]},
            {"type":"text","text":"يمكنك بدء لعبة جديدة في أي وقت","size":"sm","color":c["text_secondary"],"wrap":True,"align":"center","margin":"lg"},
            {"type":"button","action":{"type":"message","label":"العاب","text":"العاب"},"style":"primary","color":c["primary"],"height":"sm","margin":"lg"}
        ]
        bubble = {"type":"bubble","body":{
            "type":"box","layout":"vertical","contents":contents,
            "paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"
        }}
        return FlexSendMessage(alt_text="تم الإيقاف",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    # =============================
    # تبديل الثيم
    # =============================
    def theme_changed(self, theme_name):
        c = self._c()
        contents = [
            {"type":"text","text":"تم تبديل الثيم","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"md","color":c["border"]},
            {"type":"box","layout":"vertical","contents":[
                {"type":"text","text":theme_name,"size":"lg","color":c["text"],"wrap":True,"align":"center","weight":"bold"}
            ],"paddingAll":"md","cornerRadius":"md","backgroundColor":c["glass"],"margin":"lg","shadow":c.get("shadow","none")}
        ]
        bubble = {"type":"bubble","body":{
            "type":"box","layout":"vertical","contents":contents,
            "paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"
        }}
        return FlexSendMessage(alt_text="تم التبديل",contents=FlexContainer.from_dict(bubble))
