import logging
import random
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta
from linebot.v3.messaging import TextMessage, FlexMessage, FlexContainer
from config import Config
from ui_builder import UIBuilder

logger = logging.getLogger(__name__)


# ==============================
# قاعدة الألعاب النصية
# ==============================
class TextGame:
    def __init__(self, game_name: str, items: List[str], theme: str):
        self.game_name = game_name
        self.theme = theme
        self.items = items.copy()
        random.shuffle(self.items)
        self.used_items = []
        self.current_index = 0
        self.game_active = False

    def start_game(self):
        self.game_active = True
        self.current_index = 0
        return self.get_question()

    def _pick_item(self):
        if self.current_index >= len(self.items):
            self.used_items.clear()
            random.shuffle(self.items)
            self.current_index = 0
        item = self.items[self.current_index]
        self.used_items.append(item)
        self.current_index += 1
        return item

    def get_question(self):
        item = self._pick_item()
        colors = Config.get_theme(self.theme)

        flex_dict = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "24px",
                "backgroundColor": colors["bg"],
                "contents": [
                    {"type": "text","text": self.game_name,"size": "xxl","weight": "bold","color": colors["primary"],"align": "center"},
                    {"type": "separator","margin": "lg","color": colors["border"]},
                    {"type": "box","layout": "vertical","margin": "lg","paddingAll": "20px","cornerRadius": "15px","backgroundColor": colors["card"],
                     "borderColor": colors["primary"],"borderWidth": "2px","contents":[
                         {"type":"text","text": item,"size":"lg","weight":"bold","color": colors["text"],"align":"center","wrap": True}
                     ]},
                    {"type":"separator","margin":"xl","color": colors["border"]},
                    {"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[
                        {"type":"button","style":"primary","height":"sm","color":colors["primary"],
                         "action":{"type":"message","label":"اعادة","text":self.game_name}},
                        {"type":"button","style":"secondary","height":"sm",
                         "action":{"type":"message","label":"بداية","text":"بداية"}}
                    ]}
                ]
            }
        }
        return FlexMessage(alt_text=f"{self.game_name}: {item[:50]}", contents=FlexContainer.from_dict(flex_dict))

    def check_answer(self, answer: str, user_id: str, username: str) -> Optional[Dict[str, Any]]:
        # الألعاب النصية لا تحتاج تحقق
        return None


