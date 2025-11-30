from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
from constants import GAME_LIST, DEFAULT_THEME, THEMES, BOT_NAME, BOT_RIGHTS, FIXED_GAME_QR

def _c(t=None): 
    """الحصول على ألوان الثيم"""
    return THEMES.get(t or DEFAULT_THEME, THEMES[DEFAULT_THEME])

def _3d_card(contents, theme=None, padding="20px"):
    """كارد ثري دي فاخر مع ظل وتدرج"""
    c = _c(theme)
    return {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "backgroundColor": c["card"],
        "cornerRadius": "20px",
        "paddingAll": padding,
        "borderWidth": "2px",
        "borderColor": c["border"],
        "margin": "md"
    }

def _gradient_header(text, icon, theme=None):
    """هيدر بتدرج لوني"""
    c = _c(theme)
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "text",
                "text": icon,
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "flex": 0
            },
            {
                "type": "text",
                "text": text,
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "flex": 1,
                "align": "center"
            }
        ],
        "paddingBottom": "lg"
    }

def _premium_button(label, text, style="primary", theme=None):
    """زر فاخر مع تأثيرات"""
    c = _c(theme)
    return {
        "type": "button",
        "action": {
            "type": "message",
            "label": label,
            "text": text
        },
        "style": style,
        "height": "sm",
        "color": c["primary"] if style == "primary" else c["secondary"]
    }

def _separator_3d(theme=None):
    """فاصل ثري دي"""
    c = _c(theme)
    return {
        "type": "separator",
        "margin": "lg",
        "color": c["border"]
    }

def _stat_box(label, value, color_key="primary", theme=None):
    """صندوق إحصائيات أنيق"""
    c = _c(theme)
    return _3d_card([
        {
            "type": "text",
            "text": label,
            "size": "sm",
            "color": c["text2"],
            "align": "center"
        },
        {
            "type": "text",
            "text": str(value),
            "size": "xxl",
            "weight": "bold",
            "color": c[color_key],
            "align": "center",
            "margin": "sm"
        }
    ], theme, "15px")

def _flex(alt_text, body):
    """إنشاء Flex Message"""
    return FlexMessage(alt_text=alt_text, contents=FlexContainer.from_dict(body))

def build_games_quick_reply():
    """Quick Reply للألعاب"""
    return QuickReply(items=[
        QuickReplyItem(action=MessageAction(label=i["label"], text=i["text"])) 
        for i in FIXED_GAME_QR
    ])

def attach_quick_reply(m):
    """إضافة Quick Reply"""
    if m and hasattr(m, 'quick_reply'):
        m.quick_reply = build_games_quick_reply()
    return m

# ============================================================================
# 🏠 الصفحة الرئيسية - فاخرة جداً
# ============================================================================
def build_enhanced_home(username, points, is_registered=True, theme=DEFAULT_THEME):
    """صفحة رئيسية ثري دي فاخرة"""
    c = _c(theme)
    status = "☑️ مسجل" if is_registered else "⚪ غير مسجل"
    join_text = "انسحب" if is_registered else "انضم"
    
    themes_list = list(THEMES.keys())
    theme_buttons = []
    for i in range(0, len(themes_list), 3):
        row = {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [
                _premium_button(t, f"ثيم {t}", "primary" if t == theme else "secondary", theme)
                for t in themes_list[i:i+3]
            ]
        }
        theme_buttons.append(row)
    
    body = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # Header
                _gradient_header(BOT_NAME, "✨", theme),
                
                _separator_3d(theme),
                
                # Stats Card
                _3d_card([
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "👤",
                                "size": "xl",
                                "flex": 0
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": username,
                                        "size": "lg",
                                        "weight": "bold",
                                        "color": c["text"]
                                    },
                                    {
                                        "type": "text",
                                        "text": status,
                                        "size": "sm",
                                        "color": c["success"] if is_registered else c["text3"]
                                    }
                                ],
                                "flex": 1,
                                "margin": "md"
                            }
                        ]
                    },
                    {
                        "type": "separator",
                        "margin": "md",
                        "color": c["border"]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "☑️ النقاط",
                                "size": "md",
                                "color": c["text2"],
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": str(points),
                                "size": "xxl",
                                "weight": "bold",
                                "color": c["primary"],
                                "flex": 0
                            }
                        ],
                        "margin": "md"
                    }
                ], theme),
                
                # Themes Section
                {
                    "type": "text",
                    "text": "🎨 اختر الثيم",
                    "size": "lg",
                    "weight": "bold",
                    "color": c["text"],
                    "margin": "xl"
                },
                
                *theme_buttons,
                
                _separator_3d(theme),
                
                # Action Buttons
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "lg",
                    "contents": [
                        _premium_button(f"🚪 {join_text}", join_text, "primary" if is_registered else "secondary", theme),
                        _premium_button("🎮 الألعاب", "ألعاب", "secondary", theme)
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "sm",
                    "contents": [
                        _premium_button("📊 نقاطي", "نقاطي", "secondary", theme),
                        _premium_button("🏆 الصدارة", "صدارة", "secondary", theme)
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "sm",
                    "contents": [
                        _premium_button("👥 فريقين", "فريقين", "secondary", theme),
                        _premium_button("📖 مساعدة", "مساعدة", "secondary", theme)
                    ]
                },
                
                _separator_3d(theme),
                
                # Footer
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "color": c["text3"],
                    "align": "center",
                    "wrap": True,
                    "margin": "md"
                }
            ],
            "paddingAll": "24px",
            "backgroundColor": c["bg"]
        }
    }
    
    return attach_quick_reply(_flex("البداية", body))

