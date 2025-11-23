"""
لعبة إنسان حيوان نبات جماد بلاد - نسخة محسّنة مع AI ▫️▪️
"""
from linebot.models import TextSendMessage
from .base_game import BaseGame
import random

class HumanAnimalPlantGame(BaseGame):
    """لعبة إنسان حيوان نبات جماد بلاد محسّنة ▫️▪️ مع AI"""
    
    def __init__(self, line_bot_api, ai_checker=None):
        super().__init__(line_bot_api, questions_count=5)
        self.letters = list("ابتجحدرزسشصطعفقكلمنهوي")
        random.shuffle(self.letters)
        self.categories = ["إنسان", "حيوان", "نبات", "جماد", "بلاد"]
        self.ai_checker = ai_checker  # دالة للتحقق من الإجابة باستخدام AI
        
        # قاعدة بيانات موسّعة مع أمثلة أكثر
        self.answers_db = {
            "إنسان": {
                "أ": ["أحمد","أمل","أسامة","أمير","إبراهيم","أسماء"],
                "ب": ["بدر","بسمة","باسل","بشرى","بلال"],
                "ت": ["تامر","تالا","تركي","تهاني"],
            },
            "حيوان": {
                "أ": ["أسد","أرنب","أفعى","أخطبوط"],
                "ب": ["بقرة","بطة","ببغاء","بجعة"],
                "ج": ["جمل","جراد","جربوع"]
            },
            "نبات": {
                "ت": ["تفاح","توت","تين","تمر"],
                "ج": ["جزر","جوز","جعدة"],
                "ح": ["حمص","حلبة"]
            },
            "جماد": {
                "ب": ["باب","بيت","برج","بلاط"],
                "ت": ["تلفاز","ترابيزة","تاج"],
                "ج": ["جدار","جسر","جهاز"]
            },
            "بلاد": {
                "أ": ["الأردن","الإمارات","إثيوبيا","أفغانستان"],
                "ب": ["البحرين","بريطانيا","بلجيكا"],
                "ت": ["تونس","تركيا","تايلاند"]
            }
        }
        self.current_category = None
        self.current_letter = None
    
    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()
    
    def get_question(self):
        self.current_letter = self.letters[self.current_question % len(self.letters)]
        self.current_category = random.choice(self.categories)
        message = f"▫️ لعبة إنسان حيوان نبات ({self.current_question + 1}/{self.questions_count}) ▪️\n\n"
        message += f"▫️ الفئة: {self.current_category} ▪️\n"
        message += f"▫️ الحرف: {self.current_letter} ▪️\n\n"
        message += f"▫️ اكتب {self.current_category} يبدأ بحرف {self.current_letter} ▪️\n"
        message += "▫️ جاوب - لعرض إجابة مقترحة ▪️"
        return TextSendMessage(text=message)
    
    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active or user_id in self.answered_users:
            return None
        
        normalized_answer = self.normalize_text(user_answer)
        
        # أمر "جاوب"
        if normalized_answer == "جاوب":
            suggested = None
            if self.current_category in self.answers_db and self.current_letter in self.answers_db[self.current_category]:
                suggested = random.choice(self.answers_db[self.current_category][self.current_letter])
            reveal = f"▫️ إجابة مقترحة: {suggested} ▪️" if suggested else f"▫️ أي كلمة تبدأ بحرف {self.current_letter} ▪️"
            next_q = self.next_question()
            message = f"{reveal}\n\n"
            if hasattr(next_q, 'text'):
                message += next_q.text
            return {"message": message, "response": TextSendMessage(text=message), "points": 0}
        
        # التحقق من الحرف
        if not normalized_answer or normalized_answer[0] != self.normalize_text(self.current_letter):
            return {"message": f"▫️ يجب أن تبدأ الكلمة بحرف {self.current_letter} ▪️",
                    "response": TextSendMessage(text=f"▫️ يجب أن تبدأ الكلمة بحرف {self.current_letter} ▪️"),
                    "points": 0}
        
        if len(normalized_answer) < 2:
            return {"message": "▫️ الكلمة قصيرة جداً ▪️",
                    "response": TextSendMessage(text="▫️ الكلمة قصيرة جداً ▪️"),
                    "points": 0}
        
        # قبول الإجابة: من القاعدة أو AI
        valid = False
        if self.current_category in self.answers_db and self.current_letter in self.answers_db[self.current_category]:
            valid = normalized_answer in [self.normalize_text(a) for a in self.answers_db[self.current_category][self.current_letter]]
        # تحقق باستخدام AI إذا متاح
        if not valid and self.ai_checker:
            valid = self.ai_checker(self.current_category, normalized_answer)
        
        if not valid:
            return {"message": "▫️ إجابة غير صحيحة ▪️",
                    "response": TextSendMessage(text="▫️ إجابة غير صحيحة ▪️"),
                    "points": 0}
        
        # نقاط وإنتقال للسؤال التالي
        points = self.add_score(user_id, display_name, 10)
        next_q = self.next_question()
        message = f"▫️ إجابة صحيحة يا {display_name} ▪️\n+{points} نقطة\n\n"
        if hasattr(next_q, 'text'):
            message += next_q.text
        return {"message": message, "response": TextSendMessage(text=message), "points": points}
