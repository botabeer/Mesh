"""
لعبة الفروقات - آلية لعب مبسطة جداً
اللاعب يختار رقم الفرق من 1 إلى 5
"""

from linebot.models import TextSendMessage, ImageSendMessage
import random
import logging

logger = logging.getLogger(__name__)


class DifferencesGame:
    """لعبة الفروقات المبسطة"""
    
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_image = None
        self.correct_differences = set()
        self.found_count = 0
        
        # مجموعة كبيرة من الصور - ضع روابط صورك هنا
        self.images = [
            {
                'url': 'https://i.imgur.com/YOUR_IMAGE_1.jpg',
                'differences': {1, 3, 5}  # الفروقات الصحيحة (من 1 إلى 5)
            },
            {
                'url': 'https://i.imgur.com/YOUR_IMAGE_2.jpg',
                'differences': {2, 4, 5}
            },
            {
                'url': 'https://i.imgur.com/YOUR_IMAGE_3.jpg',
                'differences': {1, 2, 3}
            },
            {
                'url': 'https://i.imgur.com/YOUR_IMAGE_4.jpg',
                'differences': {1, 3, 4}
            },
            {
                'url': 'https://i.imgur.com/YOUR_IMAGE_5.jpg',
                'differences': {2, 3, 5}
            },
            {
                'url': 'https://i.imgur.com/YOUR_IMAGE_6.jpg',
                'differences': {1, 2, 5}
            },
            {
                'url': 'https://i.imgur.com/YOUR_IMAGE_7.jpg',
                'differences': {1, 4, 5}
            },
            {
                'url': 'https://i.imgur.com/YOUR_IMAGE_8.jpg',
                'differences': {2, 3, 4}
            },
            {
                'url': 'https://i.imgur.com/YOUR_IMAGE_9.jpg',
                'differences': {1, 2, 4}
            },
            {
                'url': 'https://i.imgur.com/YOUR_IMAGE_10.jpg',
                'differences': {3, 4, 5}
            },
            # أضف المزيد من الصور هنا...
        ]
    
    def start_game(self):
        """بدء لعبة جديدة"""
        try:
            self.current_image = random.choice(self.images)
            self.correct_differences = self.current_image['differences']
            self.found_count = 0
            
            # إرسال الصورة مع التعليمات
            return [
                ImageSendMessage(
                    original_content_url=self.current_image['url'],
                    preview_image_url=self.current_image['url']
                ),
                TextSendMessage(
                    text=f"اوجد الفروقات!\n\n"
                         f"اكتب رقم الفرق من 1 الى 5\n"
                         f"مثال: 1\n\n"
                         f"لمح - للحصول على تلميح\n"
                         f"جاوب - لعرض الاجابة"
                )
            ]
            
        except Exception as e:
            logger.error(f"خطأ في بدء لعبة الفروقات: {e}")
            return TextSendMessage(text="حدث خطأ في بدء اللعبة")
    
    def check_answer(self, answer, user_id, display_name):
        """فحص إجابة اللاعب"""
        try:
            if not self.current_image:
                return None
            
            answer = answer.strip()
            
            # أوامر خاصة
            if answer in ['لمح', 'تلميح']:
                return self._give_hint()
            
            if answer in ['جاوب', 'استسلم']:
                return self._show_answer()
            
            # محاولة تحويل الإجابة لرقم
            try:
                num = int(answer)
                if num < 1 or num > 5:
                    return {
                        'points': 0,
                        'won': False,
                        'response': TextSendMessage(text="اكتب رقم من 1 الى 5 فقط")
                    }
                
                # فحص الإجابة
                if num in self.correct_differences:
                    self.found_count += 1
                    remaining = len(self.correct_differences) - self.found_count
                    
                    if remaining == 0:
                        # فاز اللاعب
                        return {
                            'points': 10,
                            'won': True,
                            'game_over': False,
                            'response': TextSendMessage(
                                text=f"ممتاز {display_name}!\n\n"
                                     f"وجدت جميع الفروقات\n"
                                     f"النقاط: +10"
                            )
                        }
                    else:
                        return {
                            'points': 2,
                            'won': False,
                            'response': TextSendMessage(
                                text=f"صح!\n\n"
                                     f"النقاط: +2\n"
                                     f"الباقي: {remaining}"
                            )
                        }
                else:
                    return {
                        'points': 0,
                        'won': False,
                        'response': TextSendMessage(text="خطأ! حاول مرة اخرى")
                    }
                    
            except ValueError:
                return {
                    'points': 0,
                    'won': False,
                    'response': TextSendMessage(text="اكتب رقم من 1 الى 5")
                }
            
        except Exception as e:
            logger.error(f"خطأ في فحص الإجابة: {e}")
            return None
    
    def _give_hint(self):
        """إعطاء تلميح"""
        if self.correct_differences:
            hint_num = list(self.correct_differences)[0]
            return {
                'points': 0,
                'won': False,
                'response': TextSendMessage(text=f"تلميح: جرب رقم {hint_num}")
            }
        return None
    
    def _show_answer(self):
        """عرض الإجابة"""
        answer = ', '.join(map(str, sorted(self.correct_differences)))
        return {
            'points': 0,
            'won': False,
            'game_over': True,
            'response': TextSendMessage(
                text=f"الفروقات الصحيحة:\n{answer}"
            )
        }