# ============================================================================
# 🎮 قائمة الألعاب - تصميم Grid فاخر
# ============================================================================
def build_games_menu(theme=DEFAULT_THEME):
    """قائمة ألعاب Grid ثري دي"""
    c = _c(theme)
    
    order = ["أسرع", "ذكاء", "لعبة", "أغنيه", "خمن", "سلسلة", 
             "ترتيب", "تكوين", "ضد", "لون", "رياضيات", "توافق"]
    
    game_buttons = []
    for i in range(0, len(order), 3):
        row = {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [
                _premium_button(order[i+j], order[i+j], "primary", theme)
                for j in range(3) if i+j < len(order)
            ]
        }
        game_buttons.append(row)
    
    body = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                _gradient_header("الألعاب المتاحة", "🎮", theme),
                
                {
                    "type": "text",
                    "text": "بوت ميوشتي",
                    "size": "sm",
                    "color": c["text2"],
                    "align": "center"
                },
                
                _separator_3d(theme),
                
                *game_buttons,
                
                # Instructions Card
                _3d_card([
                    {
                        "type": "text",
                        "text": "📋 أوامر اللعب",
                        "size": "md",
                        "weight": "bold",
                        "color": c["text"]
                    },
                    {
                        "type": "text",
                        "text": "• اضغط على اسم اللعبة للبدء\n• لمح للتلميح | جاوب للكشف\n• إيقاف لإنهاء اللعبة",
                        "size": "xs",
                        "color": c["text2"],
                        "wrap": True,
                        "margin": "sm"
                    }
                ], theme, "15px"),
                
                # Bottom Buttons
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "lg",
                    "contents": [
                        _premium_button("🏠 البداية", "بداية", "secondary", theme),
                        _premium_button("⏹️ إيقاف", "إيقاف", "secondary", theme)
                    ]
                },
                
                _separator_3d(theme),
                
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "color": c["text3"],
                    "align": "center",
                    "wrap": True
                }
            ],
            "paddingAll": "24px",
            "backgroundColor": c["bg"]
        }
    }
    
    return attach_quick_reply(_flex("الألعاب", body))

# ============================================================================
# 📊 نقاطي - بطاقة إحصائيات أنيقة
# ============================================================================
def build_my_points(username, points, stats=None, theme=DEFAULT_THEME):
    """بطاقة نقاط فاخرة"""
    c = _c(theme)
    
    # تحديد المستوى
    if points < 50:
        level = "🥉 مبتدئ"
        level_color = c["text2"]
    elif points < 150:
        level = "🥈 متوسط"
        level_color = c["info"]
    elif points < 300:
        level = "🥇 متقدم"
        level_color = c["warning"]
    else:
        level = "🏆 محترف"
        level_color = c["success"]
    
    body = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                _gradient_header("إحصائياتي", "📊", theme),
                
                _separator_3d(theme),
                
                # Main Stats
                _3d_card([
                    {
                        "type": "text",
                        "text": username,
                        "size": "xl",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            _stat_box("☑️ النقاط", points, "primary", theme),
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "المستوى",
                                        "size": "sm",
                                        "color": c["text2"],
                                        "align": "center"
                                    },
                                    {
                                        "type": "text",
                                        "text": level,
                                        "size": "lg",
                                        "weight": "bold",
                                        "color": level_color,
                                        "align": "center",
                                        "margin": "sm"
                                    }
                                ],
                                "backgroundColor": c["card"],
                                "cornerRadius": "20px",
                                "paddingAll": "15px",
                                "borderWidth": "2px",
                                "borderColor": c["border"],
                                "margin": "md",
                                "flex": 1
                            }
                        ],
                        "spacing": "sm",
                        "margin": "md"
                    }
                ], theme),
                
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "xl",
                    "contents": [
                        _premium_button("🏠 البداية", "بداية", "secondary", theme),
                        _premium_button("🏆 الصدارة", "صدارة", "primary", theme)
                    ]
                },
                
                _separator_3d(theme),
                
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "color": c["text3"],
                    "align": "center"
                }
            ],
            "paddingAll": "24px",
            "backgroundColor": c["bg"]
        }
    }
    
    return attach_quick_reply(_flex("نقاطي", body))

