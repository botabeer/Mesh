"""
Bot Mesh - Flex Message Builder (Enhanced UI with Themes & Animations)
Created by: Abeer Aldosari © 2025
"""
from typing import Dict, List, Any, Optional
from config import ThemeColors, THEMES, Theme, Config
from database import User


class FlexBuilder:
    """منشئ رسائل Flex المحسن مع دعم الثيمات"""
    
    def __init__(self, theme: ThemeColors = None):
        self.theme = theme or THEMES[Theme.LIGHT]
    
    def set_theme(self, theme_name: str):
        """تغيير الثيم"""
        try:
            self.theme = THEMES[Theme(theme_name)]
        except (ValueError, KeyError):
            self.theme = THEMES[Theme.LIGHT]
    
    def _create_button(self, text: str, action_text: str, 
                       color: str = None, style: str = "primary") -> Dict:
        """إنشاء زر Neumorphic"""
        return {
            "type": "button",
            "action": {"type": "message", "label": text, "text": action_text},
            "style": style,
            "color": color or self.theme.button_primary,
            "height": "md",
            "margin": "md"
        }
    
    def _create_header(self, title: str, subtitle: str = None) -> Dict:
        """إنشاء رأس الرسالة"""
        contents = [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "size": "xxl",
                "color": self.theme.text_primary,
                "align": "center"
            }
        ]
        
        if subtitle:
            contents.append({
                "type": "text",
                "text": subtitle,
                "size": "sm",
                "color": self.theme.text_secondary,
                "align": "center",
                "margin": "sm"
            })
        
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "20px",
            "backgroundColor": self.theme.background
        }
    
    def _create_stat_box(self, emoji: str, value: str, label: str) -> Dict:
        """إنشاء صندوق إحصائية"""
        return {
            "type": "box",
            "layout": "vertical",
            "flex": 1,
            "contents": [
                {"type": "text", "text": emoji, "size": "xxl", "align": "center"},
                {
                    "type": "text", 
                    "text": str(value), 
                    "size": "xl", 
                    "weight": "bold",
                    "align": "center", 
                    "color": self.theme.text_primary
                },
                {
                    "type": "text", 
                    "text": label, 
                    "size": "xs", 
                    "align": "center", 
                    "color": self.theme.text_secondary
                }
            ],
            "backgroundColor": self.theme.surface,
            "cornerRadius": "15px",
            "paddingAll": "15px"
        }
    
    def create_main_menu(self, is_dark: bool = False) -> Dict:
        """إنشاء القائمة الرئيسية"""
        return {
            "type": "bubble",
            "size": "mega",
            "header": self._create_header("Bot Mesh 🎮", "ألعاب تفاعلية ممتعة"),
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    self._create_button("🔑 انضم للعب", "انضم", self.theme.accent),
                    self._create_button("🎮 ابدأ اللعب", "ابدأ", self.theme.button_primary),
                    self._create_button("📊 نقاطي", "نقاطي", self.theme.button_secondary),
                    self._create_button("🏆 الصدارة", "الصدارة", self.theme.button_secondary),
                    self._create_button("🎨 تغيير الثيم", "ثيم", self.theme.button_secondary),
                    self._create_button("❓ المساعدة", "مساعدة", self.theme.button_secondary)
                ],
                "paddingAll": "20px",
                "backgroundColor": self.theme.background,
                "spacing": "none"
            }
        }
    
    def create_games_carousel(self, games: Dict[str, Dict]) -> Dict:
        """إنشاء قائمة الألعاب"""
        if not games:
            return self._create_error_bubble("⚠️ لا توجد ألعاب متاحة")
        
        bubbles = []
        for arabic_name, data in games.items():
            bubble = {
                "type": "bubble",
                "size": "micro",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": data['emoji'],
                                    "size": "4xl",
                                    "align": "center"
                                }
                            ],
                            "paddingAll": "20px",
                            "backgroundColor": self.theme.surface,
                            "cornerRadius": "20px"
                        },
                        {
                            "type": "text",
                            "text": data['name'],
                            "weight": "bold",
                            "size": "sm",
                            "align": "center",
                            "color": self.theme.text_primary,
                            "margin": "md",
                            "wrap": True
                        },
                        self._create_button("▶️ العب", arabic_name, data.get('color', self.theme.accent))
                    ],
                    "paddingAll": "15px",
                    "backgroundColor": self.theme.background
                }
            }
            bubbles.append(bubble)
        
        return {"type": "carousel", "contents": bubbles}
    
    def create_stats_card(self, user: User, rank: int = 0) -> Dict:
        """إنشاء بطاقة الإحصائيات"""
        if not user:
            return {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "📊 إحصائياتك", "weight": "bold",
                         "size": "xl", "color": self.theme.text_primary, "align": "center"},
                        {"type": "separator", "margin": "lg", "color": self.theme.text_secondary},
                        {"type": "text", "text": "لم تلعب بعد!", "align": "center",
                         "color": self.theme.text_secondary, "margin": "xl"},
                        self._create_button("🎮 ابدأ اللعب", "ابدأ", self.theme.accent)
                    ],
                    "paddingAll": "25px",
                    "backgroundColor": self.theme.background
                }
            }
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": self._create_header(user.level, f"#{rank}" if rank else ""),
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": user.display_name,
                        "weight": "bold",
                        "size": "lg",
                        "align": "center",
                        "color": self.theme.text_primary
                    },
                    {"type": "separator", "margin": "lg", "color": self.theme.text_secondary},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "lg",
                        "spacing": "md",
                        "contents": [
                            self._create_stat_box("💰", str(user.total_points), "نقطة"),
                            self._create_stat_box("🎮", str(user.games_played), "لعبة")
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "spacing": "md",
                        "contents": [
                            self._create_stat_box("🏆", str(user.wins), "فوز"),
                            self._create_stat_box("📈", f"{user.win_rate:.0f}%", "نسبة فوز")
                        ]
                    },
                    self._create_button("🎮 ابدأ لعبة", "ابدأ", self.theme.accent)
                ],
                "paddingAll": "20px",
                "backgroundColor": self.theme.background
            }
        }
    
    def create_leaderboard(self, leaders: List[User]) -> Dict:
        """إنشاء لوحة الصدارة"""
        if not leaders:
            return self._create_error_bubble("لا توجد بيانات")
        
        # الثلاثة الأوائل
        top3 = []
        medals = ["🥇", "🥈", "🥉"]
        
        for i, user in enumerate(leaders[:3]):
            top3.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": medals[i], "size": "3xl", "flex": 0},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "flex": 5,
                        "contents": [
                            {
                                "type": "text",
                                "text": user.display_name,
                                "weight": "bold",
                                "size": "md",
                                "color": self.theme.text_primary,
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": f"⭐ {user.total_points} | 🎮 {user.games_played} | 🏆 {user.wins}",
                                "size": "xs",
                                "color": self.theme.text_secondary
                            }
                        ]
                    }
                ],
                "backgroundColor": self.theme.surface,
                "cornerRadius": "15px",
                "paddingAll": "15px",
                "margin": "md" if i > 0 else "none"
            })
        
        # الباقي
        others = []
        for i, user in enumerate(leaders[3:], 4):
            others.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{i}",
                        "size": "md",
                        "weight": "bold",
                        "color": self.theme.text_secondary,
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": user.display_name,
                        "size": "sm",
                        "color": self.theme.text_primary,
                        "flex": 3,
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": f"{user.total_points}⭐",
                        "size": "sm",
                        "color": self.theme.accent,
                        "flex": 2,
                        "align": "end",
                        "weight": "bold"
                    }
                ],
                "paddingAll": "12px",
                "margin": "sm"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": self._create_header("🏆 لوحة الصدارة"),
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": top3 + others,
                "paddingAll": "20px",
                "backgroundColor": self.theme.background
            }
        }
    
    def create_theme_selector(self) -> Dict:
        """إنشاء قائمة اختيار الثيم"""
        themes_data = [
            ("🌞", "فاتح", "ثيم:light", THEMES[Theme.LIGHT].accent),
            ("🌙", "داكن", "ثيم:dark", THEMES[Theme.DARK].accent),
            ("💜", "بنفسجي", "ثيم:purple", THEMES[Theme.PURPLE].accent),
            ("🌊", "محيط", "ثيم:ocean", THEMES[Theme.OCEAN].accent),
            ("🌅", "غروب", "ثيم:sunset", THEMES[Theme.SUNSET].accent)
        ]
        
        buttons = []
        for emoji, name, action, color in themes_data:
            buttons.append({
                "type": "button",
                "action": {"type": "message", "label": f"{emoji} {name}", "text": action},
                "style": "primary",
                "color": color,
                "height": "sm",
                "margin": "sm"
            })
        
        return {
            "type": "bubble",
            "size": "kilo",
            "header": self._create_header("🎨 اختر الثيم"),
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": buttons,
                "paddingAll": "20px",
                "backgroundColor": self.theme.background
            }
        }
    
    def create_help(self) -> Dict:
        """إنشاء رسالة المساعدة"""
        return {
            "type": "bubble",
            "size": "mega",
            "header": self._create_header("❓ كيف ألعب؟"),
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "خطوات سريعة:",
                        "weight": "bold",
                        "size": "lg",
                        "color": self.theme.text_primary
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "md",
                        "contents": [
                            {"type": "text", "text": "1️⃣ اكتب 'انضم' للتسجيل",
                             "size": "sm", "color": self.theme.text_secondary},
                            {"type": "text", "text": "2️⃣ اكتب 'ابدأ' لعرض الألعاب",
                             "size": "sm", "color": self.theme.text_secondary},
                            {"type": "text", "text": "3️⃣ اختر لعبة واستمتع!",
                             "size": "sm", "color": self.theme.text_secondary}
                        ]
                    },
                    {"type": "separator", "margin": "xl", "color": self.theme.text_secondary},
                    {
                        "type": "text",
                        "text": "أوامر مفيدة:",
                        "weight": "bold",
                        "size": "md",
                        "color": self.theme.text_primary,
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": "• نقاطي - عرض إحصائياتك\n• الصدارة - أفضل اللاعبين\n• ثيم - تغيير المظهر\n• إيقاف - إيقاف اللعبة",
                        "size": "sm",
                        "color": self.theme.text_secondary,
                        "margin": "md",
                        "wrap": True
                    },
                    self._create_button("🎮 ابدأ الآن", "ابدأ", self.theme.accent)
                ],
                "paddingAll": "25px",
                "backgroundColor": self.theme.background
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "تم إنشاء هذا البوت بواسطة\nعبير الدوسري © 2025",
                        "size": "xxs",
                        "color": self.theme.text_secondary,
                        "align": "center",
                        "wrap": True
                    }
                ],
                "paddingAll": "15px",
                "backgroundColor": self.theme.background
            }
        }
    
    def _create_error_bubble(self, message: str) -> Dict:
        """إنشاء رسالة خطأ"""
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": message,
                        "align": "center",
                        "color": self.theme.error
                    }
                ],
                "paddingAll": "30px",
                "backgroundColor": self.theme.background
            }
        }
    
    def create_game_result(self, title: str, message: str, 
                          points: int = 0, is_winner: bool = False) -> Dict:
        """إنشاء نتيجة اللعبة"""
        emoji = "🎉" if is_winner else "🏁"
        
        return {
            "type": "bubble",
            "size": "kilo",
            "header": self._create_header(f"{emoji} {title}"),
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": message,
                        "wrap": True,
                        "color": self.theme.text_primary,
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"+{points} نقطة" if points > 0 else "",
                        "size": "xl",
                        "weight": "bold",
                        "color": self.theme.success if points > 0 else self.theme.text_secondary,
                        "align": "center",
                        "margin": "lg"
                    },
                    self._create_button("🎮 لعبة جديدة", "ابدأ", self.theme.accent)
                ],
                "paddingAll": "20px",
                "backgroundColor": self.theme.background
            }
        }


# Singleton instance
flex_builder = FlexBuilder()
