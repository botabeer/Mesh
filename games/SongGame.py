import random
from games.base import BaseGame
from config import Config


class SongGame(BaseGame):
    """لعبة تخمين المغني من كلمات الأغنية"""
    
    def __init__(self, db, theme: str = "light"):
        super().__init__(db, theme)
        
        # قاعدة بيانات الأغاني
        self.songs = [
            {"lyrics": "رجعت لي ايام الماضي معاك", "artist": "ام كلثوم"},
            {"lyrics": "قولي احبك كي تزيد وسامتي", "artist": "كاظم الساهر"},
            {"lyrics": "بردان انا تكفى ابي احترق بدفا لعيونك", "artist": "محمد عبده"},
            {"lyrics": "جلست والخوف بعينيها تتامل فنجاني", "artist": "عبد الحليم حافظ"},
            {"lyrics": "احبك موت كلمة مالها تفسير", "artist": "ماجد المهندس"},
            {"lyrics": "تملي معاك ولو حتى بعيد عني", "artist": "عمرو دياب"},
            {"lyrics": "رحت عني ما قويت جيت لك لاتردني", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "على بالي حبيبي دايما في خاطري", "artist": "محمد عبده"},
            {"lyrics": "يا طير يا طاير في وسط السما", "artist": "محمد عبده"},
            {"lyrics": "عيونك يا حبيبي شمس وهوا", "artist": "وردة الجزائرية"},
            {"lyrics": "قلبي اشتاق لك وحن", "artist": "راشد الماجد"},
            {"lyrics": "ليه يا قلبي اخترت الصعب", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "حبيتك بالتلاتين والتلاتا", "artist": "شيرين عبد الوهاب"},
            {"lyrics": "انا مشتاق ومحتاج لحنانك", "artist": "وائل كفوري"},
            {"lyrics": "خليك حبيبي خليك معايا", "artist": "تامر حسني"}
        ]
        
        random.shuffle(self.songs)
        self.used = []

    def get_question(self):
        """عرض كلمات الأغنية"""
        # اختيار أغنية لم تُستخدم
        available = [s for s in self.songs if s not in self.used]
        if not available:
            self.used = []
            available = self.songs.copy()

        song = random.choice(available)
        self.used.append(song)
        
        # حفظ إجابات محتملة (قد يكون للفنان أسماء مختلفة)
        self.current_answer = [song["artist"]]
        
        hint = f"السؤال {self.current_q + 1}/{self.total_q} - من المغني؟"
        
        return self.build_question_flex(song["lyrics"], hint)

    def check_answer(self, answer: str) -> bool:
        """التحقق من اسم المغني"""
        normalized = Config.normalize(answer)
        
        # التحقق من تطابق الاسم
        return any(
            Config.normalize(a) == normalized 
            for a in self.current_answer
        )
