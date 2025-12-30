import random
from games.base_game import BaseGame

class FastGame(BaseGame):
    def __init__(self, line_bot_api, difficulty=3, theme='light'):
        super().__init__(line_bot_api, theme=theme)
        self.game_name = "اسرع"
        self.supports_hint = False
        self.supports_reveal = True
        
        self.phrases = [
            "سبحان الله", "الحمد لله", "الله اكبر", "لا اله الا الله",
            "استغفر الله", "لا حول ولا قوة الا بالله", "بسم الله", "يارب",
            "اللهم صل على محمد", "توكلت على الله", "ما شاء الله", "بارك الله فيك",
            "جزاك الله خيرا", "التوكل على الله طمأنينة", "العقل زينة الانسان",
            "الصبر مفتاح الفرج", "العلم نور", "من جد وجد", "احسن للناس تكن لهم خيرا",
            "الدعاء سلاح المؤمن", "الوقت كالسيف", "التقوى خير زاد", "احذر الغيبة",
            "السعادة في الرضا", "العفو من شيم الكرام", "الصدق منجاة", "الحياء من الايمان",
            "من تواضع لله رفعه", "ابتسم", "الخير فيما وقع", "النية أساس العمل",
            "التفاؤل حياة", "الصديق وقت الضيق", "الحرية تاج العز", "النجاح ثمرة اجتهاد",
            "العطاء بلا حدود", "الكرم شيمة النبلاء", "الصحة تاج الحياة", "التواضع زينة الانسان",
            "العقل ملكة", "الوقت ضيفك", "الصمت حكمة", "الصدق رأس الامانة",
            "الامل طريق الحياة", "الوعي نصف العلاج", "الحياة قصيرة", "الابتسامة صدقة",
            "النجاح يحرره الاجتهاد", "العزيمة تصنع المعجزات", "الثقة بالنفس مفتاح التقدم",
            "العمل عبادة", "الرفق من شيم الكرام", "المعرفة نور", "الاستماع فن",
            "الصداقة كنز", "التفكير قبل الكلام", "الصبر مفتاح", "العقل زينة", "الوفاء شيمة",
            "الرحمة حياة", "التعاون قوة", "المحبة حياة", "السعادة اختيار", "الطموح حياة",
            "الحرية حياة", "النجاح جهد", "العطاء سر سعادة", "الاخلاق تاج", "الصدق نعمة",
            "التسامح راحة", "الوعي قوة", "الصبر مفتاح الفرج", "العقل نور", "التواضع شيمة",
            "الحكمة ضياء", "التعلم حياة", "الشجاعة قوة", "الاستقامة حياة", "الحب حياة",
            "الوفاء معدن", "الثقة نجاح", "التفكير عقل", "المحافظة واجب", "الصحة حياة",
            "العطاء حياة", "الاحترام أساس", "النقاء قلب", "الكرم حياة", "التحدي فرصة",
            "النجاح صبر", "الحرية غاية", "الابتسامة حياة", "الامل شعاع", "الرحمة نور",
            "الاحسان عبادة", "المحبة نور", "الصدق حياة", "التواضع حياة", "الصداقة حياة",
            "التعاون اساس", "العقل مفتاح", "الصبر حياة", "التعليم مفتاح", "النية صافية"
        ]
        random.shuffle(self.phrases)
    
    def get_question(self):
        phrase = self.phrases[self.current_question % len(self.phrases)]
        self.current_answer = [phrase]
        colors = self.get_theme_colors()
        
        contents = [
            {
                "type": "text",
                "text": self.game_name,
                "size": "xl",
                "weight": "bold",
                "align": "center",
                "color": colors["primary"]
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": f"السؤال {self.current_question + 1} من {self.questions_count}",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [],
                                "width": f"{int((self.current_question / self.questions_count) * 100)}%",
                                "height": "4px",
                                "backgroundColor": colors["success"],
                                "cornerRadius": "2px"
                            }
                        ],
                        "height": "4px",
                        "backgroundColor": colors["border"],
                        "cornerRadius": "2px"
                    }
                ]
            },
            {
                "type": "separator",
                "margin": "lg",
                "color": colors["border"]
            },
            {
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "backgroundColor": colors["card"],
                "cornerRadius": "12px",
                "paddingAll": "20px",
                "contents": [
                    {
                        "type": "text",
                        "text": phrase,
                        "size": "xxl",
                        "weight": "bold",
                        "color": colors["text"],
                        "align": "center",
                        "wrap": True
                    }
                ]
            },
            {
                "type": "text",
                "text": "اكتب العبارة بسرعة ودقة",
                "size": "sm",
                "color": colors["text2"],
                "align": "center",
                "margin": "lg"
            }
        ]
        
        footer_buttons = [
            {
                "type": "button",
                "style": "secondary",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "جاوب",
                    "text": "جاوب"
                },
                "color": self.BUTTON_COLOR,
                "flex": 1
            },
            {
                "type": "button",
                "style": "secondary",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "ايقاف",
                    "text": "ايقاف"
                },
                "color": self.BUTTON_COLOR,
                "flex": 1
            }
        ]
        
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "20px",
                "backgroundColor": colors["bg"]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "contents": footer_buttons,
                "spacing": "sm",
                "paddingAll": "12px",
                "backgroundColor": colors["card"]
            }
        }
        
        from linebot.v3.messaging import FlexMessage, FlexContainer
        return FlexMessage(
            alt_text=self.game_name,
            contents=FlexContainer.from_dict(bubble)
        )
    
    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active or user_id in self.withdrawn_users:
            return None
        
        normalized = self.normalize_text(user_answer)
        
        if normalized == "ايقاف":
            return self.handle_withdrawal(user_id, display_name)
        
        if self.supports_reveal and normalized == "جاوب":
            return self.handle_reveal()
        
        if user_answer.strip() == self.current_answer[0]:
            return self.handle_correct_answer(user_id, display_name)
        
        return None
