"""
لعبة التخمين - نسخة محدثة ومحسّنة
Created by: Abeer Aldosari © 2025
"""

# ============================================================================
# الاستيراد الصحيح
# ============================================================================
from games.base_game import BaseGame  # ✅ صحيح

import random
from typing import Dict, Any, Optional, List


class GuessGame(BaseGame):
    """
    لعبة التخمين - خمّن الكلمة من الفئة والحرف الأول
    
    الميزات:
    - فئات متنوعة (مطبخ، غرفة نوم، مدرسة، فواكه، حيوانات)
    - تلميحات مفيدة
    - إمكانية كشف الإجابة
    - رسائل Flex حديثة بتصميم Neumorphism
    """
    
    def __init__(self, line_bot_api):
        """
        تهيئة اللعبة
        
        المعاملات:
            line_bot_api: واجهة LINE Bot API
        """
        super().__init__(line_bot_api, questions_count=5)
        
        # تفعيل ميزات التلميح والكشف
        self.supports_hint = True
        self.supports_reveal = True
        
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

    def start_game(self) -> Any:
        """
        بدء اللعبة وإرجاع أول سؤال
        
        العودة:
            FlexMessage: السؤال الأول
        """
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def generate_question(self) -> Dict[str, Any]:
        """
        توليد سؤال من القائمة
        
        العودة:
            dict: بيانات السؤال
        """
        return self.questions_list[self.current_question % len(self.questions_list)]

    def get_question(self) -> Any:
        """
        إنشاء وإرجاع رسالة Flex للسؤال
        
        العودة:
            FlexMessage: السؤال بتصميم Neumorphism
        """
        q_data = self.generate_question()
        self.current_answer = q_data["answers"]
        
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
                        "text": "🔮 لعبة التخمين",
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
                        "text": "💭 خمّن الكلمة...",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "lg"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "💡 اكتب 'لمح' للتلميح\n📝 اكتب 'جاوب' للكشف عن الإجابة",
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
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                }
            }
        }

        return self._create_flex_with_buttons("لعبة التخمين", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """
        التحقق من إجابة اللاعب
        
        المعاملات:
            user_answer: إجابة المستخدم
            user_id: معرف المستخدم
            display_name: اسم المستخدم
            
        العودة:
            dict: نتيجة الإجابة أو None إذا كانت خاطئة
        """
        if not self.game_active:
            return None

        normalized = self.normalize_text(user_answer)
        
        # معالجة أمر التلميح
        if normalized == "لمح":
            hint = self.get_hint()
            if self.current_answer:
                hint = f"💡 تلميح: الكلمة من {len(self.current_answer[0])} أحرف"
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }
        
        # معالجة أمر كشف الإجابة
        if normalized == "جاوب":
            answers_text = " أو ".join(self.current_answer)
            reveal = f"📝 الإجابة الصحيحة:\n{answers_text}"
            next_question = self.next_question()
            
            if isinstance(next_question, dict) and next_question.get('game_over'):
                next_question['message'] = f"{reveal}\n\n{next_question.get('message','')}"
                return next_question
            
            return {
                'message': reveal,
                'response': next_question,
                'points': 0
            }
        
        # التحقق من الإجابة
        for correct_answer in self.current_answer:
            if self.normalize_text(correct_answer) == normalized:
                points = self.add_score(user_id, display_name, 10)
                next_question = self.next_question()
                
                if isinstance(next_question, dict) and next_question.get('game_over'):
                    next_question['points'] = points
                    return next_question
                
                success_message = f"✅ إجابة صحيحة يا {display_name}!\n🎯 الكلمة: {correct_answer}\n+{points} نقطة"
                
                return {
                    'message': success_message,
                    'response': next_question,
                    'points': points
                }
        
        # إجابة خاطئة
        return {
            'message': "❌ إجابة غير صحيحة، حاول مرة أخرى",
            'response': self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
            'points': 0
        }

    def get_game_info(self) -> Dict[str, Any]:
        """
        الحصول على معلومات اللعبة
        
        العودة:
            dict: معلومات اللعبة
        """
        return {
            "name": "لعبة التخمين",
            "emoji": "🔮",
            "description": "خمّن الكلمة من الفئة والحرف الأول",
            "questions_count": self.questions_count,
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "categories_count": len(self.items)
        }


# ============================================================================
# مثال على الاستخدام
# ============================================================================
if __name__ == "__main__":
    print("✅ ملف لعبة التخمين جاهز للاستخدام!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
