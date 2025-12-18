import random, logging
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config

logger = logging.getLogger(__name__)

class MafiaGame:
    MIN_PLAYERS, MAX_PLAYERS = 4, 12
    def __init__(self, db, theme="light"):
        self.db, self.theme = db, theme
        self.game_name = "مافيا"
        self.players = {}  # {user_id: {"name":str,"role":str,"alive":bool}}
        self.phase = "registration"
        self.day = 0
        self.votes = {}
        self.night_actions = {}
        self.alive_players = []
        self.dead_players = []
        self.game_active = False
        self.mafia_list = []
        self.detective = None
        self.doctor = None

    # --- أدوات Flex ---
    def _c(self): return Config.get_theme(self.theme)
    def _qr(self): items=["سؤال","منشن","تحدي","اعتراف","شخصية","حكمة","موقف","بداية","العاب","مساعدة"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i,text=i)) for i in items])
    def _separator(self,m="md"): return {"type":"separator","margin":m}
    def _glass_box(self,contents,padding="16px",margin="none"):
        c=self._c()
        return {"type":"box","layout":"vertical","contents":contents,
                "backgroundColor":c["card_secondary"] if self.theme=="light" else "#1A202C",
                "cornerRadius":"16px","paddingAll":padding,"spacing":"sm","margin":margin}
    def _create_bubble(self,title,contents,buttons=None):
        c=self._c()
        body=[{"type":"text","text":title,"size":"xl","weight":"bold","color":c["primary"],"align":"center"},self._separator("lg")]
        body.extend(contents)
        if buttons: body.append(self._separator("lg")); body.extend(buttons)
        bubble={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":body,"backgroundColor":c["card"],"paddingAll":"24px"}}
        return FlexMessage(alt_text=title,contents=FlexContainer.from_dict(bubble),quickReply=self._qr())

    # --- شاشة تسجيل اللاعبين ---
    def registration_screen(self):
        c=self._c()
        contents=[self._glass_box([
            {"type":"text","text":"يجب إضافة البوت كصديق قبل الانضمام","size":"sm","color":"#FF0000","weight":"bold","align":"center"},
            {"type":"text","text":f"اللاعبون المسجلون: {len(self.players)}","size":"md","color":c["text"],"weight":"bold","align":"center"},
            {"type":"text","text":f"الحد الأدنى: {self.MIN_PLAYERS} لاعبين","size":"xs","color":c["text_secondary"],"align":"center","margin":"sm"},
            {"type":"text","text":f"الحد الأقصى: {self.MAX_PLAYERS} لاعبين","size":"xs","color":c["text_tertiary"],"align":"center","margin":"xs"}
        ],"20px","lg")]
        if self.players:
            buttons=[]
            for uid,pdata in self.players.items():
                buttons.append({"type":"button","action":{"type":"message","label":pdata["name"],"text":pdata["name"]},"style":"secondary","margin":"sm"})
            contents.append(self._glass_box([{"type":"text","text":"اللاعبون:","size":"sm","color":c["text_secondary"],"weight":"bold"},{"type":"box","layout":"vertical","contents":buttons,"spacing":"sm"}],"12px","md"))
        action_buttons=[{"type":"button","action":{"type":"message","label":"انضم","text":"انضم مافيا"},"style":"primary","height":"sm","flex":1},{"type":"button","action":{"type":"message","label":"بدء اللعبة","text":"بدء مافيا"},"style":"primary","height":"sm","flex":1}]
        return self._create_bubble("تسجيل المافيا",contents,[{"type":"box","layout":"horizontal","contents":action_buttons,"spacing":"sm","margin":"md"}])

    # --- شاشة التعليمات ---
    def instructions_screen(self):
        c=self._c()
        contents=[self._glass_box([
            {"type":"text","text":"طريقة اللعب","size":"md","color":c["text"],"weight":"bold"},
            {"type":"text","text":"في القروب: النقاش والتصويت\nالمافيا: يختار ضحية\nالمحقق: يسأل عن لاعب\nالطبيب: يحمي لاعب\nالمواطن: يصوت ويناقش","size":"xs","color":c["text_secondary"],"wrap":True,"margin":"sm"}
        ],"16px","lg")]
        return self._create_bubble("شرح المافيا",contents,None)

    # --- بدء اللعبة ---
    def start(self,user_id):
        try:
            self.phase, self.game_active, self.players, self.alive_players, self.dead_players = "registration", True, {}, [], []
            self.day, self.votes, self.night_actions, self.mafia_list, self.detective, self.doctor = 0, {}, {}, [], None, None
            return self.registration_screen()
        except Exception as e: logger.error(f"Error in start: {e}"); from linebot.v3.messaging import TextMessage; return TextMessage(text="حدث خطأ في بدء لعبة المافيا. حاول مرة أخرى.")

    # --- التحقق من الأوامر ---
    def check(self,text,user_id):
        try:
            cmd=Config.normalize(text)
            if self.phase=="registration":
                if cmd=="انضم مافيا": return self.add_player(user_id)
                elif cmd=="بدء مافيا": return self.assign_roles()
                elif cmd in ("الحاله","الحالة"): return {"response":self.registration_screen(),"game_over":False}
                elif cmd=="شرح": return {"response":self.instructions_screen(),"game_over":False}
            elif self.phase=="voting" and cmd.startswith("صوت "): return self.cast_vote(user_id,text[4:].strip())
            elif self.phase=="night": return self.night_phase_action(user_id,cmd)
            return None
        except Exception as e: logger.error(f"Error in check: {e}"); return None

    # --- إضافة لاعب ---
    def add_player(self,user_id):
        try:
            c=self._c()
            if self.phase!="registration": return {"response":self._create_bubble("خطأ",[self._glass_box([{"type":"text","text":"التسجيل مغلق","size":"md","color":c["text"],"align":"center"}],"16px","lg")],None),"game_over":False}
            if user_id in self.players: return {"response":self._create_bubble("خطأ",[self._glass_box([{"type":"text","text":"أنت مسجل بالفعل","size":"md","color":c["text"],"align":"center"}],"16px","lg")],None),"game_over":False}
            if len(self.players)>=self.MAX_PLAYERS: return {"response":self._create_bubble("خطأ",[self._glass_box([{"type":"text","text":"اللعبة ممتلئة","size":"md","color":c["text"],"align":"center"}],"16px","lg")],None),"game_over":False}
            user=self.db.get_user(user_id); name=user["name"] if user else f"لاعب{len(self.players)+1}"; self.players[user_id]={"name":name,"role":None,"alive":True}
            return {"response":self.registration_screen(),"game_over":False}
        except Exception as e: logger.error(f"Error in add_player: {e}"); return None

    # --- توزيع الأدوار ---
    def assign_roles(self):
        try:
            c=self._c()
            if len(self.players)<self.MIN_PLAYERS: return {"response":self._create_bubble("خطأ",[self._glass_box([{"type":"text","text":f"يجب {self.MIN_PLAYERS} لاعبين على الأقل","size":"md","color":c["text"],"align":"center"}],"16px","lg")],None),"game_over":False}
            num_players=len(self.players); num_mafia=max(1,num_players//4)
            roles=["mafia"]*num_mafia+["detective","doctor"]+["citizen"]*(num_players-len(["mafia"]*num_mafia+["detective","doctor"])); random.shuffle(roles)
            for uid,role in zip(list(self.players.keys()),roles):
                self.players[uid]["role"]=role
                if role=="mafia": self.mafia_list.append(uid)
                if role=="detective": self.detective=uid
                if role=="doctor": self.doctor=uid
            self.alive_players=list(self.players.keys()); self.phase="night"; self.day=1
            return {"response":self._create_bubble("بدأت اللعبة",[self._glass_box([{"type":"text","text":f"تم توزيع الأدوار\n{num_mafia} مافيا في اللعبة","size":"md","color":c["text"],"align":"center","wrap":True}],"16px","lg")],None),"game_over":False}
        except Exception as e: logger.error(f"Error in assign_roles: {e}"); return None

    # --- المرحلة الليلية ---
    def night_phase_action(self,user_id,cmd):
        try:
            if self.phase!="night": return None
            if user_id not in self.alive_players: return None
            # دور المافيا: يختار ضحية
            if self.players[user_id]["role"]=="mafia":
                target=cmd
                if target not in [self.players[uid]["name"] for uid in self.alive_players if uid!=user_id]:
                    return {"response":self._create_bubble("خطأ",[self._glass_box([{"type":"text","text":"لاعب غير صالح","size":"md","color":"#FF0000","align":"center"}],"16px","lg")],None),"game_over":False}
                self.night_actions.setdefault("mafia_targets",[]).append(target)
                return {"response":self._create_bubble("تم اختيار الضحية",[self._glass_box([{"type":"text","text":f"لقد اخترت {target}"}],"16px","lg")],None),"game_over":False}
            # المحقق: يسأل عن لاعب
            if self.players[user_id]["role"]=="detective":
                target=cmd
                role=None
                for uid,pdata in self.players.items():
                    if pdata["name"]==target: role=pdata["role"]; break
                if not role: return {"response":self._create_bubble("خطأ",[self._glass_box([{"type":"text","text":"لاعب غير موجود","size":"md","color":"#FF0000","align":"center"}],"16px","lg")],None),"game_over":False}
                return {"response":self._create_bubble("نتيجة التحقيق",[self._glass_box([{"type":"text","text":f"{target} هو {role}"}],"16px","lg")],None),"game_over":False}
            # الطبيب: يحمي لاعب
            if self.players[user_id]["role"]=="doctor":
                target=cmd
                if target not in [self.players[uid]["name"] for uid in self.alive_players]:
                    return {"response":self._create_bubble("خطأ",[self._glass_box([{"type":"text","text":"لاعب غير صالح","size":"md","color":"#FF0000","align":"center"}],"16px","lg")],None),"game_over":False}
                self.night_actions["doctor_target"]=target
                return {"response":self._create_bubble("تم اختيار الحماية",[self._glass_box([{"type":"text","text":f"لقد اخترت حماية {target}"}],"16px","lg")],None),"game_over":False}
            return None
        except Exception as e: logger.error(f"Error in night_phase_action: {e}"); return None

    # --- الانتقال إلى اليوم وحل الليلة ---
    def resolve_night(self):
        try:
            mafia_targets=self.night_actions.get("mafia_targets",[])
            doctor_target=self.night_actions.get("doctor_target")
            victim=None
            if mafia_targets:
                victim_name=random.choice(mafia_targets)
                if victim_name!=doctor_target:
                    for uid,pdata in self.players.items():
                        if pdata["name"]==victim_name:
                            self.players[uid]["alive"]=False
                            self.alive_players.remove(uid)
                            self.dead_players.append(uid)
                            victim=victim_name
                            break
            self.votes={}
            self.night_actions={}
            self.phase="voting"
            return victim
        except Exception as e: logger.error(f"Error in resolve_night: {e}"); return None

    # --- التصويت ---
    def cast_vote(self,user_id,target_name):
        try:
            if self.phase!="voting": return None
            if user_id not in self.alive_players: return None
            if target_name not in [self.players[uid]["name"] for uid in self.alive_players if uid!=user_id]: return {"response":self._create_bubble("خطأ",[self._glass_box([{"type":"text","text":"لاعب غير صالح للتصويت","size":"md","color":"#FF0000","align":"center"}],"16px","lg")],None),"game_over":False}
            self.votes[user_id]=target_name
            # تحقق من اكتمال الأصوات
            if len(self.votes)>=len(self.alive_players):
                counts={}
                for t in self.votes.values(): counts[t]=counts.get(t,0)+1
                max_votes=max(counts.values())
                voted_out=[name for name,count in counts.items() if count==max_votes]
                eliminated=random.choice(voted_out)
                for uid,pdata in self.players.items():
                    if pdata["name"]==eliminated:
                        self.players[uid]["alive"]=False
                        self.alive_players.remove(uid)
                        self.dead_players.append(uid)
                        break
                self.votes={}
                self.day+=1
                self.phase="night"
                winner=self.check_win()
                if winner: return self.end_game(winner)
                return {"response":self._create_bubble("اليوم انتهى",[self._glass_box([{"type":"text","text":f"{eliminated} خرج من اللعبة"}],"16px","lg")],None),"game_over":False}
            return {"response":self._create_bubble("تم التصويت",[self._glass_box([{"type":"text","text":f"تم تسجيل صوتك على {target_name}"}],"16px","lg")],None),"game_over":False}
        except Exception as e: logger.error(f"Error in cast_vote: {e}"); return None

    # --- التحقق من الفوز ---
    def check_win(self):
        mafia_alive=[uid for uid in self.mafia_list if self.players[uid]["alive"]]
        citizens_alive=[uid for uid in self.alive_players if uid not in self.mafia_list]
        if not mafia_alive: return "المواطنين"
        if len(mafia_alive)>=len(citizens_alive): return "المافيا"
        return None

    # --- شاشة النهاية ---
    def end_game(self,winner):
        try:
            c=self._c()
            contents=[]
            for uid,pdata in self.players.items():
                status=" ميت" if not pdata["alive"] else " حي"
                contents.append(self._glass_box([{"type":"text","text":f"{pdata['name']} - {pdata['role']} - {status}"}],"12px","sm"))
            bubble={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[{"type":"text","text":f"انتهت اللعبة! الفائز: {winner}","size":"xl","weight":"bold","align":"center","color":c["primary"]},{"type":"separator"},{"type":"box","layout":"vertical","contents":contents,"spacing":"sm"}],"paddingAll":"24px"}}
            self.phase="finished"
            self.game_active=False
            return FlexMessage(alt_text="نهاية اللعبة",contents=FlexContainer.from_dict(bubble),quickReply=self._qr())
        except Exception as e: logger.error(f"Error in end_game: {e}"); from linebot.v3.messaging import TextMessage; return TextMessage(text="حدث خطأ في إنهاء اللعبة.")
