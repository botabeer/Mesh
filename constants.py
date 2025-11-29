"""
Bot Mesh - Constants v13.0 FINAL
Created by: Abeer Aldosari © 2025
"""

import os
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
import re

load_dotenv()

BOT_NAME = "Bot Mesh"
BOT_VERSION = "13.0"
BOT_RIGHTS = "© 2025 Abeer Aldosari"

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def validate_env():
    if not LINE_CHANNEL_SECRET:
        raise ValueError("LINE_CHANNEL_SECRET is not set")
    if not LINE_CHANNEL_ACCESS_TOKEN:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set")

# ============================================================================
# THEMES
# ============================================================================
THEMES = {
    "أبيض": {"name": "أبيض", "bg": "#FFFFFF", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_hover": "#F8F9FA", "primary": "#1E40AF", "primary_hover": "#1E3A8A", "secondary": "#475569", "accent": "#2563EB", "text": "#0F172A", "text2": "#334155", "text3": "#64748B", "border": "#CBD5E1", "border_focus": "#2563EB", "success": "#059669", "success_bg": "#D1FAE5", "error": "#DC2626", "error_bg": "#FEE2E2", "warning": "#D97706", "warning_bg": "#FEF3C7", "info": "#1D4ED8", "info_bg": "#DBEAFE", "shadow": "rgba(0,0,0,0.1)", "shadow_lg": "rgba(0,0,0,0.2)", "overlay": "rgba(0,0,0,0.02)", "gradient": "linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%)"},
    "أسود": {"name": "أسود", "bg": "#0F172A", "card": "#1E293B", "glass": "#1E293B", "glass_hover": "#334155", "primary": "#3B82F6", "primary_hover": "#60A5FA", "secondary": "#94A3B8", "accent": "#60A5FA", "text": "#F1F5F9", "text2": "#CBD5E1", "text3": "#94A3B8", "border": "#475569", "border_focus": "#60A5FA", "success": "#10B981", "success_bg": "#064E3B", "error": "#EF4444", "error_bg": "#7F1D1D", "warning": "#F59E0B", "warning_bg": "#78350F", "info": "#3B82F6", "info_bg": "#1E3A8A", "shadow": "rgba(0,0,0,0.3)", "shadow_lg": "rgba(0,0,0,0.5)", "overlay": "rgba(255,255,255,0.03)", "gradient": "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)"},
    "رمادي": {"name": "رمادي", "bg": "#F9FAFB", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_hover": "#F3F4F6", "primary": "#374151", "primary_hover": "#1F2937", "secondary": "#6B7280", "accent": "#4B5563", "text": "#111827", "text2": "#374151", "text3": "#6B7280", "border": "#D1D5DB", "border_focus": "#4B5563", "success": "#059669", "success_bg": "#D1FAE5", "error": "#DC2626", "error_bg": "#FEE2E2", "warning": "#D97706", "warning_bg": "#FEF3C7", "info": "#4B5563", "info_bg": "#F3F4F6", "shadow": "rgba(0,0,0,0.1)", "shadow_lg": "rgba(0,0,0,0.2)", "overlay": "rgba(0,0,0,0.02)", "gradient": "linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%)"},
    "أزرق": {"name": "أزرق", "bg": "#EFF6FF", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_hover": "#DBEAFE", "primary": "#1E40AF", "primary_hover": "#1E3A8A", "secondary": "#3B82F6", "accent": "#2563EB", "text": "#1E3A8A", "text2": "#1E40AF", "text3": "#3B82F6", "border": "#93C5FD", "border_focus": "#2563EB", "success": "#059669", "success_bg": "#D1FAE5", "error": "#DC2626", "error_bg": "#FEE2E2", "warning": "#D97706", "warning_bg": "#FEF3C7", "info": "#1E40AF", "info_bg": "#DBEAFE", "shadow": "rgba(30,64,175,0.15)", "shadow_lg": "rgba(30,64,175,0.25)", "overlay": "rgba(30,64,175,0.03)", "gradient": "linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%)"},
    "بنفسجي": {"name": "بنفسجي", "bg": "#F5F3FF", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_hover": "#EDE9FE", "primary": "#5B21B6", "primary_hover": "#4C1D95", "secondary": "#8B5CF6", "accent": "#7C3AED", "text": "#4C1D95", "text2": "#5B21B6", "text3": "#8B5CF6", "border": "#C4B5FD", "border_focus": "#7C3AED", "success": "#059669", "success_bg": "#D1FAE5", "error": "#DC2626", "error_bg": "#FEE2E2", "warning": "#D97706", "warning_bg": "#FEF3C7", "info": "#5B21B6", "info_bg": "#EDE9FE", "shadow": "rgba(91,33,182,0.15)", "shadow_lg": "rgba(91,33,182,0.25)", "overlay": "rgba(91,33,182,0.03)", "gradient": "linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%)"},
    "وردي": {"name": "وردي", "bg": "#FDF2F8", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_hover": "#FCE7F3", "primary": "#9F1239", "primary_hover": "#881337", "secondary": "#DB2777", "accent": "#EC4899", "text": "#831843", "text2": "#9F1239", "text3": "#DB2777", "border": "#F9A8D4", "border_focus": "#DB2777", "success": "#059669", "success_bg": "#D1FAE5", "error": "#DC2626", "error_bg": "#FEE2E2", "warning": "#D97706", "warning_bg": "#FEF3C7", "info": "#9F1239", "info_bg": "#FCE7F3", "shadow": "rgba(159,18,57,0.15)", "shadow_lg": "rgba(159,18,57,0.25)", "overlay": "rgba(159,18,57,0.03)", "gradient": "linear-gradient(135deg, #FDF2F8 0%, #FCE7F3 100%)"},
    "أخضر": {"name": "أخضر", "bg": "#F0FDF4", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_hover": "#DCFCE7", "primary": "#065F46", "primary_hover": "#064E3B", "secondary": "#059669", "accent": "#10B981", "text": "#064E3B", "text2": "#065F46", "text3": "#059669", "border": "#86EFAC", "border_focus": "#059669", "success": "#059669", "success_bg": "#D1FAE5", "error": "#DC2626", "error_bg": "#FEE2E2", "warning": "#D97706", "warning_bg": "#FEF3C7", "info": "#065F46", "info_bg": "#DCFCE7", "shadow": "rgba(6,95,70,0.15)", "shadow_lg": "rgba(6,95,70,0.25)", "overlay": "rgba(6,95,70,0.03)", "gradient": "linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%)"},
    "برتقالي": {"name": "برتقالي", "bg": "#FFF7ED", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_hover": "#FFEDD5", "primary": "#9A3412", "primary_hover": "#7C2D12", "secondary": "#EA580C", "accent": "#F97316", "text": "#7C2D12", "text2": "#9A3412", "text3": "#EA580C", "border": "#FDBA74", "border_focus": "#EA580C", "success": "#059669", "success_bg": "#D1FAE5", "error": "#DC2626", "error_bg": "#FEE2E2", "warning": "#D97706", "warning_bg": "#FEF3C7", "info": "#9A3412", "info_bg": "#FFEDD5", "shadow": "rgba(154,52,18,0.15)", "shadow_lg": "rgba(154,52,18,0.25)", "overlay": "rgba(154,52,18,0.03)", "gradient": "linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%)"},
    "بني": {"name": "بني", "bg": "#FFFCF7", "card": "#FFFFFF", "glass": "#FFFFFF", "glass_hover": "#F5E6D8", "primary": "#78350F", "primary_hover": "#451A03", "secondary": "#92400E", "accent": "#B45309", "text": "#451A03", "text2": "#78350F", "text3": "#92400E", "border": "#F5E6D8", "border_focus": "#92400E", "success": "#059669", "success_bg": "#D1FAE5", "error": "#DC2626", "error_bg": "#FEE2E2", "warning": "#D97706", "warning_bg": "#FEF3C7", "info": "#78350F", "info_bg": "#F5E6D8", "shadow": "rgba(120,53,15,0.15)", "shadow_lg": "rgba(120,53,15,0.25)", "overlay": "rgba(120,53,15,0.03)", "gradient": "linear-gradient(135deg, #FFFCF7 0%, #F5E6D8 100%)"}
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# GAMES - أسرع أول لعبة ✅
# ============================================================================
GAME_LIST: List[Tuple[str, str, str]] = [
    ("fast_typing", "أسرع", "▪️"),  # الأولى ✅
    ("iq", "ذكاء", "▪️"),
    ("math", "رياضيات", "▪️"),
    ("guess", "تخمين", "▪️"),
    ("scramble_word", "كلمات", "▪️"),
    ("chain_words", "سلسلة", "▪️"),
    ("opposite", "أضداد", "▪️"),
    ("song", "أغنية", "▪️"),
    ("letters_words", "تكوين", "▪️"),
    ("word_color", "ألوان", "▪️"),
    ("human_animal_plant", "لعبة", "▪️"),
    ("compatibility", "توافق", "🖤")
]

GAME_NAMES = {internal: display for internal, display, icon in GAME_LIST}
GAME_ICONS = {internal: icon for internal, display, icon in GAME_LIST}

FIXED_GAME_QR = [{"label": display, "text": display} for internal, display, icon in GAME_LIST]
FIXED_GAME_QR.append({"label": "▪️ إيقاف", "text": "إيقاف"})

# ============================================================================
# Settings
# ============================================================================
PRIVACY_SETTINGS = {"auto_delete_inactive_days": 30, "cache_timeout_minutes": 10, "cleanup_interval_hours": 24, "max_sessions_per_user": 5, "session_timeout_minutes": 45}
SECURITY_SETTINGS = {"rate_limit_requests": 20, "rate_limit_window_seconds": 60, "max_message_length": 1000, "max_game_duration_minutes": 20, "enable_sql_injection_protection": True, "enable_xss_protection": True, "enable_csrf_protection": True, "enable_rate_limiting": True}

ALLOWED_COMMANDS = {"مساعدة", "help", "؟", "بداية", "home", "الرئيسية", "start", "ألعاب", "games", "العاب", "نقاطي", "points", "نقاط", "صدارة", "leaderboard", "مستوى", "انضم", "join", "تسجيل", "انسحب", "leave", "خروج", "فريقين", "teams", "فرق", "ثيمات", "themes", "مظهر", "إيقاف", "stop", "انهاء", "لمح", "hint", "جاوب", "reveal", "answer"}
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
        dangerous_patterns = [r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b', r'[;\'"\\]', r'--', r'/\*', r'\*/']
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

__all__ = ['BOT_NAME', 'BOT_VERSION', 'BOT_RIGHTS', 'LINE_CHANNEL_SECRET', 'LINE_CHANNEL_ACCESS_TOKEN', 'THEMES', 'DEFAULT_THEME', 'GAME_LIST', 'GAME_NAMES', 'GAME_ICONS', 'FIXED_GAME_QR', 'PRIVACY_SETTINGS', 'SECURITY_SETTINGS', 'ALLOWED_COMMANDS', 'GAME_COMMANDS', 'validate_env', 'normalize_text', 'sanitize_input', 'get_theme_colors', 'validate_theme', 'get_username', 'get_game_display_name', 'get_game_icon', 'is_valid_game', 'is_allowed_command']
