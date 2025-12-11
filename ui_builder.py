from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from config import Config

class UIBuilder:
    """بناء واجهات المستخدم"""
    
    def _flex(self, alt_text: str, body: dict):
        """إنشاء رسالة Flex"""
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(body)
        )
    
    def _colors(self, theme: str = None):
        """الحصول على ألوان الثيم"""
        return Config.get_theme(theme)
    
    def home_screen(self, username: str, points: int, is_registered: bool, theme: str, mode: str):
        """الشاشة الرئيسية"""
        c = self._colors(theme)
        status = "مسجل" if is_registered else "غير مسجل"
        status_color = c["success"] if is_registered else c["text3"]
        
        body = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": Config.BOT_NAME,
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": username[:30],
                                "size": "lg",
                                "weight": "bold",
                                "color": c["text"]
                            },
                            {
                                "type": "text",
                                "text": status,
                                "size": "sm",
                                "color": status_color,
                                "margin": "xs"
                            },
                            {"type": "separator", "margin": "md", "color": c["border"]},
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
                                        "flex": 0
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
                                "action": {"type": "message", "label": "الالعاب", "text": "ألعاب"},
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
                                "action": {"type": "message", "label": "الصدارة", "text": "صدارة"},
                                "style": "secondary",
                                "height": "sm"
                            }
                        ]
                    }
                ],
                "paddingAll": "20px",
                "backgroundColor": c["bg"]
            }
        }
        
        return self._flex("البداية", body)
    
    def games_menu(self, theme: str, top_games: list = None):
        """قائمة الالعاب"""
        c = self._colors(theme)
        
        default_order = [
            "أسرع", "ذكاء", "لعبة", "خمن", "أغنيه", "سلسلة",
            "ترتيب", "تكوين", "ضد", "لون", "رياضيات", "توافق", "مافيا"
        ]
        
        if top_games:
            order = top_games + [g for g in default_order if g not in top_games]
        else:
            order = default_order
        
        order = order[:13]
        
        game_buttons = []
        for i in range(0, len(order), 3):
            row = {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm",
                "contents": []
            }
            
            for j in range(3):
                if i + j < len(order):
                    row["contents"].append({
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": order[i + j],
                            "text": order[i + j]
                        },
                        "style": "primary",
                        "height": "sm",
                        "color": c["primary"]
                    })
            
            game_buttons.append(row)
        
        body = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "الالعاب",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    *game_buttons,
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {
                        "type": "text",
                        "text": "لمح - جاوب - ايقاف",
                        "size": "xs",
                        "color": c["text2"],
                        "align": "center",
                        "margin": "sm"
                    }
                ],
                "paddingAll": "20px",
                "backgroundColor": c["bg"]
            }
        }
        
        return self._flex("الالعاب", body)
    
    def help_screen(self, theme: str):
        """شاشة المساعدة"""
        c = self._colors(theme)
        
        body = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "المساعدة",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الأوامر الأساسية",
                                "size": "md",
                                "weight": "bold",
                                "color": c["text"]
                            },
                            {
                                "type": "text",
                                "text": "بداية - الالعاب - نقاطي - صدارة",
                                "size": "sm",
                                "color": c["text2"],
                                "wrap": True,
                                "margin": "sm"
                            },
                            {"type": "separator", "margin": "md", "color": c["border"]},
                            {
                                "type": "text",
                                "text": "أوامر اللعب",
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
                            {"type": "separator", "margin": "md", "color": c["border"]},
                            {
                                "type": "text",
                                "text": "الثيمات",
                                "size": "md",
                                "weight": "bold",
                                "color": c["text"],
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": "ثيم [اسم الثيم]",
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
        }
        
        return self._flex("المساعدة", body)
    
    def my_points(self, username: str, points: int, stats: dict, theme: str):
        """شاشة النقاط"""
        c = self._colors(theme)
        
        body = {
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
                    {"type": "separator", "margin": "lg", "color": c["border"]},
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
                                "text": f"النقاط: {points}",
                                "size": "xxl",
                                "weight": "bold",
                                "color": c["primary"],
                                "align": "center",
                                "margin": "md"
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
        }
        
        return self._flex("نقاطي", body)
    
    def leaderboard(self, top_users: list, theme: str):
        """لوحة الصدارة"""
        c = self._colors(theme)
        
        rows = []
        medals = ["1", "2", "3"]
        
        for i, (name, pts, is_registered) in enumerate(top_users[:20], 1):
            status = "مسجل" if is_registered else "زائر"
            status_color = c["success"] if is_registered else c["text3"]
            
            rank_text = medals[i - 1] if i <= 3 else str(i)
            rank_color = c["primary"] if i <= 3 else c["text2"]
            
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": rank_text,
                        "size": "md",
                        "weight": "bold",
                        "color": rank_color,
                        "flex": 0
                    },
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {
                        "type": "text",
                        "text": name[:20],
                        "size": "sm",
                        "color": c["text"],
                        "flex": 3,
                        "margin": "md"
                    },
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {
                        "type": "text",
                        "text": str(pts),
                        "size": "sm",
                        "weight": "bold",
                        "color": c["primary"],
                        "flex": 1,
                        "align": "center"
                    },
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {
                        "type": "text",
                        "text": status,
                        "size": "xs",
                        "color": status_color,
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
        
        body = {
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
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "box", "layout": "vertical", "contents": rows, "margin": "md"}
                ],
                "paddingAll": "20px",
                "backgroundColor": c["bg"]
            }
        }
        
        return self._flex("الصدارة", body)
    
    def registration_prompt(self, theme: str):
        """طلب التسجيل"""
        return TextMessage(text="ارسل اسمك للتسجيل\nحد اقصى 100 حرف")
    
    def registration_success(self, username: str, points: int, theme: str):
        """نجاح التسجيل"""
        return TextMessage(text=f"تم التسجيل بنجاح\n\nالاسم: {username}\nالنقاط: {points}")
    
    def unregister_confirm(self, username: str, points: int, theme: str):
        """تأكيد الانسحاب"""
        return TextMessage(text=f"تم الانسحاب\n\nالاسم: {username}\nنقاطك: {points}")
    
    def game_stopped(self, game_name: str, theme: str):
        """إيقاف اللعبة"""
        return TextMessage(text=f"تم ايقاف {game_name}")
