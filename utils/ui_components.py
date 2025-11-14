from linebot.models import QuickReply, QuickReplyButton, MessageAction
from utils.helpers import get_emoji_for_rank, format_number, get_win_rate

def get_quick_reply():
    """الأزرار الثابتة (13 زر)"""
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="🎯 ذكاء", text="ذكاء")),
        QuickReplyButton(action=MessageAction(label="🎨 لون", text="لون")),
        QuickReplyButton(action=MessageAction(label="🔗 سلسلة", text="سلسلة")),
        QuickReplyButton(action=MessageAction(label="⚡ أسرع", text="أسرع")),
        QuickReplyButton(action=MessageAction(label="🔄 ضد", text="ضد")),
        QuickReplyButton(action=MessageAction(label="📝 تكوين", text="تكوين")),
        QuickReplyButton(action=MessageAction(label="🎮 لعبة", text="لعبة")),
        QuickReplyButton(action=MessageAction(label="🎵 أغنية", text="أغنية")),
        QuickReplyButton(action=MessageAction(label="📊 نقاطي", text="نقاطي")),
        QuickReplyButton(action=MessageAction(label="🏆 الصدارة", text="الصدارة")),
        QuickReplyButton(action=MessageAction(label="✨ المزيد", text="المزيد")),
        QuickReplyButton(action=MessageAction(label="⏹️ إيقاف", text="إيقاف")),
        QuickReplyButton(action=MessageAction(label="❓ مساعدة", text="مساعدة"))
    ])

def get_more_quick_reply():
    """الأزرار الإضافية"""
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="🔀 ترتيب", text="ترتيب")),
        QuickReplyButton(action=MessageAction(label="🎲 خمن", text="خمن")),
        QuickReplyButton(action=MessageAction(label="💕 توافق", text="توافق")),
        QuickReplyButton(action=MessageAction(label="🔢 رياضيات", text="رياضيات")),
        QuickReplyButton(action=MessageAction(label="🧠 ذاكرة", text="ذاكرة")),
        QuickReplyButton(action=MessageAction(label="🎯 لغز", text="لغز")),
        QuickReplyButton(action=MessageAction(label="😊 إيموجي", text="إيموجي")),
        QuickReplyButton(action=MessageAction(label="🔙 رجوع", text="البداية"))
    ])

def get_welcome_message(display_name):
    """رسالة الترحيب الأنيقة"""
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "Bot Mesh",
                    "weight": "bold",
                    "size": "xxl",
                    "color": "#1a1a1a",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"مرحباً {display_name}",
                    "size": "md",
                    "color": "#6a6a6a",
                    "align": "center",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#e8e8e8"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "▪️ 15 لعبة تفاعلية",
                            "size": "sm",
                            "color": "#4a4a4a",
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": "▪️ نظام نقاط متطور",
                            "size": "sm",
                            "color": "#4a4a4a",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "▪️ لوحة صدارة",
                            "size": "sm",
                            "color": "#4a4a4a",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": "▪️ ذكاء اصطناعي",
                            "size": "sm",
                            "color": "#4a4a4a",
                            "margin": "md"
                        }
                    ],
                    "margin": "xl"
                },
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#e8e8e8"
                },
                {
                    "type": "text",
                    "text": "اختر لعبة من الأزرار أدناه",
                    "size": "sm",
                    "color": "#6a6a6a",
                    "align": "center",
                    "margin": "xl"
                }
            ],
            "backgroundColor": "#ffffff",
            "paddingAll": "24px"
        },
        "styles": {
            "body": {
                "separator": True
            }
        }
    }

def get_help_message():
    """رسالة المساعدة مع حقوق الملكية"""
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "دليل الاستخدام",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1a1a1a",
                    "align": "center"
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#e8e8e8"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "الأوامر الأساسية:",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#1a1a1a",
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": "▪️ انضم - التسجيل في البوت\n▪️ نقاطي - عرض إحصائياتك\n▪️ الصدارة - أفضل اللاعبين\n▪️ إيقاف - إنهاء اللعبة الحالية",
                            "size": "xs",
                            "color": "#4a4a4a",
                            "margin": "md",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "أوامر أثناء اللعب:",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#1a1a1a",
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": "▪️ لمح - الحصول على تلميح\n▪️ جاوب - عرض الإجابة والانتقال",
                            "size": "xs",
                            "color": "#4a4a4a",
                            "margin": "md",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "الألعاب المتوفرة:",
                            "weight": "bold",
                            "size": "sm",
                            "color": "#1a1a1a",
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": "ذكاء • لون • سلسلة • ترتيب\nتكوين • أسرع • لعبة • خمن\nتوافق • رياضيات • ذاكرة • لغز\nضد • إيموجي • أغنية",
                            "size": "xs",
                            "color": "#4a4a4a",
                            "margin": "md",
                            "wrap": True,
                            "align": "center"
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xl",
                    "color": "#e8e8e8"
                },
                {
                    "type": "text",
                    "text": "© بوت الحُوت",
                    "size": "xxs",
                    "color": "#9a9a9a",
                    "align": "center",
                    "margin": "lg"
                }
            ],
            "backgroundColor": "#ffffff",
            "paddingAll": "24px"
        },
        "styles": {
            "body": {
                "separator": True
            }
        }
    }

