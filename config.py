"""
Bot Mesh - Configuration
Created by: Abeer Aldosari © 2025
"""
import os

# LINE Bot Configuration
LINE_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')

# Database Configuration
DB_PATH = os.getenv('DB_PATH', 'data/game.db')

# Themes Configuration
THEMES = {
    'white': {
        'bg': '#FFFFFF',
        'card': '#F5F5F5',
        'primary': '#FFFFFF',   # 🤍
        'text': '#2C3E50',
        'text2': '#718096',
        'name': '🤍 أبيض'
    },
    'black': {
        'bg': '#0F0F1A',
        'card': '#1A1A2E',
        'primary': '#000000',   # 🖤
        'text': '#FFFFFF',
        'text2': '#A0AEC0',
        'name': '🖤 أسود'
    },
    'blue': {
        'bg': '#0C1929',
        'card': '#1E3A5F',
        'primary': '#00D9FF',   # 💙
        'text': '#E0F2FE',
        'text2': '#7DD3FC',
        'name': '💙 أزرق'
    },
    'green': {
        'bg': '#ECFDF5',
        'card': '#D1FAE5',
        'primary': '#10B981',   # 💚
        'text': '#064E3B',
        'text2': '#047857',
        'name': '💚 أخضر'
    },
    'pink': {
        'bg': '#FFF1F2',
        'card': '#FFE4E6',
        'primary': '#EC4899',   # 🩷
        'text': '#831843',
        'text2': '#BE185D',
        'name': '🩷 وردي'
    },
    'gray': {
        'bg': '#1A202C',
        'card': '#2D3748',
        'primary': '#9CA3AF',   # 🩶
        'text': '#F7FAFC',
        'text2': '#CBD5E0',
        'name': '🩶 رمادي'
    },
    'orange': {
        'bg': '#FFF7ED',
        'card': '#F97316',
        'primary': '#F97316',   # 🧡
        'text': '#FFFFFF',
        'text2': '#555555',
        'name': '🧡 برتقالي'
    },
    'purple': {
        'bg': '#F5F3FF',
        'card': '#8B5CF6',
        'primary': '#8B5CF6',   # 💜
        'text': '#FFFFFF',
        'text2': '#555555',
        'name': '💜 بنفسجي'
    },
    'brown': {
        'bg': '#FFF8F0',
        'card': '#A0522D',
        'primary': '#A0522D',   # 🤎
        'text': '#FFFFFF',
        'text2': '#555555',
        'name': '🤎 بني'
    }
}

# Game Settings
DEFAULT_ROUNDS = 5
WIN_THRESHOLD = 30
