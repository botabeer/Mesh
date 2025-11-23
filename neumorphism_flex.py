"""
Bot Mesh - Neumorphism Soft Design System
Created by: Abeer Aldosari © 2025

نظام تصميم Neumorphism احترافي مع دعم LINE Bot
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class NeumorphismTheme(Enum):
    """الثيمات المتاحة - ستايل Neumorphism"""
    SOFT = "soft"           # الثيم الأساسي من الصورة
    DARK = "dark"           # نسخة داكنة
    OCEAN = "ocean"         # أزرق محيطي
    SUNSET = "sunset"       # غروب برتقالي
    FOREST = "forest"       # أخضر طبيعي


@dataclass
class NeumorphismColors:
    """ألوان الثيم بستايل Neumorphism"""
    name: str
    name_ar: str
    emoji: str
    
    # الخلفية الرئيسية
    background: str
    
    # لون الكارد/البطاقة
    card: str
    
    # ظلال Neumorphism
    shadow_light: str    # الظل الفاتح (أعلى يسار)
    shadow_dark: str     # الظل الداكن (أسفل يمين)
    
    # الألوان الأساسية
    primary: str         # اللون الأساسي
    accent: str          # لون التمييز
    
    # النصوص
    text_primary: str
    text_secondary: str
    
    # الأزرار
    button_bg: str
    button_text: str


# =============================================
# 🎨 الثيمات الخمسة بستايل Neumorphism
# =============================================
NEUMORPHISM_THEMES: Dict[NeumorphismTheme, NeumorphismColors] = {
    # 1. Soft Theme (من الصورة)
    NeumorphismTheme.SOFT: NeumorphismColors(
        name="soft", 
        name_ar="⚪ ناعم", 
        emoji="🎨",
        background="#E0E5EC",
        card="#E0E5EC",
        shadow_light="#FFFFFF",
        shadow_dark="#A3B1C6",
        primary="#6C8EEF",
        accent="#DADE2C",
        text_primary="#2C3E50",
        text_secondary="#7D8DA6",
        button_bg="#6C8EEF",
        button_text="#FFFFFF"
    ),
    
    # 2. Dark Theme
    NeumorphismTheme.DARK: NeumorphismColors(
        name="dark",
        name_ar="⚫ داكن",
        emoji="🌙",
        background="#2C3E50",
        card="#2C3E50",
        shadow_light="#3A4D63",
        shadow_dark="#1A2633",
        primary="#00D9FF",
        accent="#9D7AEA",
        text_primary="#FFFFFF",
        text_secondary="#A0AEC0",
        button_bg="#00D9FF",
        button_text="#2C3E50"
    ),
    
    # 3. Ocean Theme
    NeumorphismTheme.OCEAN: NeumorphismColors(
        name="ocean",
        name_ar="🌊 محيطي",
        emoji="🌊",
        background="#C8D8E8",
        card="#C8D8E8",
        shadow_light="#FFFFFF",
        shadow_dark="#9EB4C8",
        primary="#0EA5E9",
        accent="#38BDF8",
        text_primary="#0C4A6E",
        text_secondary="#475569",
        button_bg="#0EA5E9",
        button_text="#FFFFFF"
    ),
    
    # 4. Sunset Theme
    NeumorphismTheme.SUNSET: NeumorphismColors(
        name="sunset",
        name_ar="🌅 غروب",
        emoji="🌅",
        background="#FFE8D6",
        card="#FFE8D6",
        shadow_light="#FFFFFF",
        shadow_dark="#D4BCA4",
        primary="#F97316",
        accent="#FB923C",
        text_primary="#7C2D12",
        text_secondary="#92400E",
        button_bg="#F97316",
        button_text="#FFFFFF"
    ),
    
    # 5. Forest Theme
    NeumorphismTheme.FOREST: NeumorphismColors(
        name="forest",
        name_ar="🌲 طبيعي",
        emoji="🌲",
        background="#D4E4D4",
        card="#D4E4D4",
        shadow_light="#FFFFFF",
        shadow_dark="#A8C4A8",
        primary="#10B981",
        accent="#34D399",
        text_primary="#064E3B",
        text_secondary="#047857",
        button_bg="#10B981",
        button_text="#FFFFFF"
    )
}


class NeumorphismFlexBuilder:
    """منشئ رسائل Flex بستايل Neumorphism"""
    
    def __init__(self, theme: NeumorphismTheme = NeumorphismTheme.SOFT):
        self.theme = NEUMORPHISM_THEMES.get(theme, NEUMORPHISM_THEMES[NeumorphismTheme.SOFT])
    
    def set_theme(self, theme_name: str):
        """تغيير الثيم"""
        theme_map = {t.value: t for t in NeumorphismTheme}
        theme = theme_map.get(theme_name.lower(), NeumorphismTheme.SOFT)
        self.theme = NEUMORPHISM_THEMES[theme]
    
    # ==========================================
    # 🎨 مكونات Neumorphism الأساسية
    # ==========================================
    
    def _neu_card(self, contents: List, padding: str = "xl", 
                  margin: str = "none", spacing: str = "md") -> Dict:
        """بطاقة بتأثير Neumorphism"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": self.theme.card,
            "cornerRadius": "20px",
            "paddingAll": padding,
            "margin": margin,
            "spacing": spacing,
            # تأثير الظل المزدوج لـ Neumorphism
            "offsetTop": "3px",
            "offsetStart": "3px"
        }
    
    def _neu_button(self, emoji: str, text: str, action_text: str) -> Dict:
        """زر بتأثير Neumorphism مع الإيموجي والنص"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        # الإيموجي
                        {
                            "type": "text",
                            "text": emoji,
                            "size": "xxl",
                            "align": "center",
                            "color": self.theme.primary
                        },
                        # النص
                        {
                            "type": "text",
                            "text": text,
                            "size": "sm",
                            "align": "center",
                            "color": self.theme.text_primary,
                            "weight": "bold",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": self.theme.card,
                    "cornerRadius": "15px",
                    "paddingAll": "md",
                    "spacing": "xs"
                }
            ],
            "action": {
                "type": "message",
                "label": text,
                "text": action_text
            },
            "flex": 1
        }
    
    def _neu_text(self, text: str, size: str = "md", weight: str = "regular",
                  color: str = None, align: str = "center") -> Dict:
        """نص مع تنسيق"""
        return {
            "type": "text",
            "text": text,
            "size": size,
            "weight": weight,
            "color": color or self.theme.text_primary,
            "align": align,
            "wrap": True
        }
    
    def _neu_separator(self) -> Dict:
        """فاصل بتأثير خفيف"""
        return {
            "type": "separator",
            "margin": "xl",
            "color": self.theme.shadow_dark + "40"
        }
    
    # ==========================================
    # 🎮 نافذة الألعاب الرئيسية (مثل الصورة)
    # ==========================================
    
    def create_game_card(self, game_data: Dict) -> Dict:
        """
        بطاقة لعبة واحدة بستايل Neumorphism
        
        game_data = {
            'emoji': '🧠',
            'title': 'لعبة تكوين الكلمات',
            'question': 'سؤال 1 من 5',
            'letters': ['ق', 'ي', 'ر', 'ل', 'ر', 'ل'],
            'hint': 'كون 3 كلمات من هذه الحروف\nاكتب كلمة واحدة في كل رسالة',
            'game_command': 'تكوين'
        }
        """
        # صف الحروف (Grid Layout)
        letters_grid = []
        for i in range(0, len(game_data['letters']), 3):
            row_letters = game_data['letters'][i:i+3]
            row = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": letter,
                                "size": "xxl",
                                "align": "center",
                                "color": self.theme.primary,
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": self.theme.card,
                        "cornerRadius": "15px",
                        "paddingAll": "lg",
                        "flex": 1,
                        "margin": "xs"
                    }
                    for letter in row_letters
                ],
                "spacing": "md",
                "margin": "sm" if i > 0 else "md"
            }
            letters_grid.append(row)
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # العنوان
                    self._neu_card([
                        self._neu_text(
                            f"{game_data['emoji']} {game_data['title']}", 
                            "lg", "bold"
                        ),
                        self._neu_text(
                            game_data['question'],
                            "sm", color=self.theme.text_secondary
                        )
                    ], padding="lg"),
                    
                    # منطقة الحروف
                    self._neu_card(letters_grid, padding="lg", margin="lg"),
                    
                    # التلميح
                    self._neu_card([
                        self._neu_text(
                            game_data['hint'],
                            "sm", color=self.theme.text_secondary
                        )
                    ], padding="md", margin="md"),
                    
                    # أزرار الحل والتلميح
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "الحل",
                                    "text": "جاوب"
                                },
                                "style": "secondary",
                                "height": "sm",
                                "color": self.theme.shadow_dark
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "تلميح",
                                    "text": "لمح"
                                },
                                "style": "primary",
                                "height": "sm",
                                "color": self.theme.button_bg
                            }
                        ],
                        "spacing": "md",
                        "margin": "lg"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px",
                "spacing": "none"
            }
        }
    
    # ==========================================
    # 🏠 الشاشة الرئيسية
    # ==========================================
    
    def create_welcome_screen(self) -> Dict:
        """شاشة الترحيب الرئيسية"""
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # الشعار والعنوان
                    self._neu_card([
                        self._neu_text("🎮", "xxl"),
                        self._neu_text("Bot Mesh", "xl", "bold", margin="sm"),
                        self._neu_text(
                            "بوت الألعاب الترفيهية",
                            "sm", color=self.theme.text_secondary
                        )
                    ], padding="xl"),
                    
                    # رسالة البداية
                    self._neu_card([
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        self._neu_text("✨", "xxl")
                                    ],
                                    "backgroundColor": self.theme.primary + "30",
                                    "cornerRadius": "15px",
                                    "paddingAll": "md",
                                    "width": "60px",
                                    "height": "60px",
                                    "justifyContent": "center"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        self._neu_text(
                                            "ابدأ الآن!",
                                            "md", "bold",
                                            align="right"
                                        ),
                                        self._neu_text(
                                            "اختر لعبة من الأزرار أسفل الشاشة",
                                            "xs",
                                            color=self.theme.text_secondary,
                                            align="right"
                                        )
                                    ],
                                    "flex": 1,
                                    "margin": "md",
                                    "justifyContent": "center"
                                }
                            ],
                            "spacing": "md"
                        }
                    ], margin="lg"),
                    
                    # المميزات
                    self._neu_card([
                        self._neu_text("⚡ المميزات", "md", "bold", align="right"),
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                self._neu_text(
                                    "• 11 لعبة متنوعة ومسلية",
                                    "sm", color=self.theme.text_secondary,
                                    align="right"
                                ),
                                self._neu_text(
                                    "• 5 ثيمات جميلة",
                                    "sm", color=self.theme.text_secondary,
                                    align="right"
                                ),
                                self._neu_text(
                                    "• نظام نقاط وترتيب",
                                    "sm", color=self.theme.text_secondary,
                                    align="right"
                                ),
                                self._neu_text(
                                    "• لوحة صدارة عالمية",
                                    "sm", color=self.theme.text_secondary,
                                    align="right"
                                )
                            ],
                            "spacing": "sm",
                            "margin": "md"
                        }
                    ], margin="lg"),
                    
                    # نصيحة
                    self._neu_card([
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                self._neu_text("💡", "md"),
                                self._neu_text(
                                    "استخدم الأزرار الثابتة أسفل الشاشة للوصول السريع!",
                                    "xs",
                                    color=self.theme.text_secondary,
                                    align="right"
                                )
                            ],
                            "justifyContent": "space-between",
                            "spacing": "sm"
                        }
                    ], padding="md", margin="lg"),
                    
                    # الحقوق
                    self._neu_text(
                        "Created by Abeer Aldosari © 2025",
                        "xxs",
                        color=self.theme.text_secondary,
                        margin="xl"
                    )
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px",
                "spacing": "none"
            }
        }
    
    # ==========================================
    # 📊 بطاقة الإحصائيات
    # ==========================================
    
    def create_stats_card(self, user_data: Dict, rank: int = 0) -> Dict:
        """بطاقة الإحصائيات بستايل Neumorphism"""
        points = user_data.get('total_points', 0)
        games = user_data.get('games_played', 0)
        wins = user_data.get('wins', 0)
        rate = (wins / games * 100) if games > 0 else 0
        
        # تحديد المستوى
        if points < 100:
            level = {'name': '🌱 مبتدئ', 'color': self.theme.primary}
        elif points < 500:
            level = {'name': '⭐ متوسط', 'color': '#F6AD55'}
        elif points < 1000:
            level = {'name': '🔥 محترف', 'color': '#FC8181'}
        else:
            level = {'name': '👑 أسطوري', 'color': '#A855F7'}
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # المستوى
                    self._neu_card([
                        self._neu_text(level['name'], "xl", "bold"),
                        self._neu_text(
                            f"المركز #{rank}" if rank else "غير مصنف",
                            "sm", color=self.theme.text_secondary
                        )
                    ]),
                    
                    # الإحصائيات
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._stat_box("💰", str(points), "نقطة"),
                            self._stat_box("🎮", str(games), "لعبة")
                        ],
                        "spacing": "md",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._stat_box("🏆", str(wins), "فوز"),
                            self._stat_box("📈", f"{rate:.0f}%", "نسبة")
                        ],
                        "spacing": "md",
                        "margin": "md"
                    },
                    
                    # زر العودة
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "🎮 ارجع للألعاب",
                            "text": "بداية"
                        },
                        "style": "primary",
                        "height": "sm",
                        "color": self.theme.button_bg,
                        "margin": "xl"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px",
                "spacing": "none"
            }
        }
    
    def _stat_box(self, emoji: str, value: str, label: str) -> Dict:
        """صندوق إحصائية واحدة"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                self._neu_text(emoji, "xxl"),
                self._neu_text(value, "xl", "bold", margin="xs"),
                self._neu_text(
                    label, "xs",
                    color=self.theme.text_secondary,
                    margin="xs"
                )
            ],
            "backgroundColor": self.theme.card,
            "cornerRadius": "20px",
            "paddingAll": "lg",
            "flex": 1,
            "spacing": "none"
        }
    
    # ==========================================
    # 🎨 اختيار الثيم
    # ==========================================
    
    def create_theme_selector(self) -> Dict:
        """نافذة اختيار الثيمات"""
        theme_buttons = []
        
        for theme_enum, theme_data in NEUMORPHISM_THEMES.items():
            theme_buttons.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._neu_text(theme_data.emoji, "xl")
                        ],
                        "backgroundColor": theme_data.primary + "30",
                        "cornerRadius": "12px",
                        "paddingAll": "sm",
                        "width": "50px",
                        "height": "50px",
                        "justifyContent": "center"
                    },
                    self._neu_text(
                        theme_data.name_ar,
                        "md", "bold",
                        align="right"
                    )
                ],
                "backgroundColor": self.theme.card,
                "cornerRadius": "15px",
                "paddingAll": "md",
                "margin": "sm",
                "justifyContent": "space-between",
                "alignItems": "center",
                "action": {
                    "type": "message",
                    "text": f"ثيم:{theme_data.name}"
                }
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._neu_card([
                        self._neu_text("🎨 اختر الثيم المفضل", "xl", "bold")
                    ]),
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": theme_buttons,
                        "margin": "lg"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px"
            }
        }
    
    # ==========================================
    # 🏆 لوحة الصدارة
    # ==========================================
    
    def create_leaderboard(self, leaders: List[Dict]) -> Dict:
        """لوحة الصدارة بستايل Neumorphism"""
        medals = ["🥇", "🥈", "🥉"]
        leader_items = []
        
        for i, leader in enumerate(leaders[:10]):
            medal = medals[i] if i < 3 else f"#{i+1}"
            is_top = i < 3
            
            leader_items.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._neu_text(medal, "xl" if is_top else "md")
                        ],
                        "backgroundColor": self.theme.primary + "30" if is_top else "transparent",
                        "cornerRadius": "12px",
                        "paddingAll": "sm",
                        "width": "50px",
                        "height": "50px",
                        "justifyContent": "center"
                    },
                    self._neu_text(
                        leader.get('display_name', 'لاعب'),
                        "md", "bold" if is_top else "regular",
                        align="right"
                    ),
                    self._neu_text(
                        f"{leader.get('total_points', 0)} ⭐",
                        "md", "bold",
                        color=self.theme.primary if is_top else self.theme.text_secondary
                    )
                ],
                "backgroundColor": self.theme.card if is_top else "transparent",
                "cornerRadius": "15px",
                "paddingAll": "md",
                "margin": "sm" if i > 0 else "none",
                "justifyContent": "space-between",
                "alignItems": "center"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._neu_card([
                        self._neu_text("🏆 لوحة الصدارة", "xl", "bold"),
                        self._neu_text(
                            f"أفضل {len(leaders)} لاعبين",
                            "sm", color=self.theme.text_secondary
                        )
                    ]),
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": leader_items,
                        "margin": "lg"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px"
            }
        }


# =============================================
# 🎮 مثال على الاستخدام
# =============================================
if __name__ == "__main__":
    # إنشاء builder
    builder = NeumorphismFlexBuilder(NeumorphismTheme.SOFT)
    
    # مثال: بطاقة لعبة
    game_data = {
        'emoji': '✏️',
        'title': 'لعبة تكوين الكلمات',
        'question': 'سؤال 1 من 5',
        'letters': ['ق', 'ي', 'ر', 'ل', 'ر', 'ل'],
        'hint': 'كون 3 كلمات من هذه الحروف\nاكتب كلمة واحدة في كل رسالة',
        'game_command': 'تكوين'
    }
    
    card = builder.create_game_card(game_data)
    print("✅ تم إنشاء بطاقة اللعبة بنجاح!")
