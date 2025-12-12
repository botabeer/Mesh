import logging
import random
from typing import Dict, Any, Optional, List
from pathlib import Path
from linebot.v3.messaging import TextMessage, FlexMessage, FlexContainer
from config import Config

# ألعاب Flex المستقلة
from games.mafia_game import MafiaGame
from games.compatibility_game import CompatibilityGame

logger = logging.getLogger(__name__)

class GameManager:
    """إدارة جميع الألعاب النصية والفلكسية مع تسجيل ونقاط وجولات 5 أسئلة."""

    TEXT_GAME_FILES = {
        "سؤال": "questions.txt",
        "منشن": "mentions.txt",
        "تحدي": "challenges.txt",
        "اعتراف": "confessions.txt",
        "موقف": "situations.txt",
        "اقتباس": "quotes.txt",
        "شخصية": "personality.txt",
    }

    TEXT_GAMES_DATA: Dict[str, List[str]] = {}

    def __init__(self, db):
        self.db = db
        self.active_games: Dict[str, Any] = {}  # context_id -> game instance
        self.game_sessions: Dict[str, dict] = {}  # context_id -> session info
        self._load_text_games()
        self.games = self._load_games()
        logger.info(f"Loaded {len(self.games)} games")

    # تحميل محتوى الألعاب النصية من الملفات
    def _load_text_games(self):
        base_path = Path(__file__).parent
        for name, filename in self.TEXT_GAME_FILES.items():
            file_path = base_path / filename
            if not file_path.exists():
                file_path = Path("games") / filename
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]
                    self.TEXT_GAMES_DATA[name] = lines
            except Exception as e:
                logger.error(f"Error loading {filename}: {e}")
                self.TEXT_GAMES_DATA[name] = ["لا يوجد محتوى"]

    # تحميل كل الألعاب
    def _load_games(self) -> Dict[str, Any]:
        return {
            "مافيا": MafiaGame,
            "توافق": CompatibilityGame,
            "سؤال": TextGame,
            "منشن": TextGame,
            "تحدي": TextGame,
            "اعتراف": TextGame,
            "موقف": TextGame,
            "اقتباس": TextGame,
            "شخصية": TextGame,
        }

    # بدء لعبة
    def start_game(self, context_id: str, game_name: str, user_id: str,
                   username: str, is_registered: bool, theme: str,
                   source_type: str) -> dict:
        if game_name not in self.games:
            return {"messages":[TextMessage(text="اللعبة غير موجودة")], "points":0}

        is_point_game = game_name in Config.POINT_GAMES
        is_fun_game = game_name in Config.FUN_GAMES

        if is_point_game and not is_registered:
            return {"messages":[TextMessage(text="يجب التسجيل أولا\nاكتب: تسجيل")], "points":0}

        if is_fun_game:
            game_cfg = Config.FUN_GAMES.get(game_name, {})
            if game_cfg.get("group_only") and source_type not in ("group","room"):
                return {"messages":[TextMessage(text="هذه اللعبة للمجموعات فقط")], "points":0}

        try:
            if game_name in ["مافيا", "توافق"]:
                GameClass = self.games[game_name]
                game = GameClass(None)
            else:
                GameClass = self.games[game_name]
                game = GameClass(game_name, self.TEXT_GAMES_DATA[game_name])

            self.active_games[context_id] = game

            if is_point_game:
                session_id = self.db.create_session(user_id, game_name)
                self.game_sessions[context_id] = {
                    "session_id": session_id,
                    "user_id": user_id,
                    "game_name": game_name,
                    "round": 0
                }

            question_msg = game.start_game()
            return {"messages":[question_msg], "points":0}

        except Exception as e:
            logger.error(f"Error starting game {game_name}: {e}", exc_info=True)
            return {"messages":[TextMessage(text="خطأ في بدء اللعبة")], "points":0}

    # معالجة الرسائل
    def process_message(self, context_id: str, user_id: str, username: str,
                        text: str, is_registered: bool, theme: str,
                        source_type: str) -> Optional[dict]:
        norm = Config.normalize(text)

        # دعم أوامر التسجيل اليدوي
        if norm == "تسجيل":
            self.db.create_user(user_id, username)
            self.db.update_user(user_id, is_registered=1)
            return {"messages":[TextMessage(text="تم التسجيل بنجاح!")], "points":0}

        if norm.startswith("تغيير "):
            new_name = text.split(" ",1)[1].strip()
            self.db.update_user(user_id, name=new_name)
            return {"messages":[TextMessage(text=f"تم تغيير الاسم إلى: {new_name}")], "points":0}

        if norm == "انسحب":
            self.db.update_user(user_id, is_registered=0)
            return {"messages":[TextMessage(text="تم الانسحاب، لن يحسب البوت إجاباتك")], "points":0}

        # بدء اللعبة مباشرة إذا النص اسم لعبة
        if norm in self.games:
            return self.start_game(context_id, norm, user_id, username, is_registered, theme, source_type)

        if context_id not in self.active_games:
            return None

        game = self.active_games[context_id]
        try:
            result = game.check_answer(user_answer=text, user_id=user_id, display_name=username)
            if not result:
                return None

            msgs = []
            pts = result.get("points",0)

            if result.get("message"):
                msgs.append(TextMessage(text=result["message"]))
            if result.get("response"):
                msgs.append(result["response"])

            if result.get("game_over"):
                sess = self.game_sessions.pop(context_id,None)
                self.active_games.pop(context_id,None)

                if sess:
                    self.db.complete_session(sess["session_id"], pts)
                    if pts>0 and is_registered:
                        self.db.record_game_stat(user_id, sess["game_name"], pts, True)

                logger.info(f"Game finished: {game.__class__.__name__}, User={user_id}, Points={pts}")

            return {"messages":msgs, "points":pts}

        except Exception as e:
            logger.error(f"Error processing answer in {game.__class__.__name__}: {e}", exc_info=True)
            return None

