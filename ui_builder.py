"""
ui_glass_flat.py
Bot Mesh - Flat + Glass Flex UI (LINE-compatible)
Created by: Abeer Aldosari © 2025
وصف: مجموعة دوال لبناء نوافذ فلكس زجاجية/مسطحة متوافقة مع LINE Messaging API v3
ملاحظة: لا تضع "backgroundColor" داخل body مباشرةً (تسبب خطأ). استخدم bubble["styles"]["body"]["backgroundColor"] بدلاً من ذلك.
"""

from typing import List, Tuple, Dict, Any, Optional
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage

# استورد ثيمات / ثوابت من ملف constants لديك (أو ضف هنا مباشرة إذا تبي)
try:
    from constants import BOT_NAME, BOT_VERSION, BOT_RIGHTS, GAME_LIST, DEFAULT_THEME
except Exception:
    BOT_NAME = "Bot Mesh"
    BOT_VERSION = "v1"
    BOT_RIGHTS = "© 2025 Abeer Aldosari - All Rights Reserved"
    # GAME_LIST: قائمة ألعاب بصيغة [(id, display_name, icon), ...]
    GAME_LIST = [
        ("id_guess", "تخمين", "🔮"),
        ("id_song", "أغنية", "🎵"),
        ("id_scramble", "كلمة مبعثرة", "🔤"),
        ("id_opposite", "أضداد", "⚖️"),
        ("id_fast", "أسرع", "⚡"),
        ("id_logic", "ذكاء", "🧠"),
    ]
    DEFAULT_THEME = "رمادي"

# ------------------------------------------------------------------
# ثيمات مسطحة مع لمسة زجاجية
# ------------------------------------------------------------------
FLAT_THEMES: Dict[str, Dict[str, str]] = {
    "رمادي": {
        "bg": "#F0F4F8",
        "card": "#FFFFFF",
        "primary": "#5B6B7A",
        "accent": "#6B7C93",
        "text": "#233040",
        "muted": "#7F8C93",
        "faint": "#E9EEF3",
        "success": "#27AE60",
        "error": "#E74C3C",
        "border": "#E0E6EB"
    },
    "أزرق": {
        "bg": "#EBF5FB",
        "card": "#FFFFFF",
        "primary": "#2E86DE",
        "accent": "#54A0FF",
        "text": "#12385A",
        "muted": "#5DADE2",
        "faint": "#DFF3FF",
        "success": "#27AE60",
        "error": "#E74C3C",
        "border": "#AED6F1"
    },
    # يمكنك إضافة ثيمات أخرى
}

def get_theme(name: str = DEFAULT_THEME) -> Dict[str, str]:
    return FLAT_THEMES.get(name, FLAT_THEMES["رمادي"])

# ------------------------------------------------------------------
# Quick Reply (ثابت للأسفل)
# ------------------------------------------------------------------
def create_games_quick_reply(limit: int = 12) -> QuickReply:
    try:
        items = []
        for _, display_name, icon in GAME_LIST[:limit]:
            items.append(QuickReplyItem(
                action=MessageAction(label=f"{icon} {display_name}", text=display_name)
            ))
        return QuickReply(items=items)
    except Exception:
        return QuickReply(items=[])

def attach_quick_reply_to_flex(flex: FlexMessage) -> FlexMessage:
    try:
        # بعض إصدارات SDK تسمح بإضافة quick_reply على FlexMessage مباشرة
        setattr(flex, "quick_reply", create_games_quick_reply())
    except Exception:
        pass
    return flex

# ------------------------------------------------------------------
# Utilities: أزرار سفلية ثابتة (التي تطلبتها)
# ------------------------------------------------------------------
def _bottom_fixed_buttons(colors: Dict[str, str]) -> Dict[str, Any]:
    # تصميم شبيه بالصورة: صفين أزرار ثابتة في الأسفل
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "الألعاب  🎮", "text": "ألعاب"},
                        "style": "primary",
                        "color": colors["accent"],
                        "height": "sm",
                        "flex": 1
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "نقاطي  ⭐", "text": "نقاطي"},
                        "style": "secondary",
                        "height": "sm",
                        "flex": 1
                    }
                ],
                "margin": "sm"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "الصدارة  🏆", "text": "صدارة"},
                        "style": "link",
                        "height": "sm",
                        "flex": 1
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "مساعدة ❓", "text": "مساعدة"},
                        "style": "link",
                        "height": "sm",
                        "flex": 1
                    }
                ],
                "margin": "sm"
            }
        ],
        "spacing": "sm",
        "margin": "xl"
    }

