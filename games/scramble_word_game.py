import random
import re
from linebot.models import TextSendMessage

class ScrambleWordGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_word = None
        self.scrambled_word = None
        self.used_words = set()
        self.current_hint = None
        self.current_category = None
        
        # قائمة الكلمات مع تلميحات وفئات
        self.words = [
            {"word": "مدرسة", "hint": "مكان التعليم", "category": "أماكن"},
            {"word": "كتاب", "hint": "للقراءة", "category": "أدوات"},
            {"word": "قلم", "hint": "للكتابة", "category": "أدوات"},
            {"word": "شجرة", "hint": "نبات كبير", "category": "طبيعة"},
            {"word": "سيارة", "hint": "وسيلة مواصلات", "category": "مركبات"},
            {"word": "طائرة", "hint": "تطير في السماء", "category": "مركبات"},
            {"word": "حاسوب", "hint": "جهاز إلكتروني", "category": "تكنولوجيا"},
            {"word": "هاتف", "hint": "للاتصال", "category": "تكنولوجيا"},
            {"word": "طاولة", "hint": "أثاث للأكل", "category": "أثاث"},
            {"word": "كرسي", "hint": "للجلوس", "category": "أثاث"},
            {"word": "نافذة", "hint": "للتهوية", "category": "أجزاء المنزل"},
            {"word": "باب", "hint": "مدخل", "category": "أجزاء المنزل"},
            {"word": "مفتاح", "hint": "لفتح الباب", "category": "أدوات"},
            {"word": "ساعة", "hint": "لمعرفة الوقت", "category": "أدوات"},
            {"word": "مرآة", "hint": "لرؤية نفسك", "category": "أدوات"},
            {"word": "مطبخ", "hint": "مكان الطبخ", "category": "أماكن"},
            {"word": "حديقة", "hint": "مكان الزهور", "category": "أماكن"},
            {"word": "مستشفى", "hint": "للعلاج", "category": "أماكن"},
            {"word": "مطار", "hint": "للسفر بالطائرة", "category": "أماكن"},
            {"word": "جامعة", "hint": "للدراسة العليا", "category": "أماكن"},
            {"word": "مكتبة", "hint": "مكان الكتب", "category": "أماكن"},
            {"word": "سوق", "hint": "للتسوق", "category": "أماكن"},
            {"word": "ملعب", "hint": "للرياضة", "category": "أماكن"},
            {"word": "شاطئ", "hint": "على البحر", "category": "طبيعة"},
            {"word": "جبل", "hint": "مرتفع جداً", "category": "طبيعة"},
            {"word": "نهر", "hint": "ماء جارٍ", "category": "طبيعة"},
            {"word": "صحراء", "hint": "رمال كثيرة", "category": "طبيعة"},
            {"word": "غابة", "hint": "أشجار كثيرة", "category": "طبيعة"},
            {"word": "قمر", "hint": "في السماء ليلاً", "category": "فلك"},
            {"word": "شمس", "hint": "نجم النهار", "category": "فلك"},
            {"word": "نجمة", "hint": "في السماء ليلاً", "category": "فلك"},
            {"word": "سحابة", "hint": "في السماء", "category": "طقس"},
            {"word": "مطر", "hint": "ماء من السماء", "category": "طقس"},
            {"word": "رعد", "hint": "صوت في السماء", "category": "طقس"},
            {"word": "برق", "hint": "ضوء في السماء", "category": "طقس"},
            {"word": "ثلج", "hint": "ماء متجمد", "category": "طقس"},
            {"word": "تفاحة", "hint": "فاكهة حمراء", "category": "طعام"},
            {"word": "برتقال", "hint": "فاكهة برتقالية", "category": "طعام"},
            {"word": "موز", "hint": "فاكهة صفراء", "category": "طعام"},
            {"word": "عنب", "hint": "فاكهة صغيرة", "category": "طعام"},
            # أمثلة إضافية
            {"word": "برتقالة", "hint": "فاكهة برتقالية", "category": "طعام"},
            {"word": "ليمون", "hint": "فاكهة حامضة", "category": "طعام"},
            {"word": "خيار", "hint": "خضار أخضر", "category": "طعام"},
            {"word": "فلفل", "hint": "خضار حار", "category": "طعام"},
            {"word": "بطاطس", "hint": "خضار مطبوخ", "category": "طعام"},
            {"word": "جزر", "hint": "خضار برتقالي", "category": "طعام"},
            {"word": "ليمونه", "hint": "صيغة عامية", "category": "طعام"},
            {"word": "مكتبه", "hint": "صيغة عامية", "category": "أماكن"},
            {"word": "مدرسته", "hint": "صيغة عامية", "category": "أماكن"}
        ]
    
    def normalize_text(self, text):
        text = text.strip().lower()
        text = re.sub(r'^ال', '', text)          # إزالة "ال" التعريف
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ة', 'ه')
        text = text.replace('ى', 'ي')
        text = re.sub(r'[\u064B-\u065F]', '', text)  # إزالة التشكيل
        return text
    
    def _scramble_word(self, word):
        letters = list(word)
        random.shuffle(letters)
        scrambled = ''.join(letters)
        attempts = 0
        while scrambled == word and attempts < 10:
            random.shuffle(letters)
            scrambled = ''.join(letters)
            attempts += 1
        return scrambled
    
    def start_game(self):
        available_words = [w for w in self.words if w["word"] not in self.used_words]
        if not available_words:
            self.used_words.clear()
            available_words = self.words
        
        word_data = random.choice(available_words)
        self.current_word = word_data["word"]
        self.current_hint = word_data["hint"]
        self.current_category = word_data["category"]
        self.scrambled_word = self._scramble_word(self.current_word)
        
        return TextSendMessage(
            text=f"رتب الحروف لتكوين كلمة صحيحة:\n{self.scrambled_word}\nالتلميح: {self.current_hint}"
        )
    
    def get_hint(self):
        if not self.current_word:
            return "لا يوجد سؤال حالي"
        first_letter = self.current_word[0]
        word_length = len(self.current_word)
        return f"{self.current_hint}\nالكلمة تبدأ بـ: {first_letter}\nعدد الحروف: {word_length}"
    
    def get_answer(self):
        return self.current_word if self.current_word else "لا يوجد سؤال حالي"
    
    def check_answer(self, answer, user_id, display_name):
        if not self.current_word:
            return None
        
        normalized_answer = self.normalize_text(answer)
        normalized_word = self.normalize_text(self.current_word)
        
        if normalized_answer == normalized_word:
            points = 12
            self.used_words.add(self.current_word)
            
            return self.start_game_response(points, display_name)
        else:
            return {
                'message': f"خطأ! حاول مرة أخرى\nالحروف: {self.scrambled_word}",
                'points': 0,
                'game_over': False,
                'response': TextSendMessage(text=f"خطأ! حاول مرة أخرى\nالحروف: {self.scrambled_word}")
            }
    
    def start_game_response(self, points, display_name):
        available_words = [w for w in self.words if w["word"] not in self.used_words]
        if not available_words:
            self.used_words.clear()
            available_words = self.words
        
        word_data = random.choice(available_words)
        self.current_word = word_data["word"]
        self.current_hint = word_data["hint"]
        self.current_category = word_data["category"]
        self.scrambled_word = self._scramble_word(self.current_word)
        
        msg = f"صحيح يا {display_name}! +{points}\nكلمة جديدة:\n{self.scrambled_word}\nالتلميح: {self.current_hint}"
        
        return {
            'points': points,
            'won': True,
            'response': TextSendMessage(text=msg)
        }
