"""
Bot Mesh - Enhanced Flex Message Builder
Created by: Abeer Aldosari © 2025
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Theme(Enum):
    """الثيمات المتاحة"""
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"
    MINT = "mint"


@dataclass
class ThemeColors:
    """ألوان الثيم"""
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
    """منشئ رسائل Flex المحسّن"""
    
    def __init__(self, theme: Theme = Theme.WHITE):
        self.theme = THEMES.get(theme, THEMES[Theme.WHITE])
    
    def set_theme(self, theme_name: str):
        """تغيير الثيم"""
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
        """إنشاء زر"""
        return {
            "type": "button",
            "action": {"type": "message", "label": text, "text": action},
            "style": style,
            "color": color or self.theme.accent,
            "height": "sm",
            "margin": "sm"
        }
    
    def _text(self, text: str, size: str = "md", weight: str = "regular", 
              color: str = None, align: str = "center", wrap: bool = True) -> Dict:
        """إنشاء نص"""
        return {
            "type": "text",
            "text": text,
            "size": size,
            "weight": weight,
            "color": color or self.theme.text_primary,
            "align": align,
            "wrap": wrap
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
    # 📋 نافذة المساعدة المحسّنة
    # =============================================
    def create_help_menu(self) -> Dict:
        """نافذة مساعدة منظمة ومريحة للعين"""
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._text("🎮 Bot Mesh", "xl", "bold"),
                    self._text("بوت الألعاب الترفيهية", "xs", color=self.theme.text_secondary)
                ],
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px",
                "spacing": "xs"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # قسم البداية
                    self._box([
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [self._text("🚀", "xxl")],
                                    "backgroundColor": self.theme.accent,
                                    "cornerRadius": "15px",
                                    "width": "55px",
                                    "height": "55px",
                                    "justifyContent": "center",
                                    "alignItems": "center"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        self._text("كيف تبدأ؟", "lg", "bold", align="right"),
                                        self._text("1. اضغط 'انضم' للتسجيل", "xs", color=self.theme.text_secondary, align="right"),
                                        self._text("2. اختر لعبة من الأزرار الثابتة أسفل الشاشة", "xs", color=self.theme.text_secondary, align="right")
                                    ],
                                    "flex": 1,
                                    "margin": "md",
                                    "spacing": "xs"
                                }
                            ],
                            "spacing": "md"
                        }
                    ], bg=self.theme.card, padding="lg", corner="20px"),
                    
                    # الأزرار الرئيسية
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._text("⚡ الأوامر السريعة", "sm", "bold", align="right"),
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    self._btn("📊 نقاطي", "نقاطي", self.theme.accent),
                                    self._btn("🏆 الصدارة", "الصدارة", self.theme.accent_dark)
                                ],
                                "spacing": "sm",
                                "margin": "sm"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    self._btn("🎨 الثيمات", "ثيم", self.theme.text_secondary),
                                    self._btn("⏹ إيقاف", "إيقاف", self.theme.text_secondary)
                                ],
                                "spacing": "sm",
                                "margin": "sm"
                            }
                        ],
                        "spacing": "xs",
                        "margin": "lg"
                    },
                    
                    # المميزات
                    self._box([
                        self._text("✨ ماذا ستحصل؟", "sm", "bold", align="right"),
                        self._text("• 11 لعبة متنوعة", "xs", color=self.theme.text_secondary, align="right"),
                        self._text("• 7 ثيمات جميلة", "xs", color=self.theme.text_secondary, align="right"),
                        self._text("• نظام نقاط وترتيب", "xs", color=self.theme.text_secondary, align="right"),
                        self._text("• لوحة صدارة عالمية", "xs", color=self.theme.text_secondary, align="right")
                    ], bg=self.theme.card, padding="md", corner="20px", margin="lg", spacing="xs"),
                    
                    # نصيحة
                    self._box([
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                self._text("💡", "lg"),
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        self._text("نصيحة", "xs", "bold", align="right"),
                                        self._text("استخدم الأزرار الثابتة أسفل الشاشة للوصول السريع للألعاب", "xxs", color=self.theme.text_secondary, align="right")
                                    ],
                                    "flex": 1,
                                    "margin": "sm"
                                }
                            ]
                        }
                    ], bg=self.theme.surface, padding="sm", corner="15px", margin="lg")
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "15px",
                "spacing": "none"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._text("Created by Abeer Aldosari © 2025", "xxs", color=self.theme.text_secondary)
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "10px"
            }
        }

    # =============================================
    # 🎨 نافذة اختيار الثيم
    # =============================================
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
                    self._text("🎨 اختر الثيم المفضل", "xl", "bold"),
                    self._text("7 ثيمات مميزة", "xs", color=self.theme.text_secondary)
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
    # 📊 بطاقة الإحصائيات المحسّنة
    # =============================================
    def create_stats_card(self, user_data: Dict, rank: int = 0) -> Dict:
        """بطاقة الإحصائيات مع حالة التسجيل"""
        if not user_data:
            return self._create_error("لم تلعب بعد! اكتب 'انضم' ثم ابدأ اللعب")
        
        points = user_data.get('total_points', 0)
        games = user_data.get('games_played', 0)
        wins = user_data.get('wins', 0)
        win_rate = (wins / games * 100) if games > 0 else 0
        is_registered = user_data.get('is_registered', False)
        
        # تحديد المستوى
        if points < 100:
            level = "🌱 مبتدئ"
            level_color = "#68D391"
        elif points < 500:
            level = "⭐ متوسط"
            level_color = "#F6AD55"
        elif points < 1000:
            level = "🔥 محترف"
            level_color = "#FC8181"
        elif points < 5000:
            level = "👑 أسطوري"
            level_color = "#A855F7"
        else:
            level = "💎 خارق"
            level_color = "#00D9FF"
        
        return {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._text(level, "xxl", "bold"),
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._text(f"المركز #{rank}" if rank else "غير مصنف", "sm", color=self.theme.text_secondary),
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    self._text("●", "xs", color="#48BB78" if is_registered else "#FC8181"),
                                    self._text("مسجل" if is_registered else "غير مسجل", "xs", color=self.theme.text_secondary)
                                ],
                                "spacing": "xs",
                                "justifyContent": "flex-end"
                            }
                        ],
                        "justifyContent": "space-between",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": level_color,
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
                    
                    # رسالة حالة التسجيل
                    self._box([
                        self._text(
                            "✅ يمكنك اللعب الآن!" if is_registered else "⚠️ سجل أولاً لتلعب",
                            "xs",
                            color="#48BB78" if is_registered else "#F6AD55"
                        )
                    ], bg=self.theme.card, padding="sm", corner="10px", margin="lg"),
                    
                    # الأزرار
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._btn("🎮 ابدأ لعبة", "ابدأ", self.theme.accent) if is_registered 
                            else self._btn("🔑 انضم الآن", "انضم", self.theme.accent),
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
    
    def _stat_box(self, emoji: str, value: str, label: str) -> Dict:
        """صندوق إحصائية"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                self._text(emoji, "xxl"),
                self._text(value, "xl", "bold"),
                self._text(label, "xs", color=self.theme.text_secondary)
            ],
            "backgroundColor": self.theme.card,
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "flex": 1,
            "spacing": "xs"
        }

    # =============================================
    # 🎮 قائمة الألعاب (Carousel محسّن)
    # =============================================
    def create_games_menu(self) -> Dict:
        """قائمة الألعاب في نافذة واحدة مدمجة"""
        games = {
            'ذكاء': {'emoji': '🧠', 'name': 'اختبار الذكاء', 'color': '#667EEA'},
            'لون': {'emoji': '🎨', 'name': 'لعبة الألوان', 'color': '#9F7AEA'},
            'سلسلة': {'emoji': '⛓️', 'name': 'سلسلة الكلمات', 'color': '#4FD1C5'},
            'ترتيب': {'emoji': '🔤', 'name': 'ترتيب الحروف', 'color': '#68D391'},
            'تكوين': {'emoji': '✏️', 'name': 'تكوين الكلمات', 'color': '#FC8181'},
            'أسرع': {'emoji': '⚡', 'name': 'الكتابة السريعة', 'color': '#F687B3'},
            'لعبة': {'emoji': '🎯', 'name': 'إنسان حيوان نبات', 'color': '#63B3ED'},
            'خمن': {'emoji': '🤔', 'name': 'خمن الكلمة', 'color': '#B794F4'},
            'توافق': {'emoji': '💖', 'name': 'نسبة التوافق', 'color': '#FEB2B2'},
            'ضد': {'emoji': '↔️', 'name': 'الأضداد', 'color': '#9AE6B4'},
            'أغنية': {'emoji': '🎵', 'name': 'خمن الأغنية', 'color': '#E9D8FD'}
        }
        
        game_buttons = []
        for key, data in games.items():
            game_buttons.append(
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [self._text(data['emoji'], "xl")],
                            "backgroundColor": data['color'],
                            "cornerRadius": "10px",
                            "width": "45px",
                            "height": "45px",
                            "justifyContent": "center",
                            "alignItems": "center"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                self._text(data['name'], "sm", "bold", align="right")
                            ],
                            "flex": 1,
                            "margin": "md",
                            "justifyContent": "center"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                self._text("▶", "md", color=data['color'])
                            ],
                            "justifyContent": "center"
                        }
                    ],
                    "action": {"type": "message", "text": key},
                    "backgroundColor": self.theme.card,
                    "cornerRadius": "12px",
                    "paddingAll": "md",
                    "margin": "sm" if game_buttons else "none"
                }
            )
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._text("🎮 اختر اللعبة", "xl", "bold"),
                    self._text("11 لعبة ممتعة", "xs", color=self.theme.text_secondary)
                ],
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": game_buttons,
                "backgroundColor": self.theme.background,
                "paddingAll": "15px",
                "spacing": "none"
            }
        }

    # =============================================
    # 🏆 لوحة الصدارة
    # =============================================
    def create_leaderboard(self, leaders: List[Dict]) -> Dict:
        """لوحة الصدارة المحسّنة"""
        if not leaders:
            return self._create_error("لا توجد بيانات")
        
        leader_items = []
        medals = ["🥇", "🥈", "🥉"]
        medal_colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
        
        for i, leader in enumerate(leaders[:10]):
            medal = medals[i] if i < 3 else f"#{i+1}"
            bg_color = medal_colors[i] if i < 3 else "transparent"
            
            leader_items.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [self._text(medal, "xl" if i < 3 else "md", align="center")],
                        "width": "45px",
                        "justifyContent": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._text(leader.get('display_name', 'لاعب'), "md", "bold" if i < 3 else "regular", align="right")
                        ],
                        "flex": 1,
                        "justifyContent": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._text(f"{leader.get('total_points', 0)} ⭐", "md", "bold", 
                                      self.theme.accent if i < 3 else self.theme.text_secondary, align="left")
                        ],
                        "justifyContent": "center"
                    }
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
                    self._text("🏆 لوحة الصدارة", "xl", "bold"),
                    self._text(f"أفضل {len(leaders)} لاعبين", "xs", color=self.theme.text_secondary)
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
                    self._text("⚠️", "xxl"),
                    self._text(message, "md", margin="md")
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "30px",
                "spacing": "sm"
            }
        }


# Singleton
flex_builder = FlexBuilder()
