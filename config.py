"""
Bot Mesh - Configuration
Created by: Abeer Aldosari © 2025
"""
import os

# LINE Bot Configuration
LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')

# Database Configuration
DATA_DIR = os.getenv('DATA_DIR', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.getenv('DB_PATH', os.path.join(DATA_DIR, 'game.db'))

# Game Settings
DEFAULT_ROUNDS = 5
POINTS_PER_CORRECT = 10  # نقاط لكل إجابة صحيحة
POINTS_PER_WIN = 50  # نقاط إضافية للفائز
WIN_THRESHOLD = 30

# Themes Configuration - Neumorphism Soft Style
THEMES = {
    'white': {
        'bg': '#E0E5EC',
        'card': '#D1D9E6',
        'primary': '#667EEA',
        'text': '#2C3E50',
        'text2': '#7F8C8D',
        'shadow_light': '#FFFFFF',
        'shadow_dark': '#A3B1C6',
        'name': '🤍 أبيض'
    },
    'black': {
        'bg': '#0F0F1A',
        'card': '#1A1A2E',
        'primary': '#00D9FF',
        'text': '#FFFFFF',
        'text2': '#A0AEC0',
        'shadow_light': '#2A2A3E',
        'shadow_dark': '#000000',
        'name': '🖤 أسود'
    },
    'gray': {
        'bg': '#1A202C',
        'card': '#2D3748',
        'primary': '#68D391',
        'text': '#F7FAFC',
        'text2': '#CBD5E0',
        'shadow_light': '#3D4758',
        'shadow_dark': '#0D1117',
        'name': '🩶 رمادي'
    },
    'blue': {
        'bg': '#0C1929',
        'card': '#1E3A5F',
        'primary': '#00D9FF',
        'text': '#E0F2FE',
        'text2': '#7DD3FC',
        'shadow_light': '#2E4A6F',
        'shadow_dark': '#000A19',
        'name': '💙 أزرق'
    },
    'green': {
        'bg': '#0F1F0F',
        'card': '#1E3F1E',
        'primary': '#10B981',
        'text': '#E0FFE0',
        'text2': '#7DFC7D',
        'shadow_light': '#2E4F2E',
        'shadow_dark': '#000F00',
        'name': '💚 أخضر'
    },
    'pink': {
        'bg': '#FFF1F2',
        'card': '#FFE4E6',
        'primary': '#EC4899',
        'text': '#831843',
        'text2': '#BE185D',
        'shadow_light': '#FFFFFF',
        'shadow_dark': '#FFD4D9',
        'name': '🩷 وردي'
    },
    'orange': {
        'bg': '#1F0F00',
        'card': '#3F1E00',
        'primary': '#F97316',
        'text': '#FFEBCF',
        'text2': '#FFB07C',
        'shadow_light': '#4F2E00',
        'shadow_dark': '#0F0700',
        'name': '🧡 برتقالي'
    },
    'purple': {
        'bg': '#1E1B4B',
        'card': '#312E81',
        'primary': '#A855F7',
        'text': '#F5F3FF',
        'text2': '#C4B5FD',
        'shadow_light': '#413E91',
        'shadow_dark': '#0E0B3B',
        'name': '💜 بنفسجي'
    },
    'brown': {
        'bg': '#1A0F0F',
        'card': '#2D1A1A',
        'primary': '#A0522D',
        'text': '#F7F5F0',
        'text2': '#C0A080',
        'shadow_light': '#3D2A2A',
        'shadow_dark': '#0A0707',
        'name': '🤎 بني'
    }
}

# AI Configuration (Optional)
AI_ENABLED = os.getenv('AI_ENABLED', 'false').lower() == 'true'
AI_MODEL = os.getenv('AI_MODEL', 'claude-sonnet-4-20250514')
AI_API_KEY = os.getenv('AI_API_KEY', '')
