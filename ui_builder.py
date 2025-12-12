from typing import Dict, List, Optional
from linebot.v3.messaging import (
    FlexMessage, FlexContainer, TextMessage, 
    QuickReply, QuickReplyItem, MessageAction
)
from config import Config


class UIBuilder:
    def __init__(self):
        self.config = Config

    # ========== Quick Reply الثابت ==========
    def _get_quick_reply(self) -> QuickReply:
        """أزرار ثابتة أسفل الشاشة"""
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="بداية", text="بداية")),
            QuickReplyItem(action=MessageAction(label="الألعاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="منشن", text="منشن")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="موقف", text="موقف")),
            QuickReplyItem(action=MessageAction(label="اقتباس", text="اقتباس")),
            QuickReplyItem(action=MessageAction(label="توافق", text="توافق"))
        ])

    # ========== بناء Flex أو نص ==========
    def _create_flex(self, alt_text: str, flex_dict: dict) -> FlexMessage:
        """إنشاء FlexMessage مع QuickReply"""
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_dict),
            quick_reply=self._get_quick_reply()
        )

    def _create_text(self, text: str) -> TextMessage:
        """إنشاء TextMessage مع QuickReply"""
        return TextMessage(text=text, quick_reply=self._get_quick_reply())

    # ========== ألوان الثيم ==========
    def _get_colors(self, theme: str = None) -> Dict[str, str]:
        """الحصول على ألوان الثيم"""
        return self.config.get_theme(theme)

    # ========== بناء أزرار الألعاب ==========
    def _build_game_buttons(self, games: List[str], colors: Dict[str,str], primary=True) -> List[dict]:
        """ترتيب الألعاب في صفوف 3 أزرار"""
        rows = []
        for i in range(0, len(games), 3):
            row = {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "xs" if i > 0 else "md",
                "contents": []
            }
            for g in games[i:i+3]:
                row["contents"].append({
                    "type": "button",
                    "style": "primary" if primary else "secondary",
                    "height": "sm",
                    "color": colors["primary"] if primary else None,
                    "action": {"type": "message", "label": g, "text": g}
                })
            rows.append(row)
        return rows

    # ========== شاشة البداية ==========
    def home_screen(self, username: str, points: int, is_registered: bool, theme: str) -> FlexMessage:
        """الشاشة الرئيسية"""
        c = self._get_colors(theme)
        status = "مسجل" if is_registered else "زائر"
        status_color = c["success"] if is_registered else c["text3"]
        other_theme = "داكن" if theme == "فاتح" else "فاتح"

        return self._create_flex("الرئيسية", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "24px",
                "backgroundColor": c["bg"],
                "contents": [
                    # العنوان
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
                    {"type": "separator", "margin": "md", "color": c["border"]},

                    # بطاقة المستخدم
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "margin": "md",
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
                            {"type": "separator", "margin": "sm", "color": c["border"]},
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "margin": "sm",
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
                                        "size": "xl",
                                        "weight": "bold",
                                        "color": c["primary"],
                                        "flex": 0,
                                        "align": "end"
                                    }
                                ]
                            }
                        ]
                    },

                    # أزرار التحكم
                    {
                        "type": "button",
                        "style": "secondary",
                        "height": "sm",
                        "margin": "md",
                        "action": {
                            "type": "message",
                            "label": f"ثيم {other_theme}",
                            "text": f"ثيم {other_theme}"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "sm",
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
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "height": "sm",
                                "color": c["primary"],
                                "action": {"type": "message", "label": "الألعاب", "text": "العاب"}
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "مساعدة", "text": "مساعدة"}
                            }
                        ]
                    },

                    # الحقوق
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {
                        "type": "text",
                        "text": self.config.RIGHTS,
                        "size": "xxs",
                        "color": c["text3"],
                        "align": "center",
                        "wrap": True,
                        "margin": "sm"
                    }
                ]
            }
        })

    # ========== قائمة الألعاب ==========
    def games_menu(self, theme: str) -> FlexMessage:
        """قائمة الألعاب الموحّدة"""
        c = self._get_colors(theme)
        point_buttons = self._build_game_buttons(list(self.config.POINT_GAMES), c, primary=True)
        fun_buttons = self._build_game_buttons(list(self.config.FUN_GAMES), c, primary=False)

        return self._create_flex("الألعاب", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "20px",
                "backgroundColor": c["bg"],
                "contents": [
                    {
                        "type": "text",
                        "text": "الألعاب المتاحة",
                        "size": "xl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "md", "color": c["border"]},

                    # ألعاب النقاط
                    {
                        "type": "text",
                        "text": "ألعاب النقاط",
                        "size": "md",
                        "weight": "bold",
                        "color": c["text"],
                        "margin": "md"
                    },
                    *point_buttons,

                    {"type": "separator", "margin": "md", "color": c["border"]},

                    # ألعاب ترفيهية
                    {
                        "type": "text",
                        "text": "ألعاب ترفيهية",
                        "size": "md",
                        "weight": "bold",
                        "color": c["text"],
                        "margin": "md"
                    },
                    *fun_buttons,

                    {"type": "separator", "margin": "md", "color": c["border"]},

                    # أزرار التحكم
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "button",
                                "style": "primary",
                                "height": "sm",
                                "color": c["success"],
                                "action": {"type": "message", "label": "تسجيل", "text": "انضم"}
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "انسحب", "text": "انسحب"}
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "ايقاف", "text": "ايقاف"}
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
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"}
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "صدارة", "text": "صدارة"}
                            },
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {"type": "message", "label": "بداية", "text": "بداية"}
                            }
                        ]
                    }
                ]
            }
        })

    # ========== شاشة المساعدة ==========
    def help_screen(self, theme: str) -> FlexMessage:
        """شاشة المساعدة المختصرة"""
        c = self._get_colors(theme)

        commands = [
            ("الأوامر الأساسية", "• بداية - الصفحة الرئيسية\n• العاب - قائمة الألعاب\n• نقاطي - إحصائياتي\n• صدارة - لوحة الصدارة\n• مساعدة - هذه الصفحة"),
            ("أوامر الحساب", "• انضم - التسجيل للنقاط\n• انسحب - إلغاء التسجيل"),
            ("أوامر اللعبة", "• لمح - تلميح للإجابة\n• جاوب - إظهار الإجابة\n• ايقاف - إيقاف اللعبة"),
            ("الثيمات", "• ثيم فاتح - الثيم الفاتح\n• ثيم داكن - الثيم الداكن")
        ]

        content = []
        for title, text in commands:
            content.append({
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "paddingAll": "14px",
                "margin": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "size": "md",
                        "weight": "bold",
                        "color": c["text"]
                    },
                    {
                        "type": "text",
                        "text": text,
                        "size": "sm",
                        "color": c["text2"],
                        "wrap": True,
                        "margin": "sm"
                    }
                ]
            })

        content.append({
            "type": "button",
            "style": "primary",
            "height": "sm",
            "color": c["primary"],
            "margin": "md",
            "action": {"type": "message", "label": "رجوع للبداية", "text": "بداية"}
        })

        return self._create_flex("المساعدة", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "20px",
                "backgroundColor": c["bg"],
                "contents": [
                    {
                        "type": "text",
                        "text": "دليل الاستخدام",
                        "size": "xl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    *content
                ]
            }
        })

    # ========== نقاطي ==========
    def my_points(self, username: str, points: int, stats: Optional[Dict], theme: str) -> FlexMessage:
        """شاشة الإحصائيات"""
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
                "text": "لا توجد إحصائيات",
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
                "paddingAll": "20px",
                "backgroundColor": c["bg"],
                "contents": [
                    {
                        "type": "text",
                        "text": "إحصائياتي",
                        "size": "xl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    
                    # بطاقة النقاط
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "margin": "md",
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
                                "text": "إجمالي النقاط",
                                "size": "sm",
                                "color": c["text2"],
                                "align": "center",
                                "margin": "sm"
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

                    # الألعاب الأكثر لعباً
                    {
                        "type": "box",
                        "layout": "vertical",
                        "backgroundColor": c["card"],
                        "cornerRadius": "16px",
                        "paddingAll": "16px",
                        "margin": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الألعاب الأكثر لعباً",
                                "size": "md",
                                "weight": "bold",
                                "color": c["text"],
                                "align": "center"
                            },
                            {"type": "separator", "margin": "sm", "color": c["border"]},
                            *rows
                        ]
                    }
                ]
            }
        })

    # ========== الصدارة ==========
    def leaderboard(self, top_users: List[tuple], theme: str) -> FlexMessage:
        """لوحة الصدارة"""
        c = self._get_colors(theme)
        
        rows = []
        for i, (name, pts, reg) in enumerate(top_users[:20], start=1):
            rank_color = c["primary"] if i <= 3 else c["text2"]
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "paddingAll": "10px",
                "margin": "xs",
                "backgroundColor": c["card"],
                "cornerRadius": "10px",
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
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": str(pts),
                        "size": "sm",
                        "weight": "bold",
                        "color": c["primary"],
                        "flex": 1,
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
                "paddingAll": "20px",
                "backgroundColor": c["bg"],
                "contents": [
                    {
                        "type": "text",
                        "text": "لوحة الصدارة",
                        "size": "xl",
                        "weight": "bold",
                        "color": c["primary"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "contents": rows
                    }
                ]
            }
        })

    # ========== رسائل التسجيل ==========
    def registration_prompt(self, theme: str) -> TextMessage:
        """طلب التسجيل"""
        return self._create_text("أرسل اسمك للتسجيل في نظام النقاط")

    def registration_success(self, username: str, points: int, theme: str) -> TextMessage:
        """نجاح التسجيل"""
        return self._create_text(f"تم التسجيل بنجاح\n\nالاسم: {username}\nالنقاط: {points}")

    def unregister_confirm(self, username: str, points: int, theme: str) -> TextMessage:
        """تأكيد الانسحاب"""
        return self._create_text(f"تم الانسحاب من النظام\n\nالاسم: {username}\nالنقاط المحفوظة: {points}")

    def game_stopped(self, game_name: str, theme: str) -> TextMessage:
        """تأكيد إيقاف اللعبة"""
        return self._create_text(f"تم إيقاف لعبة {game_name}")
