class GameName:
    def __init__(self, line_bot_api=None, use_ai=False, get_api_key=None, switch_key=None):
        """
        تهيئة اللعبة بشكل موحد لكل الألعاب.

        Args:
            line_bot_api: كائن LineBotApi للتواصل مع LINE.
            use_ai (bool): هل تستخدم الذكاء الاصطناعي في اللعبة.
            get_api_key (function): دالة لإرجاع مفتاح API للذكاء الاصطناعي.
            switch_key (function): دالة لتغيير مفتاح AI في حال فشل المفتاح الحالي.
        """
        self.line_bot_api = line_bot_api
        self.use_ai = use_ai
        self.get_api_key = get_api_key
        self.switch_key = switch_key

        # متغيرات خاصة باللعبة
        self.current_question = None
        self.current_answer = None
        self.hint_used = False

        # أي إعدادات أخرى خاصة باللعبة يمكن إضافتها هنا
