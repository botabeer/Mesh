"""
Bot Mesh - Base Game Engine
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025
"""

from typing import Dict, Any, Optional, List
from linebot.v3.messaging import FlexMessage, FlexContainer, MessageAction
from collections import defaultdict
import re
import time


class BaseGame:
    """
    القاعدة الأساسية لجميع الألعاب
    متوافقة مع جميع شروط مشروع Bot Mesh
    """

    def __init__(self, game_name="لعبة", questions_count=5):
        self.game_name = game_name
        self.questions_count = questions_count

        self.current_question = 0
        self.current_answer = None
        self.previous_answer = None

        self.scores = defaultdict(int)
        self.answered_users = set()

        self.game_active = True
        self.start_time = time.time()

        # دعم الميزات حسب نوع اللعبة
        self.supports_hint = True
        self.supports_reveal = True
        self.supports_timer = False  # للألعاب السريعة فقط

    # ======================================================
    # أدوات مساعدة
    # ======================================================

    def normalize_text(self, text):
        if not text:
            return ""
        text = text.strip().lower()
        text = re.sub(r'^ال', '', text)
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ة', 'ه').replace('ى', 'ي')
        text = re.sub(r'[\u064B-\u065F]', '', text)
        return text

    def visual_progress(self):
        filled = "▪️" * self.current_question
        empty = "▫️" * (self.questions_count - self.current_question)
        return filled + empty

    # ======================================================
    # التحكم بالجولات
    # ======================================================

    def start(self):
        self.current_question = 1
        self.game_active = True
        self.answered_users.clear()
        return self.get_question()

    def next_question(self):
        self.current_question += 1
        self.answered_users.clear()

        if self.current_question > self.questions_count:
            return self.end_game()

        return self.get_question()

    # ======================================================
    # التحقق من الإجابة
    # ======================================================

    def check_answer(self, user_answer, user_id, display_name):

        if not self.game_active:
            return None

        if user_id in self.answered_users:
            return None

        normalized_user = self.normalize_text(user_answer)
        normalized_correct = self.normalize_text(self.current_answer)

        if normalized_user == normalized_correct:
            self.answered_users.add(user_id)
            self.scores[display_name] += 1

            self.previous_answer = self.current_answer

            return {
                "correct": True,
                "next_question": self.next_question()
            }

        return {
            "correct": False,
            "message": "إجابة غير صحيحة"
        }

    # ======================================================
    # اللمح والجواب
    # ======================================================

    def get_hint(self):
        if not self.supports_hint or not self.current_answer:
            return None

        answer = str(self.current_answer)
        first_letter = answer[0]
        length = len(answer)
        return f"أول حرف: {first_letter}\nعدد الحروف: {length}"

    def reveal_answer(self):
        if not self.supports_reveal or not self.current_answer:
            return None
        return f"الجواب الصحيح: {self.current_answer}"

    # ======================================================
    # إنهاء اللعبة
    # ======================================================

    def end_game(self):
        self.game_active = False

        if not self.scores:
            winner_name = "لا يوجد"
            winner_score = 0
        else:
            winner_name = max(self.scores, key=self.scores.get)
            winner_score = self.scores[winner_name]

        flex = self.build_game_over_flex(winner_name, winner_score)

        return {
            "game_over": True,
            "winner": winner_name,
            "points": winner_score,
            "response": flex
        }

    # ======================================================
    # بناء واجهة السؤال
    # ======================================================

    def build_question_flex(self, question_text):
        contents = []

        if self.previous_answer:
            contents.append({
                "type": "text",
                "text": f"الجواب السابق: {self.previous_answer}",
                "size": "sm",
                "color": "#6B7280"
            })

        contents.append({
            "type": "text",
            "text": f"الجولة {self.current_question} من {self.questions_count}",
            "weight": "bold"
        })

        contents.append({
            "type": "text",
            "text": self.visual_progress()
        })

        contents.append({
            "type": "separator"
        })

        contents.append({
            "type": "text",
            "text": question_text,
            "wrap": True,
            "size": "lg"
        })

        buttons = []

        if self.supports_hint:
            buttons.append({
                "type": "button",
                "action": {"type": "message", "label": "لمح", "text": "لمح"},
                "style": "secondary"
            })

        if self.supports_reveal:
            buttons.append({
                "type": "button",
                "action": {"type": "message", "label": "جاوب", "text": "جاوب"},
                "style": "secondary"
            })

        buttons.append({
            "type": "button",
            "action": {"type": "message", "label": "إيقاف", "text": "إيقاف"},
            "style": "primary"
        })

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": contents
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": buttons
            }
        }

        return FlexMessage(
            alt_text=f"سؤال {self.current_question}",
            contents=FlexContainer.from_dict(bubble)
        )

    # ======================================================
    # واجهة نهاية اللعبة
    # ======================================================

    def build_game_over_flex(self, winner_name, winner_score):

        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "انتهت اللعبة",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "separator"
                    },
                    {
                        "type": "text",
                        "text": f"الفائز: {winner_name}",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": f"النقاط: {winner_score}",
                        "align": "center"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "إعادة",
                            "text": f"لعبة {self.game_name}"
                        },
                        "style": "primary"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "بداية",
                            "text": "بداية"
                        },
                        "style": "secondary"
                    }
                ]
            }
        }

        return FlexMessage(
            alt_text="انتهاء اللعبة",
            contents=FlexContainer.from_dict(bubble)
        )
