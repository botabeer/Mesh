"""
Bot Mesh - UI Builder v17.1 WHITE THEME FIXED + CAROUSEL HELP
Created by: Abeer Aldosari © 2025
✅ نظام التباين التلقائي للثيم الأبيض
✅ ظلال واضحة وحدود قوية
✅ المساعدة كاروسيل احترافي
✅ جميع النوافذ محسّنة
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from constants import GAME_LIST, DEFAULT_THEME, THEMES, BOT_NAME, BOT_RIGHTS, FIXED_GAME_QR

def _c(theme=None):
    """الحصول على ألوان الثيم"""
    return THEMES.get(theme or DEFAULT_THEME, THEMES[DEFAULT_THEME])

def _glass_box(contents, theme, radius="20px", padding="20px"):
    """صندوق زجاجي مع ظل واضح"""
    c = _c(theme)
    
    box_style = {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "cornerRadius": radius,
        "paddingAll": padding,
        "borderWidth": "2px" if theme == "أبيض" else "1px",
        "borderColor": c["border"]
    }
    
    if theme == "أبيض":
        box_style["backgroundColor"] = c["card"]
    
    return box_style

def _btn(label, text, style="primary", theme=None):
    """زر مع ألوان الثيم وتباين محسّن"""
    c = _c(theme)
    
    btn_config = {
        "type": "button",
        "action": {"type": "message", "label": label, "text": text},
        "style": style,
        "height": "sm"
    }
    
    if style == "primary":
        btn_config["color"] = c["primary"]
    elif style == "secondary":
        btn_config["color"] = c["secondary"]
    else:
        btn_config["color"] = c["text"]
    
    return btn_config

def _flex(alt, bubble):
    """إنشاء Flex Message"""
    return FlexMessage(alt_text=alt, contents=FlexContainer.from_dict(bubble))

def build_games_quick_reply():
    """Quick Reply للألعاب + إيقاف"""
    return QuickReply(items=[
        QuickReplyItem(action=MessageAction(label=item["label"], text=item["text"]))
        for item in FIXED_GAME_QR
    ])

def attach_quick_reply(msg):
    """إضافة Quick Reply لأي رسالة"""
    if msg and hasattr(msg, 'quick_reply'):
        msg.quick_reply = build_games_quick_reply()
    return msg

# ============================================================================
# البداية - محسّنة
# ============================================================================
def build_enhanced_home(username, points, is_registered=True, theme=DEFAULT_THEME):
    c = _c(theme)
    status_text = "مسجل" if is_registered else "غير مسجل"
    
    theme_list = list(THEMES.keys())
    theme_rows = []
    for i in range(0, len(theme_list), 3):
        row_themes = theme_list[i:i+3]
        theme_rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [_btn(t, f"ثيم {t}", "primary" if t==theme else "secondary", theme) for t in row_themes]
        })
    
    join_text = "انسحب" if is_registered else "انضم"
    
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": f"▪️ {BOT_NAME}", "weight": "bold", "size": "xxl", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            _glass_box([
                {"type": "box", "layout": "horizontal", "contents": [
                    {"type": "text", "text": "▪️ نقطة", "size": "md", "color": c["text"], "flex": 2, "weight": "bold"},
                    {"type": "text", "text": status_text, "size": "md", "color": c["text2"], "align": "end", "flex": 1}
                ]},
                {"type": "text", "text": str(points), "size": "xxl", "color": c["primary"], "margin": "sm", "weight": "bold"}
            ], theme, "15px", "15px"),
            
            {"type": "text", "text": "▪️ اختر الثيم", "size": "md", "weight": "bold", "color": c["text"], "margin": "xl"},
            *theme_rows,
            
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "xl", "contents": [
                _btn(f"▪️ {join_text}", join_text, "primary" if is_registered else "secondary", theme),
                _btn("▪️ الألعاب", "ألعاب", "secondary", theme)
            ]},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                _btn("▪️ نقاطي", "نقاطي", "secondary", theme),
                _btn("🏆 الصدارة", "صدارة", "secondary", theme)
            ]},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                _btn("▪️ فريقين", "فريقين", "secondary", theme),
                _btn("▪️ مساعدة", "مساعدة", "secondary", theme)
            ]},
            
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": c["text3"], "align": "center", "margin": "md"}
        ]
    }
    
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    bubble = {"type": "bubble", "size": "mega", "body": body_style}
    return attach_quick_reply(_flex("البداية", bubble))

# ============================================================================
# قائمة الألعاب - Mega Size محسّنة
# ============================================================================
def build_games_menu(theme=DEFAULT_THEME):
    c = _c(theme)
    
    games_order = ["أسرع", "ذكاء", "لعبة", "أغنيه", "خمن", "سلسلة", 
                   "ترتيب", "تكوين", "ضد", "لون", "رياضيات", "توافق"]
    
    game_rows = []
    for i in range(0, 12, 3):
        row = {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": []}
        for j in range(3):
            idx = i + j
            if idx < len(games_order):
                row["contents"].append(_btn(games_order[idx], games_order[idx], "primary", theme))
        game_rows.append(row)
    
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "▪️ الألعاب المتاحة", "weight": "bold", "size": "xl", "color": c["primary"], "align": "center"},
            {"type": "text", "text": "عدد الألعاب: 12", "size": "sm", "color": c["text2"], "align": "center", "margin": "xs"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            *game_rows,
            
            _glass_box([
                {"type": "text", "text": "▪️ أوامر اللعب", "size": "sm", "color": c["text"], "weight": "bold"},
                {"type": "text", "text": "• اضغط على اسم اللعبة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                {"type": "text", "text": "• اكتب 'لمح' للتلميح", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "• اكتب 'جاوب' لكشف الإجابة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "• اكتب 'إيقاف' لإنهاء اللعبة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
            ], theme, "15px", "15px"),
            
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "md", "contents": [
                _btn("▪️ البداية", "بداية", "secondary", theme),
                _btn("▪️ إيقاف", "إيقاف", "secondary", theme)
            ]},
            
            {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": c["text3"], "align": "center", "margin": "sm"}
        ]
    }
    
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    bubble = {"type": "bubble", "size": "mega", "body": body_style}
    return attach_quick_reply(_flex("الألعاب", bubble))

# ============================================================================
# نقاطي - محسّنة
# ============================================================================
def build_my_points(username, points, stats=None, theme=DEFAULT_THEME):
    c = _c(theme)
    level = "▪️ مبتدئ" if points<50 else "▪️ متوسط" if points<150 else "▪️ متقدم" if points<300 else "🏆 محترف"
    
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "▪️ نقاطي", "weight": "bold", "size": "xl", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": f"▪️ {username}", "size": "lg", "color": c["text"], "weight": "bold", "align": "center", "margin": "lg"},
            
            _glass_box([
                {"type": "text", "text": "النقاط الكلية", "size": "sm", "color": c["text2"], "align": "center"},
                {"type": "text", "text": str(points), "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center", "margin": "sm"}
            ], theme, "20px", "25px"),
            
            _glass_box([
                {"type": "text", "text": "المستوى الحالي", "size": "sm", "color": c["text2"], "align": "center"},
                {"type": "text", "text": level, "size": "lg", "weight": "bold", "color": c["success"], "align": "center", "margin": "sm"}
            ], theme, "15px", "15px"),
            
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": "▪️ سيتم حذف بياناتك بعد 30 يوم من عدم النشاط", "size": "xs", "color": c["error"], "wrap": True, "align": "center"},
            
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "md", "contents": [
                _btn("▪️ البداية", "بداية", "secondary", theme),
                _btn("▪️ الألعاب", "ألعاب", "secondary", theme)
            ]},
            
            {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": c["text3"], "align": "center", "margin": "sm"}
        ]
    }
    
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    bubble = {"type": "bubble", "size": "mega", "body": body_style}
    return attach_quick_reply(_flex("نقاطي", bubble))

# ============================================================================
# لوحة الصدارة - محسّنة
# ============================================================================
def build_leaderboard(top_users, theme=DEFAULT_THEME):
    c = _c(theme)
    medals = ["🥇", "🥈", "🥉"]
    
    items = []
    for i, (name, pts, is_online) in enumerate(top_users[:10], 1):
        online_text = "متصل الآن" if is_online else "غير متصل"
        online_color = c["success"] if is_online else c["text3"]
        
        items.append({
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "paddingAll": "sm",
            "borderWidth": "2px" if theme == "أبيض" else "1px",
            "borderColor": c["border"],
            "cornerRadius": "10px",
            "margin": "sm",
            "backgroundColor": c["card"] if theme == "أبيض" else None,
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": medals[i-1] if i<=3 else f"{i}.", "size": "lg", "flex": 0, "color": c["primary"] if i<=3 else c["text"], "weight": "bold"},
                        {"type": "text", "text": name, "size": "sm", "color": c["text"], "flex": 3, "margin": "sm", "weight": "bold"},
                        {"type": "text", "text": str(pts), "size": "sm", "color": c["primary"], "align": "end", "flex": 1, "weight": "bold"}
                    ]
                },
                {
                    "type": "text",
                    "text": online_text,
                    "size": "xxs",
                    "color": online_color,
                    "align": "start",
                    "margin": "xs"
                }
            ]
        })
    
    if not items:
        items = [{"type": "text", "text": "لا يوجد لاعبين مسجلين بعد", "size": "sm", "color": c["text2"], "align": "center"}]
    
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "🏆 لوحة الصدارة", "weight": "bold", "size": "xl", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            {"type": "box", "layout": "vertical", "contents": items, "margin": "lg"},
            
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "md", "contents": [
                _btn("▪️ البداية", "بداية", "secondary", theme),
                _btn("▪️ نقاطي", "نقاطي", "secondary", theme)
            ]},
            
            {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": c["text3"], "align": "center", "margin": "sm"}
        ]
    }
    
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    bubble = {"type": "bubble", "size": "mega", "body": body_style}
    return attach_quick_reply(_flex("الصدارة", bubble))

# ============================================================================
# المساعدة - كاروسيل احترافي 🎨
# ============================================================================
def build_help_window(theme=DEFAULT_THEME):
    """نافذة المساعدة كاروسيل احترافي"""
    c = _c(theme)
    
    # بطاقة 1: مقدمة وأوامر التنقل
    card1_body = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "📚 المساعدة", "weight": "bold", "size": "xl", "color": c["primary"], "align": "center"},
            {"type": "text", "text": "دليل شامل للبوت", "size": "xs", "color": c["text2"], "align": "center", "margin": "xs"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            
            _glass_box([
                {"type": "text", "text": "▪️ أوامر التنقل", "weight": "bold", "color": c["text"], "size": "md"},
                {"type": "text", "text": "• بداية / home", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                {"type": "text", "text": "• ألعاب / games", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "• نقاطي / points", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "• صدارة / leaderboard", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
            ], theme, "12px", "12px"),
            
            {"type": "text", "text": "← اسحب لليسار للمزيد", "size": "xxs", "color": c["accent"], "align": "center", "margin": "md"}
        ]
    }
    if theme == "أبيض":
        card1_body["backgroundColor"] = c["bg"]
    
    # بطاقة 2: أوامر اللعب
    card2_body = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "🎮 أوامر اللعب", "weight": "bold", "size": "xl", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            
            _glass_box([
                {"type": "text", "text": "▪️ بدء اللعب", "weight": "bold", "color": c["text"], "size": "md"},
                {"type": "text", "text": "• [اسم اللعبة] - بدء", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                {"type": "text", "text": "• لمح / hint - تلميح", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "• جاوب / reveal - كشف", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "• إيقاف / stop - إيقاف", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
            ], theme, "12px", "12px"),
            
            _glass_box([
                {"type": "text", "text": "▪️ الحساب", "weight": "bold", "color": c["text"], "size": "md"},
                {"type": "text", "text": "• انضم / join", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                {"type": "text", "text": "• انسحب / leave", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
            ], theme, "12px", "12px")
        ]
    }
    if theme == "أبيض":
        card2_body["backgroundColor"] = c["bg"]
    
    # بطاقة 3: نظام النقاط
    card3_body = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "🏆 نظام النقاط", "weight": "bold", "size": "xl", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            
            _glass_box([
                {"type": "text", "text": "▪️ كسب النقاط", "weight": "bold", "color": c["text"], "size": "md"},
                {"type": "text", "text": "• 1 نقطة لكل إجابة صحيحة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                {"type": "text", "text": "• للمسجلين فقط", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "• إجابة واحدة لكل سؤال", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
            ], theme, "12px", "12px"),
            
            _glass_box([
                {"type": "text", "text": "▪️ المستويات", "weight": "bold", "color": c["text"], "size": "md"},
                {"type": "text", "text": "• 0-49: ▪️ مبتدئ", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                {"type": "text", "text": "• 50-149: ▪️ متوسط", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "• 150-299: ▪️ متقدم", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "• 300+: 🏆 محترف", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
            ], theme, "12px", "12px")
        ]
    }
    if theme == "أبيض":
        card3_body["backgroundColor"] = c["bg"]
    
    # بطاقة 4: وضع الفريقين
    card4_body = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "👥 وضع الفريقين", "weight": "bold", "size": "xl", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            
            _glass_box([
                {"type": "text", "text": "▪️ كيفية اللعب", "weight": "bold", "color": c["text"], "size": "md"},
                {"type": "text", "text": "1. اكتب: فريقين", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                {"type": "text", "text": "2. الجميع يكتب: انضم", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "3. اختر اللعبة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "4. تقسيم تلقائي", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
            ], theme, "12px", "12px"),
            
            _glass_box([
                {"type": "text", "text": "▪️ الميزات", "weight": "bold", "color": c["text"], "size": "md"},
                {"type": "text", "text": "• تقسيم عادل", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                {"type": "text", "text": "• نقاط منفصلة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "• بدون لمح أو جاوب", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                {"type": "text", "text": "• إعلان الفائز", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
            ], theme, "12px", "12px"),
            
            _btn("▪️ البداية", "بداية", "primary", theme)
        ]
    }
    if theme == "أبيض":
        card4_body["backgroundColor"] = c["bg"]
    
    carousel = {
        "type": "carousel",
        "contents": [
            {"type": "bubble", "size": "mega", "body": card1_body},
            {"type": "bubble", "size": "mega", "body": card2_body},
            {"type": "bubble", "size": "mega", "body": card3_body},
            {"type": "bubble", "size": "mega", "body": card4_body}
        ]
    }
    
    return attach_quick_reply(_flex("المساعدة", carousel))

# ============================================================================
# باقي النوافذ - محسّنة
# ============================================================================
def build_registration_required(theme=DEFAULT_THEME):
    c = _c(theme)
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "▪️ يجب التسجيل أولاً", "weight": "bold", "size": "lg", "color": c["warning"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            _glass_box([
                {"type": "text", "text": "اضغط 'انضم' للتسجيل والبدء باللعب", "size": "sm", "color": c["text2"], "align": "center", "wrap": True}
            ], theme, "15px", "15px"),
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg", "contents": [
                _btn("▪️ انضم", "انضم", "primary", theme),
                _btn("▪️ البداية", "بداية", "secondary", theme)
            ]}
        ]
    }
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    bubble = {"type": "bubble", "size": "mega", "body": body_style}
    return attach_quick_reply(_flex("تسجيل مطلوب", bubble))

def build_winner_announcement(username, game_name, round_points, total_points, theme=DEFAULT_THEME):
    c = _c(theme)
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "▪️ مبروك!", "size": "xxl", "weight": "bold", "align": "center", "color": c["success"]},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": f"أنهيت لعبة {game_name}", "size": "lg", "color": c["text"], "align": "center", "wrap": True, "margin": "md", "weight": "bold"},
            
            _glass_box([
                {"type": "text", "text": "النقاط المكتسبة", "size": "sm", "color": c["text2"], "align": "center"},
                {"type": "text", "text": f"+{round_points}", "size": "xxl", "weight": "bold", "color": c["success"], "align": "center", "margin": "sm"}
            ], theme, "20px", "20px"),
            
            {"type": "text", "text": f"▪️ إجمالي: {total_points}", "size": "md", "color": c["text"], "align": "center", "margin": "md", "weight": "bold"},
            
            {"type": "box", "layout": "vertical", "spacing": "sm", "margin": "lg", "contents": [
                _btn(f"▪️ {game_name}", game_name, "primary", theme),
                {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                    _btn("▪️ الألعاب", "ألعاب", "secondary", theme),
                    _btn("▪️ البداية", "بداية", "secondary", theme)
                ]}
            ]}
        ]
    }
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    bubble = {"type": "bubble", "size": "mega", "body": body_style}
    return attach_quick_reply(_flex("فوز", bubble))

def build_theme_selector(theme=DEFAULT_THEME):
    c = _c(theme)
    rows = []
    for i in range(0, len(THEMES), 3):
        rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [_btn(t, f"ثيم {t}", "primary" if t==theme else "secondary", theme) for t in list(THEMES.keys())[i:i+3]]
        })
    
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "▪️ اختر الثيم", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            *rows,
            _btn("▪️ البداية", "بداية", "secondary", theme)
        ]
    }
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    bubble = {"type": "bubble", "size": "mega", "body": body_style}
    return attach_quick_reply(_flex("الثيمات", bubble))

def build_multiplayer_help_window(theme=DEFAULT_THEME):
    c = _c(theme)
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "▪️ وضع الفريقين", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            _glass_box([
                {"type": "text", "text": "1. اكتب 'انضم'", "size": "sm", "color": c["text2"], "weight": "bold"},
                {"type": "text", "text": "2. اختر اللعبة", "size": "sm", "color": c["text2"], "margin": "sm", "weight": "bold"},
                {"type": "text", "text": "3. تقسيم تلقائي", "size": "sm", "color": c["text2"], "margin": "sm", "weight": "bold"}
            ], theme, "15px", "15px"),
            _btn("▪️ انضم", "انضم", "primary", theme)
        ]
    }
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    bubble = {"type": "bubble", "size": "mega", "body": body_style}
    return attach_quick_reply(_flex("فريقين", bubble))

def build_join_confirmation(username, theme=DEFAULT_THEME):
    c = _c(theme)
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "▪️ انضممت", "size": "lg", "weight": "bold", "color": c["success"], "align": "center"},
            {"type": "text", "text": "انتظر اللعبة", "size": "sm", "color": c["text2"], "align": "center", "margin": "md"}
        ]
    }
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    return attach_quick_reply(_flex("انضمام", {"type": "bubble", "size": "mega", "body": body_style}))

def build_error_message(error_text, theme=DEFAULT_THEME):
    c = _c(theme)
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": error_text, "size": "md", "color": c["error"], "align": "center", "wrap": True, "weight": "bold"},
            _btn("▪️ البداية", "بداية", "secondary", theme)
        ]
    }
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    return attach_quick_reply(_flex("خطأ", {"type": "bubble", "size": "mega", "body": body_style}))

def build_game_stopped(game_name, theme=DEFAULT_THEME):
    c = _c(theme)
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "▪️ تم إيقاف اللعبة", "size": "lg", "weight": "bold", "color": c["error"], "align": "center"},
            {"type": "text", "text": f"لعبة {game_name}", "size": "sm", "color": c["text2"], "align": "center", "margin": "sm"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg", "contents": [
                _btn("▪️ الألعاب", "ألعاب", "primary", theme),
                _btn("▪️ البداية", "بداية", "secondary", theme)
            ]}
        ]
    }
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    return attach_quick_reply(_flex("إيقاف", {"type": "bubble", "size": "mega", "body": body_style}))

def build_team_game_end(team_points, theme=DEFAULT_THEME):
    c = _c(theme)
    t1 = team_points.get("team1", 0)
    t2 = team_points.get("team2", 0)
    winner = "الفريق الأول 🥇" if t1>t2 else "الفريق الثاني 🥈" if t2>t1 else "تعادل"
    
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": "🏆 انتهت اللعبة!", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            _glass_box([
                {"type": "box", "layout": "horizontal", "contents": [
                    {"type": "text", "text": f"الفريق 1\n{t1}", "size": "lg", "color": c["primary"], "align": "center", "flex": 1, "weight": "bold"},
                    {"type": "text", "text": "VS", "size": "sm", "color": c["text2"], "align": "center", "flex": 0, "weight": "bold"},
                    {"type": "text", "text": f"الفريق 2\n{t2}", "size": "lg", "color": c["primary"], "align": "center", "flex": 1, "weight": "bold"}
                ]},
                {"type": "text", "text": f"الفائز: {winner}", "size": "md", "weight": "bold", "color": c["success"], "align": "center", "margin": "md"}
            ], theme, "20px", "20px"),
            
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg", "contents": [
                _btn("▪️ الألعاب", "ألعاب", "primary", theme),
                _btn("▪️ البداية", "بداية", "secondary", theme)
            ]}
        ]
    }
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    return attach_quick_reply(_flex("نتيجة", {"type": "bubble", "size": "mega", "body": body_style}))

def build_answer_feedback(message, theme=DEFAULT_THEME):
    """رسالة تأكيد الإجابة"""
    c = _c(theme)
    body_style = {
        "type": "box",
        "layout": "vertical",
        "paddingAll": "20px",
        "contents": [
            {"type": "text", "text": message, "size": "md", "color": c["text"], "align": "center", "wrap": True, "weight": "bold"}
        ]
    }
    if theme == "أبيض":
        body_style["backgroundColor"] = c["bg"]
    
    return attach_quick_reply(_flex("إجابة", {"type": "bubble", "size": "mega", "body": body_style}))

__all__ = [
    'build_enhanced_home', 'build_games_menu', 'build_my_points', 'build_leaderboard',
    'build_help_window', 'build_registration_required', 'build_winner_announcement',
    'build_theme_selector', 'build_multiplayer_help_window', 'attach_quick_reply',
    'build_join_confirmation', 'build_error_message', 'build_game_stopped', 'build_team_game_end',
    'build_answer_feedback'
]
