"""
لعبة تخمين الأغنية - Neumorphism Soft with Dynamic Themes
Created by: Abeer Aldosari © 2025
"""
from .base_game import BaseGame
import random
import difflib


class SongGame(BaseGame):
    """لعبة تخمين المغني مع ثيمات ديناميكية"""
    
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

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()
    
    def get_question(self):
        """إنشاء سؤال بستايل Neumorphism Soft"""
        song = self.songs[self.current_question % len(self.songs)]
        self.current_answer = song["artist"]
        colors = self.get_theme_colors()
        progress = self.current_question + 1

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "🎵",
                                        "size": "xl",
                                        "align": "center"
                                    }
                                ],
                                "backgroundColor": colors["card"],
                                "cornerRadius": "15px",
                                "width": "45px",
                                "height": "45px",
                                "justifyContent": "center"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "لعبة الأغنية",
                                        "size": "xl",
                                        "weight": "bold",
                                        "color": colors["text"]
                                    },
                                    {
                                        "type": "text",
                                        "text": f"السؤال {progress}/{self.questions_count}",
                                        "size": "sm",
                                        "color": colors["text2"]
                                    }
                                ],
                                "margin": "lg",
                                "flex": 1
                            }
                        ]
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
                                "text": song["lyrics"],
                                "size": "lg",
                                "weight": "bold",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px",
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": "من المغني؟",
                        "size": "md",
                        "color": colors["primary"],
                        "align": "center",
                        "margin": "xl",
                        "weight": "bold"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "backgroundColor": colors["primary"],
                                "height": "5px",
                                "flex": progress,
                                "cornerRadius": "3px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "backgroundColor": colors["card"],
                                "height": "5px",
                                "flex": self.questions_count - progress,
                                "cornerRadius": "3px"
                            }
                        ],
                        "margin": "md"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                }
            }
        }
        
        return self._create_flex_with_buttons("لعبة الأغنية", flex_content)

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None
        if user_id in self.answered_users:
            return None

        answer = user_answer.strip()
        normalized = self.normalize_text(answer)
        
        # تلميح
        if normalized == 'لمح':
            hint = self.get_hint()
            return {'message': hint, 'response': self._create_text_message(hint), 'points': 0}
        
        # كشف الإجابة
        if normalized == 'جاوب':
            song = self.songs[self.current_question % len(self.songs)]
            reveal = f"🎤 المغني: {song['artist']}"
            next_q = self.next_question()
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['message'] = f"{reveal}\n\n{next_q.get('message','')}"
                return next_q
            return {'message': reveal, 'response': next_q, 'points': 0}

        # التحقق من الإجابة
        correct = self.normalize_text(self.current_answer)
        if correct in normalized or normalized in correct or \
           difflib.SequenceMatcher(None, normalized, correct).ratio() > 0.8:
            points = self.add_score(user_id, display_name, 10)
            song = self.songs[self.current_question % len(self.songs)]
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                return next_q
            
            msg = f"✅ صحيح يا {display_name}!\n🎤 {song['artist']}\n+{points} نقطة"
            return {'message': msg, 'response': next_q, 'points': points}

        return {
            'message': "▫️ إجابة غير صحيحة ▪️",
            'response': self._create_text_message("▫️ إجابة غير صحيحة ▪️"),
            'points': 0
        }
