"""
Bot Mesh - Enhanced Flex Messages System
Created by: Abeer Aldosari © 2025
"""
from typing import Dict, List, Optional
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
    button_bg: str
    success: str = "#48BB78"
    error: str = "#FC8181"
    warning: str = "#F6AD55"


THEMES: Dict[Theme, ThemeColors] = {
    Theme.WHITE: ThemeColors(
        "white", "⚪ أبيض", "⚪", "#E8EBF5", "#E8EBF5", "#FFFFFF",
        "#2C3E50", "#95A5A6", "#667EEA", "#5A67D8", "#667EEA"
    ),
    Theme.BLACK: ThemeColors(
        "black", "⚫ أسود", "⚫", "#0F0F1A", "#1A1A2E", "#252538",
        "#FFFFFF", "#A0AEC0", "#00D9FF", "#00B8D4", "#00D9FF"
    ),
    Theme.GRAY: ThemeColors(
        "gray", "🔘 رمادي", "🔘", "#1A202C", "#2D3748", "#4A5568",
        "#F7FAFC", "#CBD5E0", "#68D391", "#48BB78", "#48BB78"
    ),
    Theme.BLUE: ThemeColors(
        "blue", "💙 أزرق", "💙", "#0A1628", "#1E3A5F", "#0F2744",
        "#E0F2FE", "#7DD3FC", "#0EA5E9", "#0284C7", "#0EA5E9"
    ),
    Theme.PURPLE: ThemeColors(
        "purple", "💜 بنفسجي", "💜", "#1A0F3E", "#312E81", "#3730A3",
        "#F5F3FF", "#C4B5FD", "#A855F7", "#9333EA", "#9333EA"
    ),
    Theme.PINK: ThemeColors(
        "pink", "🌸 وردي", "🌸", "#FFF1F2", "#FFE4E6", "#FFFFFF",
        "#881337", "#BE123C", "#F43F5E", "#E11D48", "#F43F5E"
    ),
    Theme.MINT: ThemeColors(
        "mint", "🍃 نعناعي", "🍃", "#ECFDF5", "#D1FAE5", "#FFFFFF",
        "#065F46", "#059669", "#10B981", "#059669", "#10B981"
    ),
}


