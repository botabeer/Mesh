"""
Bot Mesh v6.0 - Games Engine
Simple, Clean & Group-Friendly
"""

import random
from datetime import datetime

# ============================================================================
# محرك اللعبة الأساسي
# ============================================================================

class Game:
    """محرك اللعبة الأساسي - يدعم الفردي والجماعي"""
    
    def __init__(self, game_type, mode="فردي", max_rounds=5):
        self.game_type = game_type
        self.mode = mode  # "فردي" أو "جماعي"
        self.max_rounds = max_rounds
        
        # حالة اللعبة
        self.active = True
        self.current_round = 0
        self.current_question = None
        self.current_answer = None
        
        # النقاط (للفردي والجماعي)
        self.scores = {}  # {user_id: {"name": str, "points": int}}
        self.answered_this_round = set()  # من أجاب في هذه الجولة
        
        # التوقيت
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    def start(self):
        """بدء اللعبة"""
        self.current_round = 1
        self.generate_question()
        return self.get_question_text()
    
    def generate_question(self):
        """توليد سؤال جديد - يجب تطبيقها في كل لعبة"""
        raise NotImplementedError
    
    def check_answer(self, user_id, username, answer):
        """فحص الإجابة"""
        self.last_activity = datetime.now()
        
        # في الوضع الفردي: مستخدم واحد فقط
        if self.mode == "فردي" and self.scores and user_id not in self.scores:
            return {"valid": False, "message": "هذه لعبة فردية لشخص آخر!"}
        
        # إذا أجاب في هذه الجولة (جماعي فقط)
        if self.mode == "جماعي" and user_id in self.answered_this_round:
            return {"valid": False, "message": "لقد أجبت في هذه الجولة!"}
        
        # تسجيل اللاعب إذا لم يكن موجوداً
        if user_id not in self.scores:
            self.scores[user_id] = {"name": username, "points": 0}
        
        # فحص الإجابة
        is_correct = self._check_answer_logic(answer)
        
        if is_correct:
            points = 10
            self.scores[user_id]["points"] += points
            self.answered_this_round.add(user_id)
            
            # الانتقال للجولة التالية
            self.current_round += 1
            
            if self.current_round > self.max_rounds:
                # انتهت اللعبة
                self.active = False
                return {
                    "valid": True,
                    "correct": True,
                    "points": points,
                    "game_over": True,
                    "results": self.get_results()
                }
            else:
                # جولة جديدة
                self.answered_this_round.clear()
                self.generate_question()
                return {
                    "valid": True,
                    "correct": True,
                    "points": points,
                    "next_question": self.get_question_text()
                }
        else:
            return {
                "valid": True,
                "correct": False,
                "message": "❌ إجابة خاطئة، حاول مرة أخرى!"
            }
    
    def _check_answer_logic(self, answer):
        """منطق فحص الإجابة - يجب تطبيقها في كل لعبة"""
        raise NotImplementedError
    
    def get_question_text(self):
        """الحصول على نص السؤال"""
        return {
            "game": self.game_type,
            "question": self.current_question,
            "round": self.current_round,
            "total_rounds": self.max_rounds,
            "mode": self.mode
        }
    
    def get_results(self):
        """الحصول على النتائج النهائية"""
        sorted_scores = sorted(
            self.scores.items(),
            key=lambda x: x[1]["points"],
            reverse=True
        )
        
        players = [(data["name"], data["points"]) for _, data in sorted_scores]
        
        if players:
            winner_name, winner_points = players[0]
        else:
            winner_name, winner_points = "لا أحد", 0
        
        return {
            "winner_name": winner_name,
            "winner_points": winner_points,
            "all_players": players,
            "mode": self.mode
        }
    
    def get_hint(self):
        """تلميح"""
        if isinstance(self.current_answer, list):
            ans = self.current_answer[0]
        else:
            ans = str(self.current_answer)
        
        if len(ans) > 2:
            return f"💡 الإجابة تبدأ بـ: {ans[0]}\n📏 الطول: {len(ans)} حرف"
        return f"💡 الإجابة تبدأ بـ: {ans[0]}"
    
    def reveal_answer(self):
        """كشف الإجابة والانتقال للسؤال التالي"""
        if isinstance(self.current_answer, list):
            answer_text = " أو ".join(self.current_answer)
        else:
            answer_text = str(self.current_answer)
        
        # الانتقال للجولة التالية
        self.current_round += 1
        self.answered_this_round.clear()
        
        if self.current_round > self.max_rounds:
            self.active = False
            return {
                "answer": answer_text,
                "game_over": True,
                "results": self.get_results()
            }
        else:
            self.generate_question()
            return {
                "answer": answer_text,
                "next_question": self.get_question_text()
            }
    
    def is_expired(self, max_minutes=30):
        """هل انتهت صلاحية اللعبة؟"""
        elapsed = (datetime.now() - self.last_activity).total_seconds() / 60
        return elapsed > max_minutes


