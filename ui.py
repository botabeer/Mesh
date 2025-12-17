from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config


class UI:
    def __init__(self, theme="light"):
        self.theme = theme

    def _c(self):
        return Config.get_theme(self.theme)

    def _qr(self):
        commands = [
            "بداية", "العاب", "نقاطي", "الصدارة", "ثيم", "ايقاف", "مساعدة",
            "تحدي", "سؤال", "اعتراف", "منشن", "موقف", "حكمة", "شخصية"
        ]
        return QuickReply(items=[QuickReplyItem(action=MessageAction(label=c, text=c)) for c in commands])

    # دالة مساعدة لإنشاء bubble
    def _create_bubble(self, contents, size="mega"):
        c = self._c()
        return {"type": "bubble", "size": size, "body": {"type": "box", "layout": "vertical",
                                                         "contents": contents,
                                                         "paddingAll": "lg",
                                                         "backgroundColor": c["bg"],
                                                         "spacing": "none"}}

    # دالة مساعدة لإنشاء زر
    def _button(self, label, text=None, style="primary", color=None, flex=1, height="sm"):
        return {"type": "button",
                "action": {"type": "message", "label": label, "text": text or label},
                "style": style,
                "color": color,
                "flex": flex,
                "height": height}

    # القائمة الرئيسية
    def main_menu(self, user=None):
        c = self._c()
        contents = [
            {"type": "text", "text": Config.BOT_NAME, "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]}
        ]

        if user:
            contents.append({
                "type": "box", "layout": "horizontal", "spacing": "md", "margin": "lg",
                "contents": [
                    {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": "اللاعب", "size": "xs", "color": c["text_tertiary"]},
                        {"type": "text", "text": user['name'], "size": "md", "weight": "bold", "color": c["text"], "margin": "xs"}
                    ], "flex": 3},
                    {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": "النقاط", "size": "xs", "color": c["text_tertiary"], "align": "end"},
                        {"type": "text", "text": str(user['points']), "size": "xl", "weight": "bold", "color": c["primary"], "align": "end", "margin": "xs"}
                    ], "flex": 2}
                ],
                "paddingAll": "md", "cornerRadius": "md", "backgroundColor": c["glass"],
                "borderWidth": "1px", "borderColor": c["border"]
            })

        # أزرار أساسية
        row1 = [
            self._button("العاب"),
            self._button("نقاطي" if user else "تسجيل", text="نقاطي" if user else "تسجيل", style="secondary")
        ]
        contents.append({"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "md", "contents": row1})

        row2 = [self._button("تغيير الاسم", style="secondary"), self._button("تبديل الثيم", text="ثيم", style="secondary")] if user \
               else [self._button("انسحب", style="secondary"), self._button("مساعدة", style="secondary")]
        contents.append({"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": row2})

        # الفوتر
        contents.extend([
            {"type": "separator", "margin": "xl", "color": c["border"]},
            {"type": "text", "text": Config.COPYRIGHT, "size": "xxs", "color": c["text_tertiary"], "align": "center", "wrap": True, "margin": "md"}
        ])

        bubble = self._create_bubble(contents)
        return FlexMessage(alt_text="البداية", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    # القائمة المساعدة (Help)
    def help_menu(self):
        c = self._c()
        sections = [
            {"title": "الأوامر الأساسية", "items": ["بداية: العودة للقائمة الرئيسية", "العاب: عرض جميع الألعاب المتاحة",
                                                    "نقاطي: عرض إحصائياتك الشخصية", "الصدارة: عرض أفضل اللاعبين",
                                                    "ثيم: تبديل بين الوضع الفاتح والداكن", "ايقاف: إيقاف اللعبة الحالية"]},
            {"title": "أوامر التسلية", "items": ["تحدي: تحديات عشوائية", "سؤال: أسئلة متنوعة", "اعتراف: اعترافات مسلية",
                                                "منشن: منشن أصدقائك", "موقف: مواقف افتراضية", "حكمة: حكم وأقوال",
                                                "شخصية: أسئلة شخصية"]},
            {"title": "الألعاب المتوفرة", "items": ["ذكاء: ألغاز ذكاء", "خمن: تخمين الكلمات", "رياضيات: عمليات حسابية",
                                                 "ترتيب: ترتيب الحروف", "ضد: عكس الكلمات", "اسرع: كتابة سريعة",
                                                 "سلسلة: سلسلة كلمات", "انسان حيوان: لعبة الفئات", "تكوين: تكوين كلمات",
                                                 "اغاني: تخمين المغني", "الوان: لعبة الألوان", "توافق: حساب التوافق"]},
            {"title": "كيفية اللعب", "items": ["1. اختر لعبة من قائمة الألعاب", "2. أجب على 5 أسئلة متتالية",
                                              "3. اكسب نقطة عن كل إجابة صحيحة", "4. استخدم ايقاف لحفظ تقدمك"]}
        ]

        contents = [{"type": "text", "text": "دليل الاستخدام", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "md", "color": c["border"]}]

        for section in sections:
            contents.append({"type": "text", "text": section["title"], "size": "md", "weight": "bold", "color": c["text"], "margin": "lg"})
            contents.append({"type": "box", "layout": "vertical", "backgroundColor": c["glass"], "cornerRadius": "8px",
                             "paddingAll": "12px", "margin": "sm",
                             "contents": [{"type": "text", "text": i, "size": "sm", "color": c["text"], "wrap": True, "margin": "xs" if idx>0 else None}
                                          for idx, i in enumerate(section["items"])]})

        # زر العودة للبداية
        contents.append(self._button("البداية", "بداية", flex=1, style="primary", color=c["primary"], height="sm"))

        bubble = self._create_bubble(contents)
        return FlexMessage(alt_text="المساعدة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    # قائمة الألعاب
    def games_menu(self):
        c = self._c()
        games_list = [["ذكاء", "خمن"], ["رياضيات", "ترتيب"], ["ضد", "اسرع"], ["سلسله", "انسان حيوان"], ["تكوين", "اغاني"], ["الوان", "توافق"]]
        contents = [{"type": "text", "text": "الألعاب المتاحة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]}]

        for row in games_list:
            contents.append({"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                             "contents": [self._button(row[0]), self._button(row[1])]})

        bubble = self._create_bubble(contents)
        return FlexMessage(alt_text="الالعاب", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())

    # البقية (stats_card, leaderboard_card, registration_choice, ask_name, ask_name_invalid, game_stopped, theme_changed)
    # يمكن تحويلها بنفس الطريقة مع دوال مساعدة للبنرات والأزرار لتقليل التكرار
        # بطاقة إحصائيات اللاعب
    def stats_card(self, user):
        c = self._c()
        win_rate = round((user['wins'] / user['games']) * 100) if user['games'] > 0 else 0

        stats_boxes = [
            {"title": "النقاط", "value": user['points'], "color": c["success"], "size": "xxl"},
            {"title": "الألعاب", "value": user['games'], "color": c["info"], "size": "xxl"},
            {"title": "الانتصارات", "value": user['wins'], "color": c["primary"], "size": "xl"},
            {"title": "نسبة الفوز", "value": f"{win_rate}%", "color": c["warning"], "size": "xl"}
        ]

        contents = [{"type": "text", "text": "إحصائياتي", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "separator", "margin": "lg", "color": c["border"]}]

        # تقسيم الصناديق في صفوف أفقية
        for i in range(0, len(stats_boxes), 2):
            row = stats_boxes[i:i+2]
            row_contents = []
            for box in row:
                row_contents.append({
                    "type": "box", "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": box["title"], "size": "xs", "color": c["text_tertiary"], "align": "center"},
                        {"type": "text", "text": str(box["value"]), "size": box["size"], "weight": "bold", "color": box["color"], "align": "center"}
                    ],
                    "flex": 1, "paddingAll": "md", "cornerRadius": "md", "backgroundColor": c["card"], "borderWidth": "1px", "borderColor": c["border"]
                })
            contents.append({"type": "box", "layout": "horizontal", "spacing": "md", "margin": "md", "contents": row_contents})

        bubble = self._create_bubble(contents)
        return FlexMessage(alt_text="إحصائياتي", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())


    # لوحة الصدارة
    def leaderboard_card(self, leaderboard):
        c = self._c()
        contents = [{"type": "text", "text": "لوحة الصدارة", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
                    {"type": "text", "text": "أفضل 10 لاعبين", "size": "xs", "color": c["text_tertiary"], "align": "center", "margin": "xs"},
                    {"type": "separator", "margin": "lg", "color": c["border"]}]

        if not leaderboard:
            contents.append({"type": "box", "layout": "vertical",
                             "contents": [{"type": "text", "text": "لا توجد بيانات بعد", "size": "md", "color": c["text_secondary"], "align": "center", "wrap": True}],
                             "paddingAll": "xl", "cornerRadius": "md", "backgroundColor": c["glass"], "margin": "lg"})
        else:
            for idx, player in enumerate(leaderboard[:10]):
                rank = idx + 1
                border_width = "3px" if rank == 1 else "2px" if rank <= 3 else "1px"
                bg_color = c["glass"] if rank <= 3 else c["card"]
                contents.append({
                    "type": "box", "layout": "horizontal", "spacing": "md",
                    "contents": [
                        {"type": "box", "layout": "vertical",
                         "contents": [{"type": "text", "text": str(rank), "size": "xl", "weight": "bold", "align": "center", "color": c["primary"]}],
                         "flex": 0, "width": "40px", "justifyContent": "center"},
                        {"type": "box", "layout": "vertical",
                         "contents": [
                             {"type": "text", "text": player['name'], "size": "md", "weight": "bold", "color": c["text"], "wrap": True},
                             {"type": "box", "layout": "horizontal", "spacing": "md", "margin": "xs",
                              "contents": [
                                  {"type": "text", "text": f"النقاط: {player['points']}", "size": "xs", "color": c["text_secondary"], "flex": 0},
                                  {"type": "text", "text": f"الفوز: {player['wins']}", "size": "xs", "color": c["text_secondary"], "flex": 0}
                              ]}
                         ], "flex": 1}
                    ],
                    "paddingAll": "md", "cornerRadius": "md", "backgroundColor": bg_color,
                    "borderWidth": border_width, "borderColor": c["border"], "margin": "sm"
                })

        # أزرار العودة
        contents.append({"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "md",
                         "contents": [self._button("البداية", "بداية", style="secondary"), self._button("نقاطي")]})


        bubble = self._create_bubble(contents)
        return FlexMessage(alt_text="لوحة الصدارة", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())


    # تسجيل الحساب
    def registration_choice(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "مرحباً بك", "size": "xxl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {"type": "box", "layout": "vertical",
             "contents": [
                 {"type": "text", "text": "للعب وكسب النقاط", "size": "md", "color": c["text"], "wrap": True, "align": "center", "weight": "bold"},
                 {"type": "text", "text": "سجل حسابك الآن", "size": "sm", "color": c["text_secondary"], "wrap": True, "align": "center", "margin": "sm"}
             ],
             "paddingAll": "md", "cornerRadius": "md", "backgroundColor": c["glass"], "margin": "lg"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg",
             "contents": [self._button("تسجيل", style="primary", color=c["success"]),
                          self._button("انسحب", style="secondary")]}
        ]
        bubble = self._create_bubble(contents)
        return FlexMessage(alt_text="مرحباً", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())


    # إدخال الاسم
    def ask_name(self, invalid=False):
        c = self._c()
        title = "اسم غير صالح" if invalid else "التسجيل"
        title_color = c["danger"] if invalid else c["primary"]
        subtitle = "يرجى إدخال اسم صحيح" if invalid else "يرجى إدخال اسمك"
        extra_text = [
            {"text": "من 1 إلى 50 حرف", "size": "xs", "color": c["text_secondary"]},
            {"text": "حروف عربية أو إنجليزية فقط", "size": "xs", "color": c["text_secondary"]},
            {"text": "لا يمكن استخدام أوامر البوت كاسم", "size": "xs", "color": c["text_secondary"]}
        ] if invalid else [{"text": "من 1 إلى 50 حرف", "size": "xs", "color": c["text_tertiary"]}]

        contents = [
            {"type": "text", "text": title, "size": "xl", "weight": "bold", "color": title_color, "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "box", "layout": "vertical",
             "contents": [{"type": "text", "text": subtitle, "size": "md", "color": c["text"], "wrap": True, "align": "center", "weight": "bold"}] + 
                         [{"type": "text", **t, "align": "center", "margin": "sm"} for t in extra_text],
             "paddingAll": "md", "cornerRadius": "md", "backgroundColor": c["glass"], "margin": "lg"}
        ]

        bubble = self._create_bubble(contents)
        return FlexMessage(alt_text=title, contents=FlexContainer.from_dict(bubble), quickReply=self._qr())


    # تم إيقاف اللعبة
    def game_stopped(self):
        c = self._c()
        contents = [
            {"type": "text", "text": "تم إيقاف اللعبة", "size": "xl", "weight": "bold", "color": c["warning"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "text", "text": "يمكنك بدء لعبة جديدة في أي وقت", "size": "sm", "color": c["text_secondary"], "wrap": True, "align": "center", "margin": "lg"},
            self._button("العاب")
        ]
        bubble = self._create_bubble(contents)
        return FlexMessage(alt_text="تم الإيقاف", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())


    # تغيير الثيم
    def theme_changed(self, theme_name):
        c = self._c()
        contents = [
            {"type": "text", "text": "تم تبديل الثيم", "size": "xl", "weight": "bold", "color": c["primary"], "align": "center"},
            {"type": "separator", "margin": "md", "color": c["border"]},
            {"type": "box", "layout": "vertical",
             "contents": [{"type": "text", "text": theme_name, "size": "lg", "color": c["text"], "wrap": True, "align": "center", "weight": "bold"}],
             "paddingAll": "md", "cornerRadius": "md", "backgroundColor": c["glass"], "margin": "lg"}
        ]
        bubble = self._create_bubble(contents)
        return FlexMessage(alt_text="تم التبديل", contents=FlexContainer.from_dict(bubble), quickReply=self._qr())
