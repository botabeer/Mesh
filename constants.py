"""
Bot Mesh - Enhanced Constants & Configuration
Created by: Abeer Aldosari © 2025
Version: 4.0.0 - Production Ready
"""

import os
import re
from functools import lru_cache
from typing import Dict, Any, Optional

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "4.0.0"
BOT_RIGHTS = "Bot Mesh © 2025 by Abeer Aldosari"
BOT_DESCRIPTION = "بوت ألعاب ذكي مع تصميم احترافي"

# ============================================================================
# LINE Credentials
# ============================================================================
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# ============================================================================
# Gemini AI Keys
# ============================================================================
GEMINI_API_KEY_1 = os.getenv('GEMINI_API_KEY_1')
GEMINI_API_KEY_2 = os.getenv('GEMINI_API_KEY_2')
GEMINI_API_KEY_3 = os.getenv('GEMINI_API_KEY_3')

GEMINI_KEYS = [k for k in [GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3] if k]

# ============================================================================
# Game Settings
# ============================================================================
ROUNDS_PER_GAME = 5
POINTS_PER_CORRECT_ANSWER = 10
INACTIVITY_DAYS = 7
MAX_LEADERBOARD_USERS = 10

# Security Limits
MAX_MESSAGE_LENGTH = 500
RATE_LIMIT_MESSAGES = 20  # رسائل في الدقيقة
MAX_CACHE_SIZE = 100
MAX_CONCURRENT_GAMES = 50

# ============================================================================
# Neumorphism Themes - LINE Compatible
# ============================================================================
THEMES = {
    "💜": {
        "name": "Purple Dream",
        "bg": "#EDF2F7",
        "card": "#E8EEF4",
        "primary": "#805AD5",
        "secondary": "#9F7AEA",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow1": "#CBD5E0",
        "shadow2": "#FFFFFF",
        "button": "#805AD5",
        "success": "#48BB78",
        "error": "#F56565"
    },
    "💚": {
        "name": "Green Nature",
        "bg": "#F0FDF4",
        "card": "#ECFDF5",
        "primary": "#38A169",
        "secondary": "#48BB78",
        "text": "#1C4532",
        "text2": "#276749",
        "shadow1": "#CBD5E0",
        "shadow2": "#FFFFFF",
        "button": "#38A169",
        "success": "#48BB78",
        "error": "#F56565"
    },
    "🤍": {
        "name": "Clean White",
        "bg": "#F7FAFC",
        "card": "#EDF2F7",
        "primary": "#4299E1",
        "secondary": "#63B3ED",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow1": "#CBD5E0",
        "shadow2": "#FFFFFF",
        "button": "#4299E1",
        "success": "#48BB78",
        "error": "#F56565"
    },
    "🖤": {
        "name": "Dark Elegant",
        "bg": "#1A202C",
        "card": "#2D3748",
        "primary": "#667EEA",
        "secondary": "#7F9CF5",
        "text": "#F7FAFC",
        "text2": "#CBD5E0",
        "shadow1": "#171923",
        "shadow2": "#374151",
        "button": "#667EEA",
        "success": "#48BB78",
        "error": "#FC8181"
    },
    "💙": {
        "name": "Ocean Blue",
        "bg": "#EBF8FF",
        "card": "#E6F6FF",
        "primary": "#2B6CB0",
        "secondary": "#3182CE",
        "text": "#2C5282",
        "text2": "#2B6CB0",
        "shadow1": "#CBD5E0",
        "shadow2": "#FFFFFF",
        "button": "#2B6CB0",
        "success": "#48BB78",
        "error": "#F56565"
    },
    "🩶": {
        "name": "Silver Gray",
        "bg": "#F7FAFC",
        "card": "#EDF2F7",
        "primary": "#4A5568",
        "secondary": "#718096",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow1": "#CBD5E0",
        "shadow2": "#FFFFFF",
        "button": "#4A5568",
        "success": "#48BB78",
        "error": "#F56565"
    },
    "🩷": {
        "name": "Pink Blossom",
        "bg": "#FFF5F7",
        "card": "#FED7E2",
        "primary": "#B83280",
        "secondary": "#D53F8C",
        "text": "#702459",
        "text2": "#97266D",
        "shadow1": "#CBD5E0",
        "shadow2": "#FFFFFF",
        "button": "#B83280",
        "success": "#48BB78",
        "error": "#F56565"
    },
    "🧡": {
        "name": "Warm Sunset",
        "bg": "#FFFAF0",
        "card": "#FEF5E7",
        "primary": "#C05621",
        "secondary": "#DD6B20",
        "text": "#7C2D12",
        "text2": "#9C4221",
        "shadow1": "#CBD5E0",
        "shadow2": "#FFFFFF",
        "button": "#C05621",
        "success": "#48BB78",
        "error": "#F56565"
    },
    "🤎": {
        "name": "Earth Brown",
        "bg": "#FEFCF9",
        "card": "#F5F0E8",
        "primary": "#744210",
        "secondary": "#8B4513",
        "text": "#5C2E00",
        "text2": "#7A4F1D",
        "shadow1": "#CBD5E0",
        "shadow2": "#FFFFFF",
        "button": "#744210",
        "success": "#48BB78",
        "error": "#F56565"
    }
}

