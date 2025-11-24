# -*- coding: utf-8 -*-
"""
Bot Mesh - UI Builder (LINE Compatible)
Created by: Abeer Aldosari © 2025

⚠️ IMPORTANT: LINE doesn't support 'margin' in Flex Messages!
Use 'spacing' in box layout instead
"""

from linebot.v3.messaging import FlexMessage
from config import BOT_RIGHTS, GAMES_LIST
from theme_styles import THEMES, FIXED_BUTTONS

class UIBuilder:
    """بناء جميع واجهات Flex Messages متوافقة مع LINE"""
    
    @staticmethod
    def build_home(theme="💜", username="مستخدم", points=0, is_registered=False):
        """نافذة البداية"""
        theme_color = THEMES.get(theme, THEMES["💜"])["color"]
        status = "✅ مسجل" if is_registered else "⚠️ غير مسجل"
        
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{theme} Bot Mesh",
                        "weight": "bold",
                        "size": "xl",
                        "color": theme_color
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"▪️ مرحباً: {username}",
                                "size": "sm",
                                "color": "#666666"
                            },
                            {
                                "type": "text",
                                "text": f"▪️ الحالة: {status}",
                                "size": "sm",
                                "color": "#666666"
                            },
                            {
                                "type": "text",
                                "text": f"▪️ نقاطك: {points}",
                                "size": "sm",
                                "color": "#666666"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": "اختر ثيمك:",
                        "size": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": t,
                                    "text": f"ثيم {t}"
                                },
                                "style": "primary" if t == theme else "secondary",
                                "height": "sm"
                            } for t in list(THEMES.keys())[:3]
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": t,
                                    "text": f"ثيم {t}"
                                },
                                "style": "primary" if t == theme else "secondary",
                                "height": "sm"
                            } for t in list(THEMES.keys())[3:6]
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": t,
                                    "text": f"ثيم {t}"
                                },
                                "style": "primary" if t == theme else "secondary",
                                "height": "sm"
                            } for t in list(THEMES.keys())[6:]
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": btn,
                                    "text": btn
                                },
                                "style": "primary" if btn == "Home" else "secondary",
                                "height": "sm"
                            } for btn in FIXED_BUTTONS
                        ]
                    },
                    {
                        "type": "text",
                        "text": BOT_RIGHTS,
                        "size": "xxs",
                        "color": "#999999",
                        "align": "center"
                    }
                ]
            }
        }
        return FlexMessage(alt_text="Home", contents=contents)

    @staticmethod
    def build_games_menu(theme="💜"):
        """نافذة قائمة الألعاب"""
        theme_color = THEMES.get(theme, THEMES["💜"])["color"]
        games = list(GAMES_LIST.keys())
        
        # تقسيم الألعاب إلى مجموعات
        games_group1 = games[:4]
        games_group2 = games[4:8]
        games_group3 = games[8:]
        
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{theme} قائمة الألعاب",
                        "weight": "bold",
                        "size": "xl",
                        "color": theme_color
                    },
                    {
                        "type": "text",
                        "text": "اختر لعبتك المفضلة (5 جولات)",
                        "size": "sm",
                        "color": "#666666"
                    },
                    {
                        "type": "separator"
                    },
                    # المجموعة الأولى
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": f"{GAMES_LIST[game]['emoji']} {game}",
                                    "text": f"لعبة {game}"
                                },
                                "style": "secondary",
                                "height": "sm"
                            } for game in games_group1
                        ]
                    },
                    # المجموعة الثانية
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": f"{GAMES_LIST[game]['emoji']} {game}",
                                    "text": f"لعبة {game}"
                                },
                                "style": "secondary",
                                "height": "sm"
                            } for game in games_group2
                        ]
                    },
                    # المجموعة الثالثة
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": f"{GAMES_LIST[game]['emoji']} {game}",
                                    "text": f"لعبة {game}"
                                },
                                "style": "secondary",
                                "height": "sm"
                            } for game in games_group3
                        ]
                    },
                    {
                        "type": "separator"
                    },
                    # أزرار الإجراءات
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
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
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": label,
                                    "text": label
                                },
                                "style": "secondary",
                                "height": "sm"
                            } for label in ["نقاطي", "صدارة", "إيقاف"]
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": btn,
                                    "text": btn
                                },
                                "style": "primary" if btn == "Games" else "secondary",
                                "height": "sm"
                            } for btn in FIXED_BUTTONS
                        ]
                    },
                    {
                        "type": "text",
                        "text": BOT_RIGHTS,
                        "size": "xxs",
                        "color": "#999999",
                        "align": "center"
                    }
                ]
            }
        }
        return FlexMessage(alt_text="Games", contents=contents)

    @staticmethod
    def build_info(theme="💜"):
        """نافذة المعلومات والمساعدة"""
        theme_color = THEMES.get(theme, THEMES["💜"])["color"]
        
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{theme} المساعدة",
                        "weight": "bold",
                        "size": "xl",
                        "color": theme_color
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": "🎮 الأوامر المتاحة:",
                        "weight": "bold",
                        "size": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "▪️ لمح → تلميح (أول حرف)",
                                "size": "sm",
                                "color": "#666666"
                            },
                            {
                                "type": "text",
                                "text": "▪️ جاوب → كشف الإجابة",
                                "size": "sm",
                                "color": "#666666"
                            },
                            {
                                "type": "text",
                                "text": "▪️ إيقاف → إنهاء اللعبة",
                                "size": "sm",
                                "color": "#666666"
                            }
                        ]
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": "📝 ملاحظات:",
                        "weight": "bold",
                        "size": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "text",
                                "text": "• يعمل في الخاص والمجموعات",
                                "size": "sm",
                                "color": "#666666",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": "• كل لعبة = 5 جولات",
                                "size": "sm",
                                "color": "#666666"
                            },
                            {
                                "type": "text",
                                "text": "• حذف تلقائي بعد 7 أيام",
                                "size": "sm",
                                "color": "#FF5551"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": btn,
                                    "text": btn
                                },
                                "style": "primary" if btn == "Info" else "secondary",
                                "height": "sm"
                            } for btn in FIXED_BUTTONS
                        ]
                    },
                    {
                        "type": "text",
                        "text": BOT_RIGHTS,
                        "size": "xxs",
                        "color": "#999999",
                        "align": "center"
                    }
                ]
            }
        }
        return FlexMessage(alt_text="Info", contents=contents)

    @staticmethod
    def build_my_points(username, points, theme="💜"):
        """نافذة نقاط المستخدم"""
        theme_color = THEMES.get(theme, THEMES["💜"])["color"]
        
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{theme} نقاطي",
                        "weight": "bold",
                        "size": "xl",
                        "color": theme_color
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"👤 الاسم: {username}",
                                "size": "md"
                            },
                            {
                                "type": "text",
                                "text": f"⭐ النقاط: {points}",
                                "size": "lg",
                                "weight": "bold",
                                "color": theme_color
                            },
                            {
                                "type": "separator"
                            },
                            {
                                "type": "text",
                                "text": "⚠️ تحذير: سيتم حذف بياناتك بعد 7 أيام من عدم النشاط",
                                "size": "xs",
                                "color": "#FF5551",
                                "wrap": True
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": btn,
                                    "text": btn
                                },
                                "style": "secondary",
                                "height": "sm"
                            } for btn in FIXED_BUTTONS
                        ]
                    },
                    {
                        "type": "text",
                        "text": BOT_RIGHTS,
                        "size": "xxs",
                        "color": "#999999",
                        "align": "center"
                    }
                ]
            }
        }
        return FlexMessage(alt_text="My Points", contents=contents)

    @staticmethod
    def build_leaderboard(top_users, theme="💜"):
        """نافذة لوحة الصدارة"""
        theme_color = THEMES.get(theme, THEMES["💜"])["color"]
        
        leaderboard_contents = []
        medals = ["🥇", "🥈", "🥉"]
        
        for i, (name, points) in enumerate(top_users[:10], 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            leaderboard_contents.append({
                "type": "text",
                "text": f"{medal} {name}: {points} نقطة",
                "size": "sm",
                "color": "#666666"
            })
        
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{theme} لوحة الصدارة",
                        "weight": "bold",
                        "size": "xl",
                        "color": theme_color
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": leaderboard_contents if leaderboard_contents else [
                            {
                                "type": "text",
                                "text": "لا يوجد لاعبين مسجلين بعد",
                                "size": "sm",
                                "color": "#999999",
                                "align": "center"
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": btn,
                                    "text": btn
                                },
                                "style": "secondary",
                                "height": "sm"
                            } for btn in FIXED_BUTTONS
                        ]
                    },
                    {
                        "type": "text",
                        "text": BOT_RIGHTS,
                        "size": "xxs",
                        "color": "#999999",
                        "align": "center"
                    }
                ]
            }
        }
        return FlexMessage(alt_text="Leaderboard", contents=contents)
