from linebot.models import FlexSendMessage
import json

class PersonalityGame:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        with open("data/personality_games.json", "r", encoding="utf-8") as f:
            self.games_data = json.load(f)
        self.current_game = None
        self.current_question_index = 0
        self.answers_counter = {"أ":0, "ب":0, "ج":0}
        self.user_id = None

    def start_game(self, game_key, user_id):
        self.user_id = user_id
        self.current_game = self.games_data[game_key]
        self.current_question_index = 0
        self.answers_counter = {"أ":0, "ب":0, "ج":0}
        return self.get_next_question()

    def get_next_question(self):
        if self.current_question_index >= len(self.current_game["questions"]):
            return self.show_result()
        
        q = self.current_game["questions"][self.current_question_index]
        self.current_question_index += 1

        flex_message = FlexSendMessage(
            alt_text=q["question"],
            contents={
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents":[
                        {"type":"text", "text": q["question"], "wrap": True, "weight":"bold", "size":"lg"}
                    ]
                },
                "footer": {
                    "type":"box",
                    "layout":"horizontal",
                    "spacing":"sm",
                    "contents":[
                        {"type":"button","action":{"type":"postback","label":"أ","data":"أ"}},
                        {"type":"button","action":{"type":"postback","label":"ب","data":"ب"}},
                        {"type":"button","action":{"type":"postback","label":"ج","data":"ج"}}
                    ]
                }
            }
        )
        return flex_message

    def register_answer(self, choice):
        if choice in self.answers_counter:
            self.answers_counter[choice] += 1
        return self.get_next_question()

    def show_result(self):
        max_choice = max(self.answers_counter, key=self.answers_counter.get)
        result_text = self.current_game["results_text"][max_choice]

        flex_message = FlexSendMessage(
            alt_text="نتيجتك",
            contents={
                "type":"bubble",
                "body":{
                    "type":"box",
                    "layout":"vertical",
                    "contents":[
                        {"type":"text","text":"نتيجتك","weight":"bold","size":"lg"},
                        {"type":"text","text": result_text, "wrap": True}
                    ]
                }
            }
        )
        return flex_message
