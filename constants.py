"""
Bot Mesh - Constants & Configuration v11.2 FINAL
Created by: Abeer Aldosari © 2025
✅ ألوان محسّنة للوضوح
✅ إيموجي مبسطة
✅ متوافق مع جميع الألعاب
"""

import os
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "11.2"
BOT_RIGHTS = "© 2025 Abeer Aldosari"

# ============================================================================
# LINE Configuration
# ============================================================================
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def validate_env():
    """Validate environment variables"""
    if not LINE_CHANNEL_SECRET:
        raise ValueError("LINE_CHANNEL_SECRET is not set")
    if not LINE_CHANNEL_ACCESS_TOKEN:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set")

# ============================================================================
# Glass 3D Themes (9 Themes) - ألوان محسّنة للوضوح
# ============================================================================
THEMES = {
    "أبيض": {
        "name": "أبيض",
        "bg": "linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255,255,255,0.85)",
        "primary": "#2563EB",
        "secondary": "#60A5FA",
        "text": "#0F172A",
        "text2": "#475569",
        "shadow": "0 8px 32px rgba(59,130,246,0.15)",
        "shadow1": "rgba(59,130,246,0.1)",
        "border": "rgba(59,130,246,0.1)",
        "success": "#059669",
        "error": "#DC2626",
        "warning": "#D97706"
    },
    "أسود": {
        "name": "أسود",
        "bg": "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)",
        "card": "#1E293B",
        "glass": "rgba(30,41,59,0.85)",
        "primary": "#60A5FA",
        "secondary": "#93C5FD",
        "text": "#F8FAFC",
        "text2": "#CBD5E1",
        "shadow": "0 8px 32px rgba(96,165,250,0.15)",
        "shadow1": "rgba(96,165,250,0.1)",
        "border": "rgba(96,165,250,0.1)",
        "success": "#34D399",
        "error": "#F87171",
        "warning": "#FBBF24"
    },
    "رمادي": {
        "name": "رمادي",
        "bg": "linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255,255,255,0.85)",
        "primary": "#374151",
        "secondary": "#6B7280",
        "text": "#111827",
        "text2": "#6B7280",
        "shadow": "0 8px 32px rgba(107,114,128,0.15)",
        "shadow1": "rgba(107,114,128,0.1)",
        "border": "rgba(107,114,128,0.1)",
        "success": "#059669",
        "error": "#DC2626",
        "warning": "#D97706"
    },
    "أزرق": {
        "name": "أزرق",
        "bg": "linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255,255,255,0.85)",
        "primary": "#1E40AF",
        "secondary": "#2563EB",
        "text": "#1E3A8A",
        "text2": "#3B82F6",
        "shadow": "0 8px 32px rgba(37,99,235,0.15)",
        "shadow1": "rgba(37,99,235,0.1)",
        "border": "rgba(37,99,235,0.1)",
        "success": "#059669",
        "error": "#DC2626",
        "warning": "#D97706"
    },
    "بنفسجي": {
        "name": "بنفسجي",
        "bg": "linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255,255,255,0.85)",
        "primary": "#6D28D9",
        "secondary": "#8B5CF6",
        "text": "#4C1D95",
        "text2": "#7C3AED",
        "shadow": "0 8px 32px rgba(139,92,246,0.15)",
        "shadow1": "rgba(139,92,246,0.1)",
        "border": "rgba(139,92,246,0.1)",
        "success": "#059669",
        "error": "#DC2626",
        "warning": "#D97706"
    },
    "وردي": {
        "name": "وردي",
        "bg": "linear-gradient(135deg, #FDF2F8 0%, #FCE7F3 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255,255,255,0.85)",
        "primary": "#BE185D",
        "secondary": "#EC4899",
        "text": "#831843",
        "text2": "#DB2777",
        "shadow": "0 8px 32px rgba(236,72,153,0.15)",
        "shadow1": "rgba(236,72,153,0.1)",
        "border": "rgba(236,72,153,0.1)",
        "success": "#059669",
        "error": "#DC2626",
        "warning": "#D97706"
    },
    "أخضر": {
        "name": "أخضر",
        "bg": "linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255,255,255,0.85)",
        "primary": "#047857",
        "secondary": "#10B981",
        "text": "#064E3B",
        "text2": "#059669",
        "shadow": "0 8px 32px rgba(16,185,129,0.15)",
        "shadow1": "rgba(16,185,129,0.1)",
        "border": "rgba(16,185,129,0.1)",
        "success": "#059669",
        "error": "#DC2626",
        "warning": "#D97706"
    },
    "برتقالي": {
        "name": "برتقالي",
        "bg": "linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255,255,255,0.85)",
        "primary": "#C2410C",
        "secondary": "#F97316",
        "text": "#7C2D12",
        "text2": "#EA580C",
        "shadow": "0 8px 32px rgba(249,115,22,0.15)",
        "shadow1": "rgba(249,115,22,0.1)",
        "border": "rgba(249,115,22,0.1)",
        "success": "#059669",
        "error": "#DC2626",
        "warning": "#D97706"
    },
    "بني": {
        "name": "بني",
        "bg": "linear-gradient(135deg, #FFFCF7 0%, #F5E6D8 100%)",
        "card": "#FFFFFF",
        "glass": "rgba(255,255,255,0.85)",
        "primary": "#78350F",
        "secondary": "#92400E",
        "text": "#451A03",
        "text2": "#92400E",
        "shadow": "0 8px 32px rgba(138,75,16,0.15)",
        "shadow1": "rgba(138,75,16,0.1)",
        "border": "rgba(138,75,16,0.1)",
        "success": "#059669",
        "error": "#DC2626",
        "warning": "#D97706"
    }
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# Games Configuration
# ============================================================================
GAME_LIST: List[Tuple[str, str, str]] = [
    ("fast_typing", "كتابة سريعة", "⚡"),
    ("iq", "ذكاء", "🧠"),
    ("human_animal_plant", "إنسان حيوان نبات", "🌿"),
    ("song", "أغنية", "🎵"),
    ("guess", "تخمين", "🔮"),
    ("chain_words", "سلسلة كلمات", "🔗"),
    ("scramble_word", "كلمة مبعثرة", "🔤"),
    ("letters_words", "تكوين", "📝"),
    ("opposite", "أضداد", "↔️"),
    ("word_color", "لون", "🎨"),
    ("math", "رياضيات", "🔢"),
    ("compatibility", "توافق", "💕")
]

# Game names mapping
GAME_NAMES = {internal: display for internal, display, icon in GAME_LIST}
GAME_ICONS = {internal: icon for internal, display, icon in GAME_LIST}

# ============================================================================
# Quick Reply Items (Games Only)
# ============================================================================
FIXED_GAME_QR = [
    {"label": f"{icon} {display}", "text": display}
    for internal, display, icon in GAME_LIST
]

# ============================================================================
# Privacy Settings
# ============================================================================
PRIVACY_SETTINGS = {
    "auto_delete_inactive_days": 30,  # حذف تلقائي بعد شهر من عدم النشاط
    "cache_timeout_minutes": 5,       # مدة الكاش
    "cleanup_interval_hours": 24      # تنظيف يومي
}

# ============================================================================
# Bot Commands (الأوامر المسموحة فقط)
# ============================================================================
ALLOWED_COMMANDS = {
    "مساعدة", "help", "؟",
    "بداية", "home", "الرئيسية", "start",
    "ألعاب", "games", "العاب",
    "نقاطي", "points", "نقاط",
    "صدارة", "leaderboard", "ترتيب",
    "انضم", "join", "تسجيل",
    "انسحب", "leave", "خروج",
    "فريقين", "teams", "فرق",
    "ثيمات", "themes", "مظهر",
    "إيقاف", "stop", "انهاء",
    "لمح", "hint",
    "جاوب", "reveal", "answer"
}

# أوامر الألعاب
GAME_COMMANDS = set(GAME_NAMES.values())

# ============================================================================
# Helper Functions
# ============================================================================

def normalize_text(text: str) -> str:
    """Normalize Arabic text for comparison"""
    if not text:
        return ""
    
    text = text.strip().lower()
    
    # Arabic character replacements
    replacements = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
        'ى': 'ي', 'ة': 'ه',
        'ؤ': 'و', 'ئ': 'ي'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove diacritics
    import re
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    
    return text


def get_theme_colors(theme_name: Optional[str] = None) -> Dict[str, str]:
    """Get theme colors dictionary"""
    if theme_name is None:
        theme_name = DEFAULT_THEME
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])