# ============================================================================
# الألعاب المتاحة
# ============================================================================

class IQGame(Game):
    """🧠 لعبة الذكاء"""
    
    def __init__(self, mode="فردي"):
        super().__init__("ذكاء", mode)
        self.questions = [
            {"q": "ما يمشي بلا أرجل ويبكي بلا عيون؟", "a": ["السحاب", "الغيم", "سحاب", "غيم"]},
            {"q": "له رأس ولا عين له؟", "a": ["الدبوس", "دبوس", "المسمار", "مسمار"]},
            {"q": "كلما زاد نقص؟", "a": ["العمر", "عمر", "الوقت", "وقت"]},
            {"q": "يكتب ولا يقرأ؟", "a": ["القلم", "قلم"]},
            {"q": "له أسنان ولا يعض؟", "a": ["المشط", "مشط"]},
            {"q": "في الماء ولكن الماء يميته؟", "a": ["الملح", "ملح"]},
            {"q": "يتكلم بكل اللغات؟", "a": ["الصدى", "صدى"]},
            {"q": "يؤخذ منك قبل أن تعطيه؟", "a": ["الصورة", "صورة"]},
        ]
        random.shuffle(self.questions)
    
    def generate_question(self):
        q_data = self.questions[(self.current_round - 1) % len(self.questions)]
        self.current_question = q_data["q"]
        self.current_answer = q_data["a"]
    
    def _check_answer_logic(self, answer):
        answer = answer.strip().lower()
        for correct in self.current_answer:
            if answer == correct.lower():
                return True
        return False


class MathGame(Game):
    """🔢 لعبة الرياضيات"""
    
    def __init__(self, mode="فردي"):
        super().__init__("رياضيات", mode)
    
    def generate_question(self):
        # مستوى الصعوبة حسب الجولة
        level = min(self.current_round, 5)
        max_num = 10 * level
        
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        op = random.choice(['+', '-', '×'])
        
        if op == '+':
            self.current_question = f"{a} + {b} = ؟"
            self.current_answer = str(a + b)
        elif op == '-':
            if a < b:
                a, b = b, a
            self.current_question = f"{a} - {b} = ؟"
            self.current_answer = str(a - b)
        else:  # ×
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            self.current_question = f"{a} × {b} = ؟"
            self.current_answer = str(a * b)
    
    def _check_answer_logic(self, answer):
        try:
            return int(answer.strip()) == int(self.current_answer)
        except:
            return False


