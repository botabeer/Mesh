"""
🎨 Bot Mesh v7.0 - UI Builder
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025
"""

from linebot.v3.messaging import (
    FlexMessage,
    FlexContainer,
    QuickReply,
    QuickReplyButton,
    MessageAction
)

# ============================================================
# ✅ الأزرار الثابتة أسفل الشاشة (Quick Reply)
# ============================================================

def get_quick_reply():
    return QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="🎮 الألعاب", text="العاب")),
        QuickReplyButton(action=MessageAction(label="🧠 ذكاء", text="لعبة ذكاء")),
        QuickReplyButton(action=MessageAction(label="🔢 رياضيات", text="لعبة رياضيات")),
        QuickReplyButton(action=MessageAction(label="⚡ سرعة", text="لعبة سرعة")),
        QuickReplyButton(action=MessageAction(label="🔤 كلمات", text="لعبة كلمات")),
        QuickReplyButton(action=MessageAction(label="🎵 أغنية", text="لعبة أغنية")),
        QuickReplyButton(action=MessageAction(label="🏆 الصدارة", text="صدارة")),
        QuickReplyButton(action=MessageAction(label="📊 نقاطي", text="نقاطي")),
        QuickReplyButton(action=MessageAction(label="ℹ️ مساعدة", text="مساعدة")),
        QuickReplyButton(action=MessageAction(label="⛔ إيقاف", text="ايقاف")),
    ])


