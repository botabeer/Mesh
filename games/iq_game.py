import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class IQGame:
    def __init__(self, line_bot_api, use_ai=False, get_api_key=None, switch_key=None):
        self.line_bot_api = line_bot_api
        self.use_ai = use_ai
        self.get_api_key = get_api_key
        self.switch_key = switch_key
        self.current_question = None
        self.current_answer = None
        self.hint_used = False
        
        self.questions = [
            {"q": "ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عين؟", "a": "السحاب"},
            {"q": "له رأس ولا عين له، وله عين ولا رأس لها. ما هو؟", "a": "دبوس"},
            {"q": "ما الشيء الذي كلما أخذت منه كبر؟", "a": "الحفرة"},
            {"q": "شيء موجود في السماء إذا أضفت إليه حرفاً أصبح في الأرض؟", "a": "نجم"},
            {"q": "ما هو الشيء الذي يكتب ولا يقرأ؟", "a": "القلم"},
            {"q": "له عين ولا يرى، فما هو؟", "a": "الإبرة"},
            {"q": "ما الشيء الذي تأكل منه مع أنه لا يؤكل؟", "a": "الصحن"},
            {"q": "كلمة تتكون من 8 حروف ولكنها تجمع كل الحروف؟", "a": "ابجدية"},
            {"q": "ما هو الشيء الذي له أسنان ولا يعض؟", "a": "المشط"},
            {"q": "ما هو الشيء الذي يوجد في وسط باريس؟", "a": "حرف ر"}
        ]
    
    def start_game(self):
        """بدء لعبة جديدة"""
        if self.use_ai and self.get_api_key:
            return self._generate_ai_question()
        else:
            return self._generate_manual_question()
    
    def _generate_manual_question(self):
        """توليد سؤال يدوي"""
        qa = random.choice(self.questions)
        self.current_question = qa['q']
        self.current_answer = qa['a']
        self.hint_used = False
        
        text = f"🧠 سؤال ذكاء\n\n{self.current_question}\n\n━━━━━━━━━━━━━━\nما هي الإجابة؟"
        return TextSendMessage(text=text)
    
    def _generate_ai_question(self):
        """توليد سؤال بالذكاء الاصطناعي"""
        try:
            import google.generativeai as genai
            
            api_key = self.get_api_key()
            if not api_key:
                return self._generate_manual_question()
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = """أعطني لغز ذكاء عربي مع إجابته.

الصيغة المطلوبة:
QUESTION: [اللغز]
ANSWER: [الإجابة]

مثال:
QUESTION: ما هو الشيء الذي يمشي بلا أرجل؟
ANSWER: السحاب"""
            
            response = model.generate_content(prompt)
            result = response.text.strip()
            
            question_line = [l for l in result.split('\n') if 'QUESTION:' in l]
            answer_line = [l for l in result.split('\n') if 'ANSWER:' in l]
            
            if question_line and answer_line:
                self.current_question = question_line[0].replace('QUESTION:', '').strip()
                self.current_answer = answer_line[0].replace('ANSWER:', '').strip()
                self.hint_used = False
                
                text = f"🧠 سؤال ذكاء\n\n{self.current_question}\n\n━━━━━━━━━━━━━━\nما هي الإجابة؟"
                return TextSendMessage(text=text)
            else:
                return self._generate_manual_question()
                
        except Exception as e:
            print(f"خطأ في AI: {e}")
            if self.switch_key:
                self.switch_key()
            return self._generate_manual_question()
    
    def check_answer(self, answer, user_id, display_name):
        """فحص الإجابة"""
        if not self.current_answer:
            return None
        
        normalized_answer = normalize_text(answer)
        normalized_correct = normalize_text(self.current_answer)
        
        if normalized_answer in normalized_correct or normalized_correct in normalized_answer:
            points = 10
            if self.hint_used:
                points = 5
            
            new_question = self.start_game()
            message = f"✓ إجابة صحيحة يا {display_name}\n\nالجواب: {self.current_answer}\n+{points} نقطة\n\n{new_question.text}"
            
            return {
                'points': points,
                'won': True,
                'message': message,
                'response': TextSendMessage(text=message),
                'game_over': False
            }
        
        return None
    
    def get_hint(self):
        """تلميح"""
        if not self.current_answer:
            return "لا يوجد سؤال حالي"
        
        self.hint_used = True
        first_letter = self.current_answer[0]
        letter_count = len(self.current_answer)
        
        return f"💡 التلميح\n\nأول حرف: {first_letter}\nعدد الحروف: {letter_count}\n\n⚠️ سيتم خصم 5 نقاط"
    
    def reveal_answer(self):
        """كشف الإجابة"""
        if not self.current_answer:
            return "لا يوجد سؤال حالي"
        
        answer = self.current_answer
        self.current_answer = None
        
        return f"الإجابة الصحيحة:\n{answer}"
