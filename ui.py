from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction, TextMessage
from config import Config

class UI:
    """واجهة المستخدم الموحدة"""
    
    # الألوان الموحدة (أسود/أبيض)
    COLORS = {
        "bg": "#000000",        # خلفية سوداء
        "text": "#FFFFFF",      # نص أبيض
        "secondary": "#CCCCCC", # ثانوي رمادي
        "border": "#333333",    # حدود
        "primary": "#FFFFFF",   # أساسي أبيض
        "success": "#FFFFFF",   # نجاح أبيض
        "warning": "#CCCCCC",   # تحذير رمادي
        "danger": "#FFFFFF",    # خطر أبيض
        "info": "#CCCCCC"       # معلومات رمادي
    }
    
    @staticmethod
    def get_quick_reply():
        """QuickReply ثابت في كل مكان"""
        items = [
            "سؤال", "منشن", "تحدي", "اعتراف", "شخصية",
            "حكمة", "موقف", "بداية", "العاب", "مساعدة"
        ]
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label=cmd, text=cmd))
            for cmd in items
        ])
    
    @staticmethod
    def _footer_text():
        """نص الحقوق الثابت"""
        return "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025"
    
    @staticmethod
    def main_menu(user, db):
        """القائمة الرئيسية"""
        c = UI.COLORS
        can_reward = db.can_claim_reward(user['user_id'])
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Bot Mesh",
                        "size": "xxl",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center"
                    },
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {
                        "type": "text",
                        "text": f"مرحبا {user['name']}",
                        "size": "lg",
                        "color": c["text"],
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {"type": "text", "text": f"النقاط: {user['points']}", "size": "sm", "color": c["text"]},
                                    {"type": "text", "text": f"الألعاب: {user['games']}", "size": "sm", "color": c["secondary"], "align": "end"}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {"type": "text", "text": f"الفوز: {user['wins']}", "size": "sm", "color": c["text"]},
                                    {"type": "text", "text": f"السلسلة: {user['streak']}", "size": "sm", "color": c["secondary"], "align": "end"}
                                ],
                                "margin": "sm"
                            }
                        ],
                        "margin": "md",
                        "paddingAll": "15px",
                        "backgroundColor": c["border"],
                        "cornerRadius": "8px"
                    },
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {
                        "type": "text",
                        "text": UI._footer_text(),
                        "size": "xxs",
                        "color": c["secondary"],
                        "align": "center",
                        "margin": "lg"
                    }
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "الألعاب", "text": "العاب"},
                                "style": "secondary",
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "الصدارة", "text": "الصداره"},
                                "style": "secondary",
                                "height": "sm"
                            }
                        ],
                        "spacing": "sm"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "إنجازات", "text": "انجازات"},
                                "style": "secondary",
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "مكافأة" if can_reward else "تم", "text": "مكافأة"},
                                "style": "secondary",
                                "height": "sm"
                            }
                        ],
                        "spacing": "sm",
                        "margin": "sm"
                    }
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "15px"
            }
        }
        
        return FlexMessage(
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
    
    @staticmethod
    def games_list(theme="dark"):
        """قائمة الألعاب"""
        c = UI.COLORS
        
        games = [
            ["ذكاء", "ألغاز"], ["خمن", "خمن الكلمة"],
            ["رياضيات", "حساب"], ["ترتيب", "ترتيب حروف"],
            ["ضد", "أضداد"], ["كتابه", "كتابة سريعة"],
            ["سلسله", "سلسلة كلمات"], ["انسان", "إنسان حيوان"],
            ["كلمات", "تكوين كلمات"], ["اغنيه", "خمن الأغنية"],
            ["الوان", "ألوان"], ["توافق", "توافق"]
        ]
        
        contents = [
            {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "text", "text": "اختر لعبة", "size": "lg", "color": c["text"], "margin": "lg", "align": "center"}
        ]
        
        for i in range(0, len(games), 2):
            row = []
            for j in range(2):
                if i + j < len(games):
                    cmd, label = games[i + j]
                    row.append({
                        "type": "button",
                        "action": {"type": "message", "label": label, "text": cmd},
                        "style": "secondary",
                        "height": "sm"
                    })
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": row,
                "spacing": "sm",
                "margin": "md"
            })
        
        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": UI._footer_text(), "size": "xxs", "color": c["secondary"], "align": "center", "margin": "md"}
        ])
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        
        return FlexMessage(
            alt_text="قائمة الألعاب",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
    
    @staticmethod
    def leaderboard(leaders, theme="dark"):
        """لوحة الصدارة"""
        c = UI.COLORS
        
        contents = [
            {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "text", "text": "لوحة الصدارة", "size": "lg", "color": c["text"], "margin": "lg", "align": "center"}
        ]
        
        for idx, leader in enumerate(leaders[:10]):
            rank = idx + 1
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "text", "text": f"{rank}.", "size": "md", "color": c["text"], "flex": 1},
                    {"type": "text", "text": leader['name'], "size": "md", "color": c["text"], "flex": 4},
                    {"type": "text", "text": str(leader['points']), "size": "sm", "color": c["secondary"], "align": "end", "flex": 2}
                ],
                "margin": "md",
                "paddingAll": "10px",
                "backgroundColor": c["border"] if idx < 3 else c["bg"],
                "cornerRadius": "8px"
            })
        
        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": UI._footer_text(), "size": "xxs", "color": c["secondary"], "align": "center", "margin": "md"}
        ])
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        
        return FlexMessage(
            alt_text="لوحة الصدارة",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
    
    @staticmethod
    def achievements_list(user_achievements, theme="dark"):
        """قائمة الإنجازات"""
        c = UI.COLORS
        
        contents = [
            {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "text", "text": "الإنجازات", "size": "lg", "color": c["text"], "margin": "lg", "align": "center"}
        ]
        
        for achievement_id, achievement in Config.ACHIEVEMENTS.items():
            unlocked = achievement_id in user_achievements
            
            contents.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"{'✓' if unlocked else '○'} {achievement['name']}", "size": "md", "weight": "bold", "color": c["text"]},
                    {"type": "text", "text": achievement['desc'], "size": "sm", "color": c["secondary"], "wrap": True},
                    {"type": "text", "text": f"+{achievement['points']} نقطة", "size": "xs", "color": c["secondary"]}
                ],
                "margin": "md",
                "paddingAll": "10px",
                "backgroundColor": c["border"] if unlocked else c["bg"],
                "cornerRadius": "8px"
            })
        
        contents.extend([
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "text", "text": UI._footer_text(), "size": "xxs", "color": c["secondary"], "align": "center", "margin": "md"}
        ])
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        
        return FlexMessage(
            alt_text="الإنجازات",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
    
    @staticmethod
    def achievement_unlocked(achievement, theme="dark"):
        """إشعار إنجاز جديد"""
        c = UI.COLORS
        
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "إنجاز جديد", "size": "xl", "weight": "bold", "color": c["text"], "align": "center"},
                    {"type": "text", "text": f"✓ {achievement['name']}", "size": "lg", "weight": "bold", "color": c["text"], "margin": "md", "align": "center"},
                    {"type": "text", "text": achievement['desc'], "size": "md", "color": c["secondary"], "wrap": True, "margin": "sm", "align": "center"},
                    {"type": "text", "text": f"+{achievement['points']} نقطة", "size": "sm", "color": c["secondary"], "margin": "md", "align": "center"}
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        
        return FlexMessage(
            alt_text="إنجاز جديد",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
    
    @staticmethod
    def help_screen():
        """شاشة المساعدة"""
        c = UI.COLORS
        
        help_text = """Bot Mesh - بوت ألعاب عربي

الأوامر الأساسية:
• بداية - القائمة الرئيسية
• العاب - قائمة الألعاب
• نقاطي - إحصائياتك
• الصدارة - أفضل اللاعبين
• انجازات - إنجازاتك
• مكافأة - مكافأة يومية
• ثيم - تغيير الثيم
• ايقاف - إيقاف اللعبة

الألعاب المتوفرة:
ذكاء، خمن، رياضيات، ترتيب، ضد، كتابه، سلسله، انسان، كلمات، اغنيه، الوان، توافق

محتوى إضافي:
تحدي، سؤال، اعتراف، منشن، موقف، حكمة، شخصية"""
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "Bot Mesh", "size": "xxl", "weight": "bold", "color": c["text"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {"type": "text", "text": help_text, "size": "sm", "color": c["text"], "wrap": True, "margin": "lg"},
                    {"type": "separator", "margin": "lg", "color": c["border"]},
                    {"type": "text", "text": UI._footer_text(), "size": "xxs", "color": c["secondary"], "align": "center", "margin": "md"}
                ],
                "backgroundColor": c["bg"],
                "paddingAll": "20px"
            }
        }
        
        return FlexMessage(
            alt_text="مساعدة",
            contents=FlexContainer.from_dict(bubble),
            quick_reply=UI.get_quick_reply()
        )
