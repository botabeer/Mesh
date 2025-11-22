"""
لعبة تخمين الأغنية - Enhanced UI Version
Created by: Abeer Aldosari © 2025
"""
from linebot.models import TextSendMessage, FlexSendMessage
from .base_game import BaseGame
import random


class SongGame(BaseGame):
    """لعبة تخمين المغني من كلمات الأغنية"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.theme = "blue"  # الثيم الأزرق مثل الصورة
        
        self.songs = [
            {"artist": "أم كلثوم", "title": "أيام الماضي", 
             "lyrics": "رجعت لي أيام الماضي معاك", "nationality": "مصرية"},
            {"artist": "عبد الحليم حافظ", "title": "الخوف بعينيها",
             "lyrics": "جلست والخوف بعينيها تتأمل فنجاني", "nationality": "مصري"},
            {"artist": "عمرو دياب", "title": "تملي معاك",
             "lyrics": "تملي معاك ولو حتى بعيد عني", "nationality": "مصري"},
            {"artist": "كاظم الساهر", "title": "قولي أحبك",
             "lyrics": "قولي أحبك كي تزيد وسامتي", "nationality": "عراقي"},
            {"artist": "فيروز", "title": "أنا لحبيبي",
             "lyrics": "أنا لحبيبي وحبيبي إلي", "nationality": "لبنانية"},
            {"artist": "عايض", "title": "كيف أبين لك",
             "lyrics": "كيف أبيّن لك شعوري دون ما أحكي", "nationality": "سعودي"},
            {"artist": "عبدالمجيد عبدالله", "title": "رحت عني",
             "lyrics": "رحت عني ما قويت جيت لك لاتردني", "nationality": "سعودي"},
            {"artist": "راشد الماجد", "title": "مخنوق",
             "lyrics": "تدري كثر ماني من البعد مخنوق", "nationality": "سعودي"},
            {"artist": "حسين الجسمي", "title": "أنا عندي قلب واحد",
             "lyrics": "أنا عندي قلب واحد", "nationality": "إماراتي"},
            {"artist": "محمد عبده", "title": "منوتي ليتك معي",
             "lyrics": "منوتي ليتك معي", "nationality": "سعودي"},
        ]
        
        random.shuffle(self.songs)

    def _get_colors(self):
        """ألوان الثيم الأزرق"""
        return {
            "bg": "#0C1929",
            "card": "#0F2744", 
            "accent": "#00D9FF",
            "text": "#E0F2FE",
            "text2": "#7DD3FC",
            "button": "#1E3A5F"
        }

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()
    
    def get_question(self):
        """إنشاء بطاقة السؤال"""
        song = self.songs[self.current_question % len(self.songs)]
        self.current_answer = song["artist"]
        
        colors = self._get_colors()
        progress = self.current_question + 1
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "styles": {
                "body": {"backgroundColor": colors["bg"]}
            },
            "header": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    # أيقونة الموسيقى
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "🎵", "size": "xl", "align": "center"}
                        ],
                        "backgroundColor": colors["text"],
                        "cornerRadius": "25px",
                        "width": "45px",
                        "height": "45px",
                        "justifyContent": "center"
                    },
                    # العنوان
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "لعبة الأغنية", "size": "xl",
                             "weight": "bold", "color": colors["text"]},
                            {"type": "text", "text": f"السؤال {progress}/{self.questions_count}",
                             "size": "sm", "color": colors["text2"]}
                        ],
                        "margin": "lg",
                        "flex": 1
                    }
                ],
                "backgroundColor": colors["accent"],
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # كلمات الأغنية
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": song["lyrics"],
                             "size": "lg", "weight": "bold", "color": colors["text"],
                             "align": "center", "wrap": True}
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "25px",
                        "margin": "lg"
                    },
                    
                    # سؤال
                    {"type": "text", "text": "من المغني؟", "size": "md",
                     "color": colors["accent"], "align": "center", "margin": "xl"},
                    
                    # شريط التقدم
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "backgroundColor": colors["accent"],
                                "height": "5px",
                                "flex": progress
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "backgroundColor": colors["card"],
                                "height": "5px",
                                "flex": self.questions_count - progress
                            }
                        ],
                        "cornerRadius": "3px",
                        "margin": "md"
                    },
                    
                    # الأزرار
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "💡 لمح", "text": "لمح"},
                                "style": "secondary",
                                "color": colors["button"],
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "جاوب", "text": "جاوب"},
                                "style": "primary",
                                "color": colors["accent"],
                                "height": "sm"
                            }
                        ],
                        "spacing": "md",
                        "margin": "xl"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            }
        }
        
        return FlexSendMessage(alt_text="لعبة الأغنية", contents=flex_content)

    def get_hint(self):
        """تلميح الجنسية"""
        song = self.songs[self.current_question % len(self.songs)]
        female = ["لبنانية", "سورية", "كويتية", "سعودية", "مصرية"]
        gender = "مغنية" if song["nationality"] in female else "مغني"
        return f"💡 تلميح: {gender} {song['nationality']}"

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None
        
        if user_id in self.answered_users:
            return None
        
        # تلميح
        if user_answer == 'لمح':
            hint = self.get_hint()
            return {'message': hint, 'response': TextSendMessage(text=hint), 'points': 0}
        
        # الإجابة
        if user_answer == 'جاوب':
            song = self.songs[self.current_question % len(self.songs)]
            reveal = f"🎤 المغني: {song['artist']}\n🎵 الأغنية: {song['title']}"
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['message'] = f"{reveal}\n\n{next_q.get('message', '')}"
                return next_q
            
            return {'message': reveal, 'response': next_q, 'points': 0}
        
        # فحص الإجابة
        normalized = self.normalize_text(user_answer)
        correct = self.normalize_text(self.current_answer)
        
        if correct in normalized or normalized in correct:
            points = self.add_score(user_id, display_name, 10)
            song = self.songs[self.current_question % len(self.songs)]
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                return next_q
            
            msg = f"✅ صحيح يا {display_name}!\n\n"
            msg += f"🎤 {song['artist']}\n🎵 {song['title']}\n\n+{points} نقطة"
            
            return {'message': msg, 'response': next_q, 'points': points}
        
        return None
