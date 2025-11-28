"""
Bot Mesh - Constants & Configuration v8.0 (MERGED FINAL)
Created by: Abeer Aldosari © 2025
✅ تصميم زجاجي ثلاثي الأبعاد
✅ 9 ثيمات احترافية
✅ Quick Reply للألعاب فقط
✅ دعم فردي + مجموعة + فريقين
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
    if not LINE_CHANNEL_SECRET:
        raise ValueError("LINE_CHANNEL_SECRET is not set")
    if not LINE_CHANNEL_ACCESS_TOKEN:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set")

# ============================================================================
# Glass 3D Themes - Offical Final Set
# ============================================================================
THEMES = {
    "أبيض": {
        "name": "أبيض","bg": "linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%)",
        "card": "#FFFFFF","glass": "rgba(255,255,255,0.85)",
        "primary": "#3B82F6","secondary": "#60A5FA",
        "text": "#1E293B","text2": "#64748B",
        "shadow": "0 8px 32px rgba(59,130,246,0.15)",
        "border": "rgba(59,130,246,0.1)",
        "success": "#10B981","error": "#EF4444","warning": "#F59E0B"
    },
    "أسود": {
        "name": "أسود","bg": "linear-gradient(135deg,#0F172A 0%,#1E293B 100%)",
        "card": "#1E293B","glass": "rgba(30,41,59,0.85)",
        "primary": "#60A5FA","secondary": "#93C5FD",
        "text": "#F1F5F9","text2": "#CBD5E1",
        "shadow": "0 8px 32px rgba(96,165,250,0.15)",
        "border": "rgba(96,165,250,0.1)",
        "success": "#10B981","error": "#EF4444","warning": "#F59E0B"
    },
    "رمادي": {
        "name":"رمادي","bg":"linear-gradient(135deg,#F9FAFB 0%,#F3F4F6 100%)",
        "card":"#FFFFFF","glass":"rgba(255,255,255,0.85)",
        "primary":"#6B7280","secondary":"#9CA3AF",
        "text":"#111827","text2":"#6B7280",
        "shadow":"0 8px 32px rgba(107,114,128,0.15)",
        "border":"rgba(107,114,128,0.1)",
        "success":"#10B981","error":"#EF4444","warning":"#F59E0B"
    },
    "أزرق": {
        "name":"أزرق","bg":"linear-gradient(135deg,#EFF6FF 0%,#DBEAFE 100%)",
        "card":"#FFFFFF","glass":"rgba(255,255,255,0.85)",
        "primary":"#2563EB","secondary":"#3B82F6",
        "text":"#1E3A8A","text2":"#3B82F6",
        "shadow":"0 8px 32px rgba(37,99,235,0.15)",
        "border":"rgba(37,99,235,0.1)",
        "success":"#10B981","error":"#EF4444","warning":"#F59E0B"
    },
    "بنفسجي":{
        "name":"بنفسجي","bg":"linear-gradient(135deg,#F5F3FF 0%,#EDE9FE 100%)",
        "card":"#FFFFFF","glass":"rgba(255,255,255,0.85)",
        "primary":"#8B5CF6","secondary":"#A78BFA",
        "text":"#4C1D95","text2":"#7C3AED",
        "shadow":"0 8px 32px rgba(139,92,246,0.15)",
        "border":"rgba(139,92,246,0.1)",
        "success":"#10B981","error":"#EF4444","warning":"#F59E0B"
    },
    "وردي":{
        "name":"وردي","bg":"linear-gradient(135deg,#FDF2F8 0%,#FCE7F3 100%)",
        "card":"#FFFFFF","glass":"rgba(255,255,255,0.85)",
        "primary":"#EC4899","secondary":"#F472B6",
        "text":"#831843","text2":"#DB2777",
        "shadow":"0 8px 32px rgba(236,72,153,0.15)",
        "border":"rgba(236,72,153,0.1)",
        "success":"#10B981","error":"#EF4444","warning":"#F59E0B"
    },
    "أخضر":{
        "name":"أخضر","bg":"linear-gradient(135deg,#F0FDF4 0%,#DCFCE7 100%)",
        "card":"#FFFFFF","glass":"rgba(255,255,255,0.85)",
        "primary":"#10B981","secondary":"#34D399",
        "text":"#064E3B","text2":"#059669",
        "shadow":"0 8px 32px rgba(16,185,129,0.15)",
        "border":"rgba(16,185,129,0.1)",
        "success":"#10B981","error":"#EF4444","warning":"#F59E0B"
    },
    "برتقالي":{
        "name":"برتقالي","bg":"linear-gradient(135deg,#FFF7ED 0%,#FFEDD5 100%)",
        "card":"#FFFFFF","glass":"rgba(255,255,255,0.85)",
        "primary":"#F97316","secondary":"#FB923C",
        "text":"#7C2D12","text2":"#EA580C",
        "shadow":"0 8px 32px rgba(249,115,22,0.15)",
        "border":"rgba(249,115,22,0.1)",
        "success":"#10B981","error":"#EF4444","warning":"#F59E0B"
    },
    "بني":{
        "name":"بني","bg":"linear-gradient(135deg,#FFFCF7 0%,#F5E6D8 100%)",
        "card":"#FFFFFF","glass":"rgba(255,255,255,0.85)",
        "primary":"#8A4B10","secondary":"#C08437",
        "text":"#4A2F05","text2":"#C08437",
        "shadow":"0 8px 32px rgba(138,75,16,0.15)",
        "border":"rgba(138,75,16,0.1)",
        "success":"#10B981","error":"#EF4444","warning":"#F59E0B"
    }
}

DEFAULT_THEME = "أبيض"

# ============================================================================
# Games Configuration (Ordered As Requested)
# ============================================================================
GAME_LIST = [
    ("speed", "أسرع"),
    ("iq", "ذكاء"),
    ("human_animal_plant", "لعبة"),
    ("song", "أغنية"),
    ("guess", "خمن"),
    ("chain", "سلسلة"),
    ("order", "ترتيب"),
    ("compose", "تكوين"),
    ("opposite", "ضد"),
    ("color", "لون"),
    ("math", "رياضيات"),
    ("compat", "توافق"),
]

# ============================================================================
# Persistent Quick Reply (GAMES ONLY)
# ============================================================================
FIXED_GAME_QR = [
    {"label":"▫️ أسرع","text":"أسرع"},
    {"label":"▫️ ذكاء","text":"ذكاء"},
    {"label":"▫️ لعبة","text":"لعبة"},
    {"label":"▫️ أغنية","text":"أغنية"},
    {"label":"▫️ خمن","text":"خمن"},
    {"label":"▫️ سلسلة","text":"سلسلة"},
    {"label":"▫️ ترتيب","text":"ترتيب"},
    {"label":"▫️ تكوين","text":"تكوين"},
    {"label":"▫️ ضد","text":"ضد"},
    {"label":"▫️ لون","text":"لون"},
    {"label":"▫️ رياضيات","text":"رياضيات"},
    {"label":"▫️ توافق","text":"توافق"}
]

# ============================================================================
# Group Actions
# ============================================================================
FIXED_ACTIONS = {
    "join":{"label":"انضم","text":"انضم"},
    "leave":{"label":"انسحب","text":"انسحب"},
    "teams":{"label":"فريقين","text":"فريقين"}
}

# ============================================================================
# Rate Limiting
# ============================================================================
RATE_LIMIT_CONFIG = {
    "max_requests":10,
    "window_seconds":60,
    "cleanup_interval":300
}

# ============================================================================
# Game Logic Settings
# ============================================================================
GAME_CONFIG = {
    "questions_per_game":5,
    "points_per_correct":1,
    "timeout_seconds":120,
    "max_active_games_per_user":1
}

# ============================================================================
# Helpers
# ============================================================================
def normalize_text(text:str)->str:
    if not text:
        return ""
    text = text.strip().lower()
    replacements = {'أ':'ا','إ':'ا','آ':'ا','ى':'ي','ة':'ه'}
    for o,n in replacements.items():
        text = text.replace(o,n)
    return text

def get_theme_colors(theme_name:str=None)->Dict[str,str]:
    if theme_name is None:
        theme_name = DEFAULT_THEME
    return THEMES.get(theme_name,THEMES[DEFAULT_THEME])

def validate_theme(theme_name:str)->str:
    return theme_name if theme_name in THEMES else DEFAULT_THEME

def get_username(profile)->str:
    try:
        return profile.display_name if profile.display_name else "مستخدم"
    except:
        return "مستخدم"
