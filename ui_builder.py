“””
Bot Mesh - UI Builder v8.5 COMPLETE FIXED
Created by: Abeer Aldosari © 2025
✅ واجهات زجاجية احترافية
✅ Quick Reply للألعاب فقط
✅ متوافق 100% مع آلية البوت
✅ معالجة أخطاء محسّنة
✅ دعم جميع الثيمات
✅ إصلاح جميع مشاكل color في separators
“””

import traceback
from typing import List, Optional, Dict, Any, Tuple

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
“”“الحصول على الألوان بأمان”””
try:
return get_theme_colors(theme)
except Exception:
return get_theme_colors(DEFAULT_THEME)

def create_debug_report(exc: Exception, context: Optional[Dict[str, Any]] = None) -> TextMessage:
“”“إنشاء تقرير خطأ مفصل”””
try:
tb = traceback.format_exc()
ctx_lines = []
if context:
for k, v in context.items():
ctx_lines.append(f”{k}: {str(v)[:100]}”)

```
    ctx_text = "\n".join(ctx_lines) if ctx_lines else "لا توجد معلومات إضافية"
    
    text = (
        "⚠️ تقرير خطأ\n\n"
        f"الخطأ: {str(exc)[:200]}\n\n"
        f"التفاصيل:\n{tb[:800]}\n\n"
        f"السياق:\n{ctx_text}"
    )
    
    if len(text) > 1800:
        text = text[:900] + "\n\n...[مقتطع]...\n\n" + text[-800:]
    
    return TextMessage(text=text)
except Exception:
    return TextMessage(text="⚠️ حدث خطأ غير متوقع")
```

# ============================================================================

# Quick Reply System

# ============================================================================

def create_games_quick_reply() -> QuickReply:
“”“إنشاء Quick Reply للألعاب”””
try:
items = []
for game_data in GAME_LIST:
if len(game_data) >= 3:
_, display_name, icon = game_data[:3]
items.append(
QuickReplyItem(
action=MessageAction(
label=f”{icon} {display_name}”,
text=display_name
)
)
)
return QuickReply(items=items[:13])
except Exception:
return QuickReply(items=[])

def attach_quick_reply_to_message(message):
“”“إضافة Quick Reply للرسالة”””
try:
qr = create_games_quick_reply()
if hasattr(message, ‘quick_reply’):
message.quick_reply = qr
else:
setattr(message, ‘quick_reply’, qr)
except Exception:
pass
return message

# ============================================================================

# Glass Components

# ============================================================================

def create_glass_header(colors: Dict, title: str, subtitle: str = None, icon: str = None) -> List[Dict]:
“”“إنشاء Header زجاجي”””
header_content = []

```
if icon:
    header_content.append({
        "type": "text",
        "text": icon,
        "size": "xxl",
        "align": "center",
        "color": colors["primary"]
    })

header_content.append({
    "type": "text",
    "text": title,
    "size": "xxl",
    "weight": "bold",
    "color": colors["primary"],
    "align": "center",
    "margin": "sm" if icon else "none"
})

if subtitle:
    header_content.append({
        "type": "text",
        "text": subtitle,
        "size": "sm",
        "color": colors["text2"],
        "align": "center",
        "margin": "xs"
    })

header_content.append({
    "type": "separator",
    "margin": "lg"
})

return header_content
```

