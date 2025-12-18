from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
from config import Config

class UI:
    @staticmethod
    def get_quick_reply():
        items = ["سؤال", "منشن", "تحدي", "اعتراف", "شخصية", "حكمة", "موقف", "بداية", "العاب", "مساعدة"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=cmd, text=cmd)) for cmd in items])
    
    @staticmethod
    def main_menu(user, db):
        c = Config.get_theme(user.get('theme', 'light'))
        can_reward = db.can_claim_reward(user['user_id'])
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Bot Mesh",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": c["border"]
                    },
                    {
                        "type": "text",
                        "text": f"مرحبا {user['name']}",
                        "size": "lg",
                        "color": c["text"],
                        "margin": "lg",
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"النقاط: {user['points']}",
                                        "size": "sm",
                                        "color": c["text"]
                                    },
                                    {
                                        "type": "text",
                                        "text": f"الالعاب: {user['games']}",
                                        "size": "sm",
                                        "color": c["text_secondary"],
                                        "align": "end"
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": f"الفوز: {user['wins']}",
                                        "size": "sm",
                                        "color": c["text"]
                                    },
                                    {
                                        "type": "text",
                                        "text": f"السلسلة: {user['streak']}",
                                        "size": "sm",
                                        "color": c["text_secondary"],
                                        "align": "end"
                                    }
                                ],
                                "margin": "sm"
                            }
                        ],
                        "margin": "lg",
                        "paddingAll": "15px",
                        "backgroundColor": c["card"],
                        "cornerRadius": "10px"
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": c["border"]
                    },
                    {
                        "type": "text",
                        "text": "تم الانشاء بواسطة عبير الدوسري @ 2025",
                        "size": "xxs",
                        "color": c["text_tertiary"],
                        "align": "center",
                        "margin": "lg"
                    }
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "24px"
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
                                "action": {"type": "message", "label": "العاب", "text": "العاب"},
                                "style": "primary",
                                "color": c["primary"],
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"},
                                "style": "secondary",
                                "height": "sm"
                            }
                        ],
                        "spacing": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "الصدارة", "text": "الصدارة"},
                                "style": "secondary",
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "انجازات", "text": "انجازات"},
                                "style": "secondary",
                                "height": "sm"
                            }
                        ],
                        "spacing": "sm",
                        "margin": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "مكافأة" if can_reward else "غير متاح", "text": "مكافأة"},
                                "style": "primary" if can_reward else "secondary",
                                "color": c["primary"] if can_reward else None,
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "تغيير", "text": "تغيير"},
                                "style": "secondary",
                                "height": "sm"
                            }
                        ],
                        "spacing": "sm",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        
        return FlexMessage(
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
    
    @staticmethod
    def games_list(theme="light"):
        c = Config.get_theme(theme)
        games = [
            ["خمن", "خمن"],
            ["ذكاء", "ذكاء"],
            ["ترتيب", "ترتيب"],
            ["رياضيات", "رياضيات"],
            ["اسرع", "اسرع"],
            ["ضد", "ضد"],
            ["لعبه", "لعبة"],
            ["سلسله", "سلسلة"],
            ["اغنيه", "اغنية"],
            ["تكوين", "تكوين"],
            ["لون", "لون"],
            ["حرف", "حرف"],
            ["مافيا", "مافيا"],
            ["توافق", "توافق"]
        ]
        
        contents = [
            {
                "type": "text",
                "text": "الالعاب",
                "size": "xxl",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            }
        ]
        
        for i in range(0, len(games), 2):
            row = []
            for j in range(2):
                if i + j < len(games):
                    cmd, label = games[i + j]
                    row.append({
                        "type": "button",
                        "action": {"type": "message", "label": label, "text": cmd},
                        "style": "secondary",
                        "height": "sm",
                        "flex": 1
                    })
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": row,
                "spacing": "sm",
                "margin": "md"
            })
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text="قائمة الالعاب",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
    
    @staticmethod
    def leaderboard(leaders, theme="light"):
        c = Config.get_theme(theme)
        contents = [
            {
                "type": "text",
                "text": "لوحة الصدارة",
                "size": "xxl",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            }
        ]
        
        for idx, leader in enumerate(leaders[:10]):
            rank = idx + 1
            bg_color = c["card_secondary"] if idx < 3 else c["card"]
            
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{rank}",
                        "size": "lg" if idx < 3 else "md",
                        "weight": "bold" if idx < 3 else "regular",
                        "color": c["text"],
                        "flex": 0,
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": leader['name'],
                        "size": "md",
                        "color": c["text"],
                        "flex": 1,
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": str(leader['points']),
                        "size": "sm",
                        "color": c["text_secondary"],
                        "align": "end",
                        "flex": 0
                    }
                ],
                "margin": "md",
                "paddingAll": "12px",
                "backgroundColor": bg_color,
                "cornerRadius": "8px"
            })
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text="لوحة الصدارة",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
    
    @staticmethod
    def achievements_list(user_achievements, theme="light"):
        c = Config.get_theme(theme)
        
        # تقسيم الإنجازات إلى مجموعات
        achievements_groups = [
            ("الالعاب", ["first_game", "ten_games", "fifty_games", "hundred_games"]),
            ("الانتصارات", ["first_win", "ten_wins"]),
            ("التقدم", ["hundred_points", "streak_3", "streak_5", "all_games"])
        ]
        
        contents = [
            {
                "type": "text",
                "text": "الانجازات",
                "size": "xxl",
                "weight": "bold",
                "color": c["text"],
                "align": "center"
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": c["border"]
            }
        ]
        
        for group_name, achievement_ids in achievements_groups:
            contents.append({
                "type": "text",
                "text": group_name,
                "size": "md",
                "weight": "bold",
                "color": c["text"],
                "margin": "lg"
            })
            
            group_contents = []
            for achievement_id in achievement_ids:
                achievement = Config.ACHIEVEMENTS[achievement_id]
                unlocked = achievement_id in user_achievements
                
                group_contents.append({
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": achievement['name'],
                                    "size": "sm",
                                    "weight": "bold",
                                    "color": c["text"]
                                },
                                {
                                    "type": "text",
                                    "text": achievement['desc'],
                                    "size": "xs",
                                    "color": c["text_secondary"],
                                    "wrap": True
                                }
                            ],
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": f"+{achievement['points']}" if unlocked else "مقفل",
                            "size": "xs",
                            "color": c["text"] if unlocked else c["text_tertiary"],
                            "flex": 0,
                            "align": "center"
                        }
                    ],
                    "paddingAll": "10px",
                    "backgroundColor": c["card_secondary"] if unlocked else c["card"],
                    "cornerRadius": "8px",
                    "margin": "sm"
                })
            
            contents.extend(group_contents)
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text="الانجازات",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
    
    @staticmethod
    def achievement_unlocked(achievement, theme="light"):
        c = Config.get_theme(theme)
        
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "انجاز جديد",
                        "size": "xl",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center"
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": c["border"]
                    },
                    {
                        "type": "text",
                        "text": achievement['name'],
                        "size": "lg",
                        "weight": "bold",
                        "color": c["primary"],
                        "margin": "lg",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": achievement['desc'],
                        "size": "md",
                        "color": c["text_secondary"],
                        "wrap": True,
                        "margin": "md",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"+{achievement['points']} نقطة",
                        "size": "sm",
                        "color": c["text_tertiary"],
                        "margin": "lg",
                        "align": "center"
                    }
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text="انجاز جديد",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
    
    @staticmethod
    def help_screen():
        c = Config.get_theme("light")
        
        bubble = {
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
                        "color": c["text"],
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
                                "text": "بداية - القائمة الرئيسية\nالعاب - قائمة الالعاب\nنقاطي - احصائياتك\nالصدارة - المتصدرين\nانجازات - انجازاتك\nمكافأة - مكافأة يومية\nتغيير - تغيير الاسم\nايقاف - ايقاف اللعبة",
                                "size": "sm",
                                "color": c["text_secondary"],
                                "wrap": True,
                                "margin": "sm"
                            }
                        ],
                        "margin": "lg",
                        "paddingAll": "12px",
                        "backgroundColor": c["card"],
                        "cornerRadius": "8px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الاوامر الترفيهية",
                                "size": "md",
                                "weight": "bold",
                                "color": c["text"]
                            },
                            {
                                "type": "text",
                                "text": "سؤال - سؤال عشوائي\nمنشن - منشن عشوائي\nتحدي - تحدي عشوائي\nاعتراف - اعتراف عشوائي\nشخصية - سؤال شخصي\nحكمة - حكمة عشوائية\nموقف - موقف افتراضي",
                                "size": "sm",
                                "color": c["text_secondary"],
                                "wrap": True,
                                "margin": "sm"
                            }
                        ],
                        "margin": "md",
                        "paddingAll": "12px",
                        "backgroundColor": c["card"],
                        "cornerRadius": "8px"
                    }
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "24px"
            }
        }
        
        return FlexMessage(
            alt_text="مساعدة",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
