import random
from linebot.models import TextSendMessage

class CompatibilityGameEnhanced:
    def __init__(self):
        # قائمة الأسماء المتاحة
        self.names = ["أحمد", "ليلى", "سارة", "علي", "مريم", "خالد", "فاطمة", "يوسف", "هالة", "زينب"]
        self.current_pair = None  # تخزين الزوج الحالي
        self.current_percentage = None  # نسبة التوافق الحالية
        self.players_score = {}  # نقاط اللاعبين

    def start_game(self):
        """توليد زوج جديد وعرض السؤال"""
        name1 = random.choice(self.names)
        name2 = random.choice([n for n in self.names if n != name1])
        self.current_pair = (name1, name2)
        self.current_percentage = random.randint(50, 100)
        text = f"💞 ما نسبة التوافق بين {name1} و{name2}؟\n\nاكتب أي رقم لتعرف النتيجة!"
        return TextSendMessage(text=text)

    def check_answer(self, user_id, answer):
        """أي إجابة تعتبر صحيحة، تُظهر النسبة وتمنح نقاط"""
        if not self.current_pair:
            return {"correct": False, "message": "❌ لم يبدأ السؤال بعد.", "points": 0}

        # احتساب النقاط لكل لاعب
        points = 10
        self.players_score[user_id] = self.players_score.get(user_id, 0) + points

        name1, name2 = self.current_pair
        percentage = self.current_percentage

        message = (
            f"✅ {user_id} حصل على {points} نقاط!\n\n"
            f"نسبة التوافق بين {name1} و{name2} هي: {percentage}%\n\n"
            f"المجموع الكلي لديك: {self.players_score[user_id]} نقطة"
        )

        # إعادة تعيين السؤال بعد العرض
        self.current_pair = None
        self.current_percentage = None

        return {"correct": True, "message": message, "points": points}

    def get_score(self, user_id):
        """عرض النقاط الحالية للاعب"""
        return self.players_score.get(user_id, 0)
