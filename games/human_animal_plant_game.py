"""
لعبة إنسان حيوان نبات جماد بلاد - نسخة AI ▫️▪️
Created by: Abeer Aldosari © 2025

تحديثات:
- Flex Message Neumorphism
- دعم ثيمات ديناميكية
- تتبع النقاط لكل لاعب
- دعم AI للتحقق من الإجابة
"""
from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional

class HumanAnimalPlantGame(BaseGame):
    """لعبة إنسان حيوان نبات جماد بلاد - Flex + AI Version"""
    
    def __init__(self, line_bot_api, ai_checker=None):
        super().__init__(line_bot_api, questions_count=5)
        self.letters = list("ابتجحدرزسشصطعفقكلمنهوي")
        random.shuffle(self.letters)
        self.categories = ["إنسان", "حيوان", "نبات", "جماد", "بلاد"]
        self.ai_checker = ai_checker
        self.answers_db = {
            "إنسان": {"أ": ["أحمد","أمل","أسامة","أمير"], "ب": ["بدر","بسمة"], "ت": ["تامر","تالا"]},
            "حيوان": {"أ": ["أسد","أرنب"], "ب": ["بقرة","بطة"], "ج": ["جمل","جراد"]},
            "نبات": {"ت": ["تفاح","توت"], "ج": ["جزر","جوز"]},
            "جماد": {"ب": ["باب","بيت"], "ت": ["تلفاز","ترابيزة"]},
            "بلاد": {"أ": ["الأردن","الإمارات"], "ب": ["البحرين","بريطانيا"]}
        }
        self.current_category = None
        self.current_letter = None

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def get_question(self) -> Any:
        colors = self.get_theme_colors()
        self.current_letter = self.letters[self.current_question % len(self.letters)]
        self.current_category = random.choice(self.categories)

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🎯 إنسان حيوان نبات جماد بلاد", "size": "xl",
                     "weight": "bold", "color": colors["text"], "align": "center"},
                    {"type": "text", "text": f"سؤال {self.current_question+1} من {self.questions_count}",
                     "size": "sm", "color": colors["text2"], "align": "center", "margin": "xs"}
                ],
                "backgroundColor": colors["bg"], "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"▫️ الفئة: {self.current_category}", "size": "md",
                     "color": colors["text"], "align": "center", "margin": "md"},
                    {"type": "text", "text": f"▫️ الحرف: {self.current_letter}", "size": "xxl",
                     "weight": "bold", "color": colors["primary"], "align": "center", "margin": "md"},
                    {"type": "text", "text": "💡 اكتب 'جاوب' للكشف عن إجابة مقترحة", "size": "xs",
                     "color": colors["text2"], "align": "center", "margin": "md", "wrap": True}
                ],
                "backgroundColor": colors["bg"], "paddingAll": "15px"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }
        return self._create_flex_with_buttons("إنسان حيوان نبات جماد بلاد", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized_answer = self.normalize_text(user_answer)

        # أمر "جاوب"
        if normalized_answer == "جاوب":
            suggested = None
            if self.current_category in self.answers_db and self.current_letter in self.answers_db[self.current_category]:
                suggested = random.choice(self.answers_db[self.current_category][self.current_letter])
            reveal = f"▫️ إجابة مقترحة: {suggested}" if suggested else f"▫️ أي كلمة تبدأ بحرف {self.current_letter}"
            next_q = self.next_question()
            return {"message": reveal, "response": self._create_text_message(f"{reveal}\n\n{next_q}"), "points": 0}

        # تحقق من الحرف
        if not normalized_answer or normalized_answer[0] != self.normalize_text(self.current_letter):
            msg = f"▫️ يجب أن تبدأ الكلمة بحرف {self.current_letter} ▪️"
            return {"message": msg, "response": self._create_text_message(msg), "points": 0}

        if len(normalized_answer) < 2:
            msg = "▫️ الكلمة قصيرة جداً ▪️"
            return {"message": msg, "response": self._create_text_message(msg), "points": 0}

        # تحقق من قاعدة البيانات أو AI
        valid = False
        if self.current_category in self.answers_db and self.current_letter in self.answers_db[self.current_category]:
            valid = normalized_answer in [self.normalize_text(a) for a in self.answers_db[self.current_category][self.current_letter]]
        if not valid and self.ai_checker:
            valid = self.ai_checker(self.current_category, normalized_answer)

        if not valid:
            msg = "▫️ إجابة غير صحيحة ▪️"
            return {"message": msg, "response": self._create_text_message(msg), "points": 0}

        points = self.add_score(user_id, display_name, 10)
        next_q = self.next_question()
        msg = f"▫️ إجابة صحيحة يا {display_name} ▪️\n+{points} نقطة\n\n"
        return {"message": msg, "response": next_q, "points": points}

    def get_game_info(self) -> Dict[str, Any]:
        return {
            "name": "لعبة إنسان حيوان نبات جماد بلاد",
            "emoji": "▫️▪️",
            "description": "اكتب كلمة تبدأ بالحرف المحدد في الفئة المختارة",
            "questions_count": self.questions_count,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }

# ============================================================================
# مثال على الاستخدام
# ============================================================================
if __name__ == "__main__":
    print("✅ ملف لعبة إنسان حيوان نبات جماد بلاد جاهز للاستخدام!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
