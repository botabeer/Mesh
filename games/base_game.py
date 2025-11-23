"""
Bot Mesh - Base Game Class
Created by: Abeer Aldosari © 2025
"""
import logging
from config import THEMES, DEFAULT_ROUNDS, POINTS_PER_WIN, POINTS_PER_CORRECT

logger = logging.getLogger(__name__)

class BaseGame:
    """الكلاس الأساسي لجميع الألعاب"""
    
    def __init__(self, line_api, rounds=DEFAULT_ROUNDS):
        self.line_api = line_api
        self.rounds = rounds
        self.current_round = 0
        self.theme = THEMES['white']
        self.current_question = None
        self.current_answer = None
        self.players_scores = {}
        
    def set_theme(self, theme_name):
        """تعيين الثيم"""
        if theme_name in THEMES:
            self.theme = THEMES[theme_name]
            logger.debug(f"Theme set to: {theme_name}")
        
    def start_game(self):
        """بدء اللعبة - يجب تنفيذها في الكلاس الفرعي"""
        raise NotImplementedError("يجب تنفيذ start_game في الكلاس الفرعي")
    
    def check_answer(self, answer, uid, name):
        """فحص الإجابة - يجب تنفيذها في الكلاس الفرعي"""
        raise NotImplementedError("يجب تنفيذ check_answer في الكلاس الفرعي")
    
    def next_round(self):
        """الانتقال للجولة التالية"""
        self.current_round += 1
        if self.current_round >= self.rounds:
            return self.end_game()
        return self.generate_question()
    
    def generate_question(self):
        """توليد سؤال جديد - يجب تنفيذها في الكلاس الفرعي"""
        raise NotImplementedError("يجب تنفيذ generate_question في الكلاس الفرعي")
    
    def end_game(self):
        """إنهاء اللعبة"""
        logger.info("Game ended")
        return None
    
    def add_player_score(self, uid, points):
        """إضافة نقاط للاعب"""
        if uid not in self.players_scores:
            self.players_scores[uid] = 0
        self.players_scores[uid] += points
        
    def get_winner(self):
        """الحصول على الفائز"""
        if not self.players_scores:
            return None
        return max(self.players_scores.items(), key=lambda x: x[1])
    
    def build_question_flex(self, game_name, question, extra_info=None):
        """بناء نافذة Flex للسؤال"""
        contents = [
            {
                "type": "text",
                "text": question,
                "weight": "bold",
                "size": "xl",
                "color": self.theme['text'],
                "wrap": True,
                "align": "center"
            }
        ]
        
        if extra_info:
            contents.append({
                "type": "separator",
                "margin": "lg",
                "color": self.theme['border']
            })
            contents.append({
                "type": "text",
                "text": extra_info,
                "size": "sm",
                "color": self.theme['text2'],
                "wrap": True,
                "margin": "md",
                "align": "center"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"🎯 {game_name}",
                        "weight": "bold",
                        "size": "lg",
                        "color": self.theme['text'],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"الجولة {self.current_round + 1} من {self.rounds}",
                        "size": "sm",
                        "color": self.theme['text'],
                        "align": "center",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": self.theme['primary'],
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": self.theme['card'],
                "paddingAll": "30px"
            },
            "styles": {
                "header": {
                    "backgroundColor": self.theme['primary']
                },
                "body": {
                    "backgroundColor": self.theme['card']
                }
            }
        }
    
    def build_result_flex(self, winner_name, answer, points, is_final=False):
        """بناء نافذة Flex للنتيجة"""
        title = "🏆 اللعبة انتهت!" if is_final else "✅ إجابة صحيحة!"
        
        contents = [
            {
                "type": "text",
                "text": f"الفائز: {winner_name}",
                "weight": "bold",
                "size": "lg",
                "color": self.theme['text'],
                "wrap": True
            },
            {
                "type": "separator",
                "margin": "md",
                "color": self.theme['border']
            },
            {
                "type": "text",
                "text": f"الإجابة: {answer}",
                "size": "md",
                "color": self.theme['text2'],
                "wrap": True,
                "margin": "md"
            },
            {
                "type": "text",
                "text": f"النقاط: +{points}",
                "weight": "bold",
                "size": "md",
                "color": self.theme['accent'],
                "margin": "md"
            }
        ]
        
        if is_final:
            contents.append({
                "type": "separator",
                "margin": "lg",
                "color": self.theme['border']
            })
            contents.append({
                "type": "text",
                "text": "🎉 مبروك! تم إنهاء اللعبة",
                "size": "sm",
                "color": self.theme['text2'],
                "wrap": True,
                "margin": "md",
                "align": "center"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "weight": "bold",
                        "size": "lg",
                        "color": self.theme['text'],
                        "align": "center"
                    }
                ],
                "backgroundColor": self.theme['primary'],
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": self.theme['card'],
                "paddingAll": "20px"
            },
            "styles": {
                "header": {
                    "backgroundColor": self.theme['primary']
                },
                "body": {
                    "backgroundColor": self.theme['card']
                }
            }
        }
    
    def normalize_text(self, text):
        """تطبيع النص للمقارنة"""
        # إزالة المسافات الزائدة
        text = ' '.join(text.split())
        # تحويل لحروف صغيرة
        text = text.lower()
        # إزالة علامات الترقيم
        import string
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text.strip()
    
    def is_correct_answer(self, user_answer, correct_answer):
        """التحقق من صحة الإجابة"""
        user_normalized = self.normalize_text(str(user_answer))
        correct_normalized = self.normalize_text(str(correct_answer))
        return user_normalized == correct_normalized