def get_stats_message(display_name, stats, is_registered):
    """رسالة الإحصائيات"""
    total_points = stats['total_points']
    games_played = stats['games_played']
    wins = stats['wins']
    win_rate = get_win_rate(games_played, wins)
    
    status_text = "✅ مسجل" if is_registered else "⚠️ غير مسجل"
    status_color = "#4caf50" if is_registered else "#ff9800"
    
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"📊 إحصائيات {display_name}",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1a1a1a",
                    "align": "center"
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#e8e8e8"
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
                                    "text": "الحالة",
                                    "size": "sm",
                                    "color": "#6a6a6a",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": status_text,
                                    "size": "sm",
                                    "color": status_color,
                                    "align": "end",
                                    "weight": "bold"
                                }
                            ],
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "▪️ إجمالي النقاط",
                                    "size": "sm",
                                    "color": "#4a4a4a",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": format_number(total_points),
                                    "size": "sm",
                                    "color": "#1a1a1a",
                                    "align": "end",
                                    "weight": "bold"
                                }
                            ],
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "▪️ عدد الألعاب",
                                    "size": "sm",
                                    "color": "#4a4a4a",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": str(games_played),
                                    "size": "sm",
                                    "color": "#1a1a1a",
                                    "align": "end",
                                    "weight": "bold"
                                }
                            ],
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "▪️ الانتصارات",
                                    "size": "sm",
                                    "color": "#4a4a4a",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": str(wins),
                                    "size": "sm",
                                    "color": "#1a1a1a",
                                    "align": "end",
                                    "weight": "bold"
                                }
                            ],
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "▪️ معدل الفوز",
                                    "size": "sm",
                                    "color": "#4a4a4a",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": win_rate,
                                    "size": "sm",
                                    "color": "#4caf50",
                                    "align": "end",
                                    "weight": "bold"
                                }
                            ],
                            "margin": "md"
                        }
                    ]
                }
            ],
            "backgroundColor": "#ffffff",
            "paddingAll": "24px"
        },
        "styles": {
            "body": {
                "separator": True
            }
        }
    }

def get_leaderboard_message(leaders):
    """رسالة لوحة الصدارة"""
    leader_boxes = []
    
    for rank, leader in enumerate(leaders[:10], 1):
        emoji = get_emoji_for_rank(rank)
        
        # ألوان متدرجة للمراكز الثلاثة الأولى
        if rank == 1:
            name_color = "#FFD700"  # ذهبي
        elif rank == 2:
            name_color = "#C0C0C0"  # فضي
        elif rank == 3:
            name_color = "#CD7F32"  # برونزي
        else:
            name_color = "#4a4a4a"
        
        leader_box = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": f"{emoji} {rank}",
                    "size": "sm",
                    "color": name_color,
                    "weight": "bold",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": leader['display_name'],
                    "size": "sm",
                    "color": "#1a1a1a",
                    "flex": 2,
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": format_number(leader['total_points']),
                    "size": "sm",
                    "color": "#6a6a6a",
                    "align": "end"
                }
            ],
            "margin": "md" if rank > 1 else "lg"
        }
        
        leader_boxes.append(leader_box)
    
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🏆 لوحة الصدارة",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1a1a1a",
                    "align": "center"
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#e8e8e8"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": leader_boxes
                }
            ],
            "backgroundColor": "#ffffff",
            "paddingAll": "24px"
        },
        "styles": {
            "body": {
                "separator": True
            }
        }
    }

def get_join_message(display_name):
    """رسالة الانضمام"""
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "✅ تم التسجيل بنجاح",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#4caf50",
                    "align": "center"
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#e8e8e8"
                },
                {
                    "type": "text",
                    "text": f"مرحباً {display_name}!",
                    "size": "md",
                    "color": "#1a1a1a",
                    "align": "center",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "▪️ يمكنك الآن اللعب في جميع الألعاب\n▪️ جمع النقاط والمنافسة\n▪️ الظهور في لوحة الصدارة",
                    "size": "sm",
                    "color": "#4a4a4a",
                    "align": "center",
                    "margin": "lg",
                    "wrap": True
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#e8e8e8"
                },
                {
                    "type": "text",
                    "text": "اختر لعبة للبدء!",
                    "size": "sm",
                    "color": "#6a6a6a",
                    "align": "center",
                    "margin": "lg"
                }
            ],
            "backgroundColor": "#ffffff",
            "paddingAll": "24px"
        },
        "styles": {
            "body": {
                "separator": True
            }
        }
    }

def get_winner_announcement(winner_name, winner_points, game_type, total_questions):
    """إعلان الفائز"""
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🏆",
                    "size": "4xl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "انتهت اللعبة!",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1a1a1a",
                    "align": "center",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#e8e8e8"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"لعبة {game_type}",
                            "size": "sm",
                            "color": "#6a6a6a",
                            "align": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": f"الفائز: {winner_name}",
                            "weight": "bold",
                            "size": "lg",
                            "color": "#FFD700",
                            "align": "center",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": f"▪️ النقاط: {winner_points}",
                            "size": "md",
                            "color": "#4a4a4a",
                            "align": "center",
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": f"▪️ عدد الأسئلة: {total_questions}",
                            "size": "sm",
                            "color": "#6a6a6a",
                            "align": "center",
                            "margin": "sm"
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#e8e8e8"
                },
                {
                    "type": "text",
                    "text": "أحسنت! 🎉",
                    "size": "md",
                    "color": "#4caf50",
                    "align": "center",
                    "margin": "lg"
                }
            ],
            "backgroundColor": "#ffffff",
            "paddingAll": "24px"
        },
        "styles": {
            "body": {
                "separator": True
            }
        }
    }
