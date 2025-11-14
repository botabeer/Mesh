from linebot.models import QuickReply, QuickReplyButton, MessageAction

def get_games_quick_reply():
    """الأزرار الثابتة - الألعاب فقط بأسلوب iOS"""
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="ذكاء", text="ذكاء")),
        QuickReplyButton(action=MessageAction(label="لون", text="لون")),
        QuickReplyButton(action=MessageAction(label="سلسلة", text="سلسلة")),
        QuickReplyButton(action=MessageAction(label="ترتيب", text="ترتيب")),
        QuickReplyButton(action=MessageAction(label="تكوين", text="تكوين")),
        QuickReplyButton(action=MessageAction(label="أسرع", text="أسرع")),
        QuickReplyButton(action=MessageAction(label="لعبة", text="لعبة")),
        QuickReplyButton(action=MessageAction(label="خمن", text="خمن")),
        QuickReplyButton(action=MessageAction(label="توافق", text="توافق")),
        QuickReplyButton(action=MessageAction(label="رياضيات", text="رياضيات")),
        QuickReplyButton(action=MessageAction(label="ذاكرة", text="ذاكرة")),
        QuickReplyButton(action=MessageAction(label="لغز", text="لغز")),
        QuickReplyButton(action=MessageAction(label="ضد", text="ضد"))
    ])

def get_welcome_message(display_name):
    """رسالة الترحيب بأسلوب iOS"""
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": f"مرحباً {display_name}",
                    "weight": "bold",
                    "size": "xxl",
                    "color": "#1a1a1a",
                    "align": "center"
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
                    "color": "#666666",
                    "align": "center",
                    "margin": "xl",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": "أو اكتب 'مساعدة' لعرض الأوامر",
                    "size": "xs",
                    "color": "#999999",
                    "align": "center",
                    "margin": "sm"
                }
            ],
            "paddingAll": "24px",
            "backgroundColor": "#ffffff"
        },
        "styles": {
            "body": {
                "separator": True
            }
        }
    }

def get_help_message():
    """رسالة المساعدة الكاملة بأسلوب iOS"""
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
                            "text": "الأوامر الأساسية",
                            "weight": "bold",
                            "size": "md",
                            "color": "#1a1a1a",
                            "margin": "lg"
                        },
                        {
                            "type": "text",
                            "text": "انضم • للتسجيل وجمع النقاط",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "md",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "نقاطي • عرض إحصائياتك",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "sm",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "الصدارة • أفضل اللاعبين",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "sm",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "إيقاف • إنهاء اللعبة الحالية",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "sm",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "انسحب • إلغاء التسجيل",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "sm",
                            "wrap": True
                        }
                    ],
                    "backgroundColor": "#f9f9f9",
                    "paddingAll": "16px",
                    "cornerRadius": "12px",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "أثناء اللعب",
                            "weight": "bold",
                            "size": "md",
                            "color": "#1a1a1a"
                        },
                        {
                            "type": "text",
                            "text": "لمح • تلميح للإجابة",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "md",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "جاوب • كشف الإجابة والانتقال",
                            "size": "sm",
                            "color": "#666666",
                            "margin": "sm",
                            "wrap": True
                        }
                    ],
                    "backgroundColor": "#f9f9f9",
                    "paddingAll": "16px",
                    "cornerRadius": "12px",
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "الألعاب المتاحة",
                            "weight": "bold",
                            "size": "md",
                            "color": "#1a1a1a"
                        },
                        {
                            "type": "text",
                            "text": "ذكاء • لون • سلسلة • ترتيب • تكوين • أسرع • لعبة • خمن • توافق • رياضيات • ذاكرة • لغز • ضد • إيموجي • أغنية",
                            "size": "xs",
                            "color": "#666666",
                            "margin": "md",
                            "wrap": True
                        }
                    ],
                    "backgroundColor": "#f9f9f9",
                    "paddingAll": "16px",
                    "cornerRadius": "12px",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": "#e8e8e8"
                },
                {
                    "type": "text",
                    "text": "تم إنشاء هذا البوت بواسطة عبير الدوسري",
                    "size": "xxs",
                    "color": "#999999",
                    "align": "center",
                    "margin": "lg"
                }
            ],
            "paddingAll": "24px",
            "backgroundColor": "#ffffff"
        }
    }

