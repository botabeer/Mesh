"""
🎮 Bot Mesh v7.0 - Base Game Engine
محرك الألعاب الأساسي - يدعم الفردي والمجموعة
Created by: Abeer Aldosari © 2025
"""

import random
import re
from datetime import datetime
from typing import Dict, Any, Optional, List
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage

# ============================================================================
# محرك اللعبة الأساسي
# ============================================================================

class BaseGame:
    """محرك اللعبة الأساسي - يدعم الفردي والمجموعة"""
    
    def __init__(self, line_bot_api=None, questions_count: int = 5):
        """
        تهيئة اللعبة
        
        Args:
            line_bot_api: واجهة LINE Bot API (اختياري)
            questions_count: عدد الأسئلة
        """
        self.line_bot_api = line_bot_api
        self.questions_count = questions_count
        
        # معلومات اللعبة (يجب تعيينها في الألعاب الفرعية)
        self.game_name = "لعبة"
        self.game_icon = "🎮"
        
        # حالة اللعبة
        self.game_active = False
        self.current_question = 0
        self.current_answer = None
        
        # النقاط واللاعبين
        self.scores: Dict[str, Dict[str, Any]] = {}
        self.answered_users: set = set()
        
        # التوقيت
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        
        # دعم AI (اختياري)
        self.ai_generate_question = None
        self.ai_check_answer = None
        
        # دعم التلميحات والكشف
        self.supports_hint = True
        self.supports_reveal = True
        
        # الثيمات
        self.theme_emoji = "💜"

    # ========================================================================
    # Core Game Methods
    # ========================================================================

    def start_game(self):
        """بدء اللعبة - يجب تطبيقها في الألعاب الفرعية"""
        self.current_question = 0
        self.game_active = True
        self.answered_users.clear()
        return self.get_question()
    
    def start(self):
        """Alias لـ start_game"""
        return self.start_game()

    def get_question(self):
        """الحصول على السؤال الحالي - يجب تطبيقها في الألعاب الفرعية"""
        raise NotImplementedError("يجب تطبيق get_question في اللعبة")

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """فحص الإجابة - يجب تطبيقها في الألعاب الفرعية"""
        raise NotImplementedError("يجب تطبيق check_answer في اللعبة")

    # ========================================================================
    # Score Management
    # ========================================================================

    def add_score(self, user_id: str, display_name: str, points: int) -> int:
        """إضافة نقاط للاعب"""
        if user_id not in self.scores:
            self.scores[user_id] = {
                "name": display_name,
                "points": 0,
                "correct_answers": 0
            }
        
        self.scores[user_id]["points"] += points
        self.scores[user_id]["correct_answers"] += 1
        self.answered_users.add(user_id)
        self.last_activity = datetime.now()
        
        return self.scores[user_id]["points"]

    def get_score(self, user_id: str) -> int:
        """الحصول على نقاط لاعب"""
        return self.scores.get(user_id, {}).get("points", 0)

    # ========================================================================
    # Game End
    # ========================================================================

    def end_game(self) -> Dict[str, Any]:
        """إنهاء اللعبة وإرجاع النتائج"""
        self.game_active = False
        
        # ترتيب اللاعبين حسب النقاط
        sorted_players = sorted(
            self.scores.items(),
            key=lambda x: x[1]["points"],
            reverse=True
        )
        
        # بناء رسالة النتائج
        if sorted_players:
            winner_id, winner_data = sorted_players[0]
            message = f"🏆 الفائز: {winner_data['name']}\n⭐ النقاط: {winner_data['points']}"
            
            if len(sorted_players) > 1:
                message += "\n\n📊 الترتيب:"
                for i, (uid, data) in enumerate(sorted_players[:5], 1):
                    message += f"\n{i}. {data['name']} - {data['points']} نقطة"
        else:
            message = "🎮 انتهت اللعبة!"
        
        return {
            "game_over": True,
            "message": message,
            "scores": dict(sorted_players),
            "response": self._create_text_message(message)
        }

    # ========================================================================
    # Helper Methods
    # ========================================================================

    def normalize_text(self, text: str) -> str:
        """تطبيع النص العربي"""
        if not text:
            return ""
        
        text = text.strip().lower()
        
        # إزالة التشكيل
        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
        
        # توحيد الحروف
        replacements = {
            'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ء': 'ا',
            'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text

    def get_hint(self) -> str:
        """الحصول على تلميح - يمكن تطبيقها في الألعاب الفرعية"""
        if not self.current_answer:
            return "💡 لا يوجد تلميح متاح"
        
        answer = str(self.current_answer)
        if isinstance(self.current_answer, list):
            answer = self.current_answer[0]
        
        if len(answer) > 2:
            return f"💡 الإجابة تبدأ بـ: {answer[0]}\n📏 الطول: {len(answer)} حرف"
        return f"💡 الإجابة تبدأ بـ: {answer[0]}"

    def is_expired(self, max_minutes: int = 30) -> bool:
        """هل انتهت صلاحية اللعبة؟"""
        elapsed = (datetime.now() - self.last_activity).total_seconds() / 60
        return elapsed > max_minutes

    # ========================================================================
    # UI Helpers
    # ========================================================================

    def get_theme_colors(self) -> Dict[str, str]:
        """الحصول على ألوان الثيم"""
        themes = {
            "💜": {
                "primary": "#8B5CF6", "secondary": "#A78BFA",
                "bg": "#FAF5FF", "card": "#F3E8FF",
                "text": "#1F2937", "text2": "#6B7280",
                "success": "#10B981", "error": "#EF4444",
                "shadow1": "#E9D5FF", "shadow2": "#DDD6FE"
            },
            "💚": {
                "primary": "#10B981", "secondary": "#34D399",
                "bg": "#F0FDF4", "card": "#D1FAE5",
                "text": "#1F2937", "text2": "#6B7280",
                "success": "#10B981", "error": "#EF4444",
                "shadow1": "#A7F3D0", "shadow2": "#6EE7B7"
            },
            "🤍": {
                "primary": "#3B82F6", "secondary": "#60A5FA",
                "bg": "#FFFFFF", "card": "#F3F4F6",
                "text": "#1F2937", "text2": "#6B7280",
                "success": "#10B981", "error": "#EF4444",
                "shadow1": "#DBEAFE", "shadow2": "#BFDBFE"
            }
        }
        
        return themes.get(self.theme_emoji, themes["💜"])

    def _create_text_message(self, text: str) -> TextMessage:
        """إنشاء رسالة نصية"""
        return TextMessage(text=text)

    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict) -> FlexMessage:
        """إنشاء Flex Message مع أزرار"""
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_content)
        )

    # ========================================================================
    # AI Integration (Optional)
    # ========================================================================

    def set_ai_generate_question(self, func):
        """تعيين دالة AI لتوليد الأسئلة"""
        self.ai_generate_question = func

    def set_ai_check_answer(self, func):
        """تعيين دالة AI للتحقق من الإجابات"""
        self.ai_check_answer = func


# ============================================================================
# Aliases للتوافق مع الألعاب القديمة
# ============================================================================

Game = BaseGame  # للتوافق مع الألعاب القديمة
