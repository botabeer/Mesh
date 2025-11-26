"""
UI Builder - Bot Mesh v7.0 - 3D FINAL VERSION
واجهات LINE Flex Messages
تصميم Neumorphism Soft 3D + Quick Reply ثابت
"""

from linebot.v3.messaging import (
    FlexMessage, FlexContainer
)

# محاولة استيراد Quick Reply بأمان
try:
    from linebot.v3.messaging import QuickReply, QuickReplyItem, MessageAction
    QR_AVAILABLE = True
except:
    QR_AVAILABLE = False


class UI:

    THEMES = {
        "أزرق": {
            "primary": "#5B8DEF",
            "secondary": "#9AB8FF",
            "bg": "#EAF0F9",
            "card": "#F5F8FC",
            "shadow": "#C9D4E3",
            "text": "#1E293B",
            "text2": "#64748B",
            "success": "#22C55E",
            "error": "#EF4444"
        }
    }

    GAMES_ORDERED = [
        "ذكاء", "رياضيات", "سرعة", "كلمات", "ألوان", "أضداد",
        "سلسلة", "تخمين", "أغنية", "ترتيب", "تكوين", "إنسان حيوان", "توافق"
    ]

    # -----------------------
    # Quick Reply الثابت
    # -----------------------
    def _quick_reply(self):
        if not QR_AVAILABLE:
            return None

        items = []
        for game in self.GAMES_ORDERED[:8]:
            items.append(
                QuickReplyItem(
                    action=MessageAction(label=game, text=f"لعبة {game}")
                )
            )

        items += [
            QuickReplyItem(action=MessageAction(label="الألعاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="صدارة")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة")),
            QuickReplyItem(action=MessageAction(label="إيقاف", text="إيقاف")),
        ]

        return QuickReply(items=items)

    def _separator(self):
        return {"type": "separator", "margin": "lg", "color": "#CBD5E1"}

    def _card(self, contents, theme):
        return {
            "type": "box",
            "layout": "vertical",
            "backgroundColor": theme["card"],
            "cornerRadius": "20px",
            "paddingAll": "18px",
            "contents": contents
        }

    def _button(self, label, text, color):
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": "primary",
            "color": color,
            "height": "sm"
        }

    # -----------------------
    # نافذة البداية 3D
    # -----------------------
    def build_home(self, username, points):
        theme = self.THEMES["أزرق"]

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "paddingAll": "25px",
                "contents": [
                    {"type": "text", "text": "Bot Mesh", "weight": "bold", "size": "xl", "align": "center", "color": theme["text"]},
                    {"type": "text", "text": "بوت الألعاب الترفيهي الذكي", "size": "sm", "align": "center", "color": theme["text2"], "margin": "sm"},
                    self._separator(),

                    self._card([
                        {"type": "text", "text": f"المستخدم: {username}", "size": "md", "color": theme["text"]},
                        {"type": "text", "text": f"النقاط: {points}", "size": "md", "color": theme["primary"], "margin": "sm"}
                    ], theme),

                    {"type": "box", "layout": "horizontal", "spacing": "md", "margin": "lg", "contents": [
                        self._button("الألعاب", "العاب", theme["primary"]),
                        self._button("نقاطي", "نقاطي", theme["secondary"])
                    ]},

                    {"type": "box", "layout": "horizontal", "spacing": "md", "margin": "sm", "contents": [
                        self._button("الصدارة", "صدارة", theme["secondary"]),
                        self._button("مساعدة", "مساعدة", theme["secondary"])
                    ]},

                    {"type": "text", "text": "© Bot Mesh 2025", "size": "xs", "align": "center", "color": theme["text2"], "margin": "lg"}
                ]
            }
        }

        return FlexMessage(
            alt_text="البداية",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=self._quick_reply()
        )

    # -----------------------
    # قائمة الألعاب 3D
    # -----------------------
    def build_games_menu(self):
        theme = self.THEMES["أزرق"]

        rows = []
        for i in range(0, len(self.GAMES_ORDERED), 3):
            row = []
            for g in self.GAMES_ORDERED[i:i+3]:
                row.append(self._button(g, f"لعبة {g}", theme["primary"]))
            rows.append({"type": "box", "layout": "horizontal", "spacing": "md", "contents": row})

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "paddingAll": "25px",
                "contents": [
                    {"type": "text", "text": "قائمة الألعاب", "size": "xl", "weight": "bold", "align": "center"},
                    self._separator(),
                    *rows,
                    {"type": "box", "layout": "horizontal", "spacing": "md", "margin": "lg", "contents": [
                        self._button("البداية", "بداية", theme["secondary"]),
                        self._button("إيقاف", "إيقاف", theme["error"])
                    ]}
                ]
            }
        }

        return FlexMessage(
            alt_text="الألعاب",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=self._quick_reply()
        )

    # -----------------------
    # نافذة المساعدة 3D
    # -----------------------
    def build_help(self):
        theme = self.THEMES["أزرق"]

        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "paddingAll": "25px",
                "contents": [
                    {"type": "text", "text": "دليل الاستخدام", "size": "xl", "weight": "bold", "align": "center"},
                    self._separator(),

                    self._card([
                        {"type": "text", "text": "الأوامر الأساسية", "weight": "bold"},
                        {"type": "text", "text": "بداية - @Bot Mesh. - نقاطي - الصدارة - مساعدة"}
                    ], theme),

                    self._card([
                        {"type": "text", "text": "أثناء اللعب", "weight": "bold"},
                        {"type": "text", "text": "لمح - جـواب - إيقاف"}
                    ], theme),

                    {"type": "box", "layout": "horizontal", "spacing": "md", "margin": "lg", "contents": [
                        self._button("الألعاب", "العاب", theme["secondary"]),
                        self._button("البداية", "بداية", theme["primary"])
                    ]}
                ]
            }
        }

        return FlexMessage(
            alt_text="مساعدة",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=self._quick_reply()
        )
