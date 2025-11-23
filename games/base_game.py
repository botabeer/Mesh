"""
Bot Mesh - Base Game Enhanced (Silent & Professional)
Created by: Abeer Aldosari © 2025
بدون إيموجي إلا للضرورة + ألوان احترافية
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import re
import logging
from linebot.v3.messaging import TextMessage, FlexMessage, FlexContainer

logger = logging.getLogger(__name__)

# ==================== THEMES ====================
THEMES = {
    'white': {'bg': '#E0E5EC', 'card': '#D1D9E6', 'primary': '#667EEA', 'text': '#1A202C', 'text2': '#4A5568'},
    'black': {'bg': '#0F0F1A', 'card': '#1A1A2E', 'primary': '#00D9FF', 'text': '#F7FAFC', 'text2': '#CBD5E0'},
    'gray': {'bg': '#2D3748', 'card': '#4A5568', 'primary': '#68D391', 'text': '#F7FAFC', 'text2': '#E2E8F0'},
    'blue': {'bg': '#1E3A8A', 'card': '#1E40AF', 'primary': '#60A5FA', 'text': '#F0F9FF', 'text2': '#BFDBFE'},
    'green': {'bg': '#14532D', 'card': '#166534', 'primary': '#4ADE80', 'text': '#F0FDF4', 'text2': '#BBF7D0'},
    'pink': {'bg': '#FFF1F2', 'card': '#FFE4E6', 'primary': '#EC4899', 'text': '#831843', 'text2': '#9F1239'},
    'orange': {'bg': '#431407', 'card': '#7C2D12', 'primary': '#FB923C', 'text': '#FFF7ED', 'text2': '#FDBA74'},
    'purple': {'bg': '#3B0764', 'card': '#581C87', 'primary': '#C084FC', 'text': '#FAF5FF', 'text2': '#E9D5FF'},
    'brown': {'bg': '#1C0A00', 'card': '#44403C', 'primary': '#A78BFA', 'text': '#FAFAF9', 'text2': '#D6D3D1'}
}

class BaseGame(ABC):
    """
    لعبة أساسية محسّنة:
    - 5 جولات
    - بدون إيموجي إلا للضرورة
    - ألوان احترافية ثري دي
    - صامت (لا يرد إلا على المسجلين)
    """
    
    def __init__(self, line_api):
        self.line_api = line_api
        self.rounds = 5
        self.current_round = 0
        self.current_answer = None
        self.game_active = True
        self.scores = {}
        self.answered_users = set()
        self.theme = 'white'
        self.supports_hint = True
        self.supports_reveal = True
    
    @abstractmethod
    def start_game(self):
        pass
    
    @abstractmethod
    def generate_question(self):
        pass
    
    @abstractmethod
    def check_answer(self, answer: str, uid: str, name: str) -> Optional[Dict[str, Any]]:
        pass
    
    def set_theme(self, theme_name: str):
        self.theme = theme_name
    
    def get_theme_colors(self):
        return THEMES.get(self.theme, THEMES['white'])
    
    def normalize_text(self, text: str) -> str:
        if not text:
            return ""
        t = re.sub(r'[\u0617-\u061A\u064B-\u0652]', '', text)
        t = re.sub(r'[إأآا]', 'ا', t)
        t = re.sub(r'[ة]', 'ه', t)
        t = re.sub(r'[ىئ]', 'ي', t)
        return ' '.join(t.split()).strip()
    
    def add_score(self, uid: str, name: str, points: int) -> int:
        if uid not in self.scores:
            self.scores[uid] = {'name': name, 'points': 0}
        self.scores[uid]['points'] += points
        self.answered_users.add(uid)
        return points
    
    def get_hint(self) -> str:
        """تلميح: أول حرف + عدد الحروف"""
        if not self.current_answer:
            return "لا يوجد تلميح"
        answer = str(self.current_answer).strip()
        first_char = answer[0]
        length = len(answer)
        return f"تلميح | أول حرف: {first_char} | عدد الحروف: {length}"
    
    def reveal_answer(self) -> str:
        return f"الإجابة الصحيحة: {self.current_answer}"
    
    def next_round(self):
        self.current_round += 1
        self.answered_users.clear()
        
        if self.current_round >= self.rounds:
            return self.end_game()
        
        return self.generate_question()
    
    def end_game(self) -> Dict[str, Any]:
        self.game_active = False
        
        if not self.scores:
            return {
                'game_over': True,
                'response': self.create_text_message("انتهت اللعبة | لم يشارك أحد"),
                'points': 0
            }
        
        sorted_players = sorted(self.scores.items(), key=lambda x: x[1]['points'], reverse=True)
        winner = sorted_players[0]
        
        result_flex = self.create_result_flex(sorted_players)
        
        return {
            'game_over': True,
            'response': result_flex,
            'winner_uid': winner[0],
            'winner_name': winner[1]['name'],
            'winner_points': winner[1]['points'],
            'points': winner[1]['points']
        }
    
    def create_text_message(self, text: str):
        return TextMessage(text=text)
    
    def create_flex_message(self, alt_text: str, contents: dict):
        return FlexMessage(altText=alt_text, contents=FlexContainer.from_dict(contents))
    
    def create_question_flex(self, title: str, question: str, extra_info: str = ""):
        """نافذة سؤال بدون إيموجي"""
        colors = self.get_theme_colors()
        
        contents = [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "size": "xl",
                "color": colors['primary'],
                "align": "center"
            },
            {
                "type": "text",
                "text": f"الجولة {self.current_round + 1} من {self.rounds}",
                "size": "sm",
                "color": colors['text2'],
                "align": "center",
                "margin": "sm"
            },
            {
                "type": "separator",
                "margin": "md"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": question,
                        "size": "lg",
                        "color": colors['text'],
                        "wrap": True,
                        "weight": "bold",
                        "align": "center"
                    }
                ],
                "backgroundColor": colors['card'],
                "cornerRadius": "20px",
                "paddingAll": "20px",
                "margin": "md"
            }
        ]
        
        if extra_info:
            contents.append({
                "type": "text",
                "text": extra_info,
                "size": "sm",
                "color": colors['text2'],
                "align": "center",
                "margin": "md",
                "wrap": True
            })
        
        # أزرار لمح/جاوب
        if self.supports_hint or self.supports_reveal:
            buttons = []
            if self.supports_hint:
                buttons.append({
                    "type": "button",
                    "action": {"type": "message", "label": "تلميح", "text": "لمح"},
                    "style": "secondary",
                    "color": colors['card'],
                    "height": "sm",
                    "flex": 1
                })
            if self.supports_reveal:
                buttons.append({
                    "type": "button",
                    "action": {"type": "message", "label": "كشف الإجابة", "text": "جاوب"},
                    "style": "secondary",
                    "color": colors['card'],
                    "height": "sm",
                    "flex": 1
                })
            
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": buttons,
                "spacing": "sm",
                "margin": "lg"
            })
        
        flex_content = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px",
                "backgroundColor": colors['bg']
            },
            "styles": {
                "body": {"backgroundColor": colors['bg']}
            }
        }
        
        return self.create_flex_message(title, flex_content)
    
    def create_result_flex(self, sorted_players):
        """نافذة النتائج النهائية"""
        colors = self.get_theme_colors()
        winner = sorted_players[0]
        
        contents = [
            {
                "type": "text",
                "text": "انتهت اللعبة",
                "weight": "bold",
                "size": "xxl",
                "color": colors['primary'],
                "align": "center"
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "الفائز",
                        "size": "sm",
                        "color": colors['text2'],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": winner[1]['name'],
                        "size": "xxl",
                        "weight": "bold",
                        "color": colors['primary'],
                        "align": "center",
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": f"{winner[1]['points']} نقطة",
                        "size": "lg",
                        "color": colors['text'],
                        "align": "center",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": colors['card'],
                "cornerRadius": "20px",
                "paddingAll": "20px",
                "margin": "lg"
            },
            {
                "type": "separator",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "النتائج النهائية",
                "size": "md",
                "weight": "bold",
                "color": colors['text'],
                "align": "center",
                "margin": "md"
            }
        ]
        
        ranks = ["الأول", "الثاني", "الثالث"]
        for i, (uid, data) in enumerate(sorted_players[:10]):
            rank = ranks[i] if i < 3 else f"المركز {i+1}"
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": rank, "size": "xs", "color": colors['text2'], "flex": 2},
                    {"type": "text", "text": data['name'], "size": "sm", "color": colors['text'], "flex": 3},
                    {"type": "text", "text": str(data['points']), "size": "sm", "color": colors['primary'], "weight": "bold", "align": "end", "flex": 1}
                ],
                "margin": "sm"
            })
        
        contents.append({
            "type": "button",
            "action": {"type": "message", "label": "القائمة الرئيسية", "text": "مساعدة"},
            "style": "primary",
            "color": colors['primary'],
            "margin": "lg"
        })
        
        flex_content = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px",
                "backgroundColor": colors['bg']
            },
            "styles": {
                "body": {"backgroundColor": colors['bg']}
            }
        }
        
        return self.create_flex_message("النتائج", flex_content)
