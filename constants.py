"""
Bot Mesh - Constants & Configuration v7.0
تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025

✅ 9 ثيمات زجاجية احترافية
✅ تصميم موحد لجميع الألعاب
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
# Professional Glass Themes - 9 ثيمات زجاجية احترافية
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
        "shadow2": "#FFFFFF",
        "button": "#10B981",
        "success": "#10B981",
        "error": "#EF4444"
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
        "shadow2": "#FFFFFF",
        "button": "#EC4899",
        "success": "#10B981",
        "error": "#EF4444"
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
        "shadow2": "#FFFFFF",
        "button": "#8B5CF6",
        "success": "#10B981",
        "error": "#EF4444"
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
        "shadow2": "#FFFFFF",
        "button": "#F97316",
        "success": "#10B981",
        "error": "#EF4444"
    },
    "سماوي": {
        "name": "سماوي",
        "bg": "#ECFEFF",
        "card": "#FFFFFF",
        "primary": "#06B6D4",
        "secondary": "#22D3EE",
        "text": "#164E63",
        "text2": "#0891B2",
        "shadow1": "#CFFAFE",
        "shadow2": "#FFFFFF",
        "button": "#06B6D4",
        "success": "#10B981",
        "error": "#EF4444"
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
        "shadow2": "#FFFFFF",
        "button": "#F59E0B",
        "success": "#10B981",
        "error": "#EF4444"
    }
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# Games List
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
# Fixed Buttons
# ============================================================================
FIXED_BUTTONS = {
    "home": {"label": "البداية", "text": "بداية"},
    "games": {"label": "الألعاب", "text": "ألعاب"},
    "points": {"label": "نقاطي", "text": "نقاطي"},
    "leaderboard": {"label": "الصدارة", "text": "صدارة"},
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
