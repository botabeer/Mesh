"""
لعبة الذكاء المحدثة - IQ Game
مثال على استخدام BaseGame والتصاميم الجديدة
"""

from base_game import BaseGame
from linebot.models import TextSendMessage
import random


class IQGame(BaseGame):
    """لعبة الذكاء - أسئلة IQ متنوعة"""
    
    def __init__(self, line_bot_api, use_ai=False, get_api_key=None, switch_key=None):
        super().__init__(line_bot_api, 'ذكاء')
        self.use_ai = use_ai
        self.get_api_key = get_api_key
        self.switch_key = switch_key
        
        # بنك الأسئلة
        self.questions_bank = [
            {
                'question': 'ما هو الشيء الذي له رقبة ولا يملك رأس؟',
                'answer': 'زجاجة',
                'hint': 'شيء نستخدمه للشرب'
            },
            {
                'question': 'أنا أطير بلا أجنحة، وأبكي بلا عيون. ما أنا؟',
                'answer': 'سحابة',
                'hint': 'موجود في السماء'
            },
            {
                'question': 'ما الذي يمكن كسره دون لمسه؟',
                'answer': 'وعد',
                'hint': 'شيء معنوي'
            },
            {
                'question': 'أنا خفيف كالريشة، لكن لا يمكن لأحد حملي لأكثر من دقيقة. ما أنا؟',
                'answer': 'نفس',
                'hint': 'شيء نفعله باستمرار'
            },
            {
                'question': 'له أسنان كثيرة لكنه لا يعض. ما هو؟',
                'answer': 'مشط',
                'hint': 'نستخدمه للشعر'
            },
            {
                'question': 'ما الذي يزداد حجمه كلما أخذت منه؟',
                'answer': 'حفرة',
                'hint': 'في الأرض'
            },
            {
                'question': 'له يد واحدة ووجه لكنه ليس إنسان. ما هو؟',
                'answer': 'ساعة',
                'hint': 'نراه يومياً'
            },
            {
                'question': 'أنا أركض لكن لا أمشي أبداً. ما أنا؟',
                'answer': 'ماء',
                'hint': 'سائل'
            },
            {
                'question': 'ما الشيء الذي كله ثقوب ومع ذلك يحتفظ بالماء؟',
                'answer': 'اسفنجة',
                'hint': 'نستخدمه للتنظيف'
            },
            {
                'question': 'أنا أصبح أصغر كلما استحممت. ما أنا؟',
                'answer': 'صابون',
                'hint': 'نستخدمه في الحمام'
            },
            {
                'question': 'ما الذي يمكنه السفر حول العالم دون مغادرة زاويته؟',
                'answer': 'طابع',
                'hint': 'على الرسالة'
            },
            {
                'question': 'له أربع أرجل في الصباح، ورجلان في الظهيرة، وثلاثة في المساء. ما هو؟',
                'answer': 'انسان',
                'hint': 'لغز أبو الهول الشهير'
            },
            {
                'question': 'ما هو الشيء الذي إذا أكلته كله تموت وإذا أكلت نصفه تعيش؟',
                'answer': 'سمسم',
                'hint': 'حبوب صغيرة'
            },
            {
                'question': 'شيء موجود في وسط باريس. ما هو؟',
                'answer': 'حرف الراء',
                'hint': 'فكر في الاسم'
            },
            {
                'question': 'كلما جف كلما بل. ما هو؟',
                'answer': 'منشفة',
                'hint': 'بعد الاستحمام'
            },
            {
                'question': 'له قلب ولكن لا يوجد له أعضاء أخرى. ما هو؟',
                'answer': 'بطاقة',
                'hint': 'ألعاب ورقية'
            },
            {
                'question': 'ما الذي يأتي مرة في الدقيقة ومرتين في اللحظة ولا يأتي في الساعة؟',
                'answer': 'حرف الحاء',
                'hint': 'حرف من الحروف'
            },
            {
                'question': 'يمشي بلا أرجل، ويبكي بلا عيون. ما هو؟',
                'answer': 'مطر',
                'hint': 'من السماء'
            },
            {
                'question': 'ما هو الشيء الذي تحمله وهو يحملك في نفس الوقت؟',
                'answer': 'حذاء',
                'hint': 'نلبسه في القدم'
            },
            {
                'question': 'أنا أتكلم بلا فم وأسمع بلا أذن. ما أنا؟',
                'answer': 'صدى',
                'hint': 'صوت مرتد'
            }
        ]
        
        # خلط الأسئلة
        random.shuffle(self.questions_bank)
        self.current_question_index = 0
    
    def _generate_question(self):
        """توليد سؤال جديد"""
        if self.current_question_index >= len(self.questions_bank):
            random.shuffle(self.questions_bank)
            self.current_question_index = 0
        
        question_data = self.questions_bank[self.current_question_index]
        self.current_question_index += 1
        
        self.current_answer = question_data['answer']
        self.current_hint = question_data['hint']
        self.question_start_time = None
        self.used_hints = False
        
        message = f"🧠 سؤال {self.current_question} من {self.max_questions}\n\n"
        message += f"❓ {question_data['question']}\n\n"
        message += f"━━━━━━━━━━━━━━━━\n"
        message += f"💡 للحصول على تلميح اكتب: لمح\n"
        message += f"📊 النقاط الحالية: {self.total_score}"
        
        return TextSendMessage(text=message)
    
    def _check_answer_logic(self, user_answer):
        """فحص الإجابة"""
        normalized_user = self._normalize_text(user_answer)
        normalized_correct = self._normalize_text(self.current_answer)
        
        return normalized_user == normalized_correct
    
    def _get_hint(self):
        """الحصول على تلميح"""
        if hasattr(self, 'current_hint'):
            return self.current_hint
        return super()._get_hint()


# مثال على استخدام اللعبة:
"""
from linebot import LineBotApi

line_bot_api = LineBotApi('YOUR_TOKEN')
game = IQGame(line_bot_api)

# بدء اللعبة
start_message = game.start_game()
# أرسل start_message للاعب

# فحص إجابة
result = game.check_answer("زجاجة", "user123", "أحمد")
# النتيجة تحتوي على:
# - points: النقاط المكتسبة
# - won: هل فاز اللاعب
# - game_over: هل انتهت اللعبة
# - response: الرسالة المراد إرسالها
"""
