"""
Bot Mesh - Constants v14.0 PRO
Created by: Abeer Aldosari © 2025
✅ ألوان احترافية صحيحة
✅ تباين عالي للقراءة
✅ تطبيق ذكي للثيمات
"""

import os
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
import re

load_dotenv()

BOT_NAME = "Bot Mesh"
BOT_VERSION = "14.0 PRO"
BOT_RIGHTS = "© 2025 Abeer Aldosari"

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def validate_env():
    if not LINE_CHANNEL_SECRET:
        raise ValueError("LINE_CHANNEL_SECRET is not set")
    if not LINE_CHANNEL_ACCESS_TOKEN:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set")

# ============================================================================
# THEMES - ألوان احترافية محسّنة
# ============================================================================
THEMES = {
    "أبيض": {
        "name": "أبيض",
        "bg": "#FFFFFF",
        "card": "#FAFAFA",
        "primary": "#2563EB",
        "primary_hover": "#1D4ED8",
        "secondary": "#64748B",
        "accent": "#3B82F6",
        "text": "#0F172A",
        "text2": "#334155",
        "text3": "#64748B",
        "border": "#E2E8F0",
        "success": "#10B981",
        "success_bg": "#D1FAE5",
        "error": "#EF4444",
        "error_bg": "#FEE2E2",
        "warning": "#F59E0B",
        "info": "#3B82F6",
        "info_bg": "#DBEAFE"
    },
    "أسود": {
        "name": "أسود",
        "bg": "#0A0A0A",
        "card": "#1A1A1A",
        "primary": "#60A5FA",
        "primary_hover": "#93C5FD",
        "secondary": "#94A3B8",
        "accent": "#3B82F6",
        "text": "#F8FAFC",
        "text2": "#E2E8F0",
        "text3": "#CBD5E1",
        "border": "#334155",
        "success": "#34D399",
        "success_bg": "#065F46",
        "error": "#F87171",
        "error_bg": "#7F1D1D",
        "warning": "#FBBF24",
        "info": "#60A5FA",
        "info_bg": "#1E3A8A"
    },
    "أزرق": {
        "name": "أزرق",
        "bg": "#EFF6FF",
        "card": "#DBEAFE",
        "primary": "#1E40AF",
        "primary_hover": "#1E3A8A",
        "secondary": "#3B82F6",
        "accent": "#2563EB",
        "text": "#1E3A8A",
        "text2": "#1E40AF",
        "text3": "#3B82F6",
        "border": "#93C5FD",
        "success": "#059669",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#1E40AF",
        "info_bg": "#DBEAFE"
    },
    "أخضر": {
        "name": "أخضر",
        "bg": "#F0FDF4",
        "card": "#DCFCE7",
        "primary": "#059669",
        "primary_hover": "#047857",
        "secondary": "#10B981",
        "accent": "#34D399",
        "text": "#064E3B",
        "text2": "#065F46",
        "text3": "#047857",
        "border": "#86EFAC",
        "success": "#10B981",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#059669",
        "info_bg": "#DCFCE7"
    },
    "وردي": {
        "name": "وردي",
        "bg": "#FDF2F8",
        "card": "#FCE7F3",
        "primary": "#BE185D",
        "primary_hover": "#9F1239",
        "secondary": "#DB2777",
        "accent": "#EC4899",
        "text": "#831843",
        "text2": "#9F1239",
        "text3": "#BE185D",
        "border": "#F9A8D4",
        "success": "#059669",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#BE185D",
        "info_bg": "#FCE7F3"
    },
    "بنفسجي": {
        "name": "بنفسجي",
        "bg": "#F5F3FF",
        "card": "#EDE9FE",
        "primary": "#7C3AED",
        "primary_hover": "#6B21A8",
        "secondary": "#8B5CF6",
        "accent": "#A78BFA",
        "text": "#5B21B6",
        "text2": "#6B21A8",
        "text3": "#7C3AED",
        "border": "#C4B5FD",
        "success": "#059669",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#7C3AED",
        "info_bg": "#EDE9FE"
    },
    "برتقالي": {
        "name": "برتقالي",
        "bg": "#FFF7ED",
        "card": "#FFEDD5",
        "primary": "#EA580C",
        "primary_hover": "#C2410C",
        "secondary": "#F97316",
        "accent": "#FB923C",
        "text": "#7C2D12",
        "text2": "#9A3412",
        "text3": "#C2410C",
        "border": "#FDBA74",
        "success": "#059669",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#EA580C",
        "info_bg": "#FFEDD5"
    },
    "ذهبي": {
        "name": "ذهبي",
        "bg": "#FFFBEB",
        "card": "#FEF3C7",
        "primary": "#D97706",
        "primary_hover": "#B45309",
        "secondary": "#F59E0B",
        "accent": "#FBBF24",
        "text": "#78350F",
        "text2": "#92400E",
        "text3": "#B45309",
        "border": "#FDE68A",
        "success": "#059669",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#D97706",
        "info_bg": "#FEF3C7"
    }
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# GAMES - مع معلومات دعم لمح/جاوب
# ============================================================================
GAME_CONFIG = {
    "ذكاء": {"display": "ذكاء", "icon": "🧠", "hint": True, "reveal": True, "timer": 30},
    "رياضيات": {"display": "رياضيات", "icon": "🔢", "hint": True, "reveal": True, "timer": 25},
    "تخمين": {"display": "تخمين", "icon": "🎯", "hint": True, "reveal": True, "timer": 25},
    "أسرع": {"display": "أسرع", "icon": "⚡", "hint": False, "reveal": False, "timer": 20},
    "كلمات": {"display": "كلمات", "icon": "🔤", "hint": True, "reveal": True, "timer": 25},
    "سلسلة": {"display": "سلسلة", "icon": "🔗", "hint": False, "reveal": False, "timer": 25},
    "أضداد": {"display": "أضداد", "icon": "↔️", "hint": True, "reveal": True, "timer": 0},
    "أغنية": {"display": "أغنية", "icon": "🎵", "hint": True, "reveal": True, "timer": 30},
    "تكوين": {"display": "تكوين", "icon": "📝", "hint": True, "reveal": True, "timer": 40},
    "ألوان": {"display": "ألوان", "icon": "🎨", "hint": False, "reveal": False, "timer": 15},
    "لعبة": {"display": "لعبة", "icon": "🌿", "hint": True, "reveal": True, "timer": 25},
    "توافق": {"display": "توافق", "icon": "💕", "hint": False, "reveal": False, "timer": 0}
}

GAME_LIST = [(k, v["display"], v["icon"]) for k, v in GAME_CONFIG.items()]
GAME_NAMES = {k: v["display"] for k, v in GAME_CONFIG.items()}
GAME_ICONS = {k: v["icon"] for k, v in GAME_CONFIG.items()}

FIXED_GAME_QR = [{"label": f"{v['icon']} {v['display']}", "text": v['display']} for k, v in GAME_CONFIG.items()]
FIXED_GAME_QR.append({"label": "⛔ إيقاف", "text": "إيقاف"})

# ============================================================================
# Settings
# ============================================================================
PRIVACY_SETTINGS = {
    "auto_delete_inactive_days": 30,
    "cache_timeout_minutes": 10,
    "cleanup_interval_hours": 24,
    "max_sessions_per_user": 5,
    "session_timeout_minutes": 45
}

SECURITY_SETTINGS = {
    "rate_limit_requests": 20,
    "rate_limit_window_seconds": 60,
    "max_message_length": 1000,
    "max_game_duration_minutes": 20,
    "enable_sql_injection_protection": True,
    "enable_xss_protection": True,
    "enable_csrf_protection": True,
    "enable_rate_limiting": True
}

ALLOWED_COMMANDS = {
    "مساعدة", "help", "؟", "بداية", "home", "الرئيسية", "start",
    "ألعاب", "games", "العاب", "نقاطي", "points", "نقاط",
    "صدارة", "leaderboard", "ترتيب", "انضم", "join", "تسجيل",
    "انسحب", "leave", "خروج", "فريقين", "teams", "فرق",
    "ثيمات", "themes", "مظهر", "إيقاف", "stop", "انهاء",
    "لمح", "hint", "جاوب", "reveal", "answer"
}

GAME_COMMANDS = set(GAME_NAMES.values())

# ============================================================================
# Helper Functions
# ============================================================================
def normalize_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    text = text[:SECURITY_SETTINGS["max_message_length"]].strip().lower()
    replacements = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'}
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    if SECURITY_SETTINGS["enable_xss_protection"]:
        text = re.sub(r'[<>"\']', '', text)
    return text

def sanitize_input(text: str) -> str:
    if not text:
        return ""
    if SECURITY_SETTINGS["enable_sql_injection_protection"]:
        dangerous_patterns = [
            r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b',
            r'[;\'"\\]', r'--', r'/\*', r'\*/'
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return ""
    return text[:SECURITY_SETTINGS["max_message_length"]]

def get_theme_colors(theme_name: Optional[str] = None) -> Dict[str, str]:
    if theme_name is None:
        theme_name = DEFAULT_THEME
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])

