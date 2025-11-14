import random
import logging
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

logger = logging.getLogger(__name__)

class CompatibilityGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.name1 = None
        self.name2 = None
        self.compatibility_score = None
    
    def start_game(self):
        """بدء اللعبة"""
        try:
            return TextSendMessage(
                text="🖤 لعبة التوافق\n\n▪️ اكتب اسمين مفصولين بمسافة\n\n(مثال: محمد فاطمة)"
            )
        except Exception as e:
            logger.error(f"❌ خطأ في بدء لعبة التوافق: {e}", exc_info=True)
            return TextSendMessage(text="❌ حدث خطأ في بدء اللعبة")
    
    def check_answer(self, answer, user_id, display_name):
        """فحص الإجابة وحساب التوافق"""
        try:
            names = answer.strip().split()
            
            if len(names) < 2:
                return {
                    'points': 0,
                    'won': False,
                    'response': TextSendMessage(
                        text="⚠️ يرجى كتابة اسمين مفصولين بمسافة\n\n(مثال: ميش عبير)"
                    )
                }
            
            self.name1, self.name2 = names[0], names[1]
            self.compatibility_score = self._calculate_compatibility(self.name1, self.name2)

            # تحديد الحالة حسب النسبة
            score = self.compatibility_score
            if score >= 90:
                status = "توافق مثالي 🖤"
            elif score >= 75:
                status = "توافق ممتاز 🖤"
            elif score >= 60:
                status = "توافق جيد 🖤"
            elif score >= 45:
                status = "توافق متوسط 🖤"
            elif score >= 30:
                status = "توافق ضعيف 🖤"
            else:
                status = "لا يوجد توافق 🖤"
            
            msg = (
                f"🖤 نتيجة التوافق:\n\n"
                f"▪️ {self.name1} ✨ {self.name2}\n"
                f"▪️ النسبة: {score}%\n"
                f"▪️ الحالة: {status}"
            )

            return {
                "points": 5,
                "won": True,
                "response": TextSendMessage(text=msg),
            }

        except Exception as e:
            logger.error(f"❌ خطأ في معالجة التوافق: {e}", exc_info=True)
            return None
    
    def _calculate_compatibility(self, name1, name2):
        """خوارزمية حساب التوافق"""
        n1 = normalize_text(name1)
        n2 = normalize_text(name2)

        common = set(n1) & set(n2)
        total = len(set(n1 + n2))

        if total == 0:
            return random.randint(40, 60)

        base = (len(common) / total) * 100
        random_factor = random.randint(-15, 15)

        return int(max(0, min(100, base + random_factor)))
    
    def get_hint(self):
        return "💡 لا توجد تلميحات في لعبة التوافق\n\nفقط اكتب اسمين!"
    
    def reveal_answer(self):
        return "▫️ لعبة التوافق تعتمد على الأسماء التي تدخلها"
