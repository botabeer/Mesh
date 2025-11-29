from typing import List, Dict

from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    MessageAction
)

from constants import (
    BOT_NAME,
    BOT_VERSION,
    BOT_RIGHTS,
    THEMES,
    DEFAULT_THEME,
    GAME_LIST,
    get_theme_colors
)

# ============================================================================
# Utility Functions
# ============================================================================

def _safe_get_colors(theme: str) -> Dict[str, str]:
    """الحصول على الألوان بأمان"""
    try:
        return get_theme_colors(theme)
    except Exception:
        return get_theme_colors(DEFAULT_THEME)


# ============================================================================
# Quick Reply System - الألعاب فقط
# ============================================================================

def create_games_quick_reply() -> QuickReply:
    """إنشاء Quick Reply للألعاب فقط"""
    try:
        items = []
        for game_data in GAME_LIST:
            if len(game_data) >= 3:
                _, display_name, icon = game_data[:3]
                items.append(
                    QuickReplyItem(
                        action=MessageAction(
                            label=f"{icon} {display_name}",
                            text=display_name
                        )
                    )
                )
        return QuickReply(items=items[:13])
    except Exception:
        return QuickReply(items=[])


def attach_quick_reply(message):
    """إضافة Quick Reply للرسالة (alias)"""
    try:
        qr = create_games_quick_reply()
        message.quick_reply = qr
    except Exception:
        pass
    return message


# ============================================================================
# Main UI Screens
# ============================================================================

