from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from config import Config


class UI:
    """واجهة المستخدم الأنيقة"""
    
    def __init__(self, theme: str = "light"):
        self.theme = theme

    def _c(self):
        """الحصول على ألوان السمة"""
        return Config.get_theme(self.theme)

    def _quick_reply(self):
        return QuickReply(items=[
            QuickReplyItem(action=MessageAction(label="القائمة", text="بداية")),
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
            QuickReplyItem(action=MessageAction(label="مساعدة", text="مساعدة"))
        ])

    def _create_bubble(self, contents):
        """إنشاء فقاعة رسالة"""
        c = self._c()
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "paddingAll": "24px",
                "spacing": "md",
                "backgroundColor": c["bg"]
            }
        }

    def _create_button(self, label, text, style="secondary", color=None):
        """إنشاء زر"""
        btn = {
            "type": "button",
            "action": {"type": "message", "label": label, "text": text},
            "style": style,
            "height": "sm"
        }
        if color:
            btn["color"] = color
        return btn

    def _create_header(self, title, subtitle=None):
        """إنشاء عنوان أنيق"""
        c = self._c()
        items = [
            {
                "type": "text",
                "text": title,
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            }
        ]
        if subtitle:
            items.append({
                "type": "text",
                "text": subtitle,
                "size": "sm",
                "color": c["text_tertiary"],
                "align": "center",
                "margin": "xs"
            })
        return items

    def _create_separator(self):
        """إنشاء فاصل"""
        return {"type": "separator", "margin": "lg", "color": self._c()["border"]}

    def main_menu(self, user=None):
        """القائمة الرئيسية"""
        c = self._c()
        theme_name = "فاتح" if self.theme == "light" else "داكن"

        contents = self._create_header(Config.BOT_NAME, f"الإصدار {Config.VERSION}")
        contents.append(self._create_separator())

        # معلومات المستخدم
        if user:
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"مرحبا {user['name']}",
                        "size": "lg",
                        "weight": "bold",
                        "color": c["text"],
                        "flex": 3
                    },
                    {
                        "type": "text",
                        "text": f"{user['points']}",
                        "size": "lg",
                        "weight": "bold",
                        "color": c["success"],
                        "align": "end",
                        "flex": 2
                    }
                ],
                "margin": "lg",
                "paddingAll": "16px",
                "cornerRadius": "12px",
                "backgroundColor": c["glass"],
                "borderWidth": "1px",
                "borderColor": c["border"]
            })

        # الألعاب
        contents.append({
            "type": "text",
            "text": "الألعاب",
            "size": "md",
            "weight": "bold",
            "color": c["text_secondary"],
            "margin": "xl"
        })
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                self._create_button("ابدأ اللعب", "العاب", "primary", c["primary"]),
                self._create_button("انسحب", "انسحب")
            ]
        })

        # الملف الشخصي
        contents.append({
            "type": "text",
            "text": "ملفي",
            "size": "md",
            "weight": "bold",
            "color": c["text_secondary"],
            "margin": "xl"
        })
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                self._create_button(
                    "نقاطي" if user else "تسجيل",
                    "نقاطي" if user else "تسجيل",
                    "primary" if not user else "secondary",
                    c["primary"] if not user else None
                ),
                self._create_button("الصدارة", "الصدارة")
            ]
        })

        # الإعدادات (للمستخدمين المسجلين فقط)
        if user:
            contents.append({
                "type": "text",
                "text": "الإعدادات",
                "size": "md",
                "weight": "bold",
                "color": c["text_secondary"],
                "margin": "xl"
            })
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    self._create_button(f"الوضع {theme_name}", "ثيم"),
                    self._create_button("تغيير الاسم", "تغيير الاسم")
                ]
            })

        return FlexMessage(
            alt_text="القائمة الرئيسية",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def games_menu(self):
        """قائمة الألعاب"""
        c = self._c()
        contents = self._create_header("الألعاب المتاحة")
        contents.append(self._create_separator())

        # ألعاب ذهنية
        contents.append({
            "type": "text",
            "text": "ألعاب ذهنية",
            "size": "md",
            "weight": "bold",
            "color": c["text_secondary"],
            "margin": "lg"
        })
        contents.extend([
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    self._create_button("ذكاء", "ذكاء", "primary", c["primary"]),
                    self._create_button("خمن", "خمن", "primary", c["secondary"]),
                    self._create_button("رياضيات", "رياضيات", "primary", c["success"])
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm",
                "contents": [
                    self._create_button("ترتيب", "ترتيب"),
                    self._create_button("ضد", "ضد"),
                    self._create_button("اسرع", "اسرع")
                ]
            }
        ])

        # ألعاب كلمات
        contents.append({
            "type": "text",
            "text": "ألعاب كلمات",
            "size": "md",
            "weight": "bold",
            "color": c["text_secondary"],
            "margin": "lg"
        })
        contents.extend([
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    self._create_button("سلسلة", "سلسله"),
                    self._create_button("انسان حيوان", "انسان حيوان")
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm",
                "contents": [
                    self._create_button("كون كلمات", "كون كلمات"),
                    self._create_button("اغاني", "اغاني")
                ]
            }
        ])

        # ألعاب أخرى
        contents.append({
            "type": "text",
            "text": "ألعاب أخرى",
            "size": "md",
            "weight": "bold",
            "color": c["text_secondary"],
            "margin": "lg"
        })
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                self._create_button("الوان", "الوان"),
                self._create_button("مافيا", "مافيا"),
                self._create_button("توافق", "توافق")
            ]
        })

        # زر العودة
        contents.append(self._create_separator())
        contents.append(self._create_button("العودة", "بداية", "primary", c["primary"]))

        return FlexMessage(
            alt_text="الألعاب",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def help_menu(self):
        """قائمة المساعدة"""
        c = self._c()
        contents = self._create_header("المساعدة", "دليل الاستخدام")
        contents.append(self._create_separator())

        sections = [
            ("الأوامر الرئيسية", "بداية - تسجيل - العاب - نقاطي - الصدارة"),
            ("ألعاب ذهنية", "ذكاء - خمن - رياضيات - ترتيب - ضد - اسرع"),
            ("ألعاب كلمات", "سلسله - انسان حيوان - كون كلمات - اغاني"),
            ("ألعاب أخرى", "الوان - مافيا - توافق"),
            ("محتوى تفاعلي", "تحدي - سؤال - اعتراف - منشن - موقف - حكمة - شخصية"),
            ("التحكم", "انسحب - ايقاف - ثيم - تغيير الاسم")
        ]

        for title, items in sections:
            contents.extend([
                {
                    "type": "text",
                    "text": title,
                    "size": "sm",
                    "weight": "bold",
                    "color": c["text_secondary"],
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": items,
                    "size": "xs",
                    "color": c["text"],
                    "wrap": True,
                    "margin": "xs"
                }
            ])

        contents.append(self._create_separator())
        contents.append(self._create_button("العودة", "بداية", "primary", c["primary"]))

        return FlexMessage(
            alt_text="المساعدة",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def stats_card(self, user):
        """بطاقة الإحصائيات"""
        c = self._c()
        win_rate = round((user['wins'] / user['games'] * 100)) if user['games'] > 0 else 0

        contents = self._create_header("إحصائياتي")
        contents.append(self._create_separator())

        stats = [
            ("الاسم", user['name'], c["text"]),
            ("النقاط", str(user['points']), c["success"]),
            ("الألعاب", str(user['games']), c["text"]),
            ("الفوز", str(user['wins']), c["info"]),
            ("نسبة الفوز", f"{win_rate}%", c["primary"])
        ]

        for i, (label, value, color) in enumerate(stats):
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": label,
                        "size": "sm",
                        "color": c["text_secondary"],
                        "flex": 2
                    },
                    {
                        "type": "text",
                        "text": value,
                        "size": "sm",
                        "weight": "bold",
                        "color": color,
                        "align": "end",
                        "flex": 3
                    }
                ],
                "margin": "lg" if i == 0 else "md",
                "paddingAll": "12px",
                "cornerRadius": "8px",
                "backgroundColor": c["glass"]
            })

        contents.append(self._create_separator())
        contents.append(self._create_button("العودة", "بداية", "primary", c["primary"]))

        return FlexMessage(
            alt_text="إحصائياتي",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def leaderboard_card(self, top_users):
        """بطاقة الصدارة"""
        c = self._c()
        contents = self._create_header("لوحة الصدارة", "أفضل اللاعبين")
        contents.append(self._create_separator())

        for i, u in enumerate(top_users, 1):
            rank_color = c["primary"] if i == 1 else c["secondary"] if i == 2 else c["success"] if i == 3 else c["text"]
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": str(i),
                        "size": "lg",
                        "weight": "bold",
                        "color": rank_color,
                        "flex": 1,
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": u['name'],
                                "size": "sm",
                                "weight": "bold",
                                "color": c["text"]
                            },
                            {
                                "type": "text",
                                "text": f"{u['wins']} فوز من {u['games']} لعبة",
                                "size": "xs",
                                "color": c["text_tertiary"]
                            }
                        ],
                        "flex": 4
                    },
                    {
                        "type": "text",
                        "text": str(u['points']),
                        "size": "md",
                        "weight": "bold",
                        "color": c["success"],
                        "flex": 2,
                        "align": "end"
                    }
                ],
                "margin": "lg" if i == 1 else "md",
                "paddingAll": "12px",
                "cornerRadius": "8px",
                "backgroundColor": c["glass"]
            })

        contents.append(self._create_separator())
        contents.append(self._create_button("العودة", "بداية", "primary", c["primary"]))

        return FlexMessage(
            alt_text="الصدارة",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def ask_name(self):
        """طلب إدخال الاسم"""
        c = self._c()
        contents = self._create_header("التسجيل", "أدخل اسمك للبدء")
        return FlexMessage(
            alt_text="تسجيل الاسم",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def ask_name_invalid(self):
        """اسم غير صالح"""
        c = self._c()
        contents = self._create_header("اسم غير صالح", "يرجى إدخال اسم صحيح")
        return FlexMessage(
            alt_text="اسم غير صالح",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def ask_new_name(self):
        """طلب اسم جديد"""
        c = self._c()
        contents = self._create_header("تغيير الاسم", "أدخل اسمك الجديد")
        return FlexMessage(
            alt_text="تغيير الاسم",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def ask_new_name_invalid(self):
        """اسم جديد غير صالح"""
        c = self._c()
        contents = self._create_header("اسم غير صالح", "يرجى إدخال اسم صحيح")
        return FlexMessage(
            alt_text="اسم غير صالح",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def game_stopped(self):
        """رسالة إيقاف اللعبة"""
        c = self._c()
        contents = self._create_header("تم إيقاف اللعبة")
        contents.append(self._create_separator())
        contents.append(self._create_button("العودة", "بداية", "primary", c["primary"]))
        return FlexMessage(
            alt_text="تم إيقاف اللعبة",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )

    def registration_required(self):
        """رسالة التسجيل مطلوب"""
        c = self._c()
        contents = self._create_header("التسجيل مطلوب")
        contents.append(self._create_separator())
        contents.append(self._create_button("تسجيل", "تسجيل", "primary", c["primary"]))
        return FlexMessage(
            alt_text="التسجيل مطلوب",
            contents=FlexContainer.from_dict(self._create_bubble(contents)),
            quickReply=self._quick_reply()
        )
