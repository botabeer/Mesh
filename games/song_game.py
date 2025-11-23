"""
لعبة تخمين الأغنية - النسخة النهائية مع تلميحات AI-like
Created by: Abeer Aldosari © 2025
"""
from linebot.models import TextSendMessage, FlexSendMessage
from .base_game import BaseGame
import random
import difflib

class SongGame(BaseGame):
    """لعبة تخمين المغني من كلمات الأغنية مع تلميحات محسنة"""
    
    def __init__(self, line_bot_api, theme="blue"):
        super().__init__(line_bot_api, questions_count=5)
        self.theme = theme
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
            {'lyrics': 'بردان أنا تكفى أبي احترق بدفا لعيونك', 'artist': 'محمد عبده'},
            {'lyrics': 'أشوفك كل يوم وأروح وأقول نظرة ترد الروح', 'artist': 'محمد عبده'},
            {'lyrics': 'في زحمة الناس صعبة حالتي', 'artist': 'محمد عبده'},
            {'lyrics': 'اختلفنا مين يحب الثاني أكثر', 'artist': 'محمد عبده'},
            {'lyrics': 'لبيه يا بو عيون وساع', 'artist': 'محمد عبده'},
            {'lyrics': 'اسمحيلي يا الغرام العف', 'artist': 'محمد عبده'},
            {'lyrics': 'سألوني الناس عنك يا حبيبي', 'artist': 'فيروز'},
            {'lyrics': 'أنا لحبيبي وحبيبي إلي', 'artist': 'فيروز'},
            {'lyrics': 'أحبك موت كلمة مالها تفسير', 'artist': 'ماجد المهندس'},
            {'lyrics': 'جننت قلبي بحب يلوي ذراعي', 'artist': 'ماجد المهندس'},
            {'lyrics': 'بديت أطيب بديت احس بك عادي', 'artist': 'ماجد المهندس'},
            {'lyrics': 'من أول نظرة شفتك قلت هذا اللي تمنيته', 'artist': 'ماجد المهندس'},
            {'lyrics': 'أنا بلياك إذا أرمش تنزل ألف دمعة', 'artist': 'ماجد المهندس'},
            {'lyrics': 'عطشان يا برق السما', 'artist': 'ماجد المهندس'},
            {'lyrics': 'هيجيلي موجوع دموعه ف عينه', 'artist': 'تامر عاشور'},
            {'lyrics': 'تيجي نتراهن إن هيجي اليوم', 'artist': 'تامر عاشور'},
            {'lyrics': 'خليني ف حضنك يا حبيبي', 'artist': 'تامر عاشور'},
            {'lyrics': 'أريد الله يسامحني لأن أذيت نفسي', 'artist': 'رحمة رياض'},
            {'lyrics': 'كون نصير أنا وياك نجمة بالسما', 'artist': 'رحمة رياض'},
            {'lyrics': 'على طاري الزعل والدمعتين', 'artist': 'أصيل هميم'},
            {'lyrics': 'يشبهك قلبي كنك القلب مخلوق', 'artist': 'أصيل هميم'},
            {'lyrics': 'أحبه بس مو معناه اسمحله يجرح', 'artist': 'أصيل هميم'},
            {'lyrics': 'المفروض أعوفك من زمان', 'artist': 'أصيل هميم'},
            {'lyrics': 'ضعت منك وانهدم جسر التلاقي', 'artist': 'أميمة طالب'},
            {'lyrics': 'بيان صادر من معاناة المحبة', 'artist': 'أميمة طالب'},
            {'lyrics': 'أنا ودي إذا ودك نعيد الماضي', 'artist': 'رابح صقر'},
            {'lyrics': 'مثل ما تحب ياروحي ألبي رغبتك', 'artist': 'رابح صقر'},
            {'lyrics': 'كل ما بلل مطر وصلك ثيابي', 'artist': 'رابح صقر'},
            {'lyrics': 'يراودني شعور إني أحبك أكثر من أول', 'artist': 'راشد الماجد'},
            {'lyrics': 'أنا أكثر شخص بالدنيا يحبك', 'artist': 'راشد الماجد'},
            {'lyrics': 'ليت العمر لو كان مليون مرة', 'artist': 'راشد الماجد'},
            {'lyrics': 'تلمست لك عذر', 'artist': 'راشد الماجد'},
            {'lyrics': 'عظيم إحساسي والشوق فيني', 'artist': 'راشد الماجد'},
            {'lyrics': 'خذ راحتك ماعاد تفرق معي', 'artist': 'راشد الماجد'},
            {'lyrics': 'قال الوداع ومقصده يجرح القلب', 'artist': 'راشد الماجد'},
            {'lyrics': 'اللي لقى احبابه نسى اصحابه', 'artist': 'راشد الماجد'},
            {'lyrics': 'واسع خيالك اكتبه أنا بكذبك معجبه', 'artist': 'شمة حمدان'},
            {'lyrics': 'ما دريت إني أحبك ما دريت', 'artist': 'شمة حمدان'},
            {'lyrics': 'حبيته بيني وبين نفسي', 'artist': 'شيرين'},
            {'lyrics': 'كلها غيرانة بتحقد', 'artist': 'شيرين'},
            {'lyrics': 'مشاعر تشاور تودع تسافر', 'artist': 'شيرين'},
            {'lyrics': 'أنا مش بتاعت الكلام ده', 'artist': 'شيرين'},
            {'lyrics': 'مقادير يا قلبي العنا مقادير', 'artist': 'طلال مداح'},
            {'lyrics': 'ظلمتني والله قوي يجازيك', 'artist': 'طلال مداح'},
            {'lyrics': 'فزيت من نومي أناديلك', 'artist': 'ذكرى'},
            {'lyrics': 'ابد على حطة يدك', 'artist': 'ذكرى'},
            {'lyrics': 'أنا لولا الغلا والمحبة', 'artist': 'فؤاد عبدالواحد'},
            {'lyrics': 'كلمة ولو جبر خاطر', 'artist': 'عبادي الجوهر'},
            {'lyrics': 'أحبك لو تكون حاضر', 'artist': 'عبادي الجوهر'},
            {'lyrics': 'إلحق عيني إلحق', 'artist': 'وليد الشامي'},
            {'lyrics': 'يردون قلت لازم يردون', 'artist': 'وليد الشامي'},
            {'lyrics': 'ولهان أنا ولهان', 'artist': 'وليد الشامي'},
            {'lyrics': 'اقولها كبر عن الدنيا حبيبي', 'artist': 'وليد الشامي'},
            {'lyrics': 'أنا استاهل وداع أفضل وداع', 'artist': 'نوال الكويتية'},
            {'lyrics': 'لقيت روحي بعد ما لقيتك', 'artist': 'نوال الكويتية'},
            {'lyrics': 'غريبة الناس غريبة الدنيا', 'artist': 'وائل جسار'},
            {'lyrics': 'اعذريني يوم زفافك', 'artist': 'وائل جسار'},
            {'lyrics': 'ماعاد يمديني ولا عاد يمديك', 'artist': 'عبدالمجيد عبدالله'},
            {'lyrics': 'يا بعدهم كلهم يا سراجي بينهم', 'artist': 'عبدالمجيد عبدالله'},
            {'lyrics': 'حتى الكره احساس', 'artist': 'عبدالمجيد عبدالله'},
            {'lyrics': 'استكثرك وقتي علي', 'artist': 'عبدالمجيد عبدالله'},
            {'lyrics': 'ياما حاولت الفراق وما قويت', 'artist': 'عبدالمجيد عبدالله'}
        ]
        random.shuffle(self.songs)

    def _get_colors(self):
        themes = {
            "blue": {"bg": "#0C1929", "card": "#0F2744", "accent": "#00D9FF", "text": "#E0F2FE", "text2": "#7DD3FC", "button": "#1E3A5F"},
            "red": {"bg": "#290C0C", "card": "#440F0F", "accent": "#FF0000", "text": "#FFE0E0", "text2": "#FC7D7D", "button": "#5F1E1E"},
            "green": {"bg": "#0C290C", "card": "#0F440F", "accent": "#00FF00", "text": "#E0FFE0", "text2": "#7DFC7D", "button": "#1E5F1E"}
        }
        return themes.get(self.theme, themes["blue"])

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        return self.get_question()
    
    def get_question(self):
        song = self.songs[self.current_question % len(self.songs)]
        self.current_answer = song["artist"]
        colors = self._get_colors()
        progress = self.current_question + 1

        flex_content = {
            "type": "bubble",
            "size": "kilo",
            "styles": {"body": {"backgroundColor": colors["bg"]}},
            "header": {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "🎵", "size": "xl", "align": "center"}],
                     "backgroundColor": colors["text"], "cornerRadius": "25px", "width": "45px", "height": "45px", "justifyContent": "center"},
                    {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": "لعبة الأغنية", "size": "xl", "weight": "bold", "color": colors["text"]},
                        {"type": "text", "text": f"السؤال {progress}/{self.questions_count}", "size": "sm", "color": colors["text2"]}
                    ], "margin": "lg", "flex": 1}
                ],
                "backgroundColor": colors["accent"], "paddingAll": "15px"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "box", "layout": "vertical", "contents": [
                        {"type": "text", "text": song["lyrics"], "size": "lg", "weight": "bold", "color": colors["text"], "align": "center", "wrap": True}
                    ], "backgroundColor": colors["card"], "cornerRadius": "15px", "paddingAll": "25px", "margin": "lg"},
                    {"type": "text", "text": "من المغني؟", "size": "md", "color": colors["accent"], "align": "center", "margin": "xl"},
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "box", "layout": "vertical", "contents": [], "backgroundColor": colors["accent"], "height": "5px", "flex": progress},
                        {"type": "box", "layout": "vertical", "contents": [], "backgroundColor": colors["card"], "height": "5px", "flex": self.questions_count - progress}
                    ], "cornerRadius": "3px", "margin": "md"},
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "button", "action": {"type": "message", "label": "💡 لمح", "text": "لمح"}, "style": "secondary", "color": colors["button"], "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "جاوب", "text": "جاوب"}, "style": "primary", "color": colors["accent"], "height": "sm"}
                    ], "spacing": "md", "margin": "xl"}
                ], "backgroundColor": colors["bg"], "paddingAll": "15px"
            }
        }
        return FlexSendMessage(alt_text="لعبة الأغنية", contents=flex_content)

    def get_hint(self):
        song = self.songs[self.current_question % len(self.songs)]
        artist = song["artist"].strip()
        first_char = artist[0]
        length = len(artist)
        return f"💡 تلميح: أول حرف '{first_char}' وعدد الحروف {length}"

    def check_answer(self, user_answer, user_id, display_name):
        if not self.game_active: return None
        if user_id in self.answered_users: return None

        answer = user_answer.strip()
        if answer == 'لمح':
            hint = self.get_hint()
            return {'message': hint, 'response': TextSendMessage(text=hint), 'points': 0}
        if answer == 'جاوب':
            song = self.songs[self.current_question % len(self.songs)]
            reveal = f"🎤 المغني: {song['artist']}\n🎵 الأغنية: {song.get('title','غير معروف')}"
            next_q = self.next_question()
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['message'] = f"{reveal}\n\n{next_q.get('message','')}"
                return next_q
            return {'message': reveal, 'response': next_q, 'points': 0}

        normalized = self.normalize_text(answer)
        correct = self.normalize_text(self.current_answer)
        if correct in normalized or normalized in correct or difflib.SequenceMatcher(None, normalized, correct).ratio() > 0.8:
            points = self.add_score(user_id, display_name, 10)
            song = self.songs[self.current_question % len(self.songs)]
            next_q = self.next_question()
            if isinstance(next_q, dict) and next_q.get('game_over'):
                next_q['points'] = points
                return next_q
            msg = f"✅ صحيح يا {display_name}!\n🎤 {song['artist']}\n🎵 {song.get('title','غير معروف')}\n+{points} نقطة"
            return {'message': msg, 'response': next_q, 'points': points}

        return {'message': "▫️ إجابة غير صحيحة ▪️", 'response': TextSendMessage(text="▫️ إجابة غير صحيحة ▪️"), 'points': 0}
