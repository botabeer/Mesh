"""
لعبة تخمين الأغنية - ستايل زجاجي احترافي
Created by: Abeer Aldosari © 2025
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional


class SongGame(BaseGame):
    """لعبة تخمين الأغنية"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=5)
        self.game_name = "أغنية"
        self.game_icon = "🎵"

        # ✅ تم دمج جميع الأغاني هنا بدون حذف أي شيء
        self.songs = [
{'lyrics':'رجعت لي أيام الماضي معاك','artist':'أم كلثوم'},
{'lyrics':'جلست والخوف بعينيها تتأمل فنجاني','artist':'عبد الحليم حافظ'},
{'lyrics':'تملي معاك ولو حتى بعيد عني','artist':'عمرو دياب'},
{'lyrics':'يا بنات يا بنات','artist':'نانسي عجرم'},
{'lyrics':'قولي أحبك كي تزيد وسامتي','artist':'كاظم الساهر'},
{'lyrics':'أنا لحبيبي وحبيبي إلي','artist':'فيروز'},
{'lyrics':'حبيبي يا كل الحياة اوعدني تبقى معايا','artist':'تامر حسني'},
{'lyrics':'قلبي بيسألني عنك دخلك طمني وينك','artist':'وائل كفوري'},
{'lyrics':'كيف أبيّن لك شعوري دون ما أحكي','artist':'عايض'},
{'lyrics':'اسخر لك غلا وتشوفني مقصر','artist':'عايض'},
{'lyrics':'رحت عني ما قويت جيت لك لاتردني','artist':'عبدالمجيد عبدالله'},
{'lyrics':'خذني من ليلي لليلك','artist':'عبادي الجوهر'},
{'lyrics':'تدري كثر ماني من البعد مخنوق','artist':'راشد الماجد'},
{'lyrics':'انسى هالعالم ولو هم يزعلون','artist':'عباس ابراهيم'},
{'lyrics':'أنا عندي قلب واحد','artist':'حسين الجسمي'},
{'lyrics':'منوتي ليتك معي','artist':'محمد عبده'},
{'lyrics':'خلنا مني طمني عليك','artist':'نوال الكويتية'},
{'lyrics':'أحبك ليه أنا مدري','artist':'عبدالمجيد عبدالله'},
{'lyrics':'أمر الله أقوى أحبك والعقل واعي','artist':'ماجد المهندس'},
{'lyrics':'الحب يتعب من يدله والله في حبه بلاني','artist':'راشد الماجد'},
{'lyrics':'محد غيرك شغل عقلي شغل بالي','artist':'وليد الشامي'},
{'lyrics':'نكتشف مر الحقيقة بعد ما يفوت الأوان','artist':'أصالة'},
{'lyrics':'يا هي توجع كذبة اخباري تمام','artist':'أميمة طالب'},
{'lyrics':'احس اني لقيتك بس عشان تضيع مني','artist':'عبدالمجيد عبدالله'},
{'lyrics':'بردان أنا تكفى أبي احترق بدفا لعيونك','artist':'محمد عبده'},
{'lyrics':'أشوفك كل يوم وأروح وأقول نظرة ترد الروح','artist':'محمد عبده'},
{'lyrics':'في زحمة الناس صعبة حالتي','artist':'محمد عبده'},
{'lyrics':'اختلفنا مين يحب الثاني أكثر','artist':'محمد عبده'},
{'lyrics':'لبيه يا بو عيون وساع','artist':'محمد عبده'},
{'lyrics':'اسمحيلي يا الغرام العف','artist':'محمد عبده'},
{'lyrics':'سألوني الناس عنك يا حبيبي','artist':'فيروز'},
{'lyrics':'أنا لحبيبي وحبيبي إلي','artist':'فيروز'},
{'lyrics':'أحبك موت كلمة مالها تفسير','artist':'ماجد المهندس'},
{'lyrics':'جننت قلبي بحب يلوي ذراعي','artist':'ماجد المهندس'},
{'lyrics':'بديت أطيب بديت احس بك عادي','artist':'ماجد المهندس'},
{'lyrics':'من أول نظرة شفتك قلت هذا اللي تمنيته','artist':'ماجد المهندس'},
{'lyrics':'أنا بلياك إذا أرمش تنزل ألف دمعة','artist':'ماجد المهندس'},
{'lyrics':'عطشان يا برق السما','artist':'ماجد المهندس'},
{'lyrics':'هيجيلي موجوع دموعه ف عينه','artist':'تامر عاشور'},
{'lyrics':'تيجي نتراهن إن هيجي اليوم','artist':'تامر عاشور'},
{'lyrics':'خليني ف حضنك يا حبيبي','artist':'تامر عاشور'},
{'lyrics':'أريد الله يسامحني لأن أذيت نفسي','artist':'رحمة رياض'},
{'lyrics':'كون نصير أنا وياك نجمة بالسما','artist':'رحمة رياض'},
{'lyrics':'على طاري الزعل والدمعتين','artist':'أصيل هميم'},
{'lyrics':'يشبهك قلبي كنك القلب مخلوق','artist':'أصيل هميم'},
{'lyrics':'أحبه بس مو معناه اسمحله يجرح','artist':'أصيل هميم'},
{'lyrics':'المفروض أعوفك من زمان','artist':'أصيل هميم'},
{'lyrics':'ضعت منك وانهدم جسر التلاقي','artist':'أميمة طالب'},
{'lyrics':'بيان صادر من معاناة المحبة','artist':'أميمة طالب'},
{'lyrics':'أنا ودي إذا ودك نعيد الماضي','artist':'رابح صقر'},
{'lyrics':'مثل ما تحب ياروحي ألبي رغبتك','artist':'رابح صقر'},
{'lyrics':'كل ما بلل مطر وصلك ثيابي','artist':'رابح صقر'},
{'lyrics':'يراودني شعور إني أحبك أكثر من أول','artist':'راشد الماجد'},
{'lyrics':'أنا أكثر شخص بالدنيا يحبك','artist':'راشد الماجد'},
{'lyrics':'ليت العمر لو كان مليون مرة','artist':'راشد الماجد'},
{'lyrics':'تلمست لك عذر','artist':'راشد الماجد'},
{'lyrics':'عظيم إحساسي والشوق فيني','artist':'راشد الماجد'},
{'lyrics':'خذ راحتك ماعاد تفرق معي','artist':'راشد الماجد'},
{'lyrics':'قال الوداع ومقصده يجرح القلب','artist':'راشد الماجد'},
{'lyrics':'اللي لقى احبابه نسى اصحابه','artist':'راشد الماجد'},
{'lyrics':'واسع خيالك اكتبه أنا بكذبك معجبه','artist':'شمة حمدان'},
{'lyrics':'ما دريت إني أحبك ما دريت','artist':'شمة حمدان'},
{'lyrics':'حبيته بيني وبين نفسي','artist':'شيرين'},
{'lyrics':'كلها غيرانة بتحقد','artist':'شيرين'},
{'lyrics':'مشاعر تشاور تودع تسافر','artist':'شيرين'},
{'lyrics':'أنا مش بتاعت الكلام ده','artist':'شيرين'},
{'lyrics':'مقادير يا قلبي العنا مقادير','artist':'طلال مداح'},
{'lyrics':'ظلمتني والله قوي يجازيك','artist':'طلال مداح'},
{'lyrics':'فزيت من نومي أناديلك','artist':'ذكرى'},
{'lyrics':'ابد على حطة يدك','artist':'ذكرى'},
{'lyrics':'أنا لولا الغلا والمحبة','artist':'فؤاد عبدالواحد'},
{'lyrics':'كلمة ولو جبر خاطر','artist':'عبادي الجوهر'},
{'lyrics':'أحبك لو تكون حاضر','artist':'عبادي الجوهر'},
{'lyrics':'إلحق عيني إلحق','artist':'وليد الشامي'},
{'lyrics':'يردون قلت لازم يردون','artist':'وليد الشامي'},
{'lyrics':'ولهان أنا ولهان','artist':'وليد الشامي'},
{'lyrics':'اقولها كبر عن الدنيا حبيبي','artist':'وليد الشامي'},
{'lyrics':'أنا استاهل وداع أفضل وداع','artist':'نوال الكويتية'},
{'lyrics':'لقيت روحي بعد ما لقيتك','artist':'نوال الكويتية'},
{'lyrics':'غريبة الناس غريبة الدنيا','artist':'وائل جسار'},
{'lyrics':'اعذريني يوم زفافك','artist':'وائل جسار'},
{'lyrics':'ماعاد يمديني ولا عاد يمديك','artist':'عبدالمجيد عبدالله'},
{'lyrics':'يا بعدهم كلهم يا سراجي بينهم','artist':'عبدالمجيد عبدالله'},
{'lyrics':'حتى الكره احساس','artist':'عبدالمجيد عبدالله'},
{'lyrics':'استكثرك وقتي علي','artist':'عبدالمجيد عبدالله'},
{'lyrics':'ياما حاولت الفراق وما قويت','artist':'عبدالمجيد عبدالله'}
        ]

        random.shuffle(self.songs)
        self.used_songs = []

    def start_game(self):
        self.current_question = 0
        self.game_active = True
        self.previous_question = None
        self.previous_answer = None
        self.answered_users.clear()
        self.used_songs = []
        return self.get_question()

    def get_question(self):
        available = [s for s in self.songs if s not in self.used_songs]
        if not available:
            self.used_songs = []
            available = self.songs.copy()
        
        q_data = random.choice(available)
        self.used_songs.append(q_data)
        self.current_answer = q_data['artist']

        colors = self.get_theme_colors()
        
        previous_section = []
        if self.previous_question and self.previous_answer:
            previous_section = [
                {
                    "type":"box","layout":"vertical","contents":[
                        {"type":"text","text":"الأغنية السابقة:","size":"xs","color":colors["text2"],"weight":"bold"},
                        {"type":"text","text":self.previous_question,"size":"xs","color":colors["text2"],"wrap":True,"margin":"xs"},
                        {"type":"text","text":f"✅ المغني: {self.previous_answer}","size":"xs","color":colors["success"],"wrap":True,"margin":"xs"}
                    ],
                    "backgroundColor":colors["card"],"cornerRadius":"15px","paddingAll":"12px","margin":"md"
                },
                {"type":"separator","color":colors["shadow1"],"margin":"md"}
            ]

        flex_content = {
            "type":"bubble","size":"kilo",
            "body":{"type":"box","layout":"vertical","contents":[
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":self.game_name,"size":"xxl","weight":"bold","color":colors["text"],"align":"center"},
                    {"type":"text","text":f"سؤال {self.current_question + 1} من {self.questions_count}","size":"sm","color":colors["text2"],"align":"center","margin":"sm"}
                ]},
                {"type":"separator","margin":"xl","color":colors["shadow1"]}
            ] + previous_section + [
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":"🎤 من المغني؟","size":"md","color":colors["text"],"align":"center","wrap":True,"weight":"bold"},
                    {"type":"box","layout":"vertical","contents":[
                        {"type":"text","text":q_data["lyrics"],"size":"lg","color":colors["primary"],"align":"center","wrap":True,"weight":"bold"}
                    ],
                    "backgroundColor":colors["card"],"cornerRadius":"15px","paddingAll":"20px","margin":"md"}
                ]},
                {"type":"text","text":"💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة","size":"xs","color":colors["text2"],"align":"center","wrap":True,"margin":"lg"},
                {"type":"box","layout":"horizontal","spacing":"sm","contents":[
                    {"type":"button","action":{"type":"message","label":"لمح","text":"لمح"},"style":"secondary","height":"sm","color":colors["shadow1"]},
                    {"type":"button","action":{"type":"message","label":"جاوب","text":"جاوب"},"style":"secondary","height":"sm","color":colors["shadow1"]}
                ]},
                {"type":"button","action":{"type":"message","label":"إيقاف","text":"إيقاف"},"style":"primary","height":"sm","color":colors["error"]}
            ],
            "backgroundColor":colors["bg"],"paddingAll":"24px"}
        }

        return self._create_flex_with_buttons("أغنية", flex_content)

    def check_answer(self, user_answer: str, user_id: str, display_name: str):
        if not self.game_active or user_id in self.answered_users:
            return None

        normalized = self.normalize_text(user_answer)

        if normalized == 'لمح':
            hint = f"💡 اسم المغني يبدأ بحرف '{self.current_answer[0]}'"
            return {'message':hint,'response':self._create_text_message(hint),'points':0}

        if normalized == 'جاوب':
            reveal = f"🎤 المغني: {self.current_answer}"
            self.previous_question = self.used_songs[-1]['lyrics']
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['message'] = f"{reveal}\n\n{result.get('message','')}"
                return result

            return {'message':reveal,'response':self.get_question(),'points':0}

        normalized_correct = self.normalize_text(self.current_answer)
        if normalized == normalized_correct or normalized in normalized_correct or normalized_correct in normalized:
            points = self.add_score(user_id, display_name, 10)
            self.previous_question = self.used_songs[-1]['lyrics']
            self.previous_answer = self.current_answer
            self.current_question += 1
            self.answered_users.clear()

            if self.current_question >= self.questions_count:
                result = self.end_game()
                result['points'] = points
                result['message'] = f"✅ صحيح يا {display_name}!\n🎤 {self.current_answer}\n+{points} نقطة\n\n{result.get('message','')}"
                return result

            return {'message':f"✅ صحيح يا {display_name}!\n🎤 {self.current_answer}\n+{points} نقطة",'response':self.get_question(),'points':points}

        return {'message':"❌ إجابة غير صحيحة",'response':self._create_text_message("❌ إجابة غير صحيحة"),'points':0}