def create_glass_card(colors: Dict, icon: str, title: str, description: str, highlight: bool = False) -> Dict:
“”“إنشاء بطاقة زجاجية”””
return {
“type”: “box”,
“layout”: “horizontal”,
“contents”: [
{
“type”: “box”,
“layout”: “vertical”,
“contents”: [
{“type”: “text”, “text”: icon, “size”: “xl”, “align”: “center”, “color”: colors[“text”] if not highlight else “#FFFFFF”}
],
“backgroundColor”: colors[“primary”] if highlight else colors[“card”],
“cornerRadius”: “15px”,
“width”: “50px”,
“height”: “50px”,
“justifyContent”: “center”,
“alignItems”: “center”
},
{
“type”: “box”,
“layout”: “vertical”,
“contents”: [
{“type”: “text”, “text”: title, “size”: “md”, “weight”: “bold”, “color”: colors[“text”]},
{“type”: “text”, “text”: description, “size”: “xs”, “wrap”: True, “color”: colors[“text2”]}
],
“flex”: 1,
“paddingStart”: “md”,
“justifyContent”: “center”
}
],
“backgroundColor”: colors[“glass”],
“cornerRadius”: “20px”,
“paddingAll”: “15px”,
“margin”: “sm”
}

def create_glass_button(label: str, text_cmd: str, color: str, style: str = “primary”) -> Dict:
“”“إنشاء زر زجاجي”””
return {
“type”: “button”,
“action”: {“type”: “message”, “label”: label, “text”: text_cmd},
“style”: style,
“height”: “sm”,
“color”: color
}

def create_button_grid(buttons: List[Dict], columns: int = 2) -> List[Dict]:
“”“إنشاء شبكة أزرار”””
rows = []
for i in range(0, len(buttons), columns):
row_buttons = buttons[i:i+columns]
rows.append({
“type”: “box”,
“layout”: “horizontal”,
“spacing”: “sm”,
“contents”: row_buttons,
“margin”: “sm”
})
return rows

# ============================================================================

# Main UI Screens

# ============================================================================

def build_enhanced_home(username: str, points: int, is_registered: bool, theme: str = DEFAULT_THEME) -> FlexMessage:
“”“الصفحة الرئيسية المحسّنة”””
try:
colors = _safe_get_colors(theme)

```
    header = create_glass_header(
        colors, f"مرحباً {username}", f"النقاط: {points}", "🎮"
    )

    cards = [
        create_glass_card(colors, "🎮", "الألعاب", "اختر لعبتك المفضلة"),
        create_glass_card(colors, "⭐", "نقاطي", f"لديك {points} نقطة"),
        create_glass_card(colors, "🏆", "الصدارة", "أفضل اللاعبين"),
        create_glass_card(colors, "🎨", "الثيمات", "غيّر المظهر"),
    ]

    buttons = create_button_grid([
        create_glass_button("🎮 ألعاب", "ألعاب", colors["primary"]),
        create_glass_button("⭐ نقاطي", "نقاطي", colors["primary"]),
        create_glass_button("🏆 صدارة", "صدارة", colors["secondary"]),
        create_glass_button("🎨 ثيمات", "ثيمات", colors["secondary"]),
    ])

    footer = [{
        "type": "text",
        "text": BOT_RIGHTS,
        "size": "xxs",
        "color": colors["text2"],
        "align": "center",
        "margin": "lg"
    }]

    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + cards + buttons + footer,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }

    flex_msg = FlexMessage(
        alt_text="الصفحة الرئيسية",
        contents=FlexContainer.from_dict(bubble)
    )

    return attach_quick_reply_to_message(flex_msg)

except Exception as e:
    return create_debug_report(e, {"username": username, "theme": theme})
```

def build_games_menu(theme: str = DEFAULT_THEME) -> FlexMessage:
“”“قائمة الألعاب”””
try:
colors = _safe_get_colors(theme)

```
    header = create_glass_header(colors, "🎮 الألعاب", "اختر لعبتك المفضلة")
    
    game_buttons = []
    for _, display_name, icon in GAME_LIST:
        game_buttons.append({
            "type": "button",
            "action": {"type": "message", "label": f"{icon} {display_name}", "text": display_name},
            "style": "secondary",
            "height": "sm",
            "margin": "xs"
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + game_buttons,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return FlexMessage(alt_text="قائمة الألعاب", contents=FlexContainer.from_dict(bubble))

except Exception as e:
    return create_debug_report(e, {"theme": theme})
```

def build_my_points(username: str, total_points: int, stats: Dict, theme: str = DEFAULT_THEME) -> FlexMessage:
“”“صفحة نقاطي”””
try:
colors = _safe_get_colors(theme)

```
    header = create_glass_header(colors, "⭐ نقاطي", f"{username}")
    
    total_box = {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": "مجموع النقاط", "size": "sm", "color": colors["text2"], "align": "center"},
            {"type": "text", "text": str(total_points), "size": "xxl", "weight": "bold", "color": colors["primary"], "align": "center"}
        ],
        "backgroundColor": colors["card"],
        "cornerRadius": "20px",
        "paddingAll": "20px",
        "margin": "md"
    }
    
    stats_section = [
        {"type": "text", "text": "📊 إحصائيات الألعاب", "weight": "bold", "margin": "lg", "color": colors["text"]}
    ]
    
    if stats:
        for game_name, game_stats in list(stats.items())[:5]:
            stats_section.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": game_name, "size": "sm", "flex": 2, "color": colors["text"]},
                    {"type": "text", "text": f"{game_stats.get('plays', 0)} لعبة", "size": "xs", "flex": 1, "align": "end", "color": colors["text2"]}
                ],
                "margin": "sm"
            })
    else:
        stats_section.append({
            "type": "text",
            "text": "لم تلعب بعد",
            "size": "sm",
            "color": colors["text2"],
            "align": "center",
            "margin": "md"
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + [total_box] + stats_section,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(bubble))

except Exception as e:
    return create_debug_report(e, {"username": username})
```

def build_leaderboard(top_users: List[Tuple[str, int]], theme: str = DEFAULT_THEME) -> FlexMessage:
“”“لوحة الصدارة”””
try:
colors = _safe_get_colors(theme)

```
    header = create_glass_header(colors, "🏆 لوحة الصدارة", "أفضل اللاعبين")
    
    leaderboard_items = []
    medals = ["🥇", "🥈", "🥉"]
    
    for i, (name, points) in enumerate(top_users[:10]):
        medal = medals[i] if i < 3 else f"{i+1}."
        
        leaderboard_items.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": medal, "size": "lg", "flex": 0, "color": colors["primary"]},
                {"type": "text", "text": name, "size": "md", "flex": 3, "color": colors["text"], "margin": "md"},
                {"type": "text", "text": f"{points}", "size": "md", "flex": 1, "align": "end", "weight": "bold", "color": colors["success"]}
            ],
            "backgroundColor": colors["glass"] if i < 3 else colors["bg"],
            "cornerRadius": "15px",
            "paddingAll": "12px",
            "margin": "sm"
        })
    
    if not top_users:
        leaderboard_items.append({
            "type": "text",
            "text": "لا يوجد لاعبون بعد",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + leaderboard_items,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return FlexMessage(alt_text="لوحة الصدارة", contents=FlexContainer.from_dict(bubble))

except Exception as e:
    return create_debug_report(e)
```

def build_theme_selector(current_theme: str = DEFAULT_THEME) -> FlexMessage:
“”“محدد الثيمات”””
try:
colors = _safe_get_colors(current_theme)

```
    header = create_glass_header(colors, "🎨 الثيمات", f"الحالي: {current_theme}")
    
    theme_buttons = []
    for theme_name in THEMES.keys():
        is_current = (theme_name == current_theme)
        theme_buttons.append({
            "type": "button",
            "action": {"type": "message", "label": f"{'✓ ' if is_current else ''}{theme_name}", "text": f"ثيم {theme_name}"},
            "style": "primary" if is_current else "secondary",
            "height": "sm",
            "margin": "xs"
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + theme_buttons,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return FlexMessage(alt_text="الثيمات", contents=FlexContainer.from_dict(bubble))

except Exception as e:
    return create_debug_report(e)
```

def build_registration_required(theme: str = DEFAULT_THEME) -> FlexMessage:
“”“رسالة التسجيل المطلوب”””
try:
colors = _safe_get_colors(theme)

```
    header = create_glass_header(colors, "⚠️ تنبيه", "التسجيل مطلوب")
    
    message = [
        {
            "type": "text",
            "text": "يجب الانضمام أولاً للعب",
            "size": "md",
            "color": colors["text"],
            "align": "center",
            "wrap": True,
            "margin": "lg"
        },
        {
            "type": "button",
            "action": {"type": "message", "label": "✅ انضم الآن", "text": "انضم"},
            "style": "primary",
            "color": colors["success"],
            "margin": "lg"
        }
    ]
    
    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + message,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return FlexMessage(alt_text="تسجيل مطلوب", contents=FlexContainer.from_dict(bubble))

except Exception as e:
    return create_debug_report(e)
```

def build_winner_announcement(username: str, game_name: str, points: int, total_points: int, theme: str = DEFAULT_THEME) -> FlexMessage:
“”“إعلان الفائز”””
try:
colors = _safe_get_colors(theme)

```
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "🏆", "size": "xxl", "align": "center"},
                {"type": "text", "text": "مبروك!", "size": "xl", "weight": "bold", "color": colors["success"], "align": "center", "margin": "md"},
                {"type": "separator", "margin": "lg"},
                {"type": "text", "text": username, "size": "lg", "weight": "bold", "color": colors["text"], "align": "center", "margin": "lg"},
                {"type": "text", "text": f"فائز لعبة {game_name}", "size": "sm", "color": colors["text2"], "align": "center"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"+{points}", "size": "xxl", "weight": "bold", "color": colors["primary"], "align": "center"}
                    ],
                    "backgroundColor": colors["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "20px",
                    "margin": "lg"
                },
                {"type": "text", "text": f"المجموع: {total_points} نقطة", "size": "sm", "color": colors["text2"], "align": "center", "margin": "md"}
            ],
            "paddingAll": "24px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return FlexMessage(alt_text="إعلان الفائز", contents=FlexContainer.from_dict(bubble))

except Exception as e:
    return create_debug_report(e)
```

def build_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
“”“نافذة المساعدة”””
try:
colors = _safe_get_colors(theme)

```
    header = create_glass_header(colors, "❓ المساعدة", "دليل استخدام البوت")
    
    help_items = [
        ("🎮", "ألعاب", "عرض قائمة الألعاب"),
        ("⭐", "نقاطي", "عرض نقاطك وإحصائياتك"),
        ("🏆", "صدارة", "عرض أفضل اللاعبين"),
        ("🎨", "ثيمات", "تغيير المظهر"),
        ("✅", "انضم", "التسجيل في البوت"),
        ("⛔", "إيقاف", "إيقاف اللعبة الحالية"),
    ]
    
    help_cards = []
    for icon, cmd, desc in help_items:
        help_cards.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": icon, "size": "lg", "flex": 0},
                {"type": "text", "text": cmd, "size": "md", "weight": "bold", "flex": 1, "margin": "md", "color": colors["text"]},
                {"type": "text", "text": desc, "size": "xs", "flex": 2, "wrap": True, "color": colors["text2"]}
            ],
            "margin": "md"
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + help_cards,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return FlexMessage(alt_text="المساعدة", contents=FlexContainer.from_dict(bubble))

except Exception as e:
    return create_debug_report(e)
```

def build_multiplayer_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
“”“مساعدة وضع الفريقين”””
try:
colors = _safe_get_colors(theme)

```
    header = create_glass_header(colors, "👥 وضع الفريقين", "كيف تلعب مع أصدقائك")
    
    steps = [
        "1️⃣ اكتب 'فريقين' لبدء وضع الفرق",
        "2️⃣ اكتب 'انضم' للانضمام",
        "3️⃣ ابدأ اللعبة بعد انضمام اللاعبين",
        "4️⃣ سيتم تقسيمكم لفريقين تلقائياً",
        "5️⃣ العب واربح نقاط لفريقك!"
    ]
    
    step_boxes = []
    for step in steps:
        step_boxes.append({
            "type": "text",
            "text": step,
            "size": "sm",
            "color": colors["text"],
            "wrap": True,
            "margin": "md"
        })
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + step_boxes,
            "paddingAll": "20px",
            "backgroundColor": colors["bg"]
        }
    }
    
    return FlexMessage(alt_text="مساعدة الفريقين", contents=FlexContainer.from_dict(bubble))

except Exception as e:
    return create_debug_report(e)
```

# ============================================================================

# Export All

# ============================================================================

**all** = [
‘build_enhanced_home’,
‘build_games_menu’,
‘build_my_points’,
‘build_leaderboard’,
‘build_theme_selector’,
‘build_registration_required’,
‘build_winner_announcement’,
‘build_help_window’,
‘build_multiplayer_help_window’,
‘attach_quick_reply_to_message’,
‘create_games_quick_reply’
]
