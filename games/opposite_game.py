"""
لعبة الأضداد - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
✅ دعم فردي + فريقين
✅ عداد زمني بسيط + مكافأة سرعة
✅ توافق آمن مع BaseGame (fallback إذا لم تتوفر دوال الفريق)
"""

from games.base_game import BaseGame
import random
from datetime import datetime
from typing import Dict, Any, Optional


class OppositeGame(BaseGame):
    """لعبة الأضداد"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "أضداد"
        self.game_icon = "↔️"

        # افتراضي وضع الفريق مغلق — يمكن للـ app ضبط game_instance.team_mode = True
        self.team_mode = False
        self.joined_users = set()  # إذا أراد الكود الداخلي تتبع المنضمين محلياً

        self.opposites = [
            {"word": "كبير", "opposite": ["صغير"]},
            {"word": "طويل", "opposite": ["قصير"]},
            {"word": "سريع", "opposite": ["بطيء"]},
            {"word": "قوي", "opposite": ["ضعيف"]},
            {"word": "حار", "opposite": ["بارد"]},
            {"word": "نظيف", "opposite": ["وسخ", "قذر"]},
            {"word": "سهل", "opposite": ["صعب"]},
            {"word": "جميل", "opposite": ["قبيح"]},
            {"word": "غني", "opposite": ["فقير"]},
            {"word": "ثقيل", "opposite": ["خفيف"]},
            {"word": "عميق", "opposite": ["سطحي"]},
            {"word": "واسع", "opposite": ["ضيق"]},
            {"word": "مظلم", "opposite": ["مضيء"]},
            {"word": "رطب", "opposite": ["جاف"]},
            {"word": "قديم", "opposite": ["جديد"]},
            {"word": "بعيد", "opposite": ["قريب"]},
            {"word": "مرتفع", "opposite": ["منخفض"]},
            {"word": "داخل", "opposite": ["خارج"]},
            {"word": "ناعم", "opposite": ["خشن"]},
            {"word": "حلو", "opposite": ["مر"]},
            {"word": "ذكي", "opposite": ["غبي"]},
            {"word": "نشط", "opposite": ["كسول"]},
            {"word": "مفتوح", "opposite": ["مغلق"]},
            {"word": "ممتلئ", "opposite": ["فارغ"]},
            {"word": "هادئ", "opposite": ["صاخب"]},
            {"word": "واضح", "opposite": ["غامض"]},
            {"word": "مستقيم", "opposite": ["منحني"]},
            {"word": "سعيد", "opposite": ["حزين"]},
            {"word": "سميك", "opposite": ["رفيع"]},
            {"word": "مشرق", "opposite": ["قاتم"]},
            {"word": "مجتهد", "opposite": ["مهمل"]},
            {"word": "خفيف", "opposite": ["ثقيل"]},
            {"word": "صافي", "opposite": ["عكر"]},
            {"word": "مرتب", "opposite": ["فوضوي"]},
            {"word": "لطيف", "opposite": ["قاس"]},
        ]
        random.shuffle(self.opposites)
        self.used_words = []
        self.question_start_time: Optional[datetime] = None

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.used_words = []
        self.question_start_time = None
        return self.get_question()

    def get_question(self):
        """إنشاء سؤال واجهة Flex (بدون backgroundColor في body/boxes لتوافق LINE)"""
        available = [w for w in self.opposites if w not in self.used_words]
        if not available:
            self.used_words = []
            available = self.opposites.copy()

        q_data = random.choice(available)
        self.used_words.append(q_data)
        self.current_answer = q_data["opposite"]
        self.question_start_time = datetime.utcnow()

        colors = self.get_theme_colors()

        previous_section = []
        if self.previous_question and self.previous_answer:
            previous_section = [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "السؤال السابق", "size": "xs", "color": colors["text2"]},
                        {"type": "text", "text": self.previous_question, "size": "xs", "color": colors["text2"], "wrap": True},
                        {"type": "text", "text": f"الضد: {self.previous_answer}", "size": "xs", "color": colors["success"], "wrap": True},
                    ],
                    "cornerRadius": "12px",
                    "paddingAll": "10px",
                    "margin": "md"
                }
            ]

        # نص السؤال الرئيسي (لا نستخدم backgroundColor داخل body أو الصناديق)
        body_contents = [
            {"type": "text", "text": self.game_name, "size": "xxl", "weight": "bold", "color": colors["text"], "align": "center"},
            {"type": "separator", "margin": "lg"},
        ] + previous_section + [
            {"type": "text", "text": "ما هو عكس هذه الكلمة؟", "size": "md", "color": colors["text"], "align": "center", "margin": "lg"},
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": q_data["word"], "size": "xxl", "weight": "bold", "align": "center", "color": colors["primary"]}
                ],
                "cornerRadius": "16px",
                "paddingAll": "20px",
                "margin": "md"
            }
        ]

        # زر الإيقاف فقط في الفوتر عبر _create_flex_with_buttons
        flex_content = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": body_contents,
                "paddingAll": "18px"
            },
            # ضع لون الخلفية بالطريقة المقبولة: styles.body.backgroundColor
            "styles": {
                "body": {
                    "backgroundColor": colors["bg"]
                }
            }
        }

        return self._create_flex_with_buttons(self.game_name, flex_content)

    def _user_team_helpers(self, user_id: str):
        """
        Helper to safely call optional team-related methods that may exist
        in the broader project. Returns tuple (team_name or None, add_team_score_callable or None)
        """
        team = None
        add_team = None
        try:
            if hasattr(self, "get_user_team"):
                team = self.get_user_team(user_id)
        except Exception:
            team = None
        try:
            if hasattr(self, "add_team_score"):
                add_team = getattr(self, "add_team_score")
        except Exception:
            add_team = None
        return team, add_team

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """التحقق من الإجابة مع دعم فريقي + عداد زمني"""
        if not self.game_active:
            return None

        normalized = self.normalize_text(user_answer)

        # منع غير المنضمين في وضع الفريقين (إن كان هناك تتبع محلي)
        if self.team_mode:
            if hasattr(self, "joined_users") and self.joined_users and (user_id not in self.joined_users):
                return None

        # حساب زمن الإجابة
        time_taken = 0.0
        if self.question_start_time:
            time_taken = (datetime.utcnow() - self.question_start_time).total_seconds()

        # دعم التلميح وكشف الإجابة في الوضع الفردي فقط
        if not self.team_mode:
            if normalized == "لمح":
                # تلميح: حرف البداية وعدد الحروف من أول إجابة مقصودة
                if self.current_answer and len(self.current_answer) > 0:
                    hint_base = self.current_answer[0]
                    hint = f"💡 يبدأ بحرف '{hint_base[0]}' • عدد الاحتمالات: {len(self.current_answer)}"
                else:
                    hint = "💡 فكر جيداً!"
                return {"message": hint, "response": self._create_text_message(hint), "points": 0}

            if normalized == "جاوب":
                answer_text = " أو ".join(self.current_answer)
                reveal = f"📝 الإجابة: {answer_text}"
                # حفظ السجل السابق
                if self.used_words:
                    self.previous_question = self.used_words[-1]["word"]
                    self.previous_answer = answer_text
                # الانتقال للسؤال التالي
                self.current_question += 1
                self.answered_users.clear()
                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result["message"] = f"{reveal}\n\n{result.get('message','')}"
                    return result
                return {"message": reveal, "response": self.get_question(), "points": 0}

        # التحقق من الإجابة الصحيحة
        for correct in self.current_answer:
            if self.normalize_text(correct) == normalized:
                # تم التصحيح: وضع فريقي
                if self.team_mode:
                    # نحاول استخدام دوال الفريق إن وُجدت، وإلا نمنح نقاط فردية كبديل
                    team, add_team = self._user_team_helpers(user_id)
                    points = 10
                    if not team:
                        # محاولة تعيين فريق إن وُجد assign_to_team
                        try:
                            if hasattr(self, "assign_to_team"):
                                team = self.assign_to_team(user_id)
                        except Exception:
                            team = None
                    if add_team and team:
                        try:
                            add_team(team, points)
                        except Exception:
                            # فشل في إضافة نقاط الفريق -> fallback لإضافة نقاط للاعب
                            try:
                                self.add_score(user_id, display_name, points)
                            except Exception:
                                pass
                    else:
                        # fallback: نقاط فردية
                        try:
                            self.add_score(user_id, display_name, points)
                        except Exception:
                            pass

                else:
                    # وضع فردي: مكافأة سرعة
                    base_points = 10
                    speed_bonus = 5 if time_taken > 0 and time_taken < 5 else 0
                    total = base_points + speed_bonus
                    # add_score قد تعيد 0 إن المستخدم أجاب سابقاً، لكن هنا نريد تسجيل النقاط
                    try:
                        self.add_score(user_id, display_name, total)
                    except Exception:
                        pass
                    points = total

                # حفظ السابق والانتقال
                if self.used_words:
                    self.previous_question = self.used_words[-1]["word"]
                    self.previous_answer = correct

                self.current_question += 1
                self.answered_users.clear()

                # نهاية الجولة؟
                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result["points"] = points if "points" in locals() else 0
                    result["message"] = f"✅ صحيح!\n+{result.get('points',0)} نقطة\n\n{result.get('message','')}"
                    return result

                # رسالة نجاح
                msg = f"✅ إجابة صحيحة\n+{points} نقطة"
                if not self.team_mode and speed_bonus:
                    msg = f"✅ إجابة صحيحة • {time_taken:.1f}ث\n+{points} نقطة (مكافأة سرعة +{speed_bonus})"

                return {"message": msg, "response": self.get_question(), "points": points}

        # إجابة خاطئة
        return {"message": "❌ إجابة غير صحيحة، حاول مرة أخرى", "response": self._create_text_message("❌ إجابة غير صحيحة"), "points": 0}
