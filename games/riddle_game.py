# riddle_game.py
import random
from linebot.models import TextSendMessage

class RiddleGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        
        self.riddles = [
            {"riddle": "ما هو الشيء الذي يحتوي على مفاتيح ولكن لا يوجد به أقفال؟", "answer": "لوحة المفاتيح", "hint": "تستخدم في الحاسوب", "alternatives":["الكيبورد"]},
            {"riddle": "ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟", "answer": "السحابة", "hint": "يطفو في السماء ويسقط مطرًا", "alternatives":[]},
            {"riddle": "شيء له فروع وأوراق ولكنه لا لحاء له، فما هو؟", "answer": "الكتاب", "hint": "تقرأه لتتعلم", "alternatives":[]},
            {"riddle": "شيء له أربع أرجل ولكنه لا يمشي؟", "answer": "الطاولة", "hint": "يوضع عليه الأشياء", "alternatives":[]},
            {"riddle": "شهر إذا حذفنا أول حرف منه أصبح اسم فاكهة، فما هو؟", "answer": "تموز", "hint": "حذف حرف التاء يصبح موز", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي له رقبة ولا رأس؟", "answer": "الزجاجة", "hint": "يُستخدم لوضع السوائل", "alternatives":[]},
            {"riddle": "شيء لا بداية له ولا نهاية؟", "answer": "الدائرة", "hint": "شكل هندسي مستمر", "alternatives":[]},
            {"riddle": "شيء يمكنه ملء الغرفة ولكنه لا يشغل أي مساحة؟", "answer": "الضوء", "hint": "يضيء المكان", "alternatives":[]},
            {"riddle": "شيء له أسنان لكنه لا يأكل؟", "answer": "المشط", "hint": "يستخدم لتصفيف الشعر", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يزيد ولا ينقص أبدًا؟", "answer": "العمر", "hint": "مرتبط بالوقت منذ الولادة", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي ينام وهو يرتدي حذائه؟", "answer": "الحصان", "hint": "يستخدم في الركوب والعمل", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي لا يمشي إلا بالضرب؟", "answer": "المسمار", "hint": "يُثبت الأشياء في الحائط", "alternatives":[]},
            {"riddle": "حاصل ضرب ثلاثة أعداد يساوي حاصل جمعها، ما هي؟", "answer": "1، 2، 3", "hint": "أعداد صحيحة صغيرة", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي له عين ولا يرى؟", "answer": "الإبرة", "hint": "تستخدم في الخياطة", "alternatives":[]},
            {"riddle": "أخت خالتك وليست خالتك؟", "answer": "أمك", "hint": "أقرب إنسان لك", "alternatives":["امك","والدة"]},
            {"riddle": "ما هو الشيء الذي يجري ولا يمشي؟", "answer": "الماء", "hint": "سائل ضروري للحياة", "alternatives":["نهر"]},
            {"riddle": "من هو الذي يكتب ولا يقرأ؟", "answer": "القلم", "hint": "أداة للكتابة", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يأكل ولا يشبع؟", "answer": "النار", "hint": "تحرق كل شيء", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي له أسنان ولكن لا يعض؟", "answer": "المشط", "hint": "يساعد في ترتيب الشعر", "alternatives":[]},
            {"riddle": "شيء يمشي ويقف ولا يتحرك من مكانه؟", "answer": "الساعة", "hint": "تعطي الوقت", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي تراه في الليل والنهار ولكنه لا يتحرك؟", "answer": "القمر", "hint": "يدور حول الأرض", "alternatives":[]},
            {"riddle": "شيء تملكه أنت ولكن يستخدمه الآخرون أكثر منك، ما هو؟", "answer": "اسمك", "hint": "هو هويتك", "alternatives":[]},
            {"riddle": "شيء تملكه منذ ولادتك ولكنه يزداد طولاً كل يوم؟", "answer": "العمر", "hint": "مرتبط بالوقت", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي له قلب ولكنه لا ينبض؟", "answer": "الخس", "hint": "نوع من الخضار", "alternatives":[]},
            {"riddle": "شيء كلما أخذت منه كبر، ما هو؟", "answer": "الحفرة", "hint": "تحفره الأرض", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يملك مدخلًا ولكن لا يملك مخرج؟", "answer": "الإبرة", "hint": "لخياطة الملابس", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي له مدينة ولكنه لا يعيش فيها؟", "answer": "الخريطة", "hint": "ترسم لتعرف الأماكن", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يستطيع الكتابة دون حبر؟", "answer": "القلم الرصاص", "hint": "يكتب ويُمحى", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يرى كل شيء ولكن لا يستطيع الكلام؟", "answer": "المرآة", "hint": "تعكس ما أمامها", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يسمع بلا أذن ويتحدث بلا لسان؟", "answer": "الصدى", "hint": "يتكرر الصوت", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يمتلئ بالماء ولكنه لا يبتل؟", "answer": "الإسفنج", "hint": "يمتص الماء", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يوجد في كل بيت ويُستخدم للطعام؟", "answer": "الملعقة", "hint": "لتناول الطعام", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يمشي بلا قدمين ويطير بلا أجنحة؟", "answer": "الزمن", "hint": "يمر بسرعة", "alternatives":[]},
            {"riddle": "شيء يُكسر بدون أن يُلمس، ما هو؟", "answer": "الوعد", "hint": "الوفاء مهم", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي له وجه ولا يُرى إلا عند النظر إليه؟", "answer": "الساعة", "hint": "تخبر الوقت", "alternatives":[]},
            {"riddle": "شيء موجود في كل مكان ولا يُرى، ما هو؟", "answer": "الهواء", "hint": "ضروري للتنفس", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يُشاهد ولا يُسمع؟", "answer": "الصورة", "hint": "يمكن تعليقها على الحائط", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي كلما أخذت منه يكبر؟", "answer": "الحفرة", "hint": "تُحفر الأرض", "alternatives":[]},
            {"riddle": "شيء يُسافر حول العالم ويبقى في الزاوية؟", "answer": "الطابع البريدي", "hint": "يوضع على الرسائل", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يُفتح ولا يُغلق؟", "answer": "العين", "hint": "للنظر", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي له أوراق ولكنه لا يُزرع؟", "answer": "الكتاب", "hint": "تقرأه لتتعلم", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يُمكن أن يكسر الجليد ولكنه لا يلمس؟", "answer": "الكلام", "hint": "يُستخدم للتواصل", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يتحرك دائماً ولا يمل؟", "answer": "النهر", "hint": "يسيل باستمرار", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي له جذر ولا شجرة؟", "answer": "الكلمة", "hint": "يُكتب أو يُقال", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يطفو ولا يغرق؟", "answer": "الخشب", "hint": "يُستخدم للبناء", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يُرى في الظلام ويختفي في النهار؟", "answer": "النجوم", "hint": "تزين السماء ليلاً", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يتكلم جميع لغات العالم؟", "answer": "الصدى", "hint": "يكرر ما تقوله", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يُعطيك القوة ولا يخصك؟", "answer": "المعرفة", "hint": "مفتاح النجاح", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي لا يموت أبداً؟", "answer": "الذكرى", "hint": "يبقى في الأذهان", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يتحرك في كل مكان لكنه لا يلمس؟", "answer": "الوقت", "hint": "مرتبط بالحياة", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يُشاهد ولا يُلمس؟", "answer": "الظل", "hint": "يتغير مع الضوء", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي لا يبتل إذا غُمر في الماء؟", "answer": "الظل", "hint": "يظهر على الأرض", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يملك بداية ولكن لا نهاية؟", "answer": "الخط", "hint": "يمكن رسمه", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يمتلك قلبًا ولا ينبض؟", "answer": "الخس", "hint": "خضار", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يكسر دون أن يُلمس؟", "answer": "الوعد", "hint": "الوفاء مهم", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يمشي بلا أرجل؟", "answer": "الزمن", "hint": "يمر سريعًا", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يمتلئ ولا يشغل مساحة؟", "answer": "الضوء", "hint": "يضيء المكان", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يُكتب بدون قلم؟", "answer": "الكتابة على الشاشة", "hint": "عن طريق الحاسوب أو الهاتف", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يمكن أن تكسره بدون لمسه؟", "answer": "الوعد", "hint": "الوفاء شيء مهم", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يملأ الغرفة بدون أن يلمس شيئًا؟", "answer": "الضوء", "hint": "ينير المكان", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي له وجه ولكن لا يمكن رؤيته إلا عند النظر إليه؟", "answer": "الساعة", "hint": "تحدد الوقت", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يمشي ويقف بلا قدمين؟", "answer": "الساعة", "hint": "تحدد الوقت", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يسير أمامك ولا تراه؟", "answer": "المستقبل", "hint": "الزمن الذي لم يأت بعد", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يمشي بلا أقدام ولا يستطيع الطيران؟", "answer": "النهر", "hint": "يسيل باستمرار", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يرى كل شيء لكنه لا يتحرك؟", "answer": "المرآة", "hint": "تعكس ما أمامها", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يملك مدخلًا ولا يملك مخرج؟", "answer": "الإبرة", "hint": "لخياطة الملابس", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يتكلم ولا يملك لسان؟", "answer": "الصدى", "hint": "يكرر الصوت", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يتحرك دائمًا ولا يمل؟", "answer": "النهر", "hint": "يسيل باستمرار", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي له أوراق ولكنه لا يُزرع؟", "answer": "الكتاب", "hint": "تقرأه لتتعلم", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يُكسر بدون أن يُلمس؟", "answer": "الوعد", "hint": "الوفاء مهم", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يُسافر حول العالم ويبقى في الزاوية؟", "answer": "الطابع البريدي", "hint": "يوضع على الرسائل", "alternatives":[]},
            {"riddle": "ما هو الشيء الذي يُفتح ولا يُغلق؟", "answer": "العين", "hint": "للنظر", "alternatives":[]},
        ]
        
        self.remaining_riddles = self.riddles.copy()
        random.shuffle(self.remaining_riddles)
        
        self.current_riddle = None
        self.current_answer = None
        self.current_hint = None
        self.current_alternatives = []
    
    def start_game(self):
        if not self.remaining_riddles:
            self.remaining_riddles = self.riddles.copy()
            random.shuffle(self.remaining_riddles)
        
        riddle_data = self.remaining_riddles.pop()
        self.current_riddle = riddle_data["riddle"]
        self.current_answer = riddle_data["answer"]
        self.current_hint = riddle_data["hint"]
        self.current_alternatives = riddle_data.get("alternatives", [])
        
        return TextSendMessage(
            text=f"لعبة الألغاز الصعبة\n\n{self.current_riddle}\n\nاكتب الإجابة أو اطلب تلميح"
        )
    
    def get_hint(self):
        return self.current_hint if self.current_hint else "لا يوجد تلميح متاح"
    
    def get_answer(self):
        return self.current_answer if self.current_answer else "لا يوجد لغز حالي"
    
    def check_answer(self, answer, user_id, display_name):
        if not self.current_answer:
            return None
        
        normalized_answer = answer.strip().lower()
        correct_answer = self.current_answer.lower()
        normalized_alternatives = [alt.lower() for alt in self.current_alternatives]
        
        if normalized_answer == correct_answer or normalized_answer in normalized_alternatives:
            points = 20
            
            if not self.remaining_riddles:
                self.remaining_riddles = self.riddles.copy()
                random.shuffle(self.remaining_riddles)
            new_riddle_data = self.remaining_riddles.pop()
            self.current_riddle = new_riddle_data["riddle"]
            self.current_answer = new_riddle_data["answer"]
            self.current_hint = new_riddle_data["hint"]
            self.current_alternatives = new_riddle_data.get("alternatives", [])
            
            return {
                'points': points,
                'won': True,
                'response': TextSendMessage(
                    text=f"✅ أحسنت يا {display_name}! +{points}\n\nلغز جديد:\n{self.current_riddle}"
                )
            }
        
        return {
            'points': 0,
            'won': False,
            'response': TextSendMessage(
                text=f"❌ إجابة خاطئة، حاول مرة أخرى.\n{self.current_riddle}"
            )
        }
