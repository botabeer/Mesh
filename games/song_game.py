"""
لعبة تخمين الأغنية - Neumorphism Soft مع أزرار تفاعلية
Created by: Abeer Aldosari © 2025

تحديثات:
- Flex Message Neumorphism
- ثيمات ديناميكية
- أزرار: لمّح / جاوب
- تتبع النقاط لكل لاعب
"""
from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional

class SongGame(BaseGame):
    """لعبة تخمين المغني - Flex + Buttons Version"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.supports_hint = True
        self.supports_reveal = True
        self.songs = [
            {'lyrics': 'رجعت لي أيام الماضي معاك', 'artist': 'أم كلثوم'},
            {'lyrics': 'جلست والخوف بعينيها تتأمل فنجاني', 'artist': 'عبد الحليم حافظ'},
            {'lyrics': 'تملي معاك ولو حتى بعيد عني', 'artist': 'عمرو دياب'},
            {'lyrics': 'يا بنات يا بنات', 'artist': 'نانسي عجرم'},
            {'lyrics': 'قولي أحبك كي تزيد وسامتي', 'artist': 'كاظم الساهر'},
            {'lyrics': 'أنا لحبيبي وحبيبي إلي', 'artist': 'فيروز'},
            {'lyrics': 'حبيبي يا كل الحياة اوعدني تبقى معايا', 'artist': 'تامر حسني'},
            {'lyrics': 'قلبي بيسألني عنك دخلك طمني وينك', 'artist': 'وائل كفوري'},
            {'lyrics': 'كيف أبيّن لك شعوري دون ما أحكي', 'artist': 'عايض'},
            {'lyrics': 'محد غيرك شغل عقلي شغل بالي', 'artist': 'وليد الشامي'},
        ]
        random.shuffle(self.songs)
        self.current_answer = None

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def get_question(self) -> Any:
        colors = self.get_theme_colors()
        song = self.songs[self.current_question % len(self.songs)]
        self.current_answer = song['artist']
        progress = self.current_question + 1

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🎵 لعبة تخمين الأغنية", "size": "xl",
                     "weight": "bold", "color": colors["text"], "align": "center"},
                    {"type": "text", "text": f"السؤال {progress}/{self.questions_count}",
                     "size": "sm", "color": colors["text2"], "align": "center", "margin": "xs"}
                ],
                "backgroundColor": colors["bg"], "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": song["lyrics"], "size": "lg",
                     "weight": "bold", "color": colors["text"], "align": "center", "wrap": True, "margin": "md"},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "💡 لمّح", "text": "لمح"},
                             "style": "primary", "color": colors["primary"]},
                            {"type": "button", "action": {"type": "message", "label": "🎤 جاوب", "text": "جاوب"},
                             "style": "secondary", "color": colors["secondary"]}
                        ],
                        "spacing": "md",
                        "margin": "md"
                    }
                ],
                "backgroundColor": colors["bg"], "paddingAll": "15px"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }

        return self._create_flex_with_buttons("تخمين الأغنية", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer.strip())

        # تلميح
        if normalized == 'لمح':
            hint = f"💡 تلميح: اسم المغني يبدأ بحرف '{self.current_answer[0]}'"
            return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

        # كشف الإجابة
        if normalized == 'جاوب':
            reveal = f"🎤 المغني: {self.current_answer}"
            next_q = self.next_question()
            return {"message": reveal, "response": self._create_text_message(f"{reveal}\n\n{next_q}"), "points": 0}

        # التحقق من الإجابة
        correct = self.normalize_text(self.current_answer)
        if correct in normalized or normalized in correct or difflib.SequenceMatcher(None, normalized, correct).ratio() > 0.8:
            points = self.add_score(user_id, display_name, 10)
            next_q = self.next_question()
            msg = f"✅ صحيح يا {display_name}!\n🎤 {self.current_answer}\n+{points} نقطة"
            return {'message': msg, 'response': next_q, 'points': points}

        msg = "▫️ إجابة غير صحيحة ▪️"
        return {'message': msg, 'response': self._create_text_message(msg), 'points': 0}

    def get_game_info(self) -> Dict[str, Any]:
        return {
            "name": "لعبة تخمين الأغنية",
            "emoji": "▫️▪️",
            "description": "خمن المغني بناءً على كلمات الأغنية",
            "questions_count": self.questions_count,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }

# ============================================================================
# مثال على الاستخدام
# ============================================================================
if __name__ == "__main__":
    print("✅ ملف لعبة تخمين الأغنية جاهز للاستخدام مع أزرار تفاعلية!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
