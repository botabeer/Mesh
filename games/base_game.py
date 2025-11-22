"""
Bot Mesh - Base Game
Created by: Abeer Aldosari © 2025
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Set
from linebot.models import TextSendMessage
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
    
    @abstractmethod
    def start_game(self) -> Any:
        pass
    
    @abstractmethod
    def get_question(self) -> Any:
        pass
    
    @abstractmethod
    def check_answer(self, answer: str, uid: str, name: str) -> Optional[Dict[str, Any]]:
        pass
    
    def normalize_text(self, text: str) -> str:
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
        if not self.current_answer:
            return "💡 لا يوجد تلميح"
        a = str(self.current_answer)
        h = max(1, len(a) // 3)
        return f"💡 تلميح: {a[:h]}{'_' * (len(a) - h)}"
    
    def reveal_answer(self) -> str:
        return f"📍 الإجابة: {self.current_answer}"
    
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
            'response': TextSendMessage(text=msg),
            'points': 0,
            'won': bool(sorted_players)
        }
