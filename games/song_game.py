"""لعبة الأغاني"""
‏from linebot.models import TextSendMessage
‏import random
‏import re

‏class SongGame:
‏    def __init__(self, line_bot_api):
‏        self.line_bot_api = line_bot_api
‏        self.current_song = None
‏        self.correct_answer = None
‏        self.current_question = 0
‏        self.max_questions = 5
‏        self.hint_used = False
        
        # قائمة الأغاني
‏        self.songs = [
            {
‏                "lyrics": "احبك ليه؟ انا مدري ليه اهواك؟\nانا مدري لو مرت علي ذكراك\nيفز النبض في صدري",
‏                "answer": "عبدالمجيد عبدالله",
‏                "song_name": "احبك ليه"
            },
            {
‏                "lyrics": "سود العيون كبار والشامه حلوه\nشايل جمال الكون وباليني بلوه",
‏                "answer": "راشد الماجد",
‏                "song_name": "العيون السود"
            },
            {
‏                "lyrics": "لا تخاف من الزمان\nالزمان ماله امان\nخف من اللي كل املك\nفي يديه وتامنه",
‏                "answer": "اصالة نصري",
‏                "song_name": "لا تخاف"
            },
            {
‏                "lyrics": "وين انت ماهي مثلي\nوين انت دايم\nوين انت هالمرة على الفين\nوين انت",
‏                "answer": "رابح صقر",
‏                "song_name": "وين انت"
            },
            {
‏                "lyrics": "جننت قلبي بحب يلوي ذراعي\nلاهو بتايب ولا عبر تجاريبه\nامر الله اقوى احبك والعقل واعي",
‏                "answer": "ماجد المهندس",
‏                "song_name": "جننت قلبي"
            },
            {
‏                "lyrics": "سألوني الليل ليش ساهر\nقلت لهم القمر ساهر",
‏                "answer": "حسين الجسمي",
‏                "song_name": "سألوني الليل"
            },
            {
‏                "lyrics": "يا طير يا طاير يا رايح بلاد الخير\nسلم على الغالي وقل له انا كثير",
‏                "answer": "عبدالمجيد عبدالله",
‏                "song_name": "يا طير"
            },
            {
‏                "lyrics": "تعبت وانا انادي على النوم\nوالنوم ماله خبر يجيني",
‏                "answer": "راشد الماجد",
‏                "song_name": "تعبت"
            },
            {
‏                "lyrics": "قولي وداعا للجميع وتعالي\nقولي وداعا واتركي اللي راح",
‏                "answer": "عبدالمجيد عبدالله",
‏                "song_name": "قولي وداعا"
            },
            {
‏                "lyrics": "اه يا دنيا اه يا ناس\nجاني الحب يسأل عنك",
‏                "answer": "محمد عبده",
‏                "song_name": "اه يا دنيا"
            },
            {
‏                "lyrics": "حبيبي يا نور العين\nيا ساكن خيالي",
‏                "answer": "عمرو دياب",
‏                "song_name": "نور العين"
            },
            {
‏                "lyrics": "انا عايش يا ناس معاه في الجنة\nوحياتي كلها فرحة وسعادة",
‏                "answer": "محمد منير",
‏                "song_name": "انا عايش"
            },
            {
‏                "lyrics": "بكيت يوم فارقتني وبكيت\nدموعي سالت على خدي",
‏                "answer": "كاظم الساهر",
‏                "song_name": "بكيت"
            },
            {
‏                "lyrics": "احبك موت موت\nواموت فيك حبيبي",
‏                "answer": "ماجد المهندس",
‏                "song_name": "احبك موت"
            },
            {
‏                "lyrics": "على مودك انا جيت\nوعلى غلاك انا جيت",
‏                "answer": "طلال مداح",
‏                "song_name": "على مودك"
            },
            {
‏                "lyrics": "سلملي عليها لو تشوفها يا ريح\nقلها حبيبها دايم يذكرها",
‏                "answer": "ماجد المهندس",
‏                "song_name": "سلملي عليها"
            },
            {
‏                "lyrics": "عيونه سود وحواجبه سود\nوشعره اسود اسود",
‏                "answer": "اصالة نصري",
‏                "song_name": "عيونه سود"
            },
            {
‏                "lyrics": "يا غالي على قلبي\nيا اغلى من روحي",
‏                "answer": "عبدالمجيد عبدالله",
‏                "song_name": "يا غالي"
            },
            {
‏                "lyrics": "تملي معاك يا جميل\nوالله تملي معاك",
‏                "answer": "عمرو دياب",
‏                "song_name": "تملي معاك"
            },
            {
‏                "lyrics": "بحبك يا صاحبي يا اللي معايا\nيا سندي في الدنيا",
‏                "answer": "تامر حسني",
‏                "song_name": "بحبك يا صاحبي"
            }
        ]
    
