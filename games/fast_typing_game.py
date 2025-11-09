import random
from datetime import datetime
from linebot.models import TextSendMessage

class FastTypingGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.target_text = None
        self.start_time = None
        self.finished = False
        
        # كلمات قصيرة
        self.words = [
            "برمجة", "حاسوب", "إنترنت", "تطبيق", "موقع", "بيانات",
            "تكنولوجيا", "ذكاء", "مستخدم", "تطوير", "تصميم", "خوارزمية",
            "تعلم", "ابتكار", "إبداع", "إدارة", "تحليل", "خدمة", "مشروع",
            "معرفة", "تخزين", "تحديث", "أمان", "تشفير", "خادم", "واجهة"
        ]
        
        # جمل قصيرة
        self.sentences = [
            "التدريب يصنع الإتقان", "الوقت من ذهب", "العلم نور والجهل ظلام",
            "الصبر مفتاح الفرج", "من جد وجد ومن زرع حصد", "الصديق وقت الضيق",
            "في التأني السلامة وفي العجلة الندامة", "العقل السليم في الجسم السليم",
            "لكل مجتهد نصيب", "القناعة كنز لا يفنى", "النظافة من الإيمان",
            "الأمانة غالية", "الصدق منجاة", "الحكمة ضالة المؤمن", "اطلبوا العلم من المهد إلى اللحد",
            "خير الأمور أوسطها", "رب ضارة نافعة", "الحاجة أم الاختراع", "الاتحاد قوة",
            "الصحة تاج على رؤوس الأصحاء", "العمل عبادة", "الوفاء من شيم الكرام",
            "الأخلاق الحسنة زينة الإنسان", "التواضع من صفات العظماء", "الأمل يصنع المستحيل",
            "النجاح رحلة وليس وجهة"
        ]
    
    def start_game(self):
        """اختيار كلمة أو جملة عشوائياً"""
        choice = random.choice(["word", "sentence"])
        self.target_text = random.choice(self.words) if choice == "word" else random.choice(self.sentences)
        self.start_time = datetime.now()
        self.finished = False
        
        # إيموجي خفيف واحد فقط ⚡
        return TextSendMessage(
            text=f"⚡ اكتب التالي بسرعة ودقة:\n\n{self.target_text}\n\nمن يكتبه أولاً يفوز"
        )
    
    def get_hint(self):
        """تلميح أول كلمتين للجملة أو بداية الكلمة"""
        if not self.target_text:
            return "لا يوجد نص حالي"
        words = self.target_text.split()
        return f"تبدأ بـ: {words[0]}..." if len(words) == 1 else f"تبدأ بـ: {words[0]} {words[1]}..."
    
    def get_answer(self):
        if not self.target_text:
            return "لا يوجد نص حالي"
        return self.target_text
    
    def check_answer(self, answer, user_id, display_name):
        if not self.target_text or self.finished:
            return None
        
        user_answer = answer.strip()
        if user_answer == self.target_text:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            self.finished = True
            
            # نقاط حسب السرعة
            if elapsed <= 3:
                points = 20
                speed = "سريع جداً"
            elif elapsed <= 6:
                points = 15
                speed = "جيد"
            else:
                points = 10
                speed = "بطيء"
            
            msg = f"فاز {display_name}!\n{speed}\nالوقت: {elapsed:.2f} ثانية\n+{points} نقطة"
            
            return {
                'message': msg,
                'points': points,
                'won': True,
                'game_over': True,
                'response': TextSendMessage(text=msg)
            }
        
        return None
