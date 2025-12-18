import random
import logging
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
from config import Config

logger = logging.getLogger(__name__)

class MafiaGame:
    MIN_PLAYERS = 4
    MAX_PLAYERS = 12

    def __init__(self, db, theme="light"):
        self.db = db
        self.theme = theme
        self.game_name = "مافيا"
        self.players = {}  # {user_id: {"name":..., "role":..., "alive": True}}
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

    # -------------------- ثيم وألوان --------------------
    def _c(self):
        return Config.get_theme(self.theme)

    def _qr(self):
        items = ["شرح", "انضم", "بدء اللعبة", "الحالة"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items])

    def _separator(self, margin="md"):
        return {"type": "separator", "margin": margin}

    def _glass_box(self, contents, padding="16px", margin="none"):
        c = self._c()
        bg_color = c["card_secondary"] if self.theme == "light" else "#1A202C"
        return {"type": "box","layout":"vertical","contents":contents,"backgroundColor":bg_color,
                "cornerRadius":"16px","paddingAll":padding,"spacing":"sm","margin":margin}

    def _create_bubble(self, title, contents, buttons=None):
        c = self._c()
        body_contents = [{"type":"text","text":title,"size":"xl","weight":"bold","color":c["primary"],"align":"center"}, self._separator("lg")]
        body_contents.extend(contents)
        if buttons:
            body_contents.append(self._separator("lg"))
            body_contents.extend(buttons)
        bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":body_contents,"backgroundColor":c["card"],"paddingAll":"24px"}}
        return FlexMessage(alt_text=title, contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    # -------------------- تسجيل اللاعبين --------------------
    def registration_screen(self):
        c = self._c()
        contents = [self._glass_box([
            {"type":"text","text":f"اللاعبون المسجلون: {len(self.players)}","size":"md","color":c["text"],"weight":"bold","align":"center"},
            {"type":"text","text":f"الحد الأدنى: {self.MIN_PLAYERS} لاعبين","size":"xs","color":c["text_secondary"],"align":"center","margin":"sm"},
            {"type":"text","text":f"الحد الأقصى: {self.MAX_PLAYERS} لاعبين","size":"xs","color":c["text_tertiary"],"align":"center","margin":"xs"}
        ], "20px", "lg")]
        if self.players:
            player_names = [p["name"] for p in self.players.values()]
            contents.append(self._glass_box([
                {"type":"text","text":"اللاعبون:","size":"sm","color":c["text_secondary"],"weight":"bold"},
                {"type":"text","text":" - " + "\n - ".join(player_names),"size":"xs","color":c["text"],"wrap":True,"margin":"sm"}
            ], "12px", "md"))
        buttons = [{"type":"box","layout":"horizontal","contents":[
            {"type":"button","action":{"type":"message","label":"انضم","text":"انضم مافيا"},"style":"primary","color":c["button_primary"],"height":"sm","flex":1},
            {"type":"button","action":{"type":"message","label":"بدء اللعبة","text":"بدء مافيا"},"style":"primary","color":c["button_primary"],"height":"sm","flex":1}
        ],"spacing":"sm","margin":"md"}]
        return self._create_bubble("تسجيل المافيا", contents, buttons)

    # -------------------- شرح المبتدئين --------------------
    def instructions_screen(self):
        c = self._c()
        contents = [self._glass_box([
            {"type":"text","text":"طريقة اللعب للمبتدئين","size":"md","weight":"bold","color":c["text"]},
            {"type":"text","text":(
                "• في القروب: النقاش والتصويت.\n"
                "• في الخاص مع البوت:\n"
                "   - البوت يخبرك بدورك.\n"
                "   - المافيا: اختار ضحية.\n"
                "   - المحقق: اسأل عن لاعب لمعرفة دوره.\n"
                "   - الطبيب: احمي لاعب.\n"
                "   - المواطن: صوّت وناقش.\n"
                "ملاحظة: يجب إضافة البوت كصديق ليصلك دورك بالخاص."
            ), "size":"xs","color":c["text_secondary"],"wrap":True,"margin":"sm"}
        ], "16px", "lg")]
        buttons = [{"type":"button","action":{"type":"message","label":"العودة للتسجيل","text":"تسجيل مافيا"},"style":"primary","color":c["button_primary"],"height":"sm"}]
        return self._create_bubble("شرح المافيا", contents, buttons)

    # -------------------- بدء اللعبة --------------------
    def start(self, user_id):
        try:
            self.phase = "registration"
            self.game_active = True
            self.players = {}
            self.alive_players = []
            self.dead_players = []
            self.day = 0
            self.votes = {}
            self.night_actions = {}
            self.mafia_list = []
            self.detective = None
            self.doctor = None
            return self.registration_screen()
        except Exception as e:
            logger.error(f"Error in start: {e}")
            return TextMessage(text="حدث خطأ في بدء لعبة المافيا. حاول مرة أخرى.")

    # -------------------- إضافة لاعب --------------------
    def add_player(self, user_id):
        if self.phase != "registration" or user_id in self.players or len(self.players) >= self.MAX_PLAYERS:
            return None
        user = self.db.get_user(user_id)
        name = user["name"] if user else f"لاعب{len(self.players)+1}"
        self.players[user_id] = {"name": name, "role": None, "alive": True}
        return self.registration_screen()

    # -------------------- توزيع الأدوار --------------------
    def assign_roles(self):
        if len(self.players) < self.MIN_PLAYERS: return None
        num_players = len(self.players)
        num_mafia = max(1, num_players // 4)
        roles = ["mafia"] * num_mafia + ["detective", "doctor"]
        roles += ["citizen"] * (num_players - len(roles))
        random.shuffle(roles)
        player_ids = list(self.players.keys())
        for uid, role in zip(player_ids, roles):
            self.players[uid]["role"] = role
            if role == "mafia": self.mafia_list.append(uid)
            elif role == "detective": self.detective = uid
            elif role == "doctor": self.doctor = uid
        self.alive_players = player_ids.copy()
        self.phase = "night"
        self.day = 1
        return self._create_bubble("بدأت اللعبة", [self._glass_box([{"type":"text","text":f"تم توزيع الأدوار\n{num_mafia} مافيا في اللعبة","size":"md","color":self._c()["text"],"align":"center","wrap":True}], "16px", "lg")], None)

    # -------------------- إرسال الدور الخاص لكل لاعب --------------------
    def send_role_private(self, send_func):
        role_names = {"mafia":"مافيا","detective":"محقق","doctor":"طبيب","citizen":"مواطن"}
        for uid, player in self.players.items():
            role = player["role"]
            text = f"دورك: {role_names.get(role, role)}"
            if role=="mafia":
                mafia_names=[self.players[mid]["name"] for mid in self.mafia_list if mid!=uid]
                text+=f"\nأسماء المافيا الآخرين: {', '.join(mafia_names)}"
            elif role=="detective":
                text+="\nيمكنك السؤال عن لاعب لمعرفة دوره."
            elif role=="doctor":
                text+="\nيمكنك اختيار لاعب للحماية."
            else:
                text+="\nشارك في النقاش وصوت في القروب."
            bubble=self._create_bubble("دورك في المافيا",[self._glass_box([{"type":"text","text":text,"size":"md","color":self._c()["text"],"wrap":True}],"16px","lg")],None)
            send_func(uid,bubble)

    # -------------------- مرحلة الليل --------------------
    def night_phase(self, send_func):
        if not self.alive_players: return None
        for uid in self.alive_players:
            player=self.players[uid]
            role=player["role"]
            c=self._c()
            if role=="mafia":
                targets=[self.players[pid]["name"] for pid in self.alive_players if pid not in self.mafia_list]
                buttons=[{"type":"button","action":{"type":"message","label":name,"text":f"قتل {name}"},"style":"primary","color":c["button_primary"],"height":"sm"} for name in targets]
                bubble=self._create_bubble("دور المافيا",[self._glass_box([{"type":"text","text":"اختر ضحية بالليل:","size":"md","color":c["text"],"weight":"bold"}],"16px","lg")],None)
                send_func(uid,bubble)
            elif role=="doctor":
                targets=[self.players[pid]["name"] for pid in self.alive_players]
                buttons=[{"type":"button","action":{"type":"message","label":name,"text":f"حماية {name}"},"style":"primary","color":c["button_primary"],"height":"sm"} for name in targets]
                bubble=self._create_bubble("دور الطبيب",[self._glass_box([{"type":"text","text":"اختر لاعب للحماية:","size":"md","color":c["text"],"weight":"bold"}],"16px","lg")],None)
                send_func(uid,bubble)
            elif role=="detective":
                targets=[self.players[pid]["name"] for pid in self.alive_players if pid!=uid]
                buttons=[{"type":"button","action":{"type":"message","label":name,"text":f"تحقق {name}"},"style":"primary","color":c["button_primary"],"height":"sm"} for name in targets]
                bubble=self._create_bubble("دور المحقق",[self._glass_box([{"type":"text","text":"اختر لاعب للتحقق منه:","size":"md","color":c["text"],"weight":"bold"}],"16px","lg")],None)
                send_func(uid,bubble)
        self.phase="night_waiting"

    # -------------------- معالجة أفعال الليل --------------------
    def process_night_actions(self):
        mafia_target=self.night_actions.get("mafia")
        doctor_target=self.night_actions.get("doctor")
        detective_target=self.night_actions.get("detective")
        detective_result=None
        if mafia_target and mafia_target!=doctor_target:
            self.alive_players.remove(mafia_target)
            self.dead_players.append(mafia_target)
            self.players[mafia_target]["alive"]=False
        if detective_target:
            role=self.players[detective_target]["role"]
            detective_result="مافيا" if role=="mafia" else "غير مافيا"
        self.night_actions={}
        self.phase="day"
        self.day+=1
        return detective_result

    # -------------------- ملخص الليل --------------------
    def night_summary_bubble(self, detective_result=None):
        c=self._c()
        contents=[{"type":"text","text":"انتهت مرحلة الليل","size":"md","weight":"bold","color":c["text"],"align":"center"}]
        if detective_result:
            contents.append({"type":"text","text":f"نتيجة التحقيق: {detective_result}","size":"sm","color":c["text_secondary"],"align":"center"})
        return self._create_bubble("ملخص الليل",[self._glass_box(contents,"16px","lg")],None)

    # -------------------- التصويت النهاري --------------------
    def voting_screen(self, user_id):
        if user_id not in self.alive_players: return None
        c=self._c()
        player_buttons=[]
        for uid in self.alive_players:
            if uid==user_id: continue
            player_name=self.players[uid]["name"]
            player_buttons.append({"type":"button","action":{"type":"message","label":player_name,"text":f"صوت {player_name}"},"style":"primary","color":c["button_primary"],"height":"sm"})
        contents=[self._glass_box([{"type":"text","text":"مرحلة التصويت: اختر لاعب للتصويت","size":"md","weight":"bold","color":c["text"],"align":"center"}],"16px","lg"),
                  {"type":"box","layout":"vertical","contents":player_buttons,"spacing":"sm","margin":"md"}]
        return self._create_bubble("التصويت",contents,None)

    # -------------------- تسجيل التصويت --------------------
    def cast_vote(self,user_id,target_name):
        if user_id not in self.alive_players: return None
        target_id=None
        for uid in self.alive_players:
            if Config.normalize(self.players[uid]["name"])==Config.normalize(target_name):
                target_id=uid
                break
        if not target_id: return None
        self.votes[user_id]=target_id
        if len(self.votes)>=len(self.alive_players):
            return self.process_votes()
        c=self._c()
        return self._create_bubble("تم التصويت",[self._glass_box([{"type":"text","text":f"صوتك تم احتسابه\nعدد الأصوات: {len(self.votes)}/{len(self.alive_players)}","size":"md","color":c["text"],"align":"center","wrap":True}],"16px","lg")],None)

    # -------------------- التحقق من الفائز --------------------
    def check_winner(self):
        mafia_alive=sum(1 for uid in self.alive_players if self.players[uid]["role"]=="mafia")
        citizens_alive=len(self.alive_players)-mafia_alive
        if mafia_alive==0: return "citizens"
        elif mafia_alive>=citizens_alive: return "mafia"
        return None

    # -------------------- نافذة النهاية --------------------
    def game_over_screen(self,winner):
        c=self._c()
        winner_text="فاز المواطنون" if winner=="citizens" else "فازت المافيا"
        winner_color="#00AA00" if winner=="citizens" else "#FF0000"
        player_summaries=[]
        role_names={"mafia":"مافيا","detective":"محقق","doctor":"طبيب","citizen":"مواطن"}
        for uid,player in self.players.items():
            role=role_names.get(player["role"],player["role"])
            status="حي" if player["alive"] else "مقتول"
            player_summaries.append({"type":"text","text":f"{player['name']} - {role} - {status}","size":"xs","color":c["text_secondary"],"wrap":True})
        contents=[{"type":"text","text":winner_text,"size":"xxl","weight":"bold","color":winner_color,"align":"center"},
                  self._glass_box([{"type":"text","text":f"عدد الأيام: {self.day}\nعدد اللاعبين: {len(self.players)}","size":"sm","color":c["text"],"align":"center","margin":"sm"}],"16px","lg"),
                  self._glass_box([{"type":"text","text":"ملخص اللاعبين:","size":"md","weight":"bold","color":c["text"],"align":"center"}]+player_summaries,"16px","lg")]
        buttons=[{"type":"button","action":{"type":"message","label":"لعب مرة أخرى","text":"مافيا"},"style":"primary","color":c["button_primary"],"height":"sm","margin":"md"}]
        return self._create_bubble("انتهت اللعبة",contents,buttons)
