"""
Bot Mesh - Enhanced Flex Messages System
Created by: Abeer Aldosari © 2025

نظام نوافذ Flex احترافي مع دعم 7 ثيمات جميلة
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Theme(Enum):
    """الثيمات المتاحة - 7 ثيمات احترافية"""
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
    button_bg: str
    shadow_light: str
    shadow_dark: str
    success: str = "#48BB78"
    error: str = "#FC8181"
    warning: str = "#F6AD55"


# =============================================
# 🎨 الثيمات السبعة
# =============================================
THEMES: Dict[Theme, ThemeColors] = {
    Theme.WHITE: ThemeColors(
        name="white", name_ar="⚪ أبيض", emoji="⚪",
        background="#E8EBF5", surface="#E8EBF5", card="#FFFFFF",
        text_primary="#2C3E50", text_secondary="#95A5A6",
        accent="#667EEA", accent_dark="#5A67D8", button_bg="#667EEA",
        shadow_light="#FFFFFF", shadow_dark="#B8C1E0"
    ),
    
    Theme.BLACK: ThemeColors(
        name="black", name_ar="⚫ أسود", emoji="⚫",
        background="#0F0F1A", surface="#1A1A2E", card="#252538",
        text_primary="#FFFFFF", text_secondary="#A0AEC0",
        accent="#00D9FF", accent_dark="#00B8D4", button_bg="#00D9FF",
        shadow_light="#2A2A4A", shadow_dark="#000000"
    ),
    
    Theme.GRAY: ThemeColors(
        name="gray", name_ar="🔘 رمادي", emoji="🔘",
        background="#1A202C", surface="#2D3748", card="#4A5568",
        text_primary="#F7FAFC", text_secondary="#CBD5E0",
        accent="#68D391", accent_dark="#48BB78", button_bg="#48BB78",
        shadow_light="#4A5568", shadow_dark="#0D0D0D"
    ),
    
    Theme.BLUE: ThemeColors(
        name="blue", name_ar="💙 أزرق", emoji="💙",
        background="#0A1628", surface="#1E3A5F", card="#0F2744",
        text_primary="#E0F2FE", text_secondary="#7DD3FC",
        accent="#0EA5E9", accent_dark="#0284C7", button_bg="#0EA5E9",
        shadow_light="#1E4976", shadow_dark="#000000"
    ),
    
    Theme.PURPLE: ThemeColors(
        name="purple", name_ar="💜 بنفسجي", emoji="💜",
        background="#1A0F3E", surface="#312E81", card="#3730A3",
        text_primary="#F5F3FF", text_secondary="#C4B5FD",
        accent="#A855F7", accent_dark="#9333EA", button_bg="#9333EA",
        shadow_light="#4338CA", shadow_dark="#000000"
    ),
    
    Theme.PINK: ThemeColors(
        name="pink", name_ar="🌸 وردي", emoji="🌸",
        background="#FFF1F2", surface="#FFE4E6", card="#FFFFFF",
        text_primary="#881337", text_secondary="#BE123C",
        accent="#F43F5E", accent_dark="#E11D48", button_bg="#F43F5E",
        shadow_light="#FFFFFF", shadow_dark="#FFC9D0"
    ),
    
    Theme.MINT: ThemeColors(
        name="mint", name_ar="🍃 نعناعي", emoji="🍃",
        background="#ECFDF5", surface="#D1FAE5", card="#FFFFFF",
        text_primary="#065F46", text_secondary="#059669",
        accent="#10B981", accent_dark="#059669", button_bg="#10B981",
        shadow_light="#FFFFFF", shadow_dark="#9EF3CA"
    )
}


class FlexMessageBuilder:
    """منشئ رسائل Flex احترافي"""
    
    def __init__(self, theme: Theme = Theme.WHITE):
        self.theme = THEMES.get(theme, THEMES[Theme.WHITE])
    
    def set_theme(self, theme_name: str):
        """تغيير الثيم"""
        theme_map = {t.value: t for t in Theme}
        theme = theme_map.get(theme_name.lower(), Theme.WHITE)
        self.theme = THEMES[theme]
    
    # =============================================
    # 🎨 مكونات أساسية
    # =============================================
    
    def _text(self, text: str, size: str = "md", weight: str = "regular",
              color: str = None, wrap: bool = True,
              margin: str = "none") -> Dict:
        """إنشاء نص"""
        return {
            "type": "text",
            "text": text,
            "size": size,
            "weight": weight,
            "color": color or self.theme.text_primary,
            "wrap": wrap,
            "margin": margin
        }
    
    def _box(self, contents: List, layout: str = "vertical",
             bg: str = None, padding: str = "lg", margin: str = "none",
             corner: str = "20px", spacing: str = "md",
             border_width: str = None, border_color: str = None,
             action: Dict = None) -> Dict:
        """إنشاء صندوق"""
        box = {
            "type": "box",
            "layout": layout,
            "contents": contents,
            "backgroundColor": bg or "transparent",
            "paddingAll": padding,
            "margin": margin,
            "cornerRadius": corner,
            "spacing": spacing
        }
        if border_width:
            box["borderWidth"] = border_width
            box["borderColor"] = border_color or self.theme.accent
        if action:
            box["action"] = action
        return box
    
    def _button(self, label: str, text: str, style: str = "primary",
                color: str = None, height: str = "sm") -> Dict:
        """إنشاء زر"""
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": style,
            "color": color or self.theme.button_bg,
            "height": height,
            "margin": "sm"
        }
    
    def _separator(self, margin: str = "lg", color: str = None) -> Dict:
        """فاصل"""
        return {
            "type": "separator",
            "margin": margin,
            "color": color or self.theme.text_secondary + "30"
        }
    
    # =============================================
    # 🏠 نافذة الترحيب والمساعدة الرئيسية
    # =============================================
    
    def create_welcome_screen(self) -> Dict:
        """نافذة الترحيب الأولى عند ذكر البوت أو كتابة 'مساعدة'"""
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._box([
                        self._text("🎮", "xxl", margin="md"),
                        self._text("Bot Mesh", "xxl", "bold", margin="sm"),
                        self._text("بوت الألعاب الترفيهية", "sm",
                                  color=self.theme.text_secondary, margin="xs")
                    ], bg=self.theme.card, corner="25px", padding="xl"),
                    
                    self._box([
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                self._box([self._text("✨", "xxl")],
                                         bg=self.theme.accent, corner="15px",
                                         padding="md"),
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        self._text("ابدأ الآن!", "lg", "bold"),
                                        self._text("سجل واستمتع بـ 11 لعبة ممتعة",
                                                  "xs", color=self.theme.text_secondary)
                                    ],
                                    "flex": 1,
                                    "margin": "md",
                                    "justifyContent": "center"
                                }
                            ],
                            "spacing": "md"
                        }
                    ], bg=self.theme.surface, corner="20px", margin="lg", padding="lg"),
                    
                    self._box([
                        self._text("📋 كيف تبدأ؟", "md", "bold", margin="md"),
                        
                        self._box([
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    self._text("1️⃣", "lg"),
                                    self._text("اضغط على زر 'انضم' للتسجيل", "sm")
                                ],
                                "justifyContent": "space-between"
                            }
                        ], margin="sm"),
                        
                        self._box([
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    self._text("2️⃣", "lg"),
                                    self._text("اختر لعبة من الأزرار الثابتة أسفل الشاشة", "sm")
                                ],
                                "justifyContent": "space-between"
                            }
                        ], margin="sm"),
                        
                        self._box([
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    self._text("3️⃣", "lg"),
                                    self._text("العب واجمع النقاط وكن في الصدارة!", "sm")
                                ],
                                "justifyContent": "space-between"
                            }
                        ], margin="sm")
                    ], bg=self.theme.card, corner="20px", margin="lg", padding="lg"),
                    
                    self._box([
                        self._text("⚡ المميزات", "md", "bold"),
                        self._text("• 11 لعبة متنوعة", "sm", color=self.theme.text_secondary, margin="sm"),
                        self._text("• 7 ثيمات جميلة", "sm", color=self.theme.text_secondary, margin="xs"),
                        self._text("• نظام نقاط وترتيب", "sm", color=self.theme.text_secondary, margin="xs"),
                        self._text("• لوحة صدارة عالمية", "sm", color=self.theme.text_secondary, margin="xs")
                    ], bg=self.theme.surface, corner="20px", margin="lg", padding="lg"),
                    
                    self._box([
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                self._text("💡", "md"),
                                self._text("استخدم الأزرار الثابتة أسفل الشاشة للوصول السريع!", "xs",
                                          color=self.theme.text_secondary)
                            ],
                            "justifyContent": "space-between"
                        }
                    ], bg=self.theme.card, corner="15px", margin="lg", padding="md"),
                    
                    self._text("Created by Abeer Aldosari © 2025", "xxs",
                              color=self.theme.text_secondary, margin="lg")
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px",
                "spacing": "none"
            }
        }
    
    # =============================================
    # 📋 دليل الاستخدام
    # =============================================
    
    def create_help_guide(self) -> Dict:
        """دليل الاستخدام الكامل"""
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._text("📖 دليل الاستخدام", "xl", "bold"),
                    self._text("كل ما تحتاج معرفته", "xs",
                              color=self.theme.text_primary + "CC")
                ],
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._text("🎯 الأوامر الأساسية", "lg", "bold", margin="md"),
                    
                    self._command_row("انضم", "التسجيل في البوت"),
                    self._command_row("انسحب", "إلغاء التسجيل"),
                    self._command_row("نقاطي", "عرض إحصائياتك"),
                    self._command_row("الصدارة", "أفضل اللاعبين"),
                    self._command_row("إيقاف", "إنهاء اللعبة الحالية"),
                    
                    self._separator(margin="xl"),
                    
                    self._text("🎮 أثناء اللعب", "lg", "bold", margin="lg"),
                    
                    self._command_row("لمح", "الحصول على تلميح"),
                    self._command_row("جاوب", "عرض الإجابة الصحيحة"),
                    
                    self._separator(margin="xl"),
                    
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._button("انضم", "انضم", color=self.theme.accent),
                            self._button("نقاطي", "نقاطي", color=self.theme.accent_dark),
                            self._button("الصدارة", "الصدارة",
                                         color=self.theme.text_secondary)
                        ],
                        "spacing": "sm",
                        "margin": "xl"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px",
                "spacing": "none"
            }
        }
    
    def _command_row(self, command: str, description: str) -> Dict:
        """صف أمر في دليل الاستخدام"""
        return self._box([
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._text(description, "sm", color=self.theme.text_secondary),
                    self._box([self._text(command, "sm", "bold")],
                              bg=self.theme.accent + "20",
                              corner="8px", padding="sm")
                ],
                "justifyContent": "space-between"
            }
        ], margin="sm")
    
    # =============================================
    # 📊 بطاقة الإحصائيات
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
        
        level_data = self._get_level(points)
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._box([
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                self._text(level_data['emoji'], "xxl"),
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        self._text(level_data['name'], "xl", "bold"),
                                        self._text(f"المركز #{rank}" if rank else "غير مصنف",
                                                  "sm", color=self.theme.text_secondary)
                                    ],
                                    "flex": 1,
                                    "justifyContent": "center"
                                }
                            ],
                            "justifyContent": "space-between"
                        },
                        
                        self._box([
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    self._text("●", "xs",
                                              color=self.theme.success if is_registered else self.theme.error),
                                    self._text("مسجل" if is_registered else "غير مسجل",
                                              "xs", color=self.theme.text_secondary)
                                ],
                                "spacing": "xs"
                            }
                        ], margin="sm")
                    ], bg=level_data['color'], corner="25px", padding="xl"),
                    
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
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
                            }
                        ],
                        "margin": "xl"
                    },
                    
                    self._box([
                        self._text(
                            "✅ يمكنك اللعب الآن!" if is_registered else "⚠️ سجل أولاً لتلعب",
                            "sm", "bold",
                            color=self.theme.success if is_registered else self.theme.warning
                        )
                    ], bg=self.theme.card, corner="15px", margin="lg", padding="md"),
                    
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._button("🎮 ابدأ لعبة", "ابدأ", color=self.theme.accent)
                            if is_registered else
                            self._button("🔑 انضم الآن", "انضم", color=self.theme.accent),
                            
                            self._button("🏆 الصدارة", "الصدارة",
                                         color=self.theme.text_secondary)
                        ],
                        "spacing": "sm",
                        "margin": "lg"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px",
                "spacing": "none"
            }
        }
    
    def _get_level(self, points: int) -> Dict:
        """تحديد المستوى بناءً على النقاط"""
        if points < 100:
            return {'name': '🌱 مبتدئ', 'emoji': '🌱', 'color': '#68D391'}
        elif points < 500:
            return {'name': '⭐ متوسط', 'emoji': '⭐', 'color': '#F6AD55'}
        elif points < 1000:
            return {'name': '🔥 محترف', 'emoji': '🔥', 'color': '#FC8181'}
        elif points < 5000:
            return {'name': '👑 أسطوري', 'emoji': '👑', 'color': '#A855F7'}
        else:
            return {'name': '💎 خارق', 'emoji': '💎', 'color': '#00D9FF'}
    
    def _stat_box(self, emoji: str, value: str, label: str) -> Dict:
        """صندوق إحصائية"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                self._text(emoji, "xxl"),
                self._text(value, "xl", "bold", margin="xs"),
                self._text(label, "xs", color=self.theme.text_secondary, margin="xs")
            ],
            "backgroundColor": self.theme.card,
            "cornerRadius": "20px",
            "paddingAll": "lg",
            "flex": 1,
            "spacing": "none"
        }
    
    # =============================================
    # 🎨 اختيار الثيم
    # =============================================
    
    def create_theme_selector(self) -> Dict:
        """نافذة اختيار الثيمات"""
        theme_buttons = []
        for theme_enum, theme_data in THEMES.items():
            theme_buttons.append(
                self._box([
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._box([self._text(theme_data.emoji, "xl")],
                                      bg=theme_data.accent, corner="12px",
                                      padding="sm"),
                            self._text(theme_data.name_ar, "md", "bold")
                        ],
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }
                ], bg=self.theme.card, corner="15px", padding="md", margin="sm",
                action={"type": "message", "text": f"ثيم:{theme_data.name}"})
            )
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._text("🎨 اختر الثيم المفضل", "xl", "bold"),
                    self._text("7 ثيمات مميزة", "xs",
                              color=self.theme.text_primary + "CC")
                ],
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": theme_buttons,
                "backgroundColor": self.theme.background,
                "paddingAll": "20px",
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
            is_top = i < 3
            
            leader_items.append(
                self._box([
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._box([self._text(medal, "xl" if is_top else "lg")],
                                      bg=medal_colors[i] + "30" if is_top else "transparent",
                                      corner="12px", padding="sm"),
                            
                            self._text(leader.get('display_name', 'لاعب'),
                                       "md", "bold" if is_top else "regular"),
                            
                            self._text(f"{leader.get('total_points', 0)} ⭐",
                                       "md", "bold",
                                       color=self.theme.accent if is_top else self.theme.text_secondary)
                        ],
                        "justifyContent": "space-between",
                        "alignItems": "center"
                    }
                ], bg=self.theme.card if is_top else "transparent",
                corner="15px", padding="md", margin="sm" if i > 0 else "none")
            )
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._text("🏆 لوحة الصدارة", "xl", "bold"),
                    self._text(f"أفضل {len(leaders)} لاعبين", "xs",
                              color=self.theme.text_primary + "CC")
                ],
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": leader_items,
                "backgroundColor": self.theme.background,
                "paddingAll": "20px"
            }
        }
    
    # =============================================
    # ❌ رسالة خطأ
    # =============================================
    
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
                "paddingAll": "40px",
                "spacing": "md"
            }
        }


# Singleton
flex_builder = FlexMessageBuilder()
