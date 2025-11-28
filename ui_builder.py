"""
Bot Mesh - UI Builder v7.1 PROFESSIONAL
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

✅ تصميم زجاجي ثلاثي الأبعاد احترافي
✅ بدون إيموجي زائد
✅ تناسق كامل بين جميع الواجهات
✅ أداء محسّن
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from constants import BOT_RIGHTS, THEMES, DEFAULT_THEME, GAME_LIST

# ============================================================================
# Core UI Components - Professional Glass Design
# ============================================================================

def create_glass_bubble(colors, header_content, body_content, footer_content=None):
    """إنشاء بطاقة زجاجية احترافية موحدة"""
    bubble = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": header_content,
            "backgroundColor": colors["card"],
            "paddingAll": "20px",
            "spacing": "sm"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": body_content,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px",
            "spacing": "md"
        },
        "styles": {
            "header": {
                "backgroundColor": colors["card"]
            },
            "body": {
                "backgroundColor": colors["bg"]
            }
        }
    }
    
    if footer_content:
        bubble["footer"] = {
            "type": "box",
            "layout": "vertical",
            "contents": footer_content,
            "backgroundColor": colors["card"],
            "paddingAll": "15px",
            "spacing": "sm"
        }
        bubble["styles"]["footer"] = {"backgroundColor": colors["card"]}
    
    return bubble

def create_separator(color):
    """فاصل احترافي"""
    return {"type": "separator", "color": color, "margin": "md"}

def create_text_block(text, size="md", color="#000000", weight="regular", align="start", wrap=True):
    """نص منسق"""
    return {
        "type": "text",
        "text": text,
        "size": size,
        "color": color,
        "weight": weight,
        "align": align,
        "wrap": wrap
    }

def create_button(label, text, color, style="primary"):
    """زر احترافي"""
    return {
        "type": "button",
        "action": {
            "type": "message",
            "label": label,
            "text": text
        },
        "style": style,
        "height": "sm",
        "color": color
    }

def create_info_card(colors, title, content):
    """بطاقة معلومات"""
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            create_text_block(title, "sm", colors["text2"], "bold"),
            create_text_block(content, "xs", colors["text2"], "regular", "start", True)
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "12px",
        "paddingAll": "12px",
        "margin": "sm"
    }

def create_stat_row(label, value, colors):
    """صف إحصائيات"""
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            create_text_block(label, "sm", colors["text"], "regular", "start", False),
            create_text_block(str(value), "sm", colors["primary"], "bold", "end", False)
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "8px",
        "paddingAll": "10px",
        "margin": "xs"
    }

# ============================================================================
# Games Menu - Professional
# ============================================================================

def build_games_menu(theme="أبيض"):
    """قائمة الألعاب الرئيسية - احترافية بدون إيموجي"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # ترتيب الألعاب
    games_order = ["أسرع", "ذكاء", "لعبة", "أغنية", "خمن", "سلسلة",
                   "ترتيب", "تكوين", "ضد", "لون", "رياضيات", "توافق"]
    
    # Header
    header = [
        create_text_block("الألعاب المتاحة", "xl", colors["primary"], "bold", "center"),
        create_text_block(f"اختر من {len(games_order)} لعبة", "sm", colors["text2"], "regular", "center")
    ]
    
    # Body - Game Buttons
    game_buttons = []
    for i in range(0, len(games_order), 3):
        row = {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": []
        }
        for game in games_order[i:i+3]:
            row["contents"].append(create_button(game, game, colors["shadow1"], "secondary"))
        game_buttons.append(row)
    
    body = [create_separator(colors["shadow1"])] + game_buttons + [
        create_separator(colors["shadow1"]),
        create_info_card(colors, "قواعد اللعب", 
                        "5 جولات • نقطة لكل إجابة • أول إجابة صحيحة فقط")
    ]
    
    # Footer
    footer = [
        create_separator(colors["shadow1"]),
        create_text_block(BOT_RIGHTS, "xxs", colors["text2"], "regular", "center")
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="الألعاب", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# My Points - Professional
# ============================================================================

def build_my_points(username, points, game_stats, theme="أبيض"):
    """صفحة النقاط - احترافية"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    total_games = sum(game_stats.values())
    
    # Header
    header = [
        create_text_block("نقاطي", "xl", colors["primary"], "bold", "center")
    ]
    
    # Body
    body = [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_text_block(username, "lg", colors["text"], "bold", "center"),
                create_text_block(str(points), "xxl", colors["primary"], "bold", "center"),
                create_text_block(f"إجمالي الألعاب: {total_games}", "sm", colors["text2"], "regular", "center")
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "20px"
        }
    ]
    
    # Game Stats
    if game_stats:
        body.append(create_separator(colors["shadow1"]))
        body.append(create_text_block("أكثر الألعاب", "md", colors["text"], "bold", "start"))
        
        sorted_games = sorted(game_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        for game_name, plays in sorted_games:
            body.append(create_stat_row(game_name, plays, colors))
    
    # Footer
    footer = [
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                create_button("الصدارة", "صدارة", colors["primary"]),
                create_button("الألعاب", "ألعاب", colors["shadow1"], "secondary")
            ]
        },
        create_separator(colors["shadow1"]),
        create_text_block(BOT_RIGHTS, "xxs", colors["text2"], "regular", "center")
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# Leaderboard - Professional
# ============================================================================

def build_leaderboard(leaderboard, theme="أبيض"):
    """لوحة الصدارة - احترافية"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # Header
    header = [
        create_text_block("الصدارة", "xl", colors["primary"], "bold", "center"),
        create_text_block(f"أفضل {len(leaderboard)} لاعبين", "sm", colors["text2"], "regular", "center")
    ]
    
    # Body
    body = [create_separator(colors["shadow1"])]
    
    if leaderboard:
        for i, (name, points) in enumerate(leaderboard):
            rank_display = ["المركز الأول", "المركز الثاني", "المركز الثالث"][i] if i < 3 else f"المركز {i+1}"
            body.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    create_text_block(rank_display, "xs", colors["text2"], "regular", "start"),
                    create_text_block(name[:20], "sm", colors["text"], "regular", "start"),
                    create_text_block(str(points), "sm", colors["primary"], "bold", "end")
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "10px",
                "paddingAll": "12px",
                "margin": "xs"
            })
    else:
        body.append(create_text_block("لا يوجد لاعبين بعد", "sm", colors["text2"], "regular", "center"))
    
    # Footer
    footer = [
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                create_button("نقاطي", "نقاطي", colors["primary"]),
                create_button("الألعاب", "ألعاب", colors["shadow1"], "secondary")
            ]
        },
        create_separator(colors["shadow1"]),
        create_text_block(BOT_RIGHTS, "xxs", colors["text2"], "regular", "center")
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# Registration Required
# ============================================================================

