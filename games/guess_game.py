import random
import re
from linebot.models import TextSendMessage

class GuessGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_word = None
        self.current_synonyms = None
        self.first_letter = None
        self.category = None

        # قاعدة بيانات ضخمة جداً مع فصحى وعامية سعودية
        self.riddles = [
            # المطبخ
            {"category": "المطبخ", "answer": "قدر", "synonyms": ["قدر", "طنجرة", "طنجره"], "first_letter": "ق"},
            {"category": "المطبخ", "answer": "ملعقة", "synonyms": ["ملعقة", "ملاعق"], "first_letter": "م"},
            {"category": "المطبخ", "answer": "صحن", "synonyms": ["صحن", "طبق"], "first_letter": "ص"},
            {"category": "المطبخ", "answer": "فرن", "synonyms": ["فرن", "مواقد"], "first_letter": "ف"},
            {"category": "المطبخ", "answer": "كوب", "synonyms": ["كوب", "كاسة"], "first_letter": "ك"},
            {"category": "المطبخ", "answer": "مقلاة", "synonyms": ["مقلاة", "طاسة"], "first_letter": "م"},
            {"category": "المطبخ", "answer": "براد", "synonyms": ["براد", "غلاية"], "first_letter": "ب"},
            {"category": "المطبخ", "answer": "سكاكين", "synonyms": ["سكاكين", "سكين"], "first_letter": "س"},

            # غرفة النوم
            {"category": "غرفة النوم", "answer": "سرير", "synonyms": ["سرير", "فراش"], "first_letter": "س"},
            {"category": "غرفة النوم", "answer": "وسادة", "synonyms": ["وسادة", "مخدة"], "first_letter": "و"},
            {"category": "غرفة النوم", "answer": "خزانة", "synonyms": ["خزانة", "دولاب"], "first_letter": "خ"},
            {"category": "غرفة النوم", "answer": "مصباح", "synonyms": ["مصباح", "لمبة", "لمبه"], "first_letter": "م"},
            {"category": "غرفة النوم", "answer": "ستارة", "synonyms": ["ستارة", "بردايه"], "first_letter": "س"},
            {"category": "غرفة النوم", "answer": "مكتب", "synonyms": ["مكتب", "ترابيزه"], "first_letter": "م"},

            # المجلس
            {"category": "المجلس", "answer": "كنب", "synonyms": ["كنب", "أريكة", "صوفا"], "first_letter": "ك"},
            {"category": "المجلس", "answer": "مفرش", "synonyms": ["مفرش", "سجاد", "سجاده"], "first_letter": "م"},
            {"category": "المجلس", "answer": "طاولة", "synonyms": ["طاولة", "ترابيزة"], "first_letter": "ط"},
            {"category": "المجلس", "answer": "كرسي", "synonyms": ["كرسي", "كرسيه"], "first_letter": "ك"},

            # المدرسة
            {"category": "المدرسة", "answer": "قلم", "synonyms": ["قلم", "قلام"], "first_letter": "ق"},
            {"category": "المدرسة", "answer": "دفتر", "synonyms": ["دفتر", "كراسة"], "first_letter": "د"},
            {"category": "المدرسة", "answer": "ممحاة", "synonyms": ["ممحاة", "ممسحه"], "first_letter": "م"},
            {"category": "المدرسة", "answer": "سبورة", "synonyms": ["سبورة", "لوح"], "first_letter": "س"},
            {"category": "المدرسة", "answer": "حقيبة", "synonyms": ["حقيبة", "شنطة"], "first_letter": "ح"},
            {"category": "المدرسة", "answer": "ألوان", "synonyms": ["ألوان", "دراجات"], "first_letter": "أ"},

            # أدوات شخصية
            {"category": "أدوات شخصية", "answer": "فرشاة أسنان", "synonyms": ["فرشاة أسنان", "فرشاه"], "first_letter": "ف"},
            {"category": "أدوات شخصية", "answer": "مشط", "synonyms": ["مشط", "مشطه"], "first_letter": "م"},
            {"category": "أدوات شخصية", "answer": "صابون", "synonyms": ["صابون", "صابونه"], "first_letter": "ص"},
            {"category": "أدوات شخصية", "answer": "مزيل عرق", "synonyms": ["مزيل عرق", "ديودرنت"], "first_letter": "م"},
            {"category": "أدوات شخصية", "answer": "مناشف", "synonyms": ["مناشف", "فوطة"], "first_letter": "م"},

            # الفواكه
            {"category": "الفواكه", "answer": "تفاح", "synonyms": ["تفاح", "تفاحه"], "first_letter": "ت"},
            {"category": "الفواكه", "answer": "موز", "synonyms": ["موز", "موزه"], "first_letter": "م"},
            {"category": "الفواكه", "answer": "برتقال", "synonyms": ["برتقال", "برتقاله"], "first_letter": "ب"},
            {"category": "الفواكه", "answer": "كيوي", "synonyms": ["كيوي", "كيوا"], "first_letter": "ك"},
            {"category": "الفواكه", "answer": "عنب", "synonyms": ["عنب", "عِنب"], "first_letter": "ع"},
            {"category": "الفواكه", "answer": "رمان", "synonyms": ["رمان"], "first_letter": "ر"},
            {"category": "الفواكه", "answer": "خوخ", "synonyms": ["خوخ"], "first_letter": "خ"},

            # الحلويات
            {"category": "الحلويات", "answer": "كيك", "synonyms": ["كيك", "كعكة", "كيكه"], "first_letter": "ك"},
            {"category": "الحلويات", "answer": "بسكويت", "synonyms": ["بسكويت", "كعك"], "first_letter": "ب"},
            {"category": "الحلويات", "answer": "شوكولاتة", "synonyms": ["شوكولاتة", "شوكولا"], "first_letter": "ش"},
            {"category": "الحلويات", "answer": "حلاوة", "synonyms": ["حلاوة", "حلا"], "first_letter": "ح"},

            # الحيوانات
            {"category": "حيوانات", "answer": "قطة", "synonyms": ["قطة", "بسة"], "first_letter": "ق"},
            {"category": "حيوانات", "answer": "كلب", "synonyms": ["كلب", "جرو"], "first_letter": "ك"},
            {"category": "حيوانات", "answer": "حصان", "synonyms": ["حصان", "خيل"], "first_letter": "ح"},
            {"category": "حيوانات", "answer": "جمل", "synonyms": ["جمل", "ناقة"], "first_letter": "ج"},
            {"category": "حيوانات", "answer": "غزال", "synonyms": ["غزال"], "first_letter": "غ"},

            # الطبيعة
            {"category": "الطبيعة", "answer": "شجرة", "synonyms": ["شجرة", "نخلة"], "first_letter": "ش"},
            {"category": "الطبيعة", "answer": "زهرة", "synonyms": ["زهرة", "وردة"], "first_letter": "ز"},
            {"category": "الطبيعة", "answer": "نهر", "synonyms": ["نهر", "جدول"], "first_letter": "ن"},
            {"category": "الطبيعة", "answer": "جبل", "synonyms": ["جبل", "هضبة"], "first_letter": "ج"},

            # السيارات
            {"category": "السيارات", "answer": "سيارة", "synonyms": ["سيارة", "عربية"], "first_letter": "س"},
            {"category": "السيارات", "answer": "دراجة", "synonyms": ["دراجة", "موتوسيكل"], "first_letter": "د"},
            {"category": "السيارات", "answer": "حافلة", "synonyms": ["حافلة", "باص"], "first_letter": "ح"},

            # الرياضة
            {"category": "الرياضة", "answer": "كرة قدم", "synonyms": ["كرة قدم", "كورة"], "first_letter": "ك"},
            {"category": "الرياضة", "answer": "سباحة", "synonyms": ["سباحة"], "first_letter": "س"},
            {"category": "الرياضة", "answer": "جري", "synonyms": ["جري", "ركض"], "first_letter": "ج"},
        ]

    def normalize_text(self, text):
        text = text.strip().lower()
        text = re.sub(r'^ال', '', text)
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ة', 'ه')
        text = text.replace('ى', 'ي')
        text = re.sub(r'[\u064B-\u065F]', '', text)
        return text

    def start_game(self):
        riddle = random.choice(self.riddles)
        self.current_word = riddle["answer"].lower()
        self.current_synonyms = [self.normalize_text(s) for s in riddle.get("synonyms", [self.current_word])]
        self.category = riddle["category"]
        self.first_letter = riddle["first_letter"]

        return TextSendMessage(
            text=f"خمن:\nشيء في {self.category}\nيبدأ بحرف: {self.first_letter}\nما هو؟"
        )

    def check_answer(self, answer, user_id, display_name):
        if not self.current_word:
            return None

        user_answer = self.normalize_text(answer)

        if user_answer in self.current_synonyms:
            points = 10
            msg = f"ممتاز يا {display_name}!\nالإجابة: {self.current_word}\nمن {self.category}\n+{points} نقطة"
            self.current_word = None
            self.current_synonyms = None
            return {
                'message': msg,
                'points': points,
                'won': True,
                'game_over': True,
                'response': TextSendMessage(text=msg)
            }
        else:
            return {
                'message': f"خطأ! حاول مرة أخرى\nشيء في {self.category} يبدأ بـ: {self.first_letter}",
                'points': 0,
                'game_over': False,
                'response': TextSendMessage(text=f"خطأ! حاول مرة أخرى\nشيء في {self.category} يبدأ بـ: {self.first_letter}")
            }
