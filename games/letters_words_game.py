import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class LettersWordsGame:
    def __init__(self, line_bot_api, use_ai=False, get_api_key=None, switch_key=None):
        self.line_bot_api = line_bot_api
        self.use_ai = use_ai
        self.get_api_key = get_api_key
        self.switch_key = switch_key
        self.current_letters = None
        self.valid_words = []
        self.found_words = set()
        self.hint_used = False
        
        # مجموعات حروف
        self.letter_sets = [
            "كتابةر",  # كتاب، تاب، كتب، راب
            "مدرسةه",  # مدرسة، درس، مدر
            "طعامشر",  # طعام، عام، شام
            "سلامةع",  # سلامة، علم، سلم
            "حياةرف",  # حياة، يار، حار
            "بيتمنز"   # بيت، من، زمن
        ]
    
    def start_game(self):
        """بدء لعبة جديدة"""
        self.current_letters = random.choice(self.letter_sets)
        self.found_words = set()
        self.hint_used = False
        
        if self.use_ai and self.get_api_key:
            self._generate_valid_words_ai()
        
        text = f"🔤 كون 3 كلمات من الحروف\n\n{' '.join(self.current_letters)}\n\n━━━━━━━━━━━━━━\nاكتب كلمة واحدة في كل مرة"
        return TextSendMessage(text=text)
    
    def _generate_valid_words_ai(self):
        """توليد كلمات صحيحة باستخدام AI"""
        try:
            import google.generativeai as genai
            
            api_key = self.get_api_key()
            if not api_key:
                return
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""من الحروف التالية: {self.current_letters}
            
أعطني 5 كلمات عربية صحيحة يمكن تكوينها من هذه الحروف.

اكتب كل كلمة في سطر منفصل، بدون أرقام أو رموز."""
            
            response = model.generate_content(prompt)
            words = response.text.strip().split('\n')
            self.valid_words = [normalize_text(w.strip()) for w in words if w.strip()]
                
        except Exception as e:
            print(f"خطأ في AI: {e}")
            if self.switch_key:
                self.switch_key()
    
    def check_answer(self, answer, user_id, display_name):
        """فحص الإجابة"""
        if not self.current_letters:
            return None
        
        normalized_answer = normalize_text(answer)
        
        # تحقق من أن الكلمة لم تستخدم من قبل
        if normalized_answer in self.found_words:
            return None
        
        # تحقق من أن جميع الحروف موجودة
        answer_letters = list(normalized_answer)
        available_letters = list(normalize_text(self.current_letters))
        
        for letter in answer_letters:
            if letter not in available_letters:
                return None
            available_letters.remove(letter)
        
        # إذا كان AI متوفر، تحقق من صحة الكلمة
        if self.use_ai and self.get_api_key:
            is_valid = self._verify_word_with_ai(answer)
            if not is_valid:
                return None
        
        # قبول الكلمة
        self.found_words.add(normalized_answer)
        
        # حساب النقاط
        if len(self.found_words) >= 3:
            # أكمل اللاعب 3 كلمات
            points = 15
            if self.hint_used:
                points = 10
            
            new_question = self.start_game()
            message = f"✓ رائع يا {display_name}!\n\nأكملت 3 كلمات\n+{points} نقطة\n\n{new_question.text}"
            
            return {
                'points': points,
                'won': True,
                'message': message,
                'response': TextSendMessage(text=message),
                'game_over': False
            }
        else:
            # لا يزال هناك كلمات
            remaining = 3 - len(self.found_words)
            message = f"✓ كلمة صحيحة: {answer}\n\nباقي {remaining} كلمات"
            
            return {
                'points': 0,
                'won': False,
                'message': message,
                'response': TextSendMessage(text=message),
                'game_over': False
            }
    
    def _verify_word_with_ai(self, word):
        """التحقق من صحة الكلمة باستخدام AI"""
        try:
            import google.generativeai as genai
            
            api_key = self.get_api_key()
            if not api_key:
                return True
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""هل '{word}' كلمة عربية صحيحة؟
            
أجب فقط بـ 'نعم' أو 'لا'."""
            
            response = model.generate_content(prompt)
            result = normalize_text(response.text.strip())
            
            return 'نعم' in result or 'yes' in result
                
        except Exception as e:
            print(f"خطأ في AI verification: {e}")
            return True
    
    def get_hint(self):
        """تلميح"""
        if not self.current_letters:
            return "لا يوجد سؤال حالي"
        
        self.hint_used = True
        
        # إعطاء مثال على كلمة
        if self.valid_words:
            hint_word = random.choice(self.valid_words)
            return f"💡 التلميح\n\nمثال: {hint_word}\n\n⚠️ سيتم خصم نقاط"
        
        return f"💡 حاول تكوين كلمات من: {self.current_letters}"
    
    def reveal_answer(self):
        """كشف الإجابة"""
        if not self.current_letters:
            return "لا يوجد سؤال حالي"
        
        examples = ", ".join(self.valid_words[:3]) if self.valid_words else "غير متوفر"
        self.current_letters = None
        self.found_words = set()
        
        return f"أمثلة على كلمات:\n{examples}"