def build_registration_required(theme="أبيض"):
    """تنبيه التسجيل - احترافي"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    header = [
        create_text_block("تسجيل مطلوب", "xl", colors["error"], "bold", "center")
    ]
    
    body = [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_text_block("يجب التسجيل للمشاركة في الألعاب", "md", colors["text"], "regular", "center")
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "20px"
        }
    ]
    
    footer = [
        create_button("انضم الآن", "انضم", colors["primary"]),
        create_separator(colors["shadow1"]),
        create_text_block(BOT_RIGHTS, "xxs", colors["text2"], "regular", "center")
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="تسجيل مطلوب", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# Winner Announcement
# ============================================================================

def build_winner_announcement(username, game_name, total_score, final_points, theme="أبيض"):
    """إعلان الفائز - احترافي"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    header = [
        create_text_block("تهانينا", "xxl", colors["success"], "bold", "center")
    ]
    
    body = [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                create_text_block(username, "xl", colors["text"], "bold", "center"),
                create_text_block(f"أنهيت لعبة {game_name}", "md", colors["text2"], "regular", "center"),
                create_separator(colors["shadow1"]),
                create_text_block(f"+{total_score}", "xxl", colors["primary"], "bold", "center"),
                create_text_block(f"الإجمالي: {final_points}", "md", colors["text2"], "regular", "center")
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "20px"
        }
    ]
    
    footer = [
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                create_button("إعادة", f"إعادة {game_name}", colors["primary"]),
                create_button("الألعاب", "ألعاب", colors["shadow1"], "secondary")
            ]
        },
        create_separator(colors["shadow1"]),
        create_text_block(BOT_RIGHTS, "xxs", colors["text2"], "regular", "center")
    ]
    
    bubble = create_glass_bubble(colors, header, body, footer)
    return FlexMessage(alt_text="الفائز", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# Dummy/Compatibility Functions
# ============================================================================

def build_home(theme, username, points, is_registered):
    """عرض الألعاب"""
    return build_games_menu(theme)

def build_group_game_result(theme):
    """نتيجة المجموعة"""
    return build_games_menu(theme)

def build_help_menu(theme):
    """المساعدة"""
    return build_games_menu(theme)

def build_game_stats(theme):
    """إحصائيات الألعاب"""
    return build_games_menu(theme)

def build_detailed_game_info(theme):
    """معلومات مفصلة"""
    return build_games_menu(theme)
