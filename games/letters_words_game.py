"""
لعبة تكوين الكلمات - Enhanced UI Version
Created by: Abeer Aldosari © 2025
"""
from linebot.models import TextSendMessage, FlexSendMessage
from .base_game import BaseGame
import random


class LettersWordsGame(BaseGame):
    """لعبة تكوين كلمات من حروف معينة"""

    def __init__(self, line_bot_api, use_ai=False, get_api_key=None, switch_key=None):
        super().__init__(line_bot_api, questions_count=5)
        self.theme = "white"  # default theme
        
        self.letter_sets = [
            {"letters": ["ق", "ل", "م", "ع", "ر", "ب"], 
             "words": ["قلم", "عمل", "علم", "قلب", "رقم", "مقر"]},
            {"letters": ["س", "ا", "ر", "ة", "ي", "م"],
             "words": ["سيارة", "سارية", "رئيس", "سير", "مسار"]},
            {"letters": ["ك", "ت", "ا", "ب", "ة", "ر"],
             "words": ["كتاب", "كتب", "تاب", "ركب", "بكر"]},
            {"letters": ["م", "د", "ر", "س", "ة", "ا"],
             "words": ["مدرسة", "درس", "سمر", "سرد", "مسار"]},
            {"letters": ["ح", "د", "ي", "ق", "ة", "ا"],
             "words": ["حديقة", "قيد", "حق", "دقة", "قاد"]}
        ]
        
        random.shuffle(self.letter_sets)
        self.found_words = set()
        self.required_words = 3

    def set_theme(self, theme_name: str):
        """تعيين الثيم"""
        self.theme = theme_name

    def _get_theme_colors(self):
        """ألوان الثيم"""
        themes = {
            "white": {"bg": "#E0E5EC", "card": "#D1D9E6", "accent": "#667EEA", 
                     "text": "#2C3E50", "text2": "#7F8C8D"},
            "black": {"bg": "#0F0F1A", "card": "#1A1A2E", "accent": "#00D9FF",
                     "text": "#FFFFFF", "text2": "#A0AEC0"},
            "gray": {"bg": "#1A202C", "card": "#2D3748", "accent": "#68D391",
                    "text": "#F7FAFC", "text2": "#CBD5E0"},
            "purple": {"bg": "#1E1B4B", "card": "#312E81", "accent": "#A855F7",
                      "text": "#F5F3FF", "text2": "#C4B5FD"},
            "blue": {"bg": "#0C1929", "card": "#1E3A5F", "accent": "#00D9FF",
                    "text": "#E0F2FE", "text2": "#7DD3FC"}
        }
        return themes.get(self.theme, themes["white"])

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def get_question(self):
        """إنشاء بطاقة السؤال"""
        letter_set = self.letter_sets[self.current_question % len(self.letter_sets)]
        self.current_answer = letter_set["words"]
        self.found_words.clear()
        
        colors = self._get_theme_colors()
        letters = letter_set["letters"]
        
        # إنشاء صفوف الحروف
        letter_boxes = []
        row = []
        for i, letter in enumerate(letters):
            row.append({
                "type": "box",
                "layout": "vertical",
                "contents": [{
                    "type": "text",
                    "text": letter,
                    "size": "xxl",
                    "weight": "bold",
                    "color": colors["accent"],
                    "align": "center"
                }],
                "backgroundColor": colors["card"],
                "cornerRadius": "15px",
                "paddingAll": "15px",
                "width": "55px",
                "height": "55px",
                "justifyContent": "center",
                "alignItems": "center"
            })
            
            if len(row) == 3 or i == len(letters) - 1:
                letter_boxes.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": row,
                    "spacing": "md",
                    "justifyContent": "center",
                    "margin": "sm" if letter_boxes else "none"
                })
                row = []
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🎮 Neumorphism Soft", "size": "lg", 
                     "weight": "bold", "color": "#FFFFFF", "align": "center"},
                    {"type": "text", "text": "تأثير 3D - عمق ناعم", "size": "xs",
                     "color": "#E0E0E0", "align": "center"}
                ],
                "backgroundColor": colors["accent"],
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # عنوان اللعبة
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "🔄", "text": "ابدأ"},
                                "style": "secondary",
                                "height": "sm",
                                "flex": 0
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": "■ لعبة تكوين الكلمات",
                                     "size": "md", "weight": "bold", "color": colors["text"],
                                     "align": "end"},
                                    {"type": "text", 
                                     "text": f"سؤال {self.current_question + 1} من {self.questions_count}",
                                     "size": "xs", "color": colors["text2"], "align": "end"}
                                ],
                                "flex": 1
                            }
                        ]
                    },
                    
                    # الحروف
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": letter_boxes,
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "lg"
                    },
                    
                    # التعليمات
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", 
                             "text": f"كوّن {self.required_words} كلمات من هذه الحروف",
                             "size": "sm", "color": colors["text"], "align": "center"},
                            {"type": "text", "text": "اكتب كلمة واحدة في كل رسالة",
                             "size": "xs", "color": colors["text2"], "align": "center"}
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "15px",
                        "margin": "lg"
                    },
                    
                    # الأزرار
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "💡 تلميح", "text": "لمح"},
                                "style": "primary",
                                "color": colors["accent"],
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "الحل", "text": "جاوب"},
                                "style": "secondary",
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
        
        return FlexSendMessage(alt_text="لعبة تكوين الكلمات", contents=flex_content)

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active:
            return None

        answer = user_answer.strip()
        
        # تلميح
        if answer == 'لمح':
            remaining = [w for w in self.current_answer if self.normalize_text(w) not in self.found_words]
            if remaining:
                word = remaining[0]
                hint = f"💡 الكلمة من {len(word)} حروف وأولها '{word[0]}'"
            else:
                hint = "لا توجد تلميحات"
            return {'message': hint, 'response': TextSendMessage(text=hint), 'points': 0}

        # الحل
        if answer in ['جاوب', 'تم', 'التالي']:
            if len(self.found_words) >= self.required_words or answer == 'جاوب':
                words = " • ".join(self.current_answer[:5])
                msg = f"📝 الكلمات الممكنة:\n{words}"
                return self._next_question(msg=msg)
            else:
                remaining = self.required_words - len(self.found_words)
                return {'message': f"❌ تبقى {remaining} كلمات",
                       'response': TextSendMessage(text=f"❌ تبقى {remaining} كلمات"), 'points': 0}

        # فحص الكلمة
        normalized = self.normalize_text(answer)
        valid_words = [self.normalize_text(w) for w in self.current_answer]

        if normalized in self.found_words:
            return {'message': f"⚠️ '{answer}' مكتشفة سابقاً",
                   'response': TextSendMessage(text=f"⚠️ '{answer}' مكتشفة سابقاً"), 'points': 0}

        if normalized in valid_words:
            self.found_words.add(normalized)
            points = self.add_score(user_id, display_name, 10)
            
            if len(self.found_words) >= self.required_words:
                return self._next_question(points=points, 
                    msg=f"🎉 أحسنت يا {display_name}!\n+{points} نقطة")
            
            remaining = self.required_words - len(self.found_words)
            msg = f"✅ صحيح!\n+{points} نقطة\n\n⏳ تبقى {remaining} كلمات"
            return {'message': msg, 'response': TextSendMessage(text=msg), 'points': points}

        return None

    def _next_question(self, points=0, msg=""):
        self.current_question += 1
        
        if self.current_question >= self.questions_count:
            self.game_active = False
            final_msg = f"{msg}\n\n🏁 انتهت اللعبة!" if msg else "🏁 انتهت اللعبة!"
            return {'message': final_msg, 'response': TextSendMessage(text=final_msg),
                   'game_over': True, 'points': points}

        next_q = self.get_question()
        return {'message': msg, 'response': next_q, 'points': points}
