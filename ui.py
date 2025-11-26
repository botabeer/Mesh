from linebot.models import (
    FlexSendMessage, BubbleContainer, BoxComponent,
    TextComponent, ButtonComponent,
    QuickReply, QuickReplyButton, MessageAction
)

BOT_NAME = "Bot Mesh"
BOT_FOOTER = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

# =========================================================
# ✅ أزرار الألعاب الثابتة (Quick Reply دائم)
# =========================================================
def games_quick_reply():
    games = [
        "ذكاء", "رياضيات", "ألغاز", "كلمات", "سرعة", "ألوان",
        "أضداد", "سلسلة", "تخمين", "أغنية", "تكوين", "توافق"
    ]
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label=g, text=g))
        for g in games
    ])

# =========================================================
# ✅ القالب الثلاثي الأبعاد الموحد لكامل البطاقات
# =========================================================
def base_card(title, body_items, footer_buttons=None, note=None):

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
            backgroundColor="#F4F7FB",
            paddingAll="18px",
            contents=[
                TextComponent(
                    text=title,
                    weight="bold",
                    size="xl",
                    align="center",
                    color="#2C3E50"
                ),
                TextComponent(
                    text=BOT_NAME,
                    size="sm",
                    align="center",
                    color="#5D6D7E"
                )
            ]
        ),
        body=BoxComponent(
            layout="vertical",
            spacing="md",
            backgroundColor="#FFFFFF",
            paddingAll="20px",
            contents=body_items
        ),
        footer=footer
    )

    if note:
        body_items.append(
            TextComponent(
                text=note,
                size="xs",
                color="#7F8C8D",
                align="center",
                margin="lg"
            )
        )

    return FlexSendMessage(
        alt_text=title,
        contents=bubble,
        quick_reply=games_quick_reply()
    )

# =========================================================
# ✅ نافذة البداية (3D فخمة)
# =========================================================
def start_ui(user_name, points):
    body = [
        TextComponent(text=f"المستخدم: {user_name}", weight="bold"),
        TextComponent(text="الحالة: نشط", color="#27AE60"),
        TextComponent(text=f"النقاط: {points}", color="#F39C12"),
        TextComponent(text="اختر أحد الأقسام التالية:", weight="bold", margin="md")
    ]

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="الألعاب", text="الألعاب")),
        ButtonComponent(style="secondary", action=MessageAction(label="الصدارة", text="الصدارة")),
        ButtonComponent(style="secondary", action=MessageAction(label="المساعدة", text="مساعدة"))
    ]

    return base_card("الواجهة الرئيسية", body, footer, BOT_FOOTER)

# =========================================================
# ✅ نافذة المساعدة (نفس ستايل البطاقات المصورة)
# =========================================================
def help_ui():
    body = [
        TextComponent(text="دليل الاستخدام", weight="bold"),
        TextComponent(text="اختر لعبة من الأزرار السفلية"),
        TextComponent(text="أرسل إجابتك كتابةً بدون رموز"),
        TextComponent(text="للحصول على تلميح اكتب: لمح"),
        TextComponent(text="لإيقاف اللعب: اكتب إيقاف")
    ]

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="العودة إلى البداية", text="البداية")),
        ButtonComponent(style="secondary", action=MessageAction(label="الألعاب", text="الألعاب"))
    ]

    return base_card("المساعدة", body, footer, BOT_FOOTER)

# =========================================================
# ✅ نافذة الألعاب (شبكة فخمة – ثابتة)
# =========================================================
def games_ui():
    body = [
        TextComponent(text="جميع الألعاب المتاحة:", weight="bold"),
        TextComponent(text="ذكاء – رياضيات – ألغاز – كلمات"),
        TextComponent(text="سرعة – ألوان – أضداد – سلسلة"),
        TextComponent(text="تخمين – أغنية – تكوين – توافق"),
        TextComponent(text="اختر لعبة من الأزرار السفلية", size="sm", color="#7F8C8D")
    ]

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="العودة", text="البداية")),
        ButtonComponent(style="secondary", action=MessageAction(label="المساعدة", text="مساعدة"))
    ]

    return base_card("الألعاب المتاحة", body, footer, BOT_FOOTER)

# =========================================================
# ✅ نافذة أثناء اللعب (ستايل جولات)
# =========================================================
def in_game_ui(game_name, question, round_num):
    body = [
        TextComponent(text=f"اللعبة الحالية: {game_name}", weight="bold"),
        TextComponent(text=f"الجولة: {round_num}"),
        TextComponent(text=question, wrap=True, margin="md"),
        TextComponent(text="اكتب إجابتك أو اكتب لمح للحصول على تلميح", size="sm")
    ]

    footer = [
        ButtonComponent(style="secondary", action=MessageAction(label="إيقاف", text="إيقاف")),
    ]

    return base_card("وضع اللعب", body, footer, BOT_FOOTER)

# =========================================================
# ✅ نافذة نهاية الجولة + الفائز + زر إعادة
# =========================================================
def end_round_ui(winner_name, points):
    body = [
        TextComponent(text="انتهت الجولة", weight="bold"),
        TextComponent(text=f"الفائز: {winner_name}", color="#27AE60"),
        TextComponent(text=f"النقاط المكتسبة: {points}")
    ]

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="إعادة اللعب", text="إعادة")),
        ButtonComponent(style="secondary", action=MessageAction(label="العودة", text="البداية"))
    ]

    return base_card("نهاية الجولة", body, footer, BOT_FOOTER)

# =========================================================
# ✅ نافذة الصدارة (Leaderboard)
# =========================================================
def leaderboard_ui(top_players):
    body = [TextComponent(text="أفضل اللاعبين", weight="bold")]

    for i, p in enumerate(top_players, 1):
        body.append(
            TextComponent(
                text=f"{i} - {p['name']} : {p['points']} نقطة"
            )
        )

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="العودة", text="البداية"))
    ]

    return base_card("الصدارة", body, footer, BOT_FOOTER)

# =========================================================
# ✅ نافذة التوافق (أسلوب مستقل وفخم)
# =========================================================
def compatibility_ui(name1, name2, percentage):
    body = [
        TextComponent(text="تحليل التوافق", weight="bold"),
        TextComponent(text=f"الاسم الأول: {name1}"),
        TextComponent(text=f"الاسم الثاني: {name2}"),
        TextComponent(text=f"نسبة التوافق: {percentage} %", weight="bold")
    ]

    footer = [
        ButtonComponent(style="primary", action=MessageAction(label="إعادة الحساب", text="توافق")),
        ButtonComponent(style="secondary", action=MessageAction(label="العودة", text="البداية"))
    ]

    return base_card("نظام التوافق", body, footer, BOT_FOOTER)
