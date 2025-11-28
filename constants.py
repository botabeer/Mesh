"""
Bot Mesh - Constants & Configuration v8.0
Created by: Abeer Aldosari © 2025
✅ تصميم زجاجي ثلاثي الأبعاد
✅ 9 ثيمات احترافية
✅ بدون إيموجي إلا للضرورة
"""

import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "8.0"
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
# Glass 3D Themes - 9 ثيمات زجاجية ثلاثية الأبعاد
# ============================================================================
THEMES = {
    "أبيض": {
        "name": "أبيض",
        "bg": "linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255, 255, 255, 0.85)",
        "primary": "#3B82F6",
        "secondary": "#60A5FA",
        "text": "#1E293B",
        "text2": "#64748B",
        "shadow": "0 8px 32px rgba(59, 130, 246, 0.15)",
        "border": "rgba(59, 130, 246, 0.1)",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "أسود": {
        "name": "أسود",
        "bg": "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)",
        "card": "#1E293B",
        "glass": "rgba(30, 41, 59, 0.85)",
        "primary": "#60A5FA",
        "secondary": "#93C5FD",
        "text": "#F1F5F9",
        "text2": "#CBD5E1",
        "shadow": "0 8px 32px rgba(96, 165, 250, 0.15)",
        "border": "rgba(96, 165, 250, 0.1)",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "أزرق": {
        "name": "أزرق",
        "bg": "linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255, 255, 255, 0.85)",
        "primary": "#2563EB",
        "secondary": "#3B82F6",
        "text": "#1E3A8A",
        "text2": "#3B82F6",
        "shadow": "0 8px 32px rgba(37, 99, 235, 0.15)",
        "border": "rgba(37, 99, 235, 0.1)",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "أخضر": {
        "name": "أخضر",
        "bg": "linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255, 255, 255, 0.85)",
        "primary": "#10B981",
        "secondary": "#34D399",
        "text": "#064E3B",
        "text2": "#059669",
        "shadow": "0 8px 32px rgba(16, 185, 129, 0.15)",
        "border": "rgba(16, 185, 129, 0.1)",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "وردي": {
        "name": "وردي",
        "bg": "linear-gradient(135deg, #FDF2F8 0%, #FCE7F3 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255, 255, 255, 0.85)",
        "primary": "#EC4899",
        "secondary": "#F472B6",
        "text": "#831843",
        "text2": "#DB2777",
        "shadow": "0 8px 32px rgba(236, 72, 153, 0.15)",
        "border": "rgba(236, 72, 153, 0.1)",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "بنفسجي": {
        "name": "بنفسجي",
        "bg": "linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255, 255, 255, 0.85)",
        "primary": "#8B5CF6",
        "secondary": "#A78BFA",
        "text": "#4C1D95",
        "text2": "#7C3AED",
        "shadow": "0 8px 32px rgba(139, 92, 246, 0.15)",
        "border": "rgba(139, 92, 246, 0.1)",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "برتقالي": {
        "name": "برتقالي",
        "bg": "linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255, 255, 255, 0.85)",
        "primary": "#F97316",
        "secondary": "#FB923C",
        "text": "#7C2D12",
        "text2": "#EA580C",
        "shadow": "0 8px 32px rgba(249, 115, 22, 0.15)",
        "border": "rgba(249, 115, 22, 0.1)",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "رمادي": {
        "name": "رمادي",
        "bg": "linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255, 255, 255, 0.85)",
        "primary": "#6B7280",
        "secondary": "#9CA3AF",
        "text": "#111827",
        "text2": "#6B7280",
        "shadow": "0 8px 32px rgba(107, 114, 128, 0.15)",
        "border": "rgba(107, 114, 128, 0.1)",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B"
    },
    "ذهبي": {
        "name": "ذهبي",
        "bg": "linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255, 255, 255, 0.85)",
        "primary": "#F59E0B",
        "secondary": "#FBBF24",
        "text": "#78350F",
        "text2": "#D97706",
        "shadow": "0 8px 32px rgba(245, 158, 11, 0.15)",
        "border": "rgba(245, 158, 11, 0.1)",
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
    "أسرع": {"label": "أسرع", "command": "لعبة كتابة سريعة", "description": "اختبار سرعة الكتابة"},
    "ذكاء": {"label": "ذكاء", "command": "لعبة IQ", "description": "ألغاز ذكية"},
    "لعبة": {"label": "لعبة", "command": "لعبة إنسان حيوان نبات", "description": "إنسان حيوان نبات جماد بلاد"},
    "أغنية": {"label": "أغنية", "command": "لعبة أغنية", "description": "خمن المغني"},
    "خمن": {"label": "خمن", "command": "لعبة تخمين", "description": "خمن الكلمة"},
    "سلسلة": {"label": "سلسلة", "command": "لعبة سلسلة كلمات", "description": "كلمة تبدأ بآخر حرف"},
    "ترتيب": {"label": "ترتيب", "command": "لعبة كلمة مبعثرة", "description": "رتب الحروف"},
    "تكوين": {"label": "تكوين", "command": "لعبة حروف وكلمات", "description": "كون كلمات"},
    "ضد": {"label": "ضد", "command": "لعبة عكس", "description": "اكتشف عكس الكلمة"},
    "لون": {"label": "لون", "command": "لعبة لون الكلمة", "description": "اختبار Stroop"},
    "رياضيات": {"label": "رياضيات", "command": "لعبة رياضيات", "description": "أسئلة حسابية"},
    "توافق": {"label": "توافق", "command": "لعبة توافق", "description": "اختبار التوافق"}
}

# ============================================================================
# Rate Limiting Configuration
# ============================================================================
RATE_LIMIT_CONFIG = {
    "max_requests": 10,
    "window_seconds": 60,
    "cleanup_interval": 300
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
