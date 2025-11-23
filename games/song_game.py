"""
لعبة تخمين الأغنية - محسنة
Created by: Abeer Aldosari © 2025
"""
from .base_game import BaseGame
import random
import difflib

class SongGame(BaseGame):
    """لعبة تخمين المغني من كلمات الأغنية"""
    
    def __init__(self, line_api):
        super().__init__(line_api, rounds=5)
        self.songs = [
            {'lyrics': 'رجعت لي أيام الماضي معاك', 'artist': 'أم كلثوم'},
            {'lyrics': 'جلست والخوف بعينيها تتأمل فنجاني', 'artist': 'عبد الحليم حافظ'},
            {'lyrics': 'تملي معاك ولو حتى بعيد عني', 'artist': 'عمرو دياب'},
            {'lyrics': 'يا بنات يا بنات', 'artist': 'نانسي عجرم'},
            {'lyrics': 'قولي أحبك كي تزيد وسامتي', 'artist': 'كاظم الساهر'},
            {'lyrics': 'أنا لحبيبي وحبيبي إلي', 'artist': 'فيروز'},
            {'lyrics': 'حبيبي يا كل الحياة اوعدني تبقى معايا', 'artist': 'تامر حسني'},
            {'lyrics': 'قلبي بيسألني عنك دخلك طمني وينك', 'artist': 'وائل كفوري'},
            {'lyrics': 'كيف أبيّن لك شعوري دون ما أحكي', 'artist': 'عايض'},
            {'lyrics': 'اسخر لك غلا وتشوفني مقصر', 'artist': 'عايض'},
            {'lyrics': 'رحت عني ما قويت جيت لك لاتردني', 'artist': 'عبدالمجيد عبدالله'},
            {'lyrics': 'خذني من ليلي لليلك', 'artist': 'عبادي الجوهر'},
            {'lyrics': 'تدري كثر ماني من البعد مخنوق', 'artist': 'راشد الماجد'},
            {'lyrics': 'انسى هالعالم ولو هم يزعلون', 'artist': 'عباس ابراهيم'},
            {'lyrics': 'أنا عندي قلب واحد', 'artist': 'حسين الجسمي'},
            {'lyrics': 'منوتي ليتك معي', 'artist': 'محمد عبده'},
            {'lyrics': 'خلنا مني طمني عليك', 'artist': 'نوال الكويتية'},
            {'lyrics': 'أحبك ليه أنا مدري', 'artist': 'عبدالمجيد عبدالله'},
            {'lyrics': 'أمر الله أقوى أحبك والعقل واعي', 'artist': 'ماجد المهندس'},
            {'lyrics': 'الحب يتعب من يدله والله في حبه بلاني', 'artist': 'راشد الماجد'},
            {'lyrics': 'محد غيرك شغل عقلي شغل بالي', 'artist': 'وليد الشامي'},
            {'lyrics': 'نكتشف مر الحقيقة بعد ما يفوت الأوان', 'artist': 'أصالة'},
            {'lyrics': 'يا هي توجع كذبة اخباري تمام', 'artist': 'أميمة طالب'},
            {'lyrics': 'احس اني لقيتك بس عشان تضيع مني', 'artist': 'عبدالمجيد عبدالله'},
            {'lyrics': 'بردان أنا تكفى أبي احترق بدفا لعيونك', 'artist': 'محمد عبده'}
        ]
        random.shuffle(self.songs)

    def start_game(self):
        """بدء اللعبة"""
        self.current_round = 0
        return self.generate_question()

    def generate_question(self):
        """توليد سؤال جديد"""
        song = self.songs[self.current_round % len(self.songs)]
        self.current_answer = song['artist']
        
        extra_info = f"💡 اكتب اسم المغني\n• لمح: للحصول على تلميح\n• جاوب: لمعرفة الإجابة"
        
        return self.build_question_flex(
            "لعبة الأغنية 🎵",
            f"🎤 من المغني؟\n\n« {song['lyrics']} »",
            extra_info
        )

    def check_answer(self, answer, uid, name):
        """فحص الإجابة"""
        normalized = self.normalize_text(answer)
        
        # تلميح
        if normalized == 'لمح':
            first_char = self.current_answer[0]
            length = len(self.current_answer)
            hint = f"💡 تلميح: أول حرف '{first_char}' وعدد الحروف {length}"
            return {
                'points': 0,
                'won': False,
                'response': self.build_question_flex(
                    "لعبة الأغنية 🎵",
                    hint,
                    "اكتب اسم المغني"
                )
            }
        
        # عرض الإجابة
        if normalized == 'جاوب':
            song = self.songs[self.current_round % len(self.songs)]
            reveal = f"🎤 المغني: {song['artist']}"
            
            # الانتقال للسؤال التالي
            self.current_round += 1
            if self.current_round >= self.rounds:
                return {
                    'points': 0,
                    'won': False,
                    'response': self.build_result_flex(
                        "انتهت اللعبة",
                        reveal,
                        0,
                        True
                    )
                }
            
            next_q = self.generate_question()
            return {
                'points': 0,
                'won': False,
                'response': next_q
            }
        
        # التحقق من الإجابة الصحيحة
        correct_normalized = self.normalize_text(self.current_answer)
        
        # مقارنة مع تحمل الأخطاء
        if (correct_normalized in normalized or 
            normalized in correct_normalized or 
            difflib.SequenceMatcher(None, normalized, correct_normalized).ratio() > 0.75):
            
            points = POINTS_PER_CORRECT
            self.add_player_score(uid, points)
            
            # الانتقال للسؤال التالي
            self.current_round += 1
            is_final = self.current_round >= self.rounds
            
            if is_final:
                return {
                    'points': points,
                    'won': True,
                    'response': self.build_result_flex(
                        name,
                        f"المغني: {self.current_answer}",
                        points,
                        True
                    )
                }
            
            next_q = self.generate_question()
            return {
                'points': points,
                'won': False,
                'response': next_q
            }
        
        return None
