from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class OppositeGame(BaseGame):
    """لعبة الأضداد - فردي + فريقين"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "أضداد"
        self.game_icon = "▫️"
        self.supports_hint = True
        self.supports_reveal = True

        self.opposites = {
            "كبير": ["صغير", "قصير", "ضئيل", "محدود"],
            "طويل": ["قصير", "قزم"],
            "سريع": ["بطيء", "متمهل"],
            "ساخن": ["بارد", "مثلج"],
            "نظيف": ["وسخ", "قذر", "متسخ"],
            "جديد": ["قديم", "عتيق"],
            "صعب": ["سهل", "بسيط", "ميسر"],
            "قوي": ["ضعيف", "واهن"],
            "غني": ["فقير", "معدم"],
            "سعيد": ["حزين", "تعيس", "كئيب"],
            "جميل": ["قبيح", "دميم"],
            "ثقيل": ["خفيف", "طائر"],
            "عالي": ["منخفض", "واطي"],
            "واسع": ["ضيق", "محدود"],
            "قريب": ["بعيد", "نائي"],
            "مفتوح": ["مغلق", "مقفل"],
            "نهار": ["ليل", "مساء"],
            "شمس": ["قمر", "نجم"],
            "شتاء": ["صيف", "حر"],
            "شرق": ["غرب", "مغرب"],
            "شمال": ["جنوب", "قبلة"],
            "أبيض": ["أسود", "معتم"],
            "حلو": ["مر", "حامض", "مالح"],
            "حار": ["بارد", "ثلجي"],
            "جاف": ["رطب", "مبلل"],
            "مالح": ["حلو", "عذب"],
            "صحيح": ["خطأ", "خاطئ", "غلط"],
            "حي": ["ميت", "متوفي"],
            "نور": ["ظلام", "ظلمة", "عتمة"],
            "فوق": ["تحت", "أسفل"],
            "يمين": ["يسار", "شمال"],
            "أمام": ["خلف", "وراء", "دبر"],
            "داخل": ["خارج", "برا"],
            "صباح": ["مساء", "عصر", "ليل"],
            "أول": ["آخر", "نهاية"],
            "كثير": ["قليل", "نادر"],
            "عميق": ["سطحي", "ضحل"],
            "ممتلئ": ["فارغ", "خالي"],
            "ناعم": ["خشن", "قاسي"],
            "لين": ["صلب", "قاسي"],
            "حاد": ["كليل", "غير حاد"],
            "واضح": ["غامض", "مبهم"],
            "نشيط": ["كسول", "خامل"],
            "صامت": ["صاخب", "مزعج"],
            "هادئ": ["صاخب", "عالي"],
            "مبلل": ["جاف", "ناشف"],
            "مضيء": ["مظلم", "معتم"],
            "رخيص": ["غالي", "ثمين"],
            "بسيط": ["معقد", "صعب"],
            "عريض": ["ضيق", "نحيف"]
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
        
        if self.can_use_hint() and self.can_reveal_answer():
            additional_info = "اكتب 'لمح' للتلميح أو 'جاوب' للإجابة"
        else:
            additional_info = None

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
        
        hint = f"{answer[0]}{answer[1]}" + "_" * (len(answer) - 2)
        return f"تلميح: {hint}"

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)
        
        if self.team_mode and user_id not in self.joined_users:
            return None

        if self.can_use_hint() and normalized == "لمح":
            hint = self.get_hint()
            return {
                "message": hint,
                "response": self._create_text_message(hint),
                "points": 0
            }

        if self.can_reveal_answer() and normalized == "جاوب":
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

        if self.team_mode and normalized in ["لمح", "جاوب"]:
            return None

        for correct_answer in self.current_answer:
            if self.normalize_text(correct_answer) == normalized:
                
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
