"""
Bot Mesh - Flex Message Builder (3D Themed)
Created by: Abeer Aldosari © 2025
"""
from config import THEMES

class FlexBuilder:
    """منشئ رسائل Flex Messages المتقدمة مع دعم ثيمات المستخدم"""
    
    def __init__(self, theme='white'):
        self.theme_name = theme
        self.t = THEMES.get(theme, THEMES['white'])
    
    def _btn(self, emoji, txt, cmd):
        """زر 3D"""
        return {
            "type": "box",
            "layout": "vertical",
            "action": {"type": "message", "text": cmd},
            "contents": [
                {"type": "text", "text": emoji, "size": "xl", "align": "center", "color": self.t['primary']},
                {"type": "text", "text": txt, "size": "sm", "align": "center", "weight": "bold", "margin": "sm"}
            ],
            "backgroundColor": self.t['card'],
            "cornerRadius": "15px",
            "paddingAll": "md",
            "flex": 1,
            "shadow": "md"
        }
    
    def _card(self, contents):
        """كارت 3D"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": self.t['card'],
            "cornerRadius": "20px",
            "paddingAll": "lg",
            "margin": "lg",
            "shadow": "lg"
        }
    
    def welcome(self):
        """نافذة البداية مع زر اختيار الثيم"""
        games = [
            ['🧠','ذكاء','ذكاء'], ['🎨','لون','لون'], ['🔤','ترتيب','ترتيب'],
            ['🔢','رياضيات','رياضيات'], ['⚡','أسرع','أسرع'], ['↔️','ضد','ضد'],
            ['✏️','تكوين','تكوين'], ['🎵','أغنية','أغنية'], ['🎯','لعبة','لعبة'],
            ['⛓️','سلسلة','سلسلة'], ['🤔','خمن','خمن'], ['💖','توافق','توافق']
        ]
        
        rows = []
        for i in range(0, len(games), 3):
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm",
                "contents": [self._btn(*g) for g in games[i:i+3]]
            })
        
        # زر إيقاف
        control_btn = {
            "type": "button",
            "action": {"type": "message", "label": "⏹️ إيقاف", "text": "إيقاف"},
            "style": "secondary",
            "height": "sm"
        }
        
        # زر اختيار الثيم
        theme_btn = {
            "type": "button",
            "action": {"type": "message", "label": "🎨 ثيم", "text": "ثيم"},
            "style": "primary",
            "color": self.t['primary'],
            "height": "sm"
        }
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": self.t['bg'],
                "paddingAll": "20px",
                "contents": [
                    self._card([
                        {"type": "text","text":"🎮 Bot Mesh","size":"xxl","weight":"bold","color":self.t['primary'],"align":"center"},
                        {"type": "text","text":"بوت الألعاب الترفيهية","size":"sm","color":self.t['text2'],"align":"center"}
                    ]),
                    *rows,
                    {"type": "separator","margin":"lg","color":self.t['text2']+"30"},
                    {"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[control_btn, theme_btn]},
                    {"type":"text","text":"© 2025 Abeer Aldosari","size":"xxs","color":self.t['text2'],"align":"center","margin":"md"}
                ]
            }
        }
    
    def themes(self):
        """نافذة اختيار الثيمات مباشرة من البداية"""
        rows = []
        for theme_key in THEMES:
            theme_data = THEMES[theme_key]
            rows.append({
                "type":"box",
                "layout":"horizontal",
                "margin":"sm",
                "backgroundColor": self.t['card'],
                "cornerRadius":"15px",
                "paddingAll":"md",
                "action":{"type":"message","text":f"ثيم:{theme_key}"},
                "contents":[
                    {"type":"box","layout":"vertical","backgroundColor":theme_data['primary'],"cornerRadius":"10px","width":"40px","height":"40px","justifyContent":"center",
                     "contents":[{"type":"text","text":theme_data['name'][:2],"align":"center","color":"#FFFFFF"}]},
                    {"type":"text","text":theme_data['name'],"size":"md","weight":"bold","margin":"md","gravity":"center","color":self.t['text']}
                ]
            })
        
        return {
            "type":"bubble",
            "size":"mega",
            "body":{
                "type":"box",
                "layout":"vertical",
                "backgroundColor":self.t['bg'],
                "paddingAll":"20px",
                "contents":[
                    self._card([{"type":"text","text":"🎨 اختر الثيم","size":"xl","weight":"bold","align":"center","color":self.t['primary']}]),
                    *rows
                ]
            }
        }
