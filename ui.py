from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyItem,
    MessageAction,
    TextMessage
)
from config import Config


class UI:

    # ================= Quick Reply =================
    @staticmethod
    def get_quick_reply():
        items = ["سؤال", "منشن", "تحدي", "اعتراف", "شخصية", "حكمة", "موقف", "بداية", "العاب", "مساعدة"]
        return QuickReply(
            items=[QuickReplyItem(action=MessageAction(label=i, text=i)) for i in items]
        )

    # ================= Text =================
    @staticmethod
    def text_message(text):
        return TextMessage(text=text)

    # ================= Base Components =================
    @staticmethod
    def _header(title, theme):
        c = Config.get_theme(theme)
        return [
            {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": title, "size": "lg", "weight": "bold", "color": c["text"], "align": "center", "margin": "lg"}
        ]

    @staticmethod
    def _footer(theme):
        c = Config.get_theme(theme)
        return {
            "type": "text",
            "text": "تم الانشاء بواسطة عبير الدوسري @ 2025",
            "size": "xxs",
            "color": c["text_secondary"],
            "align": "center",
            "margin": "lg"
        }

    @staticmethod
    def _card(contents, theme, margin="lg"):
        c = Config.get_theme(theme)
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": c["card"],
            "cornerRadius": "10px",
            "paddingAll": "16px",
            "margin": margin
        }

    @staticmethod
    def _button(label, text, theme, style="default"):
        c = Config.get_theme(theme)
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": "primary" if style == "primary" else "secondary",
            "color": c["button"],
            "height": "sm"
        }

    @staticmethod
    def _bubble(contents, theme, alt):
        c = Config.get_theme(theme)
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["bg"],
                "paddingAll": "24px",
                "contents": contents
            }
        }
        return FlexMessage(
            alt_text=alt,
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )

    # ================= Welcome =================
    @staticmethod
    def welcome_screen(theme="light"):
        contents = []
        contents += UI._header("مرحبا بك", theme)
        contents.append(UI._card([
            {"type": "text", "text": "للبدء يرجى التسجيل", "align": "center"}
        ], theme))
        contents.append(UI._button("تسجيل", "تسجيل", theme))
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "مرحبا بك")

    # ================= Registration =================
    @staticmethod
    def registration_success(name, theme="light"):
        contents = []
        contents += UI._header(f"مرحبا {name}", theme)
        contents.append(UI._card([
            {"type": "text", "text": "تم تسجيلك بنجاح", "align": "center"}
        ], theme))
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                UI._button("بداية", "بداية", theme),
                UI._button("العاب", "العاب", theme)
            ]
        })
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "تسجيل ناجح")

    # ================= Main Menu =================
    @staticmethod
    def main_menu(user):
        theme = user.get("theme", "light")
        contents = []
        contents += UI._header(f"مرحبا {user['name']}", theme)

        contents.append(UI._card([
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": "النقاط"},
                {"type": "text", "text": str(user["points"]), "align": "end"}
            ]},
            {"type": "box", "layout": "horizontal", "margin": "sm", "contents": [
                {"type": "text", "text": "الالعاب"},
                {"type": "text", "text": str(user["games"]), "align": "end"}
            ]},
            {"type": "box", "layout": "horizontal", "margin": "sm", "contents": [
                {"type": "text", "text": "الفوز"},
                {"type": "text", "text": str(user["wins"]), "align": "end"}
            ]},
            {"type": "box", "layout": "horizontal", "margin": "sm", "contents": [
                {"type": "text", "text": "السلسلة"},
                {"type": "text", "text": str(user["streak"]), "align": "end"}
            ]}
        ], theme))

        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                UI._button("العاب", "العاب", theme, "primary"),
                UI._button("نقاطي", "نقاطي", theme),
                UI._button("انسحب", "انسحب", theme)
            ]
        })

        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [
                UI._button("الصدارة", "الصدارة", theme),
                UI._button("انجازات", "انجازات", theme),
                UI._button("ثيم", "ثيم", theme)
            ]
        })

        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "القائمة الرئيسية")

    # ================= Games List =================
    @staticmethod
    def games_list(theme="light"):
        games = [
            "خمن", "ذكاء", "ترتيب", "رياضيات",
            "اسرع", "ضد", "سلسلة", "اغنية",
            "تكوين", "لون", "حرف", "مافيا",
            "توافق"
        ]

        contents = []
        contents += UI._header("اختر لعبة", theme)

        for i in range(0, len(games), 2):
            row = [UI._button(g, g, theme) for g in games[i:i+2]]
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm",
                "contents": row
            })

        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "قائمة الالعاب")

    # ================= Compatibility =================
    @staticmethod
    def compatibility_game(theme="light"):
        contents = []
        contents += UI._header("لعبة التوافق", theme)
        contents.append(UI._card([
            {"type": "text", "text": "اكتب اسمين بينهما كلمة و", "align": "center"},
            {"type": "text", "text": "مثال: احمد و سارة", "size": "sm", "align": "center", "margin": "md"}
        ], theme))
        contents.append({"type": "text", "text": "للترفيه فقط - بدون نقاط", "size": "xs", "align": "center"})
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "لعبة التوافق")

    @staticmethod
    def compatibility_result(name1, name2, percentage, message, theme="light"):
        contents = []
        contents += UI._header("نسبة التوافق", theme)
        contents.append(UI._card([
            {"type": "text", "text": f"{name1} و {name2}", "align": "center"},
            {"type": "text", "text": f"{percentage}%", "size": "xxl", "weight": "bold", "align": "center", "margin": "lg"},
            {"type": "text", "text": message, "size": "sm", "align": "center", "margin": "md"}
        ], theme))
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                UI._button("مرة اخرى", "توافق", theme),
                UI._button("بداية", "بداية", theme)
            ]
        })
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "نتيجة التوافق")

    # ================= Help =================
    @staticmethod
    def help_screen(theme="light"):
        contents = []
        contents += UI._header("المساعدة", theme)
        contents.append(UI._card([
            {"type": "text", "text": "الاوامر الاساسية", "weight": "bold"},
            {"type": "text", "text": "تسجيل - بداية - العاب"},
            {"type": "text", "text": "نقاطي - الصدارة - انجازات"},
            {"type": "text", "text": "ثيم - انسحب"}
        ], theme))
        contents.append(UI._button("بداية", "بداية", theme))
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "المساعدة")

    # ================= User Stats =================
    @staticmethod
    def user_stats(user):
        theme = user.get("theme", "light")
        rate = (user["wins"] / user["games"] * 100) if user["games"] else 0

        contents = []
        contents += UI._header("احصائياتي", theme)
        contents.append(UI._card([
            {"type": "text", "text": f"الاسم: {user['name']}"},
            {"type": "text", "text": f"النقاط: {user['points']}"},
            {"type": "text", "text": f"نسبة الفوز: {rate:.1f}%"}
        ], theme))
        contents.append(UI._button("بداية", "بداية", theme))
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "احصائياتي")

    # ================= Leaderboard =================
    @staticmethod
    def leaderboard(leaders, theme="light"):
        contents = []
        contents += UI._header("لوحة الصدارة", theme)

        for i, u in enumerate(leaders[:10], 1):
            contents.append(UI._card([
                {"type": "text", "text": f"{i}. {u['name']} - {u['points']} نقطة"}
            ], theme, margin="sm"))

        contents.append(UI._button("بداية", "بداية", theme))
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "لوحة الصدارة")

    # ================= Achievements =================
    @staticmethod
    def achievements_list(user_achievements, theme="light"):
        contents = []
        contents += UI._header("الانجازات", theme)

        for aid, ach in Config.ACHIEVEMENTS.items():
            unlocked = aid in user_achievements
            contents.append(UI._card([
                {"type": "text", "text": ach["name"], "weight": "bold"},
                {"type": "text", "text": ach["desc"], "size": "xs"},
                {"type": "text", "text": f"+{ach['points']} نقطة" if unlocked else "مقفل", "size": "xs"}
            ], theme, margin="sm"))

        contents.append(UI._button("بداية", "بداية", theme))
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "الانجازات")

    # ================= Achievement Unlocked =================
    @staticmethod
    def achievement_unlocked(achievement, theme="light"):
        contents = []
        contents += UI._header("انجاز جديد", theme)
        contents.append(UI._card([
            {"type": "text", "text": achievement["name"], "weight": "bold", "align": "center"},
            {"type": "text", "text": f"+{achievement['points']} نقطة", "align": "center", "size": "sm"}
        ], theme))
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "انجاز جديد")
