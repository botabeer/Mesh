"""
لعبة التوافق - نسخة محدثة ومحسّنة
Created by: Abeer Aldosari © 2025

تحديثات:
- استيراد صحيح من games.base_game
- خوارزمية حساب محسّنة
- رسائل توافق مخصصة
- دعم ثيمات ديناميكية
- رسائل Flex حديثة بتصميم Neumorphism
"""

# ============================================================================
# الاستيراد الصحيح
# ============================================================================
from games.base_game import BaseGame  # ✅ صحيح

from typing import Dict, Any, Optional


class CompatibilityGame(BaseGame):
    """
    لعبة التوافق - قياس التوافق بين اسمين
    
    الميزات:
    - خوارزمية حساب ذكية
    - رسائل توافق متدرجة
    - لعبة من جولة واحدة
    - رسائل Flex حديثة بتصميم Neumorphism
    - دعم 6 ثيمات مختلفة
    """
    
    def __init__(self, line_bot_api):
        """
        تهيئة اللعبة
        
        المعاملات:
            line_bot_api: واجهة LINE Bot API
        """
        # استدعاء الكلاس الأساسي (جولة واحدة فقط)
        super().__init__(line_bot_api, questions_count=1)
        
        # هذه اللعبة لا تدعم التلميح/الكشف
        self.supports_hint = False
        self.supports_reveal = False

    def calculate_compatibility(self, name1: str, name2: str) -> int:
        """
        حساب نسبة التوافق بين اسمين
        
        المعاملات:
            name1: الاسم الأول
            name2: الاسم الثاني
            
        العودة:
            int: نسبة التوافق (20-100)
        """
        # تنظيف الأسماء
        name1_clean = self.normalize_text(name1)
        name2_clean = self.normalize_text(name2)
        
        # دمج الأسماء وترتيبها
        combined = ''.join(sorted(name1_clean + name2_clean))
        
        # حساب seed فريد
        seed = sum(ord(c) * (i + 1) for i, c in enumerate(combined))
        
        # إرجاع نسبة بين 20 و 100
        return (seed % 81) + 20

    def get_compatibility_message(self, percentage: int) -> str:
        """
        الحصول على رسالة التوافق حسب النسبة
        
        المعاملات:
            percentage: نسبة التوافق
            
        العودة:
            str: رسالة التوافق
        """
        if percentage >= 90:
            return "✨ توافق رائع جداً! علاقة مثالية"
        elif percentage >= 75:
            return "💪 توافق ممتاز! علاقة قوية"
        elif percentage >= 60:
            return "🌟 توافق جيد! علاقة واعدة"
        elif percentage >= 45:
            return "🔧 توافق متوسط! يحتاج عمل"
        else:
            return "⚠️ توافق ضعيف! قد تكون هناك تحديات"

    def start_game(self) -> Any:
        """
        بدء اللعبة وإرجاع السؤال
        
        العودة:
            FlexMessage: السؤال
        """
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def get_question(self) -> Any:
        """
        إنشاء وإرجاع رسالة Flex للسؤال
        
        العودة:
            FlexMessage: السؤال بتصميم Neumorphism
        """
        # الحصول على ألوان الثيم الحالي
        colors = self.get_theme_colors()
        
        # بناء محتوى Flex Message
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💕 لعبة التوافق",
                        "size": "xl",
                        "weight": "bold",
                        "color": colors["text"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "اكتشف نسبة التوافق!",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "sm"
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
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📝 اكتب اسمين مفصولين بمسافة",
                                "size": "lg",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": "مثال: أحمد سارة",
                                "size": "md",
                                "color": colors["text2"],
                                "align": "center",
                                "margin": "md"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "💘",
                                "size": "xl",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": "قد تكون النتيجة للترفيه فقط!",
                                "size": "xs",
                                "color": colors["text2"],
                                "flex": 1,
                                "margin": "sm",
                                "wrap": True
                            }
                        ],
                        "margin": "lg"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    {
                        "type": "text",
                        "text": "⚠️ لا تدعم: لمح • جاوب",
                        "size": "xxs",
                        "color": "#FF6B6B",
                        "align": "center",
                        "margin": "md"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                }
            }
        }
        
        return self._create_flex_with_buttons("لعبة التوافق", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """
        التحقق من إجابة اللاعب
        
        المعاملات:
            user_answer: إجابة المستخدم
            user_id: معرف المستخدم
            display_name: اسم المستخدم
            
        العودة:
            dict: نتيجة الإجابة
        """
        # التحقق من حالة اللعبة
        if not self.game_active:
            return None

        # تقسيم الأسماء
        names = user_answer.strip().split()
        
        # التحقق من وجود اسمين
        if len(names) < 2:
            hint = "⚠️ يرجى كتابة اسمين مفصولين بمسافة\nمثال: أحمد سارة"
            return {
                'message': hint,
                'response': self._create_text_message(hint),
                'points': 0
            }
        
        # أخذ أول اسمين فقط
        name1, name2 = names[0], names[1]
        
        # حساب نسبة التوافق
        percentage = self.calculate_compatibility(name1, name2)
        message_text = self.get_compatibility_message(percentage)
        
        # الحصول على ألوان الثيم
        colors = self.get_theme_colors()
        
        # بناء نافذة النتيجة
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "💕 نتيجة التوافق",
                        "size": "xl",
                        "weight": "bold",
                        "color": "#FFFFFF",
                        "align": "center"
                    }
                ],
                "backgroundColor": "#FF69B4",
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"{name1} 💘 {name2}",
                                "size": "xl",
                                "weight": "bold",
                                "color": colors["text"],
                                "align": "center"
                            },
                            {
                                "type": "separator",
                                "margin": "lg"
                            },
                            {
                                "type": "text",
                                "text": "نسبة التوافق:",
                                "size": "sm",
                                "color": colors["text2"],
                                "align": "center",
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": f"{percentage}%",
                                "size": "xxl",
                                "weight": "bold",
                                "color": "#FF69B4",
                                "align": "center",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": message_text,
                                "size": "md",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "margin": "lg"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "20px",
                        "paddingAll": "25px"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            }
        }
        
        result_message = self._create_flex_with_buttons("نتيجة التوافق", flex_content)
        
        # إضافة نقاط رمزية
        points = self.add_score(user_id, display_name, 5)
        
        # إنهاء اللعبة (لأنها جولة واحدة)
        self.game_active = False
        
        return {
            'message': f"💕 تم حساب التوافق بين {name1} و {name2}",
            'response': result_message,
            'points': points,
            'game_over': True
        }

    def get_game_info(self) -> Dict[str, Any]:
        """
        الحصول على معلومات اللعبة
        
        العودة:
            dict: معلومات اللعبة
        """
        return {
            "name": "لعبة التوافق",
            "emoji": "💕",
            "description": "اكتشف نسبة التوافق بين اسمين",
            "questions_count": 1,
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }


# ============================================================================
# مثال على الاستخدام
# ============================================================================
if __name__ == "__main__":
    """
    مثال على كيفية استخدام اللعبة
    """
    print("✅ ملف لعبة التوافق جاهز للاستخدام!")
    print("📝 تأكد من استخدام: from games.base_game import BaseGame")