def build_enhanced_home(username: str, points: int, is_registered: bool, theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏠 نافذة البداية الرئيسية"""
    colors = _safe_get_colors(theme)

    buttons = [
        {
            "type": "button",
            "action": {"type": "message", "label": "🎮 الألعاب", "text": "ألعاب"},
            "style": "primary",
            "height": "sm",
            "margin": "md"
        },
        {
            "type": "button",
            "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"},
            "style": "link",
            "height": "sm",
            "margin": "sm"
        },
        {
            "type": "button",
            "action": {"type": "message", "label": "🏆 الصدارة", "text": "صدارة"},
            "style": "link",
            "height": "sm",
            "margin": "sm"
        },
        {
            "type": "button",
            "action": {"type": "message", "label": "❓ مساعدة", "text": "مساعدة"},
            "style": "link",
            "height": "sm",
            "margin": "sm"
        }
    ]

    if not is_registered:
        buttons.insert(1, {
            "type": "button",
            "action": {"type": "message", "label": "✅ انضم", "text": "انضم"},
            "style": "primary",
            "height": "sm",
            "margin": "sm"
        })

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"مرحباً {username}", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center"},
                {"type": "text", "text": f"النقاط: {points}", "size": "sm", "color": colors["text2"], "align": "center", "margin": "sm"},
                {"type": "separator", "margin": "lg"}
            ] + buttons + [
                {"type": "separator", "margin": "lg"},
                {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": colors["text2"], "align": "center", "margin": "md"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🏠 البداية", contents=FlexContainer.from_dict(bubble))


def build_games_menu(theme: str = DEFAULT_THEME) -> FlexMessage:
    """🎮 نافذة قائمة الألعاب"""
    colors = _safe_get_colors(theme)

    buttons = []
    for _, display_name, icon in GAME_LIST:
        buttons.append({
            "type": "button",
            "action": {"type": "message", "label": f"{icon} {display_name}", "text": display_name},
            "style": "link",
            "height": "sm",
            "margin": "sm"
        })

    buttons.extend([
        {"type": "separator", "margin": "lg"},
        {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "height": "sm", "margin": "md"}
    ])

    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎮 الألعاب", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center"},
                {"type": "separator", "margin": "md"}
            ] + buttons,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🎮 الألعاب", contents=FlexContainer.from_dict(bubble))


def build_my_points(username: str, total_points: int, stats: Dict, theme: str = DEFAULT_THEME) -> FlexMessage:
    """⭐ نافذة النقاط"""
    colors = _safe_get_colors(theme)

    contents = [
        {"type": "text", "text": "⭐ نقاطي", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center"},
        {"type": "separator", "margin": "md"},
        {"type": "text", "text": f"اللاعب: {username}", "size": "md", "margin": "md", "color": colors["text"]},
        {"type": "text", "text": f"النقاط: {total_points}", "size": "lg", "weight": "bold", "margin": "sm", "color": colors["success"]}
    ]

    if stats:
        contents.append({"type": "separator", "margin": "lg"})
        contents.append({"type": "text", "text": "📊 الإحصائيات:", "weight": "bold", "margin": "md", "color": colors["text"]})
        for game_name, data in list(stats.items())[:5]:
            contents.append({
                "type": "text",
                "text": f"• {game_name}: {data.get('plays', 0)} لعبة",
                "size": "sm",
                "margin": "xs",
                "color": colors["text2"],
                "wrap": True
            })

    contents.extend([
        {"type": "separator", "margin": "lg"},
        {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "height": "sm", "margin": "md"}
    ])

    bubble = {"type": "bubble", "size": "kilo", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px"}}
    return FlexMessage(alt_text="⭐ نقاطي", contents=FlexContainer.from_dict(bubble))


def build_leaderboard(top_users: List, theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏆 نافذة الصدارة"""
    colors = _safe_get_colors(theme)

    contents = [
        {"type": "text", "text": "🏆 الصدارة", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center"},
        {"type": "separator", "margin": "md"}
    ]

    medals = ["🥇", "🥈", "🥉"]
    for i, (name, pts) in enumerate(top_users[:10]):
        medal = medals[i] if i < 3 else f"{i+1}."
        contents.append({
            "type": "text",
            "text": f"{medal} {name} - {pts}",
            "size": "md" if i < 3 else "sm",
            "margin": "sm",
            "weight": "bold" if i < 3 else "regular",
            "color": colors["primary"] if i < 3 else colors["text"]
        })

    contents.extend([
        {"type": "separator", "margin": "lg"},
        {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "height": "sm", "margin": "md"}
    ])

    bubble = {"type": "bubble", "size": "kilo", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px"}}
    return FlexMessage(alt_text="🏆 الصدارة", contents=FlexContainer.from_dict(bubble))


def build_theme_selector(current_theme: str = DEFAULT_THEME) -> FlexMessage:
    """🎨 نافذة اختيار الثيم"""
    colors = _safe_get_colors(current_theme)

    buttons = []
    for name in THEMES.keys():
        marker = "✓ " if name == current_theme else ""
        buttons.append({
            "type": "button",
            "action": {"type": "message", "label": f"{marker}{name}", "text": f"ثيم {name}"},
            "style": "primary" if name == current_theme else "link",
            "height": "sm",
            "margin": "sm"
        })

    buttons.extend([
        {"type": "separator", "margin": "lg"},
        {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "height": "sm", "margin": "md"}
    ])

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎨 الثيمات", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center"},
                {"type": "separator", "margin": "md"}
            ] + buttons,
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🎨 الثيمات", contents=FlexContainer.from_dict(bubble))


def build_registration_required(theme: str = DEFAULT_THEME) -> FlexMessage:
    """⚠️ نافذة التسجيل المطلوب"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "⚠️", "size": "xxl", "align": "center", "color": colors["warning"]},
                {"type": "text", "text": "يجب التسجيل", "weight": "bold", "size": "lg", "align": "center", "margin": "md", "color": colors["text"]},
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "✅ انضم", "text": "انضم"}, "style": "primary", "margin": "md", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "margin": "sm", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="⚠️ التسجيل", contents=FlexContainer.from_dict(bubble))


def build_winner_announcement(username: str, game_name: str, points: int, total_points: int, theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏆 نافذة الفائز"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🏆", "size": "xxl", "align": "center", "color": colors["primary"]},
                {"type": "text", "text": "الفائز", "weight": "bold", "size": "xl", "align": "center", "margin": "sm", "color": colors["primary"]},
                {"type": "separator", "margin": "lg"},
                {"type": "text", "text": username, "size": "lg", "weight": "bold", "align": "center", "margin": "md", "color": colors["text"]},
                {"type": "text", "text": f"+{points} نقطة", "size": "md", "align": "center", "margin": "sm", "color": colors["success"]},
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "🎮 ألعاب", "text": "ألعاب"}, "style": "primary", "margin": "md", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "margin": "sm", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🏆 الفائز", contents=FlexContainer.from_dict(bubble))


def build_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """❓ نافذة المساعدة"""
    colors = _safe_get_colors(theme)

    commands = [
        "🏠 بداية - العودة للصفحة الرئيسية",
        "🎮 ألعاب - عرض قائمة الألعاب",
        "⭐ نقاطي - عرض نقاطك",
        "🏆 صدارة - أفضل اللاعبين",
        "✅ انضم - التسجيل",
        "⛔ إيقاف - إيقاف اللعبة"
    ]

    contents = [
        {"type": "text", "text": "❓ المساعدة", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center"},
        {"type": "separator", "margin": "md"}
    ]

    for cmd in commands:
        contents.append({"type": "text", "text": cmd, "size": "sm", "margin": "sm", "color": colors["text"], "wrap": True})

    contents.extend([
        {"type": "separator", "margin": "lg"},
        {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "height": "sm", "margin": "md"}
    ])

    bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "20px"}}
    return FlexMessage(alt_text="❓ مساعدة", contents=FlexContainer.from_dict(bubble))


def build_multiplayer_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """👥 نافذة الفريقين"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "👥 فريقين", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center"},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": "1. اكتب: انضم", "size": "md", "margin": "md", "color": colors["text"]},
                {"type": "text", "text": "2. اختر اللعبة", "size": "md", "margin": "sm", "color": colors["text"]},
                {"type": "separator", "margin": "lg"},
                {"type": "button", "action": {"type": "message", "label": "🎮 اختر اللعبة", "text": "ألعاب"}, "style": "primary", "margin": "md", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="👥 فريقين", contents=FlexContainer.from_dict(bubble))


