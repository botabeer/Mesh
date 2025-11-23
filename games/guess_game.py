"""
لعبة التخمين بالفئات والحروف - نسخة موسعة Neumorphism
"""
from linebot.models import TextSendMessage
from .base_game import BaseGame
import random


class GuessGame(BaseGame):
    """لعبة تخمين الكلمة من الفئة والحرف (موسعة)"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)  # 5 جولات
        self.items = {
            "المطبخ": {"ق": ["قدر", "قلاية"], "م": ["ملعقة", "مغرفة"], "س": ["سكين", "صحن"]},
            "غرفة النوم": {"س": ["سرير"], "و": ["وسادة"], "م": ["مرآة", "مخدة"]},
            "غرفة الجلوس": {"ك": ["كرسي", "كنب"], "ط": ["طاولة"], "ت": ["تلفاز"]},
            "الحمام": {"ص": ["صابون"], "م": ["مرحاض", "مغسلة"], "ش": ["شامبو"]},
            "المدرسة": {"ق": ["قلم"], "د": ["دفتر"], "ك": ["كتاب"], "م": ["مسطرة", "ممحاة"]},
            "السيارة": {"م": ["محرك", "مقود"], "ع": ["عجلة"], "ك": ["كرسي"]},
            "الحديقة": {"ش": ["شجرة"], "ز": ["زهرة"], "ع": ["عشب"]},
            "الفواكه": {"ت": ["تفاح", "تمر"], "م": ["موز", "مانجو"], "ع": ["عنب"]},
            "الخضار": {"ج": ["جزر"], "خ": ["خيار"], "ب": ["بصل"]},
            "الحيوانات": {"ق": ["قطة"], "س": ["سنجاب"], "ف": ["فيل"]},
            "المهن": {"ط": ["طبيب"], "م": ["مهندس"], "م": ["مزارع"]},
            "الأدوات": {"م": ["مطرقة"], "م": ["مفك"], "م": ["مقص"]},
            "الملابس": {"ق": ["قميص"], "س": ["سروال"], "ح": ["حذاء"]},
            "الأعضاء": {"ر": ["رأس"], "ي": ["يد"], "ق": ["قلب"]},
            "الأماكن": {"م": ["مسجد"], "س": ["سوق"], "م": ["مدرسة"]},
            "وسائل المواصلات": {"س": ["سيارة"], "ح": ["حافلة"], "د": ["دراجة"]},
            "الإلكترونيات": {"ه": ["هاتف"], "ت": ["تلفاز"], "ك": ["كمبيوتر"]}
        }
        
        self.questions_list = []
        for cat, letters in self.items.items():
            for letter, words in letters.items():
                if words:
                    self.questions_list.append({
                        "category": cat,
                        "letter": letter,
                        "answers": words
                    })
        random.shuffle(self.questions_list)
    
    def start_game(self):
        self.current_question = 0
        return self.get_question()
    
    def get_question(self):
        q_data = self.questions_list[self.current_question % len(self.questions_list)]
        self.current_answer = q_data["answers"]
        
        message = f"▫️ تخمين الكلمة ({self.current_question + 1}/{self.questions_count}) ▪️\n\n"
        message += f"▫️ الفئة: {q_data['category']} ▪️\n"
        message += f"▫️ يبدأ بحرف: {q_data['letter']} ▪️\n\n"
        message += "▫️ جاوب - لعرض الإجابة ▪️"
        
        return TextSendMessage(text=message)
    
    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None
        
        if user_id in self.answered_users:
            return None
        
        normalized_answer = self.normalize_text(user_answer)
        
        # أمر "جاوب"
        if normalized_answer == "جاوب":
            answers_text = " أو ".join(self.current_answer)
            reveal = f"▪️ الإجابة: {answers_text} ▫️"
            next_q = self.next_question()
            message = f"{reveal}\n\n"
            if hasattr(next_q, 'text'):
                message += next_q.text
            return {
                "message": message,
                "response": TextSendMessage(text=message),
                "points": 0
            }
        
        # فحص الإجابة الصحيحة
        for correct_answer in self.current_answer:
            if self.normalize_text(correct_answer) == normalized_answer:
                points = self.add_score(user_id, display_name, 10)
                next_q = self.next_question()
                message = f"▪️ إجابة صحيحة يا {display_name} ▫️\n+{points} نقطة\n\n"
                if hasattr(next_q, 'text'):
                    message += next_q.text
                return {
                    "message": message,
                    "response": TextSendMessage(text=message),
                    "points": points
                }
        
        return None