# ------------------------------------------------------------------
# شاشة البداية (Home)
# ------------------------------------------------------------------
def build_home(username: str, points: int, is_registered: bool, theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = get_theme(theme)
    status_text = "✅ مسجل" if is_registered else "⚪ غير مسجل"
    status_color = colors["success"] if is_registered else colors["muted"]

    contents: List[Dict[str, Any]] = []

    # Header
    contents.append({
        "type": "text",
        "text": f"🎮 {BOT_NAME}",
        "size": "xxl",
        "weight": "bold",
        "color": colors["primary"],
        "align": "center"
    })

    # Card (points/status) — NOTE: لا تضيف backgroundColor داخل body مباشرة
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": f"نقطة | {status_text}", "size": "sm", "color": status_color, "align": "center"},
            {"type": "text", "text": str(points), "size": "lg", "weight": "bold", "color": colors["text"], "align": "center", "margin": "sm"}
        ],
        "cornerRadius": "12px",
        "paddingAll": "18px",
        "margin": "lg",
        "backgroundColor": colors["card"]
    })

    # Theme selector grid (مبسط)
    contents.append({
        "type": "text",
        "text": "🎨 اختر الثيم",
        "size": "sm",
        "color": colors["muted"],
        "margin": "md"
    })

    theme_names = list(get_theme().keys()) if False else ["رمادي", "أزرق", "أبيض", "وردي"]
    # عرض مبسط لثيمات كأزرار
    row = {"type": "box", "layout": "horizontal", "contents": [], "spacing": "sm", "margin": "md"}
    for name in theme_names[:3]:
        row["contents"].append({
            "type": "button",
            "action": {"type": "message", "label": name, "text": f"ثيم {name}"},
            "style": "secondary",
            "height": "sm",
            "flex": 1
        })
    contents.append(row)

    # Main action buttons (بزرار زجاجي)
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "button",
                "action": {"type": "message", "label": "انضم ✅", "text": "انضم"},
                "style": "primary",
                "height": "sm",
                "color": colors["accent"]
            },
            {
                "type": "button",
                "action": {"type": "message", "label": "انسحب ❌", "text": "انسحب"},
                "style": "secondary",
                "height": "sm",
                "margin": "sm"
            }
        ],
        "margin": "lg"
    })

    # bottom fixed buttons (مطلوب)
    contents.append(_bottom_fixed_buttons(colors))

    # Footer rights
    contents.append({
        "type": "text",
        "text": BOT_RIGHTS,
        "size": "xxs",
        "color": colors["muted"],
        "align": "center",
        "margin": "md",
        "wrap": True
    })

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "paddingAll": "18px"
        },
        # ضع لون الخلفية عبر styles (متوافق مع API)
        "styles": {"body": {"backgroundColor": colors["bg"]}}
    }

    flex = FlexMessage(alt_text="الصفحة الرئيسية", contents=FlexContainer.from_dict(bubble))
    return attach_quick_reply_to_flex(flex)

