"""
لعبة تخمين الأغنية - النسخة المحسنة النهائية
Created by: Abeer Aldosari © 2025

الميزات:
✅ AI أولاً مع Fallback قوي
✅ قاعدة أغاني متنوعة
✅ واجهة Flex احترافية
✅ تشفير عربي مثالي
✅ أداء محسن
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional


class SongGame(BaseGame):
    """لعبة تخمين الأغنية المحسنة مع AI"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "أغنية"
        self.game_icon = "🎵"
        
        # قاعدة أغاني محسنة
        self.fallback_songs = [
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
        
        random.shuffle(self.fallback_songs)
        self.used_songs = []
        self.previous_question = None
        self.previous_answer = None

    def generate_question_with_ai(self):
        """توليد سؤال بالذكاء الاصطناعي مع Fallback"""
        question_data = None
        
        # محاولة AI أولاً
        if self.ai_generate_question:
            try:
                question_data = self.ai_generate_question()
                if question_data and "lyrics" in question_data and "artist" in question_data:
                    return question_data
            except Exception as e:
                print(f"⚠️ AI generation failed, using fallback: {e}")
        
        # Fallback للأغاني المخزنة
        available = [s for s in self.fallback_songs if s not in self.used_songs]
        if not available:
            self.used_songs = []
            available = self.fallback_songs.copy()
        
        question_data = random.choice(available)
        self.used_songs.append(question_data)
        return question_data

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        """إنشاء سؤال مع واجهة Flex محسنة"""
        q_data = self.generate_question_with_ai()
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
                        {
                            "type": "text",
                            "text": "📝 الأغنية السابقة:",
                            "size": "xs",
                            "color": colors["text2"],
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": self.previous_question,
                            "size": "xs",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "xs"
                        },
                        {
                            "type": "text",
                            "text": f"✅ المغني: {self.previous_answer}",
                            "size": "xs",
                            "color": colors["success"],
                            "wrap": True,
                            "margin": "xs"
                        }
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
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"{self.game_icon} {self.game_name}",
                                "size": "xl",
                                "weight": "bold",
                                "color": colors["text"],
                                "flex": 3
                            },
                            {
                                "type": "text",
                                "text": f"جولة {self.current_question + 1}/5",
                                "size": "sm",
                                "color": colors["text2"],
                                "align": "end",
                                "flex": 2
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
                "spacing": "md",
                "contents": previous_section + [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "🎤 من المغني؟",
                                "size": "sm",
                                "color": colors["text2"],
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": q_data["lyrics"],
                                "size": "lg",
                                "color": colors["text"],
                                "wrap": True,
                                "margin": "md",
                                "weight": "bold",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px"
                    },
                    {
                        "type": "text",
                        "text": "💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "wrap": True,
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
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "💡 لمّح", "text": "لمح"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "🔍 جاوب", "text": "جاوب"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            }
                        ]
                    },
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

        return self._create_flex_with_buttons(f"{self.game_name} - جولة {self.current_question + 1}", flex_content)

    def check_answer_intelligently(self, user_answer: str) -> bool:
        """فحص ذكي للإجابة مع دعم AI"""
        normalized_user = self.normalize_text(user_answer)
        normalized_correct = self.normalize_text(self.current_answer)
        
        # تطابق كامل
        if normalized_user == normalized_correct:
            return True
        
        # تطابق جزئي
        if normalized_user in normalized_correct or normalized_correct in normalized_user:
            return True
        
        # تشابه نصي (80% أو أكثر)
        ratio = difflib.SequenceMatcher(None, normalized_user, normalized_correct).ratio()
        if ratio > 0.8:
            return True
        
        # محاولة AI للتحقق
        if self.ai_check_answer:
            try:
                if self.ai_check_answer(self.current_answer, user_answer):
                    return True
            except:
                pass
        
        return False

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص الإجابة مع دعم كامل للتلميحات"""
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        # أمر التلميح
        if normalized == 'لمح':
            hint = f"💡 اسم المغني يبدأ بحرف '{self.current_answer[0]}'"
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }

        # أمر كشف الإجابة
        if normalized == 'جاوب':
            reveal = f"🎤 المغني: {self.current_answer}"
            
            # حفظ السؤال والجواب
            q_data = self.generate_question_with_ai()
            self.previous_question = q_data['lyrics']
            self.previous_answer = self.current_answer
            
            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message', '')}"
                return result
            
            next_q = self.get_question()
            return {'message': reveal, 'response': next_q, 'points': 0}

        # التحقق من الإجابة
        is_correct = self.check_answer_intelligently(user_answer)

        if is_correct:
            points = self.add_score(user_id, display_name, 10)
            
            # حفظ السؤال والجواب
            q_data = self.generate_question_with_ai()
            self.previous_question = q_data['lyrics']
            self.previous_answer = self.current_answer
            
            # الانتقال للسؤال التالي
            self.current_question += 1
            self.answered_users.clear()
            
            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ صحيح يا {display_name}!\n🎤 {self.current_answer}\n+{points} نقطة\n\n{result.get('message', '')}"
                return result
            
            next_q = self.get_question()
            success_msg = f"✅ صحيح يا {display_name}!\n🎤 {self.current_answer}\n+{points} نقطة"
            
            return {
                'message': success_msg,
                'response': next_q,
                'points': points
            }

        return {
            'message': "❌ إجابة غير صحيحة، حاول مرة أخرى",
            'response': self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
            'points': 0
        }

    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": "لعبة تخمين الأغنية",
            "emoji": "🎵",
            "description": "خمن المغني بناءً على كلمات الأغنية مع دعم AI",
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "ai_enabled": self.ai_generate_question is not None
        }
