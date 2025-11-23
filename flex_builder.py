"""
Bot Mesh - Flex Builder
Created by: Abeer Aldosari © 2025
"""
from config import THEMES

class FlexBuilder:
    def __init__(self, theme='white'):
        self.theme = THEMES.get(theme, THEMES['white'])

    def welcome(self, user_name="لاعب"):
        """رسالة الترحيب"""
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🎮 Bot Mesh",
                        "weight": "bold",
                        "size": "xl",
                        "color": self.theme['text'],
                        "align": "center"
                    }
                ],
                "backgroundColor": self.theme['primary'],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"مرحباً {user_name}! 👋",
                        "weight": "bold",
                        "size": "lg",
                        "color": self.theme['text'],
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": self.theme['border']
                    },
                    {
                        "type": "text",
                        "text": "اختر لعبة من القائمة السريعة أدناه",
                        "size": "sm",
                        "color": self.theme['text2'],
                        "wrap": True,
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "📝 للتسجيل: انضم",
                                "size": "xs",
                                "color": self.theme['text2']
                            },
                            {
                                "type": "text",
                                "text": "🚪 للانسحاب: انسحب",
                                "size": "xs",
                                "color": self.theme['text2']
                            },
                            {
                                "type": "text",
                                "text": "⛔ لإيقاف اللعبة: إيقاف",
                                "size": "xs",
                                "color": self.theme['text2']
                            }
                        ],
                        "spacing": "sm",
                        "margin": "lg"
                    }
                ],
                "backgroundColor": self.theme['card'],
                "paddingAll": "20px"
            },
            "styles": {
                "header": {
                    "backgroundColor": self.theme['primary']
                },
                "body": {
                    "backgroundColor": self.theme['card']
                }
            }
        }

    def game_start(self, game_name, question, round_num=1, total_rounds=5):
        """بداية اللعبة"""
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"🎯 {game_name}",
                        "weight": "bold",
                        "size": "lg",
                        "color": self.theme['text'],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"الجولة {round_num} من {total_rounds}",
                        "size": "sm",
                        "color": self.theme['text'],
                        "align": "center",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": self.theme['primary'],
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": question,
                        "weight": "bold",
                        "size": "xl",
                        "color": self.theme['text'],
                        "wrap": True,
                        "align": "center"
                    }
                ],
                "backgroundColor": self.theme['card'],
                "paddingAll": "30px"
            },
            "styles": {
                "header": {
                    "backgroundColor": self.theme['primary']
                },
                "body": {
                    "backgroundColor": self.theme['card']
                }
            }
        }

    def game_result(self, winner_name, answer, points, is_final=False):
        """نتيجة اللعبة"""
        title = "🏆 اللعبة انتهت!" if is_final else "✅ إجابة صحيحة!"
        
        return {
            "type": "bubble",
            "size": "mega",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": title,
                        "weight": "bold",
                        "size": "lg",
                        "color": self.theme['text'],
                        "align": "center"
                    }
                ],
                "backgroundColor": self.theme['primary'],
                "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"الفائز: {winner_name}",
                        "weight": "bold",
                        "size": "lg",
                        "color": self.theme['text'],
                        "wrap": True
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": self.theme['border']
                    },
                    {
                        "type": "text",
                        "text": f"الإجابة: {answer}",
                        "size": "md",
                        "color": self.theme['text2'],
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": f"النقاط: +{points}",
                        "weight": "bold",
                        "size": "md",
                        "color": self.theme['accent'],
                        "margin": "md"
                    }
                ],
                "backgroundColor": self.theme['card'],
                "paddingAll": "20px"
            },
            "styles": {
                "header": {
                    "backgroundColor": self.theme['primary']
                },
                "body": {
                    "backgroundColor": self.theme['card']
                }
            }
        }

    def leaderboard(self, players, title="🏆 المتصدرون"):
        """لوحة المتصدرين"""
        contents = [
            {
                "type": "text",
                "text": title,
                "weight": "bold",
                "size": "lg",
                "color": self.theme['text'],
                "align": "center"
            },
            {
                "type": "separator",
                "margin": "md",
                "color": self.theme['border']
            }
        ]
        
        for idx, player in enumerate(players[:10], 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{medal} {player['name']}",
                        "size": "sm",
                        "color": self.theme['text'],
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": f"{player['points']} نقطة",
                        "size": "sm",
                        "color": self.theme['text2'],
                        "align": "end",
                        "flex": 1
                    }
                ],
                "margin": "md"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": self.theme['card'],
                "paddingAll": "20px"
            },
            "styles": {
                "body": {
                    "backgroundColor": self.theme['card']
                }
            }
        }

    def error_message(self, message):
        """رسالة خطأ"""
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "❌ خطأ",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#FF0000"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": message,
                        "size": "sm",
                        "color": self.theme['text2'],
                        "wrap": True,
                        "margin": "md"
                    }
                ],
                "backgroundColor": self.theme['card'],
                "paddingAll": "20px"
            }
        }
