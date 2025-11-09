import random
import re
from linebot.models import TextSendMessage

class OppositeGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_word = None
        self.correct_answer = None
        
        # قاموس الأضداد الموسع
        self.opposites = {
            "كبير": "صغير",
            "صغير": "كبير",
            "طويل": "قصير",
            "قصير": "طويل",
            "سريع": "بطيء",
            "بطيء": "سريع",
            "حار": "بارد",
            "بارد": "حار",
            "نظيف": "قذر",
            "قذر": "نظيف",
            "قوي": "ضعيف",
            "ضعيف": "قوي",
            "غني": "فقير",
            "فقير": "غني",
            "سعيد": "حزين",
            "حزين": "سعيد",
            "جميل": "قبيح",
            "قبيح": "جميل",
            "صعب": "سهل",
            "سهل": "صعب",
            "ثقيل": "خفيف",
            "خفيف": "ثقيل",
            "جديد": "قديم",
            "قديم": "جديد",
            "واسع": "ضيق",
            "ضيق": "واسع",
            "عالي": "منخفض",
            "منخفض": "عالي",
            "نهار": "ليل",
            "ليل": "نهار",
            "شمس": "قمر",
            "قمر": "شمس",
            "صيف": "شتاء",
            "شتاء": "صيف",
            "ربيع": "خريف",
            "خريف": "ربيع",
            "ذكي": "غبي",
            "غبي": "ذكي",
            "شجاع": "جبان",
            "جبان": "شجاع",
            "كريم": "بخيل",
            "بخيل": "كريم",
            "أمين": "خائن",
            "خائن": "أمين",
            "صادق": "كاذب",
            "كاذب": "صادق",
            "مفيد": "ضار",
            "ضار": "مفيد",
            "ناجح": "فاشل",
            "فاشل": "ناجح",
            "حي": "ميت",
            "ميت": "حي",
            "مريض": "سليم",
            "سليم": "مريض",
            "قريب": "بعيد",
            "بعيد": "قريب",
            "داخل": "خارج",
            "خارج": "داخل",
            "فوق": "تحت",
            "تحت": "فوق",
            "أمام": "خلف",
            "خلف": "أمام",
            "مشرق": "مظلم",
            "مظلم": "مشرق",
            "مفتوح": "مغلق",
            "مغلق": "مفتوح",
            "هادئ": "صاخب",
            "صاخب": "هادئ",
            "رطب": "جاف",
            "جاف": "رطب",
            "مبلل": "جاف",
            "سميك": "رفيع",
            "رفيع": "سميك",
            "حار": "بارد",
            "قاسي": "ناعم",
            "ناعم": "قاسي",
            "مشمس": "غائم",
            "غائم": "مشمس",
            "قديم": "حديث",
            "حديث": "قديم"
        }
    
    def normalize_text(self, text):
        """تطبيع النص للمقارنة"""
        text = text.strip().lower()
        text = re.sub(r'^ال', '', text)
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ة', 'ه')
        text = text.replace('ى', 'ي')
        text = re.sub(r'[\u064B-\u065F]', '', text)
        return text
    
    def start_game(self):
        self.current_word = random.choice(list(self.opposites.keys()))
        self.correct_answer = self.opposites[self.current_word]
        
        return TextSendMessage(
            text=f"ما هو ضد:\n{self.current_word}\nاكتب الكلمة المعاكسة"
        )
    
    def check_answer(self, answer, user_id, display_name):
        if not self.current_word:
            return None
        
        user_answer = self.normalize_text(answer)
        correct_answer = self.normalize_text(self.correct_answer)
        
        if user_answer == correct_answer:
            points = 10
            msg = f"صحيح يا {display_name}!\nضد {self.current_word} = {self.correct_answer}\n+{points} نقطة"
            
            self.current_word = None
            
            return {
                'message': msg,
                'points': points,
                'won': True,
                'game_over': True,
                'response': TextSendMessage(text=msg)
            }
        else:
            return {
                'message': f"خطأ!\nالإجابة الصحيحة: {self.correct_answer}",
                'points': 0,
                'game_over': True,
                'response': TextSendMessage(text=f"خطأ!\nالإجابة الصحيحة: {self.correct_answer}")
            }