def build_join_confirmation(username: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """✅ تأكيد الانضمام"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "✅", "size": "xxl", "align": "center", "color": colors["success"]},
                {"type": "text", "text": "تم الانضمام", "weight": "bold", "size": "xl", "align": "center", "margin": "sm", "color": colors["text"]},
                {"type": "text", "text": f"{username} انضم", "size": "md", "align": "center", "margin": "md", "color": colors["text2"]},
                {"type": "button", "action": {"type": "message", "label": "🎮 الألعاب", "text": "ألعاب"}, "style": "primary", "margin": "lg", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="✅ انضمام", contents=FlexContainer.from_dict(bubble))


def build_registration_success(username: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """✅ نجاح التسجيل"""
    return build_join_confirmation(username, theme)


def build_theme_change_success(theme_name: str, current_theme: str = DEFAULT_THEME) -> FlexMessage:
    """🎨 تغيير الثيم"""
    colors = _safe_get_colors(theme_name)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🎨", "size": "xxl", "align": "center", "color": colors["primary"]},
                {"type": "text", "text": "تم التغيير", "weight": "bold", "size": "xl", "align": "center", "margin": "sm", "color": colors["text"]},
                {"type": "text", "text": f"الثيم: {theme_name}", "size": "md", "align": "center", "margin": "md", "color": colors["text2"]},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "primary", "margin": "lg", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🎨 الثيم", contents=FlexContainer.from_dict(bubble))


def build_error_message(error_text: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """❌ رسالة خطأ"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "❌", "size": "xxl", "align": "center", "color": colors["error"]},
                {"type": "text", "text": error_text, "size": "lg", "align": "center", "margin": "md", "color": colors["text"], "wrap": True},
                {"type": "button", "action": {"type": "message", "label": "🏠 الرئيسية", "text": "بداية"}, "style": "link", "margin": "lg", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="❌ خطأ", contents=FlexContainer.from_dict(bubble))


def build_game_stopped(game_name: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """⛔ إيقاف اللعبة"""
    colors = _safe_get_colors(theme)

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "⛔", "size": "xxl", "align": "center", "color": colors["error"]},
                {"type": "text", "text": "تم الإيقاف", "weight": "bold", "size": "xl", "align": "center", "margin": "sm", "color": colors["text"]},
                {"type": "text", "text": game_name, "size": "md", "align": "center", "margin": "md", "color": colors["text2"]},
                {"type": "button", "action": {"type": "message", "label": "🎮 ألعاب", "text": "ألعاب"}, "style": "primary", "margin": "lg", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="⛔ إيقاف", contents=FlexContainer.from_dict(bubble))


def build_team_game_end(team_points: Dict, theme: str = DEFAULT_THEME) -> FlexMessage:
    """🏆 نهاية الفريقين"""
    colors = _safe_get_colors(theme)

    t1 = team_points.get("team1", 0)
    t2 = team_points.get("team2", 0)
    winner = "الفريق الأول 🥇" if t1 > t2 else ("الفريق الثاني 🥈" if t2 > t1 else "تعادل ⚖️")

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🏆", "size": "xxl", "align": "center", "color": colors["primary"]},
                {"type": "text", "text": "انتهت اللعبة", "weight": "bold", "size": "xl", "align": "center", "margin": "sm", "color": colors["primary"]},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": f"الفريق الأول: {t1}", "size": "md", "align": "center", "margin": "sm", "color": colors["text"]},
                {"type": "text", "text": f"الفريق الثاني: {t2}", "size": "md", "align": "center", "margin": "xs", "color": colors["text"]},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": f"الفائز: {winner}", "size": "lg", "weight": "bold", "align": "center", "margin": "md", "color": colors["success"]},
                {"type": "button", "action": {"type": "message", "label": "🎮 لعب مرة أخرى", "text": "ألعاب"}, "style": "primary", "margin": "lg", "height": "sm"}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text="🏆 نهاية", contents=FlexContainer.from_dict(bubble))


def build_answer_feedback(message: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    """💬 رد الإجابة"""
    colors = _safe_get_colors(theme)
    icon = "✅" if "✅" in message or "صحيح" in message else ("❌" if "❌" in message or "خطأ" in message else "💬")
    color = colors["success"] if icon == "✅" else (colors["error"] if icon == "❌" else colors["primary"])

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": icon, "size": "xxl", "align": "center", "color": color},
                {"type": "text", "text": message, "size": "md", "align": "center", "margin": "md", "color": colors["text"], "wrap": True}
            ],
            "paddingAll": "20px"
        }
    }

    return FlexMessage(alt_text=message, contents=FlexContainer.from_dict(bubble))


# ============================================================================
# Export
# ============================================================================

__all__ = [
    "build_enhanced_home",
    "build_games_menu",
    "build_my_points",
    "build_leaderboard",
    "build_theme_selector",
    "build_registration_required",
    "build_winner_announcement",
    "build_help_window",
    "build_multiplayer_help_window",
    "build_join_confirmation",
    "build_registration_success",
    "build_theme_change_success",
    "build_error_message",
    "build_game_stopped",
    "build_team_game_end",
    "build_answer_feedback",
    "attach_quick_reply",
    "create_games_quick_reply"
]