# ==============================
# إدارة الألعاب
# ==============================
class GameManager:
    def __init__(self, db):
        self.db = db
        self.ui = UIBuilder()
        self.active_games: Dict[str, Any] = {}       # context_id -> game instance
        self.game_sessions: Dict[str, Dict] = {}     # context_id -> session info
        self.user_rounds: Dict[str, Dict] = {}       # context_id -> user rounds
        self.games = self._load_games()
        logger.info(f"Loaded {len(self.games)} games")

    # تحميل جميع الألعاب
    def _load_games(self) -> Dict[str, Any]:
        try:
            # الألعاب بالنقاط
            from games.iq_game import IqGame
            from games.guess_game import GuessGame
            from games.opposite_game import OppositeGame
            from games.scramble_word_game import ScrambleWordGame
            from games.math_game import MathGame
            from games.song_game import SongGame
            from games.word_color_game import WordColorGame
            from games.letters_words_game import LettersWordsGame
            from games.human_animal_plant_game import HumanAnimalPlantGame
            from games.chain_words_game import ChainWordsGame
            from games.fast_typing_game import FastTypingGame

            # الألعاب النصية
            from games.compatibility_game import CompatibilityGame
            from games.mafia_game import MafiaGame

            # نصوص جاهزة
            from text_games import QuestionGame, MentionGame, ChallengeGame, ConfessionGame

            return {
                "ذكاء": IqGame,
                "خمن": GuessGame,
                "ضد": OppositeGame,
                "ترتيب": ScrambleWordGame,
                "رياضيات": MathGame,
                "اغنيه": SongGame,
                "لون": WordColorGame,
                "تكوين": LettersWordsGame,
                "لعبة": HumanAnimalPlantGame,
                "سلسلة": ChainWordsGame,
                "اسرع": FastTypingGame,

                "سؤال": QuestionGame,
                "منشن": MentionGame,
                "تحدي": ChallengeGame,
                "اعتراف": ConfessionGame,
                "توافق": CompatibilityGame,
                "مافيا": MafiaGame,
            }
        except Exception as e:
            logger.error(f"Error loading games: {e}", exc_info=True)
            return {}

    # ==============================
    # إدارة التسجيل
    # ==============================
    def register_user(self, user_id: str, username: str) -> TextMessage:
        existing = self.db.get_user(user_id)
        if existing and existing.get("is_registered"):
            return TextMessage(text=f"أنت مسجل مسبقًا باسم: {existing['name']}")
        self.db.create_user(user_id, username)
        self.db.update_user(user_id, is_registered=1)
        return TextMessage(text=f"تم التسجيل بنجاح باسم: {username}")

    def change_name(self, user_id: str, new_name: str) -> TextMessage:
        self.db.update_user(user_id, name=new_name)
        return TextMessage(text=f"تم تغيير الاسم إلى: {new_name}")

    def unregister_user(self, user_id: str) -> TextMessage:
        user = self.db.get_user(user_id)
        if not user or not user.get("is_registered"):
            return TextMessage(text="أنت غير مسجل")
        self.db.update_user(user_id, is_registered=0)
        return TextMessage(text=f"تم الانسحاب. نقاطك محفوظة: {user['points']}")

    # ==============================
    # بدء اللعبة
    # ==============================
    def start_game(self, context_id: str, game_name: str, user_id: str, username: str,
                   is_registered: bool, theme: str, source_type: str) -> dict:

        if game_name not in self.games:
            return {"messages":[TextMessage(text="اللعبة غير موجودة")], "points":0}

        is_point_game = game_name in Config.POINT_GAMES
        is_fun_game = game_name in Config.FUN_GAMES

        # تحقق من التسجيل للألعاب بالنقاط
        if is_point_game and not is_registered:
            return {"messages":[TextMessage(text="يجب التسجيل اولا\nاكتب: تسجيل")], "points":0}

        # تحقق من الألعاب الجماعية
        if is_fun_game:
            cfg = Config.FUN_GAMES.get(game_name, {})
            if cfg.get("group_only") and source_type not in ("group","room"):
                return {"messages":[TextMessage(text="هذه اللعبة للمجموعات فقط")], "points":0}

        # إنشاء نسخة اللعبة
        GameClass = self.games[game_name]
        if isinstance(GameClass, type):
            game_instance = GameClass(None)  # مرر None أو line_bot_api
        else:
            game_instance = GameClass  # نصية مدمجة

        # دعم الثيم
        if hasattr(game_instance,"set_theme"):
            game_instance.set_theme(theme)
        if hasattr(game_instance,"set_database"):
            game_instance.set_database(self.db)

        # حفظ النشاط
        self.active_games[context_id] = game_instance

        # إنشاء جلسة للنقاط
        if is_point_game:
            session_id = self.db.create_session(user_id, game_name)
            self.game_sessions[context_id] = {"session_id":session_id,"user_id":user_id,"game_name":game_name}
            self.user_rounds[context_id] = {"current_round":1,"scores":{},"max_rounds":5,"first_correct":None}

        # بدء اللعبة
        msg = game_instance.start_game()
        return {"messages":[msg],"points":0}

    # ==============================
    # معالجة الرسائل
    # ==============================
    def process_message(self, context_id: str, user_id: str, username: str,
                        text: str, is_registered: bool, theme: str,
                        source_type: str) -> Optional[dict]:

        norm = Config.normalize(text)

        # أوامر التسجيل
        if norm == "تسجيل":
            return {"messages":[self.register_user(user_id, username)], "points":0}
        if norm.startswith("تغيير "):
            new_name = text.split(" ",1)[1].strip()
            return {"messages":[self.change_name(user_id,new_name)], "points":0}
        if norm == "انسحب":
            return {"messages":[self.unregister_user(user_id)], "points":0}

        # بدء اللعبة إذا النص اسم لعبة
        if norm in self.games:
            return self.start_game(context_id, norm, user_id, username, is_registered, theme, source_type)

        # إذا لا توجد لعبة نشطة
        if context_id not in self.active_games:
            return None

        game = self.active_games[context_id]
        rounds = self.user_rounds.get(context_id)

        try:
            result = game.check_answer(text, user_id, username)
            if not result:
                return None

            pts = result.get("points",0)
            msgs = []
            if result.get("message"):
                msgs.append(TextMessage(text=result["message"]))
            if result.get("response"):
                msgs.append(result["response"])

            # ======================
            # إدارة الجولات والخمس جولات
            # ======================
            if rounds:
                if user_id not in rounds["scores"]:
                    rounds["scores"][user_id] = 0
                if rounds["first_correct"] is None and pts>0:
                    rounds["first_correct"] = user_id
                    rounds["scores"][user_id] += pts
                    rounds["current_round"] +=1
                    # الجولة التالية
                    if rounds["current_round"] > rounds["max_rounds"]:
                        winner = max(rounds["scores"], key=lambda k: rounds["scores"][k])
                        self.active_games.pop(context_id,None)
                        self.game_sessions.pop(context_id,None)
                        self.user_rounds.pop(context_id,None)
                        msgs.append(TextMessage(text=f"انتهت اللعبة! الفائز: {winner} بنقاط {rounds['scores'][winner]}"))
                        if is_registered:
                            self.db.record_game_stat(user_id, game.game_name, pts, True)
                    else:
                        msgs.append(game.get_question())
                    rounds["first_correct"]=None

            return {"messages":msgs,"points":pts}

        except Exception as e:
            logger.error(f"Error processing answer {game.game_name}: {e}", exc_info=True)
            return None

    # ==============================
    # إيقاف اللعبة
    # ==============================
    def stop_game(self, context_id: str) -> Optional[str]:
        game = self.active_games.pop(context_id,None)
        self.game_sessions.pop(context_id,None)
        self.user_rounds.pop(context_id,None)
        if game:
            return getattr(game,"game_name","اللعبة")
        return None