# ------------------------------------------------------------------
# قائمة الألعاب (شبكة)
# ------------------------------------------------------------------
def build_games_menu(theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = get_theme(theme)
    contents: List[Dict[str, Any]] = []

    contents.append({
        "type": "text",
        "text": "🎮 الألعاب المتاحة",
        "size": "xl",
        "weight": "bold",
        "color": colors["primary"],
        "align": "center"
    })

    # separator
    contents.append({"type": "separator", "margin": "lg"})

    # grid: 3 أعمدة
    per_row = 3
    for i in range(0, len(GAME_LIST), per_row):
        row = {"type": "box", "layout": "horizontal", "contents": [], "spacing": "sm", "margin": "md"}
        for j in range(i, min(i + per_row, len(GAME_LIST))):
            _, name, icon = GAME_LIST[j]
            row["contents"].append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": icon, "size": "xxl", "align": "center"},
                    {"type": "text", "text": name, "size": "sm", "align": "center", "margin": "sm"}
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "action": {"type": "message", "text": name},
                "flex": 1
            })
        contents.append(row)

    # help box
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": "💡 أوامر اللعبة:", "weight": "bold"},
            {"type": "text", "text": "اكتب 'لمح' للتلميح • اكتب 'جاوب' لكشف الإجابة • اكتب 'إيقاف' لإنهاء", "size": "xs", "color": colors["muted"], "wrap": True, "margin": "sm"}
        ],
        "backgroundColor": colors["faint"],
        "cornerRadius": "12px",
        "paddingAll": "12px",
        "margin": "lg"
    })

    # bottom buttons
    contents.append({
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {"type": "button", "action": {"type": "message", "label": "إيقاف ⛔", "text": "إيقاف"}, "style": "secondary", "height": "sm", "flex": 1},
            {"type": "button", "action": {"type": "message", "label": "البداية 🏠", "text": "بداية"}, "style": "primary", "height": "sm", "flex": 1, "color": colors["accent"]}
        ],
        "spacing": "sm",
        "margin": "lg"
    })

    bubble = {
        "type": "bubble",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "18px"},
        "styles": {"body": {"backgroundColor": colors["bg"]}}
    }
    flex = FlexMessage(alt_text="قائمة الألعاب", contents=FlexContainer.from_dict(bubble))
    return attach_quick_reply_to_flex(flex)

# ------------------------------------------------------------------
# شاشة أثناء اللعب (قالب زجاجي) — تستخدم لبناء أي لعبة
# params:
#   title, subtitle, main_content (list), hint_buttons (bool)
# ------------------------------------------------------------------
def build_in_game_screen(
    title: str,
    subtitle: Optional[str],
    main_content: List[Dict[str, Any]],
    hint_buttons: bool,
    theme: str = DEFAULT_THEME
) -> FlexMessage:
    colors = get_theme(theme)
    contents: List[Dict[str, Any]] = []

    # Header
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": title, "size": "xl", "weight": "bold", "color": colors["primary"], "align": "start"},
            {"type": "text", "text": subtitle or "", "size": "xs", "color": colors["muted"], "align": "start", "margin": "sm"}
        ]
    })

    contents.append({"type": "separator", "margin": "md"})

    # main content (سؤال / كلمات / قائمة)
    contents.extend(main_content)

    # hint buttons (لمح / جاوب)
    if hint_buttons:
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {"type": "button", "action": {"type": "message", "label": "لمح 💡", "text": "لمح"}, "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "جاوب 🔍", "text": "جاوب"}, "style": "secondary", "height": "sm", "flex": 1}
            ],
            "margin": "md"
        })

    # stop button big
    contents.append({
        "type": "button",
        "action": {"type": "message", "label": "إيقاف ⛔", "text": "إيقاف"},
        "style": "primary",
        "color": colors["error"],
        "height": "sm",
        "margin": "lg"
    })

    # fixed bottom nav
    contents.append(_bottom_fixed_buttons(colors))

    bubble = {
        "type": "bubble",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "18px"},
        "styles": {"body": {"backgroundColor": colors["bg"]}}
    }
    return FlexMessage(alt_text=title, contents=FlexContainer.from_dict(bubble))

# ------------------------------------------------------------------
# شاشة السؤال لعناصر (مثال: لعبة أغنية تعرض كلمات)
# ------------------------------------------------------------------
def build_song_question(lyrics: str, round_info: str, theme: str = DEFAULT_THEME) -> FlexMessage:
    # main_content مبني حسب التصميم الموجود بالصور
    colors = get_theme(theme)
    main = [
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": lyrics, "size": "md", "weight": "bold", "align": "center"},
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "12px",
            "paddingAll": "14px",
            "margin": "md"
        },
        {"type": "text", "text": round_info, "size": "xs", "color": colors["muted"], "align": "center", "margin": "md"}
    ]
    return build_in_game_screen("أغنية 🎵", "من المغني؟", main, hint_buttons=True, theme=theme)

