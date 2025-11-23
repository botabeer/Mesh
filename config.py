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
os.makedirs(DATA_DIR, exist_ok=True)  # إنشاء المجلد لو لم يكن موجود

DB_PATH = os.getenv('DB_PATH', os.path.join(DATA_DIR, 'game.db'))

# Themes Configuration
THEMES = {
    'black': {
        'bg': '#0F0F1A',
        'card': '#1A1A2E',
        'primary': '#000000',
        'text': '#FFFFFF',
        'text2': '#A0AEC0',
        'name': '🖤 أسود'
    },
    'white': {
        'bg': '#FFFFFF',
        'card': '#F5F5F5',
        'primary': '#667EEA',
        'text': '#2C3E50',
        'text2': '#718096',
        'name': '🤍 أبيض'
    },
    'gray': {
        'bg': '#1A202C',
        'card': '#2D3748',
        'primary': '#68D391',
        'text': '#F7FAFC',
        'text2': '#CBD5E0',
        'name': '🩶 رمادي'
    },
    'blue': {
        'bg': '#0C1929',
        'card': '#1E3A5F',
        'primary': '#00D9FF',
        'text': '#E0F2FE',
        'text2': '#7DD3FC',
        'name': '💙 أزرق'
    },
    'green': {
        'bg': '#0F1F0F',
        'card': '#1E3F1E',
        'primary': '#10B981',
        'text': '#E0F2FE',
        'text2': '#7DD3FC',
        'name': '💚 أخضر'
    },
    'pink': {
        'bg': '#FFF1F2',
        'card': '#FFE4E6',
        'primary': '#EC4899',
        'text': '#831843',
        'text2': '#BE185D',
        'name': '🩷 وردي'
    },
    'orange': {
        'bg': '#1F0F00',
        'card': '#3F1E00',
        'primary': '#F97316',
        'text': '#FFEBCF',
        'text2': '#FFB07C',
        'name': '🧡 برتقالي'
    },
    'purple': {
        'bg': '#1E1B4B',
        'card': '#312E81',
        'primary': '#A855F7',
        'text': '#F5F3FF',
        'text2': '#C4B5FD',
        'name': '💜 بنفسجي'
    },
    'brown': {
        'bg': '#1A0F0F',
        'card': '#2D1A1A',
        'primary': '#A0522D',
        'text': '#F7F5F0',
        'text2': '#C0A080',
        'name': '🤎 بني'
    }
}

# Game Settings
DEFAULT_ROUNDS = 5
WIN_THRESHOLD = 30
