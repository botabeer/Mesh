from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from config import Config

class UIBuilder:
    def _flex(self, alt: str, body: dict):
        return FlexMessage(alt_text=alt, contents=FlexContainer.from_dict(body))
    
    def _col(self, theme: str = None):
        return Config.get_theme(theme)
    
    def home_screen(self, user: str, pts: int, is_reg: bool, theme: str, mode: str):
        c = self._col(theme)
        st = "مسجل" if is_reg else "زائر"
        sc = c["success"] if is_reg else c["text3"]
        
        return self._flex("Home", {
            "type":"bubble","size":"mega",
            "body":{"type":"box","layout":"vertical","contents":[
                {"type":"text","text":Config.BOT_NAME,"size":"xxl","weight":"bold","color":c["primary"],"align":"center"},
                {"type":"separator","margin":"lg","color":c["border"]},
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":user[:30],"size":"lg","weight":"bold","color":c["text"]},
                    {"type":"text","text":st,"size":"sm","color":sc,"margin":"xs"},
                    {"type":"separator","margin":"md","color":c["border"]},
                    {"type":"box","layout":"horizontal","contents":[
                        {"type":"text","text":"النقاط","size":"md","color":c["text2"],"flex":1},
                        {"type":"text","text":str(pts),"size":"xxl","weight":"bold","color":c["primary"],"flex":0}
                    ],"margin":"md"}
                ],"backgroundColor":c["card"],"cornerRadius":"12px","paddingAll":"16px","borderWidth":"1px","borderColor":c["border"],"margin":"md"},
                {"type":"text","text":f"الوضع {mode}","size":"sm","color":c["text2"],"align":"center","margin":"lg"},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[
                    {"type":"button","action":{"type":"message","label":"انضم","text":"انضم"},"style":"primary","height":"sm","color":c["primary"]},
                    {"type":"button","action":{"type":"message","label":"العاب","text":"العاب"},"style":"secondary","height":"sm"}
                ]},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[
                    {"type":"button","action":{"type":"message","label":"نقاطي","text":"نقاطي"},"style":"secondary","height":"sm"},
                    {"type":"button","action":{"type":"message","label":"صدارة","text":"صدارة"},"style":"secondary","height":"sm"}
                ]}
            ],"paddingAll":"20px","backgroundColor":c["bg"]}
        })
    
    def games_menu(self, theme: str, top: list = None):
        c = self._col(theme)
        default = ["اسرع","ذكاء","لعبة","خمن","اغنيه","سلسلة","ترتيب","تكوين","ضد","لون","رياضيات","توافق","روليت"]
        order = (top + [g for g in default if g not in top])[:13] if top else default[:13]
        
        rows = []
        for i in range(0, len(order), 3):
            row = {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[]}
            for j in range(3):
                if i + j < len(order):
                    row["contents"].append({"type":"button","action":{"type":"message","label":order[i+j],"text":order[i+j]},"style":"primary","height":"sm","color":c["primary"]})
            rows.append(row)
        
        return self._flex("Games", {
            "type":"bubble","size":"mega",
            "body":{"type":"box","layout":"vertical","contents":[
                {"type":"text","text":"الالعاب","size":"xxl","weight":"bold","color":c["primary"],"align":"center"},
                {"type":"separator","margin":"lg","color":c["border"]},
                *rows,
                {"type":"separator","margin":"lg","color":c["border"]},
                {"type":"text","text":"لمح - جاوب - ايقاف","size":"xs","color":c["text2"],"align":"center","margin":"sm"}
            ],"paddingAll":"20px","backgroundColor":c["bg"]}
        })
    
    def help_screen(self, theme: str):
        c = self._col(theme)
        return self._flex("Help", {
            "type":"bubble","size":"mega",
            "body":{"type":"box","layout":"vertical","contents":[
                {"type":"text","text":"المساعدة","size":"xxl","weight":"bold","color":c["primary"],"align":"center"},
                {"type":"separator","margin":"lg","color":c["border"]},
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":"الاوامر","size":"md","weight":"bold","color":c["text"]},
                    {"type":"text","text":"بداية - العاب - نقاطي - صدارة","size":"sm","color":c["text2"],"wrap":True,"margin":"sm"},
                    {"type":"separator","margin":"md","color":c["border"]},
                    {"type":"text","text":"اوامر اللعبة","size":"md","weight":"bold","color":c["text"],"margin":"md"},
                    {"type":"text","text":"لمح - جاوب - ايقاف","size":"sm","color":c["text2"],"wrap":True,"margin":"sm"},
                    {"type":"separator","margin":"md","color":c["border"]},
                    {"type":"text","text":"الثيمات","size":"md","weight":"bold","color":c["text"],"margin":"md"},
                    {"type":"text","text":"ثيم [الاسم]","size":"sm","color":c["text2"],"wrap":True,"margin":"sm"}
                ],"backgroundColor":c["card"],"cornerRadius":"12px","paddingAll":"16px","borderWidth":"1px","borderColor":c["border"],"margin":"md"}
            ],"paddingAll":"20px","backgroundColor":c["bg"]}
        })
    
    def my_points(self, user: str, pts: int, stats: dict, theme: str):
        c = self._col(theme)
        return self._flex("Points", {
            "type":"bubble","size":"mega",
            "body":{"type":"box","layout":"vertical","contents":[
                {"type":"text","text":"احصائياتي","size":"xxl","weight":"bold","color":c["primary"],"align":"center"},
                {"type":"separator","margin":"lg","color":c["border"]},
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":user[:30],"size":"lg","weight":"bold","color":c["text"],"align":"center"},
                    {"type":"text","text":f"النقاط {pts}","size":"xxl","weight":"bold","color":c["primary"],"align":"center","margin":"md"}
                ],"backgroundColor":c["card"],"cornerRadius":"12px","paddingAll":"16px","borderWidth":"1px","borderColor":c["border"],"margin":"md"}
            ],"paddingAll":"20px","backgroundColor":c["bg"]}
        })
    
    def leaderboard(self, top: list, theme: str):
        c = self._col(theme)
        rows = []
        for i, (name, pts, is_reg) in enumerate(top[:20], 1):
            rank = str(i)
            rows.append({"type":"box","layout":"horizontal","contents":[
                {"type":"text","text":rank,"size":"md","weight":"bold","color":c["primary"] if i<=3 else c["text2"],"flex":0},
                {"type":"separator","margin":"md","color":c["border"]},
                {"type":"text","text":name[:20],"size":"sm","color":c["text"],"flex":3,"margin":"md"},
                {"type":"separator","margin":"md","color":c["border"]},
                {"type":"text","text":str(pts),"size":"sm","weight":"bold","color":c["primary"],"flex":1,"align":"center"},
                {"type":"separator","margin":"md","color":c["border"]},
                {"type":"text","text":"R" if is_reg else "G","size":"xs","color":c["success"] if is_reg else c["text3"],"flex":1,"align":"center"}
            ],"paddingAll":"10px","backgroundColor":c["card"],"cornerRadius":"8px","borderWidth":"1px","borderColor":c["border"],"margin":"xs"})
        
        return self._flex("Ranks", {
            "type":"bubble","size":"mega",
            "body":{"type":"box","layout":"vertical","contents":[
                {"type":"text","text":"الصدارة","size":"xxl","weight":"bold","color":c["primary"],"align":"center"},
                {"type":"separator","margin":"lg","color":c["border"]},
                {"type":"box","layout":"vertical","contents":rows,"margin":"md"}
            ],"paddingAll":"20px","backgroundColor":c["bg"]}
        })
    
    def registration_prompt(self, theme: str):
        return TextMessage(text="ارسل اسمك ")
    
    def registration_success(self, user: str, pts: int, theme: str):
        return TextMessage(text=f"تم التسجيل\n\nالاسم {user}\nالنقاط {pts}")
    
    def unregister_confirm(self, user: str, pts: int, theme: str):
        return TextMessage(text=f"تم الانسحاب\n\nالاسم {user}\nالنقاط {pts}")
    
    def game_stopped(self, game: str, theme: str):
        return TextMessage(text=f"تم ايقاف {game}")
