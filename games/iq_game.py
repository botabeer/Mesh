"""
لعبة الذكاء - النسخة المحسنة v5.0
Created by: Abeer Aldosari © 2025

التحسينات:
✅ أزرار ثابتة موحدة
✅ نصوص مختصرة وواضحة
✅ تتبع محسّن للأسئلة السابقة
✅ واجهة نظيفة وسريعة
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional


class IqGame(BaseGame):
    """لعبة الذكاء المحسنة"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "IQ"
        self.game_icon = "🧠"
        
        # قاعدة أسئلة محسنة
        self.fallback_questions = [
            {"q": "ما يمشي بلا أرجل ويبكي بلا عيون؟", "a": ["السحاب", "الغيم"]},
            {"q": "له رأس ولا عين له؟", "a": ["الدبوس", "المسمار"]},
            {"q": "إذا أكلته كله تستفيد، نصفه تموت؟", "a": ["السمسم"]},
            {"q": "في السماء، بحرف يصبح في الأرض؟", "a": ["نجم"]},
            {"q": "كلما زاد نقص؟", "a": ["العمر", "الوقت"]},
            {"q": "يكتب ولا يقرأ؟", "a": ["القلم"]},
            {"q": "له أسنان ولا يعض؟", "a": ["المشط"]},
            {"q": "في الماء، الماء يميته؟", "a": ["الملح"]},
            {"q": "يتكلم كل اللغات؟", "a": ["الصدى"]},
            {"q": "يؤخذ منك قبل أن تعطيه؟", "a": ["الصورة"]}
        ]
        
        random.shuffle(self.fallback_questions)
        self.used_questions = []
    
    def generate_question_with_ai(self):
        """توليد سؤال مع Fallback"""
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
                if question_data and "q" in question_data and "a" in question_data:
                    if not isinstance(question_data["a"], list):
                        question_data["a"] = [str(question_data["a"])]
                    return question_data
            except Exception as e:
                print(f"⚠️ AI فشل، Fallback: {e}")
        
        # Fallback
        available = [q for q in self.fallback_questions if q not in self.used_questions]
        if not available:
            self.used_questions = []
            available = self.fallback_questions.copy()
        
        question_data = random.choice(available)
        self.used_questions.append(question_data)
        return question_data
    
    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.previous_question_text = None
        self.previous_answer_text = None
        self.answered_users.clear()
        return self.get_question()
    
    def get_question(self):
        """إنشاء سؤال"""
        q_data = self.generate_question_with_ai()
        self.current_answer = q_data["a"]
        
        colors = self.get_theme_colors()
        
        # بناء المحتوى
        contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{self.game_icon} {self.game_name}",
                        "size": "xl",
                        "weight": "bold",
                        "color": colors["text"],
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": f"{self.current_question + 1}/5",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "end",
                        "flex": 1
                    }
                ]
            }
        ]
        
        # قسم السؤال السابق
        contents.extend(self._create_previous_section(colors))
        
        # السؤال الحالي
        contents.extend([
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "❓ اللغز:",
                        "size": "sm",
                        "color": colors["text2"],
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": q_data["q"],
                        "size": "md",
                        "color": colors["text"],
                        "wrap": True,
                        "margin": "sm",
                        "weight": "bold"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "20px",
                "margin": "md"
            }
        ])
        
        flex_content = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": contents,
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": self._create_fixed_buttons(colors),
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }
        
        return self._create_flex_with_buttons(f"{self.game_name} - {self.current_question + 1}/5", flex_content)
    
    def check_answer_intelligently(self, user_answer: str) -> bool:
        """فحص ذكي للإجابة"""
        normalized_user = self.normalize_text(user_answer)
        
        for correct in self.current_answer:
            normalized_correct = self.normalize_text(correct)
            
            if normalized_user == normalized_correct:
                return True
            
            if normalized_user in normalized_correct or normalized_correct in normalized_user:
                return True
            
            ratio = difflib.SequenceMatcher(None, normalized_user, normalized_correct).ratio()
            if ratio > 0.85:
                return True
        
        if self.ai_check_answer:
            try:
                for correct in self.current_answer:
                    if self.ai_check_answer(correct, user_answer):
                        return True
            except:
                pass
        
        return False
    
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص الإجابة"""
        if not self.game_active or user_id in self.answered_users:
            return None
        
        normalized = self.normalize_text(user_answer)
        
        # أمر التلميح
        if normalized == "لمح":
            hint = self.get_hint()
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }
        
        # أمر كشف الإجابة
        if normalized == "جاوب":
            answer_text = self.current_answer[0] if isinstance(self.current_answer, list) else str(self.current_answer)
            reveal = f"📝 الجواب: {answer_text}"
            
            # حفظ السؤال والجواب
            q_data = self.generate_question_with_ai()
            self.previous_question_text = q_data["q"]
            self.previous_answer_text = answer_text
            
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result
            
            next_q = self.get_question()
            return {'message': reveal, 'response': next_q, 'points': 0}
        
        # فحص الإجابة
        is_correct = self.check_answer_intelligently(user_answer)
        
        if is_correct:
            points = self.add_score(user_id, display_name, 10)
            
            # حفظ السؤال والجواب
            q_data = self.generate_question_with_ai()
            self.previous_question_text = q_data["q"]
            self.previous_answer_text = self.current_answer[0] if isinstance(self.current_answer, list) else str(self.current_answer)
            
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ صحيح يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
                return result
            
            next_q = self.get_question()
            success_msg = f"✅ صحيح يا {display_name}!\n+{points} نقطة"
            
            return {
                'message': success_msg,
                'response': next_q,
                'points': points
            }
        
        return {
            'message': "❌ غير صحيح، حاول مرة أخرى",
            'response': self._create_text_message("❌ غير صحيح، حاول مرة أخرى"),
            'points': 0
        }
    
    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة الذكاء",
            "emoji": "🧠",
            "description": "ألغاز ذكاء ممتعة",
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "ai_enabled": self.ai_generate_question is not None
        }
