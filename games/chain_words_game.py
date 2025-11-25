"""
لعبة سلسلة الكلمات - النسخة المحسنة النهائية
Created by: Abeer Aldosari © 2025

الميزات:
✅ AI أولاً مع Fallback قوي
✅ تتبع الكلمات المستخدمة
✅ واجهة Flex احترافية
✅ تشفير عربي مثالي
✅ بدون دعم لمح/جاوب (طبيعة اللعبة)
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class ChainWordsGame(BaseGame):
    """لعبة سلسلة الكلمات المحسنة"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "سلسلة كلمات"
        self.game_icon = "🔗"
        self.supports_hint = False
        self.supports_reveal = False
        
        self.starting_words = [
            "سيارة", "تفاح", "قلم", "نجم", "كتاب", "باب", "رمل", 
            "لعبة", "حديقة", "ورد", "دفتر", "معلم", "منزل", "شمس",
            "سفر", "رياضة", "علم", "مدرسة", "طائرة", "عصير"
        ]
        self.last_word = None
        self.used_words = set()

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.last_word = random.choice(self.starting_words)
        self.used_words.add(self.normalize_text(self.last_word))
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        """إنشاء سؤال مع واجهة Flex محسنة"""
        colors = self.get_theme_colors()
        required_letter = self.last_word[-1]

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{self.game_icon} {self.game_name}",
                        "size": "xl",
                        "weight": "bold",
                        "color": colors["text"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"سؤال {self.current_question + 1} من {self.questions_count}",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "xs"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📝 الكلمة السابقة:",
                                "size": "sm",
                                "color": colors["text2"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": self.last_word,
                                "size": "xxl",
                                "weight": "bold",
                                "color": colors["primary"],
                                "align": "center",
                                "margin": "md"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🔤 اكتب كلمة تبدأ بحرف:",
                                "size": "md",
                                "color": colors["text"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": required_letter,
                                "size": "xxl",
                                "weight": "bold",
                                "color": colors["primary"],
                                "align": "center",
                                "margin": "sm"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "⚠️ لا تكرر الكلمات",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "md"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                        "style": "primary",
                        "height": "sm",
                        "color": colors["error"]
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }

        return self._create_flex_with_buttons("سلسلة الكلمات", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """التحقق من إجابة اللاعب"""
        if not self.game_active:
            return None

        normalized_answer = self.normalize_text(user_answer)

        # رفض أوامر لمح/جاوب
        if normalized_answer in ['لمح', 'جاوب']:
            msg = "❌ هذه اللعبة لا تدعم التلميحات"
            return {
                'message': msg,
                'response': self._create_text_message(msg),
                'points': 0
            }

        # التحقق من التكرار
        if normalized_answer in self.used_words:
            msg = f"❌ الكلمة '{user_answer}' مستخدمة من قبل!"
            return {
                'message': msg,
                'response': self._create_text_message(msg),
                'points': 0
            }

        # التحقق من الحرف الأول
        required_letter = self.normalize_text(self.last_word[-1])
        if normalized_answer and normalized_answer[0] == required_letter and len(normalized_answer) >= 2:
            self.used_words.add(normalized_answer)
            self.last_word = user_answer.strip()
            points = self.add_score(user_id, display_name, 10)
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ ممتاز يا {display_name}!\n+{points} نقطة\n\n{result.get('message', '')}"
                return result

            next_q = self.get_question()
            message = f"✅ ممتاز يا {display_name}!\n+{points} نقطة"
            return {
                'message': message,
                'response': next_q,
                'points': points
            }

        return {
            "message": f"❌ الكلمة يجب أن تبدأ بحرف '{required_letter}' وأن لا تكون مكررة",
            "response": self._create_text_message(f"❌ الكلمة يجب أن تبدأ بحرف '{required_letter}' وأن لا تكون مكررة"),
            "points": 0
        }

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة سلسلة الكلمات",
            "emoji": "🔗",
            "description": "اكتب كلمة تبدأ بحرف آخر كلمة",
            "questions_count": self.questions_count,
            "supports_hint": False,
            "supports_reveal": False,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "words_count": len(self.starting_words)
        }
