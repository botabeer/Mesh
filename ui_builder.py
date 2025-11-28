# ui.py
"""
Bot Mesh - UI Builder (Merged Glass Morphism) v10.0
Created by: Abeer Aldosari © 2025
ملف واجهات شامل: البداية - المساعدة - المساعدة الجماعية - الألعاب - نقاطي - الصدارة - تسجيل - إعلان الفائز
يتضمن: Quick Reply للألعاب فقط + دالة مستكشف أخطاء لإرسال تقرير مفصل عند الفشل
"""

import traceback
from typing import List, Optional, Dict, Any

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction

# ثبات الاستيراد من constants.py الموجود عندك
from constants import BOT_RIGHTS, THEMES, DEFAULT_THEME, GAME_LIST, FIXED_GAME_QR, FIXED_ACTIONS

# -------------------------
# Utilities
# -------------------------
def _get_colors(theme: str) -> Dict[str, str]:
    return THEMES.get(theme, THEMES[DEFAULT_THEME])

def create_debug_report(exc: Exception, context: Optional[Dict[str, Any]] = None) -> TextMessage:
    """
    Create a detailed debug report message (TextMessage).
    Use this when LINE doesn't reply or an exception happens to see stack trace and context.
    """
    tb = traceback.format_exc()
    ctx_lines = []
    if context:
        for k, v in context.items():
            ctx_lines.append(f"{k}: {v}")
    ctx_text = "\n".join(ctx_lines) if ctx_lines else "No extra context"
    text = (
        "⚠️ Debug Report\n\n"
        f"Exception: {str(exc)}\n\n"
        f"Traceback:\n{tb}\n"
        f"Context:\n{ctx_text}"
    )
    # keep text concise if too long (LINE limits) — truncate but keep head + tail
    if len(text) > 1800:
        text = text[:1000] + "\n\n...[truncated]...\n\n" + text[-700:]
    return TextMessage(text=text)

# -------------------------
# Quick Reply (Games Only) — persistent
# -------------------------
def create_games_quick_reply():
    """
    Build QuickReply object that contains ONLY game items (persistent games quick reply).
    Uses FIXED_GAME_QR constant (if present) or derives from GAME_LIST.
    """
    items = []
    # prefer FIXED_GAME_QR if available
    try:
        qr_items = FIXED_GAME_QR  # expected: list of {"label": "...", "text": "..."}
    except Exception:
        qr_items = None

    if qr_items:
        for it in qr_items:
            label = it.get("label") if isinstance(it, dict) else str(it)
            text = it.get("text") if isinstance(it, dict) else str(it)
            items.append(QuickReplyItem(action=MessageAction(label=label, text=text)))
    else:
        # fallback: derive from GAME_LIST (dict or list)
        if isinstance(GAME_LIST, dict):
            for k, v in GAME_LIST.items():
                label = v.get("label", k)
                items.append(QuickReplyItem(action=MessageAction(label=f"▫️ {label}", text=label)))
        else:
            # GAME_LIST may be a list of tuples (internal_key, label, icon)
            for entry in GAME_LIST:
                if isinstance(entry, (list, tuple)) and len(entry) >= 2:
                    label = entry[1]
                    items.append(QuickReplyItem(action=MessageAction(label=f"▫️ {label}", text=label)))
    return QuickReply(items=items)

def attach_quick_reply_to_message(message):
    """Attach games quick reply to a message object (if applicable)"""
    try:
        qr = create_games_quick_reply()
        if hasattr(message, "quick_reply"):
            message.quick_reply = qr
        else:
            # For FlexMessage, set quick_reply attribute (Messaging API accepts messages list where each message can have quickReply)
            setattr(message, "quick_reply", qr)
    except Exception as e:
        # If anything fails, we simply do nothing but return message
        pass
    return message

# -------------------------
# Glass components (cards / buttons)
# -------------------------
def create_glass_header(colors: Dict[str,str], title: str, subtitle: Optional[str] = None, icon: Optional[str] = None):
    header_content = []
    if icon:
        header_content.append({
            "type": "text",
            "text": icon,
            "size": "xxl",
            "align": "center"
        })
    header_content.append({
        "type": "text",
        "text": title,
        "size": "xxl",
        "weight": "bold",
        "color": colors["primary"],
        "align": "center",
        "margin": "xs" if icon else "none"
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
    return header_content

def create_glass_card(colors: Dict[str,str], icon: str, title: str, description: str, highlight: bool = False):
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [{"type": "text", "text": icon, "size": "xl", "align": "center", "gravity": "center"}],
                "backgroundColor": colors["primary"] if highlight else colors["card"],
                "cornerRadius": "15px",
                "width": "50px",
                "height": "50px",
                "justifyContent": "center",
                "alignItems": "center"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": title, "size": "md", "weight": "bold", "color": colors["text"]},
                    {"type": "text", "text": description, "size": "xs", "color": colors["text2"], "wrap": True, "margin": "xs"}
                ],
                "flex": 1,
                "spacing": "xs",
                "paddingStart": "md"
            }
        ],
        "backgroundColor": colors["glass"],
        "cornerRadius": "20px",
        "paddingAll": "15px",
        "margin": "sm",
        "borderWidth": "2px" if highlight else "1px",
        "borderColor": colors["primary"] if highlight else colors["border"],
        "spacing": "md"
    }

