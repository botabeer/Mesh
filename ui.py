"""
ui.py — واجهات Bot Mesh (ثيمات، نوافذ Flex، Quick Reply)
Created by: Abeer Aldosari © 2025
ملاحظات:
- كل زر ألعاب مع بادئة "▫️" وبدون إيموجي كما طلبت.
- محاكاة ستايل ثلاثي الأبعاد عبر تدرجات وظلال في قيمة الثيم.
- دالة get_quick_reply() لإرفاق Quick Reply دائمًا.
- الدوال تُعيد FlexMessage فقط. في app.py نُرسل رسالة نصية صغيرة مع quick reply بعد FlexMessage
  لضمان ظهور Quick Reply دائمًا في واجهة LINE.
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction

BOT_NAME = "Bot Mesh"
BOT_RIGHTS = "Bot Mesh © 2025 by Abeer Aldosari"
BOT_CREATOR = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

# الثيمات (ألوان + ظلال/محاكاة 3D عبر border/shadow/gradient string للمرجع)
THEMES = {
    "رمادي": {"primary": "#60A5FA", "bg": "#0F172A", "card": "#1E293B", "text": "#F1F5F9", "text2": "#CBD5E1", "success": "#34D399", "error": "#F87171", "warning": "#FBBF24", "shadow": "#334155", "border": "#475569", "gradient": "linear-gradient(135deg,#1F2937 0%,#111827 100%)"},
    "بنفسجي": {"primary": "#A78BFA", "bg": "#1E1B4B", "card": "#2E2558", "text": "#F3F4F6", "text2": "#C4B5FD", "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "shadow": "#6D28D9", "border": "#7C3AED", "gradient": "linear-gradient(135deg,#7C3AED 0%,#4C1D95 100%)"},
    "أخضر": {"primary": "#10B981", "bg": "#064E3B", "card": "#065F46", "text": "#F0FDF4", "text2": "#6EE7B7", "success": "#34D399", "error": "#F87171", "warning": "#FBBF24", "shadow": "#047857", "border": "#10B981", "gradient": "linear-gradient(135deg,#047857 0%,#065F46 100%)"},
    "أزرق": {"primary": "#3B82F6", "bg": "#1E3A8A", "card": "#1E40AF", "text": "#EFF6FF", "text2": "#93C5FD", "success": "#22C55E", "error": "#EF4444", "warning": "#F59E0B", "shadow": "#1D4ED8", "border": "#3B82F6", "gradient": "linear-gradient(135deg,#2563EB 0%,#1E3A8A 100%)"},
    "وردي": {"primary": "#EC4899", "bg": "#831843", "card": "#9D174D", "text": "#FFF1F2", "text2": "#FBCFE8", "success": "#22C55E", "error": "#DC2626", "warning": "#F59E0B", "shadow": "#BE185D", "border": "#EC4899", "gradient": "linear-gradient(135deg,#BE185D 0%,#831843 100%)"},
    "برتقالي": {"primary": "#F97316", "bg": "#7C2D12", "card": "#9A3412", "text": "#FFF7ED", "text2": "#FED7AA", "success": "#22C55E", "error": "#DC2626", "warning": "#FBBF24", "shadow": "#C2410C", "border": "#F97316", "gradient": "linear-gradient(135deg,#ED8F03 0%,#7C2D12 100%)"},
    "أبيض": {"primary": "#8B5CF6", "bg": "#F9FAFB", "card": "#FFFFFF", "text": "#111827", "text2": "#6B7280", "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "shadow": "#E5E7EB", "border": "#E5E7EB", "gradient": "linear-gradient(135deg,#FFFFFF 0%,#F3F4F6 100%)"},
    "بني": {"primary": "#D97706", "bg": "#451A03", "card": "#78350F", "text": "#FEF3C7", "text2": "#FCD34D", "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "shadow": "#92400E", "border": "#D97706", "gradient": "linear-gradient(135deg,#7C2D12 0%,#451A03 100%)"},
    "أصفر": {"primary": "#EAB308", "bg": "#713F12", "card": "#854D0E", "text": "#FEFCE8", "text2": "#FEF08A", "success": "#22C55E", "error": "#DC2626", "warning": "#F97316", "shadow": "#A16207", "border": "#EAB308", "gradient": "linear-gradient(135deg,#FFD89B 0%,#F59E0B 100%)"}
}

DEFAULT_THEME = "رمادي"

# -----------------------
# الألعاب — أسماؤها بدون إيموجي ومرتبة حسب الأفضلية كما طلبت (مع بادئة ▫️)
# ترتيب الأزرار في الأسفل ثابت (Quick Reply دائم)
# خريطة الأسماء الداخليه المستخدمة بواسطة game loader
# -----------------------
ORDERED_GAMES = [
    ("سرعة", "▫️ سرعة"),
    ("ذكاء", "▫️ ذكاء"),
    ("لعبة", "▫️ لعبة"),       # لعبة = إنسان حيوان نبات
    ("أغنية", "▫️ أغنية"),
    ("تخمين", "▫️ تخمين"),
    ("سلسلة", "▫️ سلسلة"),
    ("كلمات", "▫️ ترتيب"),     # عرضها كـ "ترتيب" حسب طلبك
    ("تكوين", "▫️ تكوين"),
    ("أضداد", "▫️ ضد"),        # عرضها بكلمة "ضد"
    ("ألوان", "▫️ لون"),       # عرضها بكلمة "لون"
    ("رياضيات", "▫️ رياضيات"),
    ("توافق", "▫️ توافق")       # توافق آخر شيء
]

# إذا عندك قائمة ألعاب مفصلة - ضع هنا الوصف (اختياري)
GAME_DESCRIPTIONS = {
    "لعبة": "إنسان حيوان نبات",
    "سرعة": "اختبار السرعة",
    "ذكاء": "ألغاز ذكية",
    "أغنية": "خمن المغني",
    "تخمين": "خمن الكلمة",
    "سلسلة": "سلسلة كلمات",
    "كلمات": "رتب الحروف",
    "تكوين": "كوّن كلمات",
    "أضداد": "اكتشف العكس",
    "ألوان": "تحدي الألوان",
    "رياضيات": "أسئلة حسابية",
    "توافق": "احسب نسبة التوافق"
}

# ---------- Helpers لبناء مكونات Flex (ثلاثية الأبعاد محاكاة) ----------
def _3d_button(label, text, colors, style="secondary", color_override=None):
    # زر يظهر كتدرج/حدود لإعطاء إحساس 3D
    return {
        "type": "button",
        "action": {"type": "message", "label": label, "text": text},
        "style": style,
        "height": "sm",
        "color": color_override or (colors["primary"] if style == "primary" else colors["card"])
    }

def _row(buttons, spacing="sm"):
    return {"type": "box", "layout": "horizontal", "spacing": spacing, "contents": buttons}

def _separator(colors, margin="md"):
    return {"type": "separator", "color": colors["shadow"], "margin": margin}

def _3d_card(contents, colors, corner="15px", pad="15px"):
    return {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "backgroundColor": colors["card"],
        "cornerRadius": corner,
        "paddingAll": pad,
        "borderWidth": "1px",
        "borderColor": colors["border"]
    }

def _header(title, subtitle, colors):
    contents = [
        {"type": "text", "text": title, "weight": "bold", "size": "xxl", "color": colors["primary"], "align": "center"}
    ]
    if subtitle:
        contents.append({"type": "text", "text": subtitle, "size": "sm", "color": colors["text2"], "align": "center", "margin": "sm"})
    return {"type": "box", "layout": "vertical", "contents": contents, "spacing": "xs"}

def _footer(button_rows, colors):
    contents = []
    for r in button_rows:
        contents.append(r)
    contents.append(_separator(colors))
    contents.append({"type": "text", "text": f"{BOT_RIGHTS} — {BOT_CREATOR}", "size": "xxs", "color": colors["text2"], "align": "center"})
    return {"type": "box", "layout": "vertical", "spacing": "sm", "contents": contents, "backgroundColor": colors["bg"], "paddingAll": "12px"}

def _bubble(body_contents, footer_box, colors):
    return {
        "type": "bubble",
        "size": "mega",
        "body": {"type": "box", "layout": "vertical", "spacing": "lg", "contents": body_contents, "backgroundColor": colors["bg"], "paddingAll": "18px"},
        "footer": footer_box,
        "styles": {"body": {"backgroundColor": colors["bg"]}, "footer": {"backgroundColor": colors["bg"]}}
    }

# Quick Reply — دائم (ترجع QuickReply object لاستخدامه متى شئت)
def get_quick_reply():
    items = []
    for key, label in ORDERED_GAMES:
        # نرسل نص "لعبة <الاسم الداخلي>" أثناء الضغط
        items.append(QuickReplyItem(action=MessageAction(label=label, text=f"لعبة {key}")))
    # أضف أزرار رئيسية
    main_quick = [
        QuickReplyItem(action=MessageAction(label="▫️ بداية", text="بداية")),
        QuickReplyItem(action=MessageAction(label="▫️ مساعدة", text="مساعدة")),
        QuickReplyItem(action=MessageAction(label="▫️ نقاطي", text="نقاطي")),
        QuickReplyItem(action=MessageAction(label="▫️ صدارة", text="صدارة"))
    ]
    # اجمع (نضع ألعاب أولًا ثم رئيسية)
    items = items + main_quick
    return QuickReply(items=items)

# ---------- دوال بناء النوافذ (ترجع FlexMessage) ----------
def build_home(theme=DEFAULT_THEME, username="مستخدم", points=0, is_registered=False):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])

    user_card = _3d_card([
        {"type": "text", "text": f"👤 {username}", "size": "xl", "color": colors["text"], "weight": "bold", "align": "center"},
        {"type": "box", "layout": "horizontal", "spacing": "md", "contents": [
            {"type": "text", "text": ("✅ مسجل" if is_registered else "⚪ غير مسجل"), "size": "sm", "color": (colors["success"] if is_registered else colors["text2"]), "flex": 1},
            {"type": "text", "text": f"⭐ {points}", "size": "sm", "color": colors["primary"], "align": "end", "flex": 1, "weight": "bold"}
        ], "margin": "md"}
    ], colors, corner="18px", pad="18px")

    # ثيمات مختصرة (زر لكل ثيم)
    theme_rows = []
    tkeys = list(THEMES.keys())
    for i in range(0, len(tkeys), 3):
        row_buttons = []
        for tk in tkeys[i:i+3]:
            row_buttons.append(_3d_button(f"▫️ {tk}", f"ثيم {tk}", colors, "primary" if tk == theme else "secondary", colors["primary"] if tk == theme else None))
        theme_rows.append(_row(row_buttons))

    body = [
        _header(f"🎮 {BOT_NAME}", "بوت الألعاب الترفيهي", colors),
        _separator(colors),
        user_card,
        {"type": "text", "text": "🎨 اختر ثيمك المفضل:", "size": "md", "weight": "bold", "color": colors["text"], "margin": "lg"}
    ] + theme_rows

    # أزرار رئيسية Footer
    footer_buttons = [
        _row([_3d_button("▫️ ألعاب", "العاب", colors, "primary", colors["primary"]), _3d_button("▫️ نقاطي", "نقاطي", colors)]),
        _row([_3d_button("▫️ صدارة", "صدارة", colors), _3d_button("▫️ مساعدة", "مساعدة", colors)])
    ]

    footer = _footer(footer_buttons, colors)
    return FlexMessage(alt_text=f"{BOT_NAME} - البداية", contents=FlexContainer.from_dict(_bubble(body, footer, colors)))

def build_help(theme=DEFAULT_THEME):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])

    basic = _3d_card([
        {"type": "text", "text": "📌 الأوامر الأساسية:", "size": "md", "color": colors["text"], "weight": "bold"},
        {"type": "text", "text": "• بداية → العودة للقائمة الرئيسية\n• العاب → عرض الألعاب\n• نقاطي → عرض نقاطك\n• صدارة → لوحة الصدارة\n• انضم → تسجيل\n• انسحب → إلغاء التسجيل", "size": "xs", "color": colors["text2"], "wrap": True, "margin": "sm"}
    ], colors)

    game_cmds = _3d_card([
        {"type": "text", "text": "🎮 أوامر اللعب:", "size": "md", "color": colors["text"], "weight": "bold"},
        {"type": "text", "text": "• لعبة [اسم] → بدء اللعبة\n• لمح → طلب تلميح\n• جاوب [الجواب] → للإجابة\n• إيقاف → إنهاء اللعبة", "size": "xs", "color": colors["text2"], "wrap": True, "margin": "sm"}
    ], colors)

    body = [
        _header("❓ مساعدة", "دليل استخدام البوت", colors),
        _separator(colors),
        basic,
        game_cmds
    ]

    footer_buttons = [_row([_3d_button("▫️ البداية", "بداية", colors, "primary", colors["primary"]), _3d_button("▫️ ألعاب", "العاب", colors)])]
    footer = _footer(footer_buttons, colors)
    return FlexMessage(alt_text="مساعدة", contents=FlexContainer.from_dict(_bubble(body, footer, colors)))

def build_games_menu(theme=DEFAULT_THEME):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])

    # أبني أزرار الألعاب حسب ORDERED_GAMES بمجموعات 2 في الصف ليتناسب مع Flex
    game_rows = []
    for i in range(0, len(ORDERED_GAMES), 2):
        row_buttons = []
        for gkey, glabel in ORDERED_GAMES[i:i+2]:
            row_buttons.append(_3d_button(glabel, f"لعبة {gkey}", colors))
        game_rows.append(_row(row_buttons))

    instr = _3d_card([
        {"type": "text", "text": "💡 كيفية اللعب:", "size": "sm", "color": colors["text"], "weight": "bold"},
        {"type": "text", "text": "اضغط على اسم اللعبة لبدءها. استخدم الأزرار السريعة في الأسفل للوصول السريع.", "size": "xs", "color": colors["text2"], "wrap": True, "margin": "sm"}
    ], colors)

    body = [
        _header("🎮 الألعاب المتاحة", f"{len(ORDERED_GAMES)} لعبة", colors),
        _separator(colors)
    ] + game_rows + [_separator(colors), instr]

    footer_buttons = [_row([_3d_button("▫️ البداية", "بداية", colors, "primary", colors["primary"]), _3d_button("▫️ مساعدة", "مساعدة", colors)])]
    footer = _footer(footer_buttons, colors)
    return FlexMessage(alt_text="قائمة الألعاب", contents=FlexContainer.from_dict(_bubble(body, footer, colors)))

def build_my_points(username, points, theme=DEFAULT_THEME):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])

    pts = _3d_card([
        {"type": "text", "text": "⭐", "size": "xxl", "align": "center"},
        {"type": "text", "text": str(points), "size": "xxl", "weight": "bold", "color": colors["primary"], "align": "center", "margin": "md"},
        {"type": "text", "text": "نقطة", "size": "md", "color": colors["text2"], "align": "center", "margin": "sm"}
    ], colors, corner="20px", pad="20px")

    body = [_header("⭐ نقاطي", f"مرحباً {username}", colors), _separator(colors), pts]

    footer_buttons = [
        _row([_3d_button("▫️ الصدارة", "صدارة", colors, "primary", colors["primary"]), _3d_button("▫️ ألعاب", "الالعاب", colors)]),
        _row([_3d_button("▫️ البداية", "بداية", colors)])
    ]
    footer = _footer(footer_buttons, colors)
    return FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(_bubble(body, footer, colors)))

def build_leaderboard(top_players, theme=DEFAULT_THEME):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    player_cards = []
    for i, (name, pts) in enumerate(top_players[:10], 1):
        medal = "▫️"
        color_medal = colors["text"]
        if i == 1:
            medal = "1."
            color_medal = "#FFD700"
        elif i == 2:
            medal = "2."
            color_medal = "#C0C0C0"
        elif i == 3:
            medal = "3."
            color_medal = "#CD7F32"

        player_cards.append(_3d_card([
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": medal, "size": "lg", "color": color_medal, "weight": "bold", "flex": 0, "align": "center"},
                {"type": "text", "text": name[:20] + "..." if len(name) > 20 else name, "size": "sm", "color": colors["text"], "flex": 3, "margin": "md"},
                {"type": "text", "text": f"⭐ {pts}", "size": "sm", "color": colors["primary"], "align": "end", "weight": "bold", "flex": 2}
            ]}
        ], colors, corner="12px", pad="12px"))

    if not player_cards:
        player_cards = [_3d_card([{"type": "text", "text": "لا يوجد لاعبون بعد", "size": "md", "color": colors["text2"], "align": "center"}], colors)]

    body = [_header("🏆 الصدارة", f"أفضل {len(top_players)} لاعب", colors), _separator(colors)] + player_cards
    footer_buttons = [_row([_3d_button("▫️ نقاطي", "نقاطي", colors, "primary", colors["primary"]), _3d_button("▫️ ألعاب", "العاب", colors)]), _row([_3d_button("▫️ البداية", "بداية", colors)])]
    footer = _footer(footer_buttons, colors)
    return FlexMessage(alt_text="صدارة", contents=FlexContainer.from_dict(_bubble(body, footer, colors)))

def build_registration_required(theme=DEFAULT_THEME):
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    alert = _3d_card([
        {"type": "text", "text": "⚠️", "size": "xxl", "align": "center"},
        {"type": "text", "text": "يجب التسجيل أولاً", "size": "xl", "weight": "bold", "color": colors["warning"], "align": "center", "margin": "md"},
        {"type": "text", "text": "للوصول إلى الألعاب وجمع النقاط، الرجاء التسجيل", "size": "sm", "color": colors["text2"], "align": "center", "wrap": True, "margin": "md"}
    ], colors, corner="18px", pad="18px")

    body = [_header("🔒 تسجيل", "انضم إلينا", colors), _separator(colors), alert]
    footer_buttons = [_row([_3d_button("▫️ انضم الآن", "انضم", colors, "primary", colors["success"])]), _row([_3d_button("▫️ البداية", "بداية", colors)])]
    footer = _footer(footer_buttons, colors)
    return FlexMessage(alt_text="تسجيل مطلوب", contents=FlexContainer.from_dict(_bubble(body, footer, colors)))