‏    def normalize_text(self, text):
        """تطبيع النص للمقارنة"""
‏        text = text.strip().lower()
‏        text = re.sub(r'^ال', '', text)
‏        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
‏        text = text.replace('ة', 'ه')
‏        text = text.replace('ى', 'ي')
‏        text = re.sub(r'[\u064B-\u065F]', '', text)
‏        return text
    
‏    def start_game(self):
        """بدء اللعبة"""
‏        self.current_question = 0
‏        return self.next_question()
    
‏    def next_question(self):
        """الانتقال للسؤال التالي"""
‏        song_data = random.choice(self.songs)
‏        self.current_song = song_data
‏        self.correct_answer = song_data["answer"]
‏        self.hint_used = False
        
‏        return TextSendMessage(
‏            text=f"السؤال {self.current_question + 1}/{self.max_questions}\n\n"
‏                 f"{song_data['lyrics']}\n\n"
‏                 f"خمن اسم المغني\n\n"
‏                 f"لمح - تلميح\n"
‏                 f"جاوب - لعرض الاجابة"
        )
    
‏    def check_answer(self, answer, user_id, display_name):
        """فحص الإجابة"""
‏        if not self.current_song:
‏            return None
        
‏        answer_normalized = answer.strip().lower()
        
        # أمر التلميح
‏        if answer_normalized in ['لمح', 'تلميح']:
‏            if self.hint_used:
‏                return {
‏                    'points': 0,
‏                    'won': False,
‏                    'response': TextSendMessage(text="تم استخدام التلميح مسبقا")
                }
            
‏            self.hint_used = True
‏            first_letter = self.correct_answer[0]
‏            hint = f"تلميح:\nيبدأ بحرف: {first_letter}\nعدد الاحرف: {len(self.correct_answer)}"
            
‏            return {
‏                'points': 0,
‏                'won': False,
‏                'response': TextSendMessage(text=hint)
            }
        
        # أمر عرض الإجابة
‏        if answer_normalized in ['جاوب', 'استسلم']:
‏            self.current_question += 1
            
‏            if self.current_question >= self.max_questions:
‏                return {
‏                    'points': 0,
‏                    'won': False,
‏                    'game_over': False,
‏                    'response': TextSendMessage(
‏                        text=f"الاجابة الصحيحة:\n{self.correct_answer}\n"
‏                             f"الاغنية: {self.current_song['song_name']}\n\n"
‏                             f"انتهت الاسئلة!"
                    )
                }
            
‏            next_q = self.next_question()
‏            return {
‏                'points': 0,
‏                'won': False,
‏                'response': TextSendMessage(
‏                    text=f"الاجابة الصحيحة:\n{self.correct_answer}\n"
‏                         f"الاغنية: {self.current_song['song_name']}\n\n{next_q.text}"
                )
            }
        
        # فحص الإجابة
‏        user_answer = self.normalize_text(answer)
‏        correct_answer = self.normalize_text(self.correct_answer)
        
‏        if user_answer in correct_answer or correct_answer in user_answer:
‏            points = 10 if not self.hint_used else 5
‏            self.current_question += 1
            
‏            if self.current_question >= self.max_questions:
‏                return {
‏                    'points': points,
‏                    'won': True,
‏                    'game_over': False,
‏                    'response': TextSendMessage(
‏                        text=f"ممتاز {display_name}!\n\nالنقاط: +{points}"
                    )
                }
            
‏            next_q = self.next_question()
‏            return {
‏                'points': points,
‏                'won': True,
‏                'response': TextSendMessage(
‏                    text=f"ممتاز {display_name}!\n\nالنقاط: +{points}\n\n{next_q.text}"
                )
            }
        
‏        return {
‏            'points': 0,
‏            'won': False,
‏            'response': TextSendMessage(text="خطأ! حاول مرة اخرى")
        }
