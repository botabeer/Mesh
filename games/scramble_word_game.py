import random
import re
from linebot.models import TextSendMessage

class ScrambleWordGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_word = None
        self.scrambled = None
        self.used_words = set()
        self.current_question = 1
        self.max_questions = 10
        self.players_scores = {}
        self.hint_used = False
        
        # قائمة الكلمات
        self.words = [
            "مدرسة", "كتاب", "قلم", "سيارة", "طائرة", "حاسوب",
            "مستشفى", "معلم", "طالب", "شجرة", "زهرة", "نهر",
            "جبل", "بحر", "سماء", "شمس", "قمر", "نجم",
            "مكتبة", "صديق", "عائلة", "طعام", "ماء", "هواء",
            "تلفاز", "هاتف", "ساعة", "باب", "نافذة", "سرير",
            "فراشة", "عصفور", "حمامة", "أرنب", "سمكة", "قطة",
            "حديقة", "مطبخ", "غرفة", "صالة", "حمام", "سطح"
        ]
    
    def normalize_text(self, text):
        """تطبيع النص للمقارنة"""
        text = text.strip().lower()
        text = re.sub(r'^ال', '', text)
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ة', 'ه')
        text = text.replace('ى', 'ي')
        text = re.sub(r'[\u064B-\u065F]', '', text)
        return text
    
    def scramble_word(self, word):
        """خلط حروف الكلمة"""
        letters = list(word)
        random.shuffle(letters)
        scrambled = ''.join(letters)
        
        if scrambled == word:
            random.shuffle(letters)
            scrambled = ''.join(letters)
        
        return scrambled
    
    def start_game(self):
        self.current_question = 1
        self.players_scores = {}
        self.used_words.clear()
        return self.next_question()
    
    def next_question(self):
        """الانتقال للسؤال التالي"""
        if self.current_question > self.max_questions:
            return self.end_game()
        
        available_words = [w for w in self.words if w not in self.used_words]
        
        if not available_words:
            self.used_words.clear()
            available_words = self.words
        
        self.current_word = random.choice(available_words)
        self.used_words.add(self.current_word)
        self.scrambled = self.scramble_word(self.current_word)
        self.hint_used = False
        
        return TextSendMessage(
            text=f"السؤال {self.current_question}/{self.max_questions}\n\nحروف مبعثرة:\n{self.scrambled}\n\nرتب الحروف"
        )
    
    def get_hint(self):
        """الحصول على تلميح"""
        if self.hint_used:
            return TextSendMessage(text="تم استخدام التلميح مسبقاً")
        
        self.hint_used = True
        first_two = self.current_word[:2]
        hint = f"تبدأ بـ: {first_two}"
        
        return TextSendMessage(text=f"تلميح:\n{hint}")
    
    def show_answer(self):
        """عرض الإجابة الصحيحة"""
        msg = f"الإجابة الصحيحة: {self.current_word}"
        
        self.current_question += 1
        
        if self.current_question <= self.max_questions:
            return self.next_question()
        else:
            return self.end_game()
    
    def end_game(self):
        """إنهاء اللعبة وعرض النتائج"""
        if not self.players_scores:
            return TextSendMessage(text="انتهت اللعبة\nلم يشارك أحد")
        
        sorted_players = sorted(self.players_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        msg = "النتائج النهائية\n\n"
        for i, (name, data) in enumerate(sorted_players[:5], 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"  {i}."
            msg += f"{emoji} {name}: {data['score']} نقطة\n"
        
        winner = sorted_players[0]
        msg += f"\nالفائز: {winner[0]}"
        
        return TextSendMessage(text=msg)
    
    def check_answer(self, answer, user_id, display_name):
        if not self.current_word:
            return None
        
        # التحقق من أوامر التلميح والإجابة
        if answer == 'لمح':
            return {
                'message': '',
                'points': 0,
                'game_over': False,
                'response': self.get_hint()
            }
        
        if answer == 'جاوب':
            return {
                'message': '',
                'points': 0,
                'game_over': self.current_question > self.max_questions,
                'response': self.show_answer()
            }
        
        user_answer = self.normalize_text(answer)
        correct_answer = self.normalize_text(self.current_word)
        
        if user_answer == correct_answer:
            points = 10 if not self.hint_used else 5
            
            if display_name not in self.players_scores:
                self.players_scores[display_name] = {'score': 0}
            self.players_scores[display_name]['score'] += points
            
            msg = f"صحيح يا {display_name}\n+{points} نقطة"
            
            self.current_question += 1
            
            if self.current_question <= self.max_questions:
                next_q = self.next_question()
                return {
                    'message': msg,
                    'points': points,
                    'won': True,
                    'game_over': False,
                    'response': TextSendMessage(text=f"{msg}\n\n{next_q.text}")
                }
            else:
                end_msg = self.end_game()
                return {
                    'message': msg,
                    'points': points,
                    'won': True,
                    'game_over': True,
                    'response': TextSendMessage(text=f"{msg}\n\n{end_msg.text}")
                }
        
        return None
