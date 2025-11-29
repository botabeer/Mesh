"""
Bot Mesh - Constants & Configuration v12.0 FINAL
Created by: Abeer Aldosari © 2025
✅ أمان محسّن
✅ ألوان زجاجية 3D احترافية
✅ متوافق 100% مع LINE API v3
"""

import os
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
import re

load_dotenv()

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "12.0"
BOT_RIGHTS = "© 2025 Abeer Aldosari - All Rights Reserved"

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
# Glass 3D Themes - 9 ثيمات زجاجية احترافية
# ============================================================================
THEMES = {
    "أبيض": {
        "name": "أبيض",
        "bg": "#F8FAFC",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "primary": "#2563EB",
        "secondary": "#60A5FA",
        "text": "#0F172A",
        "text2": "#64748B",
        "border": "#E2E8F0",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow": "rgba(59,130,246,0.15)"
    },
    "أسود": {
        "name": "أسود",
        "bg": "#0F172A",
        "card": "#1E293B",
        "glass": "#1E293B",
        "primary": "#60A5FA",
        "secondary": "#93C5FD",
        "text": "#F8FAFC",
        "text2": "#CBD5E1",
        "border": "#334155",
        "success": "#34D399",
        "error": "#F87171",
        "warning": "#FBBF24",
        "shadow": "rgba(96,165,250,0.15)"
    },
    "رمادي": {
        "name": "رمادي",
        "bg": "#F9FAFB",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "primary": "#6B7280",
        "secondary": "#9CA3AF",
        "text": "#111827",
        "text2": "#6B7280",
        "border": "#E5E7EB",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow": "rgba(107,114,128,0.15)"
    },
    "أزرق": {
        "name": "أزرق",
        "bg": "#EFF6FF",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "primary": "#2563EB",
        "secondary": "#60A5FA",
        "text": "#1E3A8A",
        "text2": "#3B82F6",
        "border": "#DBEAFE",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow": "rgba(37,99,235,0.15)"
    },
    "بنفسجي": {
        "name": "بنفسجي",
        "bg": "#F5F3FF",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "primary": "#7C3AED",
        "secondary": "#A78BFA",
        "text": "#4C1D95",
        "text2": "#7C3AED",
        "border": "#EDE9FE",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow": "rgba(124,58,237,0.15)"
    },
    "وردي": {
        "name": "وردي",
        "bg": "#FDF2F8",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "primary": "#DB2777",
        "secondary": "#EC4899",
        "text": "#831843",
        "text2": "#DB2777",
        "border": "#FCE7F3",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow": "rgba(219,39,119,0.15)"
    },
    "أخضر": {
        "name": "أخضر",
        "bg": "#F0FDF4",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "primary": "#059669",
        "secondary": "#10B981",
        "text": "#064E3B",
        "text2": "#059669",
        "border": "#DCFCE7",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow": "rgba(5,150,105,0.15)"
    },
    "برتقالي": {
        "name": "برتقالي",
        "bg": "#FFF7ED",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "primary": "#EA580C",
        "secondary": "#F97316",
        "text": "#7C2D12",
        "text2": "#EA580C",
        "border": "#FFEDD5",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow": "rgba(234,88,12,0.15)"
    },
    "بني": {
        "name": "بني",
        "bg": "#FFFCF7",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "primary": "#92400E",
        "secondary": "#B45309",
        "text": "#451A03",
        "text2": "#92400E",
        "border": "#F5E6D8",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "shadow": "rgba(146,64,14,0.15)"
    }
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# Games Configuration
# ============================================================================
GAME_LIST: List[Tuple[str, str, str]] = [
    ("fast_typing", "كتابة سريعة", "⚡"),
    ("iq", "ذكاء", "🧠"),
    ("guess", "تخمين", "🔮"),
    ("song", "أغنية", "🎵"),
    ("human_animal_plant", "إنسان حيوان نبات", "🌿"),
    ("chain_words", "سلسلة كلمات", "🔗"),
    ("opposite", "أضداد", "↔️"),
    ("letters_words", "تكوين", "📝"),
    ("scramble_word", "كلمة مبعثرة", "🔤"),
    ("compatibility", "توافق", "💕"),
    ("math", "رياضيات", "🔢"),
    ("word_color", "لون", "🎨")
]

GAME_NAMES = {internal: display for internal, display, icon in GAME_LIST}
GAME_ICONS = {internal: icon for internal, display, icon in GAME_LIST}

# ============================================================================
# Quick Reply Items
# ============================================================================
FIXED_GAME_QR = [
    {"label": f"{icon} {display}", "text": display}
    for internal, display, icon in GAME_LIST
]

# ============================================================================
# Privacy & Security Settings
# ============================================================================
PRIVACY_SETTINGS = {
    "auto_delete_inactive_days": 30,
    "cache_timeout_minutes": 5,
    "cleanup_interval_hours": 24,
    "max_sessions_per_user": 3,
    "session_timeout_minutes": 30
}

SECURITY_SETTINGS = {
    "rate_limit_requests": 15,
    "rate_limit_window_seconds": 60,
    "max_message_length": 500,
    "max_game_duration_minutes": 15,
    "enable_sql_injection_protection": True,
    "enable_xss_protection": True
}

# ============================================================================
# Bot Commands
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

GAME_COMMANDS = set(GAME_NAMES.values())

# ============================================================================
# Helper Functions
# ============================================================================

def normalize_text(text: str) -> str:
    """Normalize Arabic text with security"""
    if not text or not isinstance(text, str):
        return ""
    
    # Security: limit length
    text = text[:SECURITY_SETTINGS["max_message_length"]]
    
    text = text.strip().lower()
    
    # Arabic normalization
    replacements = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
        'ى': 'ي', 'ة': 'ه',
        'ؤ': 'و', 'ئ': 'ي'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove diacritics
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    
    # Security: remove dangerous characters
    if SECURITY_SETTINGS["enable_xss_protection"]:
        text = re.sub(r'[<>"\']', '', text)
    
    return text


def sanitize_input(text: str) -> str:
    """Sanitize user input for security"""
    if not text:
        return ""
    
    # SQL injection protection
    if SECURITY_SETTINGS["enable_sql_injection_protection"]:
        dangerous_patterns = [
            r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b',
            r'[;\'"\\]',
            r'--',
            r'/\*',
            r'\*/'
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return ""
    
    return text[:SECURITY_SETTINGS["max_message_length"]]


def get_theme_colors(theme_name: Optional[str] = None) -> Dict[str, str]:
    """Get theme colors dictionary"""
    if theme_name is None:
        theme_name = DEFAULT_THEME
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])


def validate_theme(theme_name: str) -> str:
    """Validate theme name"""
    return theme_name if theme_name in THEMES else DEFAULT_THEME


def get_username(profile) -> str:
    """Extract username from LINE profile with security"""
    try:
        name = profile.display_name if hasattr(profile, 'display_name') else "مستخدم"
        if not name or not isinstance(name, str):
            return "مستخدم"
        
        # Sanitize username
        name = sanitize_input(name)
        return name[:50] if name else "مستخدم"
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
    if not text or not isinstance(text, str):
        return False
    
    lowered = text.lower().strip()
    
    if lowered in ALLOWED_COMMANDS:
        return True
    
    if text.strip() in GAME_COMMANDS:
        return True
    
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
    'FIXED_GAME_QR', 'PRIVACY_SETTINGS', 'SECURITY_SETTINGS',
    'ALLOWED_COMMANDS', 'GAME_COMMANDS',
    'validate_env', 'normalize_text', 'sanitize_input',
    'get_theme_colors', 'validate_theme', 'get_username',
    'get_game_display_name', 'get_game_icon',
    'is_valid_game', 'is_allowed_command'
]
