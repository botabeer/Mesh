"""
Bot Mesh v7.1 - Base Game System PROFESSIONAL
نظام الألعاب الأساسي المحسّن
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

✅ تصميم زجاجي احترافي موحد
✅ بدون إيموجي زائد
✅ أداء محسّن
"""

from typing import Dict, Any, Optional
from datetime import datetime
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import re


class BaseGame:
    """القاعدة الأساسية المحسّنة لجميع الألعاب"""

    game_name = "لعبة"
    game_icon = ""
    supports_hint = True
    supports_reveal = True
    
    # 9 ثيمات زجاجية احترافية (رمادي بدلاً من سماوي)
    THEMES = {
        "أبيض": {
            "bg": "#F8FAFC", "card": "#FFFFFF", "primary": "#3B82F6",
            "text": "#1E293B", "text2": "#64748B", "shadow1": "#E2E8F0",
            "success": "#10B981", "error": "#EF4444"
        },
        "أسود": {
            "bg": "#0F172A", "card": "#1E293B", "primary": "#60A5FA",
            "text": "#F1F5F9", "text2": "#CBD5E1", "shadow1": "#334155",
            "success": "#10B981", "error": "#EF4444"
        },
        "أزرق": {
            "bg": "#EFF6FF", "card": "#FFFFFF", "primary": "#2563EB",
            "text": "#1E3A8A", "text2": "#3B82F6", "shadow1": "#BFDBFE",
            "success": "#10B981", "error": "#EF4444"
        },
        "أخضر": {
            "bg": "#F0FDF4", "card": "#FFFFFF", "primary": "#10B981",
            "text": "#064E3B", "text2": "#059669", "shadow1": "#D1FAE5",
            "success": "#10B981", "error": "#EF4444"
        },
        "وردي": {
            "bg": "#FDF2F8", "card": "#FFFFFF", "primary": "#EC4899",
            "text": "#831843", "text2": "#DB2777", "shadow1": "#FCE7F3",
            "success": "#10B981", "error": "#EF4444"
        },
        "بنفسجي": {
            "bg": "#F5F3FF", "card": "#FFFFFF", "primary": "#8B5CF6",
            "text": "#4C1D95", "text2": "#7C3AED", "shadow1": "#EDE9FE",
            "success": "#10B981", "error": "#EF4444"
        },
        "برتقالي": {
            "bg": "#FFF7ED", "card": "#FFFFFF", "primary": "#F97316",
            "text": "#7C2D12", "text2": "#EA580C", "shadow1": "#FFEDD5",
            "success": "#10B981", "error": "#EF4444"
        },
        "رمادي": {
            "bg": "#F9FAFB", "card": "#FFFFFF", "primary": "#6B7280",
            "text": "#111827", "text2": "#6B7280", "shadow1": "#E5E7EB",
            "success": "#10B981", "error": "#EF4444"
        },
        "ذهبي": {
            "bg": "#FFFBEB", "card": "#FFFFFF", "primary": "#F59E0B",
            "text": "#78350F", "text2": "#D97706", "shadow1": "#FEF3C7",
            "success": "#10B981", "error": "#EF4444"
        }
    }

    def __init__(self, line_bot_api=None, questions_count: int = 5):
        self.line_bot_api = line_bot_api
        self.questions_count = 5
        self.current_question = 0
        self.current_answer = None
        self.previous_question = None
        self.previous_answer = None
        self.scores: Dict[str, Dict[str, Any]] = {}
        self.answered_users = set()
        self.game_active = False
        self.game_start_time: Optional[datetime] = None
        self.current_theme = "أبيض"

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

    def get_question(self):
        """الحصول على السؤال - يجب تطبيقه في الألعاب الفرعية"""
        return {"text": "سؤال", "round": self.current_question + 1}

    def check_answer(self, user_answer: str, user_id: str, display_name: str):
        """التحقق من الإجابة - يجب تطبيقه في الألعاب الفرعية"""
        return None

    def end_game(self) -> Dict[str, Any]:
        """إنهاء اللعبة"""
        self.game_active = False
        if not self.scores:
            return {"game_over": True, "points": 0, "message": "انتهت اللعبة"}
        max_score = max(s["score"] for s in self.scores.values())
        return {"game_over": True, "points": max_score, "message": f"انتهت اللعبة • النقاط: {max_score}"}

    def add_score(self, user_id: str, display_name: str, points: int = 1) -> int:
        """إضافة نقاط للمستخدم"""
        if user_id in self.answered_users:
            return 0
        if user_id not in self.scores:
            self.scores[user_id] = {"name": display_name, "score": 0}
        self.scores[user_id]["score"] += 1
        self.answered_users.add(user_id)
        return 1

    def get_hint(self) -> str:
        """الحصول على تلميح"""
        if not self.current_answer:
            return "لا يوجد تلميح"
        answer = str(self.current_answer[0] if isinstance(self.current_answer, list) else self.current_answer)
        return f"عدد الحروف: {len(answer)}"

    def normalize_text(self, text: str) -> str:
        """تنظيف وتوحيد النص"""
        if not text:
            return ""
        text = text.strip().lower()
        replacements = {
            'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي',
            'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return re.sub(r'[\u064B-\u065F\u0670]', '', text)

    def get_theme_colors(self, theme_name: str = None):
        """الحصول على ألوان الثيم"""
        return self.THEMES.get(theme_name or self.current_theme, self.THEMES["أبيض"])
    
    def set_theme(self, theme_name: str):
        """تعيين الثيم"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name

    def _create_text_message(self, text: str):
        """إنشاء رسالة نصية"""
        return TextMessage(text=text)

    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict):
        """إنشاء رسالة Flex"""
        return FlexMessage(alt_text=alt_text, contents=FlexContainer.from_dict(flex_content))

    def build_question_flex(self, question_text: str, additional_info: str = None):
        """بناء واجهة السؤال الموحدة - تصميم احترافي"""
        colors = self.get_theme_colors()
        
        # Header
        header_contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": self.game_name,
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
        ]
        
        # Body
        body_contents = []
        
        # السؤال السابق (إن وجد)
        if self.previous_question and self.previous_answer:
            body_contents.extend([
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "السؤال السابق",
                            "size": "xs",
                            "color": colors["text2"],
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": str(self.previous_question)[:60],
                            "size": "xs",
                            "color": colors["text2"],
                            "wrap": True,
                            "margin": "xs"
                        },
                        {
                            "type": "text",
                            "text": f"الإجابة: {self.previous_answer}",
                            "size": "xs",
                            "color": colors["success"],
                            "wrap": True,
                            "margin": "xs"
                        }
                    ],
                    "backgroundColor": colors["card"],
                    "cornerRadius": "10px",
                    "paddingAll": "10px"
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
            "cornerRadius": "15px",
            "paddingAll": "20px",
            "margin": "md"
        })
        
        # معلومات إضافية
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
        
        # Footer
        footer_buttons = []
        if self.supports_hint:
            footer_buttons.append({
                "type": "button",
                "action": {"type": "message", "label": "لمح", "text": "لمح"},
                "style": "secondary",
                "height": "sm",
                "color": colors["shadow1"]
            })
        if self.supports_reveal:
            footer_buttons.append({
                "type": "button",
                "action": {"type": "message", "label": "جاوب", "text": "جاوب"},
                "style": "secondary",
                "height": "sm",
                "color": colors["shadow1"]
            })
        
        footer_contents = []
        if footer_buttons:
            footer_contents.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": footer_buttons
            })
        
        footer_contents.append({
            "type": "button",
            "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"},
            "style": "primary",
            "height": "sm",
            "color": colors["error"],
            "margin": "sm" if footer_buttons else "none"
        })
        
        # Bubble Structure
        flex_content = {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": header_contents,
                "backgroundColor": colors["card"],
                "paddingAll": "15px"
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
                "contents": footer_contents,
                "backgroundColor": colors["card"],
                "paddingAll": "12px"
            },
            "styles": {
                "header": {"backgroundColor": colors["card"]},
                "body": {"backgroundColor": colors["bg"]},
                "footer": {"backgroundColor": colors["card"]}
            }
        }
        
        return self._create_flex_with_buttons(
            f"{self.game_name} - جولة {self.current_question + 1}",
            flex_content
        )

    def get_game_info(self):
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
