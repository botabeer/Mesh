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
    
    # ================= الثيمات =================
    @staticmethod
    def get_theme(theme):
        """ثيمات فاتح وداكن"""
        if theme == "dark":
            return {
                "bg": "#000000",
                "card": "#1C1C1E",
                "card_secondary": "#2C2C2E",
                "text": "#FFFFFF",
                "text_secondary": "#8E8E93",
                "text_tertiary": "#636366",
                "border": "#38383A",
                "button": "#C7C7CC",
                "button_text": "#000000"
            }
        else:
            return {
                "bg": "#FFFFFF",
                "card": "#E5E5EA",
                "card_secondary": "#D1D1D6",
                "text": "#000000",
                "text_secondary": "#8E8E93",
                "text_tertiary": "#AEAEB2",
                "border": "#C7C7CC",
                "button": "#C7C7CC",
                "button_text": "#000000"
            }

    # ================= Quick Reply =================
    @staticmethod
    def get_quick_reply():
        items = ["سؤال", "منشن", "تحدي", "اعتراف", "شخصية", "حكمه", "موقف", "بدايه", "العاب", "مساعده"]
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
        c = UI.get_theme(theme)
        return [
            {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": title, "size": "lg", "weight": "bold", "color": c["text"], "align": "center", "margin": "lg"}
        ]

    @staticmethod
    def _footer(theme):
        c = UI.get_theme(theme)
        return {
            "type": "text",
            "text": "Bot Mesh | 2025 عبير الدوسري",
            "size": "xxs",
            "color": c["text_secondary"],
            "align": "center",
            "margin": "lg"
        }

    @staticmethod
    def _card(contents, theme, margin="lg"):
        c = UI.get_theme(theme)
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": c["card"],
            "cornerRadius": "12px",
            "paddingAll": "16px",
            "margin": margin
        }

    @staticmethod
    def _button(label, text, theme):
        c = UI.get_theme(theme)
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": "secondary",
            "color": c["button"],
            "height": "sm"
        }

    @staticmethod
    def _bubble(contents, theme, alt):
        c = UI.get_theme(theme)
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
        c = UI.get_theme(theme)
        contents = []
        contents += UI._header("مرحبا بك", theme)
        contents.append(UI._card([
            {"type": "text", "text": "للبدء يرجى التسجيل", "align": "center", "size": "md", "color": c["text"]}
        ], theme))
        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [UI._button("تسجيل", "تسجيل", theme)],
            "margin": "lg"
        })
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "مرحبا بك")

    # ================= Registration =================
    @staticmethod
    def registration_success(name, theme="light"):
        contents = []
        contents += UI._header(f"مرحبا {name}", theme)
        contents.append(UI._card([
            {"type": "text", "text": "تم تسجيلك بنجاح", "align": "center", "size": "md", "color": UI.get_theme(theme)["text"]}
        ], theme))
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "lg",
            "contents": [
                UI._button("بدايه", "بدايه", theme),
                UI._button("العاب", "العاب", theme)
            ]
        })
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "تسجيل ناجح")

    # ================= Main Menu =================
    @staticmethod
    def main_menu(user, db=None):
        theme = user.get("theme", "light")
        c = UI.get_theme(theme)
        contents = []
        contents += UI._header(f"مرحبا {user['name']}", theme)

        contents.append(UI._card([
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": "النقاط", "color": c["text"], "size": "sm"},
                {"type": "text", "text": str(user["points"]), "align": "end", "color": c["text"], "size": "sm", "weight": "bold"}
            ]},
            {"type": "box", "layout": "horizontal", "margin": "sm", "contents": [
                {"type": "text", "text": "الالعاب", "color": c["text"], "size": "sm"},
                {"type": "text", "text": str(user["games"]), "align": "end", "color": c["text"], "size": "sm", "weight": "bold"}
            ]},
            {"type": "box", "layout": "horizontal", "margin": "sm", "contents": [
                {"type": "text", "text": "الفوز", "color": c["text"], "size": "sm"},
                {"type": "text", "text": str(user["wins"]), "align": "end", "color": c["text"], "size": "sm", "weight": "bold"}
            ]},
            {"type": "box", "layout": "horizontal", "margin": "sm", "contents": [
                {"type": "text", "text": "السلسله", "color": c["text"], "size": "sm"},
                {"type": "text", "text": str(user["streak"]), "align": "end", "color": c["text"], "size": "sm", "weight": "bold"}
            ]}
        ], theme))

        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "lg",
            "contents": [
                UI._button("انسحب", "انسحب", theme),
                UI._button("تغيير", "تغيير", theme),
                UI._button("تسجيل", "تسجيل", theme)
            ]
        })

        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [
                UI._button("نقاطي", "نقاطي", theme),
                UI._button("الصداره", "الصداره", theme),
                UI._button("انجازات", "انجازات", theme)
            ]
        })

        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "sm",
            "contents": [
                UI._button("ثيم", "ثيم", theme),
                UI._button("مكافأه", "مكافأه", theme),
                UI._button("مساعده", "مساعده", theme)
            ]
        })

        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [UI._button("العاب", "العاب", theme)],
            "margin": "sm"
        })

        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "القائمه الرئيسيه")

    # ================= Games List =================
    @staticmethod
    def games_list(theme="light"):
        games = [
            ("ذكاء", "خمن"),
            ("رياضيات", "ترتيب"),
            ("ضد", "اسرع"),
            ("سلسله", "لعبه"),
            ("اغنيه", "تكوين"),
            ("حرف", "لون"),
            ("توافق", "مافيا")
        ]

        contents = []
        contents += UI._header("اختر لعبه", theme)

        for game1, game2 in games:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm",
                "contents": [
                    UI._button(game1, game1, theme),
                    UI._button(game2, game2, theme)
                ]
            })

        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "قائمه الالعاب")

    # ================= Game Result =================
    @staticmethod
    def game_result(game_name, score, total, theme="light"):
        c = UI.get_theme(theme)
        percentage = (score / total * 100) if total > 0 else 0
        
        contents = []
        contents += UI._header("نتيجه اللعبه", theme)
        
        contents.append(UI._card([
            {"type": "text", "text": game_name, "align": "center", "size": "lg", "weight": "bold", "color": c["text"]},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "box", "layout": "horizontal", "margin": "md", "contents": [
                {"type": "text", "text": "النتيجه", "color": c["text_secondary"], "size": "sm"},
                {"type": "text", "text": f"{score}/{total}", "align": "end", "color": c["text"], "size": "lg", "weight": "bold"}
            ]},
            {"type": "box", "layout": "horizontal", "margin": "sm", "contents": [
                {"type": "text", "text": "النسبه", "color": c["text_secondary"], "size": "sm"},
                {"type": "text", "text": f"{percentage:.0f}%", "align": "end", "color": c["text"], "size": "lg", "weight": "bold"}
            ]}
        ], theme))
        
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "lg",
            "contents": [
                UI._button("لعب مره اخرى", game_name, theme),
                UI._button("بدايه", "بدايه", theme)
            ]
        })
        
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "نتيجه اللعبه")

    # ================= Help =================
    @staticmethod
    def help_screen(theme="light"):
        c = UI.get_theme(theme)
        contents = []
        contents += UI._header("المساعده", theme)
        
        contents.append(UI._card([
            {"type": "text", "text": "الاوامر الاساسيه", "weight": "bold", "color": c["text"], "size": "md"},
            {"type": "text", "text": "تسجيل - بدايه - العاب", "color": c["text_secondary"], "size": "xs", "margin": "sm", "wrap": True}
        ], theme))
        
        contents.append(UI._card([
            {"type": "text", "text": "الاوامر الاضافيه", "weight": "bold", "color": c["text"], "size": "md"},
            {"type": "text", "text": "نقاطي - الصداره - انجازات", "color": c["text_secondary"], "size": "xs", "margin": "sm", "wrap": True},
            {"type": "text", "text": "ثيم - مكافأه - انسحب - تغيير", "color": c["text_secondary"], "size": "xs", "margin": "xs", "wrap": True}
        ], theme))
        
        contents.append(UI._card([
            {"type": "text", "text": "اوامر المحتوى", "weight": "bold", "color": c["text"], "size": "md"},
            {"type": "text", "text": "سؤال - منشن - تحدي - اعتراف", "color": c["text_secondary"], "size": "xs", "margin": "sm", "wrap": True},
            {"type": "text", "text": "شخصيه - حكمه - موقف", "color": c["text_secondary"], "size": "xs", "margin": "xs", "wrap": True}
        ], theme))
        
        contents.append(UI._button("بدايه", "بدايه", theme))
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "المساعده")

    # ================= User Stats =================
    @staticmethod
    def user_stats(user):
        theme = user.get("theme", "light")
        c = UI.get_theme(theme)
        rate = (user["wins"] / user["games"] * 100) if user["games"] else 0

        contents = []
        contents += UI._header("احصائياتي", theme)
        contents.append(UI._card([
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": "الاسم", "color": c["text_secondary"], "size": "sm"},
                {"type": "text", "text": user['name'], "align": "end", "color": c["text"], "size": "sm", "weight": "bold"}
            ]},
            {"type": "box", "layout": "horizontal", "margin": "sm", "contents": [
                {"type": "text", "text": "النقاط", "color": c["text_secondary"], "size": "sm"},
                {"type": "text", "text": str(user['points']), "align": "end", "color": c["text"], "size": "sm", "weight": "bold"}
            ]},
            {"type": "box", "layout": "horizontal", "margin": "sm", "contents": [
                {"type": "text", "text": "نسبه الفوز", "color": c["text_secondary"], "size": "sm"},
                {"type": "text", "text": f"{rate:.1f}%", "align": "end", "color": c["text"], "size": "sm", "weight": "bold"}
            ]},
            {"type": "box", "layout": "horizontal", "margin": "sm", "contents": [
                {"type": "text", "text": "افضل سلسله", "color": c["text_secondary"], "size": "sm"},
                {"type": "text", "text": str(user.get('best_streak', 0)), "align": "end", "color": c["text"], "size": "sm", "weight": "bold"}
            ]}
        ], theme))
        contents.append(UI._button("بدايه", "بدايه", theme))
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "احصائياتي")

    # ================= Leaderboard =================
    @staticmethod
    def leaderboard(leaders, theme="light"):
        c = UI.get_theme(theme)
        contents = []
        contents += UI._header("لوحه الصداره", theme)

        for i, u in enumerate(leaders[:10], 1):
            medal = str(i)
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "backgroundColor": c["card"],
                "cornerRadius": "8px",
                "paddingAll": "12px",
                "margin": "xs",
                "contents": [
                    {"type": "text", "text": medal, "size": "sm", "weight": "bold", "color": c["text"], "flex": 0, "align": "center"},
                    {"type": "text", "text": u['name'], "size": "sm", "color": c["text"], "margin": "md", "flex": 1},
                    {"type": "text", "text": f"{u['points']} نقطه", "size": "sm", "color": c["text_secondary"], "align": "end", "flex": 0}
                ]
            })

        contents.append(UI._button("بدايه", "بدايه", theme))
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "لوحه الصداره")

    # ================= Achievements =================
    @staticmethod
    def achievements_list(user_achievements, theme="light"):
        c = UI.get_theme(theme)
        contents = []
        contents += UI._header("الانجازات", theme)

        for aid, ach in Config.ACHIEVEMENTS.items():
            unlocked = aid in user_achievements
            status_color = c["text"] if unlocked else c["text_tertiary"]
            
            contents.append({
                "type": "box",
                "layout": "vertical",
                "backgroundColor": c["card"],
                "cornerRadius": "8px",
                "paddingAll": "12px",
                "margin": "xs",
                "contents": [
                    {"type": "text", "text": ach["name"], "weight": "bold", "color": status_color, "size": "sm"},
                    {"type": "text", "text": ach["desc"], "size": "xs", "color": c["text_secondary"], "margin": "xs", "wrap": True},
                    {"type": "text", "text": f"+{ach['points']} نقطه" if unlocked else "مقفل", "size": "xs", "color": status_color, "margin": "xs"}
                ]
            })

        contents.append(UI._button("بدايه", "بدايه", theme))
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "الانجازات")

    # ================= Achievement Unlocked =================
    @staticmethod
    def achievement_unlocked(achievement, theme="light"):
        c = UI.get_theme(theme)
        contents = []
        contents += UI._header("انجاز جديد", theme)
        contents.append(UI._card([
            {"type": "text", "text": achievement["name"], "weight": "bold", "align": "center", "size": "lg", "color": c["text"]},
            {"type": "text", "text": achievement["desc"], "align": "center", "size": "sm", "color": c["text_secondary"], "margin": "sm", "wrap": True},
            {"type": "text", "text": f"+{achievement['points']} نقطه", "align": "center", "size": "md", "color": c["text"], "margin": "md", "weight": "bold"}
        ], theme))
        contents.append(UI._footer(theme))
        return UI._bubble(contents, theme, "انجاز جديد")
