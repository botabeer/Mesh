"""
🎮 Bot Mesh v7.0 - Game UI Builder
واجهات الألعاب الاحترافية مع تصميم ثلاثي الأبعاد
Created by: Abeer Aldosari © 2025
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from constants import THEMES, DEFAULT_THEME, BOT_NAME, BOT_RIGHTS, FIXED_BUTTONS, GAME_LIST


def create_quick_reply_buttons():
    """إنشاء أزرار Quick Reply ثابتة"""
    items = [
        QuickReplyItem(
            action=MessageAction(label=FIXED_BUTTONS["home"]["label"], text=FIXED_BUTTONS["home"]["text"])
        ),
        QuickReplyItem(
            action=MessageAction(label=FIXED_BUTTONS["games"]["label"], text=FIXED_BUTTONS["games"]["text"])
        ),
        QuickReplyItem(
            action=MessageAction(label=FIXED_BUTTONS["points"]["label"], text=FIXED_BUTTONS["points"]["text"])
        ),
        QuickReplyItem(
            action=MessageAction(label=FIXED_BUTTONS["leaderboard"]["label"], text=FIXED_BUTTONS["leaderboard"]["text"])
        ),
        QuickReplyItem(
            action=MessageAction(label=FIXED_BUTTONS["help"]["label"], text=FIXED_BUTTONS["help"]["text"])
        )
    ]
    return QuickReply(items=items)


def build_game_question(
    game_name: str,
    game_icon: str,
    question_text: str,
    round_num: int,
    total_rounds: int,
    theme="💜",
    show_hint=True,
    show_reveal=True,
    previous_q=None,
    previous_a=None
):
    """
    بناء نافذة سؤال اللعبة مع تصميم احترافي
    
    Args:
        game_name: اسم اللعبة
        game_icon: أيقونة اللعبة
        question_text: نص السؤال
        round_num: رقم الجولة الحالية
        total_rounds: إجمالي الجولات
        theme: رمز الثيم
        show_hint: إظهار زر التلميح
        show_reveal: إظهار زر الإجابة
        previous_q: السؤال السابق (اختياري)
        previous_a: الإجابة السابقة (اختياري)
    
    Returns:
        FlexMessage: رسالة السؤال
    """
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # الرأس مع تأثير 3D
    header = {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{game_icon} {game_name}",
                        "weight": "bold",
                        "size": "xl",
                        "color": colors["primary"],
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": f"جولة {round_num}/{total_rounds}",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "end",
                        "flex": 2
                    }
                ]
            }
        ],
        "backgroundColor": colors["bg"],
        "paddingAll": "20px",
        "spacing": "md"
    }
    
    # المحتوى
    body_contents = []
    
    # السؤال السابق (إذا وُجد)
    if previous_q and previous_a:
        body_contents.extend([
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "📝 السؤال السابق:",
                        "size": "xs",
                        "color": colors["text2"],
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": str(previous_q)[:80],
                        "size": "xs",
                        "color": colors["text2"],
                        "wrap": True,
                        "margin": "xs"
                    },
                    {
                        "type": "text",
                        "text": f"✅ {previous_a}",
                        "size": "xs",
                        "color": colors["success"],
                        "wrap": True,
                        "margin": "xs"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "15px",
                "paddingAll": "12px",
                "margin": "none"
            },
            {
                "type": "separator",
                "color": colors["shadow1"],
                "margin": "md"
            }
        ])
    
    # السؤال الحالي مع تأثير Neumorphic
    body_contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": question_text,
                "size": "lg",
                "weight": "bold",
                "color": colors["text"],
                "align": "center",
                "wrap": True
            }
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "25px",
        "paddingAll": "30px",
        "margin": "md"
    })
    
    # معلومة إضافية
    body_contents.append({
        "type": "text",
        "text": "💡 اكتب إجابتك أو استخدم الأزرار",
        "size": "xs",
        "color": colors["text2"],
        "align": "center",
        "margin": "md",
        "wrap": True
    })
    
    body = {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": body_contents,
        "backgroundColor": colors["bg"],
        "paddingAll": "15px"
    }
    
    # التذييل مع الأزرار
    footer_buttons = []
    
    # أزرار التلميح والإجابة
    action_buttons = []
    if show_hint:
        action_buttons.append({
            "type": "button",
            "action": {"type": "message", "label": "💡 تلميح", "text": "لمح"},
            "style": "secondary",
            "height": "sm",
            "color": colors["shadow1"]
        })
    if show_reveal:
        action_buttons.append({
            "type": "button",
            "action": {"type": "message", "label": "🔍 إجابة", "text": "جاوب"},
            "style": "secondary",
            "height": "sm",
            "color": colors["shadow1"]
        })
    
    if action_buttons:
        footer_buttons.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": action_buttons
        })
    
    # زر الإيقاف
    footer_buttons.append({
        "type": "button",
        "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
        "style": "primary",
        "height": "sm",
        "color": colors["error"],
        "margin": "sm" if action_buttons else "none"
    })
    
    # الحقوق
    footer_buttons.extend([
        {"type": "separator", "color": colors["shadow1"], "margin": "md"},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ])
    
    footer = {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": footer_buttons,
        "backgroundColor": colors["bg"],
        "paddingAll": "15px"
    }
    
    # بناء البطاقة النهائية
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": header,
        "body": body,
        "footer": footer,
        "styles": {
            "header": {"backgroundColor": colors["bg"]},
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text=f"{game_name} - جولة {round_num}",
        contents=FlexContainer.from_dict(bubble),
        quick_reply=create_quick_reply_buttons()
    )


def build_game_result(
    game_name: str,
    game_icon: str,
    points: int,
    total_rounds: int,
    theme="💜"
):
    """
    بناء نافذة نهاية الجولة مع زر إعادة
    
    Args:
        game_name: اسم اللعبة
        game_icon: أيقونة اللعبة
        points: النقاط المكتسبة
        total_rounds: إجمالي الجولات
        theme: رمز الثيم
    
    Returns:
        FlexMessage: رسالة النتيجة
    """
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # تحديد المستوى والأيقونة
    if points >= 40:
        emoji = "🏆"
        status = "ممتاز جداً!"
        status_color = "#FFD700"
    elif points >= 30:
        emoji = "⭐"
        status = "رائع!"
        status_color = colors["success"]
    elif points >= 20:
        emoji = "👍"
        status = "جيد!"
        status_color = colors["primary"]
    elif points > 0:
        emoji = "💪"
        status = "حاول مرة أخرى"
        status_color = colors["text2"]
    else:
        emoji = "🎯"
        status = "المحاولة القادمة أفضل"
        status_color = colors["text2"]
    
    # الرأس
    header = {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": emoji,
                "size": "xxl",
                "align": "center",
                "color": status_color
            },
            {
                "type": "text",
                "text": "انتهت اللعبة!",
                "weight": "bold",
                "size": "xl",
                "color": colors["text"],
                "align": "center",
                "margin": "md"
            }
        ],
        "backgroundColor": colors["bg"],
        "paddingAll": "20px"
    }
    
    # المحتوى
    body = {
        "type": "box",
        "layout": "vertical",
        "spacing": "lg",
        "contents": [
            {
                "type": "text",
                "text": status,
                "size": "lg",
                "weight": "bold",
                "color": status_color,
                "align": "center"
            },
            {"type": "separator", "color": colors["shadow1"]},
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{game_icon} {game_name}",
                        "size": "md",
                        "color": colors["text"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"النقاط المكتسبة",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": str(points),
                        "size": "xxl",
                        "weight": "bold",
                        "color": colors["primary"],
                        "align": "center",
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": f"من أصل {total_rounds * 10} نقطة",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "xs"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "25px"
            }
        ],
        "backgroundColor": colors["bg"],
        "paddingAll": "20px"
    }
    
    # التذييل
    footer = {
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
                        "action": {"type": "message", "label": "🔄 إعادة", "text": f"لعبة {game_name}"},
                        "style": "primary",
                        "height": "sm",
                        "color": colors["button"]
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "🎮 ألعاب", "text": "العاب"},
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"},
                        "style": "secondary",
                        "height": "sm"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "🏆 الصدارة", "text": "صدارة"},
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
            },
            {"type": "separator", "color": colors["shadow1"], "margin": "md"},
            {
                "type": "text",
                "text": BOT_RIGHTS,
                "size": "xxs",
                "color": colors["text2"],
                "align": "center"
            }
        ],
        "backgroundColor": colors["bg"],
        "paddingAll": "15px"
    }
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "header": header,
        "body": body,
        "footer": footer,
        "styles": {
            "header": {"backgroundColor": colors["bg"]},
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text="نتيجة اللعبة",
        contents=FlexContainer.from_dict(bubble),
        quick_reply=create_quick_reply_buttons()
    )


def build_multiplayer_winner(
    game_name: str,
    game_icon: str,
    winners: list,  # [(name, points), ...]
    theme="💜"
):
    """
    بناء نافذة الفائز المتعددة
    
    Args:
        game_name: اسم اللعبة
        game_icon: أيقونة اللعبة
        winners: قائمة الفائزين [(name, points), ...]
        theme: رمز الثيم
    
    Returns:
        FlexMessage: رسالة الفائزين
    """
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    medals = ["🥇", "🥈", "🥉"]
    
    # الرأس
    header = {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "🎉",
                "size": "xxl",
                "align": "center"
            },
            {
                "type": "text",
                "text": "نتائج اللعبة",
                "weight": "bold",
                "size": "xl",
                "color": colors["text"],
                "align": "center",
                "margin": "md"
            },
            {
                "type": "text",
                "text": f"{game_icon} {game_name}",
                "size": "md",
                "color": colors["text2"],
                "align": "center",
                "margin": "sm"
            }
        ],
        "backgroundColor": colors["bg"],
        "paddingAll": "20px"
    }
    
    # قائمة الفائزين
    winner_items = []
    for i, (name, points) in enumerate(winners[:5], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        item_bg = colors["card"] if i <= 3 else "transparent"
        
        winner_items.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": medal,
                    "size": "lg" if i <= 3 else "md",
                    "flex": 0,
                    "color": colors["primary"],
                    "weight": "bold" if i <= 3 else "regular"
                },
                {
                    "type": "text",
                    "text": name,
                    "size": "md" if i <= 3 else "sm",
                    "color": colors["text"],
                    "flex": 3,
                    "weight": "bold" if i <= 3 else "regular"
                },
                {
                    "type": "text",
                    "text": f"{points} نقطة",
                    "size": "md" if i <= 3 else "sm",
                    "color": colors["primary"],
                    "align": "end",
                    "flex": 2,
                    "weight": "bold"
                }
            ],
            "spacing": "md",
            "paddingAll": "md",
            "backgroundColor": item_bg,
            "cornerRadius": "10px" if i <= 3 else "0px"
        })
        
        if i < len(winners[:5]):
            winner_items.append({
                "type": "separator",
                "color": colors["shadow1"],
                "margin": "sm"
            })
    
    # المحتوى
    body = {
        "type": "box",
        "layout": "vertical",
        "spacing": "lg",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "none",
                "contents": winner_items,
                "backgroundColor": colors["card"],
                "cornerRadius": "20px",
                "paddingAll": "15px"
            }
        ],
        "backgroundColor": colors["bg"],
        "paddingAll": "20px"
    }
    
    # التذييل
    footer = {
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
                        "action": {"type": "message", "label": "🔄 لعب مرة أخرى", "text": f"لعبة {game_name}"},
                        "style": "primary",
                        "height": "sm",
                        "color": colors["button"]
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "🏠 البداية", "text": "بداية"},
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
            },
            {"type": "separator", "color": colors["shadow1"], "margin": "md"},
            {
                "type": "text",
                "text": BOT_RIGHTS,
                "size": "xxs",
                "color": colors["text2"],
                "align": "center"
            }
        ],
        "backgroundColor": colors["bg"],
        "paddingAll": "15px"
    }
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "header": header,
        "body": body,
        "footer": footer,
        "styles": {
            "header": {"backgroundColor": colors["bg"]},
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text="نتائج اللعبة",
        contents=FlexContainer.from_dict(bubble),
        quick_reply=create_quick_reply_buttons()
    )


def build_compatibility_result(
    name1: str,
    name2: str,
    percentage: int,
    theme="💜"
):
    """
    بناء نافذة نتيجة التوافق الفخمة
    
    Args:
        name1: الاسم الأول
        name2: الاسم الثاني
        percentage: نسبة التوافق
        theme: رمز الثيم
    
    Returns:
        FlexMessage: رسالة التوافق
    """
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # تحديد الرسالة والأيقونة
    if percentage >= 90:
        message = "✨ توافق رائع جداً! علاقة مثالية 💕"
        emoji = "💕"
        result_color = "#FF1493"
    elif percentage >= 75:
        message = "💪 توافق ممتاز! علاقة قوية 💖"
        emoji = "💖"
        result_color = "#FF69B4"
    elif percentage >= 60:
        message = "🌟 توافق جيد! علاقة واعدة 💗"
        emoji = "💗"
        result_color = "#FF85C1"
    elif percentage >= 45:
        message = "🔧 توافق متوسط! يحتاج عمل 💛"
        emoji = "💛"
        result_color = "#FFD700"
    else:
        message = "⚠️ توافق ضعيف! قد تكون هناك تحديات 💔"
        emoji = "💔"
        result_color = "#808080"
    
    # الرأس
    header = {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "💖 اختبار التوافق 💖",
                "weight": "bold",
                "size": "xl",
                "color": "#FFFFFF",
                "align": "center"
            }
        ],
        "backgroundColor": "#FF69B4",
        "paddingAll": "20px"
    }
    
    # المحتوى
    body = {
        "type": "box",
        "layout": "vertical",
        "spacing": "lg",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{name1} 💘 {name2}",
                        "size": "xl",
                        "weight": "bold",
                        "color": colors["text"],
                        "align": "center",
                        "wrap": True
                    },
                    {
                        "type": "separator",
                        "margin": "lg",
                        "color": colors["shadow1"]
                    },
                    {
                        "type": "text",
                        "text": "نسبة التوافق:",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": emoji,
                                "size": "xl",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": f"{percentage}%",
                                "size": "xxl",
                                "weight": "bold",
                                "color": result_color,
                                "align": "center",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": emoji,
                                "size": "xl",
                                "flex": 0
                            }
                        ],
                        "spacing": "md",
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": message,
                        "size": "md",
                        "color": colors["text"],
                        "align": "center",
                        "wrap": True,
                        "margin": "lg"
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "25px",
                "paddingAll": "30px"
            },
            {
                "type": "text",
                "text": f"✨ نفس النسبة لو كتبت: {name2} {name1}",
                "size": "xs",
                "color": colors["text2"],
                "align": "center",
                "wrap": True
            }
        ],
        "backgroundColor": colors["bg"],
        "paddingAll": "20px"
    }
    
    # التذييل
    footer = {
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
                        "action": {"type": "message", "label": "🔄 اختبار آخر", "text": "لعبة توافق"},
                        "style": "primary",
                        "height": "sm",
                        "color": "#FF69B4"
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "🏠 البداية", "text": "بداية"},
                        "style": "secondary",
                        "height": "sm"
                    }
                ]
            },
            {"type": "separator", "color": colors["shadow1"], "margin": "md"},
            {
                "type": "text",
                "text": BOT_RIGHTS,
                "size": "xxs",
                "color": colors["text2"],
                "align": "center"
            }
        ],
        "backgroundColor": colors["bg"],
        "paddingAll": "15px"
    }
    
    bubble = {
        "type": "bubble",
        "size": "kilo",
        "header": header,
        "body": body,
        "footer": footer,
        "styles": {
            "header": {"backgroundColor": "#FF69B4"},
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(
        alt_text="نتيجة التوافق",
        contents=FlexContainer.from_dict(bubble),
        quick_reply=create_quick_reply_buttons()
    )


def build_help_menu(theme="💜"):
    """
    بناء قائمة المساعدة مع الأزرار
    
    Args:
        theme: رمز الثيم
    
    Returns:
        FlexMessage: رسالة المساعدة
    """
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # الرأس
    header = {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "❓ المساعدة",
                "weight": "bold",
                "size": "xxl",
                "color": colors["primary"],
                "align": "center"
            },
            {
                "type": "text",
                "text": "دليل استخدام Bot Mesh",
                "size": "sm",
                "color": colors["text2"],
                "align": "center",
                "margin": "sm"
            }
        ],
        "backgroundColor": colors["bg"],
        "paddingAll": "20px"
    }
    
    # أقسام المساعدة
    help_sections = [
        {
            "icon": "🎮",
            "title": "كيفية اللعب",
            "text": "• اكتب 'العاب' لعرض القائمة\n• اختر لعبة بالضغط على الزر\n• أجب على الأسئلة"
        },
        {
            "icon": "⌨️",
            "title": "الأوامر المتاحة",
            "text": "• بداية - الصفحة الرئيسية\n• العاب - قائمة الألعاب\n• نقاطي - إحصائياتك\n• صدارة - لوحة الصدارة"
        },
        {
            "icon": "🎯",
            "title": "أثناء اللعب",
            "text": "• لمح - للحصول على تلميح\n• جاوب - لكشف الإجابة\n• إيقاف - لإيقاف اللعبة"
        },
        {
            "