DEFAULT_THEME = "💜"

# ============================================================================
# Game List
# ============================================================================
GAME_LIST = {
    "IQ": {
        "icon": "🧠",
        "label": "ذكاء",
        "ai_enabled": True,
        "difficulty": "متوسط",
        "category": "عقلية"
    },
    "رياضيات": {
        "icon": "🔢",
        "label": "رياضيات",
        "ai_enabled": True,
        "difficulty": "متغير",
        "category": "عقلية"
    },
    "لون الكلمة": {
        "icon": "🎨",
        "label": "لون",
        "ai_enabled": False,
        "difficulty": "صعب",
        "category": "تركيز"
    },
    "كلمة مبعثرة": {
        "icon": "🔤",
        "label": "ترتيب",
        "ai_enabled": False,
        "difficulty": "سهل",
        "category": "لغوية"
    },
    "كتابة سريعة": {
        "icon": "⚡",
        "label": "سرعة",
        "ai_enabled": False,
        "difficulty": "متوسط",
        "category": "مهارة"
    },
    "عكس": {
        "icon": "↔️",
        "label": "ضد",
        "ai_enabled": True,
        "difficulty": "سهل",
        "category": "لغوية"
    },
    "حروف وكلمات": {
        "icon": "🔠",
        "label": "تكوين",
        "ai_enabled": False,
        "difficulty": "متوسط",
        "category": "لغوية"
    },
    "أغنية": {
        "icon": "🎵",
        "label": "أغنية",
        "ai_enabled": False,
        "difficulty": "متوسط",
        "category": "ثقافية"
    },
    "إنسان حيوان نبات": {
        "icon": "🌍",
        "label": "تنوع",
        "ai_enabled": False,
        "difficulty": "متوسط",
        "category": "معرفة"
    },
    "سلسلة كلمات": {
        "icon": "🔗",
        "label": "سلسلة",
        "ai_enabled": False,
        "difficulty": "سهل",
        "category": "لغوية"
    },
    "تخمين": {
        "icon": "🔮",
        "label": "خمّن",
        "ai_enabled": False,
        "difficulty": "سهل",
        "category": "عقلية"
    },
    "توافق": {
        "icon": "💕",
        "label": "توافق",
        "ai_enabled": False,
        "difficulty": "ترفيهي",
        "category": "تسلية"
    }
}

