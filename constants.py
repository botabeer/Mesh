"""
Bot Mesh - Enhanced Constants & Configuration
Created by: Abeer Aldosari © 2025
Enhanced: Better color schemes, LINE compatibility, smarter config
"""

import os
import re

# ============================================================================
# Bot Information
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "3.1.0"
BOT_RIGHTS = "Bot Mesh © 2025 by Abeer Aldosari"
BOT_DESCRIPTION = "بوت ألعاب ذكي مع تصميم احترافي"

# ============================================================================
# LINE Credentials
# ============================================================================
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# ============================================================================
# Gemini AI Keys (Multiple keys for better reliability)
# ============================================================================
GEMINI_API_KEY_1 = os.getenv('GEMINI_API_KEY_1')
GEMINI_API_KEY_2 = os.getenv('GEMINI_API_KEY_2')
GEMINI_API_KEY_3 = os.getenv('GEMINI_API_KEY_3')

# ============================================================================
# Game Settings
# ============================================================================
ROUNDS_PER_GAME = 5
POINTS_PER_CORRECT_ANSWER = 10
INACTIVITY_DAYS = 7
MAX_LEADERBOARD_USERS = 10

# ============================================================================
# Enhanced Neumorphism Themes (LINE Compatible)
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
# Enhanced Game List (Better organization)
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
        "label": "خمن",
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
# Fixed Buttons (LINE Compatible)
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
# Arabic Character Normalization (Enhanced)
# ============================================================================
ARABIC_NORMALIZE = {
    'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ء': 'ا',
    'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'
}

def normalize_arabic(text):
    """
    Enhanced Arabic text normalization
    
    Args:
        text: Input Arabic text
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    text = text.strip().lower()
    
    # Normalize Arabic characters
    for old, new in ARABIC_NORMALIZE.items():
        text = text.replace(old, new)
    
    # Remove diacritics
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    
    # Remove extra spaces
    text = ' '.join(text.split())
    
    return text

# ============================================================================
# Helper Functions
# ============================================================================

def get_username(profile):
    """
    Extract username from LINE profile safely
    
    Args:
        profile: LINE user profile
        
    Returns:
        Clean username or default
    """
    try:
        if hasattr(profile, 'display_name'):
            name = profile.display_name
            if name and name.strip():
                return name.strip()[:50]  # Limit length
        return "مستخدم"
    except Exception:
        return "مستخدم"

def validate_env():
    """
    Validate required environment variables
    
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If missing required variables
    """
    # Required variables
    required = ['LINE_CHANNEL_SECRET', 'LINE_CHANNEL_ACCESS_TOKEN']
    missing = [var for var in required if not os.getenv(var)]
    
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")
    
    # Check AI keys
    ai_keys = [GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3]
    active_keys = [k for k in ai_keys if k]
    
    if not active_keys:
        print("⚠️ No Gemini AI keys - Using fallback mode")
    else:
        print(f"✅ {len(active_keys)} Gemini AI key(s) available")
    
    return True

def get_theme_colors(theme_emoji):
    """
    Get theme colors safely
    
    Args:
        theme_emoji: Theme emoji identifier
        
    Returns:
        dict: Theme colors
    """
    return THEMES.get(theme_emoji, THEMES[DEFAULT_THEME])

def is_valid_theme(theme_emoji):
    """
    Check if theme is valid
    
    Args:
        theme_emoji: Theme emoji to check
        
    Returns:
        bool: True if valid
    """
    return theme_emoji in THEMES

# ============================================================================
# Game Categories
# ============================================================================
GAME_CATEGORIES = {
    "عقلية": ["IQ", "رياضيات", "تخمين"],
    "لغوية": ["كلمة مبعثرة", "عكس", "حروف وكلمات", "سلسلة كلمات"],
    "مهارة": ["كتابة سريعة", "لون الكلمة"],
    "ثقافية": ["أغنية", "إنسان حيوان نبات"],
    "تسلية": ["توافق"]
}

# ============================================================================
# User Levels
# ============================================================================
USER_LEVELS = [
    {"min": 0, "max": 49, "name": "🌱 مبتدئ", "color": "#48BB78"},
    {"min": 50, "max": 149, "name": "⭐ متوسط", "color": "#667EEA"},
    {"min": 150, "max": 299, "name": "🔥 متقدم", "color": "#DD6B20"},
    {"min": 300, "max": 999999, "name": "👑 محترف", "color": "#D53F8C"}
]

def get_user_level(points):
    """
    Get user level based on points
    
    Args:
        points: User points
        
    Returns:
        dict: Level info
    """
    for level in USER_LEVELS:
        if level["min"] <= points <= level["max"]:
            return level
    return USER_LEVELS[0]

# ============================================================================
# Validation & Sanitization
# ============================================================================

def sanitize_user_input(text, max_length=200):
    """
    Sanitize user input
    
    Args:
        text: Input text
        max_length: Maximum allowed length
        
    Returns:
        Clean text
    """
    if not text:
        return ""
    
    # Remove control characters
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    
    # Limit length
    text = text[:max_length]
    
    # Trim whitespace
    return text.strip()

# ============================================================================
# Export validation on import
# ============================================================================
if __name__ != "__main__":
    try:
        validate_env()
    except ValueError as e:
        print(f"⚠️ Configuration warning: {e}")
