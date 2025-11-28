"""
Bot Mesh - UI Builder v10.0 GLASS MORPHISM PRO
Created by: Abeer Aldosari © 2025
✨ تصميم زجاجي ثلاثي الأبعاد احترافي
🎨 نظام بطاقات ذكي مع أيقونات
🚀 تجربة مستخدم سلسة ومتكاملة
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from constants import BOT_RIGHTS, THEMES, DEFAULT_THEME, GAME_LIST

# ============================================================================
# ADVANCED GLASS COMPONENTS
# ============================================================================

def create_glass_header(colors, title, subtitle=None, icon=None):
    header_content = []
    if icon:
        header_content.append({"type": "text","text": icon,"size": "xxl","align": "center"})
    header_content.append({"type": "text","text": title,"size": "xxl","weight": "bold","color": colors["primary"],"align": "center","margin": "xs" if icon else "none"})
    if subtitle:
        header_content.append({"type": "text","text": subtitle,"size": "sm","color": colors["text2"],"align": "center","margin": "xs"})
    return header_content

def create_glass_card(colors, icon, title, description, highlight=False):
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {"type": "box","layout": "vertical","contents": [{"type": "text","text": icon,"size": "xl","align": "center","gravity": "center"}],"backgroundColor": colors["primary"] if highlight else colors["card"],"cornerRadius": "15px","width": "50px","height": "50px","justifyContent": "center","alignItems": "center"},
            {"type": "box","layout": "vertical","contents": [{"type": "text","text": title,"size": "md","weight": "bold","color": colors["text"]},{"type": "text","text": description,"size": "xs","color": colors["text2"],"wrap": True,"margin": "xs"}],"flex": 1,"spacing": "xs","paddingStart": "md"}
        ],
        "backgroundColor": colors["glass"],
        "cornerRadius": "20px",
        "paddingAll": "15px",
        "margin": "sm",
        "borderWidth": "2px" if highlight else "1px",
        "borderColor": colors["primary"] if highlight else colors["border"]
    }

def create_section_title(colors, title, icon=None):
    return {"type": "box","layout": "vertical","contents": [{"type": "text","text": f"{icon} {title}" if icon else title,"size": "lg","weight": "bold","color": colors["text"]},{"type": "separator","color": colors["primary"],"margin": "sm"}],"margin": "xl"}

def create_glass_button(label, text, color, icon=None, style="primary"):
    return {"type": "button","action": {"type": "message","label": label,"text": text},"style": style,"height": "sm","color": color}

def create_button_grid(buttons, columns=2):
    rows = []
    for i in range(0, len(buttons), columns):
        rows.append({"type": "box","layout": "horizontal","spacing": "sm","contents": buttons[i:i+columns],"margin": "sm"})
    return rows

# ============================================================================
# نافذة البداية (HOME)
# ============================================================================

def build_enhanced_home(username, points, is_registered, theme="أبيض"):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])

    header = create_glass_header(colors,"Bot Mesh","منصة الألعاب الذكية","🎮")

    body = [
        create_section_title(colors, "طرق اللعب", "🎯"),

        create_glass_card(colors,"👤","وضع فردي","العب مباشرة بدون إعداد فرق",True),
        create_glass_card(colors,"👥","وضع مجموعة","استعمل زر فريقين ثم انضم ليتم التقسيم تلقائياً"),

        create_section_title(colors, "أزرار سريعة", "⚡")
    ]

    buttons = [
        create_glass_button("🎯 الألعاب", "ألعاب", colors["primary"]),
        create_glass_button("✅ انضم", "انضم", colors["success"]),
        create_glass_button("🏠 البداية", "home", colors["secondary"]),
        create_glass_button("❓ المساعدة", "مساعدة", colors["secondary"])
    ]

    body.extend(create_button_grid(buttons, 2))

    bubble = {
        "type": "bubble",
        "body": {"type": "box","layout": "vertical","contents": header + body},
        "footer": {"type": "box","layout": "vertical","contents": [{"type": "text","text": BOT_RIGHTS}]}
    }

    return FlexMessage(alt_text="🏠 البداية", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# نافذة المساعدة (HELP) — وضع فردي + وضع مجموعة (فريقين فقط)
# ============================================================================

def build_help_window(theme="أبيض"):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])

    header = create_glass_header(colors,"دليل الاستخدام","فردي + مجموعة (فريقين)","📚")

    body = [
        create_section_title(colors, "الوضع الفردي", "👤"),
        create_glass_card(colors,"🎮","طريقة اللعب","اختر لعبة وابدأ مباشرة"),

        create_section_title(colors, "وضع المجموعة (فريقين)", "👥"),
        create_glass_card(colors,"⚔️","بدء المنافسة","اضغط زر فريقين"),
        create_glass_card(colors,"✅","الانضمام","اللاعبون يكتبون: انضم"),
        create_glass_card(colors,"🔀","التقسيم","البوت يقسمهم تلقائياً"),
        create_glass_card(colors,"🏁","المنافسة","تبدأ مباشرة بدون لمح أو جاوب"),

        create_section_title(colors, "أوامر مسموحة", "⌨️"),
        create_glass_card(colors,"✅","انضم","المشاركة"),
        create_glass_card(colors,"❌","انسحب","الخروج من الجولة"),
        create_glass_card(colors,"⛔","إيقاف","إيقاف اللعبة")
    ]

    bubble = {
        "type": "bubble",
        "body": {"type": "box","layout": "vertical","contents": header + body},
        "footer": {"type": "box","layout": "vertical","contents": [{"type": "text","text": BOT_RIGHTS}]}
    }

    return FlexMessage(alt_text="📚 المساعدة", contents=FlexContainer.from_dict(bubble))

# ============================================================================
# الدوال الأخرى تبقى كما هي دون حذف:
# build_games_menu
# build_my_points
# build_leaderboard
# build_registration_required
# build_winner_announcement
# build_theme_selector
# build_percentage_result
# ============================================================================
