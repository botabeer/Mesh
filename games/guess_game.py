‏import random
from linebot.models import TextSendMessage
from utils.helpers import normalize_text

class SongGame:
    def __init__(self, line_bot_api, use_ai=False, get_api_key=None, switch_key=None):
        self.line_bot_api = line_bot_api
        self.use_ai = use_ai
        self.get_api_key = get_api_key
        self.switch_key = switch_key
        self.current_song = None
        self.current_artist = None
        self.hint_used = False
        
        # قائمة الأغاني
        self.songs_db = [
            {"lyrics": "آه من الهوى ما أقساه\nآه من زمان اللي كان", "artist": "عبد الحليم حافظ"},
            {"lyrics": "على بالي حبيبي وأنا ماشي في الشوارع\nمشتاق لعنيه", "artist": "فيروز"},
            {"lyrics": "تعالى أسألك أنا يا هوى\nمين اللي باعني", "artist": "أم كلثوم"},
            {"lyrics": "بحبك وحشتيني\nمن زمان والله ما شفتك", "artist": "عمرو دياب"},
            {"lyrics": "كل يوم من ده\nوالله العظيم خلاص سئمت", "artist": "محمد عبده"},
            {"lyrics": "يا طير يا طاير فوق\nودي سلامي للحبايب", "artist": "طلال مداح"},
            {"lyrics": "أنا قلبي دليلي\nوأنا قلبي عليل", "artist": "وردة الجزائرية"},
            {"lyrics": "من أول ما شفتك\nوأنا حاسس بحاجة", "artist": "تامر حسني"},
            {"lyrics": "قولي يا عيني\nليه البعد يا عيني", "artist": "راشد الماجد"},
            {"lyrics": "كل ده كان ليه\nكل الحب ده كان ليه", "artist": "شيرين عبد الوهاب"}
        ]
    
    # ---------------------------- بدء اللعبة ---------------------------- #
    def start_game(self):
        if self.use_ai and self.get_api_key:
            return self._generate_ai_song()
        return self._generate_manual_song()
    
    # ---------------------------- توليد سؤال يدوي ---------------------------- #
    def _generate_manual_song(self):
        song = random.choice(self.songs_db)
        self.current_song = song["lyrics"]
        self.current_artist = song["artist"]
        self.hint_used = False
        
        text = (
            "🎵 خمن المغني\n\n"
            f"{self.current_song}\n\n"
            "━━━━━━━━━━━━━━\n"
            "من المغني؟"
        )
        
        return TextSendMessage(text=text)
    
    # ---------------------------- توليد سؤال باستخدام AI ---------------------------- #
    def _generate_ai_song(self):
        try:
            import google.generativeai as genai
            
            api_key = self.get_api_key()
            if not api_key:
                return self._generate_manual_song()
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-pro")
            
            prompt = (
                "أعطني مقطع من أغنية عربية مشهورة (سطرين فقط) مع اسم المغني.\n\n"
                "الصيغة:\n"
                "LYRICS: [مقطع الأغنية]\n"
                "ARTIST: [اسم المغني]"
            )
            
            response = model.generate_content(prompt)
            result = response.text.strip()
            
            lyrics_line = [l for l in result.split("\n") if "LYRICS:" in l]
            artist_line = [l for l in result.split("\n") if "ARTIST:" in l]
            
            if lyrics_line and artist_line:
                self.current_song = lyrics_line[0].replace("LYRICS:", "").strip()
                self.current_artist = artist_line[0].replace("ARTIST:", "").strip()
                self.hint_used = False
                
                text = (
                    "🎵 خمن المغني\n\n"
                    f"{self.current_song}\n\n"
                    "━━━━━━━━━━━━━━\n"
                    "من المغني؟"
                )
                return TextSendMessage(text=text)
            
            return self._generate_manual_song()
        
        except Exception as e:
            print(f"AI Error: {e}")
            if self.switch_key:
                self.switch_key()
            return self._generate_manual_song()
    
    # ---------------------------- فحص الإجابة ---------------------------- #
    def check_answer(self, answer, user_id, display_name):
        if not self.current_artist:
            return None
        
        normalized_answer = normalize_text(answer)
        normalized_artist = normalize_text(self.current_artist)
        
        if normalized_answer in normalized_artist or normalized_artist in normalized_answer:
            points = 5 if self.hint_used else 10
            
            new_q = self.start_game()
            message = (
                f"✓ إجابة صحيحة يا {display_name}\n\n"
                f"المغني: {self.current_artist}\n"
                f"+{points} نقطة\n\n"
                f"{new_q.text}"
            )
            
            return {
                "points": points,
                "won": True,
                "message": message,
                "response": TextSendMessage(text=message),
                "game_over": False
            }
        
        return None
    
    # ---------------------------- التلميح ---------------------------- #
    def get_hint(self):
        if not self.current_artist:
            return "لا يوجد سؤال حالي"
        
        self.hint_used = True
        
        first_letter = self.current_artist[0]
        words = len(self.current_artist.split())
        letters = len(self.current_artist.replace(" ", ""))
        
        return (
            "💡 التلميح\n\n"
            f"أول حرف: {first_letter}\n"
            f"عدد الكلمات: {words}\n"
            f"عدد الحروف: {letters}\n\n"
            "⚠️ سيتم خصم 5 نقاط"
        )
    
    # ---------------------------- كشف الإجابة ---------------------------- #
    def reveal_answer(self):
        if not self.current_artist:
            return "لا يوجد سؤال حالي"
        
        answer = self.current_artist
        self.current_artist = None
        self.current_song = None
        
        return f"الإجابة الصحيحة:\n{answer}"
