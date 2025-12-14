from typing import List, Dict

class UIBuilder:
    def __init__(self, theme: str = "light"):
        self.theme = theme
        self.themes = {
            "light": {
                "primary": "#007AFF", "secondary": "#5AC8FA", "success": "#34C759",
                "warning": "#FF9500", "danger": "#FF3B30", "bg": "#F2F2F7",
                "card": "#FFFFFF", "text": "#000000", "text2": "#3C3C43",
                "text3": "#8E8E93", "border": "#E5E5EA"
            }
        }
    
    def _colors(self) -> Dict[str, str]:
        return self.themes.get(self.theme, self.themes["light"])
    
    def welcome_card(self, name: str, registered: bool):
        c = self._colors()
        status = "مسجل" if registered else "غير مسجل"
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
        return flex
    
    def games_menu_card(self):
        c = self._colors()
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
                    {"type": "text", "text": "الالعاب", "size": "xl",
                     "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "box", "layout": "vertical", "margin": "lg", "contents": buttons}
                ]
            }
        }
        return flex
    
    def leaderboard_card(self, leaders: List[tuple]):
        c = self._colors()
        items = []
        
        for i, (name, pts) in enumerate(leaders[:10]):
            rank = str(i + 1)
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
        return flex
    
    def stats_card(self, name: str, user_data: dict):
        c = self._colors()
        points = user_data.get("total_points", 0)
        games = user_data.get("games_played", 0)
        wins = user_data.get("wins", 0)
        
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
                         {"type": "text", "text": f"الالعاب: {games}", "size": "sm",
                          "color": c["text2"], "margin": "sm"},
                         {"type": "text", "text": f"الفوز: {wins}", "size": "sm",
                          "color": c["text2"], "margin": "sm"}
                     ]}
                ]
            }
        }
        return flex
    
    def help_card(self):
        c = self._colors()
        
        flex = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical", "paddingAll": "20px",
                "backgroundColor": c["card"],
                "contents": [
                    {"type": "text", "text": "المساعدة", "size": "xl",
                     "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "text", "text": "الاوامر المتاحة:", "size": "md",
                     "color": c["text"], "weight": "bold", "margin": "lg"},
                    {"type": "text", "text": "بداية - القائمة الرئيسية\nالعاب - عرض الالعاب\nنقاطي - عرض النقاط\nالصدارة - لوحة المتصدرين\nتسجيل - التسجيل في النظام",
                     "size": "sm", "color": c["text2"], "wrap": True, "margin": "md"}
                ]
            }
        }
        return flex
