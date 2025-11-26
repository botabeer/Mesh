import sqlite3
from linebot.models import (
    FlexSendMessage, BubbleContainer, BoxComponent, TextComponent,
    ButtonComponent, URIAction, QuickReply, QuickReplyButton,
    MessageAction
)

# =========================
# قاعدة بيانات الثيمات
# =========================
DB_PATH = "themes.db"

def init_theme_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_themes (
            user_id TEXT PRIMARY KEY,
            theme TEXT
        )
    """)
    conn.commit()
    conn.close()

def set_user_theme(user_id, theme):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO user_themes VALUES (?, ?)", (user_id, theme))
    conn.commit()
    conn.close()

def get_user_theme(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT theme FROM user_themes WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else "default"

# =========================
# الثيمات
# =========================
THEMES = {
    "default": {
        "bg": "#F5F7FA",
        "card": "#FFFFFF",
        "title": "#2C3E50",
        "accent": "#4A90E2"
    },
    "dark": {
        "bg": "#1E1E2E",
        "card": "#2A2A40",
        "title": "#FFFFFF",
        "accent": "#9B59B6"
    },
    "gold": {
        "bg": "#FBF3D1",
        "card": "#FFF5CC",
        "title": "#8E6E00",
        "accent": "#D4AF37"
    }
}

# =========================
# أزرار الألعاب الثابتة
# =========================
def games_quick_reply():
    games = ["ذكاء", "رياضيات", "ألغاز", "كلمات", "سرعة", "ألوان", "أضداد", "سلسلة", "تخمين", "أغنية", "تكوين", "توافق"]
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label=g, text=g))
        for g in games
    ])

# =========================
# القالب الثلاثي الأبعاد العام
# =========================
def base_card(title, body_items, footer_buttons=None, user_id=None):

    theme = THEMES.get(get_user_theme(user_id), THEMES["default"])

    footer = None
    if footer_buttons:
        footer = BoxComponent(
            layout="horizontal",
            spacing="md",
            contents=footer_buttons
        )

    bubble = BubbleContainer(
        size="mega",
        header=BoxComponent(
            layout="vertical",
            backgroundColor=theme["accent"],
            paddingAll="12px",
            contents=[
                TextComponent(
                    text=title,
                    weight="bold",
                    size="xl",
                    align="center",
                    color="#FFFFFF"
                ),
                TextComponent(
                    text="Bot Mesh",
                    size="sm",
                    align="center",
                    color="#ECF0F1"
                )
            ]
        ),
        body=BoxComponent(
            layout="vertical",
            spacing="md",
            backgroundColor=theme["card"],
            paddingAll="18px",
            contents=body_items + [
                TextComponent(
                    text="تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025",
                    size="xs",
                    align="center",
                    color="#95A5A6"
                )
            ]
        ),
        footer=footer
    )

    return FlexSendMessage(
        alt_text=title,
        contents=bubble,
        quick_reply=games_quick_reply()
    )

# =========================
# نافذة البداية
# =========================
def start_ui(user_name, points, user_id=None):
    body = [
        TextComponent(text=f"مرحباً بك {user_name}", weight="bold", size="lg"),
        TextComponent(text="الحالة: مستخدم نشط"),
        TextComponent(text=f"النقاط: {points}"),
        TextComponent(text="اختر الخدمة المطلوبة:")
    ]

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="الألعاب", text="الألعاب")),
        ButtonComponent(style="secondary", action=MessageAction(label="الصدارة", text="الصدارة")),
        ButtonComponent(style="secondary", action=MessageAction(label="المساعدة", text="مساعدة")),
        ButtonComponent(style="secondary", action=MessageAction(label="الثيمات", text="توافق"))
    ]

    return base_card("الواجهة الرئيسية", body, footer, user_id)

# =========================
# نافذة المساعدة
# =========================
def help_ui(user_id=None):
    body = [
        TextComponent(text="دليل استخدام البوت", weight="bold"),
        TextComponent(text="• اختر لعبة من الأزرار السفلية"),
        TextComponent(text="• أجب بكتابة النص فقط"),
        TextComponent(text="• للإيقاف اكتب: إيقاف"),
        TextComponent(text="• يمكنك تغيير الثيم من نافذة التوافق")
    ]

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="الألعاب", text="الألعاب")),
        ButtonComponent(style="secondary", action=MessageAction(label="العودة", text="البداية"))
    ]

    return base_card("المساعدة", body, footer, user_id)

# =========================
# نافذة الألعاب
# =========================
def games_ui(user_id=None):
    body = [
        TextComponent(text="الألعاب المتاحة", weight="bold"),
        TextComponent(text="ذكاء - رياضيات - ألغاز - سرعة"),
        TextComponent(text="ألوان - أضداد - تخمين - توافق")
    ]

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="العودة", text="البداية"))
    ]

    return base_card("الألعاب", body, footer, user_id)

# =========================
# نافذة أثناء اللعب
# =========================
def in_game_ui(game_name, question, round_num, user_id=None):
    body = [
        TextComponent(text=f"اللعبة الحالية: {game_name}", weight="bold"),
        TextComponent(text=f"الجولة رقم: {round_num}"),
        TextComponent(text=question, wrap=True)
    ]

    footer = [
        ButtonComponent(style="secondary", action=MessageAction(label="إيقاف", text="إيقاف"))
    ]

    return base_card("وضع اللعب", body, footer, user_id)

# =========================
# نافذة الصدارة
# =========================
def leaderboard_ui(top_players, user_id=None):
    body = [TextComponent(text="أفضل اللاعبين", weight="bold")]

    for i, p in enumerate(top_players, 1):
        body.append(TextComponent(text=f"{i} - {p['name']} : {p['points']} نقطة"))

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="العودة", text="البداية"))
    ]

    return base_card("الصدارة", body, footer, user_id)

# =========================
# نافذة التوافق (الثيمات)
# =========================
def theme_ui(user_id=None):
    body = [
        TextComponent(text="اختر الثيم المفضل", weight="bold"),
        TextComponent(text="الاختيار يتم حفظه تلقائياً")
    ]

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="افتراضي", text="ثيم افتراضي")),
        ButtonComponent(style="secondary", action=MessageAction(label="داكن", text="ثيم داكن")),
        ButtonComponent(style="secondary", action=MessageAction(label="ذهبي", text="ثيم ذهبي")),
        ButtonComponent(style="secondary", action=MessageAction(label="العودة", text="البداية"))
    ]

    return base_card("التوافق والثيمات", body, footer, user_id)

# =========================
# نافذة نهاية الجولة
# =========================
def end_round_ui(winner_name, points, user_id=None):
    body = [
        TextComponent(text="نهاية الجولة", weight="bold", size="lg"),
        TextComponent(text=f"الفائز: {winner_name}"),
        TextComponent(text=f"النقاط المكتسبة: {points}")
    ]

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="إعادة اللعب", text="إعادة")),
        ButtonComponent(style="secondary", action=MessageAction(label="العودة", text="البداية"))
    ]

    return base_card("نتيجة الجولة", body, footer, user_id)

# =========================
# نافذة الفائز المتعدد
# =========================
def multi_winner_ui(winners, user_id=None):
    body = [TextComponent(text="الفائزون في هذه الجولة", weight="bold")]

    for w in winners:
        body.append(TextComponent(text=f"{w['name']} - {w['points']} نقطة"))

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="جولة جديدة", text="إعادة")),
        ButtonComponent(style="secondary", action=MessageAction(label="العودة", text="البداية"))
    ]

    return base_card("الفائزون", body, footer, user_id)

# تهيئة قاعدة البيانات تلقائياً
init_theme_db()
