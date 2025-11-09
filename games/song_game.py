import random
import re
from linebot.models import TextSendMessage

class SongGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.current_song = None
        self.correct_answer = None
        self.current_question = 1
        self.max_questions = 10
        self.players_scores = {}
        self.hint_used = False
        
        # قائمة الأغاني المحدثة
        self.songs = [
            {
                "lyrics": "أحبك ليه؟ أنا مدري ليه أهواك؟\nأنا مدري لو مرت علي ذكراك\nيفز النبض في صدري",
                "answer": "عبدالمجيد عبدالله",
                "song_name": "أحبك ليه"
            },
            {
                "lyrics": "سود العيون كبار والشامه حلوه\nشايل جمال الكون وباليني بلوه",
                "answer": "راشد الماجد",
                "song_name": "العيون السود"
            },
            {
                "lyrics": "لا تخاف من الزمان\nالزمان ماله أمان\nخف من اللي كل آمالك\nفي يديه وتامنه",
                "answer": "أصالة نصري",
                "song_name": "لا تخاف"
            },
            {
                "lyrics": "وين إنت ماهي مثلي\nوين إنت دايم\nوين إنت هالمرة على الفين\nوين إنت",
                "answer": "رابح صقر",
                "song_name": "وين إنت"
            },
            {
                "lyrics": "جنّنت قلبي بحبٍ يلوي ذراعي\nلاهو بتايب ولا عبّر تجاريبه\nأمر الله أقوى أحبك والعقل واعي",
                "answer": "ماجد المهندس",
                "song_name": "جننت قلبي"
            },
            {
                "lyrics": "سألوني الليل ليش ساهر\nقلت لهم القمر ساهر",
                "answer": "حسين الجسمي",
                "song_name": "سألوني الليل"
            },
            {
                "lyrics": "يا طير يا طاير يا رايح بلاد الخير\nسلم على الغالي وقل له أنا كثير",
                "answer": "عبدالمجيد عبدالله",
                "song_name": "يا طير"
            },
            {
                "lyrics": "تعبت وأنا أنادي على النوم\nوالنوم ماله خبر يجيني",
                "answer": "راشد الماجد",
                "song_name": "تعبت"
            },
            {
                "lyrics": "قولي وداعاً للجميع وتعالي\nقولي وداعاً واتركي اللي راح",
                "answer": "عبدالمجيد عبدالله",
                "song_name": "قولي وداعاً"
            },
            {
                "lyrics": "آه يا دنيا آه يا ناس\nجاني الحب يسأل عنك",
                "answer": "محمد عبده",
                "song_name": "آه يا دنيا"
            },
            {
                "lyrics": "حبيبي يا نور العين\nيا ساكن خيالي",
                "answer": "عمرو دياب",
                "song_name": "نور العين"
            },
            {
                "lyrics": "أنا عايش يا ناس معاه في الجنة\nوحياتي كلها فرحة وسعادة",
                "answer": "محمد منير",
                "song_name": "أنا عايش"
            },
            {
                "lyrics": "بكيت يوم فارقتني وبكيت\nدموعي سالت على خدي",
                "answer": "كاظم الساهر",
                "song_name": "بكيت"
            },
            {
                "lyrics": "أحبك موت موت\nوأموت فيك حبيبي",
                "answer": "ماجد المهندس",
                "song_name": "أحبك موت"
            },
            {
                "lyrics": "على مودك أنا جيت\nوعلى غلاك أنا جيت",
                "answer": "طلال مداح",
                "song_name": "على مودك"
            },
            {
                "lyrics": "سلملي عليها لو تشوفها يا ريح\nقلها حبيبها دايم يذكرها",
                "answer": "ماجد المهندس",
                "song_name": "سلملي عليها"
            },
            {
                "lyrics": "عيونه سود وحواجبه سود\nوشعره أسود أسود",
                "answer": "أصالة نصري",
                "song_name": "عيونه سود"
            },
            {
                "lyrics": "يا غالي على قلبي\nيا أغلى من روحي",
                "answer": "عبدالمجيد عبدالله",
                "song_name": "يا غالي"
            },
            {
                "lyrics": "تملي معاك يا جميل\nوالله تملي معاك",
                "answer": "عمرو دياب",
                "song_name": "تملي معاك"
            },
            {
                "lyrics": "بحبك يا صاحبي يا اللي معايا\nيا سندي في الدنيا",
                "answer": "تامر حسني",
                "song_name": "بحبك يا صاحبي"
            }
        ]
    
    def normalize_text(self, text):
        """تطبيع النص للمقارنة"""
        text = text.strip().lower()
        text = re.sub(r'^ال', '', text)
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ة', 'ه')
        text = text.replace('ى', 'ي')
        text = re.sub(r'[\u064B-\u065F]', '', text)
        return text
    
    def start_game(self):
        self.current_question = 1
        self.players_scores = {}
        return self.next_question()
    
    def next_question(self):
        """الانتقال للسؤال التالي"""
        if self.current_question > self.max_questions:
            return self.end_game()
        
        song_data = random.choice(self.songs)
        self.current_song = song_data
        self.correct_answer = song_data["answer"]
        self.hint_used = False
        
        return TextSendMessage(
            text=f"السؤال {self.current_question}/{self.max_questions}\n\n{song_data['lyrics']}\n\nخمن اسم المغني"
        )
    
    def get_hint(self):
        """الحصول على تلميح"""
        if self.hint_used:
            return TextSendMessage(text="تم استخدام التلميح مسبقاً")
        
        self.hint_used = True
        first_letter = self.correct_answer[0]
        hint = f"يبدأ بحرف: {first_letter}\nعدد الأحرف: {len(self.correct_answer)}"
        
        return TextSendMessage(text=f"تلميح:\n{hint}")
    
    def show_answer(self):
        """عرض الإجابة الصحيحة"""
        msg = f"الإجابة الصحيحة:\n{self.correct_answer}\nالأغنية: {self.current_song['song_name']}"
        
        self.current_question += 1
        
        if self.current_question <= self.max_questions:
            return self.next_question()
        else:
            return self.end_game()
    
    def end_game(self):
        """إنهاء اللعبة وعرض النتائج"""
        if not self.players_scores:
            return TextSendMessage(text="انتهت اللعبة\nلم يشارك أحد")
        
        # ترتيب اللاعبين
        sorted_players = sorted(self.players_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        msg = "النتائج النهائية\n\n"
        for i, (name, data) in enumerate(sorted_players[:5], 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"  {i}."
            msg += f"{emoji} {name}: {data['score']} نقطة\n"
        
        winner = sorted_players[0]
        msg += f"\nالفائز: {winner[0]}"
        
        return TextSendMessage(text=msg)
    
    def check_answer(self, answer, user_id, display_name):
        if not self.current_song:
            return None
        
        # التحقق من أوامر التلميح والإجابة
        if answer == 'لمح':
            return {
                'message': '',
                'points': 0,
                'game_over': False,
                'response': self.get_hint()
            }
        
        if answer == 'جاوب':
            return {
                'message': '',
                'points': 0,
                'game_over': self.current_question > self.max_questions,
                'response': self.show_answer()
            }
        
        user_answer = self.normalize_text(answer)
        correct_answer = self.normalize_text(self.correct_answer)
        
        # التحقق من الإجابة
        if user_answer in correct_answer or correct_answer in user_answer:
            points = 10 if not self.hint_used else 5
            
            # تسجيل النقاط
            if display_name not in self.players_scores:
                self.players_scores[display_name] = {'score': 0}
            self.players_scores[display_name]['score'] += points
            
            msg = f"صحيح يا {display_name}\n+{points} نقطة"
            
            self.current_question += 1
            
            if self.current_question <= self.max_questions:
                next_q = self.next_question()
                return {
                    'message': msg,
                    'points': points,
                    'won': True,
                    'game_over': False,
                    'response': TextSendMessage(text=f"{msg}\n\n{next_q.text}")
                }
            else:
                end_msg = self.end_game()
                return {
                    'message': msg,
                    'points': points,
                    'won': True,
                    'game_over': True,
                    'response': TextSendMessage(text=f"{msg}\n\n{end_msg.text}")
                }
        
        return None
