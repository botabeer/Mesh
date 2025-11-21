import os

# LINE Bot Configuration
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', '')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', '')

# Gemini AI Configuration
GEMINI_API_KEYS = [
    os.getenv('GEMINI_API_KEY_1', ''),
    os.getenv('GEMINI_API_KEY_2', ''),
    os.getenv('GEMINI_API_KEY_3', '')
]
GEMINI_API_KEYS = [k for k in GEMINI_API_KEYS if k]

# Bot Configuration
BOT_NAME = "Bot Mesh"
BOT_CREATOR = "عبير الدوسري"
BOT_YEAR = "2025"
VERSION = "1.0.0"

# Game Settings
MAX_MESSAGES_PER_MINUTE = 20
GAME_TIMEOUT_MINUTES = 10
CLEANUP_INTERVAL_SECONDS = 300

# Points System
POINTS = {
    'correct_answer': 10,
    'fast_answer': 15,
    'perfect_answer': 20,
    'win_game': 50
}

# Database
DB_NAME = 'bot_mesh.db'
