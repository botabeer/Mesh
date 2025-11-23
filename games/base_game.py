"""
Bot Mesh - Base Game with AI Support & Dynamic Themes
Created by: Abeer Aldosari © 2025
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class PlayerScore:
    user_id: str
    display_name: str
    points: int = 0
    correct: int = 0


class BaseGame(ABC):
    def __init__(self, line_bot_api, questions_count: int = 10):
        self.line_bot_api = line_bot_api
        self.questions_count = questions_count
        self.current_question = 0
        self.current_answer = None
        self.game_active = True
        self.scores: Dict[str, PlayerScore] = {}
        self.answered_users: Set[str] = set()
        self.created_at = datetime.now()
        self.theme = "white"  # الثيم الافتراضي
        self.supports_hint = True  # دعم التلميح
        self.supports_reveal = True  # دعم كشف الإجابة
    
    @abstractmethod
    def start_game(self) -> Any:
        pass
    
    @abstractmethod
    def get_question(self) -> Any:
        pass
    
    @abstractmethod
    def check_answer(self, answer: str, uid: str, name: str) -> Optional[Dict[str, Any]]:
        pass
    
    def set_theme(self, theme_name: str):
        """تعيين الثيم للعبة"""
        self.theme = theme_name
    
    def get_theme_colors(self):
        """الحصول على ألوان الثيم الحالي"""
        from config import THEMES
        return THEMES.get(self.theme, THEMES["white"])
    
    def normalize_text(self, text: str) -> str:
        """تطبيع النص العربي"""
        if not text:
            return ""
        # إزالة التشكيل
        t = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
        # توحيد الحروف
        t = re.sub(r'[إأآا]', 'ا', t)
        t = re.sub(r'[ة]', 'ه', t)
        t = re.sub(r'[ىئ]', 'ي', t)
        return ' '.join(t.split()).strip()
    
    def add_score(self, uid: str, name: str, pts: int) -> int:
        if uid not in self.scores:
            self.scores[uid] = PlayerScore(uid, name)
        self.scores[uid].points += pts
        self.scores[uid].correct += 1
        self.answered_users.add(uid)
        return pts
    
    def get_hint(self) -> str:
        """تلميح: أول حرف وعدد الحروف"""
        if not self.current_answer:
            return "💡 لا يوجد تلميح"
        a = str(self.current_answer).strip()
        first_char = a[0]
        length = len(a)
        return f"💡 تلميح: أول حرف '{first_char}' وعدد الحروف {length}"
    
    def reveal_answer(self) -> str:
        return f"📝 الإجابة: {self.current_answer}"
    
    def next_question(self) -> Any:
        self.current_question += 1
        self.answered_users.clear()
        if self.current_question >= self.questions_count:
            return self.end_game()
        return self.get_question()
    
    def end_game(self) -> Dict[str, Any]:
        self.game_active = False
        
        sorted_players = sorted(self.scores.values(), key=lambda x: x.points, reverse=True)
        
        msg = "🏁 انتهت اللعبة!\n" + "═" * 20 + "\n\n"
        
        if sorted_players:
            msg += "🏆 النتائج:\n\n"
            medals = ["🥇", "🥈", "🥉"]
            for i, p in enumerate(sorted_players[:10]):
                medal = medals[i] if i < 3 else f"{i+1}."
                msg += f"{medal} {p.display_name}: {p.points} نقطة\n"
            msg += f"\n🎉 مبروك {sorted_players[0].display_name}!"
        else:
            msg += "لم يشارك أحد"
        
        return {
            'game_over': True,
            'message': msg,
            'response': self._create_text_message(msg),
            'points': 0,
            'won': bool(sorted_players)
        }
    
    def _create_text_message(self, text):
        """إنشاء رسالة نصية متوافقة مع LINE SDK v3"""
        from linebot.v3.messaging import TextMessage
        return TextMessage(text=text)
    
    def _create_flex_message(self, alt_text, contents):
        """إنشاء رسالة Flex متوافقة مع LINE SDK v3"""
        from linebot.v3.messaging import FlexMessage, FlexContainer
        return FlexMessage(
            altText=alt_text,
            contents=FlexContainer.from_dict(contents)
        )
    
    def _create_flex_with_buttons(self, alt_text, flex_content):
        """إنشاء Flex Message مع أزرار لمح/جاوب إذا كانت اللعبة تدعمها"""
        colors = self.get_theme_colors()
        
        # إضافة أزرار لمح/جاوب إذا كانت اللعبة تدعمها
        if self.supports_hint or self.supports_reveal:
            buttons = []
            if self.supports_hint:
                buttons.append({
                    "type": "button",
                    "action": {"type": "message", "label": "💡 لمح", "text": "لمح"},
                    "style": "secondary",
                    "color": colors.get("card", "#F1F5F9"),
                    "height": "sm"
                })
            if self.supports_reveal:
                buttons.append({
                    "type": "button",
                    "action": {"type": "message", "label": "📝 جاوب", "text": "جاوب"},
                    "style": "primary",
                    "color": colors.get("primary", "#667EEA"),
                    "height": "sm"
                })
            
            # إضافة الأزرار للـ flex content
            if "body" in flex_content and "contents" in flex_content["body"]:
                flex_content["body"]["contents"].append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": buttons,
                    "spacing": "md",
                    "margin": "xl"
                })
        
        return self._create_flex_message(alt_text, flex_content)