class FlexMessageBuilder:
    """منشئ رسائل Flex احترافي"""
    
    def __init__(self, theme: Theme = Theme.WHITE):
        self.theme = THEMES.get(theme, THEMES[Theme.WHITE])
    
    def set_theme(self, theme_name: str):
        theme_map = {t.value: t for t in Theme}
        theme = theme_map.get(theme_name.lower(), Theme.WHITE)
        self.theme = THEMES[theme]
    
    def _text(self, text: str, size: str = "md", weight: str = "regular",
              color: Optional[str] = None, align: str = "center",
              wrap: bool = True, margin: str = "none") -> Dict:
        return {
            "type": "text", "text": text, "size": size, "weight": weight,
            "color": color or self.theme.text_primary, "align": align,
            "wrap": wrap, "margin": margin
        }
    
    def _box(self, contents: List, layout: str = "vertical",
             bg: Optional[str] = None, padding: str = "lg",
             margin: str = "none", corner: str = "20px",
             spacing: str = "md", action: Optional[Dict] = None) -> Dict:
        box = {
            "type": "box", "layout": layout, "contents": contents,
            "paddingAll": padding, "margin": margin,
            "cornerRadius": corner, "spacing": spacing
        }
        if bg:
            box["backgroundColor"] = bg
        if action:
            box["action"] = action
        return box
    
    def _button(self, label: str, text: str, style: str = "primary",
                color: Optional[str] = None, height: str = "sm") -> Dict:
        btn = {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": style, "height": height, "margin": "sm"
        }
        if color:
            btn["color"] = color
        return btn
    
    def _separator(self, margin: str = "lg") -> Dict:
        return {
            "type": "separator", "margin": margin,
            "color": self.theme.text_secondary + "30"
        }
    
    def _command_row(self, cmd: str, desc: str) -> Dict:
        return {
            "type": "box", "layout": "horizontal", "margin": "md",
            "contents": [
                self._text(desc, "sm", color=self.theme.text_secondary, align="start"),
                self._box(
                    [self._text(cmd, "sm", "bold")],
                    bg=self.theme.accent + "20", corner="8px", padding="sm"
                )
            ],
            "justifyContent": "space-between", "alignItems": "center"
        }
    
    # =========================================
    # نافذة المساعدة الرئيسية (عند المنشن/بداية)
    # =========================================
    def create_help_screen(self) -> Dict:
        """نافذة المساعدة الكاملة - تظهر عند المنشن أو أمر بداية"""
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px",
                "contents": [
                    self._text("🎮", "xxl"),
                    self._text("مساعدة البوت", "xl", "bold", "#FFFFFF"),
                ]
            },
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.background,
                "paddingAll": "20px", "spacing": "md",
                "contents": [
                    # الأوامر الأساسية
                    self._text("الأوامر الأساسية", "lg", "bold", align="end", margin="sm"),
                    self._command_row("البداية / ابدأ", "عرض قائمة الألعاب"),
                    self._command_row("انضم", "الانضمام للعبة النشطة"),
                    self._command_row("نقاطي", "عرض إحصائياتك الشخصية"),
                    self._command_row("الصدارة", "أفضل 10 لاعبين"),
                    self._command_row("إيقاف", "إنهاء اللعبة الحالية"),
                    
                    self._separator("xl"),
                    
                    # الألعاب المتاحة
                    self._text("الألعاب المتاحة", "lg", "bold", align="end", margin="md"),
                    self._text("11 لعبة تفاعلية متنوعة", "sm",
                              color=self.theme.text_secondary, align="end"),
                    
                    self._separator("xl"),
                    
                    # الحقوق
                    self._text("تم إنشاء هذا البوت بواسطة عبير الدوسري",
                              "xs", color=self.theme.text_secondary, margin="lg")
                ]
            }
        }
    
    # =========================================
    # دليل الاستخدام المفصل
    # =========================================
    def create_help_guide(self) -> Dict:
        """دليل الاستخدام التفصيلي"""
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px",
                "contents": [
                    self._text("دليل الاستخدام", "xl", "bold", "#FFFFFF"),
                ]
            },
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.background,
                "paddingAll": "20px", "spacing": "md",
                "contents": [
                    # الأوامر الأساسية
                    self._text("الأوامر الأساسية", "lg", "bold", align="end"),
                    self._command_row("انضم", "التسجيل في البوت"),
                    self._command_row("انسحب", "إلغاء التسجيل"),
                    self._command_row("نقاطي", "عرض إحصائياتك"),
                    self._command_row("الصدارة", "أفضل اللاعبين"),
                    self._command_row("إيقاف", "إنهاء اللعبة الحالية"),
                    
                    self._separator("xl"),
                    
                    # أثناء اللعب
                    self._text("أثناء اللعب", "lg", "bold", align="end", margin="md"),
                    self._command_row("لمح", "الحصول على تلميح"),
                    self._command_row("جاوب", "عرض الإجابة الصحيحة"),
                    
                    self._separator("xl"),
                    
                    # الأزرار
                    {
                        "type": "box", "layout": "horizontal",
                        "spacing": "sm", "margin": "xl",
                        "contents": [
                            self._button("انضم", "انضم", color=self.theme.accent),
                            self._button("نقاطي", "نقاطي", "secondary"),
                            self._button("الصدارة", "الصدارة", "secondary"),
                        ]
                    },
                    
                    # الحقوق
                    self._text("تم إنشاء هذا البوت بواسطة عبير الدوسري",
                              "xs", color=self.theme.text_secondary, margin="lg")
                ]
            }
        }
    
    # =========================================
    # نافذة الترحيب
    # =========================================
    def create_welcome_screen(self) -> Dict:
        """نافذة الترحيب للمستخدمين الجدد"""
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.background,
                "paddingAll": "20px", "spacing": "md",
                "contents": [
                    # الشعار
                    self._box([
                        self._text("🎮", "xxl"),
                        self._text("Bot Mesh", "xxl", "bold", margin="sm"),
                        self._text("بوت الألعاب الترفيهية", "sm",
                                  color=self.theme.text_secondary)
                    ], bg=self.theme.card, corner="25px", padding="xl"),
                    
                    # خطوات البداية
                    self._box([
                        self._text("✨ ابدأ الآن!", "lg", "bold", align="end"),
                        self._text("سجل واستمتع بـ 11 لعبة ممتعة", "sm",
                                  color=self.theme.text_secondary, align="end")
                    ], bg=self.theme.surface, corner="20px", margin="lg", padding="lg"),
                    
                    # المميزات
                    self._box([
                        self._text("⚡ المميزات", "md", "bold", align="end"),
                        self._text("• 14 لعبة متنوعة", "sm",
                                  color=self.theme.text_secondary, align="end", margin="sm"),
                        self._text("• 7 ثيمات جميلة", "sm",
                                  color=self.theme.text_secondary, align="end"),
                        self._text("• نظام نقاط وترتيب", "sm",
                                  color=self.theme.text_secondary, align="end"),
                        self._text("• لوحة صدارة عالمية", "sm",
                                  color=self.theme.text_secondary, align="end"),
                    ], bg=self.theme.card, corner="20px", margin="lg", padding="lg"),
                    
                    # أزرار
                    {
                        "type": "box", "layout": "horizontal",
                        "spacing": "sm", "margin": "xl",
                        "contents": [
                            self._button("🔑 انضم", "انضم", color=self.theme.accent),
                            self._button("📖 مساعدة", "مساعدة", "secondary"),
                        ]
                    },
                    
                    # الحقوق
                    self._text("Created by Abeer Aldosari © 2025", "xxs",
                              color=self.theme.text_secondary, margin="lg")
                ]
            }
        }
    
    # =========================================
    # بطاقة الإحصائيات
    # =========================================
    def create_stats_card(self, user_data: Dict, rank: int = 0) -> Dict:
        if not user_data:
            return self._create_error("لم تلعب بعد! اكتب 'انضم' ثم ابدأ اللعب")
        
        points = user_data.get('total_points', 0)
        games = user_data.get('games_played', 0)
        wins = user_data.get('wins', 0)
        win_rate = (wins / games * 100) if games > 0 else 0
        is_registered = user_data.get('is_registered', False)
        level = self._get_level(points)
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.background,
                "paddingAll": "20px", "spacing": "md",
                "contents": [
                    # الرأس
                    self._box([
                        {
                            "type": "box", "layout": "horizontal",
                            "justifyContent": "space-between", "alignItems": "center",
                            "contents": [
                                self._text(level['emoji'], "xxl"),
                                {
                                    "type": "box", "layout": "vertical",
                                    "contents": [
                                        self._text(level['name'], "xl", "bold", align="end"),
                                        self._text(f"المركز #{rank}" if rank else "غير مصنف",
                                                  "sm", color=self.theme.text_secondary, align="end")
                                    ]
                                }
                            ]
                        },
                        # حالة التسجيل
                        {
                            "type": "box", "layout": "horizontal",
                            "margin": "md", "spacing": "xs",
                            "contents": [
                                self._text("●", "xs",
                                          color=self.theme.success if is_registered else self.theme.error),
                                self._text("مسجل" if is_registered else "غير مسجل",
                                          "xs", color=self.theme.text_secondary)
                            ]
                        }
                    ], bg=self.theme.card, corner="25px", padding="xl"),
                    
                    # الإحصائيات
                    {
                        "type": "box", "layout": "horizontal",
                        "spacing": "md", "margin": "lg",
                        "contents": [
                            self._stat_box("💰", str(points), "نقطة"),
                            self._stat_box("🎮", str(games), "لعبة")
                        ]
                    },
                    {
                        "type": "box", "layout": "horizontal",
                        "spacing": "md", "margin": "md",
                        "contents": [
                            self._stat_box("🏆", str(wins), "فوز"),
                            self._stat_box("📈", f"{win_rate:.0f}%", "نسبة")
                        ]
                    },
                    
                    # رسالة حالة التسجيل
                    self._box([
                        self._text(
                            "✅ يمكنك اللعب الآن!" if is_registered else "⚠️ سجل أولاً لتلعب",
                            "sm", "bold",
                            color=self.theme.success if is_registered else self.theme.warning
                        )
                    ], bg=self.theme.card, corner="15px", margin="lg", padding="md"),
                    
                    # الأزرار
                    {
                        "type": "box", "layout": "vertical",
                        "spacing": "sm", "margin": "lg",
                        "contents": [
                            self._button("🎮 ابدأ لعبة", "ابدأ", color=self.theme.accent)
                            if is_registered else
                            self._button("🔑 انضم الآن", "انضم", color=self.theme.accent),
                            self._button("🏆 الصدارة", "الصدارة", "secondary")
                        ]
                    }
                ]
            }
        }
    
    def _stat_box(self, emoji: str, value: str, label: str) -> Dict:
        return {
            "type": "box", "layout": "vertical", "flex": 1,
            "backgroundColor": self.theme.card, "cornerRadius": "20px",
            "paddingAll": "lg", "spacing": "none",
            "contents": [
                self._text(emoji, "xxl"),
                self._text(value, "xl", "bold", margin="xs"),
                self._text(label, "xs", color=self.theme.text_secondary, margin="xs")
            ]
        }
    
    def _get_level(self, points: int) -> Dict:
        if points < 100:
            return {'name': '🌱 مبتدئ', 'emoji': '🌱'}
        elif points < 500:
            return {'name': '⭐ متوسط', 'emoji': '⭐'}
        elif points < 1000:
            return {'name': '🔥 محترف', 'emoji': '🔥'}
        elif points < 5000:
            return {'name': '👑 أسطوري', 'emoji': '👑'}
        return {'name': '💎 خارق', 'emoji': '💎'}
    
    # =========================================
    # لوحة الصدارة
    # =========================================
    def create_leaderboard(self, leaders: List[Dict]) -> Dict:
        if not leaders:
            return self._create_error("لا توجد بيانات")
        
        medals = ["🥇", "🥈", "🥉"]
        leader_items = []
        
        for i, leader in enumerate(leaders[:10]):
            medal = medals[i] if i < 3 else f"#{i+1}"
            is_top = i < 3
            
            leader_items.append(
                self._box([
                    {
                        "type": "box", "layout": "horizontal",
                        "justifyContent": "space-between", "alignItems": "center",
                        "contents": [
                            self._text(medal, "xl" if is_top else "lg"),
                            self._text(leader.get('display_name', 'لاعب'),
                                      "md", "bold" if is_top else "regular", align="center"),
                            self._text(f"{leader.get('total_points', 0)} ⭐",
                                      "md", "bold",
                                      color=self.theme.accent if is_top else self.theme.text_secondary)
                        ]
                    }
                ], bg=self.theme.card if is_top else "transparent",
                corner="15px", padding="md", margin="sm" if i > 0 else "none")
            )
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px",
                "contents": [
                    self._text("🏆 لوحة الصدارة", "xl", "bold", "#FFFFFF"),
                    self._text(f"أفضل {len(leaders)} لاعبين", "xs", color="#FFFFFFCC")
                ]
            },
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.background,
                "paddingAll": "20px",
                "contents": leader_items
            }
        }
    
    # =========================================
    # اختيار الثيم
    # =========================================
    def create_theme_selector(self) -> Dict:
        theme_buttons = []
        for theme_enum, theme_data in THEMES.items():
            theme_buttons.append(
                self._box([
                    {
                        "type": "box", "layout": "horizontal",
                        "justifyContent": "space-between", "alignItems": "center",
                        "contents": [
                            self._box([self._text(theme_data.emoji, "xl")],
                                    bg=theme_data.accent, corner="12px", padding="sm"),
                            self._text(theme_data.name_ar, "md", "bold", align="end")
                        ]
                    }
                ], bg=self.theme.card, corner="15px", padding="md", margin="sm",
                action={"type": "message", "text": f"ثيم:{theme_data.name}"})
            )
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.accent,
                "paddingAll": "20px",
                "contents": [
                    self._text("🎨 اختر الثيم المفضل", "xl", "bold", "#FFFFFF"),
                    self._text("7 ثيمات مميزة", "xs", color="#FFFFFFCC")
                ]
            },
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.background,
                "paddingAll": "20px", "spacing": "none",
                "contents": theme_buttons
            }
        }
    
    # =========================================
    # رسالة خطأ
    # =========================================
    def _create_error(self, message: str) -> Dict:
        return {
            "type": "bubble",
            "body": {
                "type": "box", "layout": "vertical",
                "backgroundColor": self.theme.background,
                "paddingAll": "40px", "spacing": "md",
                "contents": [
                    self._text("⚠️", "xxl"),
                    self._text(message, "md", margin="md")
                ]
            }
        }


# Singleton
flex_builder = FlexMessageBuilder()
