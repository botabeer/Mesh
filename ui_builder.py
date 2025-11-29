"""
Bot Mesh - UI Builder v13.0 FINAL ENHANCED
Created by: Abeer Aldosari © 2025
✅ حالة الاتصال نصية: "متصل الآن" / "غير متصل"
✅ نوافذ موحدة Mega Size
✅ الإيموجي المحدود: ▫️▪️⏱️🥇🥈🥉🎖️🏅🏆🖤
✅ الثيم يطبق على كل شيء
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from constants import GAME_LIST, DEFAULT_THEME, THEMES, BOT_NAME, BOT_RIGHTS, FIXED_GAME_QR

def _c(theme=None):
    """الحصول على ألوان الثيم"""
    return THEMES.get(theme or DEFAULT_THEME, THEMES[DEFAULT_THEME])

def _glass_box(contents, theme, radius="20px", padding="20px"):
    """صندوق زجاجي"""
    c = _c(theme)
    return {
        "type": "box",
        "layout": "vertical",
        "contents": contents,
        "cornerRadius": radius,
        "paddingAll": padding,
        "borderWidth": "1px",
        "borderColor": c["border"]
    }

def _btn(label, text, style="primary", theme=None):
    """زر مع ألوان الثيم"""
    c = _c(theme)
    return {
        "type": "button",
        "action": {"type": "message", "label": label, "text": text},
        "style": style,
        "height": "sm",
        "color": c["primary"] if style == "primary" else c["text"]
    }

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
# البداية - بدون تغيير
# ============================================================================
def build_enhanced_home(username, points, is_registered=True, theme=DEFAULT_THEME):
    c = _c(theme)
    status_text = "مسجل" if is_registered else "غير مسجل"
    
    # أزرار الثيمات 3×3
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
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {"type": "text", "text": f"▪️ {BOT_NAME}", "weight": "bold", "size": "xxl", "color": c["primary"], "align": "center"},
                {"type": "separator", "margin": "lg", "color": c["border"]},
                
                _glass_box([
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "text", "text": "▪️ نقطة", "size": "md", "color": c["text"], "flex": 2},
                        {"type": "text", "text": status_text, "size": "md", "color": c["text2"], "align": "end", "flex": 1}
                    ]},
                    {"type": "text", "text": str(points), "size": "xxl", "color": c["primary"], "margin": "sm"}
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
    }
    return attach_quick_reply(_flex("البداية", bubble))

# ============================================================================
# قائمة الألعاب - Mega Size
# ============================================================================
def build_games_menu(theme=DEFAULT_THEME):
    c = _c(theme)
    
    # الألعاب بالترتيب المعتمد
    games_order = ["ذكاء", "رياضيات", "تخمين", "سرعة", "كلمات", "سلسلة", 
                   "أضداد", "أغنية", "تكوين", "ألوان", "لعبة", "توافق"]
    
    # إنشاء الأزرار 3×4
    game_rows = []
    for i in range(0, 12, 3):
        row = {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": []}
        for j in range(3):
            idx = i + j
            if idx < len(games_order):
                row["contents"].append(_btn(games_order[idx], games_order[idx], "primary", theme))
        game_rows.append(row)
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
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
    }
    return attach_quick_reply(_flex("الألعاب", bubble))

# ============================================================================
# نقاطي - Mega Size
# ============================================================================
def build_my_points(username, points, stats=None, theme=DEFAULT_THEME):
    c = _c(theme)
    level = "▪️ مبتدئ" if points<50 else "▪️ متوسط" if points<150 else "▪️ متقدم" if points<300 else "🏆 محترف"
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
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
    }
    return attach_quick_reply(_flex("نقاطي", bubble))

# ============================================================================
# لوحة الصدارة - مع حالة نصية
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
            "borderWidth": "1px",
            "borderColor": c["border"],
            "cornerRadius": "10px",
            "margin": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": medals[i-1] if i<=3 else f"{i}.", "size": "lg", "flex": 0, "color": c["primary"] if i<=3 else c["text"]},
                        {"type": "text", "text": name, "size": "sm", "color": c["text"], "flex": 3, "margin": "sm"},
                        {"type": "text", "text": str(pts), "size": "sm", "color": c["primary"], "align": "end", "flex": 1}
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
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {"type": "text", "text": "🏆 لوحة الصدارة", "weight": "bold", "size": "xl", "color": c["primary"], "align": "center"},
                {"type": "separator", "margin": "lg", "color": c["border"]},
                
                _glass_box(items, theme, "20px", "15px"),
                
                {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "md", "contents": [
                    _btn("▪️ البداية", "بداية", "secondary", theme),
                    _btn("▪️ نقاطي", "نقاطي", "secondary", theme)
                ]},
                
                {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "color": c["text3"], "align": "center", "margin": "sm"}
            ]
        }
    }
    return attach_quick_reply(_flex("الصدارة", bubble))

# ============================================================================
# باقي النوافذ - Mega Size موحد
# ============================================================================
def build_registration_required(theme=DEFAULT_THEME):
    c = _c(theme)
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
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
    }
    return attach_quick_reply(_flex("تسجيل مطلوب", bubble))

def build_winner_announcement(username, game_name, round_points, total_points, theme=DEFAULT_THEME):
    c = _c(theme)
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {"type": "text", "text": "▪️ مبروك!", "size": "xxl", "weight": "bold", "align": "center", "color": c["success"]},
                {"type": "separator", "margin": "lg", "color": c["border"]},
                {"type": "text", "text": f"أنهيت لعبة {game_name}", "size": "lg", "color": c["text"], "align": "center", "wrap": True, "margin": "md"},
                
                _glass_box([
                    {"type": "text", "text": "النقاط المكتسبة", "size": "sm", "color": c["text2"], "align": "center"},
                    {"type": "text", "text": f"+{round_points}", "size": "xxl", "weight": "bold", "color": c["success"], "align": "center", "margin": "sm"}
                ], theme, "20px", "20px"),
                
                {"type": "text", "text": f"▪️ إجمالي: {total_points}", "size": "md", "color": c["text"], "align": "center", "margin": "md"},
                
                {"type": "box", "layout": "vertical", "spacing": "sm", "margin": "lg", "contents": [
                    _btn(f"▪️ {game_name}", game_name, "primary", theme),
                    {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                        _btn("▪️ الألعاب", "ألعاب", "secondary", theme),
                        _btn("▪️ البداية", "بداية", "secondary", theme)
                    ]}
                ]}
            ]
        }
    }
    return attach_quick_reply(_flex("فوز", bubble))

def build_help_window(theme=DEFAULT_THEME):
    """نافذة المساعدة المحسّنة ✅"""
    c = _c(theme)
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {"type": "text", "text": "▪️ المساعدة", "weight": "bold", "size": "xl", "color": c["primary"], "align": "center"},
                {"type": "separator", "margin": "lg", "color": c["border"]},
                
                # أوامر التنقل
                _glass_box([
                    {"type": "text", "text": "▪️ أوامر التنقل", "weight": "bold", "color": c["text"], "size": "md"},
                    {"type": "text", "text": "• بداية / home / start", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                    {"type": "text", "text": "• ألعاب / games", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• نقاطي / points", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• صدارة / leaderboard", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• مساعدة / help", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                ], theme, "15px", "15px"),
                
                # أوامر الحساب
                _glass_box([
                    {"type": "text", "text": "▪️ أوامر الحساب", "weight": "bold", "color": c["text"], "size": "md"},
                    {"type": "text", "text": "• انضم / join", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                    {"type": "text", "text": "• انسحب / leave", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                ], theme, "15px", "15px"),
                
                # أوامر اللعب
                _glass_box([
                    {"type": "text", "text": "▪️ أوامر اللعب", "weight": "bold", "color": c["text"], "size": "md"},
                    {"type": "text", "text": "• [اسم اللعبة] - بدء اللعبة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                    {"type": "text", "text": "• لمح / hint - تلميح", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• جاوب / reveal - كشف الإجابة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• إيقاف / stop - إيقاف اللعبة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                ], theme, "15px", "15px"),
                
                # أوامر الفريقين
                _glass_box([
                    {"type": "text", "text": "▪️ أوامر الفريقين (مجموعات)", "weight": "bold", "color": c["text"], "size": "md"},
                    {"type": "text", "text": "• فريقين / teams", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                    {"type": "text", "text": "• انضم - الانضمام", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• ثم اختر اللعبة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                ], theme, "15px", "15px"),
                
                # نظام النقاط
                _glass_box([
                    {"type": "text", "text": "▪️ نظام النقاط", "weight": "bold", "color": c["text"], "size": "md"},
                    {"type": "text", "text": "• 1 نقطة لكل إجابة صحيحة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                    {"type": "text", "text": "• للمسجلين فقط", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• إجابة واحدة لكل سؤال", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                ], theme, "15px", "15px"),
                
                # المستويات
                _glass_box([
                    {"type": "text", "text": "▪️ المستويات", "weight": "bold", "color": c["text"], "size": "md"},
                    {"type": "text", "text": "• 0-49: ▪️ مبتدئ", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                    {"type": "text", "text": "• 50-149: ▪️ متوسط", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• 150-299: ▪️ متقدم", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• 300+: 🏆 محترف", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                ], theme, "15px", "15px"),
                
                # وضع الفريقين
                _glass_box([
                    {"type": "text", "text": "▪️ وضع الفريقين", "weight": "bold", "color": c["text"], "size": "md"},
                    {"type": "text", "text": "1. اكتب: فريقين", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                    {"type": "text", "text": "2. الجميع يكتب: انضم", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "3. اختر اللعبة", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "4. تقسيم تلقائي لفريقين", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                ], theme, "15px", "15px"),
                
                # الميزات
                _glass_box([
                    {"type": "text", "text": "▪️ ميزات الفريقين", "weight": "bold", "color": c["text"], "size": "md"},
                    {"type": "text", "text": "• تقسيم عادل تلقائي", "size": "xs", "color": c["text2"], "wrap": True, "margin": "sm"},
                    {"type": "text", "text": "• نقاط منفصلة لكل فريق", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• بدون لمح أو جاوب", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": "• إعلان الفائز بعد الانتهاء", "size": "xs", "color": c["text2"], "wrap": True, "margin": "xs"}
                ], theme, "15px", "15px"),
                
                _btn("▪️ البداية", "بداية", "primary", theme)
            ]
        }
    }
    return attach_quick_reply(_flex("المساعدة", bubble))

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
    
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
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
    }
    return attach_quick_reply(_flex("الثيمات", bubble))

def build_multiplayer_help_window(theme=DEFAULT_THEME):
    c = _c(theme)
    bubble = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {"type": "text", "text": "▪️ وضع الفريقين", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
                {"type": "separator", "margin": "lg", "color": c["border"]},
                _glass_box([
                    {"type": "text", "text": "1. اكتب 'انضم'", "size": "sm", "color": c["text2"]},
                    {"type": "text", "text": "2. اختر اللعبة", "size": "sm", "color": c["text2"], "margin": "sm"},
                    {"type": "text", "text": "3. تقسيم تلقائي", "size": "sm", "color": c["text2"], "margin": "sm"}
                ], theme, "15px", "15px"),
                _btn("▪️ انضم", "انضم", "primary", theme)
            ]
        }
    }
    return attach_quick_reply(_flex("فريقين", bubble))

def build_join_confirmation(username, theme=DEFAULT_THEME):
    c = _c(theme)
    return attach_quick_reply(_flex("انضمام", {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {"type": "text", "text": "▪️ انضممت", "size": "lg", "weight": "bold", "color": c["success"], "align": "center"},
                {"type": "text", "text": "انتظر اللعبة", "size": "sm", "color": c["text2"], "align": "center", "margin": "md"}
            ]
        }
    }))

def build_error_message(error_text, theme=DEFAULT_THEME):
    c = _c(theme)
    return attach_quick_reply(_flex("خطأ", {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {"type": "text", "text": error_text, "size": "md", "color": c["error"], "align": "center", "wrap": True},
                _btn("▪️ البداية", "بداية", "secondary", theme)
            ]
        }
    }))

def build_game_stopped(game_name, theme=DEFAULT_THEME):
    c = _c(theme)
    return attach_quick_reply(_flex("إيقاف", {
        "type": "bubble",
        "size": "mega",
        "body": {
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
    }))

def build_team_game_end(team_points, theme=DEFAULT_THEME):
    c = _c(theme)
    t1 = team_points.get("team1", 0)
    t2 = team_points.get("team2", 0)
    winner = "الفريق الأول 🥇" if t1>t2 else "الفريق الثاني 🥈" if t2>t1 else "تعادل"
    
    return attach_quick_reply(_flex("نتيجة", {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {"type": "text", "text": "🏆 انتهت اللعبة!", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
                {"type": "separator", "margin": "lg", "color": c["border"]},
                
                _glass_box([
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "text", "text": f"الفريق 1\n{t1}", "size": "lg", "color": c["primary"], "align": "center", "flex": 1},
                        {"type": "text", "text": "VS", "size": "sm", "color": c["text2"], "align": "center", "flex": 0},
                        {"type": "text", "text": f"الفريق 2\n{t2}", "size": "lg", "color": c["primary"], "align": "center", "flex": 1}
                    ]},
                    {"type": "text", "text": f"الفائز: {winner}", "size": "md", "weight": "bold", "color": c["success"], "align": "center", "margin": "md"}
                ], theme, "20px", "20px"),
                
                {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg", "contents": [
                    _btn("▪️ الألعاب", "ألعاب", "primary", theme),
                    _btn("▪️ البداية", "بداية", "secondary", theme)
                ]}
            ]
        }
    }))

def build_answer_feedback(message, theme=DEFAULT_THEME):
    """رسالة تأكيد الإجابة"""
    c = _c(theme)
    return attach_quick_reply(_flex("إجابة", {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {"type": "text", "text": message, "size": "md", "color": c["text"], "align": "center", "wrap": True}
            ]
        }
    }))

__all__ = [
    'build_enhanced_home', 'build_games_menu', 'build_my_points', 'build_leaderboard',
    'build_help_window', 'build_registration_required', 'build_winner_announcement',
    'build_theme_selector', 'build_multiplayer_help_window', 'attach_quick_reply',
    'build_join_confirmation', 'build_error_message', 'build_game_stopped', 'build_team_game_end',
    'build_answer_feedback'
]
