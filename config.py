"""
⚙️ ملف الإعدادات المركزي
يحتوي على جميع الإعدادات القابلة للتعديل
"""

import os
from dataclasses import dataclass
from typing import List

@dataclass
class BotSettings:
    """إعدادات البوت الأساسية"""
    
    # LINE Bot Credentials
    LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_TOKEN')
    LINE_CHANNEL_SECRET: str = os.getenv('LINE_CHANNEL_SECRET', 'YOUR_SECRET')
    
    # Gemini AI Keys
    GEMINI_API_KEYS: List[str] = None
    
    # Database
    DATABASE_NAME: str = 'game_scores.db'
    
    # Game Prefix (البادئة)
    GAME_PREFIX: str = '/'  # يمكن تغييرها إلى ! أو # أو أي رمز
    BOT_MENTION: str = '@bot'  # منشن البوت
    
    # Rate Limiting
    MAX_MESSAGES_PER_MINUTE: int = 20
    MAX_GAMES_PER_HOUR: int = 10
    RATE_LIMIT_WINDOW: int = 60  # بالثواني
    
    # Game Settings
    MAX_GAME_DURATION: int = 30  # بالدقائق
    AUTO_CLEANUP_INTERVAL: int = 300  # تنظيف كل 5 دقائق
    MAX_PLAYERS_PER_GAME: int = 50
    
    # Points System
    POINTS_PER_WIN: int = 100
    POINTS_PER_CORRECT_ANSWER: int = 10
    POINTS_PER_LOSS: int = 0
    BONUS_POINTS_STREAK: int = 50  # مكافأة السلسلة
    
    # Leaderboard
    LEADERBOARD_SIZE: int = 10
    
    # Smart Response Settings
    SILENT_MODE_ENABLED: bool = True  # تفعيل الوضع الصامت
    MIN_MESSAGE_LENGTH_TO_RESPOND: int = 3  # الحد الأدنى لطول الرسالة للرد
    IGNORE_SHORT_MESSAGES: bool = True  # تجاهل الرسائل القصيرة جداً
    
    # Group Settings
    REQUIRE_REGISTRATION: bool = True  # يتطلب تسجيل
    ALLOW_NON_REGISTERED_VIEW: bool = True  # السماح بعرض الإحصائيات لغير المسجلين
    
    # Logging
    LOG_LEVEL: str = 'INFO'  # DEBUG, INFO, WARNING, ERROR
    LOG_FILE: str = 'bot.log'
    
    def __post_init__(self):
        """تهيئة بعد الإنشاء"""
        if self.GEMINI_API_KEYS is None:
            self.GEMINI_API_KEYS = [
                k for k in [
                    os.getenv(f'GEMINI_API_KEY_{i}', '') 
                    for i in range(1, 4)
                ] if k
            ]
    
    def is_valid(self) -> bool:
        """التحقق من صحة الإعدادات"""
        if self.LINE_CHANNEL_ACCESS_TOKEN == 'YOUR_TOKEN':
            return False
        if self.LINE_CHANNEL_SECRET == 'YOUR_SECRET':
            return False
        return True
    
    def get_game_commands(self) -> List[str]:
        """الحصول على قائمة أوامر الألعاب"""
        return [
            f"{self.GAME_PREFIX}ذكاء",
            f"{self.GAME_PREFIX}لون",
            f"{self.GAME_PREFIX}سلسلة",
            f"{self.GAME_PREFIX}ترتيب",
            f"{self.GAME_PREFIX}تكوين",
            f"{self.GAME_PREFIX}أسرع",
            f"{self.GAME_PREFIX}لعبة",
            f"{self.GAME_PREFIX}خمن",
            f"{self.GAME_PREFIX}رياضيات",
            f"{self.GAME_PREFIX}ذاكرة",
            f"{self.GAME_PREFIX}لغز",
            f"{self.GAME_PREFIX}ضد",
            f"{self.GAME_PREFIX}أغنية",
        ]

# إنشاء كائن الإعدادات العامة
settings = BotSettings()

# إعدادات الألعاب الفردية
GAME_CONFIGS = {
    'ذكاء': {
        'rounds': 10,
        'time_per_question': 30,
        'points_per_correct': 10,
        'use_ai': True
    },
    'لون': {
        'rounds': 10,
        'time_per_question': 10,
        'points_per_correct': 5,
        'use_ai': False
    },
    'سلسلة': {
        'rounds': 15,
        'time_per_question': 20,
        'points_per_correct': 10,
        'use_ai': False
    },
    'ترتيب': {
        'rounds': 10,
        'time_per_question': 20,
        'points_per_correct': 10,
        'use_ai': False
    },
    'تكوين': {
        'rounds': 10,
        'time_per_question': 30,
        'points_per_correct': 15,
        'use_ai': True
    },
    'أسرع': {
        'rounds': 5,
        'time_per_question': 10,
        'points_per_correct': 20,
        'use_ai': False
    },
    'لعبة': {
        'rounds': 10,
        'time_per_question': 25,
        'points_per_correct': 10,
        'use_ai': True
    },
    'خمن': {
        'rounds': 5,
        'time_per_question': 60,
        'points_per_correct': 30,
        'use_ai': False
    },
    'رياضيات': {
        'rounds': 10,
        'time_per_question': 15,
        'points_per_correct': 10,
        'use_ai': False
    },
    'ذاكرة': {
        'rounds': 5,
        'time_per_question': 30,
        'points_per_correct': 20,
        'use_ai': False
    },
    'لغز': {
        'rounds': 5,
        'time_per_question': 60,
        'points_per_correct': 25,
        'use_ai': True
    },
    'ضد': {
        'rounds': 10,
        'time_per_question': 15,
        'points_per_correct': 10,
        'use_ai': False
    },
    'أغنية': {
        'rounds': 10,
        'time_per_question': 30,
        'points_per_correct': 15,
        'use_ai': False
    }
}

# رسائل البوت
BOT_MESSAGES = {
    'welcome': "🎮 مرحباً! أنا بوت الألعاب\n\nللعب استخدم: / + اسم اللعبة\nمثال: /ذكاء",
    'not_registered': "❌ يجب التسجيل أولاً\nاكتب: انضم",
    'game_started': "🎮 بدأت اللعبة! استعد...",
    'game_ended': "🏁 انتهت اللعبة!",
    'correct_answer': "✅ إجابة صحيحة! +{points} نقطة",
    'wrong_answer': "❌ إجابة خاطئة",
    'timeout': "⏰ انتهى الوقت!",
    'rate_limit': "⚠️ كثير من الرسائل! انتظر قليلاً",
    'no_game_active': "❌ لا توجد لعبة نشطة\nاستخدم / + اسم اللعبة للبدء",
    'already_registered': "✅ أنت مسجل بالفعل",
    'registration_success': "✅ تم التسجيل بنجاح!\n\nاستخدم / + اسم اللعبة للبدء",
    'error_occurred': "❌ حدث خطأ. حاول مرة أخرى"
}

# Emojis للتنسيق
EMOJIS = {
    'trophy': '🏆',
    'star': '⭐',
    'fire': '🔥',
    'brain': '🧠',
    'game': '🎮',
    'check': '✅',
    'cross': '❌',
    'timer': '⏰',
    'medal': '🥇',
    'party': '🎉',
    'thinking': '🤔',
    'rocket': '🚀',
    'crown': '👑',
    'chart': '📊'
}
