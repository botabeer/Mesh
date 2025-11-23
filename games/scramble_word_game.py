"""
لعبة ترتيب الحروف - محسنة
Created by: Abeer Aldosari © 2025
"""
from .base_game import BaseGame
import random
import difflib
from config import POINTS_PER_CORRECT, POINTS_PER_WIN

class ScrambleWordGame(BaseGame):
    def __init__(self, line_api):
        super().__init__(line_api, rounds=10)
        self.words_list = [
            {"word": "مدرسة", "hint": "مكان للتعليم"},
            {"word": "كتاب", "hint": "نقرأ فيه"},
            {"word": "حاسوب", "hint": "جهاز إلكتروني"},
            {"word": "هاتف", "hint": "نستخدمه للاتصال"},
            {"word": "مطبخ", "hint": "نطبخ فيه"},
            {"word": "سيارة", "hint": "وسيلة مواصلات"},
            {"word": "طائرة", "hint": "تطير في السماء"},
            {"word": "حديقة", "hint": "مكان فيه أشجار"},
            {"word": "مستشفى", "hint": "نذهب إليه عند المرض"},
            {"word": "مكتبة", "hint": "مكان للكتب"}
        ]
        random.shuffle(self.words_list)

    def scramble_word(self, word):
        letters = list(word)
        scrambled = letters.copy()
        attempts = 10
        while scrambled == letters and attempts > 0:
            random.shuffle(scrambled)
            attempts -= 1
        return ''.join(scrambled)

    def start_game(self):
        self.current_round = 0
        return self.generate_question()

    def generate_question(self):
        word_data = self.words_list[self.current_round % len(self.words_list)]
        self.current_answer = word_data['word']
        self.current_hint = word_data['hint']
        scrambled = self.scramble_word(self.current_answer)
        
        question = f"رتب الحروف:\n\n{' - '.join(scrambled)}"
        extra_info = "💡 لمح: للحصول على تلميح\n• جاوب: لمعرفة الإجابة"
        
        return self.build_question_flex("ترتيب الحروف 🔤", question, extra_info)

    def check_answer(self, answer, uid, name):
        normalized = self.normalize_text(answer)
        
        if normalized == 'لمح':
            hint = f"💡 {self.current_hint}"
            return {'points': 0, 'won': False, 'response': self.build_question_flex("ترتيب الحروف 🔤", hint, "رتب الحروف")}
        
        if normalized in ['جاوب', 'تم', 'التالي']:
            self.current_round += 1
            is_final = self.current_round >= self.rounds
            if is_final:
                return {'points': 0, 'won': False, 'response': self.build_result_flex("انتهت اللعبة", f"الإجابة: {self.current_answer}", 0, True)}
            return {'points': 0, 'won': False, 'response': self.generate_question()}
        
        correct_normalized = self.normalize_text(self.current_answer)
        if normalized == correct_normalized or difflib.SequenceMatcher(None, normalized, correct_normalized).ratio() > 0.8:
            points = POINTS_PER_CORRECT
            self.add_player_score(uid, points)
            self.current_round += 1
            is_final = self.current_round >= self.rounds
            
            if is_final:
                return {'points': points, 'won': True, 'response': self.build_result_flex(name, self.current_answer, points, True)}
            return {'points': points, 'won': False, 'response': self.generate_question()}
        
        return None