# ------------------------------------------------------------------
# شاشة فوز / نهاية اللعبة
# ------------------------------------------------------------------
def build_result_screen(username: str, points_gained: int, total_points: int, theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = get_theme(theme)
    contents: List[Dict[str, Any]] = []

    contents.append({
        "type": "text",
        "text": "🎉 تهانينا!",
        "size": "xxl",
        "weight": "bold",
        "color": colors["primary"],
        "align": "center"
    })
    contents.append({"type": "text", "text": "أنهيت اللعبة", "size": "sm", "color": colors["muted"], "align": "center", "margin": "md"})

    contents.append({"type": "separator", "margin": "lg"})

    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": username, "size": "md", "align": "center", "margin": "md"},
            {"type": "text", "text": f"+{points_gained}", "size": "xxl", "weight": "bold", "color": colors["success"], "align": "center", "margin": "md"},
            {"type": "text", "text": f"الإجمالي: {total_points}", "size": "sm", "color": colors["muted"], "align": "center", "margin": "md"}
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "12px",
        "paddingAll": "16px",
        "margin": "lg"
    })

    # actions: replay / games / home
    contents.append({
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "button", "action": {"type": "message", "label": "إعادة نفس اللعبة 🔁", "text": "إعادة"}, "style": "primary", "height": "sm"},
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "button", "action": {"type": "message", "label": "الألعاب 🎮", "text": "ألعاب"}, "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message", "label": "البداية 🏠", "text": "بداية"}, "style": "secondary", "height": "sm", "flex": 1}
            ], "spacing": "sm", "margin": "md"}
        ],
        "margin": "md"
    })

    contents.append(_bottom_fixed_buttons(colors))

    bubble = {
        "type": "bubble",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "18px"},
        "styles": {"body": {"backgroundColor": colors["bg"]}}
    }
    return FlexMessage(alt_text="نتيجة اللعبة", contents=FlexContainer.from_dict(bubble))

# ------------------------------------------------------------------
# نافذة المساعدة
# ------------------------------------------------------------------
def build_help(theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = get_theme(theme)
    contents = [
        {"type": "text", "text": "❓ مساعدة", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "start"},
        {"type": "separator", "margin": "md"},
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "• اضغط على اسم اللعبة لبدء", "size": "sm", "color": colors["muted"], "margin": "sm"},
                {"type": "text", "text": "• اكتب 'لمح' للتلميح", "size": "sm", "color": colors["muted"], "margin": "sm"},
                {"type": "text", "text": "• اكتب 'جاوب' لكشف الإجابة", "size": "sm", "color": colors["muted"], "margin": "sm"},
                {"type": "text", "text": "• اكتب 'إيقاف' لإنهاء اللعبة", "size": "sm", "color": colors["muted"], "margin": "sm"}
            ],
            "backgroundColor": colors["card"],
            "cornerRadius": "12px",
            "paddingAll": "12px",
            "margin": "md"
        }
    ]
    contents.append(_bottom_fixed_buttons(colors))
    bubble = {
        "type": "bubble",
        "body": {"type": "box", "layout": "vertical", "contents": contents, "paddingAll": "18px"},
        "styles": {"body": {"backgroundColor": colors["bg"]}}
    }
    return FlexMessage(alt_text="مساعدة", contents=FlexContainer.from_dict(bubble))

# ------------------------------------------------------------------
# أمثلة سريعة للاستخدام (تعطيك فكرة)
# ------------------------------------------------------------------
if __name__ == "__main__":
    # مثال: طباعة هيكل JSON لفلكس الشاشة الرئيسية (للتجريب محلياً)
    import json
    f = build_home("اسم المستخدم", 90, True, theme="رمادي")
    print(json.dumps(f.contents.to_dict(), ensure_ascii=False, indent=2))
