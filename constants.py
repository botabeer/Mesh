"""
Bot Mesh - Constants & Configuration v7.1
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

✅ 9 ثيمات زجاجية احترافية (رمادي بدلاً من سماوي)
✅ تصميم موحد بدون إيموجي زائد
✅ أداء محسّن
"""

import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "7.1"
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
# Professional Glass Themes - 9 ثيمات محسّنة
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
        "shadow2": "#F1F5F9",
        "button": "#3B82F6",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
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
        "shadow2": "#475569",
        "button": "#60A5FA",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
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
        "shadow2": "#DBEAFE",
        "button": "#2563EB",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "أخضر": {
        "name": "أخضر",
        "bg": "#F0FDF4",
        "card": "#FFFFFF",
        "primary": "#10B981",
        "secondary": "#34D399",
        "text": "#064E3B",
        "text2": "#059669",
        "shadow1": "#D1FAE5",
        "shadow2": "#A7F3D0",
        "button": "#10B981",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "وردي": {
        "name": "وردي",
        "bg": "#FDF2F8",
        "card": "#FFFFFF",
        "primary": "#EC4899",
        "secondary": "#F472B6",
        "text": "#831843",
        "text2": "#DB2777",
        "shadow1": "#FCE7F3",
        "shadow2": "#FBCFE8",
        "button": "#EC4899",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "بنفسجي": {
        "name": "بنفسجي",
        "bg": "#F5F3FF",
        "card": "#FFFFFF",
        "primary": "#8B5CF6",
        "secondary": "#A78BFA",
        "text": "#4C1D95",
        "text2": "#7C3AED",
        "shadow1": "#EDE9FE",
        "shadow2": "#DDD6FE",
        "button": "#8B5CF6",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "برتقالي": {
        "name": "برتقالي",
        "bg": "#FFF7ED",
        "card": "#FFFFFF",
        "primary": "#F97316",
        "secondary": "#FB923C",
        "text": "#7C2D12",
        "text2": "#EA580C",
        "shadow1": "#FFEDD5",
        "shadow2": "#FED7AA",
        "button": "#F97316",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "رمادي": {
        "name": "رمادي",
        "bg": "#F9FAFB",
        "card": "#FFFFFF",
        "primary": "#6B7280",
        "secondary": "#9CA3AF",
        "text": "#111827",
        "text2": "#6B7280",
        "shadow1": "#E5E7EB",
        "shadow2": "#D1D5DB",
        "button": "#6B7280",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "ذهبي": {
        "name": "ذهبي",
        "bg": "#FFFBEB",
        "card": "#FFFFFF",
        "primary": "#F59E0B",
        "secondary": "#FBBF24",
        "text": "#78350F",
        "text2": "#D97706",
        "shadow1": "#FEF3C7",
        "shadow2": "#FDE68A",
        "button": "#F59E0B",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    }
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# Games Configuration
# ============================================================================
GAME_LIST = {
    "أسرع": {
        "label": "أسرع",
        "command": "لعبة كتابة سريعة",
        "description": "اختبار سرعة الكتابة",
        "class": "FastTypingGame"
    },
    "ذكاء": {
        "label": "ذكاء",
        "command": "لعبة IQ",
        "description": "ألغاز ذكية",
        "class": "IqGame"
    },
    "لعبة": {
        "label": "لعبة",
        "command": "لعبة إنسان حيوان نبات",
        "description": "إنسان حيوان نبات جماد بلاد",
        "class": "HumanAnimalPlantGame"
    },
    "أغنية": {
        "label": "أغنية",
        "command": "لعبة أغنية",
        "description": "خمن المغني",
        "class": "SongGame"
    },
    "خمن": {
        "label": "خمن",
        "command": "لعبة تخمين",
        "description": "خمن الكلمة",
        "class": "GuessGame"
    },
    "سلسلة": {
        "label": "سلسلة",
        "command": "لعبة سلسلة كلمات",
        "description": "كلمة تبدأ بآخر حرف",
        "class": "ChainWordsGame"
    },
    "ترتيب": {
        "label": "ترتيب",
        "command": "لعبة كلمة مبعثرة",
        "description": "رتب الحروف",
        "class": "ScrambleWordGame"
    },
    "تكوين": {
        "label": "تكوين",
        "command": "لعبة حروف وكلمات",
        "description": "كون كلمات",
        "class": "LettersWordsGame"
    },
    "ضد": {
        "label": "ضد",
        "command": "لعبة عكس",
        "description": "اكتشف عكس الكلمة",
        "class": "OppositeGame"
    },
    "لون": {
        "label": "لون",
        "command": "لعبة لون الكلمة",
        "description": "اختبار Stroop",
        "class": "WordColorGame"
    },
    "رياضيات": {
        "label": "رياضيات",
        "command": "لعبة رياضيات",
        "description": "أسئلة حسابية",
        "class": "MathGame"
    },
    "توافق": {
        "label": "توافق",
        "command": "لعبة توافق",
        "description": "اختبار التوافق",
        "class": "CompatibilityGame"
    }
}

# ============================================================================
# Rate Limiting Configuration
# ============================================================================
RATE_LIMIT_CONFIG = {
    "max_requests": 10,
    "window_seconds": 60,
    "cleanup_interval": 300  # 5 minutes
}

# ============================================================================
# Game Configuration
# ============================================================================
GAME_CONFIG = {
    "questions_per_game": 5,
    "points_per_correct": 1,
    "timeout_seconds": 120,
    "max_active_games_per_user": 1
}

# ============================================================================
# Helper Functions
# ============================================================================
def get_username(profile) -> str:
    """Get username from LINE profile"""
    try:
        return profile.display_name if profile.display_name else "مستخدم"
    except:
        return "مستخدم"

def get_theme_colors(theme_name: str = None) -> Dict[str, str]:
    """Get colors for a theme with fallback"""
    if theme_name is None:
        theme_name = DEFAULT_THEME
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])

def validate_theme(theme_name: str) -> str:
    """Validate and return theme name"""
    return theme_name if theme_name in THEMES else DEFAULT_THEME
