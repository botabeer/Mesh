"""
🎮 Bot Mesh v7.0 - Enhanced Base Game System
نظام الألعاب الأساسي المحسّن مع تصميم احترافي
Created by: Abeer Aldosari © 2025
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import re


class BaseGame:
    """
    القاعدة الأساسية المحسّنة لجميع الألعاب
    مع دعم كامل للثيمات والتصميم الاحترافي
    """

    # إعدادات اللعبة
    game_name = "لعبة"
    game_icon = "🎮"
    supports_hint = True
    supports_reveal = True
    
    # ثيمات احترافية محسّنة
    THEMES = {
        "أزرق": {
            "primary": "#0EA5E9",
            "secondary": "#38BDF8",
            "bg": "#F0F9FF",
            "card": "#E0F2FE",
            "text": "#0C4A6E",
            "text2": "#075985",
            "success": "#10B981",
            "error": "#EF4444",
            "shadow1": "#94A3B8",
            "shadow2": "#CBD5E1"
        },
        "أسود": {
            "primary": "#60A5FA",
            "secondary": "#818CF8",
            "bg": "#0F172A",
            "card": "#1E293B",
            "text": "#F1F5F9",
            "text2": "#CBD5E1",
            "success": "#34D399",
            "error": "#F87171",
            "shadow1": "#475569",
            "shadow2": "#334155"
        },
        "بنفسجي": {
            "primary": "#A78BFA",
            "secondary": "#C4B5FD",
            "bg": "#FAF5FF",
            "card": "#F3E8FF",
            "text": "#5B21B6",
            "text2": "#7C3AED",
            "success": "#10B981",
            "error": "#EF4444",
            "shadow1": "#DDD6FE",
            "shadow2": "#E9D5FF"
        },
        "وردي": {
            "primary": "#EC4899",
            "secondary": "#F472B6",
            "bg": "#FFF1F2",
            "card": "#FFE4EC",
            "text": "#831843",
            "text2": "#9D174D",
            "success": "#10B981",
            "error": "#EF4444",
            "shadow1": "#FBCFE8",
            "shadow2": "#FCE7F3"
        },
        "أخضر": {
            "primary": "#10B981",
            "secondary": "#34D399",
            "bg": "#F0FDF4",
            "card": "#D1FAE5",
            "text": "#064E3B",
            "text2": "#065F46",
            "success": "#059669",
            "error": "#EF4444",
            "shadow1": "#A7F3D0",
            "shadow2": "#BBF7D0"
        }
    }

    def __init__(self, questions_count: int = 5):
        self.questions_count = questions_count
        self.current_question = 0
        self.current_answer = None
        self.previous_question = None
        self.previous_answer = None
        
        self.scores: Dict[str, Dict[str, Any]] = {}
        self.answered_users = set()
        
        self.game_active = False
        self.game_start_time: Optional[datetime] = None
        
        # دعم AI (اختياري)
        self.ai_generate_question = None
        self.ai_check_answer = None

    # ===== دورة حياة اللعبة =====
    
    def start(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.scores.clear()
        self.answered_users.clear()
        self.previous_question = None
        self.previous_answer = None
        self.game_active = True
        self.game_start_time = datetime.now()
        return self.get_question()

    def get_question(self) -> Dict[str, Any]:
        """يجب تنفيذه في الألعاب الفرعية"""
        raise NotImplementedError("يجب تنفيذ get_question")

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Dict[str, Any]:
        """يجب تنفيذه في الألعاب الفرعية"""
        raise NotImplementedError("يجب تنفيذ check_answer")

    def end_game(self) -> Dict[str, Any]:
        """إنهاء اللعبة وإرجاع النتائج"""
        self.game_active = False
        
        if not self.scores:
            return {
                "game_over": True,
                "points": 0,
                "message": "انتهت اللعبة"
            }
        
        # حساب أعلى نقاط
        max_score = max(s["score"] for s in self.scores.values())
        
        return {
            "game_over": True,
            "points": max_score,
            "message": f"🎉 انتهت اللعبة!\nالنقاط: {max_score}"
        }

    # ===== إدارة النقاط =====
    
    def add_score(self, user_id: str, display_name: str, points: int = 10) -> int:
        """إضافة نقاط للاعب"""
        if user_id not in self.scores:
            self.scores[user_id] = {
                "name": display_name,
                "score": 0
            }
        
        self.scores[user_id]["score"] += points
        self.answered_users.add(user_id)
        return self.scores[user_id]["score"]

    # ===== التلميحات =====
    
    def get_hint(self) -> str:
        """تلميح افتراضي"""
        if not self.current_answer:
            return "💡 لا يوجد تلميح متاح"
        
        answer = str(self.current_answer)
        if isinstance(self.current_answer, list):
            answer = str(self.current_answer[0])
        
        return f"💡 عدد الحروف: {len(answer)}"

    # ===== أدوات مساعدة =====
    
    def normalize_text(self, text: str) -> str:
        """تطبيع النص العربي"""
        if not text:
            return ""
        
        text = text.strip().lower()
        
        # تطبيع الحروف العربية
        replacements = {
            'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
            'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # إزالة التشكيل
        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
        
        return text

    def get_theme_colors(self, theme_name: str = "أزرق") -> Dict[str, str]:
        """الحصول على ألوان الثيم"""
        return self.THEMES.get(theme_name, self.THEMES["أزرق"])

    # ===== بناء الواجهات =====
    
    def _create_text_message(self, text: str) -> TextMessage:
        """إنشاء رسالة نصية بسيطة"""
        return TextMessage(text=text)

    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict) -> FlexMessage:
        """إنشاء رسالة Flex"""
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_content)
        )

    def build_question_flex(
        self,
        question_text: str,
        theme_name: str = "أزرق",
        additional_info: str = None
    ) -> FlexMessage:
        """بناء واجهة السؤال بتصميم احترافي"""
        colors = self.get_theme_colors(theme_name)
        
        # محتوى الـ body
        body_contents = []
        
        # قسم السؤال السابق (إذا وُجد)
        if self.previous_question and self.previous_answer:
            body_contents.extend([
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "📝 السؤال السابق:",
                            "size": "xs",
                            "color": colors["text2"],
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": str(self.previous_question)[:100],
                            "size": "xs",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "xs"
                        },
                        {
                            "type": "text",
                            "text": f"✅ {self.previous_answer}",
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
            ])
        
        # السؤال الحالي
        body_contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": question_text,
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
            "margin": "md"
        })
        
        # معلومات إضافية (اختياري)
        if additional_info:
            body_contents.append({
                "type": "text",
                "text": additional_info,
                "size": "xs",
                "color": colors["text2"],
                "align": "center",
                "wrap": True,
                "margin": "md"
            })
        
        # أزرار التحكم
        footer_buttons = []
        
        if self.supports_hint:
            footer_buttons.append({
                "type": "button",
                "action": {"type": "message", "label": "💡 تلميح", "text": "لمح"},
                "style": "secondary",
                "height": "sm",
                "color": colors["shadow1"]
            })
        
        if self.supports_reveal:
            footer_buttons.append({
                "type": "button",
                "action": {"type": "message", "label": "🔍 إجابة", "text": "جاوب"},
                "style": "secondary",
                "height": "sm",
                "color": colors["shadow1"]
            })
        
        # بناء الـ Flex النهائي
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
                                "text": f"جولة {self.current_question + 1}/{self.questions_count}",
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
                "contents": body_contents,
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
                        "contents": footer_buttons
                    } if footer_buttons else {"type": "spacer", "size": "xs"},
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
        
        return self._create_flex_with_buttons(
            f"{self.game_name} - جولة {self.current_question + 1}",
            flex_content
        )

    # ===== معلومات اللعبة =====
    
    def get_game_info(self) -> Dict[str, Any]:
        """معلومات اللعبة"""
        return {
            "name": self.game_name,
            "icon": self.game_icon,
            "questions_count": self.questions_count,
            "current_question": self.current_question,
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "active": self.game_active,
            "players_count": len(self.scores)
        }
