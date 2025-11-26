"""
🧠 لعبة الذكاء - Bot Mesh v7.0 Enhanced
ألغاز ذكية مع تصميم احترافي وأداء محسّن
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class Game(BaseGame):
    """لعبة الذكاء المحسّنة"""

    def __init__(self):
        super().__init__(questions_count=5)
        self.game_name = "ذكاء"
        self.game_icon = "🧠"
        
        # قاعدة ألغاز محسّنة ومتنوعة
        self.riddles = [
            {
                "q": "ما الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟",
                "a": ["السحاب", "الغيم", "سحاب", "غيم", "السحابة"]
            },
            {
                "q": "له رأس ولكن لا عين له؟",
                "a": ["الدبوس", "دبوس", "المسمار", "مسمار", "الإبرة"]
            },
            {
                "q": "شيء كلما زاد نقص؟",
                "a": ["العمر", "عمر", "الوقت", "وقت"]
            },
            {
                "q": "يكتب ولا يقرأ أبداً؟",
                "a": ["القلم", "قلم"]
            },
            {
                "q": "له أسنان كثيرة ولكنه لا يعض؟",
                "a": ["المشط", "مشط"]
            },
            {
                "q": "يوجد في الماء ولكن الماء يميته؟",
                "a": ["الملح", "ملح"]
            },
            {
                "q": "يتكلم بجميع اللغات دون أن يتعلمها؟",
                "a": ["الصدى", "صدى"]
            },
            {
                "q": "شيء يُؤخذ منك قبل أن تُعطيه؟",
                "a": ["الصورة", "صورة", "الصوره"]
            },
            {
                "q": "يطير بلا جناح ويبكي بلا عين؟",
                "a": ["السحاب", "الغيم", "سحاب", "غيم"]
            },
            {
                "q": "شيء كلما أخذت منه كبر؟",
                "a": ["الحفرة", "حفرة", "الحفره"]
            },
            {
                "q": "يخترق الزجاج ولا يكسره؟",
                "a": ["الضوء", "ضوء", "النور", "نور"]
            },
            {
                "q": "يسمع بلا أذن ويتكلم بلا لسان؟",
                "a": ["الهاتف", "هاتف", "التلفون", "تلفون", "الجوال"]
            },
            {
                "q": "يجري ولا يمشي ويُشرب ولا يُؤكل؟",
                "a": ["الماء", "ماء", "النهر", "نهر"]
            },
            {
                "q": "له عنق ولكن بلا رأس؟",
                "a": ["الزجاجة", "زجاجة", "القارورة", "قارورة"]
            },
            {
                "q": "يتبعك أينما ذهبت في النهار فقط؟",
                "a": ["الظل", "ظل", "ظلك"]
            },
            {
                "q": "بيت بلا أبواب ولا نوافذ؟",
                "a": ["البيضة", "بيضة", "بيضه"]
            },
            {
                "q": "أخوان لا يلتقيان أبداً؟",
                "a": ["الليل والنهار", "النهار والليل", "ليل ونهار"]
            },
            {
                "q": "ما الذي له عين ولا يرى؟",
                "a": ["الإبرة", "ابرة", "إبرة"]
            }
        ]
        
        random.shuffle(self.riddles)
        self.used_riddles = []

    def start(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.used_riddles = []
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        """إنشاء سؤال مع واجهة Flex احترافية"""
        # اختيار لغز
        available = [r for r in self.riddles if r not in self.used_riddles]
        if not available:
            self.used_riddles = []
            available = self.riddles.copy()
        
        riddle = random.choice(available)
        self.used_riddles.append(riddle)
        
        self.current_answer = riddle["a"]
        
        # حفظ السؤال السابق
        if self.current_question > 0 and self.previous_answer:
            self.previous_question = self.used_riddles[-2]["q"] if len(self.used_riddles) > 1 else None
        
        # بناء الواجهة
        return self.build_question_flex(
            question_text=f"🧩 {riddle['q']}",
            theme_name="أزرق",
            additional_info="💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة"
        )

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص الإجابة"""
        if not self.game_active or user_id in self.answered_users:
            return None
        
        normalized = self.normalize_text(user_answer)
        
        # معالجة التلميح
        if normalized == "لمح":
            hint = self.get_hint()
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }
        
        # معالجة كشف الإجابة
        if normalized == "جاوب":
            answer_text = " أو ".join(self.current_answer[:3])
            reveal = f"📝 الإجابة: {answer_text}"
            
            # حفظ الإجابة
            self.previous_answer = answer_text
            
            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result
            
            next_q = self.get_question()
            return {
                'message': reveal,
                'response': next_q,
                'points': 0
            }
        
        # التحقق من الإجابة
        for correct in self.current_answer:
            if self.normalize_text(correct) == normalized:
                points = self.add_score(user_id, display_name, 10)
                
                # حفظ الإجابة الصحيحة
                self.previous_answer = correct
                
                # الانتقال للسؤال التالي
                self.current_question += 1
                self.answered_users.clear()
                
                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result['points'] = points
                    result['message'] = f"✅ صحيح يا {display_name}!\n🎯 {correct}\n+{points} نقطة\n\n{result.get('message', '')}"
                    return result
                
                next_q = self.get_question()
                success_msg = f"✅ صحيح يا {display_name}!\n🎯 {correct}\n+{points} نقطة"
                
                return {
                    'message': success_msg,
                    'response': next_q,
                    'points': points
                }
        
        # إجابة خاطئة
        return {
            'message': "❌ إجابة غير صحيحة، حاول مرة أخرى",
            'response': self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
            'points': 0
        }

    def get_hint(self) -> str:
        """تلميح ذكي"""
        if not self.current_answer or len(self.current_answer[0]) < 2:
            return "💡 فكر جيداً في الأمر!"
        
        answer = self.current_answer[0]
        first_letter = answer[0]
        length = len(answer)
        
        return f"💡 يبدأ بحرف '{first_letter}' وعدد الحروف: {length}"

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        info = super().get_game_info()
        info.update({
            "description": "ألغاز ذكية ومتنوعة",
            "riddles_count": len(self.riddles)
        })
        return info
