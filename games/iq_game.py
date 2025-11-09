import random
import re
from linebot.models import TextSendMessage
import google.generativeai as genai

class IQGame:
    def __init__(self, line_bot_api, use_ai=False, get_api_key=None, switch_key=None):
        self.line_bot_api = line_bot_api
        self.use_ai = use_ai
        self.get_api_key = get_api_key
        self.switch_key = switch_key
        self.current_question_text = None
        self.correct_answer = None
        self.model = None
        self.current_question = 1
        self.max_questions = 10
        self.players_scores = {}
        self.hint_used = False
        
        # تهيئة AI
        if self.use_ai and self.get_api_key:
            try:
                api_key = self.get_api_key()
                if api_key:
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            except Exception as e:
                print(f"AI initialization error: {e}")
                self.use_ai = False
        
        # بنك أسئلة كبير
        self.questions = [
            {"question": "ما هو عدد أركان الإسلام؟", "answer": "5", "hint": "رقم أقل من 10"},
            {"question": "ما هو ناتج 15 × 4؟", "answer": "60", "hint": "رقم بين 50 و 70"},
            {"question": "كم عدد أيام السنة الهجرية؟", "answer": "354", "hint": "رقم يبدأ بـ 3"},
            {"question": "ما هي عاصمة المملكة العربية السعودية؟", "answer": "الرياض", "hint": "مدينة في وسط السعودية"},
            {"question": "من هو أول خليفة راشدي؟", "answer": "أبو بكر الصديق", "hint": "صاحب النبي في الغار"},
            {"question": "كم سورة في القرآن الكريم؟", "answer": "114", "hint": "رقم أكبر من 100"},
            {"question": "ما هو أطول نهر في العالم؟", "answer": "النيل", "hint": "نهر في أفريقيا"},
            {"question": "كم عدد ألوان قوس قزح؟", "answer": "7", "hint": "رقم أقل من 10"},
            {"question": "ما هو أكبر كوكب في المجموعة الشمسية؟", "answer": "المشتري", "hint": "كوكب غازي عملاق"},
            {"question": "كم عدد أحرف الأبجدية العربية؟", "answer": "28", "hint": "رقم بين 25 و 30"},
            {"question": "ما هي عاصمة مصر؟", "answer": "القاهرة", "hint": "مدينة كبيرة في مصر"},
            {"question": "كم عدد قارات العالم؟", "answer": "7", "hint": "رقم أقل من 10"},
            {"question": "ما هو أسرع حيوان بري؟", "answer": "الفهد", "hint": "حيوان مفترس سريع"},
            {"question": "كم عدد أيام الأسبوع؟", "answer": "7", "hint": "رقم أقل من 10"},
            {"question": "ما اسم أطول سورة في القرآن؟", "answer": "البقرة", "hint": "سورة في بداية المصحف"},
            {"question": "كم عدد أشهر السنة الميلادية؟", "answer": "12", "hint": "رقم بين 10 و 15"},
            {"question": "ما هي عاصمة فرنسا؟", "answer": "باريس", "hint": "مدينة الأنوار"},
            {"question": "كم عدد أسنان الإنسان البالغ؟", "answer": "32", "hint": "رقم بين 30 و 35"},
            {"question": "ما هو أكبر محيط في العالم؟", "answer": "المحيط الهادئ", "hint": "محيط بين آسيا وأمريكا"},
            {"question": "من هو النبي الذي ابتلعه الحوت؟", "answer": "يونس", "hint": "نبي ورد ذكره في سورة تحمل اسمه"}
        ]
    
    def normalize_text(self, text):
        """تطبيع النص للمقارنة"""
        text = text.strip().lower()
        text = re.sub(r'^ال', '', text)
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ة', 'ه')
        text = text.replace('ى', 'ي')
        text = re.sub(r'[\u064B-\u065F]', '', text)
        return text
    
    def generate_ai_question(self):
        """توليد سؤال باستخدام AI"""
        if not self.model:
            return None
        
        try:
            prompt = """أنشئ سؤال ذكاء أو ثقافة عامة باللغة العربية.
            
            الرد يجب أن يكون بالصيغة التالية فقط:
            السؤال: [السؤال هنا]
            الإجابة: [الإجابة المختصرة]
            
            السؤال يجب أن يكون واضح ومباشر، والإجابة مختصرة."""
            
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            lines = text.split('\n')
            question = None
            answer = None
            
            for line in lines:
                if 'السؤال:' in line or 'سؤال:' in line:
                    question = line.split(':', 1)[1].strip()
                elif 'الإجابة:' in line or 'إجابة:' in line or 'الجواب:' in line:
                    answer = line.split(':', 1)[1].strip()
            
            if question and answer:
                return {"question": question, "answer": answer, "hint": "لا يوجد تلميح"}
            
        except Exception as e:
            print(f"AI question generation error: {e}")
            if self.switch_key and self.switch_key():
                try:
                    api_key = self.get_api_key()
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    return self.generate_ai_question()
                except:
                    pass
        
        return None
    
    def start_game(self):
        self.current_question = 1
        self.players_scores = {}
        return self.next_question()
    
    def next_question(self):
        """الانتقال للسؤال التالي"""
        if self.current_question > self.max_questions:
            return self.end_game()
        
        # محاولة توليد سؤال بالذكاء الاصطناعي
        question_data = None
        if self.use_ai:
            question_data = self.generate_ai_question()
        
        if not question_data:
            question_data = random.choice(self.questions)
        
        self.current_question_text = question_data["question"]
        self.correct_answer = question_data["answer"].strip().lower()
        self.current_hint = question_data.get("hint", "لا يوجد تلميح")
        self.hint_used = False
        
        return TextSendMessage(
            text=f"السؤال {self.current_question}/{self.max_questions}\n\n{self.current_question_text}"
        )
    
    def get_hint(self):
        """الحصول على تلميح"""
        if self.hint_used:
            return TextSendMessage(text="تم استخدام التلميح مسبقاً")
        
        self.hint_used = True
        return TextSendMessage(text=f"تلميح:\n{self.current_hint}")
    
    def show_answer(self):
        """عرض الإجابة الصحيحة"""
        msg = f"الإجابة الصحيحة: {self.correct_answer}"
        
        self.current_question += 1
        
        if self.current_question <= self.max_questions:
            return self.next_question()
        else:
            return self.end_game()
    
    def end_game(self):
        """إنهاء اللعبة وعرض النتائج"""
        if not self.players_scores:
            return TextSendMessage(text="انتهت اللعبة\nلم يشارك أحد")
        
        sorted_players = sorted(self.players_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        msg = "النتائج النهائية\n\n"
        for i, (name, data) in enumerate(sorted_players[:5], 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"  {i}."
            msg += f"{emoji} {name}: {data['score']} نقطة\n"
        
        winner = sorted_players[0]
        msg += f"\nالفائز: {winner[0]}"
        
        return TextSendMessage(text=msg)
    
    def check_answer_with_ai(self, answer):
        """التحقق من الإجابة باستخدام AI"""
        if not self.model:
            return False
        
        try:
            prompt = f"""هل الإجابة '{answer}' صحيحة للسؤال '{self.current_question_text}'؟
            الإجابة الصحيحة هي: {self.correct_answer}
            
            أجب فقط بـ 'نعم' أو 'لا'"""
            
            response = self.model.generate_content(prompt)
            ai_result = response.text.strip().lower()
            
            return 'نعم' in ai_result or 'yes' in ai_result
        except Exception as e:
            print(f"AI check error: {e}")
            if self.switch_key:
                self.switch_key()
            return False
    
    def check_answer(self, answer, user_id, display_name):
        if not self.current_question_text:
            return None
        
        # التحقق من أوامر التلميح والإجابة
        if answer == 'لمح':
            return {
                'message': '',
                'points': 0,
                'game_over': False,
                'response': self.get_hint()
            }
        
        if answer == 'جاوب':
            return {
                'message': '',
                'points': 0,
                'game_over': self.current_question > self.max_questions,
                'response': self.show_answer()
            }
        
        user_answer = self.normalize_text(answer)
        correct_answer = self.normalize_text(self.correct_answer)
        
        # التحقق باستخدام AI
        is_correct = False
        if self.use_ai:
            is_correct = self.check_answer_with_ai(answer)
        
        # التحقق التقليدي
        if not is_correct:
            if user_answer == correct_answer or correct_answer in user_answer or user_answer in correct_answer:
                is_correct = True
        
        if is_correct:
            points = 10 if not self.hint_used else 5
            
            if display_name not in self.players_scores:
                self.players_scores[display_name] = {'score': 0}
            self.players_scores[display_name]['score'] += points
            
            msg = f"صحيح يا {display_name}\n+{points} نقطة"
            
            self.current_question += 1
            
            if self.current_question <= self.max_questions:
                next_q = self.next_question()
                return {
                    'message': msg,
                    'points': points,
                    'won': True,
                    'game_over': False,
                    'response': TextSendMessage(text=f"{msg}\n\n{next_q.text}")
                }
            else:
                end_msg = self.end_game()
                return {
                    'message': msg,
                    'points': points,
                    'won': True,
                    'game_over': True,
                    'response': TextSendMessage(text=f"{msg}\n\n{end_msg.text}")
                }
        
        return None
