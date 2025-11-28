"""
Bot Mesh - UI Builder v7.0
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

✅ Professional 3D Glass Design
✅ Minimal Emojis
✅ Clean & Modern
✅ Groups Optimized
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from constants import BOT_RIGHTS, THEMES, DEFAULT_THEME, GAME_LIST

# ============================================================================
# Core UI Builder
# ============================================================================

def create_glass_card(colors, header, body_contents, footer_contents=None):
    """إنشاء بطاقة زجاجية ثلاثية الأبعاد"""
    card = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": header,
            "backgroundColor": colors["card"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": body_contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        }
    }
    
    if footer_contents:
        card["footer"] = {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_contents,
            "backgroundColor": colors["card"],
            "paddingAll": "15px"
        }
    
    return card

def create_button(label, text, colors, style="primary"):
    """إنشاء زر احترافي"""
    return {
        "type": "button",
        "action": {"type": "message", "label": label, "text": text},
        "style": style,
        "height": "sm",
        "color": colors["primary"] if style == "primary" else colors["shadow1"]
    }

# ============================================================================
# Games Menu (Main UI)
# ============================================================================

def build_games_menu(theme="أبيض"):
    """قائمة الألعاب الرئيسية - تظهر عند المنشن"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    games_ordered = [
        "أسرع", "ذكاء", "لعبة", "أغنية", "خمن", "سلسلة",
        "ترتيب", "تكوين", "ضد", "لون", "رياضيات", "توافق"
    ]
    
    # إنشاء صفوف الألعاب
    game_rows = []
    for i in range(0, len(games_ordered), 3):
        row_games = games_ordered[i:i+3]
        game_rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                create_button(game, game, colors, "secondary")
                for game in row_games
            ]
        })
    
    header = [
        {
            "type": "text",
            "text": "الألعاب المتاحة",
            "weight": "bold",
            "size": "xl",
            "color": colors["primary"]
        },
        {
            "type": "text",
            "text": f"{len(games_ordered)} لعبة",
            "size": "sm",
            "color": colors["text2"]
        }
    ]
    
    body_contents = [
        {"type": "separator", "color": colors["shadow1"]}
    ] + game_rows + [
        {"type": "separator", "color": colors["shadow1"], "margin": "lg"},
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "• اضغط على اسم اللعبة للبدء\n• خمس جولات لكل لعبة\n• نقطة واحدة لكل إجابة صحيحة\n• أول إجابة صحيحة فقط",
                    "size": "xs",
                    "color": colors["text2"],
                    "wrap": True
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "10px",
            "paddingAll": "12px"
        }
    ]
    
    footer = [
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return FlexMessage(
        alt_text="الألعاب",
        contents=FlexContainer.from_dict(
            create_glass_card(colors, header, body_contents, footer)
        )
    )

# ============================================================================
# My Points
# ============================================================================

def build_my_points(username, points, game_stats, theme="أبيض"):
    """صفحة نقاط المستخدم"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    total_games = sum(game_stats.values())
    
    header = [
        {
            "type": "text",
            "text": "نقاطي",
            "weight": "bold",
            "size": "xl",
            "color": colors["primary"]
        }
    ]
    
    stats_rows = []
    for game_name, plays in sorted(game_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
        stats_rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": game_name,
                    "size": "sm",
                    "color": colors["text"],
                    "flex": 3
                },
                {
                    "type": "text",
                    "text": f"{plays}",
                    "size": "sm",
                    "color": colors["primary"],
                    "align": "end",
                    "flex": 1
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "8px",
            "paddingAll": "8px",
            "margin": "xs"
        })
    
    body_contents = [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": username,
                    "size": "lg",
                    "weight": "bold",
                    "color": colors["text"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"{points}",
                    "size": "xxl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"عدد الألعاب: {total_games}",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center"
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "20px"
        }
    ]
    
    if stats_rows:
        body_contents.extend([
            {"type": "separator", "color": colors["shadow1"], "margin": "md"},
            {
                "type": "text",
                "text": "أكثر الألعاب لعباً",
                "weight": "bold",
                "size": "md",
                "color": colors["text"]
            }
        ] + stats_rows)
    
    footer = [
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                create_button("الصدارة", "صدارة", colors),
                create_button("الألعاب", "ألعاب", colors)
            ]
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return FlexMessage(
        alt_text="نقاطي",
        contents=FlexContainer.from_dict(
            create_glass_card(colors, header, body_contents, footer)
        )
    )

# ============================================================================
# Leaderboard
# ============================================================================

def build_leaderboard(leaderboard, theme="أبيض"):
    """لوحة الصدارة"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    header = [
        {
            "type": "text",
            "text": "الصدارة",
            "weight": "bold",
            "size": "xl",
            "color": colors["primary"]
        },
        {
            "type": "text",
            "text": f"أفضل {len(leaderboard)} لاعبين",
            "size": "sm",
            "color": colors["text2"]
        }
    ]
    
    rank_medals = ["🥇", "🥈", "🥉"]
    
    leaderboard_rows = []
    for i, (name, points) in enumerate(leaderboard):
        medal = rank_medals[i] if i < 3 else str(i+1)
        leaderboard_rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": medal,
                    "size": "sm",
                    "color": colors["text"],
                    "flex": 1
                },
                {
                    "type": "text",
                    "text": name[:15],
                    "size": "sm",
                    "color": colors["text"],
                    "flex": 3
                },
                {
                    "type": "text",
                    "text": f"{points}",
                    "size": "sm",
                    "color": colors["primary"],
                    "weight": "bold",
                    "align": "end",
                    "flex": 1
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "8px",
            "paddingAll": "10px",
            "margin": "xs"
        })
    
    body_contents = [
        {"type": "separator", "color": colors["shadow1"]}
    ] + (leaderboard_rows if leaderboard_rows else [{
        "type": "text",
        "text": "لا يوجد لاعبين بعد",
        "size": "sm",
        "color": colors["text2"],
        "align": "center"
    }])
    
    footer = [
        {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                create_button("نقاطي", "نقاطي", colors),
                create_button("الألعاب", "ألعاب", colors)
            ]
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return FlexMessage(
        alt_text="الصدارة",
        contents=FlexContainer.from_dict(
            create_glass_card(colors, header, body_contents, footer)
        )
    )

# ============================================================================
# Registration Required
# ============================================================================

def build_registration_required(theme="أبيض"):
    """تنبيه التسجيل المطلوب"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    header = [
        {
            "type": "text",
            "text": "تسجيل مطلوب",
            "weight": "bold",
            "size": "xl",
            "color": colors["error"]
        }
    ]
    
    body_contents = [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "يجب التسجيل للمشاركة في الألعاب",
                    "size": "md",
                    "color": colors["text"],
                    "wrap": True,
                    "align": "center"
                }
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "15px",
            "paddingAll": "20px"
        }
    ]
    
    footer = [
        create_button("انضم الآن", "انضم", colors, "primary"),
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return FlexMessage(
        alt_text="تسجيل مطلوب",
        contents=FlexContainer.from_dict(
            create_glass_card(colors, header, body_contents, footer)
        )
    )

# ============================================================================
# Winner Announcement
# ============================================================================

def build_winner_announcement(username, game_name, total_score, final_points, theme="أبيض"):
    """إعلان الفائز"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    header = [
        {
            "type": "text",
            "text": "تهانينا",
            "size": "xxl",
            "weight": "bold",
            "color": colors["success"]
        }
    ]
    
    body_contents = [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": username,
                    "size": "xl",
                    "weight": "bold",
                    "color": colors["text"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"أنهيت {game_name}",
                    "size": "md",
                    "color": colors["text2"],
                    "align": "center",
                    "wrap": True
                },
                {"type": "separator", "color": colors["shadow1"], "margin": "md"},
                {
                    "type": "text",
                    "text": f"+{total_score}",
                    "size": "xxl",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"الإجمالي: {final_points}",
                    "size": "md",
                    "color": colors["text2"],
                    "align": "center"
                }
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
                create_button("إعادة", f"إعادة {game_name}", colors),
                create_button("الألعاب", "ألعاب", colors)
            ]
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    return FlexMessage(
        alt_text="الفائز",
        contents=FlexContainer.from_dict(
            create_glass_card(colors, header, body_contents, footer)
        )
    )

# ============================================================================
# Dummy Functions for Compatibility
# ============================================================================

def build_home(theme, username, points, is_registered):
    """Dummy - يعرض الألعاب"""
    return build_games_menu(theme)

def build_group_game_result(theme):
    """Dummy"""
    return build_games_menu(theme)

def build_help_menu(theme):
    """Dummy"""
    return build_games_menu(theme)

def build_game_stats(theme):
    """Dummy"""
    return build_games_menu(theme)

def build_detailed_game_info(theme):
    """Dummy"""
    return build_games_menu(theme)
