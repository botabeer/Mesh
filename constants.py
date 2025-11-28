"""
Bot Mesh - Constants & Configuration v6.0
Created by: Abeer Aldosari © 2025

✅ Fixed: Circular Import Issue
✅ Style: Glassmorphism + Soft Neumorphism
✅ Quick Reply: Games Only (Permanent)
"""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "🎮 Bot Mesh"
BOT_VERSION = "6.0"
BOT_RIGHTS = "© 2025 Abeer Aldosari - All Rights Reserved"

# ============================================================================
# LINE Configuration
# ============================================================================
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def validate_env():
    """Validate required environment variables"""
    if not LINE_CHANNEL_SECRET:
        raise ValueError("LINE_CHANNEL_SECRET is not set")
    if not LINE_CHANNEL_ACCESS_TOKEN:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set")

# ============================================================================
# Glassmorphism + Soft Neumorphism Themes
# ============================================================================
THEMES = {
    "أبيض": {
        "name": "أبيض",
        "bg": "#F7FAFC",
        "card": "#FFFFFF",
        "primary": "#4299E1",
        "secondary": "#63B3ED",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow1": "#E2E8F0",
        "shadow2": "#FFFFFF",
        "button": "#4299E1",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "أسود": {
        "name": "أسود",
        "bg": "#1A202C",
        "card": "#2D3748",
        "primary": "#667EEA",
        "secondary": "#7F9CF5",
        "text": "#F7FAFC",
        "text2": "#CBD5E0",
        "shadow1": "#4A5568",
        "shadow2": "#414D5F",
        "button": "#667EEA",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "رمادي": {
        "name": "رمادي",
        "bg": "#F7FAFC",
        "card": "#FFFFFF",
        "primary": "#4A5568",
        "secondary": "#718096",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow1": "#E2E8F0",
        "shadow2": "#FFFFFF",
        "button": "#4A5568",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "أزرق": {
        "name": "أزرق",
        "bg": "#EBF8FF",
        "card": "#FFFFFF",
        "primary": "#2B6CB0",
        "secondary": "#3182CE",
        "text": "#2C5282",
        "text2": "#2B6CB0",
        "shadow1": "#BEE3F8",
        "shadow2": "#FFFFFF",
        "button": "#2B6CB0",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "بنفسجي": {
        "name": "بنفسجي",
        "bg": "#FAF5FF",
        "card": "#FFFFFF",
        "primary": "#805AD5",
        "secondary": "#9F7AEA",
        "text": "#5B21B6",
        "text2": "#7C3AED",
        "shadow1": "#DDD6FE",
        "shadow2": "#FFFFFF",
        "button": "#805AD5",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "وردي": {
        "name": "وردي",
        "bg": "#FFF5F7",
        "card": "#FFFFFF",
        "primary": "#B83280",
        "secondary": "#D53F8C",
        "text": "#702459",
        "text2": "#97266D",
        "shadow1": "#FED7E2",
        "shadow2": "#FFFFFF",
        "button": "#B83280",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "أخضر": {
        "name": "أخضر",
        "bg": "#F0FDF4",
        "card": "#FFFFFF",
        "primary": "#38A169",
        "secondary": "#48BB78",
        "text": "#064E3B",
        "text2": "#065F46",
        "shadow1": "#A7F3D0",
        "shadow2": "#FFFFFF",
        "button": "#38A169",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "برتقالي": {
        "name": "برتقالي",
        "bg": "#FFFAF0",
        "card": "#FFFFFF",
        "primary": "#C05621",
        "secondary": "#DD6B20",
        "text": "#7C2D12",
        "text2": "#9C4221",
        "shadow1": "#FEEBC8",
        "shadow2": "#FFFFFF",
        "button": "#C05621",
        "success": "#48BB78",
        "error": "#EF4444"
    },
    "بني": {
        "name": "بني",
        "bg": "#FEFCF9",
        "card": "#FFFFFF",
        "primary": "#744210",
        "secondary": "#8B4513",
        "text": "#5C2E00",
        "text2": "#7A4F1D",
        "shadow1": "#E6D5C3",
        "shadow2": "#FFFFFF",
        "button": "#744210",
        "success": "#48BB78",
        "error": "#EF4444"
    }
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# Games List - Ordered & Clear Names (No Emojis, No "لعبة" prefix)
# ============================================================================
GAME_LIST = {
    "أسرع": {
        "label": "أسرع",
        "icon": "⚡",
        "command": "لعبة كتابة سريعة",
        "description": "اختبار سرعة ودقة الكتابة"
    },
    "ذكاء": {
        "label": "ذكاء",
        "icon": "🧠",
        "command": "لعبة IQ",
        "description": "ألغاز ذكية ومتنوعة"
    },
    "لعبة": {
        "label": "لعبة",
        "icon": "🎯",
        "command": "لعبة إنسان حيوان نبات",
        "description": "إنسان، حيوان، نبات، جماد، بلاد"
    },
    "أغنية": {
        "label": "أغنية",
        "icon": "🎵",
        "command": "لعبة أغنية",
        "description": "خمن المغني من الكلمات"
    },
    "خمن": {
        "label": "خمن",
        "icon": "🔮",
        "command": "لعبة تخمين",
        "description": "خمن الكلمة من الفئة والحرف"
    },
    "سلسلة": {
        "label": "سلسلة",
        "icon": "🔗",
        "command": "لعبة سلسلة كلمات",
        "description": "كلمة تبدأ بآخر حرف"
    },
    "ترتيب": {
        "label": "ترتيب",
        "icon": "🔤",
        "command": "لعبة كلمة مبعثرة",
        "description": "رتب الحروف المبعثرة"
    },
    "تكوين": {
        "label": "تكوين",
        "icon": "📝",
        "command": "لعبة حروف وكلمات",
        "description": "كون كلمات من الحروف"
    },
    "ضد": {
        "label": "ضد",
        "icon": "↔️",
        "command": "لعبة عكس",
        "description": "اكتشف عكس الكلمة"
    },
    "لون": {
        "label": "لون",
        "icon": "🎨",
        "command": "لعبة لون الكلمة",
        "description": "اختبار Stroop Effect"
    },
    "رياضيات": {
        "label": "رياضيات",
        "icon": "🔢",
        "command": "لعبة رياضيات",
        "description": "أسئلة حسابية متدرجة"
    },
    "توافق": {
        "label": "توافق",
        "icon": "🖤",
        "command": "لعبة توافق",
        "description": "اختبار التوافق بين اسمين"
    }
}

# ============================================================================
# Fixed Buttons for UI
# ============================================================================
FIXED_BUTTONS = {
    "home": {"label": "🏠 البداية", "text": "بداية"},
    "games": {"label": "🎮 الألعاب", "text": "ألعاب"},
    "points": {"label": "⭐ نقاطي", "text": "نقاطي"},
    "leaderboard": {"label": "🏆 الصدارة", "text": "صدارة"},
    "achievements": {"label": "🎖️ الإنجازات", "text": "إنجازات"},
    "help": {"label": "❓ مساعدة", "text": "مساعدة"},
    "stop": {"label": "⛔ إيقاف", "text": "إيقاف"}
}

# ============================================================================
# Helper Functions
# ============================================================================
def get_username(profile) -> str:
    """Get username from LINE profile"""
    try:
        return profile.display_name
    except:
        return "مستخدم"

def get_theme_colors(theme_name: str = None) -> Dict[str, str]:
    """Get colors for a theme"""
    if theme_name is None:
        theme_name = DEFAULT_THEME
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])