def create_glass_button(label: str, text_cmd: str, color: str, icon: Optional[str] = None, style: str = "primary"):
    button_text = f"{icon} {label}" if icon else label
    return {
        "type": "button",
        "action": {
            "type": "message",
            "label": button_text,
            "text": text_cmd
        },
        "style": style,
        "height": "sm",
        "color": color
    }

def create_button_grid(buttons: List[Dict[str, Any]], columns: int = 2):
    rows = []
    for i in range(0, len(buttons), columns):
        row_buttons = buttons[i:i+columns]
        rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": row_buttons,
            "margin": "sm"
        })
    return rows

def create_section_title(colors: Dict[str,str], title: str, icon: Optional[str] = None):
    title_text = f"{icon} {title}" if icon else title
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {"type": "text", "text": title_text, "size": "lg", "weight": "bold", "color": colors["text"]},
            {"type": "separator", "color": colors["primary"], "margin": "sm"}
        ],
        "margin": "xl"
    }

# -------------------------
# Main windows (public functions)
# -------------------------

def build_enhanced_home(username: str, points: int, is_registered: bool, theme: str = DEFAULT_THEME) -> FlexMessage:
    """
    Enhanced Home window (Glass style).
    """
    colors = _get_colors(theme)
    status_icon = "✅" if is_registered else "⚠️"
    status_text = "مسجل" if is_registered else "غير مسجل"

    header = create_glass_header(colors, "Bot Mesh", "منصة الألعاب الذكية الشاملة", "▫️")

    body = [
        # profile card
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "▫️", "size": "xxl", "align": "center"},
                {"type": "text", "text": username, "size": "xl", "weight": "bold", "color": colors["text"], "align": "center", "margin": "sm"},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": f"{status_icon} {status_text}", "size": "sm", "color": colors["text2"], "flex": 2},
                        {"type": "text", "text": f"▫️ {points}", "size": "sm", "color": colors["primary"], "align": "end", "flex": 1}
                    ]
                }
            ],
            "backgroundColor": colors["glass"],
            "cornerRadius": "20px",
            "paddingAll": "20px",
            "borderWidth": "2px",
            "borderColor": colors["primary"]
        },
        create_section_title(colors, "الأقسام الرئيسية", "▫️"),
        create_glass_card(colors, "▫️", "الألعاب", "اختر من مجموعة ألعاب متكاملة"),
        create_glass_card(colors, "▫️", "نقاطي", "اطلع على رصيد نقاطك"),
        create_glass_card(colors, "▫️", "الصدارة", "تنافس مع الآخرين"),
        create_glass_card(colors, "▫️", "الثيمات", "غيّر مظهر البوت"),
        create_section_title(colors, "طرق اللعب", "▫️"),
        create_glass_card(colors, "▫️", "فردي", "العب بمفردك • تلميحات متاحة"),
        create_glass_card(colors, "▫️", "مجموعة", "ادعُ البوت للمجموعة • زر فريقين متاح"),
        create_section_title(colors, "أدوات سريعة", "▫️"),
    ]

    # quick action buttons (uses colors)
    buttons = [
        create_glass_button("الألعاب", "ألعاب", colors["primary"]),
        create_glass_button("نقاطي", "نقاطي", colors["primary"], style="secondary"),
        create_glass_button("صدارة", "صدارة", colors["primary"], style="secondary"),
        create_glass_button("الثيمات", "ثيمات", colors["primary"], style="secondary"),
        create_glass_button("انضم", "انضم", colors["primary"]),
        create_glass_button("فريقين", "فريقين", colors["primary"])
    ]
    body.extend(create_button_grid(buttons, columns=2))

    footer = [
        {"type": "separator", "color": colors["border"]},
        {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": colors["text2"], "align": "center", "wrap": True, "margin": "md"}
    ]

    bubble = {
        "type": "bubble",
        "size": "giga",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": header + [{"type": "separator", "color": colors["border"], "margin": "lg"}] + body,
            "paddingAll": "24px",
            "spacing": "none",
            "backgroundColor": colors["bg"]
        },
        "footer": {"type": "box", "layout": "vertical", "contents": footer, "paddingAll": "15px", "backgroundColor": colors["bg"]},
        "styles": {"body": {"backgroundColor": colors["bg"]}, "footer": {"backgroundColor": colors["bg"]}}
    }

    msg = FlexMessage(alt_text="🏠 البداية", contents=FlexContainer.from_dict(bubble))
    attach_quick_reply_to_message(msg)
    return msg

