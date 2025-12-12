"""
ألعاب نصية - Bot Mesh
الألعاب التي لا تتطلب إجابات صحيحة
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional
from pathlib import Path


class TextGame(BaseGame):
    """قاعدة للألعاب النصية"""
    
    def __init__(self, line_bot_api, file_name: str, game_name: str):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = game_name
        self.supports_hint = False
        self.supports_reveal = False
        self.items = self._load_items(file_name)
        
        if not self.items:
            # قائمة احتياطية في حال فشل التحميل
            self.items = [f"{game_name} - محتوى افتراضي"]
        
        random.shuffle(self.items)
        self.used_items = []
    
    def _load_items(self, file_name: str) -> list:
        """تحميل العناصر من ملف"""
        try:
            # محاولة المسار الكامل أولاً
            file_path = Path(__file__).parent / file_name
            
            if not file_path.exists():
                # محاولة المسار النسبي
                file_path = Path("games") / file_name
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_name}")
            
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
        
        return self.build_question_flex(
            question_text=item,
            additional_info=None
        )
    
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """الألعاب النصية لا تحتاج تحقق من الإجابة"""
        # يمكن إضافة منطق هنا إذا أردت تتبع الردود
        return None


class QuestionGame(TextGame):
    """لعبة سؤال - أسئلة عشوائية للنقاش"""
    
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
    """لعبة اعتراف - أسئلة اعترافات"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, "confessions.txt", "اعتراف")
