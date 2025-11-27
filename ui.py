"""
Bot Mesh v9.0 - Minimal UI System
Created by: Abeer Aldosari © 2025
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage, QuickReply, QuickReplyItem, MessageAction

BOT_NAME = "Bot Mesh"
BOT_RIGHTS = "Bot Mesh © 2025 by Abeer Aldosari"

THEMES = {
    "بنفسجي": {"primary": "#A78BFA", "bg": "#1E1B4B", "card": "#2E2558", "text": "#F3F4F6", "text2": "#C4B5FD", "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "shadow": "#6D28D9", "border": "#7C3AED"},
    "أخضر": {"primary": "#10B981", "bg": "#064E3B", "card": "#065F46", "text": "#F0FDF4", "text2": "#6EE7B7", "success": "#34D399", "error": "#F87171", "warning": "#FBBF24", "shadow": "#047857", "border": "#10B981"},
    "أزرق": {"primary": "#3B82F6", "bg": "#1E3A8A", "card": "#1E40AF", "text": "#EFF6FF", "text2": "#93C5FD", "success": "#22C55E", "error": "#EF4444", "warning": "#F59E0B", "shadow": "#1D4ED8", "border": "#3B82F6"},
    "رمادي": {"primary": "#60A5FA", "bg": "#0F172A", "card": "#1E293B", "text": "#F1F5F9", "text2": "#CBD5E1", "success": "#34D399", "error": "#F87171", "warning": "#FBBF24", "shadow": "#334155", "border": "#475569"},
    "وردي": {"primary": "#EC4899", "bg": "#831843", "card": "#9D174D", "text": "#FFF1F2", "text2": "#FBCFE8", "success": "#22C55E", "error": "#DC2626", "warning": "#F59E0B", "shadow": "#BE185D", "border": "#EC4899"},
    "برتقالي": {"primary": "#F97316", "bg": "#7C2D12", "card": "#9A3412", "text": "#FFF7ED", "text2": "#FED7AA", "success": "#22C55E", "error": "#DC2626", "warning": "#FBBF24", "shadow": "#C2410C", "border": "#F97316"},
    "أبيض": {"primary": "#8B5CF6", "bg": "#F9FAFB", "card": "#FFFFFF", "text": "#111827", "text2": "#6B7280", "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "shadow": "#E5E7EB", "border": "#E5E7EB"},
    "بني": {"primary": "#D97706", "bg": "#451A03", "card": "#78350F", "text": "#FEF3C7", "text2": "#FCD34D", "success": "#10B981", "error": "#EF4444", "warning": "#F59E0B", "shadow": "#92400E", "border": "#D97706"},
    "أصفر": {"primary": "#EAB308", "bg": "#713F12", "card": "#854D0E", "text": "#FEFCE8", "text2": "#FEF08A", "success": "#22C55E", "error": "#DC2626", "warning": "#F97316", "shadow": "#A16207", "border": "#EAB308"}
}

QUICK_BUTTONS = [
    {"label": "سرعة", "text": "لعبة سرعة"}, {"label": "ذكاء", "text": "لعبة ذكاء"}, {"label": "لعبة", "text": "لعبة لعبة"},
    {"label": "أغنية", "text": "لعبة أغنية"}, {"label": "تخمين", "text": "لعبة تخمين"}, {"label": "سلسلة", "text": "لعبة سلسلة"},
    {"label": "كلمات", "text": "لعبة كلمات"}, {"label": "تكوين", "text": "لعبة تكوين"}, {"label": "أضداد", "text": "لعبة أضداد"},
    {"label": "ألوان", "text": "لعبة ألوان"}, {"label": "رياضيات", "text": "لعبة رياضيات"}, {"label": "توافق", "text": "لعبة توافق"}
]

GAMES = {
    "سرعة": {"l": "سرعة", "d": "اختبار سرعة"}, "ذكاء": {"l": "ذكاء", "d": "ألغاز ذكية"}, "لعبة": {"l": "لعبة", "d": "إنسان حيوان نبات"},
    "أغنية": {"l": "أغنية", "d": "خمن المغني"}, "تخمين": {"l": "تخمين", "d": "خمن الكلمة"}, "سلسلة": {"l": "سلسلة", "d": "سلسلة الكلمات"},
    "كلمات": {"l": "كلمات", "d": "رتب الحروف"}, "تكوين": {"l": "تكوين", "d": "كوّن كلمات"}, "أضداد": {"l": "أضداد", "d": "عكس الكلمة"},
    "ألوان": {"l": "ألوان", "d": "تحدي الألوان"}, "رياضيات": {"l": "رياضيات", "d": "أسئلة حسابية"}, "توافق": {"l": "توافق", "d": "نسبة التوافق"}
}

def btn(l, t, c, s="secondary", co=None):
    return {"type": "button", "action": {"type": "message", "label": l, "text": t}, "style": s, "height": "sm", "color": co or (c["primary"] if s == "primary" else c["card"])}

def row(b): return {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": b}
def sep(c): return {"type": "separator", "color": c["shadow"], "margin": "md"}
def card(ct, c): return {"type": "box", "layout": "vertical", "contents": ct, "backgroundColor": c["card"], "cornerRadius": "15px", "paddingAll": "15px", "borderWidth": "1px", "borderColor": c["border"]}
def hdr(t, s, c): return {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": t, "weight": "bold", "size": "xxl", "color": c["primary"], "align": "center"}] + ([{"type": "text", "text": s, "size": "sm", "color": c["text2"], "align": "center", "margin": "sm"}] if s else []), "spacing": "xs"}
def ftr(b, c): return {"type": "box", "layout": "vertical", "spacing": "sm", "contents": b + [sep(c), {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": c["text2"], "align": "center"}], "backgroundColor": c["bg"], "paddingAll": "15px"}
def bubble(body, footer, c): return {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "spacing": "lg", "contents": body, "backgroundColor": c["bg"], "paddingAll": "20px"}, "footer": footer, "styles": {"body": {"backgroundColor": c["bg"]}, "footer": {"backgroundColor": c["bg"]}}}

def build_home(theme="بنفسجي", username="مستخدم", points=0, is_registered=False):
    c = THEMES.get(theme, THEMES["بنفسجي"])
    user = card([{"type": "text", "text": f"▪️ {username}", "size": "xl", "color": c["text"], "weight": "bold", "align": "center"}, {"type": "box", "layout": "horizontal", "spacing": "md", "contents": [{"type": "text", "text": "▪️ مسجل" if is_registered else "▫️ غير مسجل", "size": "sm", "color": c["success"] if is_registered else c["text2"], "flex": 1}, {"type": "text", "text": f"▪️ {points}", "size": "sm", "color": c["primary"], "align": "end", "flex": 1, "weight": "bold"}], "margin": "md"}], c)
    themes = [row([btn(t, f"ثيم {t}", c, "primary" if t == theme else "secondary", c["primary"] if t == theme else None) for t in list(THEMES.keys())[i:i+3]]) for i in range(0, 9, 3)]
    body = [hdr(BOT_NAME, "بوت الألعاب", c), sep(c), user, {"type": "text", "text": "▪️ اختر ثيمك:", "size": "md", "weight": "bold", "color": c["text"], "margin": "lg"}] + themes
    footer = ftr([row([btn("انضم" if not is_registered else "انسحب", "انضم" if not is_registered else "انسحب", c, "primary", c["success" if not is_registered else "error"]), btn("ألعاب", "العاب", c)]), row([btn("نقاطي", "نقاطي", c), btn("صدارة", "صدارة", c)])], c)
    return FlexMessage(alt_text=f"{BOT_NAME}", contents=FlexContainer.from_dict(bubble(body, footer, c)))

def build_help(theme="بنفسجي"):
    c = THEMES.get(theme, THEMES["بنفسجي"])
    basic = card([{"type": "text", "text": "▪️ الأوامر:", "size": "md", "color": c["text"], "weight": "bold"}, {"type": "text", "text": "▫️ بداية - القائمة\n▫️ العاب - الألعاب\n▫️ نقاطي - نقاطك\n▫️ صدارة - الصدارة\n▫️ انضم - التسجيل\n▫️ انسحب - الإلغاء", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"}], c)
    games = card([{"type": "text", "text": "▪️ اللعب:", "size": "md", "color": c["text"], "weight": "bold"}, {"type": "text", "text": "▫️ لعبة [اسم] - بدء\n▫️ لمح - تلميح\n▫️ جاوب - الإجابة\n▫️ إيقاف - إنهاء", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"}], c)
    body = [hdr("مساعدة", "دليل الاستخدام", c), sep(c), basic, games]
    footer = ftr([row([btn("البداية", "بداية", c, "primary", c["primary"]), btn("ألعاب", "العاب", c)])], c)
    return FlexMessage(alt_text="مساعدة", contents=FlexContainer.from_dict(bubble(body, footer, c)))

def build_games_menu(theme="بنفسجي"):
    c = THEMES.get(theme, THEMES["بنفسجي"])
    games = list(GAMES.items())
    game_btns = [row([btn(v['l'], f"لعبة {k}", c) for k, v in games[i:i+3]]) for i in range(0, len(games), 3)]
    info = card([{"type": "text", "text": "▪️ كيفية اللعب:", "size": "sm", "color": c["text"], "weight": "bold"}, {"type": "text", "text": "اضغط على اسم اللعبة!", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"}], c)
    body = [hdr("الألعاب", f"{len(GAMES)} لعبة", c), sep(c)] + game_btns + [sep(c), info]
    footer = ftr([row([btn("البداية", "بداية", c, "primary", c["primary"]), btn("مساعدة", "مساعدة", c)])], c)
    return FlexMessage(alt_text="الألعاب", contents=FlexContainer.from_dict(bubble(body, footer, c)))

def build_my_points(username, points, theme="بنفسجي"):
    c = THEMES.get(theme, THEMES["بنفسجي"])
    pts = card([{"type": "text", "text": "▪️", "size": "xxl", "align": "center"}, {"type": "text", "text": str(points), "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center", "margin": "md"}, {"type": "text", "text": "نقطة", "size": "md", "color": c["text2"], "align": "center", "margin": "sm"}], c)
    body = [hdr("نقاطي", f"مرحباً {username}", c), sep(c), pts]
    footer = ftr([row([btn("الصدارة", "صدارة", c, "primary", c["primary"]), btn("ألعاب", "العاب", c)]), row([btn("البداية", "بداية", c)])], c)
    return FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(bubble(body, footer, c)))

def build_leaderboard(top_players, theme="بنفسجي"):
    c = THEMES.get(theme, THEMES["بنفسجي"])
    medals = {1: ("🥇", "#FFD700"), 2: ("🥈", "#C0C0C0"), 3: ("🥉", "#CD7F32")}
    players = [card([{"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": medals.get(i, (f"{i}.", c["text"]))[0], "size": "lg", "color": medals.get(i, (f"{i}.", c["text"]))[1], "weight": "bold", "flex": 0, "align": "center"}, {"type": "text", "text": name[:15] + "..." if len(name) > 15 else name, "size": "sm", "color": c["text"], "flex": 3, "margin": "md"}, {"type": "text", "text": f"▪️ {pts}", "size": "sm", "color": c["primary"], "align": "end", "weight": "bold", "flex": 2}]}], c) for i, (name, pts) in enumerate(top_players[:10], 1)]
    if not players: players = [card([{"type": "text", "text": "لا يوجد لاعبون", "size": "md", "color": c["text2"], "align": "center"}], c)]
    body = [hdr("🏆 الصدارة", f"أفضل {len(top_players)}", c), sep(c)] + players
    footer = ftr([row([btn("نقاطي", "نقاطي", c, "primary", c["primary"]), btn("ألعاب", "العاب", c)]), row([btn("البداية", "بداية", c)])], c)
    return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(bubble(body, footer, c)))

def build_registration_required(theme="بنفسجي"):
    c = THEMES.get(theme, THEMES["بنفسجي"])
    alert = card([{"type": "text", "text": "▫️", "size": "xxl", "align": "center"}, {"type": "text", "text": "يجب التسجيل", "size": "xl", "weight": "bold", "color": c["warning"], "align": "center", "margin": "md"}, {"type": "text", "text": "للعب وجمع النقاط، سجل أولاً", "size": "sm", "color": c["text2"], "align": "center", "wrap": True, "margin": "md"}], c)
    body = [hdr("تسجيل", "انضم إلينا", c), sep(c), alert]
    footer = ftr([row([btn("انضم", "انضم", c, "primary", c["success"])]), row([btn("البداية", "بداية", c)])], c)
    return FlexMessage(alt_text="تسجيل", contents=FlexContainer.from_dict(bubble(body, footer, c)))

def build_game_window(game_name, question, theme="بنفسجي", hint=None, timer=None):
    c = THEMES.get(theme, THEMES["بنفسجي"])
    g = GAMES.get(game_name, {})
    q_card = card([{"type": "text", "text": g.get('l', game_name), "size": "lg", "color": c["primary"], "weight": "bold", "align": "center"}, sep(c), {"type": "text", "text": question, "size": "md", "color": c["text"], "wrap": True, "align": "center", "margin": "md"}], c)
    info = []
    if timer: info.append(card([{"type": "text", "text": "⏱️", "size": "xl", "align": "center"}, {"type": "text", "text": f"{timer}s", "size": "lg", "color": c["primary"], "align": "center", "weight": "bold"}], c))
    if hint: info.append(card([{"type": "text", "text": "▪️", "size": "xl", "align": "center"}, {"type": "text", "text": hint, "size": "sm", "color": c["text2"], "align": "center"}], c))
    body = [hdr("جارٍ اللعب", g.get('d', ''), c), sep(c), q_card] + ([{"type": "box", "layout": "horizontal", "spacing": "md", "contents": info}] if info else [])
    footer = ftr([row([btn("تلميح", "لمح", c), btn("الجواب", "جاوب", c)]), row([btn("إيقاف", "إيقاف", c, "secondary", c["error"])])], c)
    return FlexMessage(alt_text=f"لعبة {game_name}", contents=FlexContainer.from_dict(bubble(body, footer, c)))

def build_game_result(is_winner, points_earned, correct_answer, game_name, theme="بنفسجي"):
    c = THEMES.get(theme, THEMES["بنفسجي"])
    g = GAMES.get(game_name, {})
    emoji, title, color, msg = ("▪️", "أحسنت", c["success"], f"ربحت {points_earned} نقطة") if is_winner else ("▫️", "للأسف", c["error"], "حاول مرة أخرى")
    result = card([{"type": "text", "text": emoji, "size": "xxl", "align": "center"}, {"type": "text", "text": title, "size": "xl", "weight": "bold", "color": color, "align": "center", "margin": "md"}, {"type": "text", "text": msg, "size": "md", "color": c["text2"], "align": "center", "margin": "sm"}], c)
    answer = card([{"type": "text", "text": "▪️ الإجابة:", "size": "sm", "color": c["text"], "weight": "bold"}, {"type": "text", "text": correct_answer, "size": "lg", "color": c["primary"], "wrap": True, "margin": "sm", "weight": "bold", "align": "center"}], c)
    body = [hdr("نتيجة", g.get('l', game_name), c), sep(c), result, answer]
    footer = ftr([row([btn(f"▪️ {g.get('l', 'لعب')}", f"لعبة {game_name}", c, "primary", c["primary"])]), row([btn("ألعاب", "العاب", c), btn("البداية", "بداية", c)])], c)
    return FlexMessage(alt_text="نتيجة", contents=FlexContainer.from_dict(bubble(body, footer, c)))

def build_compatibility_result(name1, name2, percentage, theme="بنفسجي"):
    c = THEMES.get(theme, THEMES["بنفسجي"])
    emoji, msg, color = ("▪️", "توافق رائع", c["success"]) if percentage >= 80 else ("▪️", "توافق جيد", c["primary"]) if percentage >= 60 else ("▫️", "توافق متوسط", c["warning"]) if percentage >= 40 else ("▫️", "توافق ضعيف", c["error"])
    result = card([{"type": "text", "text": emoji, "size": "xxl", "align": "center"}, {"type": "text", "text": f"{percentage}%", "size": "xxl", "weight": "bold", "color": color, "align": "center", "margin": "md"}, {"type": "text", "text": msg, "size": "md", "color": c["text2"], "align": "center", "margin": "sm"}], c)
    names = card([{"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": name1, "size": "sm", "color": c["text"], "flex": 1, "align": "start", "weight": "bold"}, {"type": "text", "text": "▪️", "size": "md", "flex": 0, "align": "center"}, {"type": "text", "text": name2, "size": "sm", "color": c["text"], "flex": 1, "align": "end", "weight": "bold"}]}], c)
    body = [hdr("نتيجة التوافق", "لعبة التوافق", c), sep(c), names, result]
    footer = ftr([row([btn("▪️ لعبة أخرى", "لعبة توافق", c, "primary", c["primary"])]), row([btn("ألعاب", "العاب", c), btn("البداية", "بداية", c)])], c)
    return FlexMessage(alt_text="التوافق", contents=FlexContainer.from_dict(bubble(body, footer, c)))

def get_quick_reply():
    return QuickReply(items=[QuickReplyItem(action=MessageAction(label=b["label"], text=b["text"])) for b in QUICK_BUTTONS])

def send_text_with_quick_reply(text):
    return TextMessage(text=text, quick_reply=get_quick_reply())
