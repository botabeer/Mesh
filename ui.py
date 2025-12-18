from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
from config import Config

class UI:
    @staticmethod
    def get_quick_reply():
        items = ["سؤال", "منشن", "تحدي", "اعتراف", "شخصية", "حكمة", "موقف", "بداية", "العاب", "مساعدة"]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=cmd, text=cmd)) for cmd in items])
    
    @staticmethod
    def main_menu(user, db):
        c = Config.get_theme(user['theme'])
        can_reward = db.can_claim_reward(user['user_id'])
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "text", "text": f"مرحبا {user['name']}", "size": "lg", "color": c["text"], "margin": "lg"},
                    {
                        "type": "box", "layout": "vertical",
                        "contents": [
                            {"type": "box", "layout": "horizontal", "contents": [
                                {"type": "text", "text": f"النقاط: {user['points']}", "size": "sm", "color": c["text"]},
                                {"type": "text", "text": f"الالعاب: {user['games']}", "size": "sm", "color": c["secondary"], "align": "end"}
                            ]},
                            {"type": "box", "layout": "horizontal", "contents": [
                                {"type": "text", "text": f"الفوز: {user['wins']}", "size": "sm", "color": c["text"]},
                                {"type": "text", "text": f"السلسلة: {user['streak']}", "size": "sm", "color": c["secondary"], "align": "end"}
                            ], "margin": "sm"}
                        ],
                        "margin": "md", "paddingAll": "15px", "backgroundColor": c["border"], "cornerRadius": "8px"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "text", "text": "تم الانشاء بواسطة عبير الدوسري", "size": "xxs", "color": c["text_tertiary"], "align": "center", "margin": "md"}
                ],
                "backgroundColor": c["bg"], "paddingAll": "20px"
            },
            "footer": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "button", "action": {"type": "message", "label": "تغيير", "text": "تغيير"}, "style": "secondary", "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "نقاطي", "text": "نقاطي"}, "style": "secondary", "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "الصدارة", "text": "الصدارة"}, "style": "secondary", "height": "sm"}
                    ], "spacing": "sm"},
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "button", "action": {"type": "message", "label": "انجازات", "text": "انجازات"}, "style": "secondary", "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "ثيم", "text": "ثيم"}, "style": "secondary", "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "مكافأة" if can_reward else "غير متاح", "text": "مكافأة"}, "style": "primary" if can_reward else "secondary", "height": "sm"}
                    ], "spacing": "sm", "margin": "sm"},
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "button", "action": {"type": "message", "label": "العاب", "text": "العاب"}, "style": "primary", "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "مساعدة", "text": "مساعدة"}, "style": "secondary", "height": "sm"}
                    ], "spacing": "sm", "margin": "sm"}
                ],
                "backgroundColor": c["bg"], "paddingAll": "15px"
            }
        }
        
        return FlexMessage(alt_text="القائمة الرئيسية", contents=FlexContainer.from_dict(bubble), quick_reply=UI.get_quick_reply())
    
    @staticmethod
    def games_list(theme="light"):
        c = Config.get_theme(theme)
        games = [
            ["خمن", "خمن"], ["ذكاء", "ذكاء"], ["ترتيب", "ترتيب"],
            ["رياضيات", "رياضيات"], ["اسرع", "اسرع"], ["ضد", "ضد"],
            ["لعبه", "لعبة"], ["سلسله", "سلسلة"], ["اغنيه", "اغنية"],
            ["تكوين", "تكوين"], ["لون", "لون"], ["حرف", "حرف"]
        ]
        
        contents = [
            {"type": "text", "text": "الالعاب", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]
        
        for i in range(0, len(games), 3):
            row = []
            for j in range(3):
                if i + j < len(games):
                    cmd, label = games[i + j]
                    row.append({"type": "button", "action": {"type": "message", "label": label, "text": cmd}, "style": "secondary", "height": "sm"})
            contents.append({"type": "box", "layout": "horizontal", "contents": row, "spacing": "sm", "margin": "md"})
        
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text="قائمة الالعاب", contents=FlexContainer.from_dict(bubble), quick_reply=UI.get_quick_reply())
    
    @staticmethod
    def leaderboard(leaders, theme="light"):
        c = Config.get_theme(theme)
        contents = [
            {"type": "text", "text": "الصدارة", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]
        
        for idx, leader in enumerate(leaders[:10]):
            rank = idx + 1
            contents.append({
                "type": "box", "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": f"{rank}.", "size": "md", "color": c["text"], "flex": 1},
                    {"type": "text", "text": leader['name'], "size": "md", "color": c["text"], "flex": 4},
                    {"type": "text", "text": str(leader['points']), "size": "sm", "color": c["secondary"], "align": "end", "flex": 2}
                ],
                "margin": "md", "paddingAll": "10px", "backgroundColor": c["border"] if idx < 3 else c["bg"], "cornerRadius": "8px"
            })
        
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text="لوحة الصدارة", contents=FlexContainer.from_dict(bubble), quick_reply=UI.get_quick_reply())
    
    @staticmethod
    def achievements_list(user_achievements, theme="light"):
        c = Config.get_theme(theme)
        contents = [
            {"type": "text", "text": "الانجازات", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]}
        ]
        
        for achievement_id, achievement in Config.ACHIEVEMENTS.items():
            unlocked = achievement_id in user_achievements
            contents.append({
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": achievement['name'], "size": "md", "weight": "bold", "color": c["text"]},
                    {"type": "text", "text": achievement['desc'], "size": "sm", "color": c["secondary"], "wrap": True},
                    {"type": "text", "text": f"+{achievement['points']} نقطة", "size": "xs", "color": c["text_tertiary"]}
                ],
                "margin": "md", "paddingAll": "10px", "backgroundColor": c["border"] if unlocked else c["bg"], "cornerRadius": "8px"
            })
        
        bubble = {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": c["bg"], "paddingAll": "20px"}}
        return FlexMessage(alt_text="الانجازات", contents=FlexContainer.from_dict(bubble), quick_reply=UI.get_quick_reply())
    
    @staticmethod
    def achievement_unlocked(achievement, theme="light"):
        c = Config.get_theme(theme)
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "انجاز جديد", "size": "xl", "weight": "bold", "color": c["text"], "align": "center"},
                    {"type": "text", "text": achievement['name'], "size": "lg", "weight": "bold", "color": c["primary"], "margin": "md", "align": "center"},
                    {"type": "text", "text": achievement['desc'], "size": "md", "color": c["secondary"], "wrap": True, "margin": "sm", "align": "center"},
                    {"type": "text", "text": f"+{achievement['points']} نقطة", "size": "sm", "color": c["text_secondary"], "margin": "md", "align": "center"}
                ],
                "backgroundColor": c["bg"], "paddingAll": "20px"
            }
        }
        return FlexMessage(alt_text="انجاز جديد", contents=FlexContainer.from_dict(bubble), quick_reply=UI.get_quick_reply())
    
    @staticmethod
    def help_screen():
        c = Config.get_theme("light")
        help_text = """الاوامر الاساسية:
بداية - القائمة
العاب - الالعاب
نقاطي - احصائياتك
الصدارة - المتصدرين
انجازات - انجازاتك
مكافأة - مكافأة يومية
ثيم - تغيير الثيم
تغيير - تغيير الاسم
ايقاف - ايقاف اللعبة"""
        
        bubble = {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "المساعدة", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "text", "text": help_text, "size": "sm", "color": c["text"], "wrap": True, "margin": "lg"}
                ],
                "backgroundColor": c["bg"], "paddingAll": "20px"
            }
        }
        return FlexMessage(alt_text="مساعدة", contents=FlexContainer.from_dict(bubble), quick_reply=UI.get_quick_reply())
