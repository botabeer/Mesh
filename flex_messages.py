"""
Bot Mesh - Flex Messages System
Created by: Abeer Aldosari © 2025
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class Theme(Enum):
    WHITE = "white"
    BLACK = "black"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"


@dataclass
class ThemeColors:
    name: str
    name_ar: str
    emoji: str
    bg: str
    card: str
    accent: str
    text: str
    text2: str


THEMES: Dict[Theme, ThemeColors] = {
    Theme.WHITE: ThemeColors("white", "⚪ أبيض", "⚪", "#E8EBF5", "#FFFFFF", "#667EEA", "#2C3E50", "#95A5A6"),
    Theme.BLACK: ThemeColors("black", "⚫ أسود", "⚫", "#0F0F1A", "#1A1A2E", "#00D9FF", "#FFFFFF", "#A0AEC0"),
    Theme.BLUE: ThemeColors("blue", "💙 أزرق", "💙", "#0A1628", "#0F2744", "#00D9FF", "#E0F2FE", "#7DD3FC"),
    Theme.PURPLE: ThemeColors("purple", "💜 بنفسجي", "💜", "#1A0F3E", "#3730A3", "#A855F7", "#F5F3FF", "#C4B5FD"),
    Theme.PINK: ThemeColors("pink", "🌸 وردي", "🌸", "#FFF1F2", "#FFFFFF", "#F43F5E", "#881337", "#BE123C"),
}


class FlexMessageBuilder:
    def __init__(self, theme: Theme = Theme.WHITE):
        self.theme = THEMES.get(theme, THEMES[Theme.WHITE])
    
    def set_theme(self, name: str):
        for t in Theme:
            if t.value == name.lower():
                self.theme = THEMES[t]
                return
    
    # ==========================================
    # نافذة البداية - الرئيسية (عند المنشن/بداية)
    # ==========================================
    def create_start_screen(self) -> Dict:
        """نافذة البداية الرئيسية مع قائمة الألعاب"""
        games = [
            {"cmd": "ذكاء", "emoji": "🧠", "name": "اختبار الذكاء"},
            {"cmd": "لون", "emoji": "🎨", "name": "الكلمة واللون"},
            {"cmd": "ترتيب", "emoji": "🔤", "name": "ترتيب الحروف"},
            {"cmd": "تكوين", "emoji": "✏️", "name": "تكوين الكلمات"},
            {"cmd": "سلسلة", "emoji": "⛓️", "name": "سلسلة الكلمات"},
            {"cmd": "أسرع", "emoji": "⚡", "name": "الكتابة السريعة"},
            {"cmd": "لعبة", "emoji": "🎯", "name": "إنسان حيوان نبات"},
            {"cmd": "خمن", "emoji": "🤔", "name": "خمن الكلمة"},
            {"cmd": "ضد", "emoji": "↔️", "name": "الأضداد"},
            {"cmd": "توافق", "emoji": "💖", "name": "نسبة التوافق"},
            {"cmd": "أغنية", "emoji": "🎵", "name": "خمن الأغنية"},
        ]
        
        # إنشاء أزرار الألعاب (صفين)
        game_rows = []
        for i in range(0, len(games), 3):
            row_games = games[i:i+3]
            row = {
                "type": "box", "layout": "horizontal", "spacing": "sm",
                "margin": "md" if i > 0 else "none",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": g["emoji"], "text": g["cmd"]},
                        "style": "secondary", "height": "sm", "flex": 1
                    } for g in row_games
                ]
            }
            game_rows.append(row)
        
        return {
            "type": "bubble", "size": "mega",
            "header": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.accent, "paddingAll": "20px",
                "contents": [
                    {"type": "text", "text": "🎮", "size": "xxl", "align": "center"},
                    {"type": "text", "text": "Bot Mesh", "size": "xl", "weight": "bold",
                     "color": "#FFFFFF", "align": "center"},
                    {"type": "text", "text": "بوت الألعاب الترفيهية", "size": "sm",
                     "color": "#FFFFFFCC", "align": "center"}
                ]
            },
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.bg, "paddingAll": "20px", "spacing": "md",
                "contents": [
                    # قسم الألعاب
                    {"type": "text", "text": "🎯 اختر لعبة", "size": "lg", "weight": "bold",
                     "color": self.theme.text, "align": "center"},
                    
                    *game_rows,
                    
                    {"type": "separator", "margin": "xl", "color": self.theme.text2 + "30"},
                    
                    # أزرار التحكم الرئيسية
                    {"type": "text", "text": "⚙️ التحكم", "size": "md", "weight": "bold",
                     "color": self.theme.text, "align": "center", "margin": "lg"},
                    
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm", "margin": "md",
                        "contents": [
                            {"type": "button", "style": "primary", "height": "sm",
                             "color": self.theme.accent,
                             "action": {"type": "message", "label": "📊 نقاطي", "text": "نقاطي"}},
                            {"type": "button", "style": "primary", "height": "sm",
                             "color": self.theme.accent,
                             "action": {"type": "message", "label": "🏆 الصدارة", "text": "الصدارة"}},
                        ]
                    },
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                        "contents": [
                            {"type": "button", "style": "secondary", "height": "sm",
                             "action": {"type": "message", "label": "🎨 ثيم", "text": "ثيم"}},
                            {"type": "button", "style": "secondary", "height": "sm",
                             "action": {"type": "message", "label": "❓ مساعدة", "text": "مساعدة"}},
                        ]
                    },
                    
                    {"type": "text", "text": "تم إنشاء هذا البوت بواسطة عبير الدوسري",
                     "size": "xxs", "color": self.theme.text2, "align": "center", "margin": "xl"}
                ]
            }
        }
    
    # ==========================================
    # نافذة المساعدة - دليل الاستخدام
    # ==========================================
    def create_help_screen(self) -> Dict:
        """نافذة دليل الاستخدام"""
        commands = [
            {"cmd": "انضم", "desc": "التسجيل في البوت"},
            {"cmd": "انسحب", "desc": "إلغاء التسجيل"},
            {"cmd": "نقاطي", "desc": "عرض إحصائياتك"},
            {"cmd": "الصدارة", "desc": "أفضل اللاعبين"},
            {"cmd": "إيقاف", "desc": "إنهاء اللعبة الحالية"},
        ]
        
        play_commands = [
            {"cmd": "لمح", "desc": "الحصول على تلميح"},
            {"cmd": "جاوب", "desc": "عرض الإجابة الصحيحة"},
        ]
        
        cmd_rows = []
        for c in commands:
            cmd_rows.append({
                "type": "box", "layout": "horizontal", "margin": "md",
                "contents": [
                    {"type": "text", "text": c["desc"], "size": "sm",
                     "color": self.theme.text2, "flex": 3},
                    {"type": "box", "layout": "vertical", "flex": 2,
                     "backgroundColor": self.theme.accent + "20", "cornerRadius": "8px",
                     "paddingAll": "5px",
                     "contents": [
                         {"type": "text", "text": c["cmd"], "size": "sm", "weight": "bold",
                          "color": self.theme.text, "align": "center"}
                     ]}
                ]
            })
        
        play_rows = []
        for c in play_commands:
            play_rows.append({
                "type": "box", "layout": "horizontal", "margin": "md",
                "contents": [
                    {"type": "text", "text": c["desc"], "size": "sm",
                     "color": self.theme.text2, "flex": 3},
                    {"type": "box", "layout": "vertical", "flex": 2,
                     "backgroundColor": self.theme.accent + "20", "cornerRadius": "8px",
                     "paddingAll": "5px",
                     "contents": [
                         {"type": "text", "text": c["cmd"], "size": "sm", "weight": "bold",
                          "color": self.theme.text, "align": "center"}
                     ]}
                ]
            })
        
        return {
            "type": "bubble", "size": "mega",
            "header": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.accent, "paddingAll": "20px",
                "contents": [
                    {"type": "text", "text": "دليل الاستخدام", "size": "xl",
                     "weight": "bold", "color": "#FFFFFF", "align": "center"}
                ]
            },
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.bg, "paddingAll": "20px", "spacing": "none",
                "contents": [
                    {"type": "text", "text": "الأوامر الأساسية", "size": "lg", "weight": "bold",
                     "color": self.theme.text, "align": "end"},
                    *cmd_rows,
                    
                    {"type": "separator", "margin": "xl", "color": self.theme.text2 + "30"},
                    
                    {"type": "text", "text": "أثناء اللعب", "size": "lg", "weight": "bold",
                     "color": self.theme.text, "align": "end", "margin": "lg"},
                    *play_rows,
                    
                    {"type": "separator", "margin": "xl", "color": self.theme.text2 + "30"},
                    
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm", "margin": "xl",
                        "contents": [
                            {"type": "button", "style": "primary", "height": "sm",
                             "color": self.theme.accent,
                             "action": {"type": "message", "label": "انضم", "text": "انضم"}},
                            {"type": "button", "style": "secondary", "height": "sm",
                             "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"}},
                            {"type": "button", "style": "secondary", "height": "sm",
                             "action": {"type": "message", "label": "الصدارة", "text": "الصدارة"}},
                        ]
                    },
                    
                    {"type": "text", "text": "تم إنشاء هذا البوت بواسطة عبير الدوسري",
                     "size": "xxs", "color": self.theme.text2, "align": "center", "margin": "lg"}
                ]
            }
        }
    
    # ==========================================
    # نافذة الإحصائيات
    # ==========================================
    def create_stats_card(self, user_data: Dict, rank: int = 0) -> Dict:
        if not user_data:
            return self._error_screen("لم تلعب بعد! اكتب 'انضم' للبدء")
        
        points = user_data.get('total_points', 0)
        games = user_data.get('games_played', 0)
        wins = user_data.get('wins', 0)
        rate = (wins / games * 100) if games > 0 else 0
        registered = user_data.get('is_registered', False)
        level = self._get_level(points)
        
        return {
            "type": "bubble", "size": "mega",
            "header": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.accent, "paddingAll": "20px",
                "contents": [
                    {"type": "text", "text": level['emoji'], "size": "xxl", "align": "center"},
                    {"type": "text", "text": level['name'], "size": "xl", "weight": "bold",
                     "color": "#FFFFFF", "align": "center"},
                    {"type": "text", "text": f"المركز #{rank}" if rank else "غير مصنف",
                     "size": "sm", "color": "#FFFFFFCC", "align": "center"}
                ]
            },
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.bg, "paddingAll": "20px", "spacing": "md",
                "contents": [
                    # الإحصائيات
                    {
                        "type": "box", "layout": "horizontal", "spacing": "md",
                        "contents": [
                            self._stat_box("💰", str(points), "نقطة"),
                            self._stat_box("🎮", str(games), "لعبة"),
                        ]
                    },
                    {
                        "type": "box", "layout": "horizontal", "spacing": "md", "margin": "md",
                        "contents": [
                            self._stat_box("🏆", str(wins), "فوز"),
                            self._stat_box("📈", f"{rate:.0f}%", "نسبة"),
                        ]
                    },
                    
                    # حالة التسجيل
                    {
                        "type": "box", "layout": "vertical", "margin": "lg",
                        "backgroundColor": self.theme.card, "cornerRadius": "15px",
                        "paddingAll": "15px",
                        "contents": [
                            {"type": "text", "align": "center",
                             "text": "✅ مسجل - يمكنك اللعب!" if registered else "⚠️ غير مسجل - اكتب 'انضم'",
                             "size": "sm", "weight": "bold",
                             "color": "#48BB78" if registered else "#F6AD55"}
                        ]
                    },
                    
                    # أزرار
                    {
                        "type": "box", "layout": "horizontal", "spacing": "sm", "margin": "xl",
                        "contents": [
                            {"type": "button", "style": "primary", "height": "sm",
                             "color": self.theme.accent,
                             "action": {"type": "message", "label": "🎮 العب", "text": "بداية"}},
                            {"type": "button", "style": "secondary", "height": "sm",
                             "action": {"type": "message", "label": "🏆 الصدارة", "text": "الصدارة"}},
                        ]
                    }
                ]
            }
        }
    
    def _stat_box(self, emoji: str, value: str, label: str) -> Dict:
        return {
            "type": "box", "layout": "vertical", "flex": 1,
            "backgroundColor": self.theme.card, "cornerRadius": "15px",
            "paddingAll": "15px", "spacing": "xs",
            "contents": [
                {"type": "text", "text": emoji, "size": "xl", "align": "center"},
                {"type": "text", "text": value, "size": "xl", "weight": "bold",
                 "color": self.theme.text, "align": "center"},
                {"type": "text", "text": label, "size": "xs",
                 "color": self.theme.text2, "align": "center"}
            ]
        }
    
    def _get_level(self, points: int) -> Dict:
        if points < 100: return {'name': 'مبتدئ', 'emoji': '🌱'}
        if points < 500: return {'name': 'متوسط', 'emoji': '⭐'}
        if points < 1000: return {'name': 'محترف', 'emoji': '🔥'}
        if points < 5000: return {'name': 'أسطوري', 'emoji': '👑'}
        return {'name': 'خارق', 'emoji': '💎'}
    
    # ==========================================
    # لوحة الصدارة
    # ==========================================
    def create_leaderboard(self, leaders: List[Dict]) -> Dict:
        if not leaders:
            return self._error_screen("لا توجد بيانات")
        
        medals = ["🥇", "🥈", "🥉"]
        rows = []
        
        for i, l in enumerate(leaders[:10]):
            medal = medals[i] if i < 3 else f"#{i+1}"
            rows.append({
                "type": "box", "layout": "horizontal", "margin": "md",
                "backgroundColor": self.theme.card if i < 3 else "transparent",
                "cornerRadius": "10px", "paddingAll": "10px",
                "contents": [
                    {"type": "text", "text": medal, "size": "lg" if i < 3 else "md", "flex": 1},
                    {"type": "text", "text": l.get('display_name', 'لاعب'),
                     "size": "md", "weight": "bold" if i < 3 else "regular",
                     "color": self.theme.text, "flex": 3},
                    {"type": "text", "text": f"{l.get('total_points', 0)} ⭐",
                     "size": "md", "color": self.theme.accent if i < 3 else self.theme.text2,
                     "align": "end", "flex": 2}
                ]
            })
        
        return {
            "type": "bubble", "size": "mega",
            "header": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.accent, "paddingAll": "20px",
                "contents": [
                    {"type": "text", "text": "🏆 لوحة الصدارة", "size": "xl",
                     "weight": "bold", "color": "#FFFFFF", "align": "center"},
                    {"type": "text", "text": f"أفضل {len(leaders)} لاعبين",
                     "size": "sm", "color": "#FFFFFFCC", "align": "center"}
                ]
            },
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.bg, "paddingAll": "20px",
                "contents": rows + [
                    {
                        "type": "button", "style": "secondary", "height": "sm", "margin": "xl",
                        "action": {"type": "message", "label": "🎮 العب الآن", "text": "بداية"}
                    }
                ]
            }
        }
    
    # ==========================================
    # اختيار الثيم
    # ==========================================
    def create_theme_selector(self) -> Dict:
        rows = []
        for t in THEMES.values():
            rows.append({
                "type": "box", "layout": "horizontal", "margin": "sm",
                "backgroundColor": self.theme.card, "cornerRadius": "15px",
                "paddingAll": "15px",
                "action": {"type": "message", "text": f"ثيم:{t.name}"},
                "contents": [
                    {"type": "box", "layout": "vertical", "flex": 0,
                     "backgroundColor": t.accent, "cornerRadius": "10px",
                     "width": "40px", "height": "40px", "justifyContent": "center",
                     "contents": [
                         {"type": "text", "text": t.emoji, "align": "center"}
                     ]},
                    {"type": "text", "text": t.name_ar, "size": "md", "weight": "bold",
                     "color": self.theme.text, "margin": "lg", "gravity": "center"}
                ]
            })
        
        return {
            "type": "bubble", "size": "mega",
            "header": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.accent, "paddingAll": "20px",
                "contents": [
                    {"type": "text", "text": "🎨 اختر الثيم", "size": "xl",
                     "weight": "bold", "color": "#FFFFFF", "align": "center"}
                ]
            },
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.bg, "paddingAll": "20px",
                "contents": rows
            }
        }
    
    # ==========================================
    # رسالة خطأ
    # ==========================================
    def _error_screen(self, msg: str) -> Dict:
        return {
            "type": "bubble",
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.bg, "paddingAll": "30px", "spacing": "md",
                "contents": [
                    {"type": "text", "text": "⚠️", "size": "xxl", "align": "center"},
                    {"type": "text", "text": msg, "size": "md",
                     "color": self.theme.text, "align": "center", "wrap": True},
                    {"type": "button", "style": "primary", "height": "sm", "margin": "xl",
                     "color": self.theme.accent,
                     "action": {"type": "message", "label": "انضم الآن", "text": "انضم"}}
                ]
            }
        }


flex_builder = FlexMessageBuilder()