class UI:
    """بناء واجهات Flex Messages احترافية"""

    # ============================================================
    # ✅ الثيمات التسعة
    # ============================================================
    THEMES = {
        "💜": {"primary": "#8B5CF6", "secondary": "#A78BFA", "bg": "#FAF5FF", "card": "#F3E8FF", "text": "#1F2937", "text2": "#6B7280"},
        "💚": {"primary": "#10B981", "secondary": "#34D399", "bg": "#F0FDF4", "card": "#D1FAE5", "text": "#1F2937", "text2": "#6B7280"},
        "🤍": {"primary": "#3B82F6", "secondary": "#60A5FA", "bg": "#FFFFFF", "card": "#F3F4F6", "text": "#1F2937", "text2": "#6B7280"},
        "🖤": {"primary": "#8B5CF6", "secondary": "#A78BFA", "bg": "#1F2937", "card": "#374151", "text": "#F9FAFB", "text2": "#D1D5DB"},
        "💙": {"primary": "#0EA5E9", "secondary": "#38BDF8", "bg": "#F0F9FF", "card": "#E0F2FE", "text": "#0C4A6E", "text2": "#075985"},
        "🩶": {"primary": "#6B7280", "secondary": "#9CA3AF", "bg": "#F9FAFB", "card": "#E5E7EB", "text": "#1F2937", "text2": "#6B7280"},
        "🩷": {"primary": "#EC4899", "secondary": "#F472B6", "bg": "#FDF2F8", "card": "#FCE7F3", "text": "#831843", "text2": "#9D174D"},
        "🧡": {"primary": "#F97316", "secondary": "#FB923C", "bg": "#FFF7ED", "card": "#FFEDD5", "text": "#7C2D12", "text2": "#9A3412"},
        "🤎": {"primary": "#92400E", "secondary": "#B45309", "bg": "#FFFBEB", "card": "#FEF3C7", "text": "#451A03", "text2": "#78350F"},
    }

    def get_theme(self, emoji="💜"):
        return self.THEMES.get(emoji, self.THEMES["💜"])

    def _btn(self, label, text, color):
        return {
            "type": "button",
            "style": "primary",
            "color": color,
            "height": "sm",
            "action": {
                "type": "message",
                "label": label,
                "text": text
            }
        }

    def _sep(self, theme):
        return {
            "type": "separator",
            "margin": "lg",
            "color": theme["text2"]
        }

    # ============================================================
    # ✅ الصفحة الرئيسية
    # ============================================================
    def build_home(self, username, points, theme_emoji="💜"):
        theme = self.get_theme(theme_emoji)

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "contents": [
                    {"type": "text", "text": "🎮 Bot Mesh", "size": "xxl", "weight": "bold", "color": theme["primary"], "align": "center"},
                    {"type": "text", "text": "بوت الألعاب التفاعلي", "size": "sm", "color": theme["text2"], "align": "center"},
                    self._sep(theme),
                    {"type": "text", "text": f"👤 {username}", "align": "center", "color": theme["text"]},
                    {"type": "text", "text": f"⭐ نقاطك: {points}", "align": "center", "color": theme["primary"]},
                    self._sep(theme),
                    self._btn("🎮 الألعاب", "العاب", theme["primary"]),
                    self._btn("📊 نقاطي", "نقاطي", theme["secondary"]),
                    self._btn("🏆 الصدارة", "صدارة", theme["secondary"]),
                    self._btn("ℹ️ مساعدة", "مساعدة", theme["secondary"]),
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "contents": [
                    {"type": "text", "text": "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025", "size": "xs", "align": "center", "color": theme["text2"]}
                ]
            }
        }

        return FlexMessage(
            alt_text="Bot Mesh - الصفحة الرئيسية",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=get_quick_reply()
        )

    # ============================================================
    # ✅ قائمة الألعاب
    # ============================================================
    def build_games_menu(self, theme_emoji="💜"):
        theme = self.get_theme(theme_emoji)

        games = [
            "ذكاء", "رياضيات", "سرعة", "كلمات",
            "ألوان", "أضداد", "سلسلة",
            "تخمين", "أغنية", "توافق", "تكوين"
        ]

        contents = [
            {"type": "text", "text": "🎮 قائمة الألعاب", "size": "xl", "weight": "bold", "align": "center", "color": theme["primary"]},
            self._sep(theme),
        ]

        for game in games:
            contents.append(self._btn(f"🎯 {game}", f"لعبة {game}", theme["primary"]))

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "contents": contents,
            }
        }

        return FlexMessage(
            alt_text="قائمة الألعاب",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=get_quick_reply()
        )

    # ============================================================
    # ✅ شاشة المساعدة
    # ============================================================
    def build_help(self, theme_emoji="💜"):
        theme = self.get_theme(theme_emoji)

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "contents": [
                    {"type": "text", "text": "ℹ️ دليل الاستخدام", "size": "xl", "weight": "bold", "align": "center", "color": theme["primary"]},
                    self._sep(theme),
                    {"type": "text", "text":
                        "• بداية\n"
                        "• العاب\n"
                        "• نقاطي\n"
                        "• صدارة\n"
                        "• لعبة [اسم]\n"
                        "• ايقاف\n", "wrap": True, "color": theme["text"]
                    }
                ]
            }
        }

        return FlexMessage(
            alt_text="مساعدة bot",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=get_quick_reply()
        )

    # ============================================================
    # ✅ سؤال أثناء اللعب
    # ============================================================
    def build_game_question(self, game_name, question, round_num, total_rounds, theme_emoji="💜"):
        theme = self.get_theme(theme_emoji)

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "contents": [
                    {"type": "text", "text": f"🎮 {game_name}", "size": "lg", "weight": "bold", "align": "center", "color": theme["primary"]},
                    {"type": "text", "text": f"{round_num}/{total_rounds}", "align": "center", "color": theme["text2"]},
                    self._sep(theme),
                    {"type": "text", "text": question, "size": "lg", "align": "center", "wrap": True, "color": theme["text"]},
                ]
            }
        }

        return FlexMessage(
            alt_text=f"سؤال {game_name}",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=get_quick_reply()
        )

    # ============================================================
    # ✅ نتيجة اللعبة
    # ============================================================
    def build_game_result(self, game_name, total_points, theme_emoji="💜"):
        theme = self.get_theme(theme_emoji)

        bubble = {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "contents": [
                    {"type": "text", "text": "🎉 انتهت اللعبة!", "size": "xl", "weight": "bold", "align": "center", "color": theme["primary"]},
                    {"type": "text", "text": f"✅ {game_name}", "align": "center"},
                    self._sep(theme),
                    {"type": "text", "text": f"⭐ مجموع نقاطك: {total_points}", "size": "lg", "align": "center"}
                ]
            }
        }

        return FlexMessage(
            alt_text="نتيجة اللعبة",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=get_quick_reply()
        )
