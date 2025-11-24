# -*- coding: utf-8 -*-
from linebot.v3.messaging import FlexMessage
from constants import FIXED_BUTTONS, THEMES, BOT_RIGHTS

class UIBuilder:
    """بناء جميع واجهات Flex Messages"""
    
    @staticmethod
    def build_home(theme="💜"):
        """نافذة البداية مع أوامر البوت واختيار الثيم"""
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{theme} مرحبًا بك في Bot Mesh",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1DB446"
                    },
                    {
                        "type": "text",
                        "text": "استخدم الأزرار أدناه للتنقل",
                        "size": "sm",
                        "color": "#666666",
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "اختر ثيمك المفضل:",
                        "size": "sm",
                        "margin": "md",
                        "weight": "bold"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": t,
                                    "text": f"ثيم {t}"
                                },
                                "style": "secondary",
                                "height": "sm"
                            } for t in THEMES[:5]
                        ],
                        "margin": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": t,
                                    "text": f"ثيم {t}"
                                },
                                "style": "secondary",
                                "height": "sm"
                            } for t in THEMES[5:]
                        ],
                        "margin": "xs"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": btn,
                                    "text": btn
                                },
                                "style": "primary" if btn == "Games" else "secondary"
                            } for btn in FIXED_BUTTONS
                        ]
                    },
                    {
                        "type": "text",
                        "text": BOT_RIGHTS,
                        "size": "xxs",
                        "color": "#999999",
                        "align": "center",
                        "margin": "sm"
                    }
                ]
            }
        }
        return FlexMessage(alt_text="Home", contents=contents)

    @staticmethod
    def build_help(theme="💜"):
        """نافذة المساعدة مع قائمة الألعاب والأزرار الوظيفية"""
        games_list = [
            "IQ", "رياضيات", "لون الكلمة", "كلمة مبعثرة",
            "كتابة سريعة", "عكس", "حروف وكلمات", "أغنية",
            "إنسان حيوان نبات", "سلسلة كلمات", "تخمين", "توافق"
        ]
        
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{theme} قائمة الألعاب",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1DB446"
                    },
                    {
                        "type": "text",
                        "text": "اختر لعبتك المفضلة (5 جولات)",
                        "size": "sm",
                        "color": "#666666",
                        "margin": "sm"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": game,
                                    "text": f"لعبة {game}"
                                },
                                "style": "secondary",
                                "margin": "xs"
                            } for game in games_list[:6]
                        ],
                        "margin": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": game,
                                    "text": f"لعبة {game}"
                                },
                                "style": "secondary",
                                "margin": "xs"
                            } for game in games_list[6:]
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "انضم",
                                    "text": "انضم"
                                },
                                "style": "primary",
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "انسحب",
                                    "text": "انسحب"
                                },
                                "style": "secondary",
                                "height": "sm"
                            }
                        ],
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "نقاطي",
                                    "text": "نقاطي"
                                },
                                "style": "secondary",
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "صدارة",
                                    "text": "صدارة"
                                },
                                "style": "secondary",
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "إيقاف",
                                    "text": "إيقاف"
                                },
                                "style": "secondary",
                                "height": "sm"
                            }
                        ],
                        "margin": "xs"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": btn,
                                    "text": btn
                                },
                                "style": "primary" if btn == "Home" else "secondary"
                            } for btn in FIXED_BUTTONS
                        ]
                    },
                    {
                        "type": "text",
                        "text": BOT_RIGHTS,
                        "size": "xxs",
                        "color": "#999999",
                        "align": "center",
                        "margin": "sm"
                    }
                ]
            }
        }
        return FlexMessage(alt_text="Help", contents=contents)

    @staticmethod
    def build_my_points(username, points, theme="💜"):
        """نافذة عرض نقاط المستخدم"""
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{theme} نقاطي",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#1DB446"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"الاسم: {username}",
                                "size": "md",
                                "margin": "md"
                            },
                            {
                                "type": "text",
                                "text": f"النقاط: {points}",
                                "size": "md",
                                "weight": "bold",
                                "color": "#1DB446",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": "⚠️ سيتم حذف بياناتك بعد أسبوع",
                                "size": "xs",
                                "color": "#FF5551",
                                "margin": "md"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": btn,
                                    "text": btn
                                },
                                "style": "secondary"
                            } for btn in FIXED_BUTTONS
                        ]
                    },
                    {
                        "type": "text",
                        "text": BOT_RIGHTS,
                        "size": "xxs",
                        "color": "#999999",
                        "align": "center",
                        "margin": "sm"
                    }
                ]
            }
        }
        return FlexMessage(alt_text="My Points", contents=contents)
