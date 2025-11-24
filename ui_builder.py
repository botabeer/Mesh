# -*- coding: utf-8 -*-
"""
Bot Mesh - UI Builder (Redesigned)
Created by: Abeer Aldosari © 2025
"""

from linebot.v3.messaging import FlexMessage
from config import BOT_RIGHTS, GAMES_LIST
from theme_styles import THEMES

class UIBuilder:
    """بناء جميع واجهات Flex Messages"""
    
    @staticmethod
    def build_home(theme="💜", username="مستخدم", points=0, is_registered=False):
        """نافذة البداية - التصميم الجديد"""
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
                            {"type": "text", "text": f"▪️ مرحباً: {username}", "size": "sm", "color": "#666666"},
                            {"type": "text", "text": f"▪️ الحالة: {status}", "size": "sm", "color": "#666666"},
                            {"type": "text", "text": f"▪️ نقاطك: {points}", "size": "sm", "color": "#666666"},
                            {"type": "text", "text": "▪️ اختر ثيمك:", "size": "sm", "weight": "bold", "color": "#333333"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": t, "text": f"ثيم {t}"},
                             "style": "primary" if t == theme else "secondary", "height": "sm"}
                            for t in list(THEMES.keys())[:3]
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": t, "text": f"ثيم {t}"},
                             "style": "primary" if t == theme else "secondary", "height": "sm"}
                            for t in list(THEMES.keys())[3:6]
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": t, "text": f"ثيم {t}"},
                             "style": "primary" if t == theme else "secondary", "height": "sm"}
                            for t in list(THEMES.keys())[6:]
                        ]
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": "🕹️ الأزرار الثابتة:",
                        "size": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": label, "text": label},
                             "style": "secondary", "height": "sm"}
                            for label in ["انضم", "انسحب"]
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": label, "text": label},
                             "style": "secondary", "height": "sm"}
                            for label in ["نقاطي", "صدارة"]
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {"type": "text", "text": "📝 ملاحظة: يمكنك استخدام البوت في الخاص أو القروبات",
                     "size": "xxs", "color": "#999999", "align": "center", "wrap": True},
                    {"type": "separator"},
                    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": "#999999", "align": "center"}
                ]
            }
        }
        return FlexMessage(alt_text="Home", contents=contents)

    @staticmethod
    def build_games_menu(theme="💜"):
        """قائمة الألعاب - مع شريط سفلي"""
        theme_color = THEMES.get(theme, THEMES["💜"])["color"]
        
        # أسماء الألعاب المختصرة للأزرار
        game_buttons = {
            "IQ": "ذكاء", "رياضيات": "رياضيات", "لون الكلمة": "لون",
            "كلمة مبعثرة": "ترتيب", "كتابة سريعة": "أسرع", "عكس": "ضد",
            "حروف وكلمات": "تكوين", "أغنية": "أغنية", "إنسان حيوان نبات": "لعبة",
            "سلسلة كلمات": "سلسلة", "تخمين": "خمن", "توافق": "توافق"
        }
        
        games = list(GAMES_LIST.keys())
        
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {"type": "text", "text": f"{theme} الألعاب المتاحة", "weight": "bold",
                     "size": "xl", "color": theme_color},
                    {"type": "separator"},
                    # الصف الأول
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {"type": "button",
                             "action": {"type": "message", "label": game_buttons.get(game, game[:4]),
                                       "text": f"لعبة {game}"},
                             "style": "secondary", "height": "sm"}
                            for game in games[:4]
                        ]
                    },
                    # الصف الثاني
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {"type": "button",
                             "action": {"type": "message", "label": game_buttons.get(game, game[:4]),
                                       "text": f"لعبة {game}"},
                             "style": "secondary", "height": "sm"}
                            for game in games[4:8]
                        ]
                    },
                    # الصف الثالث
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {"type": "button",
                             "action": {"type": "message", "label": game_buttons.get(game, game[:4]),
                                       "text": f"لعبة {game}"},
                             "style": "secondary", "height": "sm"}
                            for game in games[8:]
                        ]
                    },
                    {"type": "separator"},
                    # زر الإيقاف
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "⏹️ إيقاف", "text": "إيقاف"},
                             "style": "primary", "color": "#FF5555", "height": "sm"}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {"type": "text", "text": "📝 ملاحظة: يمكنك استخدام البوت في الخاص أو القروبات",
                     "size": "xxs", "color": "#999999", "align": "center", "wrap": True},
                    {"type": "separator"},
                    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": "#999999", "align": "center"}
                ]
            }
        }
        return FlexMessage(alt_text="Games", contents=contents)

    @staticmethod
    def build_info(theme="💜"):
        """نافذة المساعدة - التصميم الجديد"""
        theme_color = THEMES.get(theme, THEMES["💜"])["color"]
        
        contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {"type": "text", "text": f"{theme} Bot Mesh – مساعدة", "weight": "bold",
                     "size": "xl", "color": theme_color},
                    {"type": "separator"},
                    {"type": "text", "text": "🎮 الألعاب المتاحة:", "weight": "bold", "size": "md"},
                    {"type": "text", "text": "ذكاء – رياضيات – لون – أسرع – ترتيب – أغنية",
                     "size": "sm", "color": "#666666", "wrap": True},
                    {"type": "text", "text": "كلمة – سلسلة – خمن – توافق",
                     "size": "sm", "color": "#666666", "wrap": True},
                    {"type": "separator"},
                    {"type": "text", "text": "📝 الأوامر أثناء اللعب (كنص):", "weight": "bold", "size": "md"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {"type": "text", "text": "▫️ لمح → تلميح أول حرف وعدد حروف الكلمة",
                             "size": "sm", "color": "#666666", "wrap": True},
                            {"type": "text", "text": "▫️ جاوب → كشف الإجابة الصحيحة",
                             "size": "sm", "color": "#666666"},
                            {"type": "text", "text": "▫️ إيقاف → لإيقاف اللعبة",
                             "size": "sm", "color": "#666666"}
                        ]
                    },
                    {"type": "separator"},
                    {"type": "text", "text": "🕹️ استخدم قائمة الألعاب لاختيار لعبتك المفضلة!",
                     "size": "sm", "color": theme_color, "align": "center", "wrap": True}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {"type": "text", "text": "📝 ملاحظة: يمكنك استخدام البوت في الخاص أو القروبات",
                     "size": "xxs", "color": "#999999", "align": "center", "wrap": True},
                    {"type": "separator"},
                    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": "#999999", "align": "center"}
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
                    {"type": "text", "text": f"{theme} نقاطي", "weight": "bold",
                     "size": "xl", "color": theme_color},
                    {"type": "separator"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "md",
                        "contents": [
                            {"type": "text", "text": f"👤 الاسم: {username}", "size": "md"},
                            {"type": "text", "text": f"⭐ النقاط: {points}", "size": "lg",
                             "weight": "bold", "color": theme_color},
                            {"type": "separator"},
                            {"type": "text", "text": "⚠️ تحذير: سيتم حذف بياناتك بعد 7 أيام من عدم النشاط",
                             "size": "xs", "color": "#FF5551", "wrap": True}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": "#999999", "align": "center"}
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
                    {"type": "text", "text": f"{theme} لوحة الصدارة", "weight": "bold",
                     "size": "xl", "color": theme_color},
                    {"type": "separator"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": leaderboard_contents if leaderboard_contents else [
                            {"type": "text", "text": "لا يوجد لاعبين مسجلين بعد",
                             "size": "sm", "color": "#999999", "align": "center"}
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": "#999999", "align": "center"}
                ]
            }
        }
        return FlexMessage(alt_text="Leaderboard", contents=contents)
