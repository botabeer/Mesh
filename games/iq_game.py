import random
from linebot.models import TextSendMessage
import json
import re

class IQGame:
    def __init__(self, line_bot_api, use_ai=False, get_api_key=None, switch_key=None):
        self.line_bot_api = line_bot_api
        self.use_ai = use_ai
        self.get_api_key = get_api_key
        self.switch_key = switch_key
        
        # أسئلة احتياطية
        self.backup_questions = [
            {"question": "ما هو الشيء الذي يحتوي على مفاتيح ولكن لا يوجد به أقفال؟",
             "answer": "لوحة المفاتيح", "alternatives": ["الكيبورد"], "hint": "تستخدم في الحاسوب"},
            {"question": "ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟",
             "answer": "السحابة", "alternatives": [], "hint": "يطفو في السماء ويسقط مطرًا"},
            {"question": "شيء له فروع وأوراق ولكنه لا لحاء له، فما هو؟",
             "answer": "الكتاب", "alternatives": [], "hint": "تقرأه لتتعلم"},
            {"question": "شيء له أربع أرجل ولكنه لا يمشي؟",
             "answer": "الطاولة", "alternatives": [], "hint": "يوضع عليه الأشياء"},
            {"question": "شهر إذا حذفنا أول حرف منه أصبح اسم فاكهة، فما هو؟",
             "answer": "تموز", "alternatives": [], "hint": "حذف حرف التاء يصبح موز"},
            {"question": "ما هو الشيء الذي له رقبة ولا رأس؟",
             "answer": "الزجاجة", "alternatives": [], "hint": "يُستخدم لوضع السوائل"},
            {"question": "شيء لا بداية له ولا نهاية؟",
             "answer": "الدائرة", "alternatives": [], "hint": "شكل هندسي مستمر"},
            {"question": "شيء يمكنه ملء الغرفة ولكنه لا يشغل أي مساحة؟",
             "answer": "الضوء", "alternatives": [], "hint": "يضيء المكان"},
            {"question": "شيء له أسنان لكنه لا يأكل؟",
             "answer": "المشط", "alternatives": [], "hint": "يستخدم لتصفيف الشعر"},
            {"question": "ما هو الشيء الذي يزيد ولا ينقص أبدًا؟",
             "answer": "العمر", "alternatives": [], "hint": "مرتبط بالوقت منذ الولادة"},
            {"question": "ما هو الشيء الذي ينام وهو يرتدي حذائه؟",
             "answer": "الحصان", "alternatives": [], "hint": "يستخدم في الركوب والعمل"},
            {"question": "ما هو الشيء الذي لا يمشي إلا بالضرب؟",
             "answer": "المسمار", "alternatives": [], "hint": "يُثبت الأشياء في الحائط"},
            {"question": "حاصل ضرب ثلاثة أعداد يساوي حاصل جمعها، ما هي؟",
             "answer": "1، 2، 3", "alternatives": [], "hint": "أعداد صحيحة صغيرة"},
            {"question": "ما هو الشيء الذي له عين ولا يرى؟",
             "answer": "الإبرة", "alternatives": [], "hint": "تستخدم في الخياطة"},
            {"question": "أخت خالتك وليست خالتك؟",
             "answer": "أمك", "alternatives": ["امك","والدة"], "hint": "أقرب إنسان لك"},
            {"question": "ما هو الشيء الذي يجري ولا يمشي؟",
             "answer": "الماء", "alternatives": ["نهر"], "hint": "سائل ضروري للحياة"},
            {"question": "من هو الذي يكتب ولا يقرأ؟",
             "answer": "القلم", "alternatives": [], "hint": "أداة للكتابة"},
            {"question": "ما هو الشيء الذي يأكل ولا يشبع؟",
             "answer": "النار", "alternatives": [], "hint": "تحرق كل شيء"},
            {"question": "ما هو الشيء الذي له أسنان ولكن لا يعض؟",
             "answer": "المشط", "alternatives": [], "hint": "يساعد في ترتيب الشعر"},
            {"question": "شيء يمشي ويقف ولا يتحرك من مكانه؟",
             "answer": "الساعة", "alternatives": [], "hint": "تعطي الوقت"},
            {"question": "ما هو الشيء الذي تراه في الليل والنهار ولكنه لا يتحرك؟",
             "answer": "القمر", "alternatives": [], "hint": "يدور حول الأرض"},
            {"question": "شيء تملكه أنت ولكن يستخدمه الآخرون أكثر منك، ما هو؟",
             "answer": "اسمك", "alternatives": [], "hint": "هو هويتك"},
            {"question": "شيء تملكه منذ ولادتك ولكنه يزداد طولاً كل يوم؟",
             "answer": "العمر", "alternatives": [], "hint": "مرتبط بالوقت"},
            {"question": "ما هو الشيء الذي له قلب ولكنه لا ينبض؟",
             "answer": "الخس", "alternatives": [], "hint": "نوع من الخضار"},
            {"question": "شيء كلما أخذت منه كبر، ما هو؟",
             "answer": "الحفرة", "alternatives": [], "hint": "تحفره الأرض"},
            {"question": "ما هو الشيء الذي يملك مدخلًا ولكن لا يملك مخرج؟",
             "answer": "الإبرة", "alternatives": [], "hint": "لخياطة الملابس"},
            {"question": "ما هو الشيء الذي له مدينة ولكنه لا يعيش فيها؟",
             "answer": "الخريطة", "alternatives": [], "hint": "ترسم لتعرف الأماكن"},
            {"question": "ما هو الشيء الذي يستطيع الكتابة دون حبر؟",
             "answer": "القلم الرصاص", "alternatives": [], "hint": "يكتب ويُمحى"},
            {"question": "ما هو الشيء الذي يرى كل شيء ولكن لا يستطيع الكلام؟",
             "answer": "المرآة", "alternatives": [], "hint": "تعكس ما أمامها"},
            {"question": "ما هو الشيء الذي يسمع بلا أذن ويتحدث بلا لسان؟",
             "answer": "الصدى", "alternatives": [], "hint": "يتكرر الصوت"},
            {"question": "ما هو الشيء الذي يمتلئ بالماء ولكنه لا يبتل؟",
             "answer": "الإسفنج", "alternatives": [], "hint": "يمتص الماء"},
            {"question": "ما هو الشيء الذي يوجد في كل بيت ويُستخدم للطعام؟",
             "answer": "الملعقة", "alternatives": [], "hint": "لتناول الطعام"},
            {"question": "ما هو الشيء الذي يمشي بلا قدمين ويطير بلا أجنحة؟",
             "answer": "الزمن", "alternatives": [], "hint": "يمر بسرعة"},
            {"question": "شيء يُكسر بدون أن يُلمس، ما هو؟",
             "answer": "الوعد", "alternatives": [], "hint": "الوفاء مهم"},
            {"question": "ما هو الشيء الذي له وجه ولا يُرى إلا عند النظر إليه؟",
             "answer": "الساعة", "alternatives": [], "hint": "تخبر الوقت"},
            {"question": "شيء موجود في كل مكان ولا يُرى، ما هو؟",
             "answer": "الهواء", "alternatives": [], "hint": "ضروري للتنفس"},
            {"question": "ما هو الشيء الذي يُشاهد ولا يُسمع؟",
             "answer": "الصورة", "alternatives": [], "hint": "يمكن تعليقها على الحائط"},
            {"question": "شيء يُسافر حول العالم ويبقى في الزاوية؟",
             "answer": "الطابع البريدي", "alternatives": [], "hint": "يوضع على الرسائل"},
            {"question": "ما هو الشيء الذي يُفتح ولا يُغلق؟",
             "answer": "العين", "alternatives": [], "hint": "للنظر"},
            {"question": "ما هو الشيء الذي له أوراق ولكنه لا يُزرع؟",
             "answer": "الكتاب", "alternatives": [], "hint": "تقرأه لتتعلم"},
        ]
        
        self.current_question = None
        self.current_answer = None
        self.current_alternatives = []
        self.current_hint = None

    def _generate_ai_question(self):
        """توليد سؤال بالذكاء الاصطناعي"""
        if not self.use_ai:
            return None
        
        try:
            import google.generativeai as genai
            api_key = self.get_api_key()
            if not api_key:
                return None
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = """أنت منشئ ألغاز ذكية وممتعة باللغة العربية.
أنشئ لغزاً واحداً بصيغة JSON كما يلي:
{"question": "نص السؤال", "answer": "الإجابة", "alternatives": ["بديل1", "بديل2"], "hint": "تلميح"}
            """
            
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                question_data = json.loads(json_match.group())
                return question_data
            
            return None
            
        except Exception as e:
            print(f"خطأ في توليد السؤال بالـ AI: {e}")
            if self.switch_key and self.switch_key():
                return self._generate_ai_question()
            return None

    def start_game(self):
        """بدء اللعبة"""
        question_data = self._generate_ai_question()
        if not question_data:
            question_data = random.choice(self.backup_questions)
        
        self.current_question = question_data["question"]
        self.current_answer = question_data["answer"]
        self.current_alternatives = question_data.get("alternatives", [])
        self.current_hint = question_data.get("hint", "فكر جيداً في السؤال")
        
        return TextSendMessage(
            text=f"لعبة الذكاء\n\n{self.current_question}\n\n💡 لمح: تلميح\n✅ جاوب: الإجابة"
        )
    
    def get_hint(self):
        return self.current_hint or "لا يوجد تلميح متاح"
    
    def get_answer(self):
        return self.current_answer or "لا يوجد سؤال حالي"
    
    def check_answer(self, answer, user_id, display_name):
        if not self.current_answer:
            return None
        
        normalized_answer = answer.strip().lower()
        normalized_answer = normalized_answer.replace('أ','ا').replace('إ','ا').replace('آ','ا')
        normalized_answer = normalized_answer.replace('ة','ه').replace('ى','ي').replace('ال','')
        
        correct_answer = self.current_answer.lower()
        correct_answer = correct_answer.replace('أ','ا').replace('إ','ا').replace('آ','ا')
        correct_answer = correct_answer.replace('ة','ه').replace('ى','ي').replace('ال','')
        
        normalized_alternatives = []
        for alt in self.current_alternatives:
            norm_alt = alt.lower().replace('أ','ا').replace('إ','ا').replace('آ','ا')
            norm_alt = norm_alt.replace('ة','ه').replace('ى','ي').replace('ال','')
            normalized_alternatives.append(norm_alt)
        
        if normalized_answer == correct_answer or normalized_answer in normalized_alternatives:
            points = 10
            question_data = self._generate_ai_question()
            if not question_data:
                question_data = random.choice(self.backup_questions)
            
            self.current_question = question_data["question"]
            self.current_answer = question_data["answer"]
            self.current_alternatives = question_data.get("alternatives", [])
            self.current_hint = question_data.get("hint", "فكر جيداً في السؤال")
            
            return {
                'points': points,
                'won': True,
                'response': TextSendMessage(
                    text=f"✅ صحيح يا {display_name}! +{points}\n\nسؤال جديد:\n{self.current_question}\n\n💡 لمح: تلميح\n✅ جاوب: الإجابة"
                )
            }
        
        return None
