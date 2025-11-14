import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class HumanAnimalPlantGame:
    def __init__(self, line_bot_api, use_ai=False, get_api_key=None, switch_key=None):
        self.line_bot_api = line_bot_api
        self.use_ai = use_ai
        self.get_api_key = get_api_key
        self.switch_key = switch_key
        self.current_letter = None
        self.current_category = None
        self.current_answer = None
        self.hint_used = False
        
        self.letters = list("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")
        self.categories = {
            "إنسان": ["أحمد", "محمد", "فاطمة", "عائشة", "علي", "حسن", "سارة", "مريم"],
            "حيوان": ["أسد", "فيل", "قط", "كلب", "حصان", "جمل", "ثعلب", "دب"],
            "نبات": ["ورد", "نخيل", "تفاح", "موز", "برتقال", "زيتون", "نعناع"],
            "جماد": ["كرسي", "طاولة", "قلم", "كتاب", "باب", "نافذة", "هاتف"],
            "بلاد": ["مصر", "سعودية", "عراق", "سوريا", "لبنان", "أردن", "قطر"]
        }
    
    def start_game(self):
        """بدء لعبة جديدة"""
        self.current_letter = random.choice(self.letters)
        self.current_category = random.choice(list(self.categories.keys()))
        self.current_answer = None
        self.hint_used = False
        
        if self.use_ai and self.get_api_key:
            self._get_ai_answer()
        
        text = f"🎯 {self.current_category} بحرف {self.current_letter}\n\n━━━━━━━━━━━━━━\nاكتب اسم {self.current_category} يبدأ بحرف {self.current_letter}"
        return TextSendMessage(text=text)
    
    def _get_ai_answer(self):
        """الحصول على إجابة من AI للتحقق"""
        try:
            import google.generativeai as genai
            
            api_key = self.get_api_key()
            if not api_key:
                return
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""أعطني مثال واحد فقط ل{self.current_category} يبدأ بحرف {self.current_letter}. 
            
اكتب الاسم فقط بدون أي كلام إضافي."""
            
            response = model.generate_content(prompt)
            self.current_answer = response.text.strip()
                
        except Exception as e:
            print(f"خطأ في AI: {e}")
            if self.switch_key:
                self.switch_key()
    
    def check_answer(self, answer, user_id, display_name):
        """فحص الإجابة"""
        if not self.current_letter or not self.current_category:
            return None
        
        normalized_answer = normalize_text(answer)
        normalized_letter = normalize_text(self.current_letter)
        
        # التحقق من أن الإجابة تبدأ بالحرف الصحيح
        if not normalized_answer.startswith(normalized_letter):
            return None
        
        # إذا كان لدينا AI، نتحقق من صحة الإجابة
        if self.use_ai and self.get_api_key:
            is_valid = self._verify_answer_with_ai(answer)
            if not is_valid:
                return None
        
        # قبول الإجابة
        points = 10
        if self.hint_used:
            points = 5
        
        new_question = self.start_game()
        message = f"✓ إجابة صحيحة يا {display_name}\n\n{answer}\n+{points} نقطة\n\n{new_question.text}"
        
        return {
            'points': points,
            'won': True,
            'message': message,
            'response': TextSendMessage(text=message),
            'game_over': False
        }
    
    def _verify_answer_with_ai(self, answer):
        """التحقق من صحة الإجابة باستخدام AI"""
        try:
            import google.generativeai as genai
            
            api_key = self.get_api_key()
            if not api_key:
                return True  # قبول الإجابة إذا لم يتوفر AI
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""هل '{answer}' هو {self.current_category}؟
            
أجب فقط بـ 'نعم' أو 'لا' بدون أي تفسير."""
            
            response = model.generate_content(prompt)
            result = normalize_text(response.text.strip())
            
            return 'نعم' in result or 'yes' in result
                
        except Exception as e:
            print(f"خطأ في AI verification: {e}")
            return True  # قبول الإجابة عند حدوث خطأ
    
    def get_hint(self):
        """تلميح"""
        if not self.current_letter or not self.current_category:
            return "لا يوجد سؤال حالي"
        
        self.hint_used = True
        
        # البحث عن مثال من القاعدة
        examples = []
        if self.current_category in self.categories:
            examples = [ex for ex in self.categories[self.current_category] 
                       if normalize_text(ex).startswith(normalize_text(self.current_letter))]
        
        if examples:
            example = random.choice(examples)
            return f"💡 التلميح\n\nمثال: {example}\n\n⚠️ سيتم خصم 5 نقاط"
        
        return f"💡 فكر في {self.current_category} مشهور يبدأ بحرف {self.current_letter}"
    
    def reveal_answer(self):
        """كشف الإجابة"""
        if not self.current_letter or not self.current_category:
            return "لا يوجد سؤال حالي"
        
        # البحث عن مثال
        example = "غير متوفر"
        if self.current_category in self.categories:
            examples = [ex for ex in self.categories[self.current_category] 
                       if normalize_text(ex).startswith(normalize_text(self.current_letter))]
            if examples:
                example = random.choice(examples)
            elif self.current_answer:
                example = self.current_answer
        
        self.current_letter = None
        self.current_category = None
        
        return f"مثال صحيح:\n{example}"
