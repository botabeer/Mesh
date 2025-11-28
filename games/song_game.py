"""
لعبة تخمين الأغنية - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class SongGame(BaseGame):
    """لعبة تخمين الأغنية"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "أغنية"
        self.game_icon = "🎵"

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
            {'lyrics': 'سيبك من الكلام ده وتعالى', 'artist': 'محمد منير'},
            {'lyrics': 'نفسي أشوفك كل يوم', 'artist': 'حسين الجسمي'},
            {'lyrics': 'يا طير يا طاير يا رايح لبلاد الحب', 'artist': 'راشد الماجد'},
            {'lyrics': 'عيونك يا حبيبي خطفت عقلي', 'artist': 'أنغام'},
            {'lyrics': 'سهران لوحدي والليل صاحبي', 'artist': 'ماجد المهندس'}
        ]
        random.shuffle(self.songs)
        self.used_songs = []

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.used_songs = []
        return self.get_question()

    def get_question(self):
        available = [s for s in self.songs if s not in self.used_songs]
        if not available:
            self.used_songs = []
            available = self.songs.copy()
        
        q_data = random.choice(available)
        self.used_songs.append(q_data)
        self.current_answer = q_data['artist']

        colors = self.get_theme_colors()
        
        # قسم السؤال السابق
        previous_section = []
        if self.previous_question and self.previous_answer:
            previous_section = [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "الأغنية السابقة:", "size": "xs", "color": colors["text2"], "weight": "bold"},
                        {"type": "text", "text": self.previous_question, "size": "xs", "color": colors["text2"], "wrap": True, "margin": "xs"},
                        {"type": "text", "text": f"✅ المغني: {self.previous_answer}", "size": "xs", "color": colors["success"], "wrap": True, "margin": "xs"}
                    ],
                    "backgroundColor": colors["card"],
                    "cornerRadius": "15px",
                    "paddingAll": "12px",
                    "margin": "md"
                },
                {"type": "separator", "color": colors["shadow1"], "margin": "md"}
            ]

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # Header
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": self.game_name, "size": "xxl", "weight": "bold", "color": colors["text"], "align": "center"},
                            {"type": "text", "text": f"سؤال {self.current_question + 1} من {self.questions_count}", "size": "sm", "color": colors["text2"], "align": "center", "margin": "sm"}
                        ],
                        "spacing": "xs",
                        "margin": "none",
                        "paddingAll": "0px"
                    },
                    {"type": "separator", "margin": "xl", "color": colors["shadow1"]}
                ] + previous_section + [
                    # محتوى السؤال
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "🎤 من المغني؟", "size": "md", "color": colors["text"], "align": "center", "wrap": True, "weight": "bold"},
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": q_data["lyrics"], "size": "lg", "color": colors["primary"], "align": "center", "wrap": True, "weight": "bold"}
                                ],
                                "backgroundColor": colors["card"],
                                "cornerRadius": "15px",
                                "paddingAll": "20px",
                                "margin": "md"
                            }
                        ],
                        "spacing": "md",
                        "margin": "xl"
                    },
                    {"type": "text", "text": "💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة", "size": "xs", "color": colors["text2"], "align": "center", "wrap": True, "margin": "lg"},
                    # الأزرار
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "لمح", "text": "لمح"}, "style": "secondary", "height": "sm", "color": colors["shadow1"]},
                            {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "secondary", "height": "sm", "color": colors["shadow1"]}
                        ],
                        "margin": "xl"
                    },
                    {"type": "button", "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"}, "style": "primary", "height": "sm", "color": colors["error"], "margin": "sm"}
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "24px",
                "spacing": "none"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }
        
        return self._create_flex_with_buttons("أغنية", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str):
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if normalized == 'لمح':
            hint = f"💡 اسم المغني يبدأ بحرف '{self.current_answer[0]}'"
            return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}

        if normalized == 'جاوب':
            reveal = f"🎤 المغني: {self.current_answer}"
            self.previous_question = self.used_songs[-1]['lyrics']
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result

            return {'message': reveal, 'response': self.get_question(), 'points': 0}

        # التحقق من الإجابة
        normalized_correct = self.normalize_text(self.current_answer)
        if normalized == normalized_correct or normalized in normalized_correct or normalized_correct in normalized:
            points = self.add_score(user_id, display_name, 10)
            self.previous_question = self.used_songs[-1]['lyrics']
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ صحيح يا {display_name}!\n🎤 {self.current_answer}\n+{points} نقطة\n\n{result.get('message', '')}"
                return result

            return {
                'message': f"✅ صحيح يا {display_name}!\n🎤 {self.current_answer}\n+{points} نقطة",
                'response': self.get_question(),
                'points': points
            }

        return {'message': "❌ إجابة غير صحيحة", 'response': self._create_text_message("❌ إجابة غير صحيحة"), 'points': 0}
