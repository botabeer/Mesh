from config import BOT_NAME, BOT_CREATOR, BOT_YEAR

# ألوان Neumorphism
COLORS = {
    'bg': '#E0E5EC',
    'primary': '#6C63FF',
    'secondary': '#FF6B6B',
    'accent': '#4ECDC4',
    'text_dark': '#1a1a1a',
    'text_light': '#6a6a6a',
    'shadow_dark': '#A3B1C6',
    'shadow_light': '#FFFFFF',
    'success': '#51CF66',
    'warning': '#FFE66D',
    'gold': '#FFD700',
    'silver': '#C0C0C0',
    'bronze': '#CD7F32'
}

def get_footer():
    """حقوق الملكية"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [{
            "type": "text",
            "text": f"تم إنشاء هذا البوت بواسطة {BOT_CREATOR} © {BOT_YEAR}",
            "size": "xxs",
            "color": "#999999",
            "align": "center",
            "wrap": True
        }],
        "paddingTop": "md",
        "paddingBottom": "sm"
    }

def create_neuro_button(label, text, style="primary"):
    """زر بتصميم Neumorphism"""
    colors = {
        'primary': COLORS['primary'],
        'secondary': COLORS['secondary'],
        'success': COLORS['success']
    }
    return {
        "type": "button",
        "action": {"type": "message", "label": label, "text": text},
        "style": style,
        "color": colors.get(style, COLORS['primary']),
        "height": "sm"
    }

def create_welcome_flex(display_name, total_games=15):
    """شاشة الترحيب الرئيسية"""
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"🎮 {BOT_NAME}",
                            "weight": "bold",
                            "size": "xxl",
                            "color": COLORS['text_dark'],
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": f"مرحباً {display_name} 👋",
                            "size": "lg",
                            "color": COLORS['text_light'],
                            "align": "center",
                            "margin": "md"
                        },
                        {
                            "type": "separator",
                            "margin": "xl",
                            "color": COLORS['shadow_dark']
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎯 العب مع أصدقائك",
                            "size": "md",
                            "color": COLORS['text_dark'],
                            "weight": "bold",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": f"{total_games} لعبة ممتعة في انتظارك",
                            "size": "sm",
                            "color": COLORS['text_light'],
                            "align": "center",
                            "margin": "sm",
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "📝 سجل الآن لحفظ نقاطك",
                                    "size": "xs",
                                    "color": COLORS['primary'],
                                    "align": "center"
                                }
                            ],
                            "backgroundColor": f"{COLORS['primary']}15",
                            "cornerRadius": "md",
                            "paddingAll": "md",
                            "margin": "lg"
                        }
                    ],
                    "margin": "xl"
                },
                get_footer()
            ],
            "backgroundColor": COLORS['bg'],
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
                        create_neuro_button("🎮 انضم", "انضم", "primary"),
                        create_neuro_button("📊 نقاطي", "نقاطي", "secondary")
                    ],
                    "spacing": "sm"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        create_neuro_button("🏆 الصدارة", "الصدارة", "success"),
                        create_neuro_button("❓ مساعدة", "مساعدة", "secondary")
                    ],
                    "spacing": "sm",
                    "margin": "sm"
                }
            ],
            "backgroundColor": COLORS['bg'],
            "paddingAll": "16px"
        }
    }

def create_stats_flex(user_stats, is_registered):
    """إحصائيات المستخدم"""
    status = "✅ مسجل" if is_registered else "⚠️ غير مسجل"
    status_color = COLORS['success'] if is_registered else COLORS['warning']
    win_rate = (user_stats['wins'] / user_stats['games_played'] * 100) if user_stats['games_played'] > 0 else 0
    
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "📊 إحصائياتك",
                    "weight": "bold",
                    "size": "xl",
                    "color": COLORS['text_dark'],
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "الحالة", "size": "sm", "color": COLORS['text_light'], "flex": 2},
                        {"type": "text", "text": status, "size": "sm", "color": status_color, "flex": 3, "align": "end", "weight": "bold"}
                    ],
                    "margin": "xl"
                },
                {
                    "type": "separator",
                    "margin": "md",
                    "color": COLORS['shadow_dark']
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "🏆 النقاط", "size": "md", "color": COLORS['text_light'], "flex": 2},
                        {"type": "text", "text": str(user_stats['total_points']), "size": "xxl", "color": COLORS['primary'], "flex": 3, "align": "end", "weight": "bold"}
                    ],
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "🎮 ألعاب", "size": "sm", "color": COLORS['text_light'], "flex": 2},
                        {"type": "text", "text": str(user_stats['games_played']), "size": "md", "color": COLORS['text_dark'], "flex": 3, "align": "end"}
                    ],
                    "margin": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "✨ انتصارات", "size": "sm", "color": COLORS['text_light'], "flex": 2},
                        {"type": "text", "text": str(user_stats['wins']), "size": "md", "color": COLORS['success'], "flex": 3, "align": "end"}
                    ],
                    "margin": "sm"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "📈 نسبة الفوز", "size": "sm", "color": COLORS['text_light'], "flex": 2},
                        {"type": "text", "text": f"{win_rate:.1f}%", "size": "md", "color": COLORS['accent'], "flex": 3, "align": "end"}
                    ],
                    "margin": "sm"
                },
                get_footer()
            ],
            "backgroundColor": COLORS['bg'],
            "paddingAll": "24px"
        }
    }

def create_leaderboard_flex(leaders):
    """لوحة الصدارة"""
    medal_colors = [COLORS['gold'], COLORS['silver'], COLORS['bronze']]
    medals = ["🥇", "🥈", "🥉"]
    
    players_list = []
    for i, leader in enumerate(leaders, 1):
        bg_color = medal_colors[i-1] if i <= 3 else COLORS['bg']
        text_color = "#FFFFFF" if i <= 3 else COLORS['text_dark']
        medal = medals[i-1] if i <= 3 else f"{i}"
        
        players_list.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": medal, "size": "md", "color": text_color, "flex": 0, "weight": "bold"},
                {"type": "text", "text": leader['display_name'], "size": "sm", "color": text_color, "flex": 3, "margin": "md", "weight": "bold" if i <= 3 else "regular"},
                {"type": "text", "text": f"{leader['total_points']} 🏆", "size": "sm", "color": text_color, "flex": 2, "align": "end", "weight": "bold" if i <= 3 else "regular"}
            ],
            "backgroundColor": bg_color,
            "cornerRadius": "lg",
            "paddingAll": "14px",
            "margin": "sm" if i > 1 else "none"
        })
    
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🏆 لوحة الصدارة",
                    "weight": "bold",
                    "size": "xl",
                    "color": COLORS['text_dark'],
                    "align": "center"
                },
                {
                    "type": "separator",
                    "margin": "lg",
                    "color": COLORS['shadow_dark']
                },
                *players_list,
                get_footer()
            ],
            "backgroundColor": COLORS['bg'],
            "paddingAll": "20px"
        }
    }

def create_game_card(game_name, question, options=None):
    """بطاقة اللعبة بتصميم Neumorphism"""
    contents = [
        {
            "type": "text",
            "text": f"🎮 {game_name}",
            "weight": "bold",
            "size": "xl",
            "color": COLORS['text_dark'],
            "align": "center"
        },
        {
            "type": "separator",
            "margin": "lg",
            "color": COLORS['shadow_dark']
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "text",
                "text": question,
                "size": "lg",
                "color": COLORS['text_dark'],
                "align": "center",
                "wrap": True,
                "weight": "bold"
            }],
            "backgroundColor": f"{COLORS['primary']}15",
            "cornerRadius": "xl",
            "paddingAll": "20px",
            "margin": "lg"
        }
    ]
    
    if options:
        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [{
                "type": "text",
                "text": opt,
                "size": "sm",
                "color": COLORS['text_light'],
                "align": "center"
            } for opt in options],
            "margin": "lg",
            "spacing": "sm"
        })
    
    contents.append(get_footer())
    
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": COLORS['bg'],
            "paddingAll": "24px"
        }
    }
