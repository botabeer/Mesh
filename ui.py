from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config

class UI:
    def __init__(self, theme="light"):
        self.theme = theme

    def _c(self):
        """ارجاع ألوان الثيم الحالي"""
        return Config.get_theme(self.theme)

    def _qr(self):
        """الاختصارات السريعة لكل النوافذ"""
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="القائمة", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
            QuickReplyItem(action=MessageAction(label="ايقاف", text="ايقاف")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
        ])

    ### ==================== النوافذ الرئيسية ====================

    def main_menu(self, user=None):
        c = self._c()
        contents = [
            {"type":"text","text":Config.BOT_NAME,"size":"xxl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"text","text":f"الإصدار {Config.VERSION}","size":"xs","color":c["text_tertiary"],"align":"center","margin":"xs"},
            {"type":"separator","margin":"md","color":c["border"]}
        ]

        if user:
            contents.append({
                "type":"box","layout":"horizontal","spacing":"md","margin":"md","contents":[
                    {"type":"box","layout":"vertical","contents":[
                        {"type":"text","text":"اللاعب","size":"xs","color":c["text_tertiary"]},
                        {"type":"text","text":user['name'],"size":"md","weight":"bold","color":c["text"],"margin":"xs"}
                    ],"flex":3},
                    {"type":"box","layout":"vertical","contents":[
                        {"type":"text","text":"النقاط","size":"xs","color":c["text_tertiary"],"align":"end"},
                        {"type":"text","text":str(user['points']),"size":"xl","weight":"bold","color":c["primary"],"align":"end","margin":"xs"}
                    ],"flex":2}
                ],"paddingAll":"md","cornerRadius":"md","backgroundColor":c["glass"],"borderWidth":"1px","borderColor":c["border"]}
            )

        contents.extend([
            {"type":"separator","margin":"lg","color":c["border"]},
            {"type":"button","action":{"type":"message","label":"الالعاب","text":"العاب"},"style":"primary","color":c["primary"],"margin":"md","height":"md"},
            {"type":"box","layout":"horizontal","spacing":"md","margin":"md","contents":[
                {"type":"button","action":{"type":"message","label":"نقاطي" if user else "تسجيل","text":"نقاطي" if user else "تسجيل"},"style":"secondary","height":"sm","flex":1},
                {"type":"button","action":{"type":"message","label":"الصدارة","text":"الصدارة"},"style":"secondary","height":"sm","flex":1}
            ]}
        ])

        if user:
            contents.append({
                "type":"box","layout":"horizontal","spacing":"md","margin":"sm","contents":[
                    {"type":"button","action":{"type":"message","label":"تغيير الاسم","text":"تغيير الاسم"},"style":"secondary","height":"sm","flex":1},
                    {"type":"button","action":{"type":"message","label":"تبديل الثيم","text":"ثيم"},"style":"secondary","height":"sm","flex":1}
                ]
            })
        else:
            contents.append({"type":"button","action":{"type":"message","label":"انسحب","text":"انسحب"},"style":"secondary","height":"sm","margin":"sm"})

        contents.extend([
            {"type":"separator","margin":"xl","color":c["border"]},
            {"type":"text","text":Config.COPYRIGHT,"size":"xxs","color":c["text_tertiary"],"align":"center","wrap":True,"margin":"md"}
        ])

        bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        
        quick_reply = QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="نقاطي", text="نقاطي")),
            QuickReplyItem(action=MessageAction(label="الصدارة", text="الصدارة")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="منشن", text="منشن")),
            QuickReplyItem(action=MessageAction(label="موقف", text="موقف")),
            QuickReplyItem(action=MessageAction(label="حكمة", text="حكمة")),
            QuickReplyItem(action=MessageAction(label="شخصية", text="شخصية")),
            QuickReplyItem(action=MessageAction(label="توافق", text="توافق")),
            QuickReplyItem(action=MessageAction(label="مافيا", text="مافيا")),
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
        ])
        
        return FlexMessage(alt_text="البداية",contents=FlexContainer.from_dict(bubble),quickReply=quick_reply)

    def help_menu(self):
        c = self._c()
        contents = [
            {"type":"text","text":"دليل الاستخدام","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"lg","color":c["border"]},
            {"type":"text","text":"الأوامر الأساسية","size":"md","weight":"bold","color":c["text"],"margin":"lg"},
            {"type":"text","text":"بداية - العاب - نقاطي - الصدارة - ثيم - مساعدة","size":"sm","color":c["text_secondary"],"wrap":True,"margin":"sm"},
            {"type":"text","text":"التسجيل","size":"md","weight":"bold","color":c["text"],"margin":"lg"},
            {"type":"text","text":"تسجيل: للعب وحساب النقاط\nانسحب: تجاهل كامل (لن يرد البوت)","size":"sm","color":c["text_secondary"],"wrap":True,"margin":"sm"},
            {"type":"text","text":"الألعاب","size":"md","weight":"bold","color":c["text"],"margin":"lg"},
            {"type":"text","text":"ذكاء - خمن - رياضيات - ترتيب - ضد - اسرع - سلسله - انسان حيوان - تكوين - اغاني - الوان - توافق - مافيا","size":"sm","color":c["text_secondary"],"wrap":True,"margin":"sm"},
            {"type":"text","text":"المحتوى التفاعلي","size":"md","weight":"bold","color":c["text"],"margin":"lg"},
            {"type":"text","text":"تحدي - سؤال - اعتراف - منشن - موقف - حكمة - شخصية","size":"sm","color":c["text_secondary"],"wrap":True,"margin":"sm"},
            {"type":"text","text":"ملاحظات","size":"md","weight":"bold","color":c["text"],"margin":"lg"},
            {"type":"text","text":"ايقاف: يوقف اللعبة مؤقتاً\nانسحب: يتجاهلك البوت حتى تسجل","size":"xs","color":c["text_tertiary"],"wrap":True,"margin":"sm"},
            {"type":"separator","margin":"xl","color":c["border"]},
            {"type":"button","action":{"type":"message","label":"البداية","text":"بداية"},"style":"secondary","height":"sm","margin":"md"}
        ]
        bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        
        quick_reply = QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="بداية", text="بداية")),
            QuickReplyItem(action=MessageAction(label="العاب", text="العاب")),
            QuickReplyItem(action=MessageAction(label="تحدي", text="تحدي")),
            QuickReplyItem(action=MessageAction(label="سؤال", text="سؤال")),
            QuickReplyItem(action=MessageAction(label="اعتراف", text="اعتراف")),
            QuickReplyItem(action=MessageAction(label="منشن", text="منشن")),
            QuickReplyItem(action=MessageAction(label="موقف", text="موقف")),
            QuickReplyItem(action=MessageAction(label="حكمة", text="حكمة")),
            QuickReplyItem(action=MessageAction(label="شخصية", text="شخصية")),
            QuickReplyItem(action=MessageAction(label="توافق", text="توافق")),
            QuickReplyItem(action=MessageAction(label="مافيا", text="مافيا"))
        ])
        
        return FlexMessage(alt_text="المساعدة",contents=FlexContainer.from_dict(bubble),quickReply=quick_reply)

    ### ==================== ألعاب ====================

    def games_menu(self, user=None):
        c = self._c()
        games_list = ["ذكاء","خمن","رياضيات","ترتيب","ضد","اسرع","سلسله","انسان حيوان","تكوين","اغاني","الوان","توافق","مافيا"]
        
        contents = [
            {"type":"text","text":"الألعاب المتاحة","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
            {"type":"separator","margin":"md","color":c["border"]}
        ]

        for i in range(0,len(games_list),2):
            row = {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[]}
            for j in range(2):
                if i+j < len(games_list):
                    row["contents"].append({
                        "type":"button",
                        "action":{"type":"message","label":games_list[i+j],"text":games_list[i+j]},
                        "style":"primary",
                        "height":"sm",
                        "flex":1,
                        "color":c["primary"]
                    })
            contents.append(row)

        contents.extend([
            {"type":"separator","margin":"lg","color":c["border"]},
            {"type":"text","text":"محتوى تفاعلي","size":"md","weight":"bold","color":c["text"],"align":"center","margin":"md"},
            {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[
                {"type":"button","action":{"type":"message","label":"تحدي","text":"تحدي"},"style":"secondary","height":"sm","flex":1},
                {"type":"button","action":{"type":"message","label":"سؤال","text":"سؤال"},"style":"secondary","height":"sm","flex":1},
                {"type":"button","action":{"type":"message","label":"اعتراف","text":"اعتراف"},"style":"secondary","height":"sm","flex":1}
            ]},
            {"type":"box","layout":"horizontal","spacing":"sm","margin":"xs","contents":[
                {"type":"button","action":{"type":"message","label":"منشن","text":"منشن"},"style":"secondary","height":"sm","flex":1},
                {"type":"button","action":{"type":"message","label":"موقف","text":"موقف"},"style":"secondary","height":"sm","flex":1},
                {"type":"button","action":{"type":"message","label":"حكمة","text":"حكمة"},"style":"secondary","height":"sm","flex":1}
            ]},
            {"type":"box","layout":"horizontal","spacing":"sm","margin":"xs","contents":[
                {"type":"button","action":{"type":"message","label":"شخصية","text":"شخصية"},"style":"secondary","height":"sm","flex":1}
            ]},
            {"type":"separator","margin":"lg","color":c["border"]},
            {"type":"button","action":{"type":"message","label":"البداية","text":"بداية"},"style":"secondary","height":"sm","margin":"md"}
        ])

        bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":contents,"paddingAll":"lg","backgroundColor":c["bg"],"spacing":"none"}}
        
        quick_reply = QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="ذكاء", text="ذكاء")),
            QuickReplyItem(action=MessageAction(label="خمن", text="خمن")),
            QuickReplyItem(action=MessageAction(label="رياضيات", text="رياضيات")),
            QuickReplyItem(action=MessageAction(label="ترتيب", text="ترتيب")),
            QuickReplyItem(action=MessageAction(label="ضد", text="ضد")),
            QuickReplyItem(action=MessageAction(label="اسرع", text="اسرع")),
            QuickReplyItem(action=MessageAction(label="سلسله", text="سلسله")),
            QuickReplyItem(action=MessageAction(label="انسان حيوان", text="انسان حيوان")),
            QuickReplyItem(action=MessageAction(label="تكوين", text="تكوين")),
            QuickReplyItem(action=MessageAction(label="اغاني", text="اغاني")),
            QuickReplyItem(action=MessageAction(label="الوان", text="الوان")),
            QuickReplyItem(action=MessageAction(label="توافق", text="توافق")),
            QuickReplyItem(action=MessageAction(label="مافيا", text="مافيا"))
        ])
        
        return FlexMessage(alt_text="الالعاب",contents=FlexContainer.from_dict(bubble),quickReply=quick_reply)

    ### ==================== نقاطي وإحصائياتي ====================

    def stats_card(self, user):
        """بطاقة إحصائيات المستخدم"""
        c = self._c()
        
        win_rate = 0
        if user['games'] > 0:
            win_rate = round((user['wins'] / user['games']) * 100)
        
        contents = [
            {"type": "text", "text": "إحصائياتي", "size": "xl", "weight": "bold", 
             "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": "اللاعب", "size": "xs", 
                 "color": c["text_tertiary"], "align": "center"},
                {"type": "text", "text": user['name'], "size": "xl", "weight": "bold",
                 "color": c["text"], "align": "center", "margin": "xs"}
            ], "paddingAll": "md", "cornerRadius": "md", 
               "backgroundColor": c["glass"], "margin": "lg"},
            
            {"type": "box", "layout": "horizontal", "spacing": "md", 
             "margin": "lg", "contents": [
                {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "النقاط", "size": "xs", 
                     "color": c["text_tertiary"], "align": "center"},
                    {"type": "text", "text": str(user['points']), "size": "xxl", 
                     "weight": "bold", "color": c["success"], "align": "center"}
                ], "flex": 1, "paddingAll": "md", "cornerRadius": "md",
                   "backgroundColor": c["card"], "borderWidth": "2px",
                   "borderColor": c["border"]},
                
                {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "الألعاب", "size": "xs",
                     "color": c["text_tertiary"], "align": "center"},
                    {"type": "text", "text": str(user['games']), "size": "xxl",
                     "weight": "bold", "color": c["info"], "align": "center"}
                ], "flex": 1, "paddingAll": "md", "cornerRadius": "md",
                   "backgroundColor": c["card"], "borderWidth": "2px",
                   "borderColor": c["border"]}
            ]},
            
            {"type": "box", "layout": "horizontal", "spacing": "md",
             "margin": "md", "contents": [
                {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "الانتصارات", "size": "xs",
                     "color": c["text_tertiary"], "align": "center"},
                    {"type": "text", "text": str(user['wins']), "size": "xl",
                     "weight": "bold", "color": c["primary"], "align": "center"}
                ], "flex": 1, "paddingAll": "md", "cornerRadius": "md",
                   "backgroundColor": c["card"], "borderWidth": "1px",
                   "borderColor": c["border"]},
                
                {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "نسبة الفوز", "size": "xs",
                     "color": c["text_tertiary"], "align": "center"},
                    {"type": "text", "text": f"{win_rate}%", "size": "xl",
                     "weight": "bold", "color": c["warning"], "align": "center"}
                ], "flex": 1, "paddingAll": "md", "cornerRadius": "md",
                   "backgroundColor": c["card"], "borderWidth": "1px",
                   "borderColor": c["border"]}
            ]},
            
            {"type": "separator", "margin": "xl", "color": c["border"]},
            
            {"type": "box", "layout": "horizontal", "spacing": "sm",
             "margin": "md", "contents": [
                {"type": "button", "action": {"type": "message", 
                 "label": "البداية", "text": "بداية"},
                 "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message",
                 "label": "الصدارة", "text": "الصدارة"},
                 "style": "primary", "color": c["primary"], 
                 "height": "sm", "flex": 1}
            ]}
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        
        return FlexMessage(
            alt_text="إحصائياتي",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    ### ==================== لوحة الصدارة ====================

    def leaderboard_card(self, leaderboard):
        """لوحة الصدارة"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "لوحة الصدارة", "size": "xl", "weight": "bold",
             "color": c["primary"], "align": "center"},
            {"type": "text", "text": "أفضل 10 لاعبين", "size": "xs",
             "color": c["text_tertiary"], "align": "center", "margin": "xs"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]
        
        if not leaderboard:
            contents.append({
                "type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "لا توجد بيانات بعد",
                     "size": "md", "color": c["text_secondary"],
                     "align": "center", "wrap": True}
                ],
                "paddingAll": "xl",
                "cornerRadius": "md",
                "backgroundColor": c["glass"],
                "margin": "lg"
            })
        else:
            for idx, player in enumerate(leaderboard[:10]):
                rank = idx + 1
                
                if rank == 1:
                    rank_text = "1"
                    bg_color = c["glass"]
                    border_color = "#FFD700"
                    border_width = "3px"
                elif rank == 2:
                    rank_text = "2"
                    bg_color = c["glass"]
                    border_color = "#C0C0C0"
                    border_width = "2px"
                elif rank == 3:
                    rank_text = "3"
                    bg_color = c["glass"]
                    border_color = "#CD7F32"
                    border_width = "2px"
                else:
                    rank_text = str(rank)
                    bg_color = c["card"]
                    border_color = c["border"]
                    border_width = "1px"
                
                player_box = {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "md",
                    "contents": [
                        {"type": "box", "layout": "vertical", "contents": [
                            {"type": "text", "text": rank_text, "size": "xl",
                             "weight": "bold", "align": "center",
                             "color": c["primary"]}
                        ], "flex": 0, "width": "40px", "justifyContent": "center"},
                        
                        {"type": "box", "layout": "vertical", "contents": [
                            {"type": "text", "text": player['name'], "size": "md",
                             "weight": "bold", "color": c["text"], "wrap": True},
                            {"type": "box", "layout": "horizontal", "spacing": "md",
                             "margin": "xs", "contents": [
                                {"type": "text", "text": f"النقاط: {player['points']}",
                                 "size": "xs", "color": c["text_secondary"], "flex": 0},
                                {"type": "text", "text": f"الفوز: {player['wins']}",
                                 "size": "xs", "color": c["text_secondary"], "flex": 0}
                            ]}
                        ], "flex": 1}
                    ],
                    "paddingAll": "md",
                    "cornerRadius": "md",
                    "backgroundColor": bg_color,
                    "borderWidth": border_width,
                    "borderColor": border_color,
                    "margin": "sm"
                }
                
                contents.append(player_box)
        
        contents.extend([
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "box", "layout": "horizontal", "spacing": "sm",
             "margin": "md", "contents": [
                {"type": "button", "action": {"type": "message",
                 "label": "البداية", "text": "بداية"},
                 "style": "secondary", "height": "sm", "flex": 1},
                {"type": "button", "action": {"type": "message",
                 "label": "نقاطي", "text": "نقاطي"},
                 "style": "primary", "color": c["primary"],
                 "height": "sm", "flex": 1}
            ]}
        ])
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        
        return FlexMessage(
            alt_text="لوحة الصدارة",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    ### ==================== رسائل إضافية ====================

    def registration_choice(self):
        """خيار التسجيل للمستخدمين الجدد"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "مرحباً بك!", "size": "xxl",
             "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": "للعب وكسب النقاط:",
                 "size": "md", "color": c["text"], "wrap": True,
                 "align": "center", "weight": "bold"},
                {"type": "text", "text": "سجل حسابك الآن",
                 "size": "sm", "color": c["text_secondary"],
                 "wrap": True, "align": "center", "margin": "sm"}
            ], "paddingAll": "md", "cornerRadius": "md",
               "backgroundColor": c["glass"], "margin": "lg"},
            
            {"type": "button", "action": {"type": "message",
             "label": "تسجيل", "text": "تسجيل"},
             "style": "primary", "color": c["success"],
             "height": "md", "margin": "lg"},
            
            {"type": "separator", "margin": "lg", "color": c["border"]},
            
            {"type": "text", "text": "أو",
             "size": "sm", "color": c["text_tertiary"],
             "align": "center", "margin": "md"},
            
            {"type": "button", "action": {"type": "message",
             "label": "انسحب (لن يرد البوت)", "text": "انسحب"},
             "style": "secondary", "height": "sm", "margin": "md"}
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        
        return FlexMessage(
            alt_text="مرحباً",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def ask_name(self):
        """طلب الاسم من المستخدم الجديد"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "التسجيل", "size": "xl",
             "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": "يرجى إدخال اسمك:",
                 "size": "md", "color": c["text"], "wrap": True,
                 "align": "center", "weight": "bold"},
                {"type": "text", "text": "من 1 إلى 50 حرف",
                 "size": "xs", "color": c["text_tertiary"],
                 "align": "center", "margin": "sm"}
            ], "paddingAll": "lg", "cornerRadius": "md",
               "backgroundColor": c["glass"], "margin": "lg"}
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        
        return FlexMessage(
            alt_text="إدخال الاسم",
            contents=FlexContainer.from_dict(bubble)
        )

    def ask_name_invalid(self):
        """رسالة خطأ في الاسم"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "اسم غير صالح", "size": "lg",
             "weight": "bold", "color": c["danger"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": "يرجى إدخال اسم صحيح:",
                 "size": "sm", "color": c["text"], "wrap": True},
                {"type": "text", "text": "من 1 إلى 50 حرف",
                 "size": "xs", "color": c["text_secondary"], "margin": "sm"},
                {"type": "text", "text": "حروف عربية أو إنجليزية فقط",
                 "size": "xs", "color": c["text_secondary"], "margin": "xs"},
                {"type": "text", "text": "لا يمكن استخدام أوامر البوت كاسم",
                 "size": "xs", "color": c["text_secondary"], "margin": "xs"}
            ], "paddingAll": "md", "cornerRadius": "md",
               "backgroundColor": c["glass"], "margin": "lg"}
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        
        return FlexMessage(
            alt_text="اسم غير صالح",
            contents=FlexContainer.from_dict(bubble)
        )

    def game_stopped(self):
        """رسالة إيقاف اللعبة"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "تم إيقاف اللعبة", "size": "xl",
             "weight": "bold", "color": c["warning"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            
            {"type": "text", "text": "يمكنك بدء لعبة جديدة في أي وقت",
             "size": "sm", "color": c["text_secondary"],
             "wrap": True, "align": "center", "margin": "lg"},
            
            {"type": "button", "action": {"type": "message",
             "label": "العاب", "text": "العاب"},
             "style": "primary", "color": c["primary"],
             "height": "sm", "margin": "lg"}
        ]
        
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        
        return FlexMessage(
            alt_text="تم الإيقاف",
            contents=FlexContainer.from_dict(bubble),
            quickReply=self._qr()
        )

    def theme_changed(self, theme_name):
        """رسالة تأكيد تبديل الثيم"""
        c = self._c()
        
        contents = [
            {"type": "text", "text": "تم تبديل الثيم", "size": "xl",
             "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": theme_name,
                 "size": "lg", "color": c["text"], "wrap": True,
                 "align": "center", "weight": "bold"}
            ], "paddingAll": "md", "cornerRadius": "md",
               "backgroundColor": c["glass"], "margin": "lg"}
        ]
        
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "lg",
                "backgroundColor": c["bg"],
                "spacing": "none"
            }
        }
        
        return FlexMessage(
            alt_text="تم التبديل",
            contents=FlexContainer.from_dict(bubble)
        )
