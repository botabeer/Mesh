"""
لعبة أسئلة الذكاء - Enhanced Version
Created by: Abeer Aldosari © 2025
"""
from linebot.models import TextSendMessage
from .base_game import BaseGame
import random


class IqGame(BaseGame):
    """لعبة أسئلة الذكاء المحسنة"""
    
    def __init__(self, line_bot_api, use_ai=False, get_api_key=None, switch_key=None):
        super().__init__(line_bot_api, questions_count=10)
        self.use_ai = use_ai
        self.get_api_key = get_api_key
        self.switch_key = switch_key
        
        self.questions = [
            {"q": "ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟", "a": "السحاب",
             "hint": "يُرى في السماء ويجلب المطر"},
            {"q": "ما هو الشيء الذي له رأس ولا يملك عيون؟", "a": "الدبوس",
             "hint": "أداة صغيرة للتثبيت"},
            {"q": "شيء موجود في السماء إذا أضفت له حرفاً أصبح في الأرض؟", "a": "نجم",
             "hint": "يضيء ليلاً، والحرف هو 'م'"},
            {"q": "ما هو الشيء الذي كلما زاد نقص؟", "a": "العمر",
             "hint": "يمر مع كل يوم"},
            {"q": "له عين ولا يرى؟", "a": "الإبرة",
             "hint": "تُستخدم في الخياطة"},
            {"q": "ما هو الشيء الذي يكتب ولا يقرأ؟", "a": "القلم",
             "hint": "أداة الكتابة"},
            {"q": "شيء إذا أكلته كله تستفيد وإذا أكلت نصفه تموت؟", "a": "السمسم",
             "hint": "حبوب صغيرة"},
            {"q": "ما هو البيت الذي ليس له أبواب ولا نوافذ؟", "a": "بيت الشعر",
             "hint": "يُكتب ولا يُسكن"},
            {"q": "شيء له أسنان ولا يعض؟", "a": "المشط",
             "hint": "يُستخدم للشعر"},
            {"q": "ما هو الشيء الذي يسمع بلا أذن ويتكلم بلا لسان؟", "a": "الهاتف",
             "hint": "جهاز اتصال"},
            {"q": "أنا ابن الماء فإن تركوني في الماء مت، فمن أنا؟", "a": "الثلج",
             "hint": "يذوب في الحرارة"},
            {"q": "ما هو الشيء الذي يقرصك ولا تراه؟", "a": "الجوع",
             "hint": "شعور من نقص الطعام"},
            {"q": "له رقبة وليس له رأس؟", "a": "الزجاجة",
             "hint": "تُستخدم لحفظ السوائل"},
            {"q": "ما هو الحيوان الذي يحك أذنه بأنفه؟", "a": "الفيل",
             "hint": "له خرطوم طويل"},
            {"q": "كلما أخذت منه كبر؟", "a": "الحفرة",
             "hint": "تُحفر في الأرض"},
            {"q": "ما هو الشيء الذي يخترق الزجاج ولا يكسره؟", "a": "الضوء",
             "hint": "يأتي من الشمس"},
            {"q": "شيء أمامك لا تراه؟", "a": "المستقبل",
             "hint": "الزمن القادم"},
            {"q": "ما هو الشيء الذي له أربع أرجل ولا يمشي؟", "a": "الكرسي",
             "hint": "نجلس عليه"},
            {"q": "ما هو الشيء الذي ينبض بلا قلب؟", "a": "الساعة",
             "hint": "تقيس الوقت"},
            {"q": "شيء تحمله ويحملك؟", "a": "الحذاء",
             "hint": "نلبسه في القدم"},
        ]
        
        random.shuffle(self.questions)

    def start_game(self):
        """بدء اللعبة"""
        self.current_question = 0
        self.game_active = True
        return self.get_question()

    def get_question(self):
        """عرض السؤال الحالي"""
        q_data = self.questions[self.current_question % len(self.questions)]
        self.current_answer = q_data["a"]
        self._current_hint = q_data.get("hint", "")

        message = f"🧠 سؤال ذكاء ({self.current_question + 1}/{self.questions_count})\n\n"
        message += f"❓ {q_data['q']}\n\n"
        message += "اكتب الإجابة أو:\n"
        message += "• لمح - للحصول على تلميح\n"
        message += "• جاوب - لمعرفة الإجابة"

        return TextSendMessage(text=message)

    def get_hint(self):
        """إرجاع تلميح"""
        if hasattr(self, '_current_hint') and self._current_hint:
            return f"💡 تلميح: {self._current_hint}"
        return f"💡 تلميح: الإجابة تبدأ بـ '{self.current_answer[0]}'"

    def check_answer(self, user_answer, user_id, display_name):
        """فحص الإجابة"""
        if not self.game_active:
            return None

        if user_answer == 'لمح':
            hint = self.get_hint()
            return {
                'message': hint,
                'response': TextSendMessage(text=hint),
                'points': 0
            }

        if user_answer == 'جاوب':
            reveal = self.reveal_answer()
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                return next_q
            
            message = f"{reveal}\n\n"
            if hasattr(next_q, 'text'):
                message += next_q.text
            return {
                'message': message,
                'response': TextSendMessage(text=message),
                'points': 0
            }

        # فحص الإجابة
        normalized_answer = self.normalize_text(user_answer)
        normalized_correct = self.normalize_text(self.current_answer)

        if normalized_answer == normalized_correct or normalized_answer in normalized_correct:
            points = self.add_score(user_id, display_name, 10)
            next_q = self.next_question()
            
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                return next_q

            message = f"✅ إجابة صحيحة يا {display_name}!\n+{points} نقطة\n\n"
            if hasattr(next_q, 'text'):
                message += next_q.text

            return {
                'message': message,
                'response': TextSendMessage(text=message),
                'points': points
            }

        return None