class ColorGame(Game):
    """🎨 لعبة الألوان (Stroop Effect)"""
    
    def __init__(self, mode="فردي"):
        super().__init__("ألوان", mode)
        self.colors = {
            "أحمر": "#E53E3E",
            "أزرق": "#3182CE",
            "أخضر": "#38A169",
            "أصفر": "#D69E2E",
            "برتقالي": "#DD6B20",
            "بنفسجي": "#805AD5"
        }
        self.color_names = list(self.colors.keys())
    
    def generate_question(self):
        word = random.choice(self.color_names)
        # 70% مختلف، 30% نفس اللون
        if random.random() < 0.7:
            color = random.choice([c for c in self.color_names if c != word])
        else:
            color = word
        
        self.current_question = f"ما لون هذه الكلمة؟\n[{word} بلون {color}]"
        self.current_answer = [color]
    
    def _check_answer_logic(self, answer):
        answer = answer.strip().lower()
        return answer == self.current_answer[0].lower()


class SpeedGame(Game):
    """⚡ لعبة السرعة"""
    
    def __init__(self, mode="فردي"):
        super().__init__("سرعة", mode)
        self.phrases = [
            "السرعة والدقة",
            "التركيز مهم",
            "اكتب بسرعة",
            "الوقت من ذهب",
            "التحدي يبدأ الآن",
            "كن الأفضل دائماً",
            "النجاح يحتاج صبر",
            "الأمل نور الحياة"
        ]
    
    def generate_question(self):
        phrase = random.choice(self.phrases)
        self.current_question = f"اكتب هذا النص بالضبط:\n{phrase}"
        self.current_answer = phrase
    
    def _check_answer_logic(self, answer):
        return answer.strip() == self.current_answer


class WordsGame(Game):
    """🔤 لعبة الكلمات"""
    
    def __init__(self, mode="فردي"):
        super().__init__("كلمات", mode)
        self.words = [
            {"scrambled": "سرمدة", "answer": ["مدرسة"]},
            {"scrambled": "باتك", "answer": ["كتاب"]},
            {"scrambled": "ملق", "answer": ["قلم"]},
            {"scrambled": "رسية", "answer": ["سيارة"]},
            {"scrambled": "بحر", "answer": ["حرب", "برح"]},
            {"scrambled": "رمق", "answer": ["قمر"]},
        ]
    
    def generate_question(self):
        word_data = random.choice(self.words)
        self.current_question = f"رتّب الحروف:\n{word_data['scrambled']}"
        self.current_answer = word_data['answer']
    
    def _check_answer_logic(self, answer):
        answer = answer.strip().lower()
        for correct in self.current_answer:
            if answer == correct.lower():
                return True
        return False


class SongGame(Game):
    """🎵 لعبة الأغاني"""
    
    def __init__(self, mode="فردي"):
        super().__init__("أغاني", mode)
        self.songs = [
            {"lyrics": "رجعت لي أيام الماضي", "artist": ["أم كلثوم", "ام كلثوم"]},
            {"lyrics": "جلست والخوف بعينيها", "artist": ["عبد الحليم", "عبدالحليم"]},
            {"lyrics": "تملي معاك ولو حتى بعيد", "artist": ["عمرو دياب", "عمرودياب"]},
            {"lyrics": "يا بنات يا بنات", "artist": ["نانسي عجرم", "نانسي"]},
        ]
    
    def generate_question(self):
        song = random.choice(self.songs)
        self.current_question = f"من المغني؟\n\"{song['lyrics']}\""
        self.current_answer = song['artist']
    
    def _check_answer_logic(self, answer):
        answer = answer.strip().lower().replace(" ", "")
        for correct in self.current_answer:
            if answer == correct.lower().replace(" ", ""):
                return True
        return False


# ============================================================================
# مدير الألعاب
# ============================================================================

GAMES = {
    "ذكاء": IQGame,
    "رياضيات": MathGame,
    "ألوان": ColorGame,
    "سرعة": SpeedGame,
    "كلمات": WordsGame,
    "أغاني": SongGame
}

def create_game(game_type, mode="فردي"):
    """إنشاء لعبة جديدة"""
    if game_type in GAMES:
        return GAMES[game_type](mode)
    return None
