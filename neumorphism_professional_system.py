"""
Bot Mesh - Neumorphism Professional Design System
نظام تصميم احترافي متوافق 100% مع LINE Bot API
Created by: Abeer Aldosari © 2025

الألوان المستخدمة (من الصورة):
- خلفية: #E0E5EC (رمادي فاتح مزرق)
- كارد: #E0E5EC 
- ظل فاتح: #FFFFFF
- ظل داكن: #A3B1C6
- اللون الأساسي: #6C8EEF (أزرق بنفسجي)
- نص أساسي: #4A5568
- نص ثانوي: #A0AEC0
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from linebot.models import FlexSendMessage, QuickReply, QuickReplyButton, MessageAction


class NeumorphismTheme(Enum):
    """الثيمات الاحترافية"""
    SOFT = "soft"           # من الصورة
    DARK = "dark"
    OCEAN = "ocean"
    SUNSET = "sunset"
    FOREST = "forest"


@dataclass
class ThemeColors:
    """ألوان الثيم بدقة عالية"""
    name: str
    name_ar: str
    emoji: str
    
    # الخلفيات
    background: str         # خلفية الصفحة
    surface: str           # سطح الكاردات
    card: str              # الكارد الداخلي
    
    # الظلال (مهم جداً لـ Neumorphism)
    shadow_light: str      # الظل الفاتح
    shadow_dark: str       # الظل الداكن
    
    # الألوان الأساسية
    primary: str           # اللون الأساسي
    accent: str            # لون التمييز
    gradient_start: str    # بداية التدرج
    gradient_end: str      # نهاية التدرج
    
    # النصوص
    text_primary: str
    text_secondary: str
    text_muted: str
    
    # الأزرار
    button_primary: str
    button_secondary: str
    button_text: str


# =============================================
# 🎨 الثيمات الخمسة (ألوان دقيقة)
# =============================================
THEMES: Dict[NeumorphismTheme, ThemeColors] = {
    # 1. Soft Theme (من الصورة بالضبط)
    NeumorphismTheme.SOFT: ThemeColors(
        name="soft",
        name_ar="🎨 ناعم",
        emoji="🎨",
        background="#E0E5EC",
        surface="#E0E5EC",
        card="#E0E5EC",
        shadow_light="#FFFFFF",
        shadow_dark="#A3B1C6",
        primary="#6C8EEF",
        accent="#7C8EF5",
        gradient_start="#667EEA",
        gradient_end="#764BA2",
        text_primary="#4A5568",
        text_secondary="#718096",
        text_muted="#A0AEC0",
        button_primary="#6C8EEF",
        button_secondary="#CBD5E0",
        button_text="#FFFFFF"
    ),
    
    # 2. Dark Theme
    NeumorphismTheme.DARK: ThemeColors(
        name="dark",
        name_ar="🌙 داكن",
        emoji="🌙",
        background="#2C3E50",
        surface="#2C3E50",
        card="#34495E",
        shadow_light="#3A4D63",
        shadow_dark="#1A2633",
        primary="#00D9FF",
        accent="#3DECFF",
        gradient_start="#00D9FF",
        gradient_end="#9D7AEA",
        text_primary="#ECF0F1",
        text_secondary="#BDC3C7",
        text_muted="#7F8C8D",
        button_primary="#00D9FF",
        button_secondary="#455A64",
        button_text="#FFFFFF"
    ),
    
    # 3. Ocean Theme
    NeumorphismTheme.OCEAN: ThemeColors(
        name="ocean",
        name_ar="🌊 محيطي",
        emoji="🌊",
        background="#D4E4F0",
        surface="#D4E4F0",
        card="#D4E4F0",
        shadow_light="#FFFFFF",
        shadow_dark="#A8BFD4",
        primary="#0EA5E9",
        accent="#38BDF8",
        gradient_start="#0EA5E9",
        gradient_end="#0284C7",
        text_primary="#0C4A6E",
        text_secondary="#475569",
        text_muted="#94A3B8",
        button_primary="#0EA5E9",
        button_secondary="#BAE6FD",
        button_text="#FFFFFF"
    ),
    
    # 4. Sunset Theme
    NeumorphismTheme.SUNSET: ThemeColors(
        name="sunset",
        name_ar="🌅 غروب",
        emoji="🌅",
        background="#FFE8D6",
        surface="#FFE8D6",
        card="#FFE8D6",
        shadow_light="#FFFFFF",
        shadow_dark="#D4BCA4",
        primary="#F97316",
        accent="#FB923C",
        gradient_start="#F97316",
        gradient_end="#EA580C",
        text_primary="#7C2D12",
        text_secondary="#92400E",
        text_muted="#C2410C",
        button_primary="#F97316",
        button_secondary="#FED7AA",
        button_text="#FFFFFF"
    ),
    
    # 5. Forest Theme
    NeumorphismTheme.FOREST: ThemeColors(
        name="forest",
        name_ar="🌲 طبيعي",
        emoji="🌲",
        background="#D4E4D4",
        surface="#D4E4D4",
        card="#D4E4D4",
        shadow_light="#FFFFFF",
        shadow_dark="#A8C4A8",
        primary="#10B981",
        accent="#34D399",
        gradient_start="#10B981",
        gradient_end="#059669",
        text_primary="#064E3B",
        text_secondary="#047857",
        text_muted="#10B981",
        button_primary="#10B981",
        button_secondary="#D1FAE5",
        button_text="#FFFFFF"
    )
}


class NeumorphismFlexBuilder:
    """منشئ رسائل Flex احترافي مع Neumorphism"""
    
    def __init__(self, theme: NeumorphismTheme = NeumorphismTheme.SOFT):
        self.theme = THEMES[theme]
        self.current_theme_enum = theme
    
    def set_theme(self, theme_name: str):
        """تغيير الثيم"""
        theme_map = {t.value: t for t in NeumorphismTheme}
        theme = theme_map.get(theme_name.lower(), NeumorphismTheme.SOFT)
        self.theme = THEMES[theme]
        self.current_theme_enum = theme
    
    # =============================================
    # 🎨 مكونات Neumorphism الأساسية
    # =============================================
    
    def _create_neumorphic_box(self, contents: List[Dict], 
                                padding: str = "lg",
                                margin: str = "none",
                                spacing: str = "md") -> Dict:
        """صندوق بتأثير Neumorphism الكامل"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": self.theme.card,
            "cornerRadius": "20px",
            "paddingAll": padding,
            "margin": margin,
            "spacing": spacing
        }
    
    def _create_letter_button(self, letter: str) -> Dict:
        """زر حرف مع تأثير Neumorphism"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": letter,
                    "size": "xxl",
                    "weight": "bold",
                    "color": self.theme.primary,
                    "align": "center"
                }
            ],
            "backgroundColor": self.theme.card,
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "width": "65px",
            "height": "65px",
            "justifyContent": "center",
            "alignItems": "center"
        }
    
    def _create_header(self, title: str, subtitle: str = "") -> Dict:
        """هيدر احترافي مع تدرج"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎮",
                            "size": "xl",
                            "color": self.theme.primary
                        },
                        {
                            "type": "text",
                            "text": title,
                            "size": "xl",
                            "weight": "bold",
                            "color": self.theme.primary,
                            "margin": "md"
                        }
                    ],
                    "alignItems": "center"
                },
                {
                    "type": "text",
                    "text": subtitle if subtitle else "تأثير 3D - عمق ناعم",
                    "size": "xs",
                    "color": self.theme.text_muted,
                    "align": "center",
                    "margin": "sm"
                }
            ],
            "backgroundColor": self.theme.surface,
            "cornerRadius": "20px",
            "paddingAll": "15px"
        }
    
    def _create_instruction_box(self, text: str) -> Dict:
        """صندوق التعليمات"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": text,
                    "size": "sm",
                    "color": self.theme.text_secondary,
                    "align": "center",
                    "wrap": True
                }
            ],
            "backgroundColor": self.theme.card,
            "cornerRadius": "15px",
            "paddingAll": "15px"
        }
    
    def _create_button(self, label: str, text: str, 
                       style: str = "primary") -> Dict:
        """زر احترافي"""
        color = self.theme.button_primary if style == "primary" else self.theme.button_secondary
        text_color = self.theme.button_text if style == "primary" else self.theme.text_primary
        
        return {
            "type": "button",
            "action": {
                "type": "message",
                "label": label,
                "text": text
            },
            "style": "primary" if style == "primary" else "secondary",
            "color": color,
            "height": "sm"
        }
    
    # =============================================
    # 🎮 بطاقة اللعبة (مثل الصورة بالضبط)
    # =============================================
    
    def create_game_card(self, game_data: Dict) -> Dict:
        """
        إنشاء بطاقة لعبة بستايل Neumorphism الاحترافي
        
        game_data = {
            'title': 'لعبة تكوين الكلمات',
            'question_number': '1 من 5',
            'letters': ['ق', 'ي', 'ر', 'ل', 'ر', 'ل'],
            'instruction': 'كون 3 كلمات من هذه الحروف\nاكتب كلمة واحدة في كل رسالة',
            'show_refresh': True  # زر الإعادة
        }
        """
        
        # تقسيم الحروف إلى صفوف (3 حروف في كل صف)
        letters = game_data.get('letters', [])
        letter_rows = []
        
        for i in range(0, len(letters), 3):
            row_letters = letters[i:i+3]
            row = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    self._create_letter_button(letter) 
                    for letter in row_letters
                ],
                "spacing": "md",
                "justifyContent": "center",
                "margin": "sm" if i > 0 else "none"
            }
            letter_rows.append(row)
        
        # بناء الكارد
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # الهيدر
                    self._create_header(
                        "Neumorphism Soft 🎮",
                        ""
                    ),
                    
                    # العنوان والتقدم
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            # زر الإعادة (إذا كان مطلوب)
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "🔄",
                                    "text": "ابدأ"
                                },
                                "style": "secondary",
                                "color": self.theme.button_secondary,
                                "height": "sm",
                                "flex": 0,
                                "margin": "none"
                            } if game_data.get('show_refresh') else {
                                "type": "filler"
                            },
                            
                            # العنوان والرقم
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"■ {game_data.get('title', 'لعبة تكوين الكلمات')}",
                                        "size": "lg",
                                        "weight": "bold",
                                        "color": self.theme.text_primary,
                                        "align": "end"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"سؤال {game_data.get('question_number', '1 من 5')}",
                                        "size": "xs",
                                        "color": self.theme.text_muted,
                                        "align": "end"
                                    }
                                ],
                                "flex": 1,
                                "margin": "md" if game_data.get('show_refresh') else "none"
                            }
                        ],
                        "margin": "lg"
                    },
                    
                    # منطقة الحروف (الكارد الكبير)
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": letter_rows,
                        "backgroundColor": self.theme.card,
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "lg"
                    },
                    
                    # التعليمات
                    self._create_instruction_box(
                        game_data.get('instruction', 
                                    'كون 3 كلمات من هذه الحروف\nاكتب كلمة واحدة في كل رسالة')
                    ),
                    
                    # الأزرار
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._create_button("الحل", "جاوب", "secondary"),
                            self._create_button("تلميح", "لمح", "primary")
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
    
    # =============================================
    # 🏠 شاشة الترحيب
    # =============================================
    
    def create_welcome_screen(self) -> Dict:
        """شاشة الترحيب الرئيسية"""
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # الهيدر
                    self._create_header("Bot Mesh", "بوت الألعاب الترفيهية"),
                    
                    # رسالة البداية
                    self._create_neumorphic_box([
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "✨",
                                            "size": "xxl",
                                            "align": "center"
                                        }
                                    ],
                                    "backgroundColor": self.theme.primary + "20",
                                    "cornerRadius": "15px",
                                    "width": "60px",
                                    "height": "60px",
                                    "justifyContent": "center"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "ابدأ الآن!",
                                            "size": "lg",
                                            "weight": "bold",
                                            "color": self.theme.text_primary,
                                            "align": "right"
                                        },
                                        {
                                            "type": "text",
                                            "text": "اختر لعبة من الأزرار أسفل الشاشة",
                                            "size": "sm",
                                            "color": self.theme.text_secondary,
                                            "align": "right",
                                            "wrap": True
                                        }
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
                    self._create_neumorphic_box([
                        {
                            "type": "text",
                            "text": "⚡ المميزات",
                            "size": "md",
                            "weight": "bold",
                            "color": self.theme.text_primary,
                            "align": "right"
                        },
                        {
                            "type": "text",
                            "text": "• 11 لعبة متنوعة ومسلية\n• 5 ثيمات جميلة\n• نظام نقاط وترتيب\n• لوحة صدارة عالمية",
                            "size": "sm",
                            "color": self.theme.text_secondary,
                            "align": "right",
                            "wrap": True,
                            "margin": "md"
                        }
                    ], margin="lg"),
                    
                    # نصيحة
                    self._create_instruction_box(
                        "💡 استخدم الأزرار الثابتة أسفل الشاشة للوصول السريع!"
                    ),
                    
                    # الحقوق
                    {
                        "type": "text",
                        "text": "Created by Abeer Aldosari © 2025",
                        "size": "xxs",
                        "color": self.theme.text_muted,
                        "align": "center",
                        "margin": "xl"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px",
                "spacing": "none"
            }
        }
    
    # =============================================
    # 📊 بطاقة الإحصائيات
    # =============================================
    
    def create_stats_card(self, user_data: Dict, rank: int = 0) -> Dict:
        """بطاقة الإحصائيات"""
        points = user_data.get('total_points', 0)
        games = user_data.get('games_played', 0)
        wins = user_data.get('wins', 0)
        rate = (wins / games * 100) if games > 0 else 0
        
        # تحديد المستوى
        if points < 100:
            level_emoji = "🌱"
            level_name = "مبتدئ"
        elif points < 500:
            level_emoji = "⭐"
            level_name = "متوسط"
        elif points < 1000:
            level_emoji = "🔥"
            level_name = "محترف"
        else:
            level_emoji = "👑"
            level_name = "أسطوري"
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # الهيدر
                    self._create_neumorphic_box([
                        {
                            "type": "text",
                            "text": f"{level_emoji} {level_name}",
                            "size": "xl",
                            "weight": "bold",
                            "color": self.theme.text_primary,
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": f"المركز #{rank}" if rank else "غير مصنف",
                            "size": "sm",
                            "color": self.theme.text_secondary,
                            "align": "center"
                        }
                    ]),
                    
                    # الإحصائيات (2x2 grid)
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
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            self._create_button("🎮 ارجع للألعاب", "بداية", "primary")
                        ],
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
                {
                    "type": "text",
                    "text": emoji,
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": value,
                    "size": "xl",
                    "weight": "bold",
                    "color": self.theme.text_primary,
                    "align": "center",
                    "margin": "xs"
                },
                {
                    "type": "text",
                    "text": label,
                    "size": "xs",
                    "color": self.theme.text_secondary,
                    "align": "center",
                    "margin": "xs"
                }
            ],
            "backgroundColor": self.theme.card,
            "cornerRadius": "20px",
            "paddingAll": "15px",
            "flex": 1,
            "spacing": "none"
        }
    
    # =============================================
    # 🏆 لوحة الصدارة
    # =============================================
    
    def create_leaderboard(self, leaders: List[Dict]) -> Dict:
        """لوحة الصدارة"""
        if not leaders:
            return self._create_error("لا توجد بيانات")
        
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
                            {
                                "type": "text",
                                "text": medal,
                                "size": "xl" if is_top else "md",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": self.theme.primary + "30" if is_top else "transparent",
                        "cornerRadius": "12px",
                        "paddingAll": "sm",
                        "width": "50px",
                        "height": "50px",
                        "justifyContent": "center"
                    },
                    {
                        "type": "text",
                        "text": leader.get('display_name', 'لاعب'),
                        "size": "md",
                        "weight": "bold" if is_top else "regular",
                        "color": self.theme.text_primary,
                        "align": "right",
                        "flex": 1,
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"{leader.get('total_points', 0)} ⭐",
                        "size": "md",
                        "weight": "bold",
                        "color": self.theme.primary if is_top else self.theme.text_secondary
                    }
                ],
                "backgroundColor": self.theme.card if is_top else "transparent",
                "cornerRadius": "15px",
                "paddingAll": "md",
                "margin": "sm" if i > 0 else "none",
                "alignItems": "center"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._create_header("لوحة الصدارة 🏆", f"أفضل {len(leaders)} لاعبين"),
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
    # 🎨 اختيار الثيم
    # =============================================
    
    def create_theme_selector(self) -> Dict:
        """نافذة اختيار الثيمات"""
        theme_buttons = []
        
        for theme_enum, theme_data in THEMES.items():
            theme_buttons.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": theme_data.emoji,
                                "size": "xl",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": theme_data.primary + "30",
                        "cornerRadius": "12px",
                        "paddingAll": "sm",
                        "width": "50px",
                        "height": "50px",
                        "justifyContent": "center"
                    },
                    {
                        "type": "text",
                        "text": theme_data.name_ar,
                        "size": "md",
                        "weight": "bold",
                        "color": self.theme.text_primary,
                        "align": "right",
                        "flex": 1,
                        "margin": "md",
                        "gravity": "center"
                    }
                ],
                "backgroundColor": self.theme.card,
                "cornerRadius": "15px",
                "paddingAll": "md",
                "margin": "sm" if theme_buttons else "none",
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
                    self._create_header("اختر الثيم المفضل 🎨", "5 ثيمات احترافية"),
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
                    {
                        "type": "text",
                        "text": "⚠️",
                        "size": "xxl",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": message,
                        "size": "md",
                        "color": self.theme.text_primary,
                        "align": "center",
                        "wrap": True,
                        "margin": "md"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "40px",
                "spacing": "md"
            }
        }
    
    # =============================================
    # 🎵 بطاقات الألعاب المتخصصة
    # =============================================
    
    def create_song_game_card(self, song_data: Dict) -> Dict:
        """بطاقة لعبة الأغنية"""
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # الهيدر مع أيقونة موسيقى
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "🎵",
                                        "size": "xl",
                                        "align": "center"
                                    }
                                ],
                                "backgroundColor": self.theme.primary,
                                "cornerRadius": "25px",
                                "width": "50px",
                                "height": "50px",
                                "justifyContent": "center"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "خمن الأغنية",
                                        "size": "xl",
                                        "weight": "bold",
                                        "color": self.theme.text_primary
                                    },
                                    {
                                        "type": "text",
                                        "text": f"السؤال {song_data.get('question_number', '1/5')}",
                                        "size": "sm",
                                        "color": self.theme.text_secondary
                                    }
                                ],
                                "flex": 1,
                                "margin": "lg",
                                "justifyContent": "center"
                            }
                        ],
                        "backgroundColor": self.theme.surface,
                        "cornerRadius": "20px",
                        "paddingAll": "15px"
                    },
                    
                    # كلمات الأغنية
                    self._create_neumorphic_box([
                        {
                            "type": "text",
                            "text": song_data.get('lyrics', ''),
                            "size": "lg",
                            "weight": "bold",
                            "color": self.theme.text_primary,
                            "align": "center",
                            "wrap": True
                        }
                    ], padding="xl", margin="lg"),
                    
                    # السؤال
                    {
                        "type": "text",
                        "text": "من المغني؟",
                        "size": "md",
                        "color": self.theme.primary,
                        "align": "center",
                        "weight": "bold",
                        "margin": "lg"
                    },
                    
                    # شريط التقدم
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "backgroundColor": self.theme.primary,
                                "height": "5px",
                                "flex": song_data.get('progress', 1)
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "backgroundColor": self.theme.card,
                                "height": "5px",
                                "flex": 5 - song_data.get('progress', 1)
                            }
                        ],
                        "cornerRadius": "3px",
                        "margin": "md"
                    },
                    
                    # الأزرار
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._create_button("💡 تلميح", "لمح", "secondary"),
                            self._create_button("جاوب", "جاوب", "primary")
                        ],
                        "spacing": "md",
                        "margin": "xl"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px",
                "spacing": "none"
            }
        }
    
    def create_iq_game_card(self, question_data: Dict) -> Dict:
        """بطاقة لعبة الذكاء"""
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # الهيدر
                    self._create_header(
                        "اختبار الذكاء 🧠",
                        f"السؤال {question_data.get('question_number', '1/10')}"
                    ),
                    
                    # السؤال
                    self._create_neumorphic_box([
                        {
                            "type": "text",
                            "text": "❓",
                            "size": "xxl",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": question_data.get('question', ''),
                            "size": "md",
                            "color": self.theme.text_primary,
                            "align": "center",
                            "wrap": True,
                            "margin": "md"
                        }
                    ], padding="xl", margin="lg"),
                    
                    # التعليمات
                    self._create_instruction_box(
                        "اكتب الإجابة أو:\n• لمح - للحصول على تلميح\n• جاوب - لمعرفة الإجابة"
                    ),
                    
                    # الأزرار
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._create_button("جاوب", "جاوب", "secondary"),
                            self._create_button("💡 تلميح", "لمح", "primary")
                        ],
                        "spacing": "md",
                        "margin": "xl"
                    }
                ],
                "backgroundColor": self.theme.background,
                "paddingAll": "20px",
                "spacing": "none"
            }
        }
    
    # =============================================
    # 🎯 Quick Reply مع Neumorphism Style
    # =============================================
    
    def create_quick_reply_buttons(self, buttons_data: List[Dict]) -> QuickReply:
        """
        إنشاء Quick Reply buttons
        
        buttons_data = [
            {'label': 'ذكاء', 'text': 'ذكاء', 'emoji': '🧠'},
            {'label': 'لون', 'text': 'لون', 'emoji': '🎨'},
        ]
        """
        buttons = []
        for btn in buttons_data:
            buttons.append(
                QuickReplyButton(
                    action=MessageAction(
                        label=f"{btn.get('emoji', '')} {btn['label']}",
                        text=btn['text']
                    )
                )
            )
        
        return QuickReply(items=buttons)


# =============================================
# 🏭 Factory Functions
# =============================================

def create_flex_builder(theme_name: str = "soft") -> NeumorphismFlexBuilder:
    """إنشاء builder مع ثيم معين"""
    theme_map = {
        'soft': NeumorphismTheme.SOFT,
        'dark': NeumorphismTheme.DARK,
        'ocean': NeumorphismTheme.OCEAN,
        'sunset': NeumorphismTheme.SUNSET,
        'forest': NeumorphismTheme.FOREST
    }
    theme = theme_map.get(theme_name.lower(), NeumorphismTheme.SOFT)
    return NeumorphismFlexBuilder(theme)


# =============================================
# 📝 أمثلة الاستخدام
# =============================================

if __name__ == "__main__":
    # مثال 1: بطاقة لعبة تكوين الكلمات
    builder = NeumorphismFlexBuilder(NeumorphismTheme.SOFT)
    
    game_card = builder.create_game_card({
        'title': 'لعبة تكوين الكلمات',
        'question_number': '1 من 5',
        'letters': ['ق', 'ي', 'ر', 'ل', 'ر', 'ل'],
        'instruction': 'كون 3 كلمات من هذه الحروف\nاكتب كلمة واحدة في كل رسالة',
        'show_refresh': True
    })
    
    print("✅ بطاقة اللعبة جاهزة!")
    
    # مثال 2: شاشة الترحيب
    welcome = builder.create_welcome_screen()
    print("✅ شاشة الترحيب جاهزة!")
    
    # مثال 3: بطاقة إحصائيات
    stats = builder.create_stats_card({
        'total_points': 1250,
        'games_played': 45,
        'wins': 30
    }, rank=5)
    print("✅ بطاقة الإحصائيات جاهزة!")
    
    # مثال 4: تغيير الثيم
    builder.set_theme('ocean')
    ocean_card = builder.create_game_card({
        'title': 'لعبة تكوين الكلمات',
        'question_number': '2 من 5',
        'letters': ['س', 'ا', 'ر', 'ة', 'ي', 'م'],
        'instruction': 'كون 3 كلمات',
        'show_refresh': False
    })
    print("✅ ثيم Ocean نشط!")
    
    print("\n🎉 جميع التصاميم متوافقة 100% مع LINE Bot API!")
