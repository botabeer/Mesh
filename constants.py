# constants.py
import os

# -------------------------------
# LINE Bot Credentials
# -------------------------------
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

# -------------------------------
# Gemini AI API Keys
# -------------------------------
GEMINI_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
]

GEMINI_MODEL = "Gemini (gemini-2.0-flash-exp)"

# -------------------------------
# Bot Settings
# -------------------------------
BOT_NAME = "Bot Mesh"
BOT_CREATOR = "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025"
BOT_COLOR_THEME = "3D_Professional"
BOT_RESPONSE_MODE = "silent"  # يرد فقط على المسجلين والأوامر
MAX_ROUNDS_DEFAULT = 5
POINTS_PER_WIN = 10
POINTS_PER_CORRECT = 5

# -------------------------------
# UI / UX Settings
# -------------------------------
THEMES = [
    "💜", "💚", "🤍", "🖤", "💙", "🩶", "🩷", "🧡", "🤎"
]

# رموز ثابتة للواجهات
UI_SYMBOLS = {
    "bullet_white": "▫️",
    "bullet_black": "▪️",
    "medal": "🏅",
    "trophy": "🏆",
}

# -------------------------------
# Arabic Character Normalization
# -------------------------------
ARABIC_CHAR_MAP = {
    "أ": "ا",
    "إ": "ا",
    "آ": "ا",
    "ة": "ه",
    "ى": "ي",
    "ئ": "ي",
    "ؤ": "و",
}

def normalize_arabic(text: str) -> str:
    """حول الحروف العربية إلى صيغها العادية لتسهيل المطابقة."""
    normalized = text.strip()
    for key, val in ARABIC_CHAR_MAP.items():
        normalized = normalized.replace(key, val)
    return normalized.lower()

# -------------------------------
# Game Settings
# -------------------------------
# جميع الألعاب يمكن تغييرها أو إضافة ألعاب جديدة بدون قاعدة ثابته
GAMES_DIR = "games"
# هذا مجرد مثال على أسماء الألعاب
AVAILABLE_GAMES = [
    "IqGame",
    "MathGame",
    "WordColorGame",
    "ScrambleWordGame",
    "FastTypingGame",
    "OppositeGame",
    "LettersWordsGame",
    "SongGame",
    "HumanAnimalPlantGame",
    "ChainWordsGame",
    "GuessGame",
    "CompatibilityGame",
]

# -------------------------------
# Fixed Buttons (Bottom Screen)
# -------------------------------
# كل البوت نوافذ فلكس وأزرار أسفل الشاشة بشكل دائم
FIXED_BOTTOM_BUTTONS = [
    {"title": "🏠 الرئيسية", "action": "home"},
    {"title": "🎮 الألعاب", "action": "games"},
    {"title": "ℹ️ مساعدة", "action": "help"},
    {"title": "🔄 إعادة", "action": "restart"},
]

# -------------------------------
# User Settings
# -------------------------------
# قاعدة بيانات للأسماء لتصحيح الاسم حسب Line
USER_NAME_DATABASE = {}

def get_user_name(user_id: str, line_profile_name: str) -> str:
    """احفظ اسم المستخدم حسب ID وأرجعه."""
    if user_id not in USER_NAME_DATABASE:
        USER_NAME_DATABASE[user_id] = line_profile_name
    return USER_NAME_DATABASE[user_id]

# -------------------------------
# Answer Validation
# -------------------------------
def is_valid_answer(user_answer: str, correct_answers: list[str]) -> bool:
    """
    تحقق من الإجابة وقارن مع قائمة الإجابات الصحيحة بعد التطبيع.
    يقبل تنويعات الكلمات والأحرف العربية المختلفة.
    """
    normalized_answer = normalize_arabic(user_answer)
    for ans in correct_answers:
        if normalize_arabic(ans) == normalized_answer:
            return True
    return False

# -------------------------------
# LINE Policy Compliance
# -------------------------------
# جميع الصيغ والنوافذ والتنسيق متوافق مع قوانين LINE
LINE_COMPLIANCE = True
