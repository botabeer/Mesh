"""Bot Mesh - Flex Builder Fixed | Abeer Aldosari © 2025"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class Theme(Enum):
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"
    MINT = "mint"

@dataclass
class ThemeColors:
    name: str
    name_ar: str
    emoji: str
    background: str
    surface: str
    card: str
    text_primary: str
    text_secondary: str
    accent: str
    accent_dark: str
    shadow_light: str
    shadow_dark: str

THEMES: Dict[Theme, ThemeColors] = {
    Theme.WHITE: ThemeColors(
        name="white", name_ar="⚪ أبيض", emoji="⚪",
        background="#E0E5EC", surface="#E0E5EC", card="#D1D9E6",
        text_primary="#2C3E50", text_secondary="#7F8C8D",
        accent="#667EEA", accent_dark="#5A67D8",
        shadow_light="#FFFFFF", shadow_dark="#A3B1C6"
    ),
    Theme.BLACK: ThemeColors(
        name="black", name_ar="⚫ أسود", emoji="⚫",
        background="#1A1A2E", surface="#16213E", card="#0F3460",
        text_primary="#FFFFFF", text_secondary="#A0AEC0",
        accent="#00D9FF", accent_dark="#00B8D4",
        shadow_light="#2A2A4A", shadow_dark="#0D0D1A"
    ),
    Theme.GRAY: ThemeColors(
        name="gray", name_ar="🔘 رمادي", emoji="🔘",
        background="#2D3748", surface="#4A5568", card="#1A202C",
        text_primary="#F7FAFC", text_secondary="#CBD5E0",
        accent="#68D391", accent_dark="#48BB78",
        shadow_light="#4A5568", shadow_dark="#1A202C"
    ),
    Theme.BLUE: ThemeColors(
        name="blue", name_ar="💙 أزرق", emoji="💙",
        background="#0C1929", surface="#1E3A5F", card="#0F2744",
        text_primary="#E0F2FE", text_secondary="#7DD3FC",
        accent="#0EA5E9", accent_dark="#0284C7",
        shadow_light="#1E4976", shadow_dark="#061224"
    ),
    Theme.PURPLE: ThemeColors(
        name="purple", name_ar="💜 بنفسجي", emoji="💜",
        background="#1E1B4B", surface="#312E81", card="#3730A3",
        text_primary="#F5F3FF", text_secondary="#C4B5FD",
        accent="#A855F7", accent_dark="#9333EA",
        shadow_light="#4338CA", shadow_dark="#0F0A2E"
    ),
    Theme.PINK: ThemeColors(
        name="pink", name_ar="🌸 وردي", emoji="🌸",
        background="#FFF1F2", surface="#FFE4E6", card="#FECDD3",
        text_primary="#881337", text_secondary="#BE123C",
        accent="#F43F5E", accent_dark="#E11D48",
        shadow_light="#FFFFFF", shadow_dark="#FBBBC9"
    ),
    Theme.MINT: ThemeColors(
        name="mint", name_ar="🍃 نعناعي", emoji="🍃",
        background="#ECFDF5", surface="#D1FAE5", card="#A7F3D0",
        text_primary="#065F46", text_secondary="#059669",
        accent="#10B981", accent_dark="#059669",
        shadow_light="#FFFFFF", shadow_dark="#6EE7B7"
    )
}

class FlexBuilder:
    def __init__(self, theme: Theme = Theme.WHITE):
        self.theme = THEMES.get(theme, THEMES[Theme.WHITE])
    
    def set_theme(self, theme_name: str):
        theme_map = {
            'white': Theme.WHITE, 'أبيض': Theme.WHITE,
            'black': Theme.BLACK, 'أسود': Theme.BLACK,
            'gray': Theme.GRAY, 'رمادي': Theme.GRAY,
            'blue': Theme.BLUE, 'أزرق': Theme.BLUE,
            'purple': Theme.PURPLE, 'بنفسجي': Theme.PURPLE,
            'pink': Theme.PINK, 'وردي': Theme.PINK,
            'mint': Theme.MINT, 'نعناعي': Theme.MINT
        }
        theme = theme_map.get(theme_name.lower(), Theme.WHITE)
        self.theme = THEMES[theme]
    
    def _btn(self, text: str, action: str, color: str = None, style: str = "primary") -> Dict:
        return {
            "type": "button",
            "action": {"type": "message", "label": text, "text": action},
            "style": style,
            "color": color or self.theme.accent,
            "height": "sm"
        }
    
    def _text(self, text: str, size: str = "md", weight: str = "regular", 
              color: str = None, wrap: bool = True) -> Dict:
        return {
            "type": "text",
            "text": text,
            "size": size,
            "weight": weight,
            "color": color or self.theme.text_primary,
            "wrap": wrap
        }

    def create_help_menu(self) -> Dict:
        """نافذة المساعدة - مُصلحة"""
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🎮 Bot Mesh", "size": "xl", "weight": "bold", "color": "#FFFFFF"},
                    {"type": "text", "text": "بوت الألعاب الترفيهية", "size": "xs", "color": "#E0E0E0"}
                ],
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # العنوان
                    {
                        "type": "text",
                        "text": "🚀 كيف تبدأ؟",
                        "size": "lg",
                        "weight": "bold",
                        "color": self.theme.text_primary,
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "1. اضغط 'انضم' للتسجيل\n2. اختر لعبة من الأزرار الثابتة",
                        "size": "sm",
                        "color": self.theme.text_secondary,
                        "wrap": True,
                        "margin": "sm"
                    },
                    
                    # الأوامر السريعة
                    {
                        "type": "text",
                        "text": "⚡ الأوامر السريعة",
                        "size": "md",
                        "weight": "bold",
                        "color": self.theme.text_primary,
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._btn("📊 نقاطي", "نقاطي", self.theme.accent),
                            self._btn("🏆 الصدارة", "الصدارة", self.theme.accent_dark),
                            self._btn("🎨 الثيمات", "ثيم", self.theme.text_secondary),
                        ],
                        "spacing": "sm",
                        "margin": "md"
                    },
                    
                    # المميزات
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "text", "text": "✨ ماذا ستحصل؟", "size": "sm", "weight": "bold", "color": self.theme.text_primary},
                            {"type": "text", "text": "• 13 لعبة متنوعة\n• 7 ثيمات جميلة\n• نظام نقاط وترتيب\n• لوحة صدارة عالمية", 
                             "size": "xs", "color": self.theme.text_secondary, "wrap": True, "margin": "sm"}
                        ],
                        "backgroundColor": self.theme.card,
                        "cornerRadius": "15px",
                        "paddingAll": "15px",
                        "margin": "lg"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "Created by Abeer Aldosari © 2025", "size": "xxs", "color": self.theme.text_secondary}
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "10px"
            }
        }

    def create_games_menu(self) -> Dict:
        """قائمة الألعاب"""
        games = [
            {'key': 'ذكاء', 'emoji': '🧠', 'name': 'اختبار الذكاء'},
            {'key': 'لون', 'emoji': '🎨', 'name': 'لعبة الألوان'},
            {'key': 'سلسلة', 'emoji': '⛓️', 'name': 'سلسلة الكلمات'},
            {'key': 'ترتيب', 'emoji': '🔤', 'name': 'ترتيب الحروف'},
            {'key': 'تكوين', 'emoji': '✏️', 'name': 'تكوين الكلمات'},
            {'key': 'أسرع', 'emoji': '⚡', 'name': 'الكتابة السريعة'},
            {'key': 'لعبة', 'emoji': '🎯', 'name': 'إنسان حيوان نبات'},
            {'key': 'خمن', 'emoji': '🤔', 'name': 'خمن الكلمة'},
            {'key': 'توافق', 'emoji': '💖', 'name': 'نسبة التوافق'},
            {'key': 'ضد', 'emoji': '↔️', 'name': 'الأضداد'},
            {'key': 'أغنية', 'emoji': '🎵', 'name': 'خمن الأغنية'},
        ]
        
        game_buttons = []
        for g in games:
            game_buttons.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": g['emoji'], "size": "xl", "flex": 0},
                    {"type": "text", "text": g['name'], "size": "sm", "weight": "bold", "flex": 1, "margin": "md"},
                    {"type": "text", "text": "▶", "size": "md", "color": self.theme.accent, "flex": 0}
                ],
                "action": {"type": "message", "text": g['key']},
                "backgroundColor": self.theme.card,
                "cornerRadius": "12px",
                "paddingAll": "md",
                "spacing": "sm",
                "margin": "sm" if game_buttons else "none"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🎮 اختر اللعبة", "size": "xl", "weight": "bold", "color": "#FFFFFF"},
                    {"type": "text", "text": "11 لعبة ممتعة", "size": "xs", "color": "#E0E0E0"}
                ],
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": game_buttons,
                "backgroundColor": self.theme.background,
                "paddingAll": "15px"
            }
        }

    def create_theme_selector(self) -> Dict:
        """نافذة اختيار الثيمات"""
        theme_buttons = []
        for theme_enum, theme_data in THEMES.items():
            theme_buttons.append(
                self._btn(theme_data.name_ar, f"ثيم:{theme_data.name}", theme_data.accent)
            )
        
        return {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🎨 اختر الثيم المفضل", "size": "xl", "weight": "bold", "color": "#FFFFFF"},
                    {"type": "text", "text": "7 ثيمات مميزة", "size": "xs", "color": "#E0E0E0"}
                ],
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": theme_buttons,
                "backgroundColor": self.theme.background,
                "paddingAll": "15px",
                "spacing": "sm"
            }
        }

    def create_stats_card(self, user_data: Dict, rank: int = 0) -> Dict:
        """بطاقة الإحصائيات"""
        if not user_data:
            return {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "⚠️", "size": "xxl", "color": self.theme.accent},
                        {"type": "text", "text": "لم تلعب بعد!", "size": "lg", "weight": "bold", "margin": "md"},
                        {"type": "text", "text": "اكتب 'انضم' ثم ابدأ اللعب", "size": "sm", "color": self.theme.text_secondary, "wrap": True, "margin": "sm"}
                    ],
                    "backgroundColor": self.theme.background,
                    "paddingAll": "30px"
                }
            }
        
        points = user_data.get('total_points', 0)
        games = user_data.get('games_played', 0)
        wins = user_data.get('wins', 0)
        win_rate = (wins / games * 100) if games > 0 else 0
        is_registered = user_data.get('is_registered', False)
        
        return {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"المركز #{rank}" if rank else "غير مصنف", "size": "lg", "weight": "bold", "color": "#FFFFFF"},
                    {"type": "text", "text": "مسجل ✅" if is_registered else "غير مسجل ❌", "size": "sm", "color": "#E0E0E0"}
                ],
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"💰 {points} نقطة", "size": "md", "weight": "bold"},
                    {"type": "text", "text": f"🎮 {games} لعبة", "size": "sm", "margin": "sm"},
                    {"type": "text", "text": f"🏆 {wins} فوز", "size": "sm", "margin": "sm"},
                    {"type": "text", "text": f"📈 {win_rate:.0f}% نسبة الفوز", "size": "sm", "margin": "sm"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._btn("🎮 ابدأ لعبة" if is_registered else "🔑 انضم الآن", "ابدأ" if is_registered else "انضم", self.theme.accent),
                            self._btn("🏆 الصدارة", "الصدارة", self.theme.text_secondary)
                        ],
                        "spacing": "sm",
                        "margin": "lg"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px"
            }
        }

    def create_leaderboard(self, leaders: List[Dict]) -> Dict:
        """لوحة الصدارة"""
        if not leaders:
            return {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "⚠️ لا توجد بيانات", "size": "lg", "weight": "bold", "color": self.theme.text_primary}
                    ],
                    "backgroundColor": self.theme.background,
                    "paddingAll": "30px"
                }
            }
        
        leader_items = []
        medals = ["🥇", "🥈", "🥉"]
        
        for i, leader in enumerate(leaders[:10]):
            medal = medals[i] if i < 3 else f"#{i+1}"
            
            leader_items.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": medal, "size": "xl" if i < 3 else "md", "flex": 0},
                    {"type": "text", "text": leader.get('display_name', 'لاعب'), "size": "md", "weight": "bold" if i < 3 else "regular", "flex": 1, "margin": "md"},
                    {"type": "text", "text": f"{leader.get('total_points', 0)} ⭐", "size": "md", "weight": "bold", "color": self.theme.accent if i < 3 else self.theme.text_secondary, "flex": 0}
                ],
                "backgroundColor": self.theme.card if i < 3 else "transparent",
                "cornerRadius": "12px",
                "paddingAll": "md",
                "margin": "sm" if i > 0 else "none"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🏆 لوحة الصدارة", "size": "xl", "weight": "bold", "color": "#FFFFFF"},
                    {"type": "text", "text": f"أفضل {len(leaders)} لاعبين", "size": "xs", "color": "#E0E0E0"}
                ],
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": leader_items,
                "backgroundColor": self.theme.background,
                "paddingAll": "15px"
            }
        }

flex_builder = FlexBuilder()
