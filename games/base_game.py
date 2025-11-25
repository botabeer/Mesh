"""
Bot Mesh - Enhanced Base Game Class
Created by: Abeer Aldosari © 2025

Features:
✅ Unified game system
✅ Perfect Arabic support
✅ Smart state management
✅ LINE-optimized messages
✅ AI-ready architecture
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from constants import (
    THEMES, DEFAULT_THEME, BOT_RIGHTS,
    POINTS_PER_CORRECT_ANSWER, normalize_arabic
)
from typing import Dict, Any, Optional, List


class BaseGame:
    """
    الكلاس الأساسي المحسن لجميع الألعاب
    
    الميزات:
    - دعم كامل للعربية
    - إدارة ذكية للحالة
    - واجهات Flex احترافية
    - تكامل سلس مع AI
    """
    
    def __init__(self, line_bot_api, questions_count=5):
        """
        تهيئة اللعبة
        
        Args:
            line_bot_api: واجهة LINE Bot API
            questions_count: عدد الأسئلة (افتراضي 5)
        """
        self.line_bot_api = line_bot_api
        
        # إعدادات اللعبة
        self.game_name = "لعبة"
        self.game_icon = "🎮"
        self.theme = DEFAULT_THEME
        
        # نظام الأسئلة
        self.questions_count = questions_count
        self.current_question = 0
        
        # نظام النقاط
        self.scores = {}  # {user_id: {"name": str, "score": int}}
        
        # حالة اللعبة
        self.game_active = False
        self.answered_users = set()
        self.current_answer = None
        
        # دعم الميزات
        self.supports_hint = True
        self.supports_reveal = True
        
        # AI functions (will be set by app.py)
        self.ai_generate_question = None
        self.ai_check_answer = None
    
    # ========================================================================
    # إدارة الثيمات
    # ========================================================================
    
    def set_theme(self, theme: str):
        """تعيين ثيم اللعبة"""
        self.theme = theme if theme in THEMES else DEFAULT_THEME
    
    def get_theme_colors(self) -> Dict[str, str]:
        """الحصول على ألوان الثيم الحالي"""
        return THEMES.get(self.theme, THEMES[DEFAULT_THEME])
    
    # ========================================================================
    # إدارة النقاط
    # ========================================================================
    
    def add_score(self, user_id: str, display_name: str, points: int) -> int:
        """
        إضافة نقاط للاعب
        
        Args:
            user_id: معرف المستخدم
            display_name: اسم المستخدم
            points: النقاط المضافة
        
        Returns:
            int: النقاط المضافة
        """
        if user_id not in self.scores:
            self.scores[user_id] = {"name": display_name, "score": 0}
        
        self.scores[user_id]["score"] += points
        self.answered_users.add(user_id)
        return points
    
    def get_top_players(self, limit: int = 3) -> List[tuple]:
        """
        الحصول على أفضل اللاعبين
        
        Args:
            limit: عدد اللاعبين
        
        Returns:
            List[tuple]: قائمة (name, score)
        """
        sorted_scores = sorted(
            self.scores.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )
        return [(data["name"], data["score"]) for _, data in sorted_scores[:limit]]
    
    # ========================================================================
    # دورة حياة اللعبة
    # ========================================================================
    
    def start_game(self):
        """بدء اللعبة - يجب تجاوزها في الكلاسات الفرعية"""
        self.current_question = 0
        self.game_active = True
        self.answered_users.clear()
        return self.get_question()
    
    def get_question(self):
        """إنشاء السؤال - يجب تجاوزها"""
        raise NotImplementedError("يجب تطبيق get_question()")
    
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """
        التحقق من الإجابة - يجب تجاوزها
        
        Args:
            user_answer: إجابة المستخدم
            user_id: معرف المستخدم
            display_name: اسم المستخدم
        
        Returns:
            Optional[Dict]: نتيجة الإجابة أو None
        """
        raise NotImplementedError("يجب تطبيق check_answer()")
    
    def next_question(self) -> Any:
        """الانتقال للسؤال التالي"""
        self.current_question += 1
        self.answered_users.clear()
        
        if self.current_question >= self.questions_count:
            return self.end_game()
        
        return self.get_question()
    
    def end_game(self) -> Dict[str, Any]:
        """إنهاء اللعبة وإرجاع النتيجة"""
        self.game_active = False
        
        # تحديد الفائز
        if self.scores:
            winner = max(self.scores.items(), key=lambda x: x[1]["score"])
            winner_name = winner[1]["name"]
            winner_score = winner[1]["score"]
        else:
            winner_name = "لا يوجد"
            winner_score = 0
        
        # بناء رسالة النهاية
        result_message = self._build_game_over_message(winner_name, winner_score)
        
        return {
            "message": f"🎉 انتهت اللعبة! الفائز: {winner_name}",
            "response": result_message,
            "points": 0,
            "game_over": True
        }
    
    # ========================================================================
    # دوال مساعدة
    # ========================================================================
    
    def normalize_text(self, text: str) -> str:
        """تطبيع النص للمقارنة"""
        return normalize_arabic(text)
    
    def get_hint(self) -> str:
        """الحصول على تلميح - يمكن تجاوزها"""
        if not self.current_answer:
            return "لا يوجد تلميح متاح"
        
        answer = str(self.current_answer)
        if isinstance(self.current_answer, list):
            answer = str(self.current_answer[0])
        
        if len(answer) > 3:
            return f"💡 يبدأ بحرف: {answer[0]}\n📏 عدد الحروف: {len(answer)}"
        return f"💡 يبدأ بحرف: {answer[0]}"
    
    def reveal_answer(self) -> str:
        """كشف الإجابة الصحيحة"""
        if isinstance(self.current_answer, list):
            return f"📝 الإجابة: {' أو '.join(self.current_answer)}"
        return f"📝 الإجابة: {self.current_answer}"
    
    # ========================================================================
    # بناء الرسائل
    # ========================================================================
    
    def _create_flex_with_buttons(self, alt_text: str, flex_content: Dict) -> FlexMessage:
        """إنشاء Flex Message"""
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_content)
        )
    
    def _create_text_message(self, text: str) -> TextMessage:
        """إنشاء رسالة نصية"""
        return TextMessage(text=text)
    
    def _build_game_over_message(self, winner_name: str, winner_score: int) -> FlexMessage:
        """بناء رسالة نهاية اللعبة"""
        colors = self.get_theme_colors()
        
        # تحديد الأداء
        max_score = self.questions_count * POINTS_PER_CORRECT_ANSWER
        performance_ratio = winner_score / max_score if max_score > 0 else 0
        
        if performance_ratio >= 1.0:
            performance = "🏆 ممتاز! إجابات كاملة!"
            perf_color = "#D53F8C"
        elif performance_ratio >= 0.8:
            performance = "⭐ أداء رائع!"
            perf_color = "#667EEA"
        elif performance_ratio >= 0.6:
            performance = "👍 أداء جيد"
            perf_color = "#48BB78"
        else:
            performance = "💪 حاول مرة أخرى"
            perf_color = "#DD6B20"
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "xl",
                "contents": [
                    {
                        "type": "text",
                        "text": "🎉 انتهت اللعبة",
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
                                "text": f"👤 {winner_name}",
                                "size": "xl",
                                "color": colors["text"],
                                "weight": "bold",
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": str(winner_score),
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
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
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
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }
        
        return FlexMessage(
            alt_text=f"انتهت اللعبة - {winner_score} نقطة",
            contents=FlexContainer.from_dict(flex_content)
        )
    
    # ========================================================================
    # معلومات اللعبة
    # ========================================================================
    
    def get_game_info(self) -> Dict[str, Any]:
        """الحصول على معلومات اللعبة"""
        return {
            "name": self.game_name,
            "icon": self.game_icon,
            "theme": self.theme,
            "current_question": self.current_question,
            "total_questions": self.questions_count,
            "active": self.game_active,
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "players_count": len(self.scores)
        }
