"""
لعبة التخمين - النسخة المحسنة النهائية
Created by: Abeer Aldosari © 2025

الميزات:
✅ AI أولاً مع Fallback قوي
✅ فئات متنوعة ومحدثة
✅ واجهة Flex احترافية
✅ تشفير عربي مثالي
✅ أداء محسن
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional, List


class GuessGame(BaseGame):
    """لعبة التخمين المحسنة مع AI"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "تخمين"
        self.game_icon = "🔮"
        
        # قاعدة بيانات الأشياء مع الفئات
        self.items = {
            "المطبخ 🍳": {
                "ق": ["قدر", "قلاية"],
                "م": ["ملعقة", "مغرفة"],
                "س": ["سكين", "صحن"],
                "ط": ["طنجرة"],
                "ف": ["فرن", "فنجان"]
            },
            "غرفة النوم 🛏️": {
                "س": ["سرير"],
                "و": ["وسادة"],
                "م": ["مرآة", "مخدة"],
                "خ": ["خزانة"],
                "ل": ["لحاف"]
            },
            "المدرسة 🏫": {
                "ق": ["قلم"],
                "د": ["دفتر"],
                "ك": ["كتاب"],
                "م": ["مسطرة", "ممحاة"],
                "س": ["سبورة"],
                "ح": ["حقيبة"]
            },
            "الفواكه 🍎": {
                "ت": ["تفاح", "تمر"],
                "م": ["موز", "مشمش"],
                "ع": ["عنب"],
                "ب": ["برتقال", "بطيخ"],
                "ر": ["رمان"],
                "ك": ["كمثرى"]
            },
            "الحيوانات 🦁": {
                "ق": ["قطة"],
                "س": ["سنجاب"],
                "ف": ["فيل"],
                "أ": ["أسد", "أرنب"],
                "ج": ["جمل"],
                "ن": ["نمر"]
            }
        }
        
        # إنشاء قائمة الأسئلة
        self.questions_list: List[Dict[str, Any]] = []
        for category, letters in self.items.items():
            for letter, words in letters.items():
                if words:
                    self.questions_list.append({
                        "category": category,
                        "letter": letter,
                        "answers": words
                    })
        
        random.shuffle(self.questions_list)
        self.previous_question = None
        self.previous_answer = None

    def generate_question_with_ai(self):
        """توليد سؤال بالذكاء الاصطناعي مع Fallback"""
        question_data = None
        
        # محاولة AI أولاً
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
                if question_data and "category" in question_data and "letter" in question_data and "answers" in question_data:
                    return question_data
            except Exception as e:
                print(f"⚠️ AI generation failed, using fallback: {e}")
        
        # Fallback
        return self.questions_list[self.current_question % len(self.questions_list)]

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        """إنشاء سؤال مع واجهة Flex محسنة"""
        q_data = self.generate_question_with_ai()
        self.current_answer = q_data["answers"]
        
        colors = self.get_theme_colors()
        
        # قسم السؤال السابق
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
                            "text": f"{self.previous_question['category']} - {self.previous_question['letter']}",
                            "size": "xs",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "xs"
                        },
                        {
                            "type": "text",
                            "text": f"✅ الجواب: {self.previous_answer}",
                            "size": "xs",
                            "color": colors["success"],
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
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{self.game_icon} {self.game_name}",
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
                "contents": previous_section + [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📂 الفئة:",
                                "size": "sm",
                                "color": colors["text2"],
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": q_data["category"],
                                "size": "xl",
                                "color": colors["primary"],
                                "weight": "bold",
                                "align": "center",
                                "margin": "sm"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🔤 يبدأ بحرف:",
                                "size": "sm",
                                "color": colors["text2"],
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": q_data["letter"],
                                "size": "xxl",
                                "color": colors["primary"],
                                "weight": "bold",
                                "align": "center",
                                "margin": "sm"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "md",
                        "wrap": True
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
                        "color": colors["error"]
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

        return self._create_flex_with_buttons("لعبة التخمين", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """التحقق من إجابة اللاعب"""
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)
        
        # معالجة أمر التلميح
        if normalized == "لمح":
            hint = self.get_hint()
            if self.current_answer:
                hint = f"💡 الكلمة من {len(self.current_answer[0])} أحرف"
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }
        
        # معالجة أمر كشف الإجابة
        if normalized == "جاوب":
            answers_text = " أو ".join(self.current_answer)
            reveal = f"📝 الإجابة: {answers_text}"
            
            # حفظ السؤال والجواب
            q_data = self.generate_question_with_ai()
            self.previous_question = q_data
            self.previous_answer = answers_text
            
            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message','')}"
                return result
            
            next_q = self.get_question()
            return {
                'message': reveal,
                'response': next_q,
                'points': 0
            }
        
        # التحقق من الإجابة
        for correct_answer in self.current_answer:
            if self.normalize_text(correct_answer) == normalized:
                points = self.add_score(user_id, display_name, 10)
                
                # حفظ السؤال والجواب
                q_data = self.generate_question_with_ai()
                self.previous_question = q_data
                self.previous_answer = correct_answer
                
                # الانتقال للسؤال التالي
                self.current_question += 1
                self.answered_users.clear()
                
                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result['points'] = points
                    result['message'] = f"✅ إجابة صحيحة يا {display_name}!\n🎯 الكلمة: {correct_answer}\n+{points} نقطة\n\n{result.get('message', '')}"
                    return result
                
                next_q = self.get_question()
                success_message = f"✅ إجابة صحيحة يا {display_name}!\n🎯 الكلمة: {correct_answer}\n+{points} نقطة"
                
                return {
                    'message': success_message,
                    'response': next_q,
                    'points': points
                }
        
        # إجابة خاطئة
        return {
            'message': "❌ إجابة غير صحيحة، حاول مرة أخرى",
            'response': self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
            'points': 0
        }

    def get_game_info(self) -> Dict[str, Any]:
        """الحصول على معلومات اللعبة"""
        return {
            "name": "لعبة التخمين",
            "emoji": "🔮",
            "description": "خمّن الكلمة من الفئة والحرف الأول مع دعم AI",
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "categories_count": len(self.items),
            "ai_enabled": self.ai_generate_question is not None
        }
