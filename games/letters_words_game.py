"""
لعبة تكوين الكلمات - Neumorphism Edition
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional

class LettersWordsGame(BaseGame):
    """لعبة تكوين كلمات من حروف معينة"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.supports_hint = True
        self.supports_reveal = True
        
        self.letter_sets = [
            {"letters": ["ق", "ل", "م", "ع", "ر", "ب"], "words": ["قلم", "عمل", "علم", "قلب", "رقم", "مقر"]},
            {"letters": ["س", "ا", "ر", "ة", "ي", "م"], "words": ["سيارة", "سارية", "رئيس", "سير", "مسار"]},
            {"letters": ["ك", "ت", "ا", "ب", "م", "ل"], "words": ["كتاب", "كتب", "مكتب", "كلام", "ملك"]},
            {"letters": ["د", "ر", "س", "ة", "م", "ا"], "words": ["مدرسة", "درس", "مدرس", "سادر"]},
            {"letters": ["ح", "د", "ي", "ق", "ة", "ر"], "words": ["حديقة", "حديد", "قرد", "دقيق"]}
        ]
        random.shuffle(self.letter_sets)
        self.current_set = None
        self.found_words = set()
        self.required_words = 3

    def start_game(self) -> Any:
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.found_words.clear()
        return self.get_question()

    def get_question(self) -> Any:
        """إنشاء Flex Message للسؤال"""
        colors = self.get_theme_colors()
        self.current_set = self.letter_sets[self.current_question % len(self.letter_sets)]
        self.current_answer = self.current_set["words"]
        self.found_words.clear()
        
        letters_display = ' - '.join(self.current_set["letters"])
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "تكوين الكلمات", "size": "xl", "weight": "bold",
                     "color": colors["text"], "align": "center"},
                    {"type": "text", "text": f"سؤال {self.current_question+1} من {self.questions_count}",
                     "size": "sm", "color": colors["text2"], "align": "center"}
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
                "contents": [
                    {"type": "text", "text": "استخدم الحروف التالية لتكوين الكلمات:", "size": "md",
                     "color": colors["text"], "align": "center", "wrap": True},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": letters_display, "size": "xl", "weight": "bold",
                             "color": colors["primary"], "align": "center", "wrap": True}
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px"
                    },
                    {"type": "text", "text": f"يجب إيجاد {self.required_words} كلمات", "size": "sm",
                     "color": colors["text2"], "align": "center"}
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }
        return self._create_flex_with_buttons("تكوين الكلمات", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        answer = user_answer.strip()
        normalized = self.normalize_text(answer)

        # التلميح
        if normalized == 'لمح':
            remaining = [w for w in self.current_answer if self.normalize_text(w) not in self.found_words]
            if remaining:
                word = remaining[0]
                hint = f"تلميح: الكلمة من {len(word)} حروف وأولها '{word[0]}'"
            else:
                hint = "لا توجد تلميحات"
            return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

        # كشف الإجابة
        if normalized == 'جاوب':
            words = " • ".join(self.current_answer)
            msg = f"الكلمات الممكنة:\n{words}"
            next_q = self.next_question()
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['message'] = f"{msg}\n\n{next_q.get('message','')}"
                return next_q
            return {'message': msg, 'response': next_q, 'points': 0}

        # التحقق من الإجابة
        valid_words = [self.normalize_text(w) for w in self.current_answer]
        is_valid = False
        
        if normalized in valid_words and normalized not in self.found_words:
            is_valid = True
        else:
            for w in valid_words:
                if difflib.SequenceMatcher(None, normalized, w).ratio() > 0.8:
                    is_valid = True
                    break

        if not is_valid:
            return {'message': "إجابة غير صحيحة",
                    'response': self._create_text_message("إجابة غير صحيحة"),
                    'points': 0}

        self.found_words.add(normalized)
        points = self.add_score(user_id, display_name, 10)

        if len(self.found_words) >= self.required_words:
            next_q = self.next_question()
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                next_q['message'] = f"أحسنت يا {display_name}!\n+{points} نقطة\n\n{next_q.get('message','')}"
                return next_q
            return {'message': f"أحسنت يا {display_name}!\n+{points} نقطة", 
                    'response': next_q, 'points': points}

        remaining = self.required_words - len(self.found_words)
        msg = f"صحيح!\n+{points} نقطة\nتبقى {remaining} كلمات"
        return {'message': msg, 'response': self._create_text_message(msg), 'points': points}

    def get_game_info(self) -> Dict[str, Any]:
        return {
            "name": "لعبة تكوين الكلمات",
            "description": "كوّن كلمات من الحروف المعطاة",
            "questions_count": self.questions_count,
            "required_words": self.required_words,
            "found_words_count": len(self.found_words),
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }
