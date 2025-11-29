"""
لعبة ألوان (Stroop Effect) - Bot Mesh v13.0 FINAL
Created by: Abeer Aldosari © 2025
✅ 1 نقطة فقط (بدون بونص)
✅ عرض السؤال السابق
✅ Flex بدلاً من TextMessage
"""

from games.base_game import BaseGame
import random
import time
from typing import Dict, Any, Optional


class WordColorGame(BaseGame):
    """لعبة ألوان - اختبار Stroop"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "ألوان"
        self.game_icon = "▪️"
        self.supports_hint = False  # ❌ لعبة بصرية
        self.supports_reveal = False  # ❌ لعبة بصرية

        self.round_time = 15  # ⏱️ 15 ثانية
        self.round_start_time = None

        self.colors = {
            "أحمر": "#E53E3E",
            "أزرق": "#3182CE",
            "أخضر": "#38A169",
            "أصفر": "#D69E2E",
            "برتقالي": "#DD6B20",
            "بنفسجي": "#805AD5",
            "وردي": "#D53F8C",
            "بني": "#8B4513"
        }
        self.color_names = list(self.colors.keys())
        self.current_word = None
        self.current_color_name = None

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        return self.get_question()

    def get_question(self):
        # اختيار كلمة ولون مختلف (70% من الوقت)
        word = random.choice(self.color_names)
        color_name = random.choice([c for c in self.color_names if c != word]) if random.random() < 0.7 else word
        
        self.current_word = word
        self.current_color_name = color_name
        self.current_answer = [color_name]
        self.round_start_time = time.time()

        colors = self.get_theme_colors()
        display_color = self.colors[color_name]

        # بناء Flex بدلاً من TextMessage
        flex_contents = [
            {"type": "text", "text": f"{self.game_icon} {self.game_name}", "size": "xl", "weight": "bold", "color": colors["primary"], "align": "center"},
            {"type": "text", "text": f"سؤال {self.current_question + 1} من {self.questions_count}", "size": "sm", "color": colors["text2"], "align": "center", "margin": "xs"},
            {"type": "separator", "margin": "lg", "color": colors["border"]}
        ]
        
        # عرض السؤال السابق والإجابة
        if self.previous_question and self.previous_answer:
            prev_answer_text = self.previous_answer if isinstance(self.previous_answer, str) else (self.previous_answer[0] if isinstance(self.previous_answer, list) and self.previous_answer else "")
            
            flex_contents.append({
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "▪️ السؤال السابق", "size": "xs", "color": colors["text3"], "weight": "bold"},
                    {"type": "text", "text": str(self.previous_question)[:30] + "..." if len(str(self.previous_question)) > 30 else str(self.previous_question), "size": "xs", "color": colors["text2"], "wrap": True, "margin": "xs"},
                    {"type": "text", "text": f"▪️ الإجابة: {prev_answer_text}", "size": "xs", "color": colors["success"], "wrap": True, "margin": "xs"}
                ],
                "backgroundColor": colors["info_bg"],
                "cornerRadius": "10px",
                "paddingAll": "10px",
                "margin": "md"
            })
            flex_contents.append({"type": "separator", "margin": "md", "color": colors["border"]})
        
        # السؤال الحالي - الكلمة الملونة
        flex_contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "ما لون هذه الكلمة؟", "size": "md", "color": colors["text2"], "align": "center", "wrap": True},
                {"type": "text", "text": word, "size": "xxl", "weight": "bold", "color": display_color, "align": "center", "margin": "lg"}
            ],
            "cornerRadius": "15px",
            "paddingAll": "20px",
            "margin": "lg",
            "borderWidth": "2px",
            "borderColor": colors["border"]
        })
        
        # معلومات إضافية
        flex_contents.append({
            "type": "text",
            "text": f"⏱️ {self.round_time} ثانية",
            "size": "xs",
            "color": colors["text2"],
            "align": "center",
            "margin": "md"
        })
        
        flex_content = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": flex_contents,
                "paddingAll": "20px"
            }
        }
        
        return self._create_flex_with_buttons(self.game_name, flex_content)

    def _time_expired(self) -> bool:
        if not self.round_start_time:
            return False
        return (time.time() - self.round_start_time) > self.round_time

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        # التحقق من الوقت
        if self._time_expired():
            correct_answer = self.current_answer[0]
            self.previous_question = f"كلمة '{self.current_word}' ملونة بـ"
            self.previous_answer = correct_answer
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["message"] = f"⏱️ انتهى الوقت!\n▪️ الإجابة: {correct_answer}\n\n{result.get('message', '')}"
                return result

            return {
                "message": f"⏱️ انتهى الوقت!\n▪️ الإجابة: {correct_answer}",
                "response": self.get_question(),
                "points": 0
            }

        if user_id in self.answered_users:
            return None

        if self.team_mode and user_id not in self.joined_users:
            return None

        normalized = self.normalize_text(user_answer)
        correct = self.normalize_text(self.current_answer[0])

        if normalized == correct:
            # نقطة واحدة فقط (بدون بونص الوقت)
            total_points = 1

            if self.team_mode:
                team = self.get_user_team(user_id)
                if not team:
                    team = self.assign_to_team(user_id)
                self.add_team_score(team, total_points)
            else:
                self.add_score(user_id, display_name, total_points)

            self.previous_question = f"كلمة '{self.current_word}' ملونة بـ"
            self.previous_answer = self.current_answer[0]

            self.answered_users.add(user_id)
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result["points"] = total_points
                return result

            return {
                "message": f"▪️ صحيح!\n+{total_points} نقطة",
                "response": self.get_question(),
                "points": total_points
            }

        return {
            "message": "▪️ خطأ",
            "response": self._create_text_message("▪️ خطأ"),
            "points": 0
        }
