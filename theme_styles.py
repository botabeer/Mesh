# -*- coding: utf-8 -*-
"""
Bot Mesh - Theme & UI Styles (Unified Source)
Created by: Abeer Aldosari © 2025
"""

# ===================== الثيمات الموحدة =====================
THEMES = {
    "💜": {
        "name": "purple",
        "color": "#9F7AEA",
        "bg": "#F3E8FF",
        "card": "#FAF5FF",
        "primary": "#9F7AEA",
        "text": "#44337A",
        "text2": "#6B46C1"
    },
    "💚": {
        "name": "green",
        "color": "#48BB78",
        "bg": "#E6FFFA",
        "card": "#F0FFF4",
        "primary": "#38B2AC",
        "text": "#234E52",
        "text2": "#2C7A7B"
    },
    "🤍": {
        "name": "white",
        "color": "#CBD5E0",
        "bg": "#F8F9FA",
        "card": "#FFFFFF",
        "primary": "#667EEA",
        "text": "#2D3748",
        "text2": "#718096"
    },
    "🖤": {
        "name": "black",
        "color": "#2D3748",
        "bg": "#1A202C",
        "card": "#2D3748",
        "primary": "#667EEA",
        "text": "#E2E8F0",
        "text2": "#CBD5E0"
    },
    "💙": {
        "name": "blue",
        "color": "#3182CE",
        "bg": "#EBF8FF",
        "card": "#BEE3F8",
        "primary": "#3182CE",
        "text": "#2C5282",
        "text2": "#2B6CB0"
    },
    "🩶": {
        "name": "gray",
        "color": "#718096",
        "bg": "#F7FAFC",
        "card": "#EDF2F7",
        "primary": "#718096",
        "text": "#2D3748",
        "text2": "#4A5568"
    },
    "🩷": {
        "name": "pink",
        "color": "#ED64A6",
        "bg": "#FFF5F7",
        "card": "#FED7E2",
        "primary": "#D53F8C",
        "text": "#702459",
        "text2": "#97266D"
    },
    "🧡": {
        "name": "orange",
        "color": "#DD6B20",
        "bg": "#FFFAF0",
        "card": "#FEEBC8",
        "primary": "#DD6B20",
        "text": "#7C2D12",
        "text2": "#C05621"
    },
    "🤎": {
        "name": "brown",
        "color": "#8B4513",
        "bg": "#F7F3EF",
        "card": "#EDE0D4",
        "primary": "#8B4513",
        "text": "#5C2E00",
        "text2": "#7A4F1D"
    }
}

DEFAULT_THEME = "💜"

# ===================== الأزرار الثابتة =====================
FIXED_BUTTONS = ["Home", "Games", "Info"]

# ===================== دالة مساعدة =====================
def get_theme_colors(theme_emoji):
    """الحصول على ألوان الثيم المطلوب"""
    return THEMES.get(theme_emoji, THEMES[DEFAULT_THEME])
