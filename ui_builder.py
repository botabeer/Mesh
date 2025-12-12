# ui_builder.py
from typing import Dict, List, Optional
from linebot.v3.messaging import (
    FlexMessage, FlexContainer, TextMessage, 
    QuickReply, QuickReplyItem, MessageAction
)
from config import Config

class UIBuilder:
    def __init__(self):
        self.config = Config

    # ========== Quick Reply ثابت ==========
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
    def _get_colors(self, theme: Optional[str] = None) -> Dict[str, str]:
        return self.config.get_theme(theme or "فاتح")

    # ========== بناء أزرار ==========
    def _build_buttons(self, actions: List[str], colors: Dict[str,str], primary=True) -> List[dict]:
        rows = []
        for i in range(0, len(actions), 3):
            row = {"type": "box","layout": "horizontal","spacing": "sm","margin": "md","contents":[]}
            for a in actions[i:i+3]:
                row["contents"].append({
                    "type": "button",
                    "style": "primary" if primary else "secondary",
                    "height": "sm",
                    "color": colors["primary"] if primary else None,
                    "action": {"type": "message", "label": a, "text": a}
                })
            rows.append(row)
        return rows

    # ========== شاشة سؤال/نص ==========
    def text_game_screen(self, game_name: str, question: str, round_num: int, theme: str) -> FlexMessage:
        c = self._get_colors(theme)
        flex_dict = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "20px",
                "backgroundColor": c["bg"],
                "contents": [
                    {"type": "text","text": game_name,"size": "xl","weight": "bold","color": c["primary"],"align": "center"},
                    {"type": "text","text": f"جولة {round_num}","size": "sm","color": c["text3"],"align": "center","margin": "xs"},
                    {"type": "separator","margin": "md","color": c["border"]},
                    {"type": "text","text": question,"size": "md","color": c["text"],"wrap": True,"margin": "md"},
                    {"type": "separator","margin": "md","color": c["border"]},
                    *self._build_buttons(["جاوب", "لمح", "وقف"], c, primary=False)
                ]
            }
        }
        return self._create_flex(game_name, flex_dict)

    # ========== شاشة نهاية اللعبة ==========
    def game_over_screen(self, game_name: str, points: int, theme: str) -> FlexMessage:
        c = self._get_colors(theme)
        flex_dict = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "20px",
                "backgroundColor": c["bg"],
                "contents": [
                    {"type": "text","text": f"{game_name} انتهت","size": "xl","weight": "bold","color": c["primary"],"align": "center"},
                    {"type": "text","text": f"نقاطك: {points}","size": "md","color": c["text"],"align": "center","margin": "md"},
                    {"type": "separator","margin": "md","color": c["border"]},
                    {"type": "button","style": "primary","height": "sm","margin": "md","color": c["primary"],"action":{"type":"message","label":"الرئيسية","text":"بداية"}}
                ]
            }
        }
        return self._create_flex(f"{game_name} انتهت", flex_dict)

    # ========== تسجيل وانسحاب ==========
    def registration_prompt(self) -> TextMessage:
        return self._create_text("أرسل اسمك للتسجيل في نظام النقاط")

    def registration_success(self, username: str, points: int, theme: str) -> TextMessage:
        return self._create_text(f"تم التسجيل بنجاح!\nالاسم: {username}\nالنقاط: {points}")

    def unregister_confirm(self, username: str, points: int, theme: str) -> TextMessage:
        return self._create_text(f"تم الانسحاب من النظام\nالاسم: {username}\nالنقاط المحفوظة: {points}")

    def game_stopped(self, game_name: str, theme: str) -> TextMessage:
        return self._create_text(f"تم إيقاف لعبة {game_name}")
