"""
Bot Mesh - Constants & Configuration v7.0
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

✅ Professional 3D Glass Design
✅ Minimal Emojis
✅ Groups Optimized
"""

import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "7.0"
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

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
# Professional 3D Glass Themes (Minimal Colors)
# ============================================================================
THEMES = {
    "أبيض": {
        "name": "أبيض",
        "bg": "#F8FAFC",
        "card": "#FFFFFF",
        "primary": "#3B82F6",
        "secondary": "#60A5FA",
        "text": "#1E293B",
        "text2": "#64748B",
        "shadow1": "#E2E8F0",
        "shadow2": "#FFFFFF",
        "button": "#3B82F6",
        "success": "#10B981",
        "error": "#EF4444"
    },
    "أسود": {
        "name": "أسود",
        "bg": "#0F172A",
        "card": "#1E293B",
        "primary": "#60A5FA",
        "secondary": "#93C5FD",
        "text": "#F1F5F9",
        "text2": "#CBD5E1",
        "shadow1": "#334155",
        "shadow2": "#1E293B",
        "button": "#60A5FA",
        "success": "#10B981",
        "error": "#EF4444"
    },
    "أزرق": {
        "name": "أزرق",
        "bg": "#EFF6FF",
        "card": "#FFFFFF",
        "primary": "#2563EB",
        "secondary": "#3B82F6",
        "text": "#1E3A8A",
        "text2": "#3B82F6",
        "shadow1": "#BFDBFE",
        "shadow2": "#FFFFFF",
        "button": "#2563EB",
        "success": "#10B981",
        "error": "#EF4444"
    }
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# Games List - Clean Labels (Minimal Emojis)
# ============================================================================
GAME_LIST = {
    "أسرع": {
        "label": "أسرع",
        "command": "لعبة كتابة سريعة",
        "description": "اختبار سرعة الكتابة"
    },
    "ذكاء": {
        "label": "ذكاء",
        "command": "لعبة IQ",
        "description": "ألغاز ذكية"
    },
    "لعبة": {
        "label": "لعبة",
        "command": "لعبة إنسان حيوان نبات",
        "description": "إنسان حيوان نبات جماد بلاد"
    },
    "أغنية": {
        "label": "أغنية",
        "command": "لعبة أغنية",
        "description": "خمن المغني"
    },
    "خمن": {
        "label": "خمن",
        "command": "لعبة تخمين",
        "description": "خمن الكلمة"
    },
    "سلسلة": {
        "label": "سلسلة",
        "command": "لعبة سلسلة كلمات",
        "description": "كلمة تبدأ بآخر حرف"
    },
    "ترتيب": {
        "label": "ترتيب",
        "command": "لعبة كلمة مبعثرة",
        "description": "رتب الحروف"
    },
    "تكوين": {
        "label": "تكوين",
        "command": "لعبة حروف وكلمات",
        "description": "كون كلمات"
    },
    "ضد": {
        "label": "ضد",
        "command": "لعبة عكس",
        "description": "اكتشف عكس الكلمة"
    },
    "لون": {
        "label": "لون",
        "command": "لعبة لون الكلمة",
        "description": "اختبار Stroop"
    },
    "رياضيات": {
        "label": "رياضيات",
        "command": "لعبة رياضيات",
        "description": "أسئلة حسابية"
    },
    "توافق": {
        "label": "توافق",
        "command": "لعبة توافق",
        "description": "اختبار التوافق"
    }
}

# ============================================================================
# Fixed Buttons (Minimal Emojis)
# ============================================================================
FIXED_BUTTONS = {
    "home": {"label": "البداية", "text": "بداية"},
    "games": {"label": "الألعاب", "text": "ألعاب"},
    "points": {"label": "نقاطي", "text": "نقاطي"},
    "leaderboard": {"label": "الصدارة", "text": "صدارة"},
    "groups": {"label": "المجموعة", "text": "مجموعة"},
    "help": {"label": "مساعدة", "text": "مساعدة"},
    "stop": {"label": "إيقاف", "text": "إيقاف"}
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
