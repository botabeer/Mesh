"""
Bot Mesh - Constants v18.0 DYNAMIC THEMES
Created by: Abeer Aldosari © 2025
✅ نظام ثيمات ديناميكي 100%
✅ خلفيات ذكية لكل ثيم
✅ تباين احترافي ومريح للعين
✅ بدون شروط if theme == "أبيض"
"""

import os
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
import re

load_dotenv()

BOT_NAME = "Bot Mesh"
BOT_VERSION = "18.0 DYNAMIC"
BOT_RIGHTS = "© 2025 Abeer Aldosari"

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def validate_env():
    if not LINE_CHANNEL_SECRET:
        raise ValueError("LINE_CHANNEL_SECRET is not set")
    if not LINE_CHANNEL_ACCESS_TOKEN:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set")

# ============================================================================
# 9 ثيمات ديناميكية - كل ثيم له شخصيته
# ============================================================================
THEMES = {
    "أبيض": {
        "name": "أبيض",
        "bg": "#FAFBFC",                    # خلفية رمادية فاتحة جداً (ليست بيضاء نقية)
        "card": "#FFFFFF",                  # بطاقات بيضاء نقية
        "primary": "#2563EB",               # أزرق حيوي
        "primary_hover": "#1D4ED8",         # أزرق أغمق
        "secondary": "#64748B",             # رمادي متوسط
        "accent": "#3B82F6",                # أزرق لامع
        "text": "#1E293B",                  # نص داكن (contrast 13:1)
        "text2": "#475569",                 # نص ثانوي (contrast 8:1)
        "text3": "#64748B",                 # نص ثالثي (contrast 5:1)
        "border": "#E2E8F0",                # حدود ناعمة
        "success": "#10B981",               # أخضر زاهي
        "success_bg": "#D1FAE5",            # خلفية خضراء
        "error": "#EF4444",                 # أحمر واضح
        "error_bg": "#FEE2E2",              # خلفية حمراء
        "warning": "#F59E0B",               # برتقالي دافئ
        "info": "#2563EB",                  # أزرق معلومات
        "info_bg": "#EFF6FF",               # خلفية زرقاء فاتحة
        "shadow": "rgba(15, 23, 42, 0.06)", # ظل ناعم
        "button_text": "#FFFFFF",           # نص الأزرار
        "disabled": "#94A3B8",              # معطل
        "disabled_bg": "#F1F5F9"            # خلفية معطلة
    },
    "أسود": {
        "name": "أسود",
        "bg": "#0A0A0A",
        "card": "#1E1E1E",
        "primary": "#3B82F6",
        "primary_hover": "#60A5FA",
        "secondary": "#64748B",
        "accent": "#3B82F6",
        "text": "#FFFFFF",
        "text2": "#E2E8F0",
        "text3": "#94A3B8",
        "border": "#334155",
        "success": "#10B981",
        "success_bg": "#064E3B",
        "error": "#EF4444",
        "error_bg": "#7F1D1D",
        "warning": "#F59E0B",
        "info": "#3B82F6",
        "info_bg": "#1E3A8A",
        "shadow": "rgba(0, 0, 0, 0.3)",
        "button_text": "#FFFFFF",
        "disabled": "#475569",
        "disabled_bg": "#1E293B"
    },
    "رمادي": {
        "name": "رمادي",
        "bg": "#F9FAFB",
        "card": "#F3F4F6",
        "primary": "#374151",
        "primary_hover": "#1F2937",
        "secondary": "#6B7280",
        "accent": "#9CA3AF",
        "text": "#111827",
        "text2": "#374151",
        "text3": "#6B7280",
        "border": "#D1D5DB",
        "success": "#059669",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#374151",
        "info_bg": "#E5E7EB",
        "shadow": "rgba(17, 24, 39, 0.08)",
        "button_text": "#FFFFFF",
        "disabled": "#9CA3AF",
        "disabled_bg": "#E5E7EB"
    },
    "أزرق": {
        "name": "أزرق",
        "bg": "#EFF6FF",
        "card": "#DBEAFE",
        "primary": "#1E3A8A",
        "primary_hover": "#1E40AF",
        "secondary": "#1E40AF",
        "accent": "#2563EB",
        "text": "#0F172A",
        "text2": "#1E3A8A",
        "text3": "#3B82F6",
        "border": "#93C5FD",
        "success": "#059669",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#1E3A8A",
        "info_bg": "#DBEAFE",
        "shadow": "rgba(30, 58, 138, 0.1)",
        "button_text": "#FFFFFF",
        "disabled": "#93C5FD",
        "disabled_bg": "#BFDBFE"
    },
    "بنفسجي": {
        "name": "بنفسجي",
        "bg": "#F5F3FF",
        "card": "#EDE9FE",
        "primary": "#6B21A8",
        "primary_hover": "#5B21B6",
        "secondary": "#7C3AED",
        "accent": "#8B5CF6",
        "text": "#5B21B6",
        "text2": "#6B21A8",
        "text3": "#7C3AED",
        "border": "#C4B5FD",
        "success": "#059669",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#6B21A8",
        "info_bg": "#EDE9FE",
        "shadow": "rgba(107, 33, 168, 0.1)",
        "button_text": "#FFFFFF",
        "disabled": "#C4B5FD",
        "disabled_bg": "#DDD6FE"
    },
    "وردي": {
        "name": "وردي",
        "bg": "#FDF2F8",
        "card": "#FCE7F3",
        "primary": "#9F1239",
        "primary_hover": "#831843",
        "secondary": "#BE185D",
        "accent": "#DB2777",
        "text": "#831843",
        "text2": "#9F1239",
        "text3": "#BE185D",
        "border": "#F9A8D4",
        "success": "#059669",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#9F1239",
        "info_bg": "#FCE7F3",
        "shadow": "rgba(159, 18, 57, 0.1)",
        "button_text": "#FFFFFF",
        "disabled": "#F9A8D4",
        "disabled_bg": "#FBCFE8"
    },
    "أخضر": {
        "name": "أخضر",
        "bg": "#F0FDF4",
        "card": "#DCFCE7",
        "primary": "#047857",
        "primary_hover": "#065F46",
        "secondary": "#059669",
        "accent": "#10B981",
        "text": "#064E3B",
        "text2": "#065F46",
        "text3": "#059669",
        "border": "#86EFAC",
        "success": "#10B981",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#047857",
        "info_bg": "#DCFCE7",
        "shadow": "rgba(4, 120, 87, 0.1)",
        "button_text": "#FFFFFF",
        "disabled": "#86EFAC",
        "disabled_bg": "#BBF7D0"
    },
    "برتقالي": {
        "name": "برتقالي",
        "bg": "#FFF7ED",
        "card": "#FFEDD5",
        "primary": "#C2410C",
        "primary_hover": "#9A3412",
        "secondary": "#EA580C",
        "accent": "#F97316",
        "text": "#7C2D12",
        "text2": "#9A3412",
        "text3": "#C2410C",
        "border": "#FED7AA",
        "success": "#059669",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#C2410C",
        "info_bg": "#FFEDD5",
        "shadow": "rgba(194, 65, 12, 0.1)",
        "button_text": "#FFFFFF",
        "disabled": "#FED7AA",
        "disabled_bg": "#FED7AA"
    },
    "ذهبي": {
        "name": "ذهبي",
        "bg": "#FFFBEB",
        "card": "#FEF3C7",
        "primary": "#B45309",
        "primary_hover": "#92400E",
        "secondary": "#D97706",
        "accent": "#F59E0B",
        "text": "#78350F",
        "text2": "#92400E",
        "text3": "#B45309",
        "border": "#FDE68A",
        "success": "#059669",
        "success_bg": "#D1FAE5",
        "error": "#DC2626",
        "error_bg": "#FEE2E2",
        "warning": "#D97706",
        "info": "#B45309",
        "info_bg": "#FEF3C7",
        "shadow": "rgba(180, 83, 9, 0.1)",
        "button_text": "#FFFFFF",
        "disabled": "#FDE68A",
        "disabled_bg": "#FDE68A"
    }
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# أسماء الألعاب - بدون تغيير
# ============================================================================
GAME_CONFIG = {
    "كتابة سريعة": {"display": "أسرع", "icon": "▫️", "hint": False, "reveal": False, "timer": 20},
    "ذكاء": {"display": "ذكاء", "icon": "▫️", "hint": True, "reveal": True, "timer": 30},
    "إنسان حيوان نبات": {"display": "لعبة", "icon": "▫️", "hint": True, "reveal": True, "timer": 25},
    "أغنية": {"display": "أغنيه", "icon": "▫️", "hint": True, "reveal": True, "timer": 30},
    "تخمين": {"display": "خمن", "icon": "▫️", "hint": True, "reveal": True, "timer": 25},
    "سلسلة كلمات": {"display": "سلسلة", "icon": "▫️", "hint": False, "reveal": False, "timer": 25},
    "كلمة مبعثرة": {"display": "ترتيب", "icon": "▫️", "hint": True, "reveal": True, "timer": 25},
    "تكوين": {"display": "تكوين", "icon": "▫️", "hint": True, "reveal": True, "timer": 40},
    "أضداد": {"display": "ضد", "icon": "▫️", "hint": True, "reveal": True, "timer": 0},
    "لون": {"display": "لون", "icon": "▫️", "hint": False, "reveal": False, "timer": 15},
    "رياضيات": {"display": "رياضيات", "icon": "▫️", "hint": True, "reveal": True, "timer": 25},
    "توافق": {"display": "توافق", "icon": "🖤", "hint": False, "reveal": False, "timer": 0}
}

GAME_LIST = [(k, v["display"], v["icon"]) for k, v in GAME_CONFIG.items()]
GAME_NAMES = {k: v["display"] for k, v in GAME_CONFIG.items()}
GAME_ICONS = {k: v["icon"] for k, v in GAME_CONFIG.items()}
DISPLAY_TO_CLASS = {v["display"]: k for k, v in GAME_CONFIG.items()}

FIXED_GAME_QR = [{"label": f"{v['icon']} {v['display']}", "text": v['display']} for k, v in GAME_CONFIG.items()]
FIXED_GAME_QR.append({"label": "🔘 إيقاف", "text": "إيقاف"})

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
    "صدارة", "leaderboard", "مستوى", "انضم", "join", "تسجيل",
    "انسحب", "leave", "خروج", "فريقين", "teams", "فرق",
    "ثيمات", "themes", "مظهر", "إيقاف", "stop", "انهاء",
    "لمح", "hint", "جاوب", "reveal", "answer"
}

GAME_COMMANDS = set(GAME_NAMES.values())

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

def get_game_class_name(display_name: str) -> str:
    return DISPLAY_TO_CLASS.get(display_name, display_name)

def get_game_icon(internal_name: str) -> str:
    return GAME_ICONS.get(internal_name, "▫️")

def get_game_config(game_name: str) -> Dict:
    return GAME_CONFIG.get(game_name, {})

def is_valid_game(game_name: str) -> bool:
    return game_name in GAME_NAMES.values() or game_name in GAME_CONFIG.keys()

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
    'GAME_NAMES', 'GAME_ICONS', 'FIXED_GAME_QR', 'DISPLAY_TO_CLASS',
    'PRIVACY_SETTINGS', 'SECURITY_SETTINGS',
    'ALLOWED_COMMANDS', 'GAME_COMMANDS',
    'validate_env', 'normalize_text', 'sanitize_input',
    'get_theme_colors', 'validate_theme', 'get_username',
    'get_game_display_name', 'get_game_class_name', 'get_game_icon', 
    'get_game_config', 'is_valid_game', 'is_allowed_command'
]
