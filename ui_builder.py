# ui_builder.py
from constants import BOT_NAME, THEMES, FIXED_BOTTOM_BUTTONS, get_user_name

class UIBuilder:
    """تبني واجهة المستخدم للبوت Bot Mesh"""
    
    def __init__(self, line_api):
        self.line_api = line_api

    def build_welcome_message(self, user_id: str, user_name: str) -> dict:
        """تبني رسالة الترحيب مع اسم المستخدم فقط"""
        display_name = get_user_name(user_id, user_name)
        
        message = {
            "type": "flex",
            "altText": f"مرحبا {display_name} في {BOT_NAME}",
            "contents": {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": f"مرحباً {display_name} 👋", "weight": "bold", "size": "lg"},
                        {"type": "text", "text": f"مرحبا بك في {BOT_NAME}", "size": "sm", "color": "#888888"}
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "اختر ما تريد من الأسفل:", "size": "md"}
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": btn["title"], "text": btn["title"]}
                        } for btn in FIXED_BOTTOM_BUTTONS
                    ],
                    "spacing": "sm"
                }
            }
        }
        return message

    def build_game_buttons(self, game_names: list[str]) -> dict:
        """ترجع أزرار الألعاب بشكل مرن يمكن تغييره"""
        return {
            "type": "flex",
            "altText": "قائمة الألعاب",
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "button", "action": {"type": "message", "label": name, "text": name}} for name in game_names
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "button", "action": {"type": "message", "label": btn["title"], "text": btn["title"]}} for btn in FIXED_BOTTOM_BUTTONS
                    ]
                }
            }
        }
