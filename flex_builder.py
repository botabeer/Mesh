from linebot.models import FlexSendMessage, BubbleContainer, BoxComponent, TextComponent

class FlexBuilder:
    def __init__(self, theme):
        from config import THEMES
        self.theme = THEMES.get(theme, THEMES['white'])

    def welcome(self):
        return BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[TextComponent(text='🎮 أهلاً بك في Bot Mesh!', weight='bold', color=self.theme['text'])]
            )
        )

    def help(self):
        return BubbleContainer(
            body=BoxComponent(
                layout='vertical',
                contents=[TextComponent(text='📌 أوامر البوت:\nانضم - للبدء\nانسحب - للخروج\nإيقاف - لإنهاء اللعبة', color=self.theme['text'])]
            )
        )

    def themes(self):
        boxes = []
        for name, t in self.theme.items():
            boxes.append(TextComponent(text=t, color=self.theme['text']))
        return BubbleContainer(body=BoxComponent(layout='vertical', contents=boxes))
