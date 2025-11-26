"""
UI Builder - Bot Mesh v7.0
واجهة رسائل LINE (Flex + QuickReply)
اللغة: العربية فقط
ملاحظات:
- لا إيموجي إلا عند الضرورة (▫️ ▪️ ووسام/كأس)
- ثيمات مرتبة حسب التفضيل المطلوب
- أزرار ألعاب ثابتة (Quick Reply)
"""

from linebot.v3.messaging import (
    FlexMessage, FlexContainer,
    QuickReply, QuickReplyButton, MessageAction
)

class UI:
    """
    UI builder لبوت Bot Mesh
    يوفر: صفحات البداية، قائمة الألعاب، المساعدة،
    نافذة السؤال، نتيجة اللعبة، لوحة الصدارة، وإعداد QuickReply.
    """

    # ثيمات (أسماء عربية، ألوان HEX)
    THEMES = {
        "أسود":    {"primary": "#000000", "secondary": "#374151", "bg": "#0F172A", "card": "#111827", "text": "#F9FAFB", "text2": "#D1D5DB"},
        "أبيض":    {"primary": "#111827", "secondary": "#6B7280", "bg": "#FFFFFF", "card": "#F3F4F6", "text": "#0F172A", "text2": "#6B7280"},
        "رمادي":    {"primary": "#6B7280", "secondary": "#9CA3AF", "bg": "#F9FAFB", "card": "#E5E7EB", "text": "#111827", "text2": "#4B5563"},
        "أزرق":     {"primary": "#0EA5E9", "secondary": "#38BDF8", "bg": "#F0F9FF", "card": "#E0F2FE", "text": "#0C4A6E", "text2": "#075985"},
        "بنفسجي":   {"primary": "#7C3AED", "secondary": "#A78BFA", "bg": "#FAF5FF", "card": "#F3E8FF", "text": "#1F2937", "text2": "#6B7280"},
        "وردي":     {"primary": "#DB2777", "secondary": "#F472B6", "bg": "#FFF1F2", "card": "#FFE4EC", "text": "#831843", "text2": "#9D174D"},
        "أصفر":     {"primary": "#F59E0B", "secondary": "#FBBF24", "bg": "#FFFBEB", "card": "#FEF3C7", "text": "#92400E", "text2": "#92400E"},
        "أخضر":     {"primary": "#10B981", "secondary": "#34D399", "bg": "#F0FDF4", "card": "#D1FAE5", "text": "#064E3B", "text2": "#065F46"},
        "بني":      {"primary": "#7C2D12", "secondary": "#B45309", "bg": "#FFFBEB", "card": "#FEF3C7", "text": "#3B1F0F", "text2": "#7C2D12"}
    }

    # ترتيب الألعاب النهائي (حسب طلبك: الأفضل أولاً، "توافق" في الأخير كونه ليس لعبة)
    GAMES_ORDERED = [
        "ذكاء",
        "رياضيات",
        "سرعة",
        "كلمات",
        "ألوان",
        "أضداد",
        "سلسلة",
        "تخمين",
        "أغنية",
        "ترتيب",
        "تكوين",
        "توافق"   # تبقى في الأخير (ليس لعبة تقليدية)
    ]

    # أزرار Quick Reply (ثابتة أسفل الشاشة) - عربي فقط، نص الرسالة يبدأ بـ "لعبة " عند اختيار لعبة
    def get_games_quick_reply(self):
        items = []
        # نعرض أول 10 كأزرار سريعة (تعديل سهل هنا)
        for name in self.GAMES_ORDERED[:10]:
            items.append(
                QuickReplyButton(
                    action=MessageAction(label=name, text=f"لعبة {name}")
                )
            )
        # زر لمعرض الألعاب بالكامل
        items.append(
            QuickReplyButton(
                action=MessageAction(label="قائمة الألعاب", text="العاب")
            )
        )
        return QuickReply(items=items)

    # مساعدة داخلية قصيرة (تستخدم بدون إيموجي)
    def _separator(self, color):
        return {"type": "separator", "margin": "lg", "color": color}

    def _create_button(self, label, text, color):
        return {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": "primary",
            "color": color,
            "height": "sm"
        }

    # الصفحة الرئيسية
    def build_home(self, username: str, points: int, theme_name: str = "أزرق") -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": theme["bg"],
                "paddingAll": "20px",
                "contents": [
                    {"type": "text", "text": "Bot Mesh", "size": "xl", "weight": "bold", "color": theme["primary"], "align": "center"},
                    {"type": "text", "text": f"الاسم: {username}", "size": "sm", "color": theme["text2"], "align": "center", "margin": "sm"},
                    {"type": "text", "text": f"النقاط: {points}", "size": "sm", "color": theme["text2"], "align": "center", "margin": "sm"},
                    self._separator(theme["text2"]),
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._create_button("قائمة الألعاب", "العاب", theme["primary"]),
                            self._create_button("نقاطي", "نقاطي", theme["secondary"])
                        ],
                        "spacing": "sm",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            self._create_button("الصدارة", "صدارة", theme["secondary"]),
                            self._create_button("مساعدة", "مساعدة", theme["secondary"])
                        ],
                        "spacing": "sm",
                        "margin": "sm"
                    },
                    {"type": "text", "text": "▫️ النسخة الرسمية — تم إنشاؤه بواسطة عبير الدوسري @ 2025", "size": "xs", "color": theme["text2"], "align": "center", "margin": "md"}
                ]
            }
        }
        msg = FlexMessage(alt_text="البداية — Bot Mesh", contents=FlexContainer.from_dict(bubble))
        # attach quick reply
        msg.quick_reply = self.get_games_quick_reply()
        return msg

    # صفحة قائمة الألعاب (زراير لكل لعبة)
    def build_games_menu(self, theme_name: str = "أزرق") -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        contents = [
            {"type": "text", "text": "قائمة الألعاب", "size": "lg", "weight": "bold", "color": theme["primary"], "align": "center"},
            self._separator(theme["text2"])
        ]

        # زر لكل لعبة بصفوف (صفين كل صف)
        rows = []
        for i in range(0, len(self.GAMES_ORDERED), 2):
            row_games = self.GAMES_ORDERED[i:i+2]
            row_contents = []
            for g in row_games:
                row_contents.append(
                    self._create_button(g, f"لعبة {g}", theme["primary"])
                )
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": row_contents,
                "spacing": "sm",
                "margin": "sm"
            })

        bubble = {"type": "bubble", "size": "mega",
                  "body": {"type": "box", "layout": "vertical", "backgroundColor": theme["bg"], "paddingAll": "20px", "contents": contents},
                  "footer": {"type": "box", "layout": "vertical", "contents": [
                      {"type": "text", "text": "▫️ اختر لعبة للبدء", "size": "xs", "color": theme["text2"], "align": "center"}
                  ], "paddingAll": "12px", "backgroundColor": theme["bg"]}}
        msg = FlexMessage(alt_text="قائمة الألعاب — Bot Mesh", contents=FlexContainer.from_dict(bubble))
        msg.quick_reply = self.get_games_quick_reply()
        return msg

    # صفحة الإحصائيات للمستخدم
    def build_user_stats(self, username: str, stats: dict, rank: int, theme_name: str = "أزرق") -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        bubble = {
            "type": "bubble", "size": "kilo",
            "body": {"type": "box", "layout": "vertical", "backgroundColor": theme["bg"], "paddingAll": "20px",
                     "contents": [
                         {"type": "text", "text": "إحصائياتك", "size": "lg", "weight": "bold", "color": theme["primary"], "align": "center"},
                         {"type": "text", "text": username, "size": "sm", "color": theme["text2"], "align": "center", "margin": "sm"},
                         self._separator(theme["text2"]),
                         {"type": "text", "text": f"النقاط: {stats.get('points',0)}", "size": "md", "weight": "bold", "color": theme["primary"], "align": "center", "margin": "md"},
                         {"type": "box", "layout": "horizontal", "contents": [
                             {"type": "text", "text": f"ألعاب: {stats.get('games_played',0)}", "size": "sm", "color": theme["text"]},
                             {"type": "text", "text": f"فوز: {stats.get('wins',0)}", "size": "sm", "color": theme["text"], "align": "end"},
                             {"type": "text", "text": f"الترتيب: #{rank}", "size": "sm", "color": theme["text"], "align": "end"}
                         ], "spacing": "sm", "margin": "md"}
                     ]}}
        msg = FlexMessage(alt_text="نقاطي — Bot Mesh", contents=FlexContainer.from_dict(bubble))
        msg.quick_reply = self.get_games_quick_reply()
        return msg

    # لوحة الصدارة
    def build_leaderboard(self, top_users: list, theme_name: str = "أزرق") -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        contents = [
            {"type": "text", "text": "لوحة الصدارة", "size": "lg", "weight": "bold", "color": theme["primary"], "align": "center"},
            self._separator(theme["text2"])
        ]
        medals = ["🥇", "🥈", "🥉"]
        for i, u in enumerate(top_users[:10], 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            contents.append({
                "type": "box", "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": medal, "size": "sm", "color": theme["primary"], "flex": 0},
                    {"type": "text", "text": u.get("name","مستخدم"), "size": "sm", "color": theme["text"], "flex": 3, "wrap": True},
                    {"type": "text", "text": str(u.get("points",0)), "size": "sm", "color": theme["primary"], "flex": 1, "align": "end"}
                ],
                "paddingAll": "10px",
                "margin": "sm",
                "backgroundColor": theme["card"] if i <= 3 else "transparent",
                "cornerRadius": "12px"
            })
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "backgroundColor": theme["bg"], "paddingAll": "20px", "contents": contents}}
        msg = FlexMessage(alt_text="لوحة الصدارة — Bot Mesh", contents=FlexContainer.from_dict(bubble))
        msg.quick_reply = self.get_games_quick_reply()
        return msg

    # سؤال اللعبة
    def build_game_question(self, game_name: str, question: str, round_num: int, total_rounds: int, theme_name: str = "أزرق", note: str = None) -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        contents = []
        if note:
            contents.append({"type": "text", "text": note, "size": "sm", "color": theme["primary"], "align": "center", "margin": "sm"})
        contents.extend([
            {"type": "text", "text": f"اللعبة: {game_name}", "size": "sm", "weight": "bold", "color": theme["primary"]},
            {"type": "text", "text": f"الجولة: {round_num} / {total_rounds}", "size": "xs", "color": theme["text2"], "align": "end"},
            self._separator(theme["text2"]),
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": question, "size": "md", "weight": "bold", "color": theme["text"], "align": "center", "wrap": True}
            ], "backgroundColor": theme["card"], "cornerRadius": "12px", "paddingAll": "16px", "margin": "md"}
        ])
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "backgroundColor": theme["bg"], "paddingAll": "18px", "contents": contents},
                  "footer": {"type": "box", "layout": "horizontal", "contents": [
                      self._create_button("تلميح", "لمح", theme["secondary"]),
                      self._create_button("إيقاف", "ايقاف", theme["secondary"])
                  ], "spacing": "sm", "paddingAll": "12px", "backgroundColor": theme["bg"]}}
        msg = FlexMessage(alt_text=f"سؤال — {game_name}", contents=FlexContainer.from_dict(bubble))
        msg.quick_reply = self.get_games_quick_reply()
        return msg

    # نتيجة اللعبة
    def build_game_result(self, game_name: str, total_points: int, theme_name: str = "أزرق") -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        bubble = {"type": "bubble", "size": "kilo",
                  "body": {"type": "box", "layout": "vertical", "backgroundColor": theme["bg"], "paddingAll": "20px",
                           "contents": [
                               {"type": "text", "text": "انتهت اللعبة", "size": "lg", "weight": "bold", "color": theme["primary"], "align": "center"},
                               self._separator(theme["text2"]),
                               {"type": "text", "text": f"مجموع النقاط: {total_points}", "size": "md", "weight": "bold", "color": theme["text"], "align": "center", "margin": "md"}
                           ]},
                  "footer": {"type": "box", "layout": "horizontal", "contents": [
                      self._create_button("إعادة تشغيل", f"لعبة {game_name}", theme["primary"]),
                      self._create_button("قائمة الألعاب", "العاب", theme["secondary"])
                  ], "spacing": "sm", "paddingAll": "12px", "backgroundColor": theme["bg"]}}
        msg = FlexMessage(alt_text="النتيجة — Bot Mesh", contents=FlexContainer.from_dict(bubble))
        msg.quick_reply = self.get_games_quick_reply()
        return msg

    # شاشة المساعدة التفصيلية
    def build_help(self, theme_name: str = "أزرق") -> FlexMessage:
        theme = self.THEMES.get(theme_name, self.THEMES["أزرق"])
        contents = [
            {"type": "text", "text": "دليل الاستخدام", "size": "lg", "weight": "bold", "color": theme["primary"], "align": "center"},
            self._separator(theme["text2"]),
            {"type": "text", "text": "الأوامر الأساسية:", "size": "sm", "weight": "bold", "margin": "md"},
            {"type": "text", "text": "بداية — الرجوع للصفحة الرئيسية\nالعاب — عرض قائمة الألعاب\nنقاطي — عرض الإحصائيات\nصدارة — عرض لوحة الصدارة\nلعبة [اسم] — بدء اللعبة", "size": "sm", "wrap": True, "color": theme["text2"], "margin": "sm"},
            {"type": "text", "text": "خلال اللعب:", "size": "sm", "weight": "bold", "margin": "md"},
            {"type": "text", "text": "لمح — الحصول على تلميح\nايقاف — إيقاف اللعبة", "size": "sm", "wrap": True, "color": theme["text2"], "margin": "sm"}
        ]
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "backgroundColor": theme["bg"], "paddingAll": "20px", "contents": contents}}
        msg = FlexMessage(alt_text="مساعدة — Bot Mesh", contents=FlexContainer.from_dict(bubble))
        msg.quick_reply = self.get_games_quick_reply()
        return msg
