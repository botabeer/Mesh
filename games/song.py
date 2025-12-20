import random
from games.base import BaseGame
from config import Config


class SongGame(BaseGame):
    def __init__(self, db, theme="light"):
        super().__init__(db, theme)
        self.game_name = "اغنيه"
        self.supports_hint = True
        self.supports_reveal = True
        
        self.songs = [
            {"lyrics": "رجعت لي أيام الماضي معاك", "artist": "أم كلثوم"},
            {"lyrics": "قولي أحبك كي تزيد وسامتي", "artist": "كاظم الساهر"},
            {"lyrics": "بردان أنا تكفى أبي احترق بدفا لعيونك", "artist": "محمد عبده"},
            {"lyrics": "جلست والخوف بعينيها تتأمل فنجاني", "artist": "عبد الحليم حافظ"},
            {"lyrics": "أحبك موت كلمة مالها تفسير", "artist": "ماجد المهندس"},
            {"lyrics": "تملي معاك ولو حتى بعيد عني", "artist": "عمرو دياب"},
            {"lyrics": "رحت عني ما قويت جيت لك لاتردني", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "أنا لحبيبي وحبيبي إلي", "artist": "فيروز"},
            {"lyrics": "كيف أبيّن لك شعوري دون ما أحكي", "artist": "عايض"},
            {"lyrics": "خذني من ليلي لليلك", "artist": "عبادي الجوهر"},
            {"lyrics": "تدري كثر ماني من البعد مخنوق", "artist": "راشد الماجد"},
            {"lyrics": "اسخر لك غلا وتشوفني مقصر", "artist": "عايض"},
            {"lyrics": "أشوفك كل يوم وأروح وأقول نظرة ترد الروح", "artist": "محمد عبده"},
            {"lyrics": "منوتي ليتك معي", "artist": "محمد عبده"},
            {"lyrics": "جننت قلبي بحب يلوي ذراعي", "artist": "ماجد المهندس"},
            {"lyrics": "أحبك ليه أنا مدري", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "في زحمة الناس صعبة حالتي", "artist": "محمد عبده"},
            {"lyrics": "الحب يتعب من يدله والله في حبه بلاني", "artist": "راشد الماجد"},
            {"lyrics": "محد غيرك شغل عقلي شغل بالي", "artist": "وليد الشامي"},
            {"lyrics": "بديت أطيب بديت احس بك عادي", "artist": "ماجد المهندس"},
            {"lyrics": "احس اني لقيتك بس عشان تضيع مني", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "اختلفنا مين يحب الثاني أكثر", "artist": "محمد عبده"},
            {"lyrics": "من أول نظرة شفتك قلت هذا اللي تمنيته", "artist": "ماجد المهندس"},
            {"lyrics": "لبيه يا بو عيون وساع", "artist": "محمد عبده"},
            {"lyrics": "سألوني الناس عنك يا حبيبي", "artist": "فيروز"},
            {"lyrics": "أنا بلياك إذا أرمش تنزل ألف دمعة", "artist": "ماجد المهندس"},
            {"lyrics": "عطشان يا برق السما", "artist": "ماجد المهندس"},
            {"lyrics": "يراودني شعور إني أحبك أكثر من أول", "artist": "راشد الماجد"},
            {"lyrics": "أنا أكثر شخص بالدنيا يحبك", "artist": "راشد الماجد"},
            {"lyrics": "ليت العمر لو كان مليون مرة", "artist": "راشد الماجد"},
            {"lyrics": "تلمست لك عذر", "artist": "راشد الماجد"},
            {"lyrics": "عظيم إحساسي والشوق فيني", "artist": "راشد الماجد"},
            {"lyrics": "قال الوداع ومقصده يجرح القلب", "artist": "راشد الماجد"},
            {"lyrics": "حبيته بيني وبين نفسي", "artist": "شيرين"},
            {"lyrics": "اللي لقى احبابه نسى اصحابه", "artist": "راشد الماجد"},
            {"lyrics": "مقادير يا قلبي العنا مقادير", "artist": "طلال مداح"},
            {"lyrics": "ظلمتني والله قوي يجازيك", "artist": "طلال مداح"},
            {"lyrics": "كلمة ولو جبر خاطر", "artist": "عبادي الجوهر"},
            {"lyrics": "أنا لولا الغلا والمحبة", "artist": "فؤاد عبدالواحد"},
            {"lyrics": "أحبك لو تكون حاضر", "artist": "عبادي الجوهر"},
            {"lyrics": "ماعاد يمديني ولا عاد يمديك", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "يا بعدهم كلهم يا سراجي بينهم", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "حتى الكره احساس", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "استكثرك وقتي علي", "artist": "عبدالمجيد عبدالله"},
            {"lyrics": "ياما حاولت الفراق وما قويت", "artist": "عبدالمجيد عبدالله"}
        ]
        
        random.shuffle(self.songs)
        self.used = []

    def get_question(self):
        available = [s for s in self.songs if s not in self.used]
        if not available:
            self.used = []
            available = self.songs.copy()

        song = random.choice(available)
        self.used.append(song)
        self.current_answer = [song["artist"]]
        
        hint = "من المغني"
        return self.build_question_flex(song["lyrics"], hint)

    def check_answer(self, answer):
        normalized = Config.normalize(answer)
        return any(Config.normalize(a) == normalized for a in self.current_answer)
