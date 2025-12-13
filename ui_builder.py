from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
from typing import List, Dict

class UIBuilder:
    def __init__(self):
        self.themes = {
            "light": {
                "primary": "#007AFF", "secondary": "#5AC8FA", "success": "#34C759",
                "warning": "#FF9500", "danger": "#FF3B30", "bg": "#F2F2F7",
                "card": "#FFFFFF", "text": "#000000", "text2": "#3C3C43",
                "text3": "#8E8E93", "border": "#E5E5EA"
            },
            "dark": {
                "primary": "#0A84FF", "secondary": "#64D2FF", "success": "#30D158",
                "warning": "#FF9F0A", "danger": "#FF453A", "bg": "#000000",
                "card": "#1C1C1E", "text": "#FFFFFF", "text2": "#EBEBF5",
                "text3": "#8E8E93", "border": "#3A3A3C"
            }
        }

    def _colors(self, theme: str = "light") -> Dict[str, str]:
        return self.themes.get(theme, self.themes["light"])

    def _flex(self, alt: str, contents: dict) -> FlexMessage:
        return FlexMessage(alt_text=alt, contents=FlexContainer.from_dict(contents))

    def _text(self, text: str) -> TextMessage:
        return TextMessage(text=text)

    def welcome_card(self, name: str, registered: bool, points: int = 0, theme: str = "light") -> FlexMessage:
        c = self._colors(theme)
        status = f"مسجل | النقاط: {points}" if registered else "غير مسجل"
        color = c["success"] if registered else c["warning"]
        
        buttons = [
            {"type": "button", "style": "primary", "height": "sm", "color": c["primary"],
             "action": {"type": "message", "label": "العاب", "text": "العاب"}},
            {"type": "button", "style": "secondary", "height": "sm",
             "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"}},
            {"type": "button", "style": "secondary", "height": "sm",
             "action": {"type": "message", "label": "الصدارة", "text": "الصدارة"}}
        ]
        
        if not registered:
            buttons.append({"type": "button", "style": "secondary", "height": "sm",
                          "action": {"type": "message", "label": "تسجيل", "text": "تسجيل"}})
        
        flex = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical", "paddingAll": "20px",
                "backgroundColor": c["card"],
                "contents": [
                    {"type": "text", "text": f"مرحبا {name}", "size": "xl",
                     "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "text", "text": status, "size": "sm",
                     "color": color, "align": "center", "margin": "md"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "box", "layout": "vertical", "spacing": "sm",
                     "margin": "lg", "contents": buttons}
                ]
            }
        }
        return self._flex("بداية", flex)

    def games_menu_card(self, theme: str = "light") -> FlexMessage:
        c = self._colors(theme)
        games = [
            "ذكاء", "خمن", "ضد", "ترتيب", "رياضيات", "اغنيه",
            "لون", "تكوين", "لعبة", "سلسلة", "اسرع", "توافق", "مافيا"
        ]
        
        buttons = []
        for i in range(0, len(games), 3):
            row = {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": []}
            for game in games[i:i+3]:
                row["contents"].append({
                    "type": "button", "style": "primary", "height": "sm",
                    "action": {"type": "message", "label": game, "text": game}
                })
            buttons.append(row)
        
        flex = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical", "paddingAll": "20px",
                "backgroundColor": c["card"],
                "contents": [
                    {"type": "text", "text": "الألعاب", "size": "xl",
                     "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "box", "layout": "vertical", "margin": "lg", "contents": buttons}
                ]
            }
        }
        return self._flex("الألعاب", flex)

    def leaderboard_card(self, leaders: List[tuple], theme: str = "light") -> FlexMessage:
        c = self._colors(theme)
        items = []
        
        for i, (name, pts) in enumerate(leaders[:10]):
            rank = str(i + 1) if i >= 3 else ["1", "2", "3"][i]
            items.append({
                "type": "box", "layout": "horizontal", "margin": "sm",
                "contents": [
                    {"type": "text", "text": rank, "size": "sm", "color": c["text"], "flex": 0},
                    {"type": "text", "text": name, "size": "sm", "color": c["text"],
                     "flex": 3, "margin": "sm"},
                    {"type": "text", "text": str(pts), "size": "sm",
                     "color": c["primary"], "weight": "bold", "flex": 1, "align": "end"}
                ]
            })
        
        flex = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical", "paddingAll": "20px",
                "backgroundColor": c["card"],
                "contents": [
                    {"type": "text", "text": "لوحة الصدارة", "size": "xl",
                     "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "box", "layout": "vertical", "margin": "lg", "contents": items}
                ]
            }
        }
        return self._flex("الصدارة", flex)

    def stats_card(self, name: str, user_data: dict, theme: str = "light") -> FlexMessage:
        c = self._colors(theme)
        points = user_data.get("points", 0)
        temp = user_data.get("temp_points", 0)
        
        flex = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical", "paddingAll": "20px",
                "backgroundColor": c["card"],
                "contents": [
                    {"type": "text", "text": "احصائياتي", "size": "xl",
                     "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "box", "layout": "vertical", "margin": "lg",
                     "contents": [
                         {"type": "text", "text": f"الاسم: {name}", "size": "md", "color": c["text"]},
                         {"type": "text", "text": f"النقاط: {points}", "size": "md",
                          "color": c["primary"], "weight": "bold", "margin": "md"},
                         {"type": "text", "text": f"نقاط مؤقتة: {temp}", "size": "sm",
                          "color": c["text3"], "margin": "sm"}
                     ]}
                ]
            }
        }
        return self._flex("احصائياتي", flex)

    def help_card(self, theme: str = "light") -> FlexMessage:
        c = self._colors(theme)
        
        flex = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical", "paddingAll": "20px",
                "backgroundColor": c["card"],
                "contents": [
                    {"type": "text", "text": "المساعدة", "size": "xl",
                     "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "text", "text": "الأوامر المتاحة:", "size": "md",
                     "color": c["text"], "weight": "bold", "margin": "lg"},
                    {"type": "text", "text": "بداية - القائمة الرئيسية\nالعاب - عرض الألعاب\nنقاطي - عرض النقاط\nالصدارة - لوحة المتصدرين\nتسجيل - التسجيل في النظام",
                     "size": "sm", "color": c["text2"], "wrap": True, "margin": "md"}
                ]
            }
        }
        return self._flex("المساعدة", flex)

    def registration_success(self, name: str, points: int, theme: str = "light") -> TextMessage:
        return self._text(f"تم التسجيل بنجاح\nالاسم: {name}\nالنقاط: {points}")
