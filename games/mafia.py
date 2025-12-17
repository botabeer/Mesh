import random
import logging
from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction
)
from config import Config

logger = logging.getLogger(__name__)


class MafiaGame:
    """لعبة المافيا - Turn Based مناسبة لـ LINE"""

    MIN_PLAYERS = 4
    MAX_PLAYERS = 12

    def __init__(self, db, theme="light"):
        self.db = db
        self.theme = theme
        self.game_name = "مافيا"
        self.reset()

    # ================= Core =================

    def reset(self):
        self.players = {}           # user_id -> {name, role, alive}
        self.alive = []
        self.dead = []
        self.phase = "registration" # registration | night | day | end
        self.day = 0
        self.votes = {}             # voter -> target

    def start(self, user_id):
        self.reset()
        return self._bubble(
            "لعبة المافيا",
            [
                "اضغط (انضم مافيا) للتسجيل",
                f"اللاعبون: 0 / {self.MAX_PLAYERS}",
                "الحد الأدنى: 4 لاعبين",
                "يجب إضافة البوت كصديق"
            ],
            buttons=[
                self._btn("انضم", "انضم مافيا", "primary"),
                self._btn("بدء اللعبة", "بدء مافيا", "secondary")
            ]
        )

    def check(self, text, user_id):
        cmd = Config.normalize(text)

        if cmd == "انضم مافيا":
            return self._join(user_id)

        if cmd == "بدء مافيا":
            return self._start_game()

        if cmd in ("الحاله", "الحالة"):
            return {"response": self._status(), "game_over": False}

        if self.phase == "day" and cmd.startswith("صوت"):
            return self._vote(user_id, cmd.replace("صوت", "").strip())

        return None

    # ================= Registration =================

    def _join(self, user_id):
        if self.phase != "registration":
            return self._err("التسجيل مغلق")

        if user_id in self.players:
            return self._err("أنت مسجل بالفعل")

        if len(self.players) >= self.MAX_PLAYERS:
            return self._err("اللعبة ممتلئة")

        user = self.db.get_user(user_id)
        name = user["name"] if user else f"لاعب{len(self.players) + 1}"

        self.players[user_id] = {"name": name, "role": None, "alive": True}

        return {
            "response": self._bubble(
                "تم التسجيل",
                [f"عدد اللاعبين: {len(self.players)}"]
            ),
            "game_over": False
        }

    # ================= Game Flow =================

    def _start_game(self):
        if self.phase != "registration":
            return self._err("اللعبة بدأت بالفعل")

        if len(self.players) < self.MIN_PLAYERS:
            return self._err("يجب 4 لاعبين على الأقل")

        self._assign_roles()
        self.alive = list(self.players.keys())
        self.day = 1
        self.phase = "day"

        return {
            "response": self._bubble(
                "بدأت اللعبة",
                [
                    "تم توزيع الأدوار",
                    "ابدأوا النقاش",
                    "استخدموا (صوت <اسم>)"
                ]
            ),
            "game_over": False
        }

    def _assign_roles(self):
        ids = list(self.players.keys())
        random.shuffle(ids)

        mafia_count = max(1, len(ids) // 4)
        roles = (
            ["mafia"] * mafia_count +
            ["detective", "doctor"] +
            ["citizen"] * (len(ids) - mafia_count - 2)
        )

        for uid, role in zip(ids, roles):
            self.players[uid]["role"] = role

    # ================= Voting =================

    def _vote(self, voter_id, target_name):
        if voter_id not in self.alive:
            return None

        target_id = next(
            (uid for uid, p in self.players.items()
             if p["name"] == target_name and p["alive"]),
            None
        )

        if not target_id:
            return self._err("الاسم غير صحيح")

        self.votes[voter_id] = target_id

        if len(self.votes) < len(self.alive):
            return {
                "response": self._bubble(
                    "تم التصويت",
                    [f"صوتك: {target_name}"]
                ),
                "game_over": False
            }

        return self._resolve_votes()

    def _resolve_votes(self):
        tally = {}
        for t in self.votes.values():
            tally[t] = tally.get(t, 0) + 1

        eliminated = max(tally, key=tally.get)
        self.players[eliminated]["alive"] = False
        self.alive.remove(eliminated)
        self.dead.append(eliminated)
        self.votes.clear()

        if self._check_end():
            return self._end_game()

        self.day += 1
        return {
            "response": self._bubble(
                "انتهى التصويت",
                [f"تم إقصاء {self.players[eliminated]['name']}"]
            ),
            "game_over": False
        }

    # ================= End =================

    def _check_end(self):
        mafia = [u for u in self.alive if self.players[u]["role"] == "mafia"]
        citizens = [u for u in self.alive if self.players[u]["role"] != "mafia"]
        return not mafia or len(mafia) >= len(citizens)

    def _end_game(self):
        mafia_alive = any(
            self.players[u]["role"] == "mafia" for u in self.alive
        )
        winner = "المافيا" if mafia_alive else "المواطنون"
        self.phase = "end"

        return {
            "response": self._bubble(
                "انتهت اللعبة",
                [f"الفائز: {winner}"]
            ),
            "game_over": True
        }

    # ================= UI =================

    def _status(self):
        alive = [self.players[u]["name"] for u in self.alive]
        dead = [self.players[u]["name"] for u in self.dead]

        return {
            "response": self._bubble(
                "حالة اللعبة",
                [
                    f"اليوم: {self.day}",
                    f"الأحياء: {', '.join(alive) or 'لا أحد'}",
                    f"الموتى: {', '.join(dead) or 'لا أحد'}"
                ],
                buttons=[
                    self._btn(p["name"], f"صوت {p['name']}", "secondary")
                    for u, p in self.players.items()
                    if p["alive"]
                ][:5]
            ),
            "game_over": False
        }

    def _err(self, msg):
        return {
            "response": self._bubble("خطأ", [msg]),
            "game_over": False
        }

    def _btn(self, label, text, style):
        c = Config.get_theme(self.theme)
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": style,
            "color": c["primary"] if style == "primary" else None,
            "margin": "sm"
        }

    def _bubble(self, title, texts, buttons=None):
        c = Config.get_theme(self.theme)

        body = [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "size": "xl",
                "align": "center",
                "color": c["primary"]
            },
            {"type": "separator", "margin": "lg"}
        ]

        for t in texts:
            body.append({
                "type": "text",
                "text": t,
                "size": "sm",
                "wrap": True,
                "margin": "md",
                "color": c["text"]
            })

        if buttons:
            body.append({"type": "separator", "margin": "lg"})
            body.extend(buttons)

        return FlexMessage(
            alt_text=title,
            contents=FlexContainer.from_dict({
                "type": "bubble",
                "size": "mega",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": body,
                    "backgroundColor": c["bg"],
                    "paddingAll": "20px"
                }
            }),
            quickReply=QuickReply(items=[
                QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
                QuickReplyItem(action=MessageAction(label="حالة", text="الحالة")),
                QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
            ])
        )