def build_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """
    General help window (concise, includes quick actions).
    """
    colors = _get_colors(theme)
    header = create_glass_header(colors, "دليل الاستخدام", "كل ما تحتاج معرفته", "▫️")

    body = []
    body.append(create_section_title(colors, "البدء السريع", "▫️"))
    body.append(create_glass_card(colors, "▫️", "انضم", "اضغط 'انضم' للتسجيل واللعب"))
    body.append(create_glass_card(colors, "▫️", "الألعاب", "اضغط 'الألعاب' لعرض القائمة"))
    body.append(create_glass_card(colors, "▫️", "فريقين", "في المجموعات: اضغط 'فريقين' ثم اكتب 'انضم'"))
    body.append(create_section_title(colors, "أوامر مهمة", "▫️"))
    body.append(create_glass_card(colors, "▫️", "لمح", "احصل على تلميح (فردي فقط)"))
    body.append(create_glass_card(colors, "▫️", "جاوب", "اكشف الإجابة (فردي فقط)"))
    body.append({
        "type": "box",
        "layout": "vertical",
        "contents": create_button_grid([
            create_glass_button("الألعاب", "ألعاب", colors["primary"]),
            create_glass_button("الرئيسية", "home", colors["primary"], style="secondary")
        ], columns=2)[0]["contents"]
    })

    footer = [{"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": colors["text2"], "align": "center"}]

    bubble = {
        "type": "bubble",
        "size": "giga",
        "body": {"type": "box", "layout": "vertical", "contents": header + [{"type": "separator", "color": colors["border"], "margin": "lg"}] + body, "paddingAll": "24px", "spacing": "none", "backgroundColor": colors["bg"]},
        "footer": {"type": "box", "layout": "vertical", "contents": footer, "paddingAll": "15px", "backgroundColor": colors["bg"]},
        "styles": {"body": {"backgroundColor": colors["bg"]}, "footer": {"backgroundColor": colors["bg"]}}
    }

    msg = FlexMessage(alt_text="📚 المساعدة", contents=FlexContainer.from_dict(bubble))
    attach_quick_reply_to_message(msg)
    return msg

def build_multiplayer_help_window(theme: str = DEFAULT_THEME) -> FlexMessage:
    """
    Multiplayer help window (explains الفريقين workflow).
    """
    colors = _get_colors(theme)
    header = create_glass_header(colors, "دليل اللعب للمجموعات", "شرح وضع الفريقين", "▫️")

    body = []
    body.append(create_section_title(colors, "الخطوات", "▫️"))
    body.append(create_glass_card(colors, "▫️", "زر فريقين", "اضغط 'فريقين' ثم اكتب 'انضم' للانضمام"))
    body.append(create_glass_card(colors, "▫️", "قسّم تلقائي", "البوت يقسم المنضمين إلى فريقين بالتساوي"))
    body.append(create_glass_card(colors, "▫️", "الإجابات", "تُحتسب فقط إجابات المنضمين • لا يُقَبَل 'لمح'/'جاوب' في الفريقين"))
    body.append({
        "type": "box",
        "layout": "vertical",
        "contents": create_button_grid([
            create_glass_button("جرب الآن", "ألعاب", colors["primary"]),
            create_glass_button("الرئيسية", "home", colors["primary"], style="secondary")
        ], columns=2)[0]["contents"]
    })

    footer = [{"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": colors["text2"], "align": "center"}]

    bubble = {
        "type": "bubble",
        "size": "giga",
        "body": {"type": "box", "layout": "vertical", "contents": header + [{"type": "separator", "color": colors["border"], "margin": "lg"}] + body, "paddingAll": "24px", "spacing": "none", "backgroundColor": colors["bg"]},
        "footer": {"type": "box", "layout": "vertical", "contents": footer, "paddingAll": "15px", "backgroundColor": colors["bg"]},
        "styles": {"body": {"backgroundColor": colors["bg"]}, "footer": {"backgroundColor": colors["bg"]}}
    }

    msg = FlexMessage(alt_text="👥 مساعدة المجموعة", contents=FlexContainer.from_dict(bubble))
    attach_quick_reply_to_message(msg)
    return msg

