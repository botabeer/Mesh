"""
Bot Mesh - Flex Message Builder (Enhanced)
Created by: Abeer Aldosari © 2025
"""
from config import THEMES


class FlexBuilder:
    """منشئ رسائل Flex Messages المتقدمة"""
    
    def __init__(self, theme='white'):
        self.t = THEMES.get(theme, THEMES['white'])
    
    def _btn(self, emoji, txt, cmd):
        """إنشاء زر لعبة"""
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
            "flex": 1
        }
    
    def _card(self, contents):
        """إنشاء كارت"""
        return {
            "type": "box",
            "layout": "vertical",
            "contents": contents,
            "backgroundColor": self.t['card'],
            "cornerRadius": "20px",
            "paddingAll": "lg",
            "margin": "lg"
        }
    
    def welcome(self):
        """نافذة البداية الجديدة مع تعريف البوت"""
        games = [
            ['🧠', 'ذكاء', 'ذكاء'],
            ['🎨', 'لون', 'لون'],
            ['🔤', 'ترتيب', 'ترتيب'],
            ['🔢', 'رياضيات', 'رياضيات'],
            ['⚡', 'أسرع', 'أسرع'],
            ['↔️', 'ضد', 'ضد'],
            ['✏️', 'تكوين', 'تكوين'],
            ['🎵', 'أغنية', 'أغنية'],
            ['🎯', 'لعبة', 'لعبة'],
            ['⛓️', 'سلسلة', 'سلسلة'],
            ['🤔', 'خمن', 'خمن'],
            ['💖', 'توافق', 'توافق']
        ]
        
        rows = []
        for i in range(0, len(games), 3):
            row_games = games[i:i+3]
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "sm",
                "contents": [self._btn(*g) for g in row_games]
            })
        
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
                        {"type": "text", "text": "🎮 @bot Mesh", "size": "xxl", "weight": "bold", "color": self.t['primary'], "align": "center"},
                        {"type": "text", "text": "بوت الألعاب الترفيهية", "size": "sm", "color": self.t['text2'], "align": "center"},
                        {"type": "text", "text": "📝 أوامر ومميزات البوت:", "size": "sm", "weight": "bold", "color": self.t['primary'], "margin": "md"},
                        {"type": "text", "text": "• يمكنك اللعب في المجموعات والخاص\n• تغيير الثيم الخاص بك\n• قائمة الألعاب: ذكاء، لون، ترتيب، رياضيات، أسرع، ضد، تكوين، أغنية، لعبة، سلسلة، خمن، توافق", "size": "xs", "color": self.t['text2'], "wrap": True, "margin": "sm"},
                        {"type": "text", "text": "💡 تقدر تستخدم البوت في المجموعات والخاص", "size": "xs", "color": self.t['text2'], "wrap": True, "margin": "sm"}
                    ]),
                    *rows,
                    {"type": "separator", "margin": "lg", "color": self.t['text2'] + "30"},
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "lg",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "📊 نقاطي", "text": "نقاطي"}, "style": "secondary", "height": "sm"},
                            {"type": "button", "action": {"type": "message", "label": "🏆 صدارة", "text": "الصدارة"}, "style": "secondary", "height": "sm"}
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "sm",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "🛑 إيقاف", "text": "إيقاف"}, "style": "secondary", "height": "sm"},
                            {"type": "button", "action": {"type": "message", "label": "🎨 ثيم", "text": "ثيم"}, "style": "primary", "color": self.t['primary'], "height": "sm"}
                        ]
                    },
                    {"type": "text", "text": "© 2025 Abeer Aldosari", "size": "xxs", "color": self.t['text2'], "align": "center", "margin": "md"}
                ]
            }
        }
    
    def stats(self, data, rank):
        """إحصائيات المستخدم"""
        pts = data.get('points', 0)
        games_count = data.get('games', 0)
        wins = data.get('wins', 0)
        rate = (wins / games_count * 100) if games_count > 0 else 0
        
        if pts < 100:
            lvl = '🌱 مبتدئ'
        elif pts < 500:
            lvl = '⭐ متوسط'
        elif pts < 1000:
            lvl = '🔥 محترف'
        else:
            lvl = '👑 أسطوري'
        
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
                        {"type": "text", "text": lvl, "size": "xl", "weight": "bold", "align": "center", "color": self.t['primary']},
                        {"type": "text", "text": f"المركز #{rank}" if rank else "غير مصنف", "size": "sm", "color": self.t['text2'], "align": "center"}
                    ]),
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "md",
                        "margin": "lg",
                        "contents": [
                            self._stat('💰', str(pts), 'نقطة'),
                            self._stat('🎮', str(games_count), 'لعبة')
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "md",
                        "margin": "sm",
                        "contents": [
                            self._stat('🏆', str(wins), 'فوز'),
                            self._stat('📈', f"{rate:.0f}%", 'نسبة')
                        ]
                    },
                    {"type": "button", "action": {"type": "message", "label": "🎮 العب الآن", "text": "بداية"}, "style": "primary", "color": self.t['primary'], "height": "sm", "margin": "xl"}
                ]
            }
        }
    
    def _stat(self, emoji, val, lbl):
        """إحصائية واحدة"""
        return {
            "type": "box",
            "layout": "vertical",
            "flex": 1,
            "backgroundColor": self.t['card'],
            "cornerRadius": "15px",
            "paddingAll": "md",
            "contents": [
                {"type": "text", "text": emoji, "size": "xl", "align": "center"},
                {"type": "text", "text": val, "size": "lg", "weight": "bold", "align": "center", "margin": "xs", "color": self.t['text']},
                {"type": "text", "text": lbl, "size": "xs", "color": self.t['text2'], "align": "center"}
            ]
        }
    
    def leaderboard(self, leaders):
        """لوحة الصدارة"""
        medals = ['🥇', '🥈', '🥉']
        rows = []
        for i, u in enumerate(leaders[:10]):
            medal = medals[i] if i < 3 else f"#{i+1}"
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "backgroundColor": self.t['card'] if i < 3 else "transparent",
                "cornerRadius": "10px",
                "paddingAll": "sm",
                "contents": [
                    {"type": "text", "text": medal, "size": "md", "flex": 1, "color": self.t['text']},
                    {"type": "text", "text": u.get('name', 'لاعب'), "size": "md", "weight": "bold" if i < 3 else "regular", "flex": 3, "color": self.t['text']},
                    {"type": "text", "text": f"{u.get('points', 0)}⭐", "size": "md", "color": self.t['primary'] if i < 3 else self.t['text2'], "align": "end", "flex": 2}
                ]
            })
        return {
            "type": "bubble",
            "size": "mega",
            "body": {"type": "box", "layout": "vertical", "backgroundColor": self.t['bg'], "paddingAll": "20px",
                     "contents": [self._card([{"type": "text", "text": "🏆 لوحة الصدارة", "size": "xl", "weight": "bold", "align": "center", "color": self.t['primary']}])] + rows + [
                         {"type": "button", "action": {"type": "message", "label": "🎮 العب الآن", "text": "بداية"}, "style": "primary", "color": self.t['primary'], "height": "sm", "margin": "xl"}
                     ]}
        }
    
    def themes(self):
        """قائمة الثيمات"""
        rows = []
        for theme_key in THEMES:
            theme_data = THEMES[theme_key]
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "backgroundColor": self.t['card'],
                "cornerRadius": "15px",
                "paddingAll": "md",
                "action": {"type": "message", "text": f"ثيم:{theme_key}"},
                "contents": [
                    {"type": "box", "layout": "vertical", "backgroundColor": theme_data['primary'], "cornerRadius": "10px", "width": "40px", "height": "40px", "justifyContent": "center", "contents":[{"type":"text","text":theme_data['name'][:2],"align":"center","color":"#FFFFFF"}]},
                    {"type": "text", "text": theme_data['name'], "size": "md", "weight": "bold", "margin": "md", "gravity": "center", "color": self.t['text']}
                ]
            })
        return {
            "type": "bubble",
            "size": "mega",
            "body": {"type": "box", "layout": "vertical", "backgroundColor": self.t['bg'], "paddingAll": "20px",
                     "contents": [self._card([{"type":"text","text":"🎨 اختر الثيم","size":"xl","weight":"bold","align":"center","color":self.t['primary']}])] + rows}
        }
