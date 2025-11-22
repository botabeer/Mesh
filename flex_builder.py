"""
Bot Mesh - Flex Message Builder (Fixed Version)
Created by: Abeer Aldosari © 2025
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Theme(Enum):
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"
    PURPLE = "purple"
    BLUE = "blue"


@dataclass
class ThemeColors:
    name: str
    name_ar: str
    background: str
    surface: str
    card: str
    text_primary: str
    text_secondary: str
    accent: str
    button_primary: str
    button_secondary: str
    border: str
    shadow_dark: str
    shadow_light: str


THEMES: Dict[Theme, ThemeColors] = {
    Theme.WHITE: ThemeColors(
        name="white", name_ar="⚪ أبيض",
        background="#E0E5EC", surface="#E0E5EC", card="#E0E5EC",
        text_primary="#2C3E50", text_secondary="#7F8C8D",
        accent="#667EEA", button_primary="#667EEA", button_secondary="#A0AEC0",
        border="#D1D5DB", shadow_dark="#A3B1C6", shadow_light="#FFFFFF"
    ),
    Theme.BLACK: ThemeColors(
        name="black", name_ar="⚫ أسود",
        background="#1A1A2E", surface="#16213E", card="#0F0F1A",
        text_primary="#FFFFFF", text_secondary="#A0AEC0",
        accent="#00D9FF", button_primary="#00D9FF", button_secondary="#4A5568",
        border="#2D3748", shadow_dark="#0D0D1A", shadow_light="#2A2A4A"
    ),
    Theme.GRAY: ThemeColors(
        name="gray", name_ar="🔘 رمادي",
        background="#2D3748", surface="#4A5568", card="#1A202C",
        text_primary="#F7FAFC", text_secondary="#CBD5E0",
        accent="#68D391", button_primary="#48BB78", button_secondary="#718096",
        border="#4A5568", shadow_dark="#1A202C", shadow_light="#4A5568"
    ),
    Theme.PURPLE: ThemeColors(
        name="purple", name_ar="💜 بنفسجي",
        background="#1E1B4B", surface="#312E81", card="#1E1B4B",
        text_primary="#F5F3FF", text_secondary="#C4B5FD",
        accent="#A855F7", button_primary="#9333EA", button_secondary="#6B21A8",
        border="#4C1D95", shadow_dark="#0F0A2E", shadow_light="#4338CA"
    ),
    Theme.BLUE: ThemeColors(
        name="blue", name_ar="💙 أزرق",
        background="#0C1929", surface="#1E3A5F", card="#0F2744",
        text_primary="#E0F2FE", text_secondary="#7DD3FC",
        accent="#00D9FF", button_primary="#0EA5E9", button_secondary="#0369A1",
        border="#0369A1", shadow_dark="#061224", shadow_light="#1E4976"
    )
}


class FlexBuilder:
    """منشئ رسائل Flex المحسّن"""
    
    def __init__(self, theme: Theme = Theme.WHITE):
        self.theme = THEMES.get(theme, THEMES[Theme.WHITE])
    
    def set_theme(self, theme_name: str):
        """تغيير الثيم"""
        theme_map = {
            'white': Theme.WHITE, 'أبيض': Theme.WHITE,
            'black': Theme.BLACK, 'أسود': Theme.BLACK,
            'gray': Theme.GRAY, 'رمادي': Theme.GRAY,
            'purple': Theme.PURPLE, 'بنفسجي': Theme.PURPLE,
            'blue': Theme.BLUE, 'أزرق': Theme.BLUE
        }
        theme = theme_map.get(theme_name.lower(), Theme.WHITE)
        self.theme = THEMES[theme]
    
    def _btn(self, text: str, action: str, color: str = None, style: str = "primary") -> Dict:
        """إنشاء زر"""
        return {
            "type": "button",
            "action": {"type": "message", "label": text, "text": action},
            "style": style,
            "color": color or self.theme.button_primary,
            "height": "sm",
            "margin": "sm"
        }
    
    def _text(self, text: str, size: str = "md", weight: str = "regular", 
              color: str = None) -> Dict:
        """إنشاء نص - بدون align و margin"""
        return {
            "type": "text",
            "text": text,
            "size": size,
            "weight": weight,
            "color": color or self.theme.text_primary,
            "wrap": True
        }
    
    def _box(self, contents: List, layout: str = "vertical", 
             bg: str = None, padding: str = "lg", margin: str = "none",
             corner: str = "xl", spacing: str = "sm") -> Dict:
        """إنشاء صندوق"""
        return {
            "type": "box",
            "layout": layout,
            "contents": contents,
            "backgroundColor": bg or self.theme.surface,
            "paddingAll": padding,
            "margin": margin,
            "cornerRadius": corner,
            "spacing": spacing
        }

    # =============================================
    # 📋 نافذة المساعدة الشاملة
    # =============================================
    def create_help_menu(self) -> Dict:
        """إنشاء نافذة المساعدة مع كل الأزرار"""
        return {
            "type": "bubble",
            "size": "giga",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🎮 Bot Mesh",
                        "size": "xxl",
                        "weight": "bold",
                        "color": self.theme.text_primary
                    },
                    {
                        "type": "text",
                        "text": "مرحباً بك في بوت الألعاب",
                        "size": "sm",
                        "color": self.theme.text_secondary
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # قسم التسجيل
                    self._box([
                        {
                            "type": "text",
                            "text": "🔐 التسجيل",
                            "size": "lg",
                            "weight": "bold",
                            "color": self.theme.text_primary
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                self._btn("🚪 انسحب", "انسحب", self.theme.button_secondary),
                                self._btn("🔑 انضم", "انضم", self.theme.accent)
                            ],
                            "spacing": "sm",
                            "margin": "md"
                        }
                    ], bg=self.theme.card, margin="none"),
                    
                    # قسم اللعب
                    self._box([
                        {
                            "type": "text",
                            "text": "🎯 اللعب",
                            "size": "lg",
                            "weight": "bold",
                            "color": self.theme.text_primary
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                self._btn("⏹️ إيقاف", "إيقاف", self.theme.button_secondary),
                                self._btn("🎮 ابدأ", "ابدأ", self.theme.accent)
                            ],
                            "spacing": "sm",
                            "margin": "md"
                        }
                    ], bg=self.theme.card, margin="md"),
                    
                    # قسم الإحصائيات
                    self._box([
                        {
                            "type": "text",
                            "text": "📊 الإحصائيات",
                            "size": "lg",
                            "weight": "bold",
                            "color": self.theme.text_primary
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                self._btn("🏆 الصدارة", "الصدارة", self.theme.button_secondary),
                                self._btn("📈 نقاطي", "نقاطي", self.theme.accent)
                            ],
                            "spacing": "sm",
                            "margin": "md"
                        }
                    ], bg=self.theme.card, margin="md"),
                    
                    # قسم الإعدادات
                    self._box([
                        {
                            "type": "text",
                            "text": "⚙️ الإعدادات",
                            "size": "lg",
                            "weight": "bold",
                            "color": self.theme.text_primary
                        },
                        self._btn("🎨 تغيير الثيم", "ثيم", self.theme.accent)
                    ], bg=self.theme.card, margin="md"),
                    
                    # الألعاب المتاحة
                    self._box([
                        {
                            "type": "text",
                            "text": "🎲 الألعاب المتاحة",
                            "size": "lg",
                            "weight": "bold",
                            "color": self.theme.text_primary
                        },
                        {
                            "type": "text",
                            "text": "ذكاء • لون • سلسلة • ترتيب • تكوين • أسرع • لعبة • خمن • توافق • رياضيات • ذاكرة • لغز • ضد • إيموجي • أغنية",
                            "size": "xs",
                            "color": self.theme.text_secondary,
                            "wrap": True
                        }
                    ], bg=self.theme.card, margin="md")
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "15px",
                "spacing": "none"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Created by Abeer Aldosari © 2025",
                        "size": "xxs",
                        "color": self.theme.text_secondary
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "10px"
            }
        }

    # =============================================
    # 🎨 نافذة اختيار الثيم
    # =============================================
    def create_theme_selector(self) -> Dict:
        """إنشاء نافذة اختيار الثيم"""
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
                    {
                        "type": "text",
                        "text": "🎨 اختر الثيم",
                        "size": "xl",
                        "weight": "bold",
                        "color": "#FFFFFF"
                    }
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

    # =============================================
    # 🎮 قائمة الألعاب المحسّنة
    # =============================================
    def create_games_carousel(self, games: Dict[str, Dict]) -> Dict:
        """إنشاء قائمة الألعاب"""
        if not games:
            return self._create_error("⚠️ لا توجدألعاب متاحة")
        
        bubbles = []
        for arabic_name, data in games.items():
            bubble = {
                "type": "bubble",
                "size": "micro",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        # أيقونة اللعبة
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": data['emoji'],
                                    "size": "4xl"
                                }
                            ],
                            "backgroundColor": self.theme.card,
                            "cornerRadius": "20px",
                            "paddingAll": "25px"
                        },
                        # اسم اللعبة
                        {
                            "type": "text",
                            "text": data['name'],
                            "size": "sm",
                            "weight": "bold",
                            "color": self.theme.text_primary,
                            "margin": "md"
                        },
                        # زر اللعب
                        self._btn("▶️ العب", arabic_name, data.get('color', self.theme.accent))
                    ],
                    "backgroundColor": self.theme.background,
                    "paddingAll": "15px",
                    "spacing": "sm"
                }
            }
            bubbles.append(bubble)
        
        return {"type": "carousel", "contents": bubbles}

    # =============================================
    # 📊 بطاقة الإحصائيات
    # =============================================
    def create_stats_card(self, user_data: Dict, rank: int = 0) -> Dict:
        """إنشاء بطاقة الإحصائيات"""
        if not user_data:
            return self._create_error("لم تلعب بعد! اكتب 'انضم' ثم 'ابدأ'")
        
        points = user_data.get('total_points', 0)
        games = user_data.get('games_played', 0)
        wins = user_data.get('wins', 0)
        win_rate = (wins / games * 100) if games > 0 else 0
        
        # تحديد المستوى
        if points < 100:
            level = "🌱 مبتدئ"
        elif points < 500:
            level = "⭐ متوسط"
        elif points < 1000:
            level = "🔥 محترف"
        else:
            level = "👑 أسطوري"
        
        return {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": level,
                        "size": "xxl",
                        "weight": "bold",
                        "color": "#FFFFFF"
                    },
                    {
                        "type": "text",
                        "text": f"المركز #{rank}" if rank else "",
                        "size": "sm",
                        "color": "#E0E0E0"
                    }
                ],
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # الإحصائيات
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._stat_box("💰", str(points), "نقطة"),
                            self._stat_box("🎮", str(games), "لعبة")
                        ],
                        "spacing": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._stat_box("🏆", str(wins), "فوز"),
                            self._stat_box("📈", f"{win_rate:.0f}%", "نسبة")
                        ],
                        "spacing": "md",
                        "margin": "md"
                    },
                    self._btn("🎮 ابدأ لعبة جديدة", "ابدأ", self.theme.accent)
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px"
            }
        }
    
    def _stat_box(self, emoji: str, value: str, label: str) -> Dict:
        """صندوق إحصائية"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": emoji,
                    "size": "xxl"
                },
                {
                    "type": "text",
                    "text": value,
                    "size": "xl",
                    "weight": "bold",
                    "color": self.theme.text_primary
                },
                {
                    "type": "text",
                    "text": label,
                    "size": "xs",
                    "color": self.theme.text_secondary
                }
            ],
            "backgroundColor": self.theme.card,
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "flex": 1
        }

    # =============================================
    # 🏆 لوحة الصدارة
    # =============================================
    def create_leaderboard(self, leaders: List[Dict]) -> Dict:
        """إنشاء لوحة الصدارة"""
        if not leaders:
            return self._create_error("لا توجد بيانات")
        
        leader_items = []
        medals = ["🥇", "🥈", "🥉"]
        
        for i, leader in enumerate(leaders[:10]):
            medal = medals[i] if i < 3 else f"{i+1}"
            leader_items.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": medal,
                        "size": "xl" if i < 3 else "md",
                        "color": self.theme.text_primary
                    },
                    {
                        "type": "text",
                        "text": leader.get('display_name', 'لاعب'),
                        "size": "md",
                        "color": self.theme.text_primary,
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"{leader.get('total_points', 0)}⭐",
                        "size": "md",
                        "weight": "bold",
                        "color": self.theme.accent
                    }
                ],
                "backgroundColor": self.theme.card if i < 3 else "transparent",
                "cornerRadius": "10px",
                "paddingAll": "12px",
                "margin": "sm" if i > 0 else "none"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🏆 لوحة الصدارة",
                        "size": "xl",
                        "weight": "bold",
                        "color": "#FFFFFF"
                    }
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
    
    def _create_error(self, message: str) -> Dict:
        """رسالة خطأ"""
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": message,
                        "size": "md",
                        "color": self.theme.text_primary
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "30px"
            }
        }


# Singleton
flex_builder = FlexBuilder()
