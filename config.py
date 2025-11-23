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

# Themes Configuration
THEMES = {
    'black': {
        'bg': '#0F0F1A',
        'card': '#1A1A2E',
        'primary': '#000000',
        'secondary': '#2D2D44',
        'accent': '#4A4A6A',
        'text': '#FFFFFF',
        'text2': '#A0AEC0',
        'border': '#2D2D44',
        'name': '🖤 أسود'
    },
    'white': {
        'bg': '#FFFFFF',
        'card': '#F5F5F5',
        'primary': '#667EEA',
        'secondary': '#E8E8F0',
        'accent': '#7C3AED',
        'text': '#2C3E50',
        'text2': '#718096',
        'border': '#E2E8F0',
        'name': '🤍 أبيض'
    },
    'gray': {
        'bg': '#1A202C',
        'card': '#2D3748',
        'primary': '#68D391',
        'secondary': '#3F4A5A',
        'accent': '#48BB78',
        'text': '#F7FAFC',
        'text2': '#CBD5E0',
        'border': '#4A5568',
        'name': '🩶 رمادي'
    },
    'blue': {
        'bg': '#0C1929',
        'card': '#1E3A5F',
        'primary': '#00D9FF',
        'secondary': '#2A4A6F',
        'accent': '#38BDF8',
        'text': '#E0F2FE',
        'text2': '#7DD3FC',
        'border': '#2E5A8F',
        'name': '💙 أزرق'
    },
    'green': {
        'bg': '#0F1F0F',
        'card': '#1E3F1E',
        'primary': '#10B981',
        'secondary': '#2A4F2A',
        'accent': '#34D399',
        'text': '#E0F2FE',
        'text2': '#7DD3FC',
        'border': '#3A5F3A',
        'name': '💚 أخضر'
    },
    'pink': {
        'bg': '#FFF1F2',
        'card': '#FFE4E6',
        'primary': '#EC4899',
        'secondary': '#FBCFE8',
        'accent': '#F472B6',
        'text': '#831843',
        'text2': '#BE185D',
        'border': '#F9A8D4',
        'name': '🩷 وردي'
    },
    'orange': {
        'bg': '#1F0F00',
        'card': '#3F1E00',
        'primary': '#F97316',
        'secondary': '#5F2E00',
        'accent': '#FB923C',
        'text': '#FFEBCF',
        'text2': '#FFB07C',
        'border': '#7F3E00',
        'name': '🧡 برتقالي'
    },
    'purple': {
        'bg': '#1E1B4B',
        'card': '#312E81',
        'primary': '#A855F7',
        'secondary': '#4C3F91',
        'accent': '#C084FC',
        'text': '#F5F3FF',
        'text2': '#C4B5FD',
        'border': '#5B4FA1',
        'name': '💜 بنفسجي'
    },
    'brown': {
        'bg': '#1A0F0F',
        'card': '#2D1A1A',
        'primary': '#A0522D',
        'secondary': '#3D2A2A',
        'accent': '#D2691E',
        'text': '#F7F5F0',
        'text2': '#C0A080',
        'border': '#4D3A3A',
        'name': '🤎 بني'
    }
}

# Game Settings
DEFAULT_ROUNDS = 5
WIN_THRESHOLD = 30
MAX_GAME_TIME = 300  # 5 دقائق
POINTS_PER_WIN = 10
POINTS_PER_CORRECT = 5

# Bot Settings
BOT_NAME = "Bot Mesh"
BOT_VERSION = "2.0.0"
CLEANUP_DAYS = 7
