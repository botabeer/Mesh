from typing import Dict, List, Optional
from linebot.v3.messaging import (
    FlexMessage, FlexContainer, TextMessage, 
    QuickReply, QuickReplyItem, MessageAction
)
from config import Config


class UIBuilder:
    def __init__(self):
        self.config = Config

    # ========== Quick Reply الثابت ==========
    def _get_quick_reply(self) -> QuickReply:
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="بداية", text="بداية")),
            QuickReplyItem(action=MessageAction(label="الألعاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="منشن", text="منشن")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="موقف", text="موقف")),
            QuickReplyItem(action=MessageAction(label="اقتباس", text="اقتباس")),
            QuickReplyItem(action=MessageAction(label="توافق", text="توافق"))
        ])

    # ========== إنشاء Flex أو نص ==========
    def _create_flex(self, alt_text: str, flex_dict: dict) -> FlexMessage:
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_dict),
            quick_reply=self._get_quick_reply()
        )

    def _create_text(self, text: str) -> TextMessage:
        return TextMessage(text=text, quick_reply=self._get_quick_reply())

    # ========== ألوان الثيم ==========
    def _get_colors(self, theme: str = None) -> Dict[str, str]:
        return self.config.get_theme(theme)

    # ========== بناء أزرار الألعاب ==========
    def _build_game_buttons(self, games: List[str], colors: Dict[str,str], primary=True) -> List[dict]:
        rows = []
        for i in range(0, len(games), 3):
            row = {
                "type": "box",
                "layout": "horizontal",
                "spacing": 4,
                "margin": 8 if i > 0 else 12,
                "contents": []
            }
            for g in games[i:i+3]:
                row["contents"].append({
                    "type": "button",
                    "style": "primary" if primary else "secondary",
                    "height": "sm",
                    "color": colors["primary"] if primary else None,
                    "action": {"type": "message", "label": g, "text": g}
                })
            rows.append(row)
        return rows

    # ========== شاشة البداية ==========
    def home_screen(self, username: str, points: int, is_registered: bool, theme: str) -> FlexMessage:
        c = self._get_colors(theme)
        status = "مسجل" if is_registered else "زائر"
        status_color = c["success"] if is_registered else c["text3"]
        other_theme = "داكن" if theme == "فاتح" else "فاتح"

        return self._create_flex("الرئيسية", {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": 24,
                "backgroundColor": c["bg"],
                "contents": [
                    {"type": "text","text": self.config.BOT_NAME,"size": "xxl","weight": "bold","color": c["primary"],"align": "center"},
                    {"type": "text","text": f"v{self.config.VERSION}","size": "xs","color": c["text3"],"align": "center","margin": 4},
                    {"type": "separator","margin": 12,"color": c["border"]},
                    {
                        "type": "box","layout": "vertical","backgroundColor": c["card"],
                        "cornerRadius": 16,"paddingAll": 16,"margin": 12,
                        "contents": [
                            {"type": "text","text": username[:30],"size": "lg","weight": "bold","color": c["text"],"align": "center"},
                            {"type": "text","text": status,"size": "sm","color": status_color,"align": "center","margin": 4},
                            {"type": "separator","margin": 4,"color": c["border"]},
                            {
                                "type": "box","layout": "horizontal","margin": 4,
                                "contents": [
                                    {"type": "text","text": "النقاط","size": "md","color": c["text2"],"flex": 1},
                                    {"type": "text","text": str(points),"size": "xl","weight": "bold","color": c["primary"],"flex": 0,"align": "end"}
                                ]
                            }
                        ]
                    },
                    {"type": "button","style": "secondary","height": "sm","margin": 12,"action": {"type": "message","label": f"ثيم {other_theme}","text": f"ثيم {other_theme}"}},
                    {
                        "type": "box","layout": "horizontal","spacing": 4,"margin": 4,
                        "contents": [
                            {"type": "button","style": "secondary","height": "sm","action": {"type": "message","label": "نقاطي","text": "نقاطي"}},
                            {"type": "button","style": "secondary","height": "sm","action": {"type": "message","label": "صدارة","text": "صدارة"}}
                        ]
                    },
                    {
                        "type": "box","layout": "horizontal","spacing": 4,"margin": 4,
                        "contents": [
                            {"type": "button","style": "primary","height": "sm","color": c["primary"],"action": {"type": "message","label": "الألعاب","text": "العاب"}},
                            {"type": "button","style": "secondary","height": "sm","action": {"type": "message","label": "مساعدة","text": "مساعدة"}}
                        ]
                    },
                    {"type": "separator","margin": 12,"color": c["border"]},
                    {"type": "text","text": self.config.RIGHTS,"size": "xxs","color": c["text3"],"align": "center","wrap": True,"margin": 4}
                ]
            }
        })

    # ========== شاشة النقاط ==========
    def my_points(self, username: str, points: int, stats: Optional[Dict], theme: str) -> FlexMessage:
        c = self._get_colors(theme)
        rows = []
        if stats:
            for game, data in list(stats.items())[:5]:
                rows.append({
                    "type": "box",
                    "layout": "horizontal",
                    "margin": 4,
                    "contents": [
                        {"type": "text","text": game,"size": "sm","color": c["text"],"flex": 2},
                        {"type": "text","text": f"{data['plays']} مرة","size": "xs","color": c["text3"],"flex": 1,"align": "end"}
                    ]
                })
        else:
            rows.append({"type": "text","text": "لا توجد إحصائيات","size": "sm","color": c["text3"],"align": "center","wrap": True})

        return self._create_flex("نقاطي", {
            "type": "bubble","size": "mega",
            "body": {"type": "box","layout": "vertical","paddingAll": 20,"backgroundColor": c["bg"],
                "contents": [
                    {"type": "text","text": "إحصائياتي","size": "xl","weight": "bold","color": c["primary"],"align": "center"},
                    {"type": "separator","margin": 12,"color": c["border"]},
                    {"type": "box","layout": "vertical","backgroundColor": c["card"],"cornerRadius": 16,"paddingAll": 16,"margin": 12,
                     "contents":[
                         {"type": "text","text": username[:30],"size": "lg","weight": "bold","color": c["text"],"align": "center"},
                         {"type": "text","text": "إجمالي النقاط","size": "sm","color": c["text2"],"align": "center","margin": 4},
                         {"type": "text","text": str(points),"size": "xxl","weight": "bold","color": c["primary"],"align": "center","margin": 4}
                     ]
                    },
                    {"type": "box","layout": "vertical","backgroundColor": c["card"],"cornerRadius": 16,"paddingAll": 16,"margin": 12,
                     "contents":[
                         {"type": "text","text": "الألعاب الأكثر لعباً","size": "md","weight": "bold","color": c["text"],"align": "center"},
                         {"type": "separator","margin": 4,"color": c["border"]},
                         *rows
                     ]}
                ]
            }
        })

    # ========== لوحة الصدارة ==========
    def leaderboard(self, top_users: List[tuple], theme: str) -> FlexMessage:
        c = self._get_colors(theme)
        rows = []
        for i, (name, pts, reg) in enumerate(top_users[:20], start=1):
            rank_color = c["primary"] if i <=3 else c["text2"]
            rows.append({
                "type": "box","layout": "horizontal","paddingAll": 10,"margin": 4,"backgroundColor": c["card"],"cornerRadius": 10,
                "contents":[
                    {"type": "text","text": str(i),"size": "md","weight": "bold","color": rank_color,"flex": 0},
                    {"type": "text","text": name[:20],"size": "sm","color": c["text"],"flex": 3,"margin": 4},
                    {"type": "text","text": str(pts),"size": "sm","weight": "bold","color": c["primary"],"flex": 1,"align": "end"}
                ]
            })
        return self._create_flex("الصدارة", {
            "type": "bubble","size": "mega",
            "body":{"type":"box","layout":"vertical","paddingAll":20,"backgroundColor":c["bg"],
                    "contents":[
                        {"type":"text","text":"لوحة الصدارة","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
                        {"type":"separator","margin":12,"color":c["border"]},
                        {"type":"box","layout":"vertical","margin":12,"contents":rows}
                    ]}
        })

    # ========== رسائل التسجيل ==========
    def registration_prompt(self, theme: str) -> TextMessage:
        return self._create_text("أرسل اسمك للتسجيل في نظام النقاط")

    def registration_success(self, username: str, points: int, theme: str) -> TextMessage:
        return self._create_text(f"تم التسجيل بنجاح\n\nالاسم: {username}\nالنقاط: {points}")

    def unregister_confirm(self, username: str, points: int, theme: str) -> TextMessage:
        return self._create_text(f"تم الانسحاب من النظام\n\nالاسم: {username}\nالنقاط المحفوظة: {points}")

    def game_stopped(self, game_name: str, theme: str) -> TextMessage:
        return self._create_text(f"تم إيقاف لعبة {game_name}")