# -------------------------
# Games menu, points, leaderboard, registration, winner
# -------------------------
def build_games_menu(theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _get_colors(theme)
    # Build game buttons from GAME_LIST
    game_buttons = []
    # GAME_LIST might be dict or list
    if isinstance(GAME_LIST, dict):
        for k, v in GAME_LIST.items():
            label = v.get("label", k)
            cmd = v.get("command", label) if isinstance(v, dict) else label
            game_buttons.append(create_glass_button(label, label, colors["primary"]))
    else:
        # list of tuples (internal_key, label, icon)
        for entry in GAME_LIST:
            if isinstance(entry, (list, tuple)) and len(entry) >= 2:
                label = entry[1]
                game_buttons.append(create_glass_button(label, label, colors["primary"]))

    body = [
        create_section_title(colors, "قائمة الألعاب", "▫️"),
    ]
    body.extend(create_button_grid(game_buttons, columns=3))

    footer = [{"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": colors["text2"], "align": "center"}]

    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {"type": "box", "layout": "vertical", "contents": body, "paddingAll": "18px", "backgroundColor": colors["bg"]},
        "footer": {"type": "box", "layout": "vertical", "contents": footer, "paddingAll": "12px", "backgroundColor": colors["bg"]},
        "styles": {"body": {"backgroundColor": colors["bg"]}, "footer": {"backgroundColor": colors["bg"]}}
    }

    msg = FlexMessage(alt_text="🎮 الألعاب", contents=FlexContainer.from_dict(bubble))
    attach_quick_reply_to_message(msg)
    return msg

def build_my_points(username: str, points: int, user_game_stats: Optional[dict], theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _get_colors(theme)
    header = create_section_title(colors, "▫️ نقاطي", None)
    contents = [
        {"type": "text", "text": username, "size": "lg", "weight": "bold", "color": colors["text"], "align": "center"},
        {"type": "box", "layout": "vertical", "contents": [
            {"type": "text", "text": "▫️ إجمالي النقاط", "size": "sm", "color": colors["text2"], "align": "center"},
            {"type": "text", "text": str(points), "size": "xxl", "weight": "bold", "color": colors["primary"], "align": "center"}
        ], "backgroundColor": colors["glass"], "cornerRadius": "15px", "paddingAll": "18px", "margin": "md"}
    ]
    footer = [{"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": colors["text2"], "align": "center"}]

    bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": header["contents"] + contents, "paddingAll": "18px", "backgroundColor": colors["bg"]}, "footer": {"type": "box", "layout": "vertical", "contents": footer, "paddingAll": "12px", "backgroundColor": colors["bg"]}}
    msg = FlexMessage(alt_text="⭐ نقاطي", contents=FlexContainer.from_dict(bubble))
    attach_quick_reply_to_message(msg)
    return msg

def build_leaderboard(top_users: List[tuple], theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _get_colors(theme)
    rows = []
    medals = ["🥇", "🥈", "🥉"]
    for i, (name, pts) in enumerate(top_users[:20], 1):
        medal = medals[i-1] if i <= 3 else str(i)
        rows.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {"type": "text", "text": medal, "size": "sm", "flex": 0},
                {"type": "text", "text": name, "size": "sm", "flex": 3, "color": colors["text"]},
                {"type": "text", "text": str(pts), "size": "sm", "flex": 1, "align": "end", "color": colors["primary"]}
            ],
            "spacing": "sm",
            "paddingAll": "sm"
        })

    if not rows:
        rows = [{"type":"text","text":"لا يوجد لاعبين مسجلين بعد","size":"sm","color":colors["text2"],"align":"center"}]

    body = [create_section_title(colors, "▫️ لوحة الصدارة", None), {"type":"box","layout":"vertical","contents": rows, "backgroundColor": colors["glass"], "cornerRadius":"15px","paddingAll":"12px", "margin":"md"}]
    footer = [{"type":"text","text":BOT_RIGHTS,"size":"xxs","color":colors["text2"],"align":"center"}]
    bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":body,"paddingAll":"18px","backgroundColor":colors["bg"]},"footer":{"type":"box","layout":"vertical","contents":footer,"paddingAll":"12px","backgroundColor":colors["bg"]}}
    msg = FlexMessage(alt_text="🏆 الصدارة", contents=FlexContainer.from_dict(bubble))
    attach_quick_reply_to_message(msg)
    return msg

