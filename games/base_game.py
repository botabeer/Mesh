"""
Bot Mesh v7.0 - Base Game System
نظام الألعاب الأساسي المحسّن
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

Features:
✅ 5 Rounds Per Game
✅ 1 Point Per Correct Answer
✅ First Correct Answer Only
✅ Registered Users Only
✅ Professional 3D Glass UI
✅ Minimal Emojis
"""

from typing import Dict, Any, Optional
from datetime import datetime
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import re


class BaseGame:
    """القاعدة الأساسية لجميع الألعاب"""

    # إعدادات اللعبة
    game_name = "لعبة"
    game_icon = ""
    supports_hint = True
    supports_reveal = True
    
    # ثيمات احترافية
    THEMES = {
        "أبيض": {
            "name": "أبيض",
            "bg": "#F8FAFC",
            "card": "#FFFFFF",
            "primary": "#3B82F6",
            "secondary": "#60A5FA",
            "text": "#1E293B",
            "text2": "#64748B",
            "shadow1": "#E2E8F0",
            "button": "#3B82F6",
            "success": "#10B981",
            "error": "#EF4444"
        },
        "أسود": {
            "name": "أسود",
            "bg": "#0F172A",
            "card": "#1E293B",
            "primary": "#60A5FA",
            "secondary": "#93C5FD",
            "text": "#F1F5F9",
            "text2": "#CBD5E1",
            "shadow1": "#334155",
            "button": "#60A5FA",
            "success": "#10B981",
            "error": "#EF4444"
        },
        "أزرق": {
            "name": "أزرق",
            "bg": "#EFF6FF",
            "card": "#FFFFFF",
            "primary": "#2563EB",
            "secondary": "#3B82F6",
            "text": "#1E3A8A",
            "text2": "#3B82F6",
            "shadow1": "#BFDBFE",
            "button": "#2563EB",
            "success": "#10B981",
            "error": "#EF4444"
        }
    }

    def __init__(self, line_bot_api=None, questions_count: int = 5):
        """تهيئة اللعبة - دائماً 5 جولات"""
        self.line_bot_api = line_bot_api
        self.questions_count = 5  # ثابت: 5 جولات
        self.current_question = 0
        self.current_answer = None
        self.previous_question = None
        self.previous_answer = None
        
        self.scores: Dict[str, Dict[str, Any]] = {}
        self.answered_users = set()  # للمسجلين الذين أجابوا على السؤال الحالي
        
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
            "message": f"انتهت اللعبة\nالنقاط: {max_score}"
        }

    def add_score(self, user_id: str, display_name: str, points: int = 1) -> int:
        """إضافة نقاط (نقطة واحدة لكل إجابة صحيحة)"""
        if user_id in self.answered_users:
            return 0  # أجاب من قبل
        
        if user_id not in self.scores:
            self.scores[user_id] = {
                "name": display_name,
                "score": 0
            }
        
        # نقطة واحدة فقط
        self.scores[user_id]["score"] += 1
        self.answered_users.add(user_id)
        return 1

    def get_hint(self) -> str:
        """تلميح افتراضي"""
        if not self.current_answer:
            return "لا يوجد تلميح متاح"
        
        answer = str(self.current_answer)
        if isinstance(self.current_answer, list):
            answer = str(self.current_answer[0])
        
        return f"عدد الحروف: {len(answer)}"

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

    def _create_text_message(self, text: str) -> TextMessage:
        """إنشاء رسالة نصية"""
        return TextMessage(text=text)

    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict) -> FlexMessage:
        """إنشاء رسالة Flex"""
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_content)
        )

    def build_question_flex(self, question_text: str, additional_info: str = None) -> FlexMessage:
        """بناء واجهة السؤال"""
        colors = self.get_theme_colors()
        
        body_contents = []
        
        # قسم السؤال السابق
        if self.previous_question and self.previous_answer:
            body_contents.extend([
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "السؤال السابق:",
                            "size": "xs",
                            "color": colors["text2"],
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": str(self.previous_question)[:50],
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
                    "paddingAll": "10px",
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
        
        # أزرار التحكم
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
        
        # بناء الـ Flex
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
                                "text": f"{self.game_name}",
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
                ],
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
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": footer_buttons
                    } if footer_buttons else {"type": "spacer", "size": "xs"},
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"},
                        "style": "primary",
                        "height": "sm",
                        "color": colors["error"]
                    }
                ],
                "backgroundColor": colors["card"],
                "paddingAll": "12px"
            }
        }
        
        return self._create_flex_with_buttons(
            f"{self.game_name} - جولة {self.current_question + 1}",
            flex_content
        )

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
