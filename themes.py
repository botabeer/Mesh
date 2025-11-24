# -*- coding: utf-8 -*-
"""
Themes and UI Styles for Bot Mesh
Created by: Abeer Aldosari © 2025
Includes: themes, buttons, windows, games styles
"""

from typing import Dict, List

# =============================================================================
# Available Themes
# =============================================================================
THEMES = {
    "💜": "Purple",
    "💚": "Green",
    "🤍": "White",
    "🖤": "Black",
    "💙": "Blue",
    "🩶": "Gray",
    "🩷": "Pink",
    "🧡": "Orange",
    "🤎": "Brown"
}

THEME_COLORS = {
    "💜": {
        "bg": "#F3E8FF",
        "card": "#FAF5FF",
        "primary": "#9F7AEA",
        "text": "#44337A",
        "text2": "#6B46C1"
    },
    "💚": {
        "bg": "#E6FFFA",
        "card": "#F0FFF4",
        "primary": "#38B2AC",
        "text": "#234E52",
        "text2": "#2C7A7B"
    },
    "🤍": {
        "bg": "#F8F9FA",
        "card": "#FFFFFF",
        "primary": "#667EEA",
        "text": "#2D3748",
        "text2": "#718096"
    },
    "🖤": {
        "bg": "#1A202C",
        "card": "#2D3748",
        "primary": "#667EEA",
        "text": "#E2E8F0",
        "text2": "#CBD5E0"
    },
    "💙": {
        "bg": "#EBF8FF",
        "card": "#BEE3F8",
        "primary": "#3182CE",
        "text": "#2C5282",
        "text2": "#2B6CB0"
    },
    "🩶": {
        "bg": "#F7FAFC",
        "card": "#EDF2F7",
        "primary": "#718096",
        "text": "#2D3748",
        "text2": "#4A5568"
    },
    "🩷": {
        "bg": "#FFF5F7",
        "card": "#FED7E2",
        "primary": "#D53F8C",
        "text": "#702459",
        "text2": "#97266D"
    },
    "🧡": {
        "bg": "#FFFAF0",
        "card": "#FEEBC8",
        "primary": "#DD6B20",
        "text": "#7C2D12",
        "text2": "#C05621"
    },
    "🤎": {
        "bg": "#F7F3EF",
        "card": "#EDE0D4",
        "primary": "#8B4513",
        "text": "#5C2E00",
        "text2": "#7A4F1D"
    }
}

# =============================================================================
# Fixed Footer Buttons
# =============================================================================
FOOTER_BUTTONS = [
    {
        "type": "button",
        "action": {"type": "message", "label": "Home", "text": "Home"},
        "style": "primary",
        "height": "sm"
    },
    {
        "type": "button",
        "action": {"type": "message", "label": "Games", "text": "Games"},
        "style": "secondary",
        "height": "sm"
    },
    {
        "type": "button",
        "action": {"type": "message", "label": "Help", "text": "Info"},
        "style": "secondary",
        "height": "sm"
    }
]

# =============================================================================
# Default Bot Style (UI)
# =============================================================================
BOT_STYLE = {
    "font": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    "border_radius": "20px",
    "padding": "20px",
    "shadow": "0 8px 32px 0 rgba(31, 38, 135, 0.37)",
    "blur": "10px"
}

# =============================================================================
# Windows / Screens Templates
# =============================================================================

HOME_WINDOW = {
    "title": "🤖 Bot Mesh",
    "subtitle": "مرحباً بك في البوت!",
    "description": "اختر لعبة من قائمة الألعاب أو استعرض معلومات البوت.",
    "buttons": FOOTER_BUTTONS
}

GAMES_WINDOW = {
    "title": "🎮 قائمة الألعاب",
    "description": "اختر اللعبة التي تريد لعبها من القائمة أدناه.",
    "buttons": FOOTER_BUTTONS
}

INFO_WINDOW = {
    "title": "ℹ️ معلومات البوت",
    "description": "هذا البوت يحتوي على ألعاب، نقاط، ثيمات قابلة للتغيير، ودعم للذكاء الاصطناعي.",
    "buttons": FOOTER_BUTTONS
}

HELP_WINDOW = {
    "title": "🆘 نافذة المساعدة",
    "description": (
        "طريقة استخدام البوت:\n"
        "- انضم للعب: اكتب 'انضم'\n"
        "- انسحب: اكتب 'انسحب'\n"
        "- عرض نقاطك: 'نقاطي'\n"
        "- عرض قائمة الألعاب: 'Games'\n"
        "- تغيير الثيم: 'ثيم 💜'\n"
        "- العودة للصفحة الرئيسية: 'Home'"
    ),
    "buttons": FOOTER_BUTTONS
}

# =============================================================================
# Game Menu Templates
# =============================================================================
GAMES_LIST = [
    "IQ",
    "رياضيات",
    "لون الكلمة",
    "كلمة مبعثرة",
    "كتابة سريعة",
    "عكس",
    "حروف وكلمات",
    "أغنية",
    "إنسان حيوان نبات",
    "سلسلة كلمات",
    "تخمين",
    "توافق"
]

# Mapping Game Names to Emojis (for Flex display)
GAME_ICONS = {
    "IQ": "🧠",
    "رياضيات": "➕",
    "لون الكلمة": "🎨",
    "كلمة مبعثرة": "🔤",
    "كتابة سريعة": "⌨️",
    "عكس": "↔️",
    "حروف وكلمات": "🔠",
    "أغنية": "🎵",
    "إنسان حيوان نبات": "🌱",
    "سلسلة كلمات": "🔗",
    "تخمين": "❓",
    "توافق": "❤️"
}

# =============================================================================
# Utility Functions
# =============================================================================
def get_theme_colors(theme_emoji: str) -> Dict[str, str]:
    """Return colors dictionary for a given theme"""
    return THEME_COLORS.get(theme_emoji, THEME_COLORS["🤍"])

def build_footer_buttons() -> List[Dict]:
    """Return footer buttons list for Flex messages"""
    return FOOTER_BUTTONS

def get_game_icon(game_name: str) -> str:
    """Return emoji for game"""
    return GAME_ICONS.get(game_name, "🎮")
