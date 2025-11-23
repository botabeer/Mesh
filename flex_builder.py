"""
Bot Mesh - Flex Builder (Enhanced 3D Theme Version)
Created by: Abeer Aldosari © 2025
"""
from linebot.models import BubbleContainer, BoxComponent, TextComponent, ButtonComponent, URIAction, FlexSendMessage

from config import THEMES

class FlexBuilder:
    def __init__(self, theme_key: str = 'white'):
        self.theme = THEMES.get(theme_key, THEMES['white'])

    def _card(self, title: str, subtitle: str = '', emoji: str = '', button_text: str = None):
        """إنشاء بطاقة 3D"""
        return BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                spacing='md',
                contents=[
                    TextComponent(text=f"{emoji} {title}", size='lg', weight='bold', color=self.theme['text']),
                    TextComponent(text=subtitle, size='sm', color=self.theme['text2']) if subtitle else None,
                    ButtonComponent(
                        action=URIAction(label=button_text or 'فتح', uri='https://line.me'),
                        style='primary',
                        color=self.theme['primary']
                    ) if button_text else None
                ]
            ),
            styles={
                'header': {'backgroundColor': self.theme['card']},
                'hero': {'backgroundColor': self.theme['bg']},
                'body': {'backgroundColor': self.theme['bg']}
            }
        )

    def welcome(self):
        """نافذة البداية"""
        cards = [
            self._card("🎮 مرحباً بك في Bot Mesh", "اختر لعبة من الأزرار أدناه", "🎉"),
            self._card("🎨 اختر ثيمك", "يمكنك تغييره في أي وقت", "🖌️")
        ]
        return {
            "type": "carousel",
            "contents": cards
        }

    def help(self):
        """نافذة المساعدة"""
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "💡 مساعدة Bot Mesh", "weight": "bold", "color": self.theme['text']},
                    {"type": "text", "text": "• اكتب اسم اللعبة لبدء اللعب\n• اكتب 'إيقاف' لإنهاء اللعبة\n• اكتب 'ثيم' لتغيير ثيمك", "color": self.theme['text2']}
                ],
                "backgroundColor": self.theme['bg']
            }
        }

    def themes(self):
        """نافذة الثيمات"""
        items = []
        for key, theme in THEMES.items():
            items.append({
                "type": "button",
                "action": {"type": "message", "label": theme['name'], "text": f"ثيم:{key}"},
                "color": theme['primary'],
                "style": "primary",
                "margin": "sm"
            })
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": items,
                "backgroundColor": self.theme['bg']
            }
        }

    def stats(self, data: dict, rank: int):
        """نافذة إحصائيات المستخدم"""
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": f"👤 نقاط {data.get('points',0)}", "weight": "bold", "color": self.theme['text']},
                    {"type": "text", "text": f"🎮 الألعاب: {data.get('games',0)}", "color": self.theme['text2']},
                    {"type": "text", "text": f"🏆 الانتصارات: {data.get('wins',0)}", "color": self.theme['text2']},
                    {"type": "text", "text": f"🥇 ترتيبك: {rank}", "color": self.theme['text2']}
                ],
                "backgroundColor": self.theme['bg']
            }
        )
