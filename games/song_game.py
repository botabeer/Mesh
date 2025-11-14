from linebot.models import TextSendMessage
import random
import logging
from utils.helpers import normalize_text

logger = logging.getLogger(__name__)

class SongGame:
    def __init__(self, line_bot_api, use_ai=False, get_api_key=None, switch_key=None):
        self.line_bot_api = line_bot_api
        self.use_ai = use_ai
        self.get_api_key = get_api_key
        self.switch_key = switch_key
        
        self.current_song = None
        self.current_artist = None
        self.hint_count = 0
        
        # قاعدة بيانات الأغاني (مقطع + المغني)
        self.songs_database = [
            {
                "lyrics": "يا ليل يا عين\nيا ليلي يا ليلي يا عيني\nيا ليلي يا ليلي يا عيني",
                "artist": "ام كلثوم",
                "song_name": "يا ليل يا عين"
            },
            {
                "lyrics": "على بالي\nوالله على بالي\nمن يوم فراقك يا عمري على بالي",
                "artist": "عبد الحليم حافظ",
                "song_name": "على بالي"
            },
            {
                "lyrics": "اه يا اسمراني اللون\nيا واخد العقل والجنون\nانت اللي فؤادي باعته",
                "artist": "محمد عبده",
                "song_name": "اه يا اسمراني"
            },
            {
                "lyrics": "تعالى اقولك\nاللي بقالي سنين عايز اقولك\nبحبك وعمري ما قولت قبل كده لحد",
                "artist": "عمرو دياب",
                "song_name": "تعالى اقولك"
            },
            {
                "lyrics": "حبيبي يا نور العين\nيا ساكن خيالي\nحبيتك من سنين وانا في دنيا الاطفال",
                "artist": "عمرو دياب",
                "song_name": "نور العين"
            },
            {
                "lyrics": "قولي وانا اسمع\nانا كل اللي تأمره باسمع\nانتي اللي بتملي حياتي",
                "artist": "محمد عبده",
                "song_name": "قولي وانا اسمع"
            },
            {
                "lyrics": "انت عمري\nاللي ابتدا بنورك صباحه\nد كان زماني راح ومش حسابه",
                "artist": "ام كلثوم",
                "song_name": "انت عمري"
            },
            {
                "lyrics": "وياك\nكل الدنيا معاك\nانا ارتاحلك انا وياك",
                "artist": "راشد الماجد",
                "song_name": "وياك"
            },
            {
                "lyrics": "بتونس بيك\nكل يوم بتونس بيك\nقلبي اللي كان ميال بيك اتعدل",
                "artist": "تامر حسني",
                "song_name": "بتونس بيك"
            },
            {
                "lyrics": "ادلعك\nاه لو ادلعك\nياما احكي عيوني ليك",
                "artist": "حسين الجسمي",
                "song_name": "ادلعك"
            },
            {
                "lyrics": "ست الحبايب\nيا ام الضفاير السودا\nالحلوة اللي ما لاقيت زيها ابدا",
                "artist": "عبد الحليم حافظ",
                "song_name": "ست الحبايب"
            },
            {
                "lyrics": "كده كده\nانا معاك كده كده\nمش فارقه معايا الدنيا",
                "artist": "حسام حبيب",
                "song_name": "كده كده"
            }
        ]
    
    def start_game(self):
        """بدء اللعبة"""
        try:
            if self.use_ai:
                # استخدام AI لتوليد سؤال
                return self._generate_ai_question()
            else:
                # اختيار أغنية عشوائية
                song = random.choice(self.songs_database)
                self.current_song = song["song_name"]
                self.current_artist = normalize_text(song["artist"])
                self.hint_count = 0
                
                message = f"🎵 خمّن المغني:\n\n{song['lyrics']}\n\n▪️ من هو المغني؟"
                
                return TextSendMessage(text=message)
                
        except Exception as e:
            logger.error(f"❌ خطأ في بدء لعبة الأغاني: {e}", exc_info=True)
            return TextSendMessage(text="❌ حدث خطأ في بدء اللعبة")
    
    def _generate_ai_question(self):
        """توليد سؤال باستخدام AI"""
        try:
            import google.generativeai as genai
            
            api_key = self.get_api_key()
            if not api_key:
                logger.warning("⚠️ لا يوجد مفتاح API متاح، التحويل للوضع اليدوي")
                return self.start_game()  # العودة للوضع اليدوي
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = """أنت مولد أسئلة أغاني عربية.

اختر أغنية عربية مشهورة وأعطني:
1. مقطع من كلمات الأغنية (3-4 أسطر)
2. اسم المغني

الإجابة يجب أن تكون بالشكل التالي فقط:
LYRICS: [كلمات الأغنية]
ARTIST: [اسم المغني]

مثال:
LYRICS: على بالي\\nوالله على بالي\\nمن يوم فراقك يا عمري على بالي
ARTIST: عبد الحليم حافظ"""

            response = model.generate_content(prompt)
            result_text = response.text.strip()
            
            # استخراج البيانات
            lyrics = ""
            artist = ""
            
            for line in result_text.split('\n'):
                if line.startswith('LYRICS:'):
                    lyrics = line.replace('LYRICS:', '').strip()
                elif line.startswith('ARTIST:'):
                    artist = line.replace('ARTIST:', '').strip()
            
            if lyrics and artist:
                self.current_artist = normalize_text(artist)
                self.hint_count = 0
                
                message = f"🎵 خمّن المغني:\n\n{lyrics}\n\n▪️ من هو المغني؟"
                return TextSendMessage(text=message)
            else:
                raise Exception("فشل استخراج البيانات من AI")
                
        except Exception as e:
            logger.error(f"❌ خطأ في AI: {e}")
            if self.switch_key:
                self.switch_key()
                return self._generate_ai_question()
            else:
                # العودة للوضع اليدوي
                return self.start_game()
    
    def check_answer(self, answer, user_id, display_name):
        """فحص الإجابة"""
        answer_normalized = normalize_text(answer)
        
        if answer_normalized == self.current_artist:
            points = max(10 - (self.hint_count * 3), 1)
            
            return {
                'points': points,
                'won': True,
                'response': TextSendMessage(
                    text=f"✅ إجابة صحيحة يا {display_name}!\n\n▪️ المغني: {self.current_artist}\n▪️ نقاطك: {points}"
                )
            }
        
        return None
    
    def get_hint(self):
        """الحصول على تلميح"""
        self.hint_count += 1
        
        artist_letters = list(self.current_artist)
        word_count = len(self.current_artist.split())
        letter_count = len(self.current_artist.replace(' ', ''))
        
        if self.hint_count == 1:
            return f"💡 تلميح 1:\n\n▪️ الحرف الأول: {artist_letters[0]}\n▪️ عدد الحروف: {letter_count}"
        elif self.hint_count == 2:
            return f"💡 تلميح 2:\n\n▪️ عدد الكلمات: {word_count}\n▪️ الأحرف الأولى: {' '.join([word[0] for word in self.current_artist.split()])}"
        else:
            half = len(self.current_artist) // 2
            revealed = self.current_artist[:half] + ('_' * (len(self.current_artist) - half))
            return f"💡 تلميح 3:\n\n▪️ نصف الاسم: {revealed}"
    
    def reveal_answer(self):
        """الكشف عن الإجابة"""
        return f"▫️ الإجابة الصحيحة:\n\nالمغني: {self.current_artist}"
