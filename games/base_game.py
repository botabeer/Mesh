"""
Bot Mesh - Unified Base Game Class
Created by: Abeer Aldosari © 2025

النظام الموحد يجمع بين:
- نظام الثيمات الديناميكية
- نظام النقاط المتقدم
- واجهات Neumorphism احترافية
- دعم كامل لجميع الألعاب
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from constants import (
    THEMES, DEFAULT_THEME, BOT_RIGHTS, ROUNDS_PER_GAME,
    POINTS_PER_CORRECT_ANSWER, normalize_arabic
)
from typing import Dict, Any, Optional


class BaseGame:
    """
    الكلاس الأساسي لجميع الألعاب
    
    يدعم:
    - نظامين مختلفين للتهيئة
    - ثيمات ديناميكية
    - نقاط متقدمة
    - واجهات Flex احترافية
    """
    
    def __init__(self, line_bot_api, questions_count=None):
        """
        تهيئة اللعبة
        
        المعاملات:
            line_bot_api: واجهة LINE Bot API
            questions_count: عدد الأسئلة (اختياري، افتراضي 5)
        """
        self.line_bot_api = line_bot_api
        
        # إعدادات اللعبة الأساسية
        self.theme = DEFAULT_THEME
        self.game_name = "لعبة"
        self.game_icon = "🎮"
        
        # نظام الجولات (يدعم النظامين)
        if questions_count is not None:
            # النظام الجديد
            self.questions_count = questions_count
            self.total_rounds = questions_count
            self.current_question = 0
        else:
            # النظام القديم
            self.total_rounds = ROUNDS_PER_GAME
            self.current_round = 1
            self.current_question = 0
        
        # نظام النقاط
        self.score = 0
        self.scores = {}  # {user_id: {"name": str, "score": int}}
        
        # السؤال الحالي
        self.current_answer = None
        
        # حالة اللعبة
        self.game_active = False
        self.answered_users = set()
        
        # دعم التلميحات
        self.supports_hint = True
        self.supports_reveal = True
    
    # ========================================================================
    # إدارة الثيمات
    # ========================================================================
    
    def set_theme(self, theme):
        """تعيين ثيم اللعبة"""
        self.theme = theme if theme in THEMES else DEFAULT_THEME
    
    def get_colors(self):
        """الحصول على ألوان الثيم الحالي (للتوافق مع النظام القديم)"""
        return THEMES.get(self.theme, THEMES[DEFAULT_THEME])
    
    def get_theme_colors(self):
        """الحصول على ألوان الثيم الحالي (للتوافق مع النظام الجديد)"""
        return THEMES.get(self.theme, THEMES[DEFAULT_THEME])
    
    # ========================================================================
    # إدارة النقاط
    # ========================================================================
    
    def add_score(self, user_id: str, display_name: str, points: int) -> int:
        """
        إضافة نقاط للاعب
        
        المعاملات:
            user_id: معرف المستخدم
            display_name: اسم المستخدم
            points: النقاط المضافة
            
        العودة:
            int: النقاط المضافة
        """
        if user_id not in self.scores:
            self.scores[user_id] = {"name": display_name, "score": 0}
        
        self.scores[user_id]["score"] += points
        self.answered_users.add(user_id)
        return points
    
    # ========================================================================
    # أساليب اللعبة الأساسية (يجب تجاوزها)
    # ========================================================================
    
    def start_game(self):
        """بدء اللعبة - يجب تجاوزها في الكلاسات الفرعية"""
        # دعم النظامين
        if hasattr(self, 'questions_count'):
            self.current_question = 0
        else:
            self.current_round = 1
        
        self.score = 0
        self.game_active = True
        return self.next_question()
    
    def next_question(self):
        """
        إنشاء السؤال التالي - يجب تجاوزها
        
        العودة:
            FlexMessage أو dict
        """
        # للألعاب الجديدة
        if hasattr(self, 'questions_count'):
            self.current_question += 1
            if self.current_question > self.questions_count:
                return self.end_game()
            return self.get_question()
        
        # للألعاب القديمة
        raise NotImplementedError("يجب تطبيق next_question()")
    
    def get_question(self):
        """إنشاء السؤال - للنظام الجديد"""
        raise NotImplementedError("يجب تطبيق get_question()")
    
    def check_answer(self, user_answer: str, user_id: str, username: str):
        """
        التحقق من الإجابة - يجب تجاوزها
        
        المعاملات:
            user_answer: إجابة المستخدم
            user_id: معرف المستخدم
            username: اسم المستخدم
            
        العودة:
            dict: نتيجة الإجابة
        """
        raise NotImplementedError("يجب تطبيق check_answer()")
    
    def end_game(self):
        """
        إنهاء اللعبة وإرجاع النتيجة النهائية
        
        العودة:
            dict: نتيجة نهاية اللعبة
        """
        self.game_active = False
        
        # حساب الفائز
        if self.scores:
            winner = max(self.scores.items(), key=lambda x: x[1]["score"])
            winner_name = winner[1]["name"]
            winner_score = winner[1]["score"]
        else:
            winner_name = "لا يوجد"
            winner_score = 0
        
        colors = self.get_theme_colors()
        
        # بناء رسالة نهاية اللعبة
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🎉 انتهت اللعبة",
                        "size": "xl",
                        "weight": "bold",
                        "color": colors["text"],
                        "align": "center"
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
                        "type": "text",
                        "text": f"🏆 الفائز: {winner_name}",
                        "size": "lg",
                        "color": colors["primary"],
                        "weight": "bold",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"⭐ النقاط: {winner_score}",
                        "size": "md",
                        "color": colors["text"],
                        "align": "center",
                        "margin": "md"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "styles": {"body": {"backgroundColor": colors["bg"]}}
        }
        
        response = self._create_flex_with_buttons("نهاية اللعبة", flex_content)
        
        return {
            "message": f"🎉 انتهت اللعبة! الفائز: {winner_name}",
            "response": response,
            "points": 0,
            "game_over": True
        }
    
    # ========================================================================
    # دوال مساعدة
    # ========================================================================
    
    def normalize_answer(self, text):
        """تطبيع الإجابة للمقارنة"""
        return normalize_arabic(text)
    
    def normalize_text(self, text):
        """تطبيع النص (للتوافق مع النظام الجديد)"""
        return normalize_arabic(text)
    
    def get_hint(self):
        """الحصول على تلميح - يمكن تجاوزها"""
        if not self.current_answer:
            return "لا يوجد تلميح متاح"
        
        answer = str(self.current_answer)
        hint_length = max(1, len(answer) // 2)
        return answer[:hint_length] + "..."
    
    def reveal_answer(self):
        """كشف الإجابة الصحيحة"""
        return f"الإجابة الصحيحة: {self.current_answer}"
    
    # ========================================================================
    # بناء الواجهات (النظام القديم)
    # ========================================================================
    
    def build_question_card(self, question_text, hint_text=None, additional_contents=None):
        """بناء بطاقة السؤال مع تصميم Neumorphism"""
        colors = self.get_colors()
        
        # تحديد رقم الجولة الحالي
        if hasattr(self, 'current_round'):
            round_num = self.current_round
            total = self.total_rounds
        else:
            round_num = self.current_question + 1
            total = self.questions_count
        
        contents = [
            # رأس اللعبة
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{self.game_icon} {self.game_name}",
                        "weight": "bold",
                        "size": "lg",
                        "color": colors["primary"],
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": f"سؤال {round_num} من {total}",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "end",
                        "flex": 2
                    }
                ]
            },
            {"type": "separator", "color": colors["shadow1"]},
            
            # بطاقة السؤال
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": question_text,
                        "size": "lg",
                        "color": colors["text"],
                        "wrap": True,
                        "weight": "bold",
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "25px"
            }
        ]
        
        # إضافة التلميح إن وجد
        if hint_text:
            contents.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"💡 {hint_text}",
                        "size": "sm",
                        "color": colors["text2"],
                        "wrap": True,
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "15px",
                "paddingAll": "15px"
            })
        
        # إضافة محتويات إضافية
        if additional_contents:
            contents.extend(additional_contents)
        
        # مؤشر النقاط
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": f"⭐ النقاط: {self.score}",
                    "size": "sm",
                    "color": colors["primary"],
                    "weight": "bold"
                }
            ]
        })
        
        # التذييل مع أزرار الإجراءات
        footer = [
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "💡 لمح", "text": "لمح"},
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
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                        "style": "primary",
                        "height": "sm",
                        "color": "#FF5555"
                    }
                ]
            },
            {"type": "separator", "color": colors["shadow1"]},
            {
                "type": "text",
                "text": BOT_RIGHTS,
                "size": "xxs",
                "color": colors["text2"],
                "align": "center"
            }
        ]
        
        card = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
                "contents": contents,
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": footer,
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }
        
        return FlexMessage(
            alt_text=f"{self.game_name} - {round_num}/{total}",
            contents=FlexContainer.from_dict(card)
        )
    
    def build_result_card(self, is_correct, correct_answer, message):
        """بناء بطاقة النتيجة (صحيح/خطأ)"""
        colors = self.get_colors()
        
        result_emoji = "✅" if is_correct else "❌"
        result_text = "إجابة صحيحة!" if is_correct else "إجابة خاطئة"
        result_color = "#48BB78" if is_correct else "#FF5555"
        
        contents = [
            {
                "type": "text",
                "text": f"{result_emoji} {result_text}",
                "weight": "bold",
                "size": "xl",
                "color": result_color,
                "align": "center"
            },
            {"type": "separator", "color": colors["shadow1"]},
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": message,
                        "size": "md",
                        "color": colors["text"],
                        "wrap": True,
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"الإجابة الصحيحة: {correct_answer}",
                        "size": "sm",
                        "color": colors["text2"],
                        "wrap": True,
                        "align": "center"
                    } if not is_correct else None
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "20px"
            },
            {
                "type": "text",
                "text": f"⭐ النقاط الحالية: {self.score}",
                "size": "md",
                "color": colors["primary"],
                "weight": "bold",
                "align": "center"
            }
        ]
        
        # إزالة القيم None
        contents = [c for c in contents if c is not None]
        
        card = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
                "contents": contents,
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]}
            }
        }
        
        return FlexMessage(
            alt_text=result_text,
            contents=FlexContainer.from_dict(card)
        )
    
    def build_game_over_card(self, username, final_score):
        """بناء بطاقة نهاية اللعبة مع خيار إعادة اللعب"""
        colors = self.get_colors()
        
        # تحديد رسالة الأداء
        max_score = self.total_rounds * POINTS_PER_CORRECT_ANSWER
        
        if final_score == max_score:
            performance = "🏆 ممتاز! إجابات كاملة!"
            perf_color = "#D53F8C"
        elif final_score >= max_score * 0.6:
            performance = "⭐ أداء جيد جداً!"
            perf_color = "#667EEA"
        elif final_score >= max_score * 0.4:
            performance = "👍 أداء جيد"
            perf_color = "#48BB78"
        else:
            performance = "💪 حاول مرة أخرى"
            perf_color = "#DD6B20"
        
        contents = [
            {
                "type": "text",
                "text": f"🎉 انتهت اللعبة",
                "weight": "bold",
                "size": "xxl",
                "color": colors["primary"],
                "align": "center"
            },
            {"type": "separator", "color": colors["shadow1"]},
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
                "contents": [
                    {
                        "type": "text",
                        "text": f"👤 {username}",
                        "size": "lg",
                        "color": colors["text"],
                        "weight": "bold",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"{final_score}",
                        "size": "xxl",
                        "weight": "bold",
                        "color": colors["primary"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "نقطة",
                        "size": "md",
                        "color": colors["text2"],
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "30px"
            },
            {
                "type": "text",
                "text": performance,
                "size": "lg",
                "color": perf_color,
                "weight": "bold",
                "align": "center"
            }
        ]
        
        footer = [
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "🔄 إعادة اللعبة",
                            "text": f"لعبة {self.game_name}"
                        },
                        "style": "primary",
                        "height": "sm",
                        "color": colors["button"]
                    }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "🏠 بداية", "text": "بداية"},
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "🎮 ألعاب", "text": "مساعدة"},
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
            },
            {"type": "separator", "color": colors["shadow1"]},
            {
                "type": "text",
                "text": BOT_RIGHTS,
                "size": "xxs",
                "color": colors["text2"],
                "align": "center"
            }
        ]
        
        card = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xl",
                "contents": contents,
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": footer,
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }
        
        return FlexMessage(
            alt_text=f"انتهت اللعبة - {final_score} نقطة",
            contents=FlexContainer.from_dict(card)
        )
    
    # ========================================================================
    # دوال مساعدة للنظام الجديد
    # ========================================================================
    
    def _create_flex_with_buttons(self, alt_text: str, flex_content: Dict) -> FlexMessage:
        """
        إنشاء Flex Message مع أزرار
        
        المعاملات:
            alt_text: النص البديل
            flex_content: محتوى Flex
            
        العودة:
            FlexMessage
        """
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_content)
        )
    
    def _create_text_message(self, text: str):
        """
        إنشاء رسالة نصية بسيطة
        
        المعاملات:
            text: النص
            
        العودة:
            TextMessage
        """
        return TextMessage(text=text)
    
    # ========================================================================
    # معلومات اللعبة
    # ========================================================================
    
    def get_game_info(self) -> Dict[str, Any]:
        """
        الحصول على معلومات اللعبة
        
        العودة:
            dict: معلومات اللعبة
        """
        if hasattr(self, 'questions_count'):
            current = self.current_question
            total = self.questions_count
        else:
            current = self.current_round
            total = self.total_rounds
        
        return {
            "name": self.game_name,
            "icon": self.game_icon,
            "theme": self.theme,
            "current_question": current,
            "total_questions": total,
            "score": self.score,
            "active": self.game_active,
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "players_count": len(self.scores)
        }
