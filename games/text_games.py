"""
العاب نصية - Bot Mesh
الالعاب التي لا تتطلب اجابات صحيحة
"""

from games.base_game import BaseGame
from linebot.v3.messaging import FlexMessage, FlexContainer
import random
from typing import Dict, Any, Optional
from pathlib import Path


class TextGame(BaseGame):
    """قاعدة للالعاب النصية"""
    
    def __init__(self, line_bot_api, file_name: str, game_name: str):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = game_name
        self.supports_hint = False
        self.supports_reveal = False
        self.items = self._load_items(file_name)
        
        if not self.items:
            self.items = [f"{game_name} - محتوى افتراضي"]
        
        random.shuffle(self.items)
        self.used_items = []
    
    def _load_items(self, file_name: str) -> list:
        """تحميل العناصر من ملف"""
        try:
            file_path = Path(__file__).parent / file_name
            
            if not file_path.exists():
                file_path = Path("games") / file_name
            
            if not file_path.exists():
                return []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                items = [line.strip() for line in f if line.strip()]
            
            return items
        except Exception as e:
            print(f"Error loading {file_name}: {e}")
            return []
    
    def start_game(self):
        """بدء اللعبة"""
        self.game_active = True
        return self.get_question()
    
    def get_question(self):
        """اختيار عنصر عشوائي"""
        available = [item for item in self.items if item not in self.used_items]
        
        if not available:
            self.used_items.clear()
            random.shuffle(self.items)
            available = self.items.copy()
        
        item = random.choice(available)
        self.used_items.append(item)
        
        # استخدام build_question_flex من BaseGame
        colors = self.get_theme_colors()
        
        flex_dict = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": self.game_name,
                        "size": "xxl",
                        "weight": "bold",
                        "color": colors["primary"],
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": colors["border"]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": item,
                                "size": "lg",
                                "color": colors["text"],
                                "align": "center",
                                "wrap": True,
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "20px",
                        "borderWidth": "2px",
                        "borderColor": colors["primary"],
                        "margin": "lg"
                    },
                    {
                        "type": "separator",
                        "margin": "xl",
                        "color": colors["border"]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "lg",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "اعادة",
                                    "text": self.game_name
                                },
                                "style": "primary",
                                "height": "sm",
                                "color": colors["primary"]
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "بداية",
                                    "text": "بداية"
                                },
                                "style": "secondary",
                                "height": "sm"
                            }
                        ]
                    }
                ],
                "paddingAll": "24px",
                "backgroundColor": colors["bg"]
            }
        }
        
        return FlexMessage(
            alt_text=f"{self.game_name}: {item[:50]}",
            contents=FlexContainer.from_dict(flex_dict)
        )
    
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """الالعاب النصية لا تحتاج تحقق من الاجابة"""
        return None


class QuestionGame(TextGame):
    """لعبة سؤال - اسئلة عشوائية للنقاش"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, "questions.txt", "سؤال")


class MentionGame(TextGame):
    """لعبة منشن - طلبات منشن عشوائية"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, "mentions.txt", "منشن")


class ChallengeGame(TextGame):
    """لعبة تحدي - تحديات ممتعة"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, "challenges.txt", "تحدي")


class ConfessionGame(TextGame):
    """لعبة اعتراف - اسئلة اعترافات"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, "confessions.txt", "اعتراف")