def validate_theme(theme_name: str) -> str:
    """Validate theme name and return valid theme"""
    return theme_name if theme_name in THEMES else DEFAULT_THEME


def get_username(profile) -> str:
    """Extract username from LINE profile"""
    try:
        return profile.display_name if hasattr(profile, 'display_name') and profile.display_name else "مستخدم"
    except:
        return "مستخدم"


def get_game_display_name(internal_name: str) -> str:
    """Get display name for game"""
    return GAME_NAMES.get(internal_name, internal_name)


def get_game_icon(internal_name: str) -> str:
    """Get icon for game"""
    return GAME_ICONS.get(internal_name, "▪️")


def is_valid_game(game_name: str) -> bool:
    """Check if game name is valid"""
    return game_name in GAME_NAMES.values()


def is_allowed_command(text: str) -> bool:
    """Check if text is an allowed command"""
    lowered = text.lower().strip()
    
    # تحقق من الأوامر الأساسية
    if lowered in ALLOWED_COMMANDS:
        return True
    
    # تحقق من أوامر الألعاب
    if text.strip() in GAME_COMMANDS:
        return True
    
    # تحقق من أوامر الثيمات
    if lowered.startswith("ثيم "):
        return True
    
    return False


# ============================================================================
# Export All
# ============================================================================
__all__ = [
    'BOT_NAME', 'BOT_VERSION', 'BOT_RIGHTS',
    'LINE_CHANNEL_SECRET', 'LINE_CHANNEL_ACCESS_TOKEN',
    'THEMES', 'DEFAULT_THEME',
    'GAME_LIST', 'GAME_NAMES', 'GAME_ICONS',
    'FIXED_GAME_QR', 'PRIVACY_SETTINGS',
    'ALLOWED_COMMANDS', 'GAME_COMMANDS',
    'validate_env', 'normalize_text', 'get_theme_colors',
    'validate_theme', 'get_username', 'get_game_display_name',
    'get_game_icon', 'is_valid_game', 'is_allowed_command'
]
