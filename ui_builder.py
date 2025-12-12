# ui_builder.py
from typing import Dict, List, Optional
from linebot.v3.messaging import (
    FlexMessage, FlexContainer, TextMessage, 
    QuickReply, QuickReplyItem, MessageAction
)
from config import Config


class UIBuilder:
    """بناء واجهات بوت احترافية بنمط iOS Glassy"""

    def __init__(self):
        self.config = Config

    # ---------------- Quick Reply ثابت ----------------
    def _get_quick_reply(self) -> QuickReply:
        items = [
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
        ]
        return QuickReply(items=items)

    # ---------------- Flex / Text Builder ----------------
    def _create_flex(self, alt_text: str, flex_dict: dict) -> FlexMessage:
        return FlexMessage(
            alt_text=alt_text,
            contents=FlexContainer.from_dict(flex_dict),
            quick_reply=self._get_quick_reply()
        )

    def _create_text(self, text: str) -> TextMessage:
        return TextMessage(text=text, quick_reply=self._get_quick_reply())

    # ---------------- ألوان الثيم ----------------
    def _get_colors(self, theme: Optional[str] = None) -> Dict[str, str]:
        return self.config.get_theme(theme or "فاتح")

    # ---------------- أزرار الألعاب ----------------
    def _build_game_buttons(self, games: List[str], colors: Dict[str,str], primary=True) -> List[dict]:
        rows = []
        for i in range(0, len(games), 3):
            row = {"type": "box","layout": "horizontal","spacing": "sm","margin": "md","contents":[]}
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

    # ---------------- شاشات ----------------
    def home_screen(self, username: str, points: int, is_registered: bool, theme: str) -> FlexMessage:
        c = self._get_colors(theme)
        status = "مسجل" if is_registered else "زائر"
        status_color = c["success"] if is_registered else c["text3"]
        other_theme = "داكن" if theme == "فاتح" else "فاتح"

        flex_dict = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "20px",
                "backgroundColor": c["bg"],
                "contents": [
                    {"type": "text","text": self.config.BOT_NAME,"size": "xxl","weight": "bold","color": c["primary"],"align": "center"},
                    {"type": "text","text": f"v{self.config.VERSION}","size": "xs","color": c["text3"],"align": "center","margin": "xs"},
                    {"type": "separator","margin": "md","color": c["border"]},
                    {
                        "type": "box","layout": "vertical","backgroundColor": c["card"],
                        "cornerRadius": "16px","paddingAll": "16px","margin": "md",
                        "contents":[
                            {"type": "text","text": username[:30],"size": "lg","weight": "bold","color": c["text"],"align": "center"},
                            {"type": "text","text": status,"size": "sm","color": status_color,"align": "center","margin": "xs"},
                            {"type": "separator","margin": "xs","color": c["border"]},
                            {
                                "type": "box","layout": "horizontal","margin": "xs",
                                "contents":[
                                    {"type": "text","text": "النقاط","size": "md","color": c["text2"],"flex": 1},
                                    {"type": "text","text": str(points),"size": "xl","weight": "bold","color": c["primary"],"flex": 0,"align": "end"}
                                ]
                            }
                        ]
                    },
                    {"type": "button","style": "secondary","height": "sm","margin": "md","action": {"type": "message","label": f"ثيم {other_theme}","text": f"ثيم {other_theme}"}},
                    {
                        "type": "box","layout": "horizontal","spacing": "sm","margin": "xs",
                        "contents":[
                            {"type":"button","style":"secondary","height":"sm","action":{"type":"message","label":"نقاطي","text":"نقاطي"}},
                            {"type":"button","style":"secondary","height":"sm","action":{"type":"message","label":"صدارة","text":"صدارة"}}
                        ]
                    },
                    {
                        "type": "box","layout": "horizontal","spacing": "sm","margin": "xs",
                        "contents":[
                            {"type":"button","style":"primary","height":"sm","color":c["primary"],"action":{"type":"message","label":"الألعاب","text":"العاب"}},
                            {"type":"button","style":"secondary","height":"sm","action":{"type":"message","label":"مساعدة","text":"مساعدة"}}
                        ]
                    },
                    {"type": "separator","margin":"md","color":c["border"]},
                    {"type": "text","text": self.config.RIGHTS,"size":"xxs","color":c["text3"],"align":"center","wrap":True,"margin":"xs"}
                ]
            }
        }
        return self._create_flex("الرئيسية", flex_dict)

    def games_menu(self, theme: str) -> FlexMessage:
        c = self._get_colors(theme)
        point_games = self.config.POINT_GAMES[:9]
        fun_games = list(self.config.FUN_GAMES.keys())[:6]
        flex_dict = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "20px",
                "backgroundColor": c["bg"],
                "contents":[
                    {"type": "text","text": "الألعاب","size": "xxl","weight": "bold","color": c["primary"],"align": "center"},
                    {"type": "separator","margin": "md","color": c["border"]},
                    {"type": "text","text": "ألعاب النقاط","size": "md","weight": "bold","color": c["text"],"margin": "md"},
                    *self._build_game_buttons(point_games, c, primary=True),
                    {"type": "separator","margin": "lg","color": c["border"]},
                    {"type": "text","text": "ألعاب الترفيه","size": "md","weight": "bold","color": c["text"],"margin": "md"},
                    *self._build_game_buttons(fun_games, c, primary=False),
                    {"type": "separator","margin": "lg","color": c["border"]},
                    {"type": "button","style": "secondary","height": "sm","margin": "md","action":{"type":"message","label":"الرئيسية","text":"بداية"}}
                ]
            }
        }
        return self._create_flex("قائمة الألعاب", flex_dict)

    def registration_prompt(self, theme: str) -> TextMessage:
        return self._create_text("أرسل اسمك للتسجيل في نظام النقاط")

    def registration_success(self, username: str, points: int, theme: str) -> TextMessage:
        return self._create_text(f"✅ تم التسجيل بنجاح!\n\n👤 الاسم: {username}\n⭐ النقاط: {points}")

    def unregister_confirm(self, username: str, points: int, theme: str) -> TextMessage:
        return self._create_text(f"تم الانسحاب من النظام\n\n👤 الاسم: {username}\n⭐ النقاط المحفوظة: {points}")

    def game_stopped(self, game_name: str, theme: str) -> TextMessage:
        return self._create_text(f"⏹️ تم إيقاف لعبة {game_name}")