def validate_theme(theme_name: str) -> str:
    return theme_name if theme_name in THEMES else DEFAULT_THEME

def get_username(profile) -> str:
    try:
        name = profile.display_name if hasattr(profile, 'display_name') else "مستخدم"
        if not name or not isinstance(name, str):
            return "مستخدم"
        name = sanitize_input(name)
        return name[:50] if name else "مستخدم"
    except:
        return "مستخدم"

def get_game_display_name(internal_name: str) -> str:
    return GAME_NAMES.get(internal_name, internal_name)

def get_game_icon(internal_name: str) -> str:
    return GAME_ICONS.get(internal_name, "▪️")

def get_game_config(game_name: str) -> Dict:
    return GAME_CONFIG.get(game_name, {})

def is_valid_game(game_name: str) -> bool:
    return game_name in GAME_NAMES.values()

def is_allowed_command(text: str) -> bool:
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

__all__ = [
    'BOT_NAME', 'BOT_VERSION', 'BOT_RIGHTS',
    'LINE_CHANNEL_SECRET', 'LINE_CHANNEL_ACCESS_TOKEN',
    'THEMES', 'DEFAULT_THEME', 'GAME_CONFIG', 'GAME_LIST',
    'GAME_NAMES', 'GAME_ICONS', 'FIXED_GAME_QR',
    'PRIVACY_SETTINGS', 'SECURITY_SETTINGS',
    'ALLOWED_COMMANDS', 'GAME_COMMANDS',
    'validate_env', 'normalize_text', 'sanitize_input',
    'get_theme_colors', 'validate_theme', 'get_username',
    'get_game_display_name', 'get_game_icon', 'get_game_config',
    'is_valid_game', 'is_allowed_command'
]
