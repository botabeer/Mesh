"""
لعبة ضد الكلمة - مع دعم Gemini AI
Created by: Abeer Aldosari © 2025
LINE Compatible - Neumorphism Soft Design
"""

from games.base_game import BaseGame
import random
import difflib
from typing import Dict, Any, Optional
import os
import logging

logger = logging.getLogger(__name__)


class OppositeGame(BaseGame):
    """لعبة ضد الكلمة مع AI Fallback"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.supports_hint = True
        self.supports_reveal = True
        
        # Gemini AI Keys
        self.gemini_keys = [
            os.getenv('GEMINI_API_KEY_1'),
            os.getenv('GEMINI_API_KEY_2'),
            os.getenv('GEMINI_API_KEY_3')
        ]
        self.current_key_index = 0
        
        # Fallback opposites
        self.default_opposites = [
            {"word": "كبير", "opposite": "صغير"},
            {"word": "طويل", "opposite": "قصير"},
            {"word": "سريع", "opposite": "بطيء"},
            {"word": "ساخن", "opposite": "بارد"},
            {"word": "جديد", "opposite": "قديم"},
            {"word": "سهل", "opposite": "صعب"},
            {"word": "قوي", "opposite": "ضعيف"},
            {"word": "ثقيل", "opposite": "خفيف"},
            {"word": "جميل", "opposite": "قبيح"},
            {"word": "سعيد", "opposite": "حزين"}
        ]
        random.shuffle(self.default_opposites)
        
        self.current_word = None
        self.last_correct_answer = None
        self.using_ai = False

    def get_gemini_client(self):
        """الحصول على Gemini Client مع التبديل التلقائي"""
        try:
            import google.generativeai as genai
            
            for i in range(len(self.gemini_keys)):
                key = self.gemini_keys[self.current_key_index]
                if key:
                    try:
                        genai.configure(api_key=key)
                        model = genai.GenerativeModel('gemini-pro')
                        self.using_ai = True
                        logger.info(f"✅ Gemini AI connected with key #{self.current_key_index + 1}")
                        return model
                    except Exception as e:
                        logger.warning(f"⚠️ Gemini key #{self.current_key_index + 1} failed: {e}")
                        self.current_key_index = (self.current_key_index + 1) % len(self.gemini_keys)
            
            logger.warning("⚠️ All Gemini keys failed, using fallback")
            self.using_ai = False
            return None
        except ImportError:
            logger.warning("⚠️ google-generativeai not installed, using fallback")
            self.using_ai = False
            return None

    def generate_opposite_with_ai(self) -> Optional[Dict[str, str]]:
        """توليد كلمة وعكسها باستخدام AI"""
        model = self.get_gemini_client()
        if not model:
            return None
        
        try:
            prompt = """أنشئ كلمة عربية وعكسها للعبة الأضداد.

المتطلبات:
- كلمة شائعة ويستخدمها الناس يومياً
- الضد واضح ومعروف

الرد بصيغة JSON فقط:
{"word": "الكلمة", "opposite": "الضد"}"""

            response = model.generate_content(prompt)
            text = response.text.strip()
            
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            import json
            data = json.loads(text.strip())
            
            if "word" in data and "opposite" in data:
                logger.info(f"✅ AI generated: {data['word']} ↔️ {data['opposite']}")
                return data
            
            return None
        except Exception as e:
            logger.error(f"❌ AI generation failed: {e}")
            return None

    def check_answer_with_ai(self, correct: str, user: str) -> bool:
        """التحقق من الإجابة باستخدام AI"""
        model = self.get_gemini_client()
        if not model:
            return False
        
        try:
            prompt = f"""هل هاتان الكلمتان متطابقتان أو متشابهتان جداً في المعنى؟

الكلمة الصحيحة: {correct}
إجابة المستخدم: {user}

