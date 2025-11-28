"""
لعبة الأضداد - Bot Mesh v8.5
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class OppositeGame(BaseGame):
    """لعبة الأضداد - فردي + فريقين"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "أضداد"
        self.game_icon = "↔️"
        self.supports_hint = True
        self.supports_reveal = True

        # قاعدة الأضداد (50+ زوج)
        self.opposites = {
            "كبير": ["صغير"],
            "طويل": ["قصير"],
            "سريع": ["بطيء"],
            "ساخن": ["بارد"],
            "نظيف": ["وسخ"],
            "جديد": ["قديم"],
            "صعب": ["سهل"],
            "قوي": ["ضعيف"],
            "غني": ["فقير"],
            "سعيد": ["حزين"],
            "جميل": ["قبيح"],
            "ثقيل": ["خفيف"],
            "عالي": ["منخفض"],
            "واسع": ["ضيق"],
            "قريب": ["بعيد"],
            "مفتوح": ["مغلق"],
            "نهار": ["ليل"],
            "شمس": ["قمر"],
            "شتاء": ["صيف"],
            "شرق": ["غرب"],
            "شمال": ["جنوب"],
            "أبيض": ["أسود"],
            "حلو": ["مر"],
            "حار": ["بارد"],
            "جاف": ["رطب"],
            "مالح": ["حلو"],
            "صحيح": ["خطأ"],
            "حي": ["ميت"],
            "نور": ["ظلام"],
            "فوق": ["تحت"],
            "يمين": ["يسار"],
            "أمام": ["خلف"],
            "داخل": ["خارج"],
            "صباح": ["مساء"],
            "أول": ["آخر"],
            "كثير": ["قليل"],
            "عميق": ["سطحي"],
            "ممتلئ": ["فارغ"],
            "ناعم": ["خشن"],
            "لين": ["صلب"],
            "حاد": ["كليل"],
            "واضح": ["غامض"],
            "نشيط": ["كسول"],
            "صامت": ["صاخب"],
            "هادئ": ["صاخب"],
            "مبلل": ["جاف"],
            "مضيء": ["مظلم"],
            "رخيص": ["غالي"],
            "بسيط": ["معقد"],
            "عريض": ["ضيق"]
        }

        self.questions_list = list(self.opposites.items())
        random.shuffle(self.questions_list)

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        word, opposites = self.questions_list[self.current_question % len(self.questions_list)]
        self.current_answer = opposites

        question_text = f"ما هو عكس كلمة:\n\n{word}"
        
        # إخفاء لمح/جاوب في وضع الفريقين
        additional_info = None if self.team_mode else "اكتب 'لمح' للتلميح أو 'جاوب' للإجابة"

        return self.build_question_flex(
            question_text=question_text,
            additional_info=additional_info
        )

    def get_hint(self) -> str:
        """الحصول على تلميح"""
        if not self.current_answer:
            return "لا توجد تلميحات متاحة"
        
        answer = self.current_answer[0]
        if len(answer) <= 2:
            return f"الكلمة قصيرة: {answer[0]}_"
        
        # إظهار أول حرفين
        hint = f"{answer[0]}{answer[1]}" + "_" * (len(answer) - 2)
        return f"💡 تلميح: {hint}"

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)
        
        # في وضع الفريقين: تجاهل غير المنضمين
        if self.team_mode and user_id not in self.joined_users:
            return None
        
        # في وضع الفريقين: لا يوجد لمح أو جاوب
        if self.team_mode and normalized in ["لمح", "جاوب"]:
            return None

        # الوضع الفردي فقط
        if not self.team_mode:
            # التلميح
            if normalized == "لمح":
                hint = self.get_hint()
                return {
                    "message": hint,
                    "response": self._create_text_message(hint),
                    "points": 0
                }

            # كشف الإجابة
            if normalized == "جاوب":
                answers_text = " أو ".join(self.current_answer)
                self.current_question += 1
                self.answered_users.clear()

                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result["message"] = f"الإجابة: {answers_text}\n\n{result.get('message','')}"
                    return result

                return {
                    "message": f"الإجابة: {answers_text}",
                    "response": self.get_question(),
                    "points": 0
                }

        # التحقق من الإجابة
        for correct_answer in self.current_answer:
            if self.normalize_text(correct_answer) == normalized:
                
                # نقاط الفريقين أو الفردي
                if self.team_mode:
                    team = self.get_user_team(user_id)
                    if not team:
                        team = self.assign_to_team(user_id)
                    self.add_team_score(team, 10)
                    points = 10
                else:
                    points = self.add_score(user_id, display_name, 10)

                self.current_question += 1
                self.answered_users.clear()

                if self.current_question >= self.questions_count:
                    result = self.end_game()
                    result["points"] = points
                    
                    if self.team_mode:
                        result["message"] = f"إجابة صحيحة\n+{points} نقطة\n\n{result.get('message', '')}"
                    else:
                        result["message"] = (
                            f"إجابة صحيحة يا {display_name}\n"
                            f"الكلمة: {correct_answer}\n"
                            f"+{points} نقطة\n\n"
                            f"{result.get('message', '')}"
                        )
                    return result

                msg = f"إجابة صحيحة\n+{points} نقطة" if self.team_mode else f"إجابة صحيحة يا {display_name}\nالكلمة: {correct_answer}\n+{points} نقطة"
                
                return {
                    "message": msg,
                    "response": self.get_question(),
                    "points": points
                }

        return {
            "message": "إجابة غير صحيحة، حاول مرة أخرى",
            "response": self._create_text_message("إجابة غير صحيحة، حاول مرة أخرى"),
            "points": 0
        }

    def get_game_info(self) -> Dict[str, Any]:
        return {
            "name": self.game_name,
            "description": "اكتشف الكلمة المضادة",
            "questions_count": self.questions_count,
            "supports_hint": True,
            "supports_reveal": True,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores),
            "team_mode": self.team_mode
        }
