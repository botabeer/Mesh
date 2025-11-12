import random
import re
from linebot.models import TextSendMessage

class GuessGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_word = None
        self.hint = None
        self.category = None
        self.first_letter = None
        self.current_question = 1
        self.max_questions = 10
        self.players_scores = {}
        self.hint_used = False
        
        # قائمة الألغاز
        self.riddles = [
            {"category": "المطبخ", "answer": "قدر", "first_letter": "ق"},
            {"category": "المطبخ", "answer": "ملعقة", "first_letter": "م"},
            {"category": "المطبخ", "answer": "سكين", "first_letter": "س"},
            {"category": "المطبخ", "answer": "طنجرة", "first_letter": "ط"},
            {"category": "المطبخ", "answer": "كوب", "first_letter": "ك"},
            {"category": "المطبخ", "answer": "صحن", "first_letter": "ص"},
            {"category": "المطبخ", "answer": "فرن", "first_letter": "ف"},
            {"category": "المطبخ", "answer": "ثلاجة", "first_letter": "ث"},
            {"category": "المطبخ", "answer": "خلاط", "first_letter": "خ"},
            {"category": "المطبخ", "answer": "مقلاة", "first_letter": "م"},
            {"category": "المدرسة", "answer": "مسطرة", "first_letter": "م"},
            {"category": "المدرسة", "answer": "قلم", "first_letter": "ق"},
            {"category": "المدرسة", "answer": "كتاب", "first_letter": "ك"},
            {"category": "المدرسة", "answer": "دفتر", "first_letter": "د"},
            {"category": "المدرسة", "answer": "ممحاة", "first_letter": "م"},
            {"category": "المدرسة", "answer": "شنطة", "first_letter": "ش"},
            {"category": "المدرسة", "answer": "طاولة", "first_letter": "ط"},
            {"category": "المدرسة", "answer": "سبورة", "first_letter": "س"},
            {"category": "المدرسة", "answer": "براية", "first_letter": "ب"},
            {"category": "المدرسة", "answer": "حقيبة", "first_letter": "ح"},
            {"category": "البيت", "answer": "باب", "first_letter": "ب"},
            {"category": "البيت", "answer": "نافذة", "first_letter": "ن"},
            {"category": "البيت", "answer": "سرير", "first_letter": "س"},
            {"category": "البيت", "answer": "كرسي", "first_letter": "ك"},
            {"category": "البيت", "answer": "مرآة", "first_letter": "م"},
            {"category": "البيت", "answer": "تلفاز", "first_letter": "ت"},
            {"category": "البيت", "answer": "ساعة", "first_letter": "س"},
            {"category": "البيت", "answer": "مكتب", "first_letter": "م"},
            {"category": "الشارع", "answer": "سيارة", "first_letter": "س"},
            {"category": "الشارع", "answer": "إشارة", "first_letter": "ا"},
            {"category": "الشارع", "answer": "رصيف", "first_letter": "ر"},
            {"category": "الشارع", "answer": "شجرة", "first_letter": "ش"},
            {"category": "الشارع", "answer": "دراجة", "first_letter": "د"},
            {"category": "الشارع", "answer": "حافلة", "first_letter": "ح"},
            {"category": "المستشفى", "answer": "سرير", "first_letter": "س"},
            {"category": "المستشفى", "answer": "حقنة", "first_letter": "ح"},
            {"category": "المستشفى", "answer": "دواء", "first_letter": "د"},
            {"category": "المستشفى", "answer": "كرسي", "first_letter": "ك"},
            {"category": "المستشفى", "answer": "ميزان", "first_letter": "م"},
            {"category": "الملابس", "answer": "قميص", "first_letter": "ق"},
            {"category": "الملابس", "answer": "بنطال", "first_letter": "ب"},
            {"category": "الملابس", "answer": "حذاء", "first_letter": "ح"},
            {"category": "الملابس", "answer": "جورب", "first_letter": "ج"},
            {"category": "الملابس", "answer": "معطف", "first_letter": "م"},
            {"category": "الملابس", "answer": "طاقية", "first_letter": "ط"},
            {"category": "الملابس", "answer": "عباءة", "first_letter": "ع"}
        ]
    
    def normalize_text(self, text):
        text = text.strip().lower()
        text = re.sub(r'^ال', '', text)
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ة', 'ه')
        text = text.replace('ى', 'ي')
        text = re.sub(r'[\u064B-\u065F]', '', text)
        return text
    
    def start_game(self):
        self.current_question = 1
        self.players_scores = {}
        return self.next_question()
    
    def next_question(self):
        riddle = random.choice(self.riddles)
        self.current_word = riddle["answer"].lower()
        self.category = riddle["category"]
        self.first_letter = riddle["first_letter"]
        self.hint_used = False
        
        return TextSendMessage(
            text=f"شيء في {self.category}\nيبدأ بحرف: {self.first_letter}\nما هو؟"
        )
    
    def get_hint(self):
        """تلميح متقدم: عدد الأحرف، أول حرفين، ومثال مشابه"""
        if self.hint_used:
            return TextSendMessage(text="تم استخدام التلميح مسبقاً")
        
        self.hint_used = True
        hint_parts = [f"عدد الأحرف: {len(self.current_word)}"]
        
        if len(self.current_word) > 2:
            hint_parts.append(f"تبدأ بـ: {self.current_word[:2]}")
        else:
            hint_parts.append(f"تبدأ بـ: {self.current_word[0]}")
        
        similar_words = [r["answer"] for r in self.riddles if r["category"] == self.category and r["answer"] != self.current_word]
        if similar_words:
            example = random.choice(similar_words)
            hint_parts.append(f"مثال مشابه: {example}")
        
        hint_text = " | ".join(hint_parts)
        return TextSendMessage(text=f"تلميح:\n{hint_text}")
    
    def show_answer(self):
        msg = f"الإجابة الصحيحة: {self.current_word}"
        self.current_question += 1
        
        if self.current_question <= self.max_questions:
            return self.next_question()
        else:
            return self.end_game()
    
    def end_game(self):
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
