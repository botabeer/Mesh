# ========================================
# ui_builder.py
# ========================================

from typing import List, Dict, Optional
from config import Config


class UIBuilder:
    """بناء واجهات Flex Message بأسلوب iOS Glass"""

    def __init__(self):
        self.config = Config

    # ------------------------------------
    # Theme helpers
    # ------------------------------------
    def _get_colors(self, theme: str) -> Dict[str, str]:
        return self.config.get_theme(theme)

    # ------------------------------------
    # Base components
    # ------------------------------------
    def _separator(self, theme: str, margin: str = "xl") -> Dict:
        c = self._get_colors(theme)
        return {
            "type": "separator",
            "margin": margin,
            "color": c["separator"]
        }

    def _create_glass_card(self, contents: List, theme: str) -> Dict:
        c = self._get_colors(theme)
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "24px",
                "backgroundColor": c["card"],
                "cornerRadius": "20px"
            }
        }

    def _create_header(
        self,
        title: str,
        subtitle: Optional[str],
        theme: str
    ) -> List:
        c = self._get_colors(theme)

        header = [{
            "type": "text",
            "text": title,
            "size": "xxl",
            "weight": "bold",
            "color": c["text"],
            "align": "center"
        }]

        if subtitle:
            header.append({
                "type": "text",
                "text": subtitle,
                "size": "sm",
                "color": c["text_secondary"],
                "align": "center",
                "margin": "sm"
            })

        header.append(self._separator(theme))
        return header

    def _create_button(
        self,
        label: str,
        text: str,
        style: str,
        theme: str
    ) -> Dict:
        c = self._get_colors(theme)

        color_map = {
            "primary": c["primary"],
            "secondary": c["secondary"],
            "success": c["success"]
        }

        return {
            "type": "button",
            "action": {
                "type": "message",
                "label": label,
                "text": text
            },
            "style": "primary" if style == "primary" else "secondary",
            "color": color_map.get(style, c["primary"]),
            "height": "sm",
            "flex": 1
        }

    def _create_info_row(self, label: str, value: str, theme: str) -> Dict:
        c = self._get_colors(theme)
        return {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
                {
                    "type": "text",
                    "text": label,
                    "size": "sm",
                    "color": c["text_secondary"],
                    "flex": 2
                },
                {
                    "type": "text",
                    "text": value,
                    "size": "sm",
                    "color": c["text"],
                    "weight": "bold",
                    "align": "end",
                    "flex": 1
                }
            ]
        }

    # ------------------------------------
    # Cards
    # ------------------------------------
    def welcome_card(self, name: str, registered: bool, theme: str) -> Dict:
        c = self._get_colors(theme)

        status_text = "مسجل" if registered else "غير مسجل"
        status_color = c["success"] if registered else c["warning"]

        contents = self._create_header(
            f"مرحباً {name}",
            Config.BOT_NAME,
            theme
        )

        contents.append({
            "type": "box",
            "layout": "vertical",
            "margin": "xl",
            "paddingAll": "12px",
            "cornerRadius": "12px",
            "backgroundColor": f"{status_color}22",
            "contents": [{
                "type": "text",
                "text": status_text,
                "align": "center",
                "weight": "bold",
                "color": status_color
            }]
        })

        contents.append(self._separator(theme))

        buttons = [
            self._create_button("الألعاب", "العاب", "primary", theme),
            self._create_button("إحصائياتي", "نقاطي", "secondary", theme),
            self._create_button("الصدارة", "الصدارة", "secondary", theme),
        ]

        if not registered:
            buttons.append(
                self._create_button("تسجيل", "تسجيل", "success", theme)
            )

        contents.append({
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "margin": "xl",
            "contents": buttons
        })

        contents.append({
            "type": "text",
            "text": f"الإصدار {Config.VERSION}",
            "size": "xs",
            "color": c["text_tertiary"],
            "align": "center",
            "margin": "xl"
        })

        return self._create_glass_card(contents, theme)

    def games_menu_card(self, theme: str) -> Dict:
        c = self._get_colors(theme)

        contents = self._create_header("الألعاب المتاحة", None, theme)

        sections = [
            ("ألعاب النقاط", ["ذكاء", "خمن", "ضد", "ترتيب", "رياضيات", "اغنيه"]),
            ("ألعاب التحدي", ["لون", "تكوين", "لعبة", "سلسلة", "اسرع"]),
            ("ألعاب أخرى", ["توافق", "مافيا"]),
        ]

        for title, games in sections:
            contents.append({
                "type": "text",
                "text": title,
                "weight": "bold",
                "margin": "xl",
                "color": c["text"]
            })

            for i in range(0, len(games), 3):
                row = {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "margin": "sm",
                    "contents": [
                        self._create_button(g, g, "secondary", theme)
                        for g in games[i:i + 3]
                    ]
                }
                contents.append(row)

        contents.append(self._separator(theme))
        contents.append(
            self._create_button("العودة للبداية", "بداية", "primary", theme)
        )

        return self._create_glass_card(contents, theme)

    def stats_card(self, name: str, user: Dict, theme: str) -> Dict:
        c = self._get_colors(theme)

        games = user.get("games_played", 0)
        wins = user.get("wins", 0)
        points = user.get("total_points", 0)
        rate = int((wins / games) * 100) if games else 0

        contents = self._create_header("إحصائياتي", name, theme)

        contents.append({
            "type": "box",
            "layout": "vertical",
            "margin": "xl",
            "paddingAll": "20px",
            "cornerRadius": "16px",
            "backgroundColor": f"{c['primary']}11",
            "contents": [
                {
                    "type": "text",
                    "text": str(points),
                    "size": "xxl",
                    "weight": "bold",
                    "align": "center",
                    "color": c["text"]
                },
                {
                    "type": "text",
                    "text": "النقاط الإجمالية",
                    "size": "sm",
                    "align": "center",
                    "color": c["text_secondary"]
                }
            ]
        })

        contents.append(self._separator(theme))
        contents.extend([
            self._create_info_row("عدد الألعاب", str(games), theme),
            self._create_info_row("عدد مرات الفوز", str(wins), theme),
            self._create_info_row("نسبة الفوز", f"{rate}%", theme),
        ])

        contents.append(self._separator(theme))
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "xl",
            "contents": [
                self._create_button("الصدارة", "الصدارة", "secondary", theme),
                self._create_button("البداية", "بداية", "primary", theme),
            ]
        })

        return self._create_glass_card(contents, theme)

    def leaderboard_card(self, leaders: List[tuple], theme: str) -> Dict:
        c = self._get_colors(theme)

        contents = self._create_header("لوحة الصدارة", "أفضل 10 لاعبين", theme)

        if not leaders:
            contents.append({
                "type": "text",
                "text": "لا توجد بيانات حالياً",
                "align": "center",
                "color": c["text_tertiary"],
                "margin": "xl"
            })
        else:
            for i, (name, points) in enumerate(leaders[:10], 1):
                contents.append({
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "sm",
                    "paddingAll": "12px",
                    "cornerRadius": "8px",
                    "backgroundColor": f"{c['primary']}08" if i <= 3 else "transparent",
                    "contents": [
                        {
                            "type": "text",
                            "text": str(i),
                            "weight": "bold",
                            "flex": 0,
                            "color": c["text"]
                        },
                        {
                            "type": "text",
                            "text": name,
                            "flex": 3,
                            "margin": "md",
                            "color": c["text"]
                        },
                        {
                            "type": "text",
                            "text": str(points),
                            "align": "end",
                            "flex": 1,
                            "color": c["text_secondary"]
                        }
                    ]
                })

        contents.append(self._separator(theme))
        contents.append(
            self._create_button("العودة للبداية", "بداية", "primary", theme)
        )

        return self._create_glass_card(contents, theme)

    def help_card(self, theme: str) -> Dict:
        c = self._get_colors(theme)

        contents = self._create_header("المساعدة", Config.BOT_NAME, theme)

        commands = [
            ("بداية", "القائمة الرئيسية"),
            ("العاب", "عرض جميع الألعاب"),
            ("نقاطي", "إحصائياتك"),
            ("الصدارة", "أفضل اللاعبين"),
            ("تسجيل", "التسجيل في النظام"),
            ("مساعدة", "هذه الصفحة"),
        ]

        for cmd, desc in commands:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": cmd,
                        "weight": "bold",
                        "flex": 2,
                        "color": c["text"]
                    },
                    {
                        "type": "text",
                        "text": desc,
                        "flex": 3,
                        "size": "xs",
                        "color": c["text_secondary"]
                    }
                ]
            })

        contents.append(self._separator(theme))
        contents.append({
            "type": "text",
            "text": Config.RIGHTS,
            "size": "xs",
            "align": "center",
            "color": c["text_tertiary"],
            "margin": "xl"
        })

        contents.append(
            self._create_button("العودة للبداية", "بداية", "primary", theme)
        )

        return self._create_glass_card(contents, theme)