def build_registration_required(theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _get_colors(theme)
    body = [
        {"type":"text","text":"⚠️ يجب التسجيل أولاً","size":"lg","weight":"bold","color":colors["primary"],"align":"center"},
        {"type":"text","text":"اضغط 'انضم' للتسجيل والبدء باللعب","size":"sm","color":colors["text2"],"align":"center","wrap":True}
    ]
    footer = [create_glass_button("انضم", "انضم", colors["primary"])]
    bubble = {"type":"bubble","size":"kilo","body":{"type":"box","layout":"vertical","contents":body,"paddingAll":"18px","backgroundColor":colors["bg"]},"footer":{"type":"box","layout":"vertical","contents":[{"type":"button","action":{"type":"message","label":"انضم","text":"انضم"},"style":"primary","height":"sm","color":colors["primary"}],"paddingAll":"12px","backgroundColor":colors["bg"]}}
    msg = FlexMessage(alt_text="تسجيل مطلوب", contents=FlexContainer.from_dict(bubble))
    attach_quick_reply_to_message(msg)
    return msg

def build_winner_announcement(username: str, game_name: str, total_score: int, final_points: int, theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _get_colors(theme)
    body = [
        {"type":"text","text":"🏆 تهانينا!","size":"xl","weight":"bold","color":colors["primary"],"align":"center"},
        {"type":"text","text":f"▫️ لاعب: {username}","size":"sm","color":colors["text"],"align":"center"},
        {"type":"text","text":f"▫️ اللعبة: {game_name}","size":"sm","color":colors["text2"],"align":"center"},
        {"type":"text","text":f"▫️ نقاط الجولة: +{total_score}","size":"md","weight":"bold","color":colors["primary"],"align":"center","margin":"md"},
        {"type":"text","text":f"▫️ إجمالي النقاط: {final_points}","size":"sm","color":colors["text2"],"align":"center","margin":"md"}
    ]
    footer_buttons = [
        {"type":"button","action":{"type":"message","label":"إعادة نفس اللعبة","text":f"إعادة {game_name}"},"style":"primary","height":"sm","color":colors["primary"]},
        {"type":"button","action":{"type":"message","label":"الألعاب","text":"ألعاب"},"style":"secondary","height":"sm","color":colors["primary"]}
    ]
    bubble = {"type":"bubble","size":"kilo","body":{"type":"box","layout":"vertical","contents":body,"paddingAll":"18px","backgroundColor":colors["bg"]},"footer":{"type":"box","layout":"vertical","contents":footer_buttons + [{"type":"text","text":BOT_RIGHTS,"size":"xxs","color":colors["text2"],"align":"center"}],"paddingAll":"12px","backgroundColor":colors["bg"]}}
    msg = FlexMessage(alt_text="🏆 فوز", contents=FlexContainer.from_dict(bubble))
    attach_quick_reply_to_message(msg)
    return msg

# -------------------------
# Theme selector (simple)
# -------------------------
def build_theme_selector(current_theme: str = DEFAULT_THEME) -> FlexMessage:
    colors = _get_colors(current_theme)
    # create rows of 3
    theme_keys = list(THEMES.keys())
    rows = []
    for i in range(0, len(theme_keys), 3):
        row = []
        for t in theme_keys[i:i+3]:
            style = "primary" if t == current_theme else "secondary"
            color = colors["primary"] if t == current_theme else colors["border"]
            row.append(create_glass_button(t, f"ثيم {t}", color, style=style))
        rows.append({"type":"box","layout":"horizontal","spacing":"sm","contents":row})
    body = [create_section_title(colors, "اختيار الثيم", "▫️")] + rows
    bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":body,"paddingAll":"18px","backgroundColor":colors["bg"]},"footer":{"type":"box","layout":"vertical","contents":[{"type":"text","text":BOT_RIGHTS,"size":"xxs","color":colors["text2"],"align":"center"}],"paddingAll":"12px","backgroundColor":colors["bg"]}}
    msg = FlexMessage(alt_text="🎨 الثيمات", contents=FlexContainer.from_dict(bubble))
    attach_quick_reply_to_message(msg)
    return msg

# -------------------------
# Export helpers for use by app.py and games
# -------------------------
__all__ = [
    "build_enhanced_home",
    "build_help_window",
    "build_multiplayer_help_window",
    "build_games_menu",
    "build_my_points",
    "build_leaderboard",
    "build_registration_required",
    "build_winner_announcement",
    "build_theme_selector",
    "create_games_quick_reply",
    "attach_quick_reply_to_message",
    "create_debug_report"
]
