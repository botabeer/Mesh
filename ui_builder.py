"""
Bot Mesh UI Builder Module
نظام بناء الواجهات المحسّن
Created by: Abeer Aldosari - 2025
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from config import Config
from typing import Dict, List, Optional

class UIBuilder:
    """بناء واجهات Flex Messages الاحترافية"""
    
    def __init__(self):
        self.config = Config
    
    def _create_flex(self, alt_text: str, flex_dict: dict) -> FlexMessage:
        """إنشاء رسالة Flex"""
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_dict)
        )
    
    def _get_colors(self, theme: str = None) -> Dict[str, str]:
        """الحصول على ألوان الثيم"""
        return self.config.get_theme(theme)
    
    def _create_text_message(self, text: str) -> TextMessage:
        """إنشاء رسالة نصية بسيطة"""
        return TextMessage(text=text)
    
    def home_screen(self, username: str, points: int, is_registered: bool, 
                    theme: str, mode: str = "فردي") -> FlexMessage:
        """الشاشة الرئيسية"""
        c = self._get_colors(theme)
        
        status_text = "مسجل" if is_registered else "زائر"
        status_color = c["success"] if is_registered else c["text3"]
        
        return self._create_flex("الرئيسية", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": self.config.BOT_NAME,
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"v{self.config.VERSION}",
                        "size": "xs",
                        "color": c["text3"],
                        "align": "center",
                        "margin": "xs"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": c["border"]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": username[:30],
                                "size": "lg",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": status_text,
                                "size": "sm",
                                "color": status_color,
                                "align": "center",
                                "margin": "xs"
                            },
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": c["border"]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "النقاط",
                                        "size": "md",
                                        "color": c["text2"],
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": str(points),
                                        "size": "xxl",
                                        "weight": "bold",
                                        "color": c["primary"],
                                        "flex": 0,
                                        "align": "end"
                                    }
                                ],
                                "margin": "md"
                            }
                        ],
                        "backgroundColor": c["card"],
                        "cornerRadius": "12px",
                        "paddingAll": "16px",
                        "borderWidth": "1px",
                        "borderColor": c["border"],
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"الوضع: {mode}",
                        "size": "sm",
                        "color": c["text2"],
                        "align": "center",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "lg",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "انضم", "text": "انضم"},
                                "style": "primary",
                                "height": "sm",
                                "color": c["primary"]
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "العاب", "text": "العاب"},
                                "style": "secondary",
                                "height": "sm"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"},
                                "style": "secondary",
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "صدارة", "text": "صدارة"},
                                "style": "secondary",
                                "height": "sm"
                            }
                        ]
                    }
                ],
                "paddingAll": "20px",
                "backgroundColor": c["bg"]
            }
        })
    
    def games_menu(self, theme: str, top_games: List[str] = None) -> FlexMessage:
        """قائمة الألعاب"""
        c = self._get_colors(theme)
        
        all_games = self.config.get_all_games()
        
        if top_games:
            games_order = top_games + [g for g in all_games if g not in top_games]
        else:
            games_order = all_games
        
        games_order = games_order[:13]
        
        rows = []
        for i in range(0, len(games_order), 3):
            row = {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm",
                "contents": []
            }
            
            for j in range(3):
                if i + j < len(games_order):
                    game_name = games_order[i + j]
                    row["contents"].append({
                        "type": "button",
                        "action": {"type": "message", "label": game_name, "text": game_name},
                        "style": "primary",
                        "height": "sm",
                        "color": c["primary"]
                    })
            
            rows.append(row)
        
        return self._create_flex("الالعاب", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "الالعاب المتاحة",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": c["border"]
                    },
                    *rows,
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": c["border"]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "أوامر اللعبة",
                                "size": "sm",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": "لمح - جاوب - ايقاف",
                                "size": "xs",
                                "color": c["text2"],
                                "align": "center",
                                "margin": "xs"
                            }
                        ],
                        "margin": "md"
                    }
                ],
                "paddingAll": "20px",
                "backgroundColor": c["bg"]
            }
        })
    
    def help_screen(self, theme: str) -> FlexMessage:
        """شاشة المساعدة"""
        c = self._get_colors(theme)
        
        return self._create_flex("المساعدة", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "دليل الاستخدام",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": c["border"]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الاوامر الاساسية",
                                "size": "md",
                                "weight": "bold",
                                "color": c["text"]
                            },
                            {
                                "type": "text",
                                "text": "بداية - العاب - نقاطي - صدارة - مساعدة",
                                "size": "sm",
                                "color": c["text2"],
                                "wrap": True,
                                "margin": "sm"
                            },
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": c["border"]
                            },
                            {
                                "type": "text",
                                "text": "اوامر الحساب",
                                "size": "md",
                                "weight": "bold",
                                "color": c["text"],
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": "انضم - انسحب",
                                "size": "sm",
                                "color": c["text2"],
                                "wrap": True,
                                "margin": "sm"
                            },
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": c["border"]
                            },
                            {
                                "type": "text",
                                "text": "اوامر اللعبة",
                                "size": "md",
                                "weight": "bold",
                                "color": c["text"],
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": "لمح - جاوب - ايقاف",
                                "size": "sm",
                                "color": c["text2"],
                                "wrap": True,
                                "margin": "sm"
                            },
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": c["border"]
                            },
                            {
                                "type": "text",
                                "text": "تغيير الثيم",
                                "size": "md",
                                "weight": "bold",
                                "color": c["text"],
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": "ثيم [الاسم]\nمثال: ثيم اسود",
                                "size": "sm",
                                "color": c["text2"],
                                "wrap": True,
                                "margin": "sm"
                            },
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": c["border"]
                            },
                            {
                                "type": "text",
                                "text": "للمجموعات",
                                "size": "md",
                                "weight": "bold",
                                "color": c["text"],
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": "فريقين - فردي",
                                "size": "sm",
                                "color": c["text2"],
                                "wrap": True,
                                "margin": "sm"
                            }
                        ],
                        "backgroundColor": c["card"],
                        "cornerRadius": "12px",
                        "paddingAll": "16px",
                        "borderWidth": "1px",
                        "borderColor": c["border"],
                        "margin": "md"
                    }
                ],
                "paddingAll": "20px",
                "backgroundColor": c["bg"]
            }
        })
    
    def my_points(self, username: str, points: int, stats: Optional[Dict], theme: str) -> FlexMessage:
        """شاشة النقاط والإحصائيات"""
        c = self._get_colors(theme)
        
        stats_content = []
        
        if stats:
            for game_name, game_stats in list(stats.items())[:5]:
                stats_content.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": game_name,
                            "size": "sm",
                            "color": c["text"],
                            "flex": 2
                        },
                        {
                            "type": "text",
                            "text": f"{game_stats['plays']} مرة",
                            "size": "xs",
                            "color": c["text3"],
                            "flex": 1,
                            "align": "end"
                        }
                    ],
                    "margin": "sm"
                })
        
        if not stats_content:
            stats_content.append({
                "type": "text",
                "text": "لا توجد إحصائيات بعد\nابدأ باللعب الآن",
                "size": "sm",
                "color": c["text3"],
                "align": "center",
                "wrap": True
            })
        
        return self._create_flex("نقاطي", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "احصائياتي",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": c["border"]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": username[:30],
                                "size": "lg",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": "اجمالي النقاط",
                                "size": "sm",
                                "color": c["text2"],
                                "align": "center",
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": str(points),
                                "size": "xxl",
                                "weight": "bold",
                                "color": c["primary"],
                                "align": "center",
                                "margin": "xs"
                            }
                        ],
                        "backgroundColor": c["card"],
                        "cornerRadius": "12px",
                        "paddingAll": "16px",
                        "borderWidth": "1px",
                        "borderColor": c["border"],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الالعاب الاكثر لعباً",
                                "size": "md",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            },
                            {
                                "type": "separator",
                                "margin": "sm",
                                "color": c["border"]
                            },
                            *stats_content
                        ],
                        "backgroundColor": c["card"],
                        "cornerRadius": "12px",
                        "paddingAll": "16px",
                        "borderWidth": "1px",
                        "borderColor": c["border"],
                        "margin": "md"
                    }
                ],
                "paddingAll": "20px",
                "backgroundColor": c["bg"]
            }
        })
    
    def leaderboard(self, top_users: List[tuple], theme: str) -> FlexMessage:
        """لوحة الصدارة"""
        c = self._get_colors(theme)
        
        rows = []
        for i, (name, points, is_registered) in enumerate(top_users[:20], 1):
            rank_color = c["primary"] if i <= 3 else c["text2"]
            badge = "R" if is_registered else "G"
            badge_color = c["success"] if is_registered else c["text3"]
            
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": str(i),
                        "size": "md",
                        "weight": "bold",
                        "color": rank_color,
                        "flex": 0
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": c["border"]
                    },
                    {
                        "type": "text",
                        "text": name[:20],
                        "size": "sm",
                        "color": c["text"],
                        "flex": 3,
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": c["border"]
                    },
                    {
                        "type": "text",
                        "text": str(points),
                        "size": "sm",
                        "weight": "bold",
                        "color": c["primary"],
                        "flex": 1,
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": c["border"]
                    },
                    {
                        "type": "text",
                        "text": badge,
                        "size": "xs",
                        "color": badge_color,
                        "flex": 1,
                        "align": "center"
                    }
                ],
                "paddingAll": "10px",
                "backgroundColor": c["card"],
                "cornerRadius": "8px",
                "borderWidth": "1px",
                "borderColor": c["border"],
                "margin": "xs"
            })
        
        return self._create_flex("الصدارة", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "لوحة الصدارة",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": c["border"]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": rows,
                        "margin": "md"
                    }
                ],
                "paddingAll": "20px",
                "backgroundColor": c["bg"]
            }
        })
    
    def registration_prompt(self, theme: str) -> TextMessage:
        """طلب التسجيل"""
        return self._create_text_message("ارسل اسمك للتسجيل\nالاسم يجب ان يكون من 1-100 حرف")
    
    def registration_success(self, username: str, points: int, theme: str) -> TextMessage:
        """رسالة نجاح التسجيل"""
        return self._create_text_message(f"تم التسجيل بنجاح\n\nالاسم: {username}\nالنقاط: {points}")
    
    def unregister_confirm(self, username: str, points: int, theme: str) -> TextMessage:
        """تأكيد إلغاء التسجيل"""
        return self._create_text_message(f"تم الانسحاب\n\nالاسم: {username}\nالنقاط: {points}")
    
    def game_stopped(self, game_name: str, theme: str) -> TextMessage:
        """رسالة إيقاف اللعبة"""
        return self._create_text_message(f"تم ايقاف لعبة {game_name}")
