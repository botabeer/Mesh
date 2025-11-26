"""
Bot Mesh v7.0 - UI
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025
"""

from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyButton,
    MessageAction
)


class UI:

    # ============================================================
    # الثيمات (تسعة ألوان مرتبة حسب الاستخدام)
    # ============================================================
    THEMES = {
        "أسود": {"primary": "#111827", "secondary": "#374151", "bg": "#020617", "card": "#111827", "text": "#FFFFFF"},
        "أبيض": {"primary": "#2563EB", "secondary": "#D1D5DB", "bg": "#FFFFFF", "card": "#F3F4F6", "text": "#111827"},
        "رمادي": {"primary": "#4B5563", "secondary": "#9CA3AF", "bg": "#F9FAFB", "card": "#E5E7EB", "text": "#111827"},
        "أزرق": {"primary": "#2563EB", "secondary": "#60A5FA", "bg": "#EFF6FF", "card": "#DBEAFE", "text": "#111827"},
        "بنفسجي": {"primary": "#7C3AED", "secondary": "#A78BFA", "bg": "#F5F3FF", "card": "#EDE9FE", "text": "#111827"},
        "وردي": {"primary": "#EC4899", "secondary": "#F9A8D4", "bg": "#FDF2F8", "card": "#FCE7F3", "text": "#111827"},
        "أصفر": {"primary": "#CA8A04", "secondary": "#FDE047", "bg": "#FEFCE8", "card": "#FEF3C7", "text": "#111827"},
        "أخضر": {"primary": "#059669", "secondary": "#34D399", "bg": "#ECFDF5", "card": "#D1FAE5", "text": "#111827"},
        "بني": {"primary": "#92400E", "secondary": "#D97706", "bg": "#FFFBEB", "card": "#FEF3C7", "text": "#111827"},
    }

    # ============================================================
    def get_theme(self, name):
        return self.THEMES.get(name, self.THEMES["أبيض"])

    # ============================================================
    def _btn(self, label, text, color):
        return {
            "type": "button",
            "style": "primary",
            "color": color,
            "action": {"type": "message", "label": label, "text": text},
        }

    # ============================================================
    # الأزرار الثابتة أسفل الشاشة
    # ============================================================
    def get_quick_reply(self):
        games = [
            "ذكاء", "رياضيات", "سرعة", "ألوان",
            "أضداد", "سلسلة", "تخمين",
            "أغنية", "كلمات", "توافق"
        ]
        return QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(label=g, text=f"لعبة {g}")
                ) for g in games
            ]
        )

    # ============================================================
    # الصفحة الرئيسية
    # ============================================================
    def build_home(self, username, points, theme_name):
        theme = self.get_theme(theme_name)

        contents = [
            {"type": "text", "text": "Bot Mesh", "weight": "bold", "size": "xl"},
            {"type": "text", "text": f"المستخدم: {username}", "size": "md"},
            {"type": "text", "text": f"النقاط: {points}", "size": "lg"},

            {"type": "separator", "margin": "lg"},

            self._btn("الألعاب", "العاب", theme["primary"]),
            self._btn("نقاطي", "نقاطي", theme["secondary"]),
            self._btn("الصدارة", "صدارة", theme["secondary"]),
            self._btn("تغيير الثيم", "ثيمات", theme["secondary"]),
            self._btn("المساعدة", "مساعدة", theme["secondary"]),
        ]

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "contents": contents,
            },
        }

        return FlexMessage("الرئيسية", FlexContainer.from_dict(bubble))

    # ============================================================
    # قائمة الألعاب
    # ============================================================
    def build_games_menu(self, theme_name):
        theme = self.get_theme(theme_name)

        games = [
            "ذكاء",
            "رياضيات",
            "سرعة",
            "ألوان",
            "أضداد",
            "سلسلة",
            "تخمين",
            "أغنية",
            "كلمات",
            "توافق",
        ]

        contents = [
            {"type": "text", "text": "قائمة الألعاب", "weight": "bold", "size": "xl"},
            {"type": "separator", "margin": "lg"},
        ]

        for game in games:
            contents.append(self._btn(game, f"لعبة {game}", theme["primary"]))

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "contents": contents,
            },
        }

        return FlexMessage("الألعاب", FlexContainer.from_dict(bubble))

    # ============================================================
    # شاشة اختيار الثيم
    # ============================================================
    def build_themes_menu(self):
        contents = [
            {"type": "text", "text": "اختر الثيم", "weight": "bold", "size": "xl"},
            {"type": "separator", "margin": "lg"},
        ]

        for name in self.THEMES.keys():
            contents.append(self._btn(name, f"ثيم {name}", self.THEMES[name]["primary"]))

        bubble = {
            "type": "bubble",
            "body": {"type": "box", "layout": "vertical", "contents": contents},
        }

        return FlexMessage("الثيمات", FlexContainer.from_dict(bubble))

    # ============================================================
    # شاشة النقاط
    # ============================================================
    def build_user_stats(self, username, user_data, rank, theme_name):
        theme = self.get_theme(theme_name)

        contents = [
            {"type": "text", "text": "إحصائيات المستخدم", "weight": "bold", "size": "xl"},
            {"type": "separator", "margin": "lg"},
            {"type": "text", "text": f"الاسم: {username}"},
            {"type": "text", "text": f"النقاط: {user_data['points']}"},
            {"type": "text", "text": f"عدد الألعاب: {user_data['games_played']}"},
            {"type": "text", "text": f"عدد مرات الفوز: {user_data['wins']}"},
            {"type": "text", "text": f"الترتيب: {rank}"},
        ]

        bubble = {
            "type": "bubble",
            "body": {"type": "box", "layout": "vertical", "backgroundColor": theme["bg"], "contents": contents},
        }

        return FlexMessage("الإحصائيات", FlexContainer.from_dict(bubble))

    # ============================================================
    # شاشة الصدارة
    # ============================================================
    def build_leaderboard(self, leaderboard, theme_name):
        theme = self.get_theme(theme_name)

        contents = [
            {"type": "text", "text": "لوحة الصدارة", "weight": "bold", "size": "xl"},
            {"type": "separator", "margin": "lg"},
        ]

        for i, user in enumerate(leaderboard, start=1):
            contents.append(
                {"type": "text", "text": f"{i} ▫️ {user['name']} - {user['points']} نقطة"}
            )

        bubble = {
            "type": "bubble",
            "body": {"type": "box", "layout": "vertical", "backgroundColor": theme["bg"], "contents": contents},
        }

        return FlexMessage("الصدارة", FlexContainer.from_dict(bubble))

    # ============================================================
    # شاشة سؤال اللعبة
    # ============================================================
    def build_game_question(self, game_name, question_text, round_num, total_rounds, theme_name, note=None):
        theme = self.get_theme(theme_name)

        contents = [
            {"type": "text", "text": f"اللعبة: {game_name}", "weight": "bold"},
            {"type": "text", "text": f"الجولة: {round_num} من {total_rounds}"},
            {"type": "separator", "margin": "lg"},
            {"type": "text", "text": question_text, "wrap": True},
        ]

        if note:
            contents.append({"type": "text", "text": note})

        bubble = {
            "type": "bubble",
            "body": {"type": "box", "layout": "vertical", "backgroundColor": theme["bg"], "contents": contents},
        }

        return FlexMessage("سؤال", FlexContainer.from_dict(bubble))

    # ============================================================
    # شاشة نتيجة اللعبة
    # ============================================================
    def build_game_result(self, game_name, points, theme_name):
        theme = self.get_theme(theme_name)

        contents = [
            {"type": "text", "text": "انتهت اللعبة", "weight": "bold", "size": "xl"},
            {"type": "separator", "margin": "lg"},
            {"type": "text", "text": f"اللعبة: {game_name}"},
            {"type": "text", "text": f"النقاط: {points}"},
        ]

        bubble = {
            "type": "bubble",
            "body": {"type": "box", "layout": "vertical", "backgroundColor": theme["bg"], "contents": contents},
        }

        return FlexMessage("النتيجة", FlexContainer.from_dict(bubble))

    # ============================================================
    # شاشة المساعدة
    # ============================================================
    def build_help(self, theme_name):
        theme = self.get_theme(theme_name)

        text = (
            "الأوامر المتاحة:\n"
            "بداية\n"
            "العاب\n"
            "نقاطي\n"
            "صدارة\n"
            "ثيمات\n"
            "لعبة [اسم اللعبة]\n"
            "ايقاف"
        )

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "contents": [
                    {"type": "text", "text": "المساعدة", "weight": "bold", "size": "xl"},
                    {"type": "separator", "margin": "lg"},
                    {"type": "text", "text": text, "wrap": True},
                ],
            },
        }

        return FlexMessage("المساعدة", FlexContainer.from_dict(bubble))