# ============================================================================
# 🏆 لوحة الصدارة - تصميم فاخر
# ============================================================================
def build_leaderboard(top_users, theme=DEFAULT_THEME):
    """لوحة صدارة ثري دي فاخرة"""
    c = _c(theme)
    medals = ["🥇", "🥈", "🥉"]
    
    leaderboard_items = []
    for i, (name, pts, is_registered) in enumerate(top_users[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        medal_color = c["primary"] if i <= 3 else c["text"]
        
        item = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": medal,
                            "size": "xl",
                            "weight": "bold",
                            "color": medal_color,
                            "flex": 0
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": name,
                                    "size": "md",
                                    "weight": "bold",
                                    "color": c["text"]
                                },
                                {
                                    "type": "text",
                                    "text": "☑️ نشط" if is_registered else "⚪ غير نشط",
                                    "size": "xs",
                                    "color": c["success"] if is_registered else c["text3"]
                                }
                            ],
                            "flex": 3,
                            "margin": "md"
                        },
                        {
                            "type": "text",
                            "text": str(pts),
                            "size": "xl",
                            "weight": "bold",
                            "color": c["primary"],
                            "align": "end",
                            "flex": 1
                        }
                    ]
                }
            ],
            "backgroundColor": c["card"],
            "cornerRadius": "15px",
            "paddingAll": "15px",
            "borderWidth": "2px",
            "borderColor": c["border"],
            "margin": "sm"
        }
        leaderboard_items.append(item)
    
    if not leaderboard_items:
        leaderboard_items = [{
            "type": "text",
            "text": "لا يوجد لاعبين بعد",
            "size": "md",
            "color": c["text2"],
            "align": "center"
        }]
    
    body = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                _gradient_header("لوحة الصدارة", "🏆", theme),
                
                _separator_3d(theme),
                
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": leaderboard_items,
                    "margin": "md"
                },
                
                _separator_3d(theme),
                
                {
                    "type": "text",
                    "text": "☑️ نشط = مسجل | ⚪ غير مسجل = ألغى التسجيل",
                    "size": "xxs",
                    "color": c["text3"],
                    "align": "center",
                    "wrap": True
                },
                
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "lg",
                    "contents": [
                        _premium_button("🏠 البداية", "بداية", "secondary", theme),
                        _premium_button("📊 نقاطي", "نقاطي", "primary", theme)
                    ]
                },
                
                _separator_3d(theme),
                
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "color": c["text3"],
                    "align": "center"
                }
            ],
            "paddingAll": "24px",
            "backgroundColor": c["bg"]
        }
    }
    
    return attach_quick_reply(_flex("الصدارة", body))

