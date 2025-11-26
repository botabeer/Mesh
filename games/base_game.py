import random
from datetime import datetime

# ============================================================================
# محرك اللعبة الأساسي
# ============================================================================

class Game:
    """محرك اللعبة الأساسي - يدعم الفردي والمجموعة"""
    
    def __init__(self, game_type, mode="فردي", max_rounds=5):
        self.game_type = game_type
        self.mode = mode  # "فردي" أو "مجموعة"
        self.max_rounds = max_rounds
        
        # حالة اللعبة
        self.active = True
        self.current_round = 0
        self.current_question = None
        self.current_answer = None
        
        # النقاط (للفردي والمجموعة)
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
        
        # إذا أجاب في هذه الجولة (مجموعة فقط)
        if self.mode == "مجموعة" and user_id in self.answered_this_round:
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
# Alias للتوافق مع الألعاب
# ============================================================================
BaseGame = Game
