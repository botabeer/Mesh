"""
🎮 Bot Mesh v3.2 - Enhanced Base Game System (NO AI)
نظام الألعاب الأساسي المحسّن بدون AI
Created by: Abeer Aldosari © 2025

Features:
- عرض السؤال والإجابة السابقة
- أول إجابة صحيحة فقط
- دعم كامل للثيمات
- أزرار مخصصة حسب نوع اللعبة
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import re


class BaseGame:
    """
    القاعدة الأساسية المحسّنة لجميع الألعاب
    """

    # إعدادات اللعبة
    game_name = "لعبة"
    game_icon = "🎮"
    supports_hint = True
    supports_reveal = True
    
    # ثيمات احترافية محسّنة
    THEMES = {
        "أبيض": {
            "name": "أبيض",
            "bg": "#F7FAFC",
            "card": "#FFFFFF",
            "primary": "#4299E1",
            "secondary": "#63B3ED",
            "text": "#2D3748",
            "text2": "#718096",
            "shadow1": "#E2E8F0",
            "shadow2": "#FFFFFF",
            "button": "#4299E1",
            "success": "#48BB78",
            "error": "#EF4444"
        },
        "أسود": {
            "name": "أسود",
            "bg": "#1A202C",
            "card": "#2D3748",
            "primary": "#667EEA",
            "secondary": "#7F9CF5",
            "text": "#F7FAFC",
            "text2": "#CBD5E0",
            "shadow1": "#4A5568",
            "shadow2": "#414D5F",
            "button": "#667EEA",
            "success": "#48BB78",
            "error": "#EF4444"
        },
        "رمادي": {
            "name": "رمادي",
            "bg": "#F7FAFC",
            "card": "#FFFFFF",
            "primary": "#4A5568",
            "secondary": "#718096",
            "text": "#2D3748",
            "text2": "#718096",
            "shadow1": "#E2E8F0",
            "shadow2": "#FFFFFF",
            "button": "#4A5568",
            "success": "#48BB78",
            "error": "#EF4444"
        },
        "أزرق": {
            "name": "أزرق",
            "bg": "#EBF8FF",
            "card": "#FFFFFF",
            "primary": "#2B6CB0",
            "secondary": "#3182CE",
            "text": "#2C5282",
            "text2": "#2B6CB0",
            "shadow1": "#BEE3F8",
            "shadow2": "#FFFFFF",
            "button": "#2B6CB0",
            "success": "#48BB78",
            "error": "#EF4444"
        },
        "بنفسجي": {
            "name": "بنفسجي",
            "bg": "#FAF5FF",
            "card": "#FFFFFF",
            "primary": "#805AD5",
            "secondary": "#9F7AEA",
            "text": "#5B21B6",
            "text2": "#7C3AED",
            "shadow1": "#DDD6FE",
            "shadow2": "#FFFFFF",
            "button": "#805AD5",
            "success": "#48BB78",
            "error": "#EF4444"
        },
        "وردي": {
            "name": "وردي",
            "bg": "#FFF5F7",
            "card": "#FFFFFF",
            "primary": "#B83280",
            "secondary": "#D53F8C",
            "text": "#702459",
            "text2": "#97266D",
            "shadow1": "#FED7E2",
            "shadow2": "#FFFFFF",
            "button": "#B83280",
            "success": "#48BB78",
            "error": "#EF4444"
        },
        "أخضر": {
            "name": "أخضر",
            "bg": "#F0FDF4",
            "card": "#FFFFFF",
            "primary": "#38A169",
            "secondary": "#48BB78",
            "text": "#064E3B",
            "text2": "#065F46",
            "shadow1": "#A7F3D0",
            "shadow2": "#FFFFFF",
            "button": "#38A169",
            "success": "#48BB78",
            "error": "#EF4444"
        },
        "برتقالي": {
            "name": "برتقالي",
            "bg": "#FFFAF0",
            "card": "#FFFFFF",
            "primary": "#C05621",
            "secondary": "#DD6B20",
            "text": "#7C2D12",
            "text2": "#9C4221",
            "shadow1": "#FEEBC8",
            "shadow2": "#FFFFFF",
            "button": "#C05621",
            "success": "#48BB78",
            "error": "#EF4444"
        },
        "بني": {
            "name": "بني",
            "bg": "#FEFCF9",
            "card": "#FFFFFF",
            "primary": "#744210",
            "secondary": "#8B4513",
            "text": "#5C2E00",
            "text2": "#7A4F1D",
            "shadow1": "#E6D5C3",
            "shadow2": "#FFFFFF",
            "button": "#744210",
            "success": "#48BB78",
            "error": "#EF4444"
        }
    }

    def __init__(self, line_bot_api=None, questions_count: int = 5):
        """تهيئة اللعبة"""
        self.line_bot_api = line_bot_api
        self.questions_count = questions_count
        self.current_question = 0
        self.current_answer = None
        self.previous_question = None
        self.previous_answer = None
        
        self.scores: Dict[str, Dict[str, Any]] = {}
        self.answered_users = set()
        
        self.game_active = False
        self.game_start_time: Optional[datetime] = None
        self.current_theme = "أبيض"

    # ===== دورة حياة اللعبة =====
    
    def start_game(self):
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
        return {
            "text": "سؤال تجريبي",
            "round": self.current_question + 1,
            "total_rounds": self.questions_count
        }

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """يجب تنفيذه في الألعاب الفرعية"""
        return None

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
        """إضافة نقاط للاعب (أول إجابة فقط)"""
        if user_id in self.answered_users:
            return 0
        
        if user_id not in self.scores:
            self.scores[user_id] = {
                "name": display_name,
                "score": 0
            }
        
        self.scores[user_id]["score"] += points
        self.answered_users.add(user_id)
        return points

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

    def get_theme_colors(self, theme_name: str = None) -> Dict[str, str]:
        """الحصول على ألوان الثيم"""
        if theme_name is None:
            theme_name = self.current_theme
        return self.THEMES.get(theme_name, self.THEMES["أبيض"])
    
    def set_theme(self, theme_name: str):
        """تعيين ثيم اللعبة"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name

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
        additional_info: str = None
    ) -> FlexMessage:
        """بناء واجهة السؤال بتصميم احترافي مع السؤال السابق"""
        colors = self.get_theme_colors()
        
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
                            "text": f"✅ الإجابة: {self.previous_answer}",
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
                "action": {"type": "message", "label": "💡 لمح", "text": "لمح"},
                "style": "secondary",
                "height": "sm",
                "color": colors["shadow1"]
            })
        
        if self.supports_reveal:
            footer_buttons.append({
                "type": "button",
                "action": {"type": "message", "label": "🔍 جاوب", "text": "جاوب"},
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