def get_stats_message(display_name, stats, is_registered):
    """رسالة الإحصائيات بأسلوب iOS"""
    total_points = stats.get('total_points', 0)
    games_played = stats.get('games_played', 0)
    wins = stats.get('wins', 0)
    win_rate = (wins / games_played * 100) if games_played > 0 else 0
    
    status_text = "مسجل" if is_registered else "غير مسجل"
    status_color = "#34c759" if is_registered else "#999999"
    
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": display_name,
                    "weight": "bold",
                    "size": "xl",
                    "color": "#1a1a1a",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": status_text,
                    "size": "xs",
                    "color": status_color,
                    "align": "center",
                    "margin": "sm"
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
                                    "text": "إجمالي النقاط",
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(total_points),
                                    "size": "sm",
                                    "color": "#1a1a1a",
                                    "weight": "bold",
                                    "align": "end"
                                }
                            ],
                            "spacing": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "عدد الألعاب",
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(games_played),
                                    "size": "sm",
                                    "color": "#1a1a1a",
                                    "weight": "bold",
                                    "align": "end"
                                }
                            ],
                            "spacing": "md",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "الانتصارات",
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": str(wins),
                                    "size": "sm",
                                    "color": "#1a1a1a",
                                    "weight": "bold",
                                    "align": "end"
                                }
                            ],
                            "spacing": "md",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "معدل الفوز",
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f"{win_rate:.1f}%",
                                    "size": "sm",
                                    "color": "#1a1a1a",
                                    "weight": "bold",
                                    "align": "end"
                                }
                            ],
                            "spacing": "md",
                            "margin": "md"
                        }
                    ],
                    "backgroundColor": "#f9f9f9",
                    "paddingAll": "16px",
                    "cornerRadius": "12px",
                    "margin": "lg"
                }
            ],
            "paddingAll": "24px",
            "backgroundColor": "#ffffff"
        }
    }

def get_leaderboard_message(leaders):
    """رسالة لوحة الصدارة بأسلوب iOS"""
    contents = [
        {
            "type": "text",
            "text": "لوحة الصدارة",
            "weight": "bold",
            "size": "xl",
            "color": "#1a1a1a",
            "align": "center"
        },
        {
            "type": "separator",
            "margin": "lg",
            "color": "#e8e8e8"
        }
    ]
    
    medal_colors = {
        0: "#FFD700",  # ذهبي
        1: "#C0C0C0",  # فضي
        2: "#CD7F32"   # برونزي
    }
    
    for idx, leader in enumerate(leaders[:10]):
        rank = idx + 1
        name = leader.get('display_name', 'لاعب')
        points = leader.get('total_points', 0)
        
        medal = ""
        rank_color = "#666666"
        
        if rank == 1:
            medal = "🥇 "
            rank_color = medal_colors[0]
        elif rank == 2:
            medal = "🥈 "
            rank_color = medal_colors[1]
        elif rank == 3:
            medal = "🥉 "
            rank_color = medal_colors[2]
        
        box_bg = "#f9f9f9" if idx % 2 == 0 else "#ffffff"
        
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": f"{medal}{rank}",
                    "size": "sm",
                    "color": rank_color,
                    "weight": "bold",
                    "flex": 0,
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": name,
                    "size": "sm",
                    "color": "#1a1a1a",
                    "flex": 3,
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": str(points),
                    "size": "sm",
                    "color": "#1a1a1a",
                    "weight": "bold",
                    "align": "end",
                    "flex": 0
                }
            ],
            "backgroundColor": box_bg,
            "paddingAll": "12px",
            "cornerRadius": "8px",
            "margin": "sm"
        })
    
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "24px",
            "backgroundColor": "#ffffff"
        }
    }

def get_join_message(display_name):
    """رسالة الانضمام بأسلوب iOS"""
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "✓",
                    "size": "xxl",
                    "color": "#34c759",
                    "align": "center",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": f"مرحباً {display_name}",
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
                    "type": "text",
                    "text": "تم تسجيلك بنجاح",
                    "size": "sm",
                    "color": "#666666",
                    "align": "center",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "يمكنك الآن اللعب وجمع النقاط",
                    "size": "xs",
                    "color": "#999999",
                    "align": "center",
                    "margin": "sm"
                }
            ],
            "paddingAll": "24px",
            "backgroundColor": "#ffffff"
        }
    }

def get_winner_announcement(winner_name, winner_points, game_type, total_questions):
    """إعلان الفائز بأسلوب iOS"""
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🏆",
                    "size": "xxl",
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "انتهت اللعبة",
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
                            "text": "الفائز",
                            "size": "sm",
                            "color": "#666666",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": winner_name,
                            "weight": "bold",
                            "size": "lg",
                            "color": "#1a1a1a",
                            "align": "center",
                            "margin": "sm"
                        },
                        {
                            "type": "text",
                            "text": f"{winner_points} نقطة",
                            "size": "md",
                            "color": "#34c759",
                            "align": "center",
                            "margin": "sm",
                            "weight": "bold"
                        }
                    ],
                    "backgroundColor": "#f9f9f9",
                    "paddingAll": "16px",
                    "cornerRadius": "12px",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": f"لعبة {game_type} • {total_questions} أسئلة",
                    "size": "xs",
                    "color": "#999999",
                    "align": "center",
                    "margin": "lg"
                }
            ],
            "paddingAll": "24px",
            "backgroundColor": "#ffffff"
        }
    }