# ============================================================================
# 🏆 إعلان الفوز - تصميم احتفالي
# ============================================================================
def build_winner_announcement(username, game_name, round_points, total_points, theme=DEFAULT_THEME):
    """نافذة فوز ثري دي احتفالية"""
    c = _c(theme)
    
    body = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎉 مبروك! 🎉",
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": c["success"]
                },
                
                _separator_3d(theme),
                
                _3d_card([
                    {
                        "type": "text",
                        "text": username,
                        "size": "xl",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center"
                    }
                ], theme, "15px"),
                
                _3d_card([
                    {
                        "type": "text",
                        "text": "🎮 اللعبة",
                        "size": "sm",
                        "color": c["text2"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": game_name,
                        "size": "lg",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center",
                        "margin": "xs"
                    }
                ], theme, "15px"),
                
                _3d_card([
                    {
                        "type": "text",
                        "text": "💎 النقاط المكتسبة",
                        "size": "sm",
                        "color": c["text2"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"+{round_points}",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["success"],
                        "align": "center",
                        "margin": "sm"
                    }
                ], theme, "20px"),
                
                {
                    "type": "text",
                    "text": f"☑️ الإجمالي: {total_points}",
                    "size": "lg",
                    "weight": "bold",
                    "color": c["primary"],
                    "align": "center",
                    "margin": "md"
                },
                
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "xl",
                    "contents": [
                        _premium_button("🎮 الألعاب", "ألعاب", "primary", theme),
                        _premium_button("🏠 البداية", "بداية", "secondary", theme)
                    ]
                }
            ],
            "paddingAll": "24px",
            "backgroundColor": c["bg"]
        }
    }
    
    return attach_quick_reply(_flex("فوز", body))

# ============================================================================
# بقية الدوال (مختصرة)
# ============================================================================
def build_help_window(theme=DEFAULT_THEME):
    """نافذة مساعدة"""
    return build_games_menu(theme)  # Simplified

def build_theme_selector(theme=DEFAULT_THEME):
    """اختيار الثيمات"""
    return build_enhanced_home("مستخدم", 0, True, theme)  # Simplified

def build_registration_status(username, points, theme=DEFAULT_THEME):
    return TextMessage(text=f"☑️ تم التسجيل\nالاسم: {username}\nالنقاط: {points}")

def build_registration_required(theme=DEFAULT_THEME):
    return TextMessage(text="⚠️ التسجيل مطلوب\nاكتب: انضم")

def build_unregister_confirmation(username, points, theme=DEFAULT_THEME):
    return TextMessage(text=f"☑️ تم الانسحاب\nنقاطك: {points}")

def build_multiplayer_help_window(theme=DEFAULT_THEME):
    return TextMessage(text="👥 وضع الفريقين\n1. اكتب: انضم\n2. اختر اللعبة\n3. تقسيم تلقائي")

def build_join_confirmation(username, theme=DEFAULT_THEME):
    return TextMessage(text="☑️ انضممت للفريق")

def build_error_message(error_text, theme=DEFAULT_THEME):
    return TextMessage(text=f"❌ {error_text}")

def build_game_stopped(game_name, theme=DEFAULT_THEME):
    return TextMessage(text=f"⏹️ تم إيقاف {game_name}")

def build_team_game_end(team_points, theme=DEFAULT_THEME):
    c = _c(theme)
    t1, t2 = team_points.get("team1", 0), team_points.get("team2", 0)
    winner = "الفريق الأول 🥇" if t1 > t2 else "الفريق الثاني 🥈" if t2 > t1 else "⚖️ تعادل"
    
    body = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                _gradient_header("انتهت اللعبة!", "🏆", theme),
                _separator_3d(theme),
                _3d_card([
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"الفريق 1\n{t1}",
                                "size": "xl",
                                "weight": "bold",
                                "color": c["primary"],
                                "align": "center",
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": "VS",
                                "size": "lg",
                                "color": c["text2"],
                                "align": "center",
                                "flex": 0,
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": f"الفريق 2\n{t2}",
                                "size": "xl",
                                "weight": "bold",
                                "color": c["primary"],
                                "align": "center",
                                "flex": 1
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": f"الفائز: {winner}",
                        "size": "lg",
                        "weight": "bold",
                        "color": c["success"],
                        "align": "center",
                        "margin": "lg"
                    }
                ], theme),
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "xl",
                    "contents": [
                        _premium_button("🎮 الألعاب", "ألعاب", "primary", theme),
                        _premium_button("🏠 البداية", "بداية", "secondary", theme)
                    ]
                }
            ],
            "paddingAll": "24px",
            "backgroundColor": c["bg"]
        }
    }
    
    return attach_quick_reply(_flex("نتيجة", body))

def build_answer_feedback(message, theme=DEFAULT_THEME):
    return TextMessage(text=message)

__all__ = [
    'build_enhanced_home', 'build_games_menu', 'build_my_points', 'build_leaderboard',
    'build_help_window', 'build_registration_status', 'build_registration_required',
    'build_unregister_confirmation', 'build_winner_announcement', 'build_theme_selector',
    'build_multiplayer_help_window', 'attach_quick_reply', 'build_join_confirmation',
    'build_error_message', 'build_game_stopped', 'build_team_game_end', 'build_answer_feedback'
]
