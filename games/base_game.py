"""
Bot Mesh - Enhanced Base Game Class v5.0
Created by: Abeer Aldosari © 2025

التحسينات الجديدة:
✅ أزرار ثابتة أسفل كل نافذة
✅ نظام تتبع محسّن للأسئلة السابقة
✅ واجهة موحدة لجميع الألعاب
✅ نصوص مختصرة وواضحة
✅ معالجة أخطاء شاملة
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from constants import (
    THEMES, DEFAULT_THEME, BOT_RIGHTS,
    POINTS_PER_CORRECT_ANSWER, normalize_arabic
)
from typing import Dict, Any, Optional, List
from datetime import datetime
import threading

class BaseGame:
    """الكلاس الأساسي المحسّن لجميع الألعاب"""
    
    _lock = threading.Lock()
    
    def __init__(self, line_bot_api, questions_count=5):
        """تهيئة اللعبة"""
        self.line_bot_api = line_bot_api
        
        # إعدادات اللعبة
        self.game_name = "لعبة"
        self.game_icon = "🎮"
        self.theme = DEFAULT_THEME
        
        # نظام الأسئلة
        self.questions_count = questions_count
        self.current_question = 0
        
        # نظام النقاط
        self.scores = {}
        self._scores_lock = threading.Lock()
        
        # حالة اللعبة
        self.game_active = False
        self.answered_users = set()
        self.current_answer = None
        self.created_at = datetime.now()
        
        # تتبع الأسئلة السابقة
        self.previous_question_text = None
        self.previous_answer_text = None
        
        # دعم الميزات
        self.supports_hint = True
        self.supports_reveal = True
        
        # AI functions
        self.ai_generate_question = None
        self.ai_check_answer = None
    
    def set_theme(self, theme: str):
        """تعيين ثيم اللعبة"""
        self.theme = theme if theme in THEMES else DEFAULT_THEME
    
    def get_theme_colors(self) -> Dict[str, str]:
        """الحصول على ألوان الثيم"""
        return THEMES.get(self.theme, THEMES[DEFAULT_THEME])
    
    def add_score(self, user_id: str, display_name: str, points: int) -> int:
        """إضافة نقاط للاعب"""
        with self._scores_lock:
            if user_id not in self.scores:
                self.scores[user_id] = {"name": display_name, "score": 0}
            
            self.scores[user_id]["score"] += points
            self.answered_users.add(user_id)
            return points
    
    def get_top_players(self, limit: int = 3) -> List[tuple]:
        """الحصول على أفضل اللاعبين"""
        with self._scores_lock:
            sorted_scores = sorted(
                self.scores.items(),
                key=lambda x: x[1]["score"],
                reverse=True
            )
            return [(data["name"], data["score"]) for _, data in sorted_scores[:limit]]
    
    def start_game(self):
        """بدء اللعبة"""
        with BaseGame._lock:
            self.current_question = 0
            self.game_active = True
            self.answered_users.clear()
            self.previous_question_text = None
            self.previous_answer_text = None
            return self.get_question()
    
    def get_question(self):
        """إنشاء السؤال - يجب تجاوزها"""
        raise NotImplementedError("يجب تطبيق get_question()")
    
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """التحقق من الإجابة - يجب تجاوزها"""
        raise NotImplementedError("يجب تطبيق check_answer()")
    
    def end_game(self) -> Dict[str, Any]:
        """إنهاء اللعبة"""
        with BaseGame._lock:
            self.game_active = False
            
            if self.scores:
                with self._scores_lock:
                    winner = max(self.scores.items(), key=lambda x: x[1]["score"])
                    winner_name = winner[1]["name"]
                    winner_score = winner[1]["score"]
            else:
                winner_name = "لا يوجد"
                winner_score = 0
            
            result_message = self._build_game_over_message(winner_name, winner_score)
            
            return {
                "message": f"🎉 انتهت اللعبة! الفائز: {winner_name}",
                "response": result_message,
                "points": 0,
                "game_over": True
            }
    
    def normalize_text(self, text: str) -> str:
        """تطبيع النص للمقارنة"""
        return normalize_arabic(text)
    
    def get_hint(self) -> str:
        """الحصول على تلميح"""
        if not self.current_answer:
            return "💡 لا يوجد تلميح"
        
        answer = str(self.current_answer)
        if isinstance(self.current_answer, list):
            answer = str(self.current_answer[0])
        
        if len(answer) > 3:
            return f"💡 يبدأ بـ: {answer[0]}\n📏 الطول: {len(answer)} حرف"
        return f"💡 يبدأ بـ: {answer[0]}"
    
    def reveal_answer(self) -> str:
        """كشف الإجابة"""
        if isinstance(self.current_answer, list):
            return f"📝 الجواب: {' أو '.join(self.current_answer)}"
        return f"📝 الجواب: {self.current_answer}"
    
    def is_expired(self, max_age_minutes: int = 30) -> bool:
        """التحقق من انتهاء الصلاحية"""
        age = (datetime.now() - self.created_at).total_seconds() / 60
        return age > max_age_minutes
    
    def cleanup(self):
        """تنظيف الموارد"""
        with self._scores_lock:
            self.scores.clear()
        self.answered_users.clear()
        self.game_active = False
        self.current_answer = None
        self.previous_question_text = None
        self.previous_answer_text = None
    
    def _create_previous_section(self, colors: Dict[str, str]) -> List[Dict]:
        """إنشاء قسم السؤال السابق الموحد"""
        if not self.previous_question_text or not self.previous_answer_text:
            return []
        
        return [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "📝 السابق:",
                        "size": "xs",
                        "color": colors["text2"],
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": self.previous_question_text[:50] + "..." if len(self.previous_question_text) > 50 else self.previous_question_text,
                        "size": "xs",
                        "color": colors["text2"],
                        "wrap": True,
                        "margin": "xs"
                    },
                    {
                        "type": "text",
                        "text": f"✅ {self.previous_answer_text[:30]}..." if len(self.previous_answer_text) > 30 else f"✅ {self.previous_answer_text}",
                        "size": "xs",
                        "color": colors["success"],
                        "wrap": True,
                        "margin": "xs"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "15px",
                "paddingAll": "10px",
                "margin": "md"
            },
            {"type": "separator", "color": colors["shadow1"], "margin": "sm"}
        ]
    
    def _create_fixed_buttons(self, colors: Dict[str, str]) -> List[Dict]:
        """إنشاء الأزرار الثابتة الموحدة"""
        buttons = []
        
        # أزرار التلميح والكشف (إذا كانت مدعومة)
        hint_reveal_row = []
        if self.supports_hint:
            hint_reveal_row.append({
                "type": "button",
                "action": {"type": "message", "label": "💡 لمّح", "text": "لمح"},
                "style": "secondary",
                "height": "sm",
                "color": colors["shadow1"]
            })
        
        if self.supports_reveal:
            hint_reveal_row.append({
                "type": "button",
                "action": {"type": "message", "label": "🔍 جاوب", "text": "جاوب"},
                "style": "secondary",
                "height": "sm",
                "color": colors["shadow1"]
            })
        
        if hint_reveal_row:
            buttons.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": hint_reveal_row
            })
        
        # زر الإيقاف
        buttons.append({
            "type": "button",
            "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
            "style": "primary",
            "height": "sm",
            "color": colors["error"]
        })
        
        # فاصل وحقوق
        buttons.extend([
            {"type": "separator", "color": colors["shadow1"], "margin": "sm"},
            {
                "type": "text",
                "text": BOT_RIGHTS,
                "size": "xxs",
                "color": colors["text2"],
                "align": "center"
            }
        ])
        
        return buttons
    
    def _create_flex_with_buttons(self, alt_text: str, flex_content: Dict) -> FlexMessage:
        """إنشاء Flex Message مع الأزرار الثابتة"""
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_content)
        )
    
    def _create_text_message(self, text: str) -> TextMessage:
        """إنشاء رسالة نصية"""
        return TextMessage(text=text)
    
    def _build_game_over_message(self, winner_name: str, winner_score: int) -> FlexMessage:
        """بناء رسالة نهاية اللعبة المحسّنة"""
        colors = self.get_theme_colors()
        
        # تحديد الأداء
        max_score = self.questions_count * POINTS_PER_CORRECT_ANSWER
        performance_ratio = winner_score / max_score if max_score > 0 else 0
        
        if performance_ratio >= 1.0:
            performance = "🏆 أداء مثالي!"
            perf_color = "#D53F8C"
        elif performance_ratio >= 0.8:
            performance = "⭐ أداء ممتاز!"
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
                "spacing": "lg",
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
                        "spacing": "md",
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
                        "paddingAll": "25px"
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
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "🔄 إعادة اللعبة",
                            "text": f"لعبة {self.game_name}"
                        },
                        "style": "primary",
                        "height": "sm",
                        "color": colors["button"]
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
    
    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": self.game_name,
            "icon": self.game_icon,
            "theme": self.theme,
            "current_question": self.current_question,
            "total_questions": self.questions_count,
            "active": self.game_active,
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "players_count": len(self.scores),
            "age_minutes": (datetime.now() - self.created_at).total_seconds() / 60
        }
    
    def __del__(self):
        """تنظيف تلقائي"""
        try:
            self.cleanup()
        except:
            pass
