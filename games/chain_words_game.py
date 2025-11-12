import random
from linebot.models import TextSendMessage

class ChainWordsGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_word = None
        self.used_words = set()
        self.current_question = 1
        self.max_questions = 10
        self.players_scores = {}
        self.hint_used = False
        
        # كلمات البداية
        self.start_words = [
            "سيارة", "قمر", "شمس", "كتاب", "مدرسة", "بيت",
            "طائر", "نهر", "جبل", "زهرة", "سحاب", "مطر",
            "حديقة", "مكتب", "سرير", "باب", "نافذة", "ساعة"
        ]
    
    def normalize_letter(self, letter):
        """تحويل الحروف الخاصة لحروف قياسية"""
        if letter in ['ة', 'ه']:
            return 'ه'
        elif letter in ['ء', 'ؤ', 'ئ', 'ى']:
            return 'ا'
        elif letter in ['أ', 'إ', 'آ']:
            return 'ا'
        return letter
    
    def start_game(self):
        self.current_question = 1
        self.players_scores = {}
        self.used_words.clear()
        return self.next_question()
    
    def next_question(self):
        """الانتقال للسؤال التالي بدون ترقيم"""
        if self.current_question > self.max_questions:
            return self.end_game()
        
        if self.current_question == 1:
            self.current_word = random.choice(self.start_words)
            self.used_words.add(self.current_word.lower())
        
        last_letter = self.normalize_letter(self.current_word[-1])
        self.hint_used = False
        
        return TextSendMessage(
            text=f"الكلمة: {self.current_word}\nاكتب كلمة تبدأ بحرف: {last_letter}"
        )
    
    def get_hint(self):
        """الحصول على تلميح"""
        if self.hint_used:
            return TextSendMessage(text="تم استخدام التلميح مسبقاً")
        
        self.hint_used = True
        last_letter = self.normalize_letter(self.current_word[-1])
        hint = f"ابدأ بحرف: {last_letter}\nتجنب الكلمات المستخدمة"
        
        return TextSendMessage(text=f"تلميح:\n{hint}")
    
    def show_answer(self):
        """عرض كلمة مقترحة بدون ترقيم"""
        last_letter = self.normalize_letter(self.current_word[-1])
        suggestions = {
            'ا': ['أمل', 'إبراهيم', 'أحمد'],
            'م': ['محمد', 'مريم', 'مدرسة'],
            'ه': ['هاتف', 'هدية', 'هند'],
            'س': ['سيارة', 'سماء', 'سعيد'],
            'ر': ['رمان', 'رياض', 'رسالة'],
            'ب': ['بيت', 'باب', 'بحر'],
            'ن': ['نهر', 'نور', 'نافذة'],
            'ل': ['ليمون', 'ليل', 'لبن']
        }
        
        suggested = suggestions.get(last_letter, [f'كلمة بحرف {last_letter}'])
        msg = f"أمثلة:\n{', '.join(suggested)}"
        
        self.current_question += 1
        
        if self.current_question <= self.max_questions:
            next_q = self.next_question()
            return TextSendMessage(text=f"{msg}\n\n{next_q.text}")
        else:
            end_msg = self.end_game()
            return TextSendMessage(text=f"{msg}\n\n{end_msg.text}")
    
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
        
        user_word = answer.strip()
        user_word_lower = user_word.lower()
        
        # التحقق من التكرار
        if user_word_lower in self.used_words:
            return {
                'message': f"الكلمة '{user_word}' مستخدمة مسبقاً",
                'points': 0,
                'game_over': False,
                'response': TextSendMessage(text=f"الكلمة '{user_word}' مستخدمة مسبقاً")
            }
        
        # التحقق من الحرف الأول
        last_letter = self.normalize_letter(self.current_word[-1])
        first_letter = self.normalize_letter(user_word[0])
        
        if first_letter != last_letter:
            return {
                'message': f"يجب أن تبدأ بحرف: {last_letter}",
                'points': 0,
                'game_over': False,
                'response': TextSendMessage(text=f"يجب أن تبدأ بحرف: {last_letter}")
            }
        
        # إجابة صحيحة
        self.used_words.add(user_word_lower)
        self.current_word = user_word
        points = 10 if not self.hint_used else 5
        
        if display_name not in self.players_scores:
            self.players_scores[display_name] = {'score': 0}
        self.players_scores[display_name]['score'] += points
        
        msg = f"صحيح يا {display_name}"
        
        self.current_question += 1
        
        if self.current_question <= self.max_questions:
            next_q = self.next_question()
            return {
                'message': msg,
                'points': points,
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