أجب بـ "نعم" أو "لا" فقط."""

            response = model.generate_content(prompt)
            answer = response.text.strip().lower()
            
            return "نعم" in answer or "yes" in answer
        except Exception as e:
            logger.error(f"❌ AI check failed: {e}")
            return False

    def start_game(self) -> Any:
        self.current_question = 0
        self.game_active = True
        self.last_correct_answer = None
        return self.get_question()

    def get_progress_bar(self) -> Dict:
        colors = self.get_theme_colors()
        progress_boxes = []
        
        for i in range(self.questions_count):
            if i < self.current_question:
                bg_color = "#10B981"
            elif i == self.current_question:
                bg_color = colors["primary"]
            else:
                bg_color = "#E5E7EB"
            
            progress_boxes.append({
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "width": f"{100//self.questions_count}%",
                "height": "6px",
                "backgroundColor": bg_color,
                "cornerRadius": "3px"
            })
        
        return {
            "type": "box",
            "layout": "horizontal",
            "contents": progress_boxes,
            "spacing": "xs"
        }

    def get_question(self) -> Any:
        # محاولة استخدام AI أولاً
        q_data = self.generate_opposite_with_ai()
        
        # Fallback إذا فشل AI
        if not q_data:
            q_data = self.default_opposites[self.current_question % len(self.default_opposites)]
            self.using_ai = False
        
        self.current_word = q_data['word']
        self.current_answer = q_data['opposite']
        
        colors = self.get_theme_colors()
        progress_bar = self.get_progress_bar()
        
        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "header": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "↔️ ضد الكلمة",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#FFFFFF",
                                "flex": 0
                            },
                            {
                                "type": "text",
                                "text": "🤖 AI" if self.using_ai else "📦 DB",
                                "size": "xs",
                                "color": "#FFFFFF",
                                "align": "end"
                            }
                        ]
                    },
                    progress_bar,
                    {
                        "type": "text",
                        "text": f"السؤال {self.current_question + 1} من {self.questions_count}",
                        "size": "xs",
                        "color": "#FFFFFF",
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["primary"],
                "paddingAll": "20px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "lg",
                "contents": [
                    {
                        "type": "text",
                        "text": "ما هو ضد:",
                        "size": "sm",
                        "color": colors["text2"],
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": f"『 {self.current_word} 』",
                                "size": "xxl",
                                "color": colors["text"],
                                "align": "center",
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "15px",
                        "paddingAll": "25px"
                    },
                    {
                        "type": "text",
                        "text": "🤔 فكر في العكس...",
                        "size": "xs",
                        "color": colors["text2"],
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "20px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "text",
                                "text": "✅ الإجابة السابقة:",
                                "size": "xxs",
                                "color": colors["text2"],
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": self.last_correct_answer if self.last_correct_answer else "لا يوجد بعد",
                                "size": "xs",
                                "color": colors["text"]
                            }
                        ],
                        "backgroundColor": colors["card"],
                        "cornerRadius": "10px",
                        "paddingAll": "10px"
                    },
                    {
                        "type": "separator",
                        "color": colors["shadow1"]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "💡 لمح", "text": "لمح"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            },
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "📝 جاوب", "text": "جاوب"},
                                "style": "secondary",
                                "height": "sm",
                                "color": colors["shadow1"]
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "xs",
                        "contents": [
                            {
                                "type": "button",
                                "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                                "style": "primary",
                                "color": "#FF5555",
                                "height": "sm"
                            }
                        ]
                    },
                    {
                        "type": "separator",
                        "color": colors["shadow1"]
                    },
                    {
                        "type": "text",
                        "text": "تم إنشاؤه بواسطة عبير الدوسري © 2025",
                        "size": "xxs",
                        "color": colors["text2"],
                        "align": "center"
                    }
                ],
                "backgroundColor": colors["bg"],
                "paddingAll": "15px"
            },
            "styles": {
                "body": {"backgroundColor": colors["bg"]},
                "header": {"backgroundColor": colors["primary"]},
                "footer": {"backgroundColor": colors["bg"]}
            }
        }
        
        return self._create_flex_message("ضد الكلمة", flex_content)

    def get_hint(self) -> str:
        if not self.current_answer:
            return "💡 لا يوجد تلميح متاح"
        
        first_char = self.current_answer[0]
        length = len(self.current_answer)
        
        return f"💡 تلميح: الإجابة تبدأ بـ '{first_char}'\n🔢 عدد الحروف: {length}"

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        normalized_answer = self.normalize_text(user_answer)

        if normalized_answer == "لمح":
            hint = self.get_hint()
            return {"message": hint, "response": self._create_text_message(hint), "points": 0}

        if normalized_answer == "جاوب":
            self.last_correct_answer = self.current_answer
            reveal = f"📝 الإجابة الصحيحة: {self.current_answer}"
            next_question = self.next_question()
            
            if isinstance(next_question, dict) and next_question.get('game_over'):
                next_question['message'] = f"{reveal}\n\n{next_question.get('message','')}"
                return next_question
            
            return {'message': reveal, 'response': next_question, 'points': 0}

        normalized_correct = self.normalize_text(self.current_answer)
        is_valid = False

        if normalized_answer == normalized_correct:
            is_valid = True
        elif self.using_ai:
            is_valid = self.check_answer_with_ai(self.current_answer, user_answer)
        elif difflib.SequenceMatcher(None, normalized_answer, normalized_correct).ratio() > 0.8:
            is_valid = True

        if not is_valid:
            return {
                "message": "❌ إجابة غير صحيحة",
                "response": self._create_text_message("❌ إجابة غير صحيحة، حاول مرة أخرى"),
                "points": 0
            }

        self.last_correct_answer = self.current_answer
        points = self.add_score(user_id, display_name, 10)
        next_question = self.next_question()
        
        if isinstance(next_question, dict) and next_question.get('game_over'):
            next_question['points'] = points
            return next_question
        
        success_message = f"✅ صحيح يا {display_name}!\n📝 {self.current_word} ↔️ {self.current_answer}\n+{points} نقطة"
        
        return {
            "message": success_message,
            "response": next_question,
            "points": points
        }

    def get_game_info(self) -> Dict[str, Any]:
        return {
            "name": "لعبة ضد الكلمة",
            "emoji": "↔️",
            "description": "أوجد عكس الكلمة",
            "questions_count": self.questions_count,
            "words_count": len(self.default_opposites),
            "using_ai": self.using_ai,
            "supports_hint": self.supports_hint,
            "supports_reveal": self.supports_reveal,
            "active": self.game_active,
            "current_question": self.current_question,
            "players_count": len(self.scores)
        }
