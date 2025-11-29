"""
Bot Mesh - Constants v13.0 GLASS 3D
Created by: Abeer Aldosari © 2025
✅ ستايل زجاجي 3D احترافي شامل
✅ 9 ثيمات زجاجية مع تأثيرات متقدمة
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
BOT_VERSION = "13.0"
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
# GLASS 3D THEMES - 9 ثيمات زجاجية احترافية شاملة
# ============================================================================
THEMES = {
    "أبيض": {
        "name": "أبيض",
        "bg": "#F8FAFC",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_hover": "#F1F5F9",
        "primary": "#2563EB",
        "primary_hover": "#1D4ED8",
        "secondary": "#60A5FA",
        "accent": "#3B82F6",
        "text": "#0F172A",
        "text2": "#64748B",
        "text3": "#94A3B8",
        "border": "#E2E8F0",
        "border_focus": "#3B82F6",
        "success": "#10B981",
        "success_bg": "#D1FAE5",
        "error": "#EF4444",
        "error_bg": "#FEE2E2",
        "warning": "#F59E0B",
        "warning_bg": "#FEF3C7",
        "info": "#3B82F6",
        "info_bg": "#DBEAFE",
        "shadow": "rgba(59,130,246,0.15)",
        "shadow_lg": "rgba(59,130,246,0.25)",
        "overlay": "rgba(0,0,0,0.02)",
        "gradient": "linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%)"
    },
    "أسود": {
        "name": "أسود",
        "bg": "#0F172A",
        "card": "#1E293B",
        "glass": "#1E293B",
        "glass_hover": "#334155",
        "primary": "#60A5FA",
        "primary_hover": "#3B82F6",
        "secondary": "#93C5FD",
        "accent": "#60A5FA",
        "text": "#F8FAFC",
        "text2": "#CBD5E1",
        "text3": "#94A3B8",
        "border": "#334155",
        "border_focus": "#60A5FA",
        "success": "#34D399",
        "success_bg": "#064E3B",
        "error": "#F87171",
        "error_bg": "#7F1D1D",
        "warning": "#FBBF24",
        "warning_bg": "#78350F",
        "info": "#60A5FA",
        "info_bg": "#1E3A8A",
        "shadow": "rgba(96,165,250,0.15)",
        "shadow_lg": "rgba(96,165,250,0.25)",
        "overlay": "rgba(255,255,255,0.02)",
        "gradient": "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)"
    },
    "رمادي": {
        "name": "رمادي",
        "bg": "#F9FAFB",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_hover": "#F3F4F6",
        "primary": "#6B7280",
        "primary_hover": "#4B5563",
        "secondary": "#9CA3AF",
        "accent": "#6B7280",
        "text": "#111827",
        "text2": "#6B7280",
        "text3": "#9CA3AF",
        "border": "#E5E7EB",
        "border_focus": "#6B7280",
        "success": "#10B981",
        "success_bg": "#D1FAE5",
        "error": "#EF4444",
        "error_bg": "#FEE2E2",
        "warning": "#F59E0B",
        "warning_bg": "#FEF3C7",
        "info": "#6B7280",
        "info_bg": "#F3F4F6",
        "shadow": "rgba(107,114,128,0.15)",
        "shadow_lg": "rgba(107,114,128,0.25)",
        "overlay": "rgba(0,0,0,0.02)",
        "gradient": "linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%)"
    },
    "أزرق": {
        "name": "أزرق",
        "bg": "#EFF6FF",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_hover": "#DBEAFE",
        "primary": "#2563EB",
        "primary_hover": "#1D4ED8",
        "secondary": "#60A5FA",
        "accent": "#3B82F6",
        "text": "#1E3A8A",
        "text2": "#3B82F6",
        "text3": "#60A5FA",
        "border": "#DBEAFE",
        "border_focus": "#2563EB",
        "success": "#10B981",
        "success_bg": "#D1FAE5",
        "error": "#EF4444",
        "error_bg": "#FEE2E2",
        "warning": "#F59E0B",
        "warning_bg": "#FEF3C7",
        "info": "#2563EB",
        "info_bg": "#DBEAFE",
        "shadow": "rgba(37,99,235,0.2)",
        "shadow_lg": "rgba(37,99,235,0.3)",
        "overlay": "rgba(37,99,235,0.03)",
        "gradient": "linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)"
    },
    "بنفسجي": {
        "name": "بنفسجي",
        "bg": "#F5F3FF",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_hover": "#EDE9FE",
        "primary": "#7C3AED",
        "primary_hover": "#6D28D9",
        "secondary": "#A78BFA",
        "accent": "#8B5CF6",
        "text": "#4C1D95",
        "text2": "#7C3AED",
        "text3": "#A78BFA",
        "border": "#EDE9FE",
        "border_focus": "#7C3AED",
        "success": "#10B981",
        "success_bg": "#D1FAE5",
        "error": "#EF4444",
        "error_bg": "#FEE2E2",
        "warning": "#F59E0B",
        "warning_bg": "#FEF3C7",
        "info": "#7C3AED",
        "info_bg": "#EDE9FE",
        "shadow": "rgba(124,58,237,0.2)",
        "shadow_lg": "rgba(124,58,237,0.3)",
        "overlay": "rgba(124,58,237,0.03)",
        "gradient": "linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%)"
    },
    "وردي": {
        "name": "وردي",
        "bg": "#FDF2F8",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_hover": "#FCE7F3",
        "primary": "#DB2777",
        "primary_hover": "#BE185D",
        "secondary": "#EC4899",
        "accent": "#F472B6",
        "text": "#831843",
        "text2": "#DB2777",
        "text3": "#F472B6",
        "border": "#FCE7F3",
        "border_focus": "#DB2777",
        "success": "#10B981",
        "success_bg": "#D1FAE5",
        "error": "#EF4444",
        "error_bg": "#FEE2E2",
        "warning": "#F59E0B",
        "warning_bg": "#FEF3C7",
        "info": "#DB2777",
        "info_bg": "#FCE7F3",
        "shadow": "rgba(219,39,119,0.2)",
        "shadow_lg": "rgba(219,39,119,0.3)",
        "overlay": "rgba(219,39,119,0.03)",
        "gradient": "linear-gradient(135deg, #FDF2F8 0%, #FCE7F3 100%)"
    },
    "أخضر": {
        "name": "أخضر",
        "bg": "#F0FDF4",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_hover": "#DCFCE7",
        "primary": "#059669",
        "primary_hover": "#047857",
        "secondary": "#10B981",
        "accent": "#34D399",
        "text": "#064E3B",
        "text2": "#059669",
        "text3": "#34D399",
        "border": "#DCFCE7",
        "border_focus": "#059669",
        "success": "#10B981",
        "success_bg": "#D1FAE5",
        "error": "#EF4444",
        "error_bg": "#FEE2E2",
        "warning": "#F59E0B",
        "warning_bg": "#FEF3C7",
        "info": "#059669",
        "info_bg": "#DCFCE7",
        "shadow": "rgba(5,150,105,0.2)",
        "shadow_lg": "rgba(5,150,105,0.3)",
        "overlay": "rgba(5,150,105,0.03)",
        "gradient": "linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%)"
    },
    "برتقالي": {
        "name": "برتقالي",
        "bg": "#FFF7ED",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_hover": "#FFEDD5",
        "primary": "#EA580C",
        "primary_hover": "#C2410C",
        "secondary": "#F97316",
        "accent": "#FB923C",
        "text": "#7C2D12",
        "text2": "#EA580C",
        "text3": "#FB923C",
        "border": "#FFEDD5",
        "border_focus": "#EA580C",
        "success": "#10B981",
        "success_bg": "#D1FAE5",
        "error": "#EF4444",
        "error_bg": "#FEE2E2",
        "warning": "#F59E0B",
        "warning_bg": "#FEF3C7",
        "info": "#EA580C",
        "info_bg": "#FFEDD5",
        "shadow": "rgba(234,88,12,0.2)",
        "shadow_lg": "rgba(234,88,12,0.3)",
        "overlay": "rgba(234,88,12,0.03)",
        "gradient": "linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%)"
    },
    "بني": {
        "name": "بني",
        "bg": "#FFFCF7",
        "card": "#FFFFFF",
        "glass": "#FFFFFF",
        "glass_hover": "#F5E6D8",
        "primary": "#92400E",
        "primary_hover": "#78350F",
        "secondary": "#B45309",
        "accent": "#D97706",
        "text": "#451A03",
        "text2": "#92400E",
        "text3": "#D97706",
        "border": "#F5E6D8",
        "border_focus": "#92400E",
        "success": "#10B981",
        "success_bg": "#D1FAE5",
        "error": "#EF4444",
        "error_bg": "#FEE2E2",
        "warning": "#F59E0B",
        "warning_bg": "#FEF3C7",
        "info": "#92400E",
        "info_bg": "#F5E6D8",
        "shadow": "rgba(146,64,14,0.2)",
        "shadow_lg": "rgba(146,64,14,0.3)",
        "overlay": "rgba(146,64,14,0.03)",
        "gradient": "linear-gradient(135deg, #FFFCF7 0%, #F5E6D8 100%)"
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
# Privacy & Security Settings - محسّنة
# ============================================================================
PRIVACY_SETTINGS = {
    "auto_delete_inactive_days": 30,
    "cache_timeout_minutes": 10,  # زيادة من 5 إلى 10
    "cleanup_interval_hours": 24,
    "max_sessions_per_user": 5,  # زيادة من 3 إلى 5
    "session_timeout_minutes": 45  # زيادة من 30 إلى 45
}

SECURITY_SETTINGS = {
    "rate_limit_requests": 20,  # زيادة من 15 إلى 20
    "rate_limit_window_seconds": 60,
    "max_message_length": 1000,  # زيادة من 500 إلى 1000
    "max_game_duration_minutes": 20,  # زيادة من 15 إلى 20
    "enable_sql_injection_protection": True,
    "enable_xss_protection": True,
    "enable_csrf_protection": True,
    "enable_rate_limiting": True
}

# ============================================================================
# Bot Commands - موسّعة
# ============================================================================
ALLOWED_COMMANDS = {
    "مساعدة", "help", "؟",
    "بداية", "home", "الرئيسية", "start",
    "ألعاب", "games", "العاب",
    "نقاطي", "points", "نقاط",
    "صدارة", "leaderboard", "مستوى",
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
# Helper Functions - محسّنة
# ============================================================================

def normalize_text(text: str) -> str:
    """Normalize Arabic text with security"""
    if not text or not isinstance(text, str):
        return ""
    
    text = text[:SECURITY_SETTINGS["max_message_length"]]
    text = text.strip().lower()
    
    replacements = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
        'ى': 'ي', 'ة': 'ه',
        'ؤ': 'و', 'ئ': 'ي'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    
    if SECURITY_SETTINGS["enable_xss_protection"]:
        text = re.sub(r'[<>"\']', '', text)
    
    return text


def sanitize_input(text: str) -> str:
    """Sanitize user input for security"""
    if not text:
        return ""
    
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
