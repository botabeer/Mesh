from linebot.models import TextSendMessage
import random
import logging
from utils.helpers import normalize_text

logger = logging.getLogger(__name__)

class CompatibilityGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.name1 = None
        self.name2 = None
        self.compatibility_score = None
        self.hint_count = 0
    
    def start_game(self):
        """بدء اللعبة"""
        try:
            message = "🖤 لعبة التوافق\n\n▪️ اكتب اسمين مفصولين بمسافة\n\n(مثال: محمد فاطمة)"
            
            return TextSendMessage(text=message)
            
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
            
            self.name1 = names[0]
            self.name2 = names[1]
            
            # حساب نسبة التوافق (خوارزمية بسيطة)
            self.compatibility_score = self._calculate_compatibility(self.name1, self.name2)
            
            # رسالة التوافق
            if self.compatibility_score >= 90:
                emoji = "🖤"
                status = "توافق مثالي"
            elif self.compatibility_score >= 75:
                emoji = "🖤"
                status = "توافق ممتاز"
            elif self.compatibility_score >= 60:
                emoji = "🖤"
                status = "توافق جيد"
            elif self.compatibility_score >= 45:
                emoji = "🖤"
                status = "توافق متوسط"
            elif self.compatibility_score >= 30:
                emoji = "🖤"
                status = "توافق ضعيف"
            else:
                emoji = "🖤"
                status = "لا يوجد توافق"
            
            message = f"{emoji} نتيجة التوافق:\n\n▪️ {self.name1} ✨ {self.name2}\n▪️ النسبة: {self.compatibility_score}%\n▪️ الحالة: {status}"
            
            # منح نقاط بناءً على استخدام اللعبة
            points = 5
            
            return {
                'points': points,
                'won': True,
                'response': TextSendMessage(text=message)
            }
            
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة التوافق: {e}", exc_info=True)
            return None
    
    def _calculate_compatibility(self, name1, name2):
        """خوارزمية حساب التوافق"""
        # استخدام طريقة FLAMES المعدلة
        name1_clean = normalize_text(name1)
        name2_clean = normalize_text(name2)
        
        # حساب الأحرف المشتركة
        common_letters = set(name1_clean) & set(name2_clean)
        total_letters = len(set(name1_clean + name2_clean))
        
        if total_letters == 0:
            return random.randint(40, 60)
        
        # نسبة التوافق الأولية
        base_score = (len(common_letters) / total_letters) * 100
        
        # إضافة عامل عشوائي للتنويع
        random_factor = random.randint(-15, 15)
        
        # النتيجة النهائية
        final_score = int(max(0, min(100, base_score + random_factor)))
        
        return final_score
    
    def get_hint(self):
        """تلميح غير متوفر في هذه اللعبة"""
        return "💡 لا توجد تلميحات في لعبة التوافق\n\nفقط اكتب اسمين!"
    
    def reveal_answer(self):
        """لا يوجد جواب محدد في هذه اللعبة"""
        return "▫️ لعبة التوافق تعتمد على الأسماء التي تدخلها"
