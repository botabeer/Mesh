"""
Bot Mesh - Flex Builder
Creates all Flex messages with 3D-style buttons and colored themes
Created by: Abeer Aldosari © 2025
"""
from linebot.models import FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, ButtonComponent, URIAction, MessageAction

class FlexBuilder:
    def __init__(self, theme):
        """
        theme: str -> theme key from THEMES
        """
        from config import THEMES
        self.theme = THEMES.get(theme, THEMES['white'])
    
    def _card(self, title, subtitle='', buttons=[]):
        """
        Generic 3D card bubble
        """
        body = [
            TextComponent(text=title, weight='bold', size='lg', color=self.theme['text']),
        ]
        if subtitle:
            body.append(TextComponent(text=subtitle, size='sm', color=self.theme['text2']))

        bubble = BubbleContainer(
            size='mega',
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=body,
                spacing='md',
                padding_all='lg',
                background_color=self.theme['card'],
            ),
            footer=BoxComponent(
                layout='vertical',
                contents=buttons,
                spacing='sm',
                padding_all='lg',
                background_color=self.theme['bg']
            ) if buttons else None,
            styles={
                "header": {"backgroundColor": self.theme['primary']},
                "hero": {"backgroundColor": self.theme['card']},
                "body": {"backgroundColor": self.theme['card']},
                "footer": {"backgroundColor": self.theme['bg']}
            }
        )
        return bubble

    def button(self, label, text=None, uri=None):
        if text:
            return ButtonComponent(action=MessageAction(label=label, text=text), style='primary', color=self.theme['primary'])
        elif uri:
            return ButtonComponent(action=URIAction(label=label, uri=uri), style='primary', color=self.theme['primary'])
        return None

    def welcome(self):
        """
        Main welcome screen
        """
        buttons = [
            self.button('بدء اللعب', text='بداية'),
            self.button('مساعدة', text='مساعدة'),
            self.button('ثيم', text='ثيم')
        ]
        bubble = self._card('مرحباً بك في Bot Mesh', 'اختر لعبة أو أمر من الأزرار أدناه', buttons)
        return FlexSendMessage(alt_text='مرحباً', contents=bubble)

    def help(self):
        """
        Help window
        """
        text = (
            "⚡ قائمة الأوامر:\n"
            "- اكتب اسم اللعبة لبدء اللعب.\n"
            "- نقاطي: عرض نقاطك وترتيبك.\n"
            "- ثيم: اختيار ثيم للواجهة.\n"
            "- انضم: للتسجيل قبل اللعب.\n"
            "- انسحب: لإلغاء المشاركة من اللعبة.\n"
            "- إيقاف: لإنهاء أي لعبة نشطة."
        )
        bubble = self._card('مساعدة Bot Mesh', text)
        return FlexSendMessage(alt_text='مساعدة', contents=bubble)

    def stats(self, data, rank):
        """
        Show user stats
        """
        text = f"نقاطك: {data['points']}\nعدد الألعاب: {data['games']}\nعدد الفوز: {data['wins']}\nترتيبك: {rank}"
        bubble = self._card('إحصائياتك', text)
        return FlexSendMessage(alt_text='إحصائيات', contents=bubble)

    def themes(self):
        """
        Show theme selection
        """
        from config import THEMES
        buttons = []
        for key, t in THEMES.items():
            buttons.append(self.button(t['name'], text=f'ثيم:{key}'))
        bubble = self._card('اختر ثيمك', 'الثيم سيطبق على جميع النوافذ والأزرار', buttons)
        return FlexSendMessage(alt_text='ثيمات', contents=bubble)

    def game_result(self, title, message):
        """
        Display game results
        """
        bubble = self._card(title, message)
        return FlexSendMessage(alt_text=title, contents=bubble)
