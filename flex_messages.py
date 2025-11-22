# =============================================
# Bot Mesh - Enhanced Flex Messages System (Fixed)
# Created by: Abeer Aldosari © 2025
# =============================================
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

# =============================================
# الثيمات
# =============================================
class Theme(Enum):
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"
    MINT = "mint"

@dataclass
class ThemeColors:
    name: str
    name_ar: str
    emoji: str
    background: str
    surface: str
    card: str
    text_primary: str
    text_secondary: str
    accent: str
    accent_dark: str
    button_bg: str
    shadow_light: str
    shadow_dark: str
    success: str = "#48BB78"
    error: str = "#FC8181"
    warning: str = "#F6AD55"

# ثيمات
THEMES: Dict[Theme, ThemeColors] = {
    Theme.WHITE: ThemeColors("white","⚪ أبيض","⚪","#E8EBF5","#E8EBF5","#FFFFFF",
                             "#2C3E50","#95A5A6","#667EEA","#5A67D8","#667EEA","#FFFFFF","#B8C1E0"),
    Theme.BLACK: ThemeColors("black","⚫ أسود","⚫","#0F0F1A","#1A1A2E","#252538",
                             "#FFFFFF","#A0AEC0","#00D9FF","#00B8D4","#00D9FF","#2A2A4A","#000000"),
    Theme.GRAY:  ThemeColors("gray","🔘 رمادي","🔘","#1A202C","#2D3748","#4A5568",
                             "#F7FAFC","#CBD5E0","#68D391","#48BB78","#48BB78","#4A5568","#0D0D0D"),
    Theme.BLUE:  ThemeColors("blue","💙 أزرق","💙","#0A1628","#1E3A5F","#0F2744",
                             "#E0F2FE","#7DD3FC","#0EA5E9","#0284C7","#0EA5E9","#1E4976","#000000"),
    Theme.PURPLE:ThemeColors("purple","💜 بنفسجي","💜","#1A0F3E","#312E81","#3730A3",
                             "#F5F3FF","#C4B5FD","#A855F7","#9333EA","#9333EA","#4338CA","#000000"),
    Theme.PINK:  ThemeColors("pink","🌸 وردي","🌸","#FFF1F2","#FFE4E6","#FFFFFF",
                             "#881337","#BE123C","#F43F5E","#E11D48","#F43F5E","#FFFFFF","#FFC9D0"),
    Theme.MINT:  ThemeColors("mint","🍃 نعناعي","🍃","#ECFDF5","#D1FAE5","#FFFFFF",
                             "#065F46","#059669","#10B981","#059669","#10B981","#FFFFFF","#9EF3CA"),
}

# =============================================
# Flex Builder
# =============================================
class FlexMessageBuilder:
    def __init__(self, theme: Theme = Theme.WHITE):
        self.theme = THEMES.get(theme, THEMES[Theme.WHITE])

    def set_theme(self, theme_name: str):
        theme_map = {t.value: t for t in Theme}
        theme = theme_map.get(theme_name.lower(), Theme.WHITE)
        self.theme = THEMES[theme]

    # -----------------------------------------
    # عناصر أساسية
    # -----------------------------------------
    def _text(self, text: str, size: str = "md", weight: str = "regular",
              color: str = None, wrap: bool = True, margin: str = "none") -> dict:
        """إنشاء نص (لا backgroundColor هنا)"""
        return {"type": "text", "text": text, "size": size, "weight": weight,
                "color": color or self.theme.text_primary, "wrap": wrap, "margin": margin}

    def _box(self, contents: List[dict], layout: str = "vertical",
             bg: str = None, padding: str = "lg", margin: str = "none",
             corner: str = "20px", spacing: str = "md", border_width: str = None,
             border_color: str = None, action: dict = None) -> dict:
        """إنشاء صندوق"""
        box = {"type": "box", "layout": layout, "contents": contents,
               "paddingAll": padding, "margin": margin, "cornerRadius": corner,
               "spacing": spacing}
        if bg:
            box["backgroundColor"] = bg
        if border_width:
            box["borderWidth"] = border_width
            box["borderColor"] = border_color or self.theme.accent
        if action:
            box["action"] = action
        return box

    def _button(self, label: str, text: str, style: str = "primary",
                color: str = None, height: str = "sm") -> dict:
        """زر"""
        btn = {"type": "button",
               "action": {"type": "message", "label": label, "text": text},
               "style": style, "height": height}
        if color:
            btn["color"] = color
        return btn

    def _separator(self, margin: str = "lg", color: str = None) -> dict:
        """فاصل"""
        return {"type": "separator", "margin": margin,
                "color": color or self.theme.text_secondary + "30"}

    # -----------------------------------------
    # نافذة ترحيب
    # -----------------------------------------
    def create_welcome_screen(self) -> dict:
        return {
            "type": "bubble",
            "size": "mega",
            "body": self._box([
                self._box([self._text("🎮", "xxl"),
                           self._text("Bot Mesh","xxl","bold"),
                           self._text("بوت الألعاب الترفيهية","sm",
                                      self.theme.text_secondary)],
                          bg=self.theme.card, corner="25px", padding="xl"),
                self._box([self._text("ابدأ الآن!","lg","bold"),
                           self._text("سجل واستمتع بـ 11 لعبة ممتعة","xs",
                                      color=self.theme.text_secondary)],
                          bg=self.theme.surface, corner="20px", margin="lg", padding="lg")
            ], bg=self.theme.background, padding="20px", spacing="none")
        }

    # -----------------------------------------
    # بطاقة الإحصائيات
    # -----------------------------------------
    def create_stats_card(self, user_data: dict, rank: int = 0) -> dict:
        if not user_data:
            return self._create_error("لم تلعب بعد! اكتب 'انضم' ثم ابدأ اللعب")
        points = user_data.get('total_points', 0)
        games = user_data.get('games_played', 0)
        wins = user_data.get('wins', 0)
        win_rate = (wins / games * 100) if games else 0
        is_registered = user_data.get('is_registered', False)
        level = self._get_level(points)
        return {
            "type": "bubble",
            "size": "mega",
            "body": self._box([
                self._text(f"{level['emoji']} {level['name']}", "xl","bold"),
                self._text(f"المركز #{rank}" if rank else "غير مصنف","sm",color=self.theme.text_secondary),
                self._text(f"نقاط: {points} | ألعاب: {games} | فوز: {wins} | نسبة: {win_rate:.0f}%","sm",color=self.theme.text_secondary)
            ], bg=self.theme.background, padding="20px", spacing="md")
        }

    def _get_level(self, points: int) -> dict:
        if points<100: return {"name":"🌱 مبتدئ","emoji":"🌱"}
        if points<500: return {"name":"⭐ متوسط","emoji":"⭐"}
        if points<1000: return {"name":"🔥 محترف","emoji":"🔥"}
        if points<5000: return {"name":"👑 أسطوري","emoji":"👑"}
        return {"name":"💎 خارق","emoji":"💎"}

    def _create_error(self, msg: str) -> dict:
        return {
            "type":"bubble",
            "body": self._box([self._text("⚠️","xxl"), self._text(msg,"md")],
                              bg=self.theme.background, padding="40px", spacing="md")
        }

# Singleton
flex_builder = FlexMessageBuilder()
