"""
لعبة أسئلة الذكاء - Neumorphism Soft with AI
Created by: Abeer Aldosari © 2025
"""
from .base_game import BaseGame
import random
import difflib


class IqGame(BaseGame):
    """لعبة أسئلة الذكاء مع دعم AI وثيمات ديناميكية"""
    
    def __init__(self, line_bot_api, ai_generate_question=None, ai_check_answer=None):
        super().__init__(line_bot_api, questions_count=5)
        self.ai_generate_question = ai_generate_question
        self.ai_check_answer = ai_check_answer
        self.supports_hint = True
        self.supports_reveal = True
        
        # قائمة أسئلة افتراضية
        self.questions = [
            {"q": "ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟", "a": "السحاب"},
            {"q": "ما هو الشيء الذي له رأس ولا يملك عيون؟", "a": "الدبوس"},
            {"q": "شيء موجود في السماء إذا أضفت له حرفاً أصبح في الأرض؟", "a": "نجم"},
            {"q": "ما هو الشيء الذي كلما زاد نقص؟", "a": "العمر"},
            {"q": "ما هو الشيء الذي يكتب ولا يقرأ؟", "a": "القلم"},
            {"q": "له أوراق وليس شجرة؟", "a": "الكتاب"},
            {"q": "ما هو الشيء الذي يسمع بلا أذن ويتكلم بلا لسان؟", "a": "الهاتف"},
            {"q": "له عين واحدة ولا يرى؟", "a": "الإبرة"},
        ]
        random.shuffle(self.questions)

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def generate_question(self):
        """توليد سؤال باستخدام AI أو القائمة الافتراضية"""
        if self.ai_generate_question:
            try:
                new_q = self.ai_generate_question()
                if new_q and "q" in new_q and "a" in new_q:
                    return new_q
            except:
                pass
        return self.questions[self.current_question % len(self.questions)]

    def get_question(self):
        """إنشاء سؤال بستايل Neumorphism Soft"""
        q_data = self.generate_question()
        self.current_answer = q_data["a"]
        colors = self.get_theme_colors()
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🧠 لعبة الذكاء",
                        "size": "xl",
                        "weight": "bold",
                        "color": colors["text"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"سؤال {self.current_question + 1} من {self.questions_count}",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": q_data["q"],
                                "size": "lg",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "💭 فكر جيداً...",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "lg"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                }
            }
        }
        
        return self._create_flex_with_buttons("لعبة الذكاء", flex_content)

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None

        normalized_answer = self.normalize_text(user_answer)

        # تلميح
        if normalized_answer == "لمح":
            hint = self.get_hint()
            return {"message": hint, "response": self._create_text_message(hint), "points": 0}

        # كشف الإجابة
        if normalized_answer == "جاوب":
            reveal = self.reveal_answer()
            next_q = self.next_question()
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['message'] = f"{reveal}\n\n{next_q.get('message','')}"
                return next_q
            return {'message': reveal, 'response': next_q, 'points': 0}

        # التحقق من الإجابة
        normalized_correct = self.normalize_text(self.current_answer)
        valid = False

        # مطابقة تامة
        if normalized_answer == normalized_correct:
            valid = True
        # مطابقة جزئية (80%)
        elif difflib.SequenceMatcher(None, normalized_answer, normalized_correct).ratio() > 0.8:
            valid = True
        # استخدام AI للتحقق
        elif self.ai_check_answer:
            try:
                valid = self.ai_check_answer(self.current_answer, user_answer)
            except:
                pass

        if not valid:
            return {
                "message": "▫️ إجابة غير صحيحة ▪️",
                "response": self._create_text_message("▫️ إجابة غير صحيحة ▪️"),
                "points": 0
            }

        # إجابة صحيحة
        points = self.add_score(user_id, display_name, 10)
        next_q = self.next_question()
        
        if isinstance(next_q, dict) and next_q.get('game_over'):
            next_q['points'] = points
            return next_q
        
        message = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة"
        return {"message": message, "response": next_q, "points": points}