# ============================================================================
# Fixed Buttons
# ============================================================================
FIXED_BUTTONS = {
    "home": {"label": "🏠 البداية", "text": "بداية"},
    "games": {"label": "🎮 الألعاب", "text": "مساعدة"},
    "points": {"label": "⭐ نقاطي", "text": "نقاطي"},
    "leaderboard": {"label": "🏆 الصدارة", "text": "صدارة"},
    "stop": {"label": "⛔ إيقاف", "text": "إيقاف"},
    "hint": {"label": "💡 تلميح", "text": "لمح"},
    "reveal": {"label": "👁️ الجواب", "text": "جاوب"}
}

# ============================================================================
# Arabic Normalization with LRU Cache
# ============================================================================
ARABIC_NORMALIZE = {
    'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ء': 'ا',
    'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'
}

@lru_cache(maxsize=1000)
def normalize_arabic(text: str) -> str:
    """
    تطبيع النصوص العربية مع Cache
    
    Args:
        text: النص المدخل
        
    Returns:
        النص المطبع
    """
    if not text:
        return ""
    
    text = text.strip().lower()
    
    # تطبيع الأحرف العربية
    for old, new in ARABIC_NORMALIZE.items():
        text = text.replace(old, new)
    
    # إزالة التشكيل
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    
    # إزالة المسافات الزائدة
    text = ' '.join(text.split())
    
    return text

# ============================================================================
# Helper Functions
# ============================================================================

def get_username(profile) -> str:
    """استخراج اسم المستخدم بأمان"""
    try:
        if hasattr(profile, 'display_name'):
            name = profile.display_name
            if name and name.strip():
                name = re.sub(r'[<>"\'\\]', '', name)
                return name.strip()[:50]
        return "مستخدم"
    except Exception:
        return "مستخدم"

def validate_env() -> bool:
    """التحقق من المتغيرات البيئية"""
    required = ['LINE_CHANNEL_SECRET', 'LINE_CHANNEL_ACCESS_TOKEN']
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        raise ValueError(f"❌ متغيرات ناقصة: {', '.join(missing)}")
    
    if not GEMINI_KEYS:
        print("⚠️ لا توجد مفاتيح Gemini AI - وضع Fallback")
    else:
        print(f"✅ {len(GEMINI_KEYS)} مفتاح AI متاح")
    
    return True

@lru_cache(maxsize=10)
def get_theme_colors(theme_emoji: str) -> Dict[str, str]:
    """الحصول على ألوان الثيم مع Cache"""
    return THEMES.get(theme_emoji, THEMES[DEFAULT_THEME])

def is_valid_theme(theme_emoji: str) -> bool:
    """التحقق من صحة الثيم"""
    return theme_emoji in THEMES

# ============================================================================
# User Levels
# ============================================================================
USER_LEVELS = [
    {"min": 0, "max": 49, "name": "🌱 مبتدئ", "color": "#48BB78"},
    {"min": 50, "max": 149, "name": "⭐ متوسط", "color": "#667EEA"},
    {"min": 150, "max": 299, "name": "🔥 متقدم", "color": "#DD6B20"},
    {"min": 300, "max": 999999, "name": "👑 محترف", "color": "#D53F8C"}
]

@lru_cache(maxsize=100)
def get_user_level(points: int) -> Dict[str, Any]:
    """تحديد مستوى المستخدم مع Cache"""
    for level in USER_LEVELS:
        if level["min"] <= points <= level["max"]:
            return level
    return USER_LEVELS[0]

# ============================================================================
# Input Sanitization
# ============================================================================

def sanitize_user_input(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> str:
    """تنظيف مدخلات المستخدم بشكل آمن"""
    if not text:
        return ""
    
    # إزالة الأحرف الخطيرة
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    text = re.sub(r'[<>"\'\\]', '', text)
    
    # تحديد الطول
    text = text[:max_length]
    
    return text.strip()

# ============================================================================
# Validation
# ============================================================================
if __name__ != "__main__":
    try:
        validate_env()
    except ValueError as e:
        print(f"⚠️ تحذير: {e}")
