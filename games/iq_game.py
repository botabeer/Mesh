"""
لعبة الذكاء - نسخة محسّنة مع AI ذكي
Created by: Abeer Aldosari © 2025

التحسينات:
- AI أولاً مع Fallback تلقائي
- قبول إجابات منطقية ومتشابهة
- 5 جولات مع إعلان فوري للفائز
- واجهة Flex احترافية
- عرض السؤال السابق والجواب
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional

class IqGame(BaseGame):
    """لعبة الذكاء المحسّنة"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "IQ"
        self.game_icon = "🧠"
        
        # AI functions (will be set by app.py)
        self.ai_generate_question = None
        self.ai_check_answer = None
        
        # Fallback questions (محسّنة)
        self.fallback_questions = [
            {"q": "ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟", "a": ["السحاب", "السحابة", "الغيم"]},
            {"q": "له رأس ولا عين له؟", "a": ["الدبوس", "الدبابيس", "المسمار"]},
            {"q": "ما هو الشيء الذي إذا أكلته كله تستفيد وإذا أكلت نصفه تموت؟", "a": ["السمسم", "سمسم"]},
            {"q": "شيء موجود في السماء إذا أضفت إليه حرفا أصبح في الأرض؟", "a": ["نجم", "نجمة"]},
            {"q": "ما هو الشيء الذي كلما زاد نقص؟", "a": ["العمر", "الوقت", "الزمن"]},
            {"q": "ما هو الشيء الذي يكتب ولا يقرأ؟", "a": ["القلم", "الاقلام"]},
            {"q": "ما هو الشيء الذي له أسنان ولا يعض؟", "a": ["المشط", "الامشاط", "المسطرة"]},
            {"q": "أنا في الماء ولكن إذا لمسني الماء أموت، من أنا؟", "a": ["الملح", "ملح"]},
            {"q": "ما هو الشيء الذي يتحدث جميع لغات العالم؟", "a": ["صدى الصوت", "الصدى", "صدى"]},
            {"q": "شيء يؤخذ منك قبل أن تعطيه؟", "a": ["الصورة", "الصوره", "صورة"]},
            {"q": "ما هو الشيء الذي إذا دخل الماء لم يبتل؟", "a": ["الضوء", "ضوء", "الشعاع"]},
            {"q": "رجل معه ست بنات لكل بنت أخ واحد، كم عدد أولاد الرجل؟", "a": ["7", "سبعة", "سبعه"]},
            {"q": "ما هو الشيء الذي يقرصك ولا تراه؟", "a": ["الجوع", "جوع"]},
            {"q": "ما الذي يحترق دون أن يحترق؟", "a": ["الشمعة", "الشمعه", "شمعة"]},
            {"q": "ما هو الشيء الذي كلما أخذت منه كبر؟", "a": ["الحفرة", "الحفره", "حفرة"]},
            {"q": "ما هو الشيء الذي له عين ولا يرى؟", "a": ["الابرة", "الإبرة", "ابرة"]},
            {"q": "ما هو الشيء الذي تراه في الليل ثلاث مرات وفي النهار مرة واحدة؟", "a": ["حرف اللام", "اللام", "ل"]},
            {"q": "كلمة من أربعة حروف إذا أكلت نصفها تموت وإذا أكلتها كلها لا تموت؟", "a": ["سمسم", "السمسم"]},
            {"q": "ما هو الشيء الذي يوجد في وسط باريس؟", "a": ["حرف الراء", "الراء", "ر"]},
            {"q": "ما هو الشيء الذي ترميه كلما احتجت إليه؟", "a": ["شبكة الصيد", "الشبكة", "شبكه"]}
        ]
        
        self.used_questions = []
        self.previous_question = None
        self.previous_answer = None
    
    def generate_question_with_ai(self):
        """توليد سؤال بالذكاء الاصطناعي مع Fallback"""
        question_data = None
        
        # محاولة AI أولاً
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
                if question_data and "q" in question_data and "a" in question_data:
                    # تأكد من أن الإجابة قائمة
                    if not isinstance(question_data["a"], list):
                        question_data["a"] = [str(question_data["a"])]
                    return question_data
            except Exception as e:
                print(f"⚠️ AI failed, using fallback: {e}")
        
        # Fallback للأسئلة المخزنة
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
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()
    
    def get_question(self):
        """إنشاء سؤال مع واجهة Flex محسّنة"""
        q_data = self.generate_question_with_ai()
        self.current_answer = q_data["a"]
        
        colors = self.get_theme_colors()
        
        # بناء السؤال السابق إن وجد
        previous_section = []
        if self.previous_question and self.previous_answer:
            previous_section = [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 السؤال السابق:",
                            "size": "xs",
                            "color": colors["text2"],
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": self.previous_question,
                            "size": "xs",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "xs"
                        },
                        {
                            "type": "text",
                            "text": f"✅ الجواب: {self.previous_answer}",
                            "size": "xs",
                            "color": "#48BB78",
                            "wrap": True,
                            "margin": "xs"
                        }
                    ],
                    "backgroundColor": colors["card"],
                    "cornerRadius": "15px",
                    "paddingAll": "12px",
                    "margin": "md"
                },
                {"type": "separator", "color": colors["shadow1"], "margin": "md"}
            ]
        
        flex_content = {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
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
                                "text": f"جولة {self.current_question + 1}/5",
                                "size": "sm",
                                "color": colors["text2"],
                                "align": "end",
                                "flex": 2
                            }
                        ]
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": previous_section + [
                    # السؤال الحالي
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "❓ السؤال:",
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
                                "margin": "md",
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px"
                    },
                    # معلومات
                    {
                        "type": "text",
                        "text": "💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "wrap": True,
                        "margin": "md"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "💡 لمّح", "text": "لمح"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "🔍 جاوب", "text": "جاوب"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            }
                        ]
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                        "style": "primary",
                        "height": "sm",
                        "color": "#FF5555"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }
        
        return self._create_flex_with_buttons(f"{self.game_name} - جولة {self.current_question + 1}", flex_content)
    
    def check_answer_intelligently(self, user_answer: str) -> bool:
        """فحص ذكي للإجابة"""
        normalized_user = self.normalize_text(user_answer)
        
        # فحص مباشر
        for correct in self.current_answer:
            normalized_correct = self.normalize_text(correct)
            
            # تطابق كامل
            if normalized_user == normalized_correct:
                return True
            
            # تطابق جزئي (يحتوي على)
            if normalized_user in normalized_correct or normalized_correct in normalized_user:
                return True
            
            # تشابه نصي (أكثر من 80%)
            ratio = difflib.SequenceMatcher(None, normalized_user, normalized_correct).ratio()
            if ratio > 0.80:
                return True
        
        # محاولة AI للتحقق
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
        if not self.game_active:
            return None
        
        # تجاهل المستخدمين الذين أجابوا
        if user_id in self.answered_users:
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
        
        # أمر الإجابة
        if normalized == "جاوب":
            answer_text = self.current_answer[0] if isinstance(self.current_answer, list) else self.current_answer
            reveal = f"📝 الإجابة: {answer_text}"
            
            # حفظ السؤال والجواب
            self.previous_question = self.generate_question_with_ai()["q"]
            self.previous_answer = answer_text
            
            # الانتقال للسؤال التالي
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
            self.previous_question = self.generate_question_with_ai()["q"]
            self.previous_answer = self.current_answer[0] if isinstance(self.current_answer, list) else self.current_answer
            
            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
                return result
            
            next_q = self.get_question()
            success_msg = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة"
            
            return {
                'message': success_msg,
                'response': next_q,
                'points': points
            }
        
        return {
            'message': "❌ إجابة غير صحيحة",
            'response': self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
            'points': 0
        }
    
    def get_hint(self):
        """تلميح ذكي"""
        answer = self.current_answer[0] if isinstance(self.current_answer, list) else self.current_answer
        answer_str = str(answer)
        
        if len(answer_str) <= 3:
            return f"💡 يبدأ بحرف: {answer_str[0]}"
        
        return f"💡 يبدأ بحرف: {answer_str[0]}\n📏 عدد الحروف: {len(answer_str)}"
    
    def get_game_info(self) -> Dict[str, Any]:
        return {
            "name": "لعبة الذكاء",
            "emoji": "🧠",
            "description": "ألغاز ذكاء ممتعة",
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }
