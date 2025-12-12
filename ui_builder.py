from typing import Dict, List, Optional
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from config import Config


class UIBuilder:
    """بناء واجهات Flex Messages بتصميم iOS"""

    def __init__(self):
        self.config = Config

    def _create_flex(self, alt_text: str, flex_dict: dict) -> FlexMessage:
        """إنشاء رسالة Flex"""
        return FlexMessage(alt_text=alt_text, contents=FlexContainer.from_dict(flex_dict))

    def _create_text(self, text: str) -> TextMessage:
        """إنشاء رسالة نصية"""
        return TextMessage(text=text)

    def _get_colors(self, theme: str = None) -> Dict[str, str]:
        """الحصول على ألوان الثيم"""
        return self.config.get_theme(theme)

    def home_screen(self, username: str, points: int, is_registered: bool, 
                    theme: str, mode: str = "فردي") -> FlexMessage:
        """شاشة البداية"""
        c = self._get_colors(theme)
        status = "مسجل" if is_registered else "زائر"
        status_color = c["success"] if is_registered else c["text3"]

        return self._create_flex("الرئيسية", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "24px",
                "backgroundColor": c["bg"],
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
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "20px",
                        "margin": "lg",
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
                                "text": status,
                                "size": "sm",
                                "color": status_color,
                                "align": "center",
                                "margin": "sm"
                            },
                            {"type": "separator", "margin": "md", "color": c["border"]},
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "md",
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
                                ]
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "md",
                        "margin": "xl",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "height": "sm",
                                "color": c["primary"],
                                "action": {"type": "message", "label": "انضم", "text": "انضم"}
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "العاب", "text": "العاب"}
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "md",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"}
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "صدارة", "text": "صدارة"}
                            }
                        ]
                    }
                ]
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
                "paddingAll": "24px",
                "backgroundColor": c["bg"],
                "contents": [
                    {
                        "type": "text",
                        "text": "دليل الاستخدام",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "20px",
                        "margin": "lg",
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
                                "text": "بداية - العاب - نقاطي - صدارة",
                                "size": "sm",
                                "color": c["text2"],
                                "wrap": True,
                                "margin": "sm"
                            },
                            {"type": "separator", "margin": "md", "color": c["border"]},
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
                                "margin": "sm"
                            },
                            {"type": "separator", "margin": "md", "color": c["border"]},
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
                                "margin": "sm"
                            },
                            {"type": "separator", "margin": "md", "color": c["border"]},
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
                            }
                        ]
                    }
                ]
            }
        })

    def my_points(self, username: str, points: int, stats: Optional[Dict], theme: str) -> FlexMessage:
        """شاشة النقاط"""
        c = self._get_colors(theme)
        
        rows = []
        if stats:
            for game, data in list(stats.items())[:5]:
                rows.append({
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": game,
                            "size": "sm",
                            "color": c["text"],
                            "flex": 2
                        },
                        {
                            "type": "text",
                            "text": f"{data['plays']} مرة",
                            "size": "xs",
                            "color": c["text3"],
                            "flex": 1,
                            "align": "end"
                        }
                    ]
                })
        else:
            rows.append({
                "type": "text",
                "text": "لا توجد إحصائيات\nابدأ باللعب الآن",
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
                "paddingAll": "24px",
                "backgroundColor": c["bg"],
                "contents": [
                    {
                        "type": "text",
                        "text": "احصائياتي",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "20px",
                        "margin": "lg",
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
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "20px",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الالعاب الاكثر لعبا",
                                "size": "md",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            },
                            {"type": "separator", "margin": "md", "color": c["border"]},
                            *rows
                        ]
                    }
                ]
            }
        })

    def leaderboard(self, top_users: List[tuple], theme: str) -> FlexMessage:
        """لوحة الصدارة"""
        c = self._get_colors(theme)
        rows = []
        
        for i, (name, pts, reg) in enumerate(top_users[:20], start=1):
            rank_color = c["primary"] if i <= 3 else c["text2"]
            badge = "R" if reg else "G"
            badge_color = c["success"] if reg else c["text3"]
            
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "paddingAll": "12px",
                "margin": "xs",
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
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
                        "type": "text",
                        "text": name[:20],
                        "size": "sm",
                        "color": c["text"],
                        "flex": 3,
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": str(pts),
                        "size": "sm",
                        "weight": "bold",
                        "color": c["primary"],
                        "flex": 1,
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": badge,
                        "size": "xs",
                        "color": badge_color,
                        "flex": 0,
                        "align": "end"
                    }
                ]
            })
        
        return self._create_flex("الصدارة", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "24px",
                "backgroundColor": c["bg"],
                "contents": [
                    {
                        "type": "text",
                        "text": "لوحة الصدارة",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "box", "layout": "vertical", "margin": "lg", "contents": rows}
                ]
            }
        })

    def registration_prompt(self, theme: str) -> TextMessage:
        """رسالة طلب التسجيل"""
        return self._create_text("ارسل اسمك للتسجيل\nالاسم يجب ان يكون من 1-100 حرف")

    def registration_success(self, username: str, points: int, theme: str) -> TextMessage:
        """رسالة نجاح التسجيل"""
        return self._create_text(f"تم التسجيل بنجاح\n\nالاسم: {username}\nالنقاط: {points}")

    def unregister_confirm(self, username: str, points: int, theme: str) -> TextMessage:
        """رسالة تأكيد الانسحاب"""
        return self._create_text(f"تم الانسحاب\n\nالاسم: {username}\nالنقاط: {points}")

    def game_stopped(self, game_name: str, theme: str) -> TextMessage:
        """رسالة إيقاف اللعبة"""
        return self._create_text(f"تم ايقاف لعبة {game_name}")

    def games_menu(self, theme: str, top_games: List[str] = None) -> FlexMessage:
        """قائمة الألعاب"""
        c = self._get_colors(theme)
        all_games = self.config.get_all_games()
        
        if top_games:
            order = top_games + [g for g in all_games if g not in top_games]
        else:
            order = all_games
        
        order = order[:12]
        
        rows = []
        for i in range(0, len(order), 3):
            row = {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm" if i > 0 else "lg",
                "contents": []
            }
            for g in order[i:i+3]:
                row["contents"].append({
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "color": c["primary"],
                    "action": {"type": "message", "label": g, "text": g}
                })
            rows.append(row)
        
        return self._create_flex("الالعاب", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "24px",
                "backgroundColor": c["bg"],
                "contents": [
                    {
                        "type": "text",
                        "text": "الالعاب المتاحة",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    *rows,
                    {"type": "separator", "margin": "xl", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "12px",
                        "paddingAll": "16px",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "لمح - جاوب - ايقاف",
                                "size": "sm",
                                "color": c["text2"],
                                "align": "center"
                            }
                        ]
                    }
                ]
            }
        })