# ======= فئة الألعاب النصية =======
class TextGame:
    """قاعدة الألعاب النصية من الملفات"""

    def __init__(self, game_name:str, items:List[str]):
        self.game_name = game_name
        self.items = items.copy()
        random.shuffle(self.items)
        self.used_items: List[str] = []
        self.round = 0
        self.max_rounds = 5
        self.game_active = False
        self.current_item = None

    def start_game(self):
        self.game_active = True
        return self.get_question()

    def _pick_item(self) -> str:
        available = [x for x in self.items if x not in self.used_items]
        if not available:
            self.used_items.clear()
            available = self.items.copy()
        item = available[0]  # نأخذ من البداية لتجنب تكرار العشوائي
        self.used_items.append(item)
        self.current_item = item
        self.round +=1
        return item

    def get_question(self):
        item = self._pick_item()
        colors = Config.get_theme(Config.DEFAULT_THEME)
        flex_dict = {
            "type":"bubble",
            "size":"mega",
            "body":{
                "type":"box",
                "layout":"vertical",
                "paddingAll":"24px",
                "backgroundColor": colors["bg"],
                "contents":[
                    {"type":"text","text":self.game_name,"size":"xxl","weight":"bold","color":colors["primary"],"align":"center"},
                    {"type":"separator","margin":"lg","color":colors["border"]},
                    {"type":"box","layout":"vertical","margin":"lg","paddingAll":"20px","cornerRadius":"15px","backgroundColor":colors["card"],"borderColor":colors["primary"],"borderWidth":"2px","contents":[
                        {"type":"text","text":item,"size":"lg","weight":"bold","color":colors["text"],"align":"center","wrap":True}
                    ]},
                    {"type":"separator","margin":"xl","color":colors["border"]},
                    {"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[
                        {"type":"button","style":"primary","height":"sm","color":colors["primary"],"action":{"type":"message","label":"اعادة","text":self.game_name}},
                        {"type":"button","style":"secondary","height":"sm","action":{"type":"message","label":"بداية","text":"بداية"}}
                    ]}
                ]
            }
        }
        return FlexMessage(alt_text=f"{self.game_name}: {item[:50]}", contents=FlexContainer.from_dict(flex_dict))

    def check_answer(self, user_answer:str, user_id:str, display_name:str) -> Optional[Dict[str,Any]]:
        """للألعاب النصية نأخذ أول إجابة صحيحة أو نمر للعنصر التالي"""
        # الألعاب النصية ليست بحاجة لإجابة صحيحة محددة
        if self.round >= self.max_rounds:
            return {"game_over":True, "message":"انتهت اللعبة"}
        return {"points":0, "message":f"تم تسجيل إجابتك: {user_answer}", "game_over":False}
