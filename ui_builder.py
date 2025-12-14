from typing import List, Dict


class UIBuilder:
    def __init__(self, theme: str = "glass"):
        self.theme = theme

        self.themes = {
            "glass": {
                "bg": "#F5F5F7",
                "card": "#FFFFFFCC",
                "primary": "#000000",
                "secondary": "#3A3A3C",
                "button": "#E5E5EA",
                "button_active": "#D1D1D6",
                "text": "#000000",
                "text2": "#6E6E73",
                "text3": "#8E8E93",
                "border": "#D1D1D6",
                "success": "#34C759",
                "warning": "#FF9500"
            },
            "dark": {
                "bg": "#1C1C1E",
                "card": "#2C2C2ECC",
                "primary": "#FFFFFF",
                "secondary": "#EBEBF5",
                "button": "#3A3A3C",
                "button_active": "#48484A",
                "text": "#FFFFFF",
                "text2": "#AEAEB2",
                "text3": "#8E8E93",
                "border": "#3A3A3C",
                "success": "#30D158",
                "warning": "#FF9F0A"
            }
        }

    # =========================
    # Helpers
    # =========================
    def _colors(self) -> Dict[str, str]:
        return self.themes.get(self.theme, self.themes["glass"])

    def _section_title(self, text: str) -> Dict:
        return {
            "type": "text",
            "text": text,
            "weight": "bold",
            "size": "md",
            "margin": "md",
            "color": self._colors()["primary"]
        }

    def _two_buttons(self, text1: str, action1: str, text2: str, action2: str) -> Dict:
        c = self._colors()
        return {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {"type": "message", "label": text1, "text": action1},
                    "color": c["button"]
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {"type": "message", "label": text2, "text": action2},
                    "color": c["button"]
                }
            ]
        }

    def _theme_toggle_button(self) -> Dict:
        c = self._colors()
        label = "الوضع الداكن" if self.theme != "dark" else "الوضع الفاتح"
        return {
            "type": "button",
            "style": "secondary",
            "height": "sm",
            "action": {"type": "message", "label": label, "text": "تغيير_الثيم"},
            "color": c["button"],
            "margin": "sm"
        }

    # =========================
    # Cards
    # =========================
    def welcome_card(self, name: str, registered: bool):
        c = self._colors()
        status = f"{name} مسجل" if registered else f"{name} غير مسجل"
        status_color = c["success"] if registered else c["warning"]

        contents = [
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "cornerRadius": "16px",
                "paddingAll": "16px",
                "contents": [
                    {
                        "type": "text",
                        "text": "Bot Mesh",
                        "align": "center",
                        "weight": "bold",
                        "size": "xl",
                        "color": c["primary"]
                    }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "8px",
                "contents": [
                    {
                        "type": "text",
                        "text": "مرحبا",
                        "align": "center",
                        "weight": "bold",
                        "size": "lg",
                        "color": c["primary"]
                    },
                    {
                        "type": "text",
                        "text": status,
                        "align": "center",
                        "color": status_color,
                        "size": "sm"
                    }
                ]
            }
        ]

        if registered:
            contents.extend([
                self._section_title("الحساب"),
                self._two_buttons("تغيير الاسم", "تغيير", "نقاطي", "نقاطي"),
                self._section_title("الإعدادات"),
                self._theme_toggle_button(),
                self._section_title("الإحصائيات"),
                self._two_buttons("الصدارة", "الصدارة", "مساعدة", "مساعدة"),
                self._section_title("القوائم"),
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {"type": "message", "label": "الألعاب", "text": "العاب"},
                    "color": c["primary"],
                    "margin": "sm"
                }
            ])
        else:
            contents.extend([
                self._section_title("ابدأ الآن"),
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {"type": "message", "label": "تسجيل", "text": "تسجيل"},
                    "color": c["primary"],
                    "margin": "sm"
                }
            ])

        contents.append({
            "type": "text",
            "text": "تم إنشاء هذا البوت بواسطة\nعبير الدوسري 2025",
            "align": "center",
            "size": "xs",
            "color": c["text3"],
            "margin": "lg"
        })

        return {
            "type": "bubble",
            "styles": {"body": {"backgroundColor": c["bg"]}},
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": contents
            }
        }

    def games_menu_card(self):
        c = self._colors()
        games = [
            ["ذكاء", "خمن", "ضد"],
            ["ترتيب", "رياضيات", "اغنيه"],
            ["لون", "تكوين", "لعبة"],
            ["سلسلة", "اسرع", "توافق"],
            ["مافيا", "سؤال", "منشن"]
        ]
        
        buttons = []
        for row in games:
            row_buttons = {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm",
                "contents": []
            }
            for game in row:
                row_buttons["contents"].append({
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {"type": "message", "label": game, "text": game},
                    "color": c["button"]
                })
            buttons.append(row_buttons)
        
        return {
            "type": "bubble",
            "styles": {"body": {"backgroundColor": c["bg"]}},
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الالعاب",
                                "align": "center",
                                "weight": "bold",
                                "size": "xl",
                                "color": c["primary"]
                            }
                        ]
                    },
                    *buttons,
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {"type": "message", "label": "رجوع", "text": "بداية"},
                        "color": c["primary"],
                        "margin": "md"
                    }
                ]
            }
        }
    
    def leaderboard_card(self, leaders: List[tuple]):
        c = self._colors()
        items = []
        
        for i, (name, pts) in enumerate(leaders[:10]):
            rank = str(i + 1)
            items.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "backgroundColor": c["card"],
                "cornerRadius": "8px",
                "paddingAll": "8px",
                "contents": [
                    {"type": "text", "text": rank, "size": "sm", "color": c["text"], "flex": 0, "weight": "bold"},
                    {"type": "text", "text": name, "size": "sm", "color": c["text"], "flex": 3, "margin": "sm"},
                    {"type": "text", "text": str(pts), "size": "sm", "color": c["primary"], "weight": "bold", "flex": 1, "align": "end"}
                ]
            })
        
        return {
            "type": "bubble",
            "styles": {"body": {"backgroundColor": c["bg"]}},
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "contents": [
                            {
                                "type": "text",
                                "text": "لوحة الصدارة",
                                "align": "center",
                                "weight": "bold",
                                "size": "xl",
                                "color": c["primary"]
                            }
                        ]
                    },
                    {"type": "box", "layout": "vertical", "spacing": "sm", "contents": items},
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {"type": "message", "label": "رجوع", "text": "بداية"},
                        "color": c["primary"],
                        "margin": "md"
                    }
                ]
            }
        }
    
    def stats_card(self, name: str, user_data: dict):
        c = self._colors()
        points = user_data.get("total_points", 0)
        games = user_data.get("games_played", 0)
        wins = user_data.get("wins", 0)
        
        return {
            "type": "bubble",
            "styles": {"body": {"backgroundColor": c["bg"]}},
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "contents": [
                            {
                                "type": "text",
                                "text": "احصائياتي",
                                "align": "center",
                                "weight": "bold",
                                "size": "xl",
                                "color": c["primary"]
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "12px",
                        "paddingAll": "16px",
                        "spacing": "sm",
                        "contents": [
                            {"type": "text", "text": f"الاسم: {name}", "size": "md", "color": c["text"]},
                            {"type": "text", "text": f"النقاط: {points}", "size": "lg", "color": c["primary"], "weight": "bold"},
                            {"type": "text", "text": f"الالعاب: {games}", "size": "sm", "color": c["text2"]},
                            {"type": "text", "text": f"الفوز: {wins}", "size": "sm", "color": c["text2"]}
                        ]
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {"type": "message", "label": "رجوع", "text": "بداية"},
                        "color": c["primary"],
                        "margin": "md"
                    }
                ]
            }
        }
    
    def help_card(self):
        c = self._colors()
        
        return {
            "type": "bubble",
            "styles": {"body": {"backgroundColor": c["bg"]}},
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "contents": [
                            {
                                "type": "text",
                                "text": "المساعدة",
                                "align": "center",
                                "weight": "bold",
                                "size": "xl",
                                "color": c["primary"]
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "12px",
                        "paddingAll": "16px",
                        "spacing": "sm",
                        "contents": [
                            {"type": "text", "text": "الاوامر المتاحة:", "size": "md", "color": c["text"], "weight": "bold"},
                            {"type": "text", "text": "بداية - القائمة الرئيسية", "size": "sm", "color": c["text2"], "wrap": True},
                            {"type": "text", "text": "العاب - عرض الالعاب", "size": "sm", "color": c["text2"], "wrap": True},
                            {"type": "text", "text": "نقاطي - عرض النقاط", "size": "sm", "color": c["text2"], "wrap": True},
                            {"type": "text", "text": "الصدارة - المتصدرين", "size": "sm", "color": c["text2"], "wrap": True},
                            {"type": "text", "text": "تسجيل - انشاء حساب", "size": "sm", "color": c["text2"], "wrap": True}
                        ]
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {"type": "message", "label": "رجوع", "text": "بداية"},
                        "color": c["primary"],
                        "margin": "md"
                    }
                ]
            }
        }
