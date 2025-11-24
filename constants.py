#import os

# ----------------------
# Gemini AI
# ----------------------
GEMINI_MODEL = "gemini-2.0-flash-exp"
GEMINI_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3")
]

# ----------------------
# الثيمات (9 ألوان)
# ----------------------
THEMES = {
    "💜": "#9C27B0",
    "💚": "#4CAF50",
    "🤍": "#FFFFFF",
    "🖤": "#000000",
    "💙": "#1976D2",
    "🩶": "#E0E0E0",
    "🩷": "#E91E63",
    "🧡": "#FF9800",
    "🤎": "#795548"
}

# ----------------------
# أزرار ثابتة أسفل الشاشة
# ----------------------

# أزرار خاصة بكل لعبة (ألعاب + إيقاف)
FIXED_GAME_BUTTONS = [
    {"type":"button","style":"secondary","color":"#E0E0E0","height":"sm",
     "action":{"type":"message","label":"ألعاب","text":"ألعاب"}},
    {"type":"button","style":"secondary","color":"#D32F2F","height":"sm",
     "action":{"type":"message","label":"إيقاف","text":"إيقاف"}}
]

# أزرار نافذة المساعدة
HELP_SCREEN_BUTTONS = [
    {"type":"button","style":"primary","color":"#3F51B5","height":"sm",
     "action":{"type":"message","label":"انضم","text":"انضم"}},
    {"type":"button","style":"secondary","color":"#E0E0E0","height":"sm",
     "action":{"type":"message","label":"انسحب","text":"انسحب"}},
    {"type":"button","style":"secondary","color":"#E0E0E0","height":"sm",
     "action":{"type":"message","label":"نقاطي","text":"نقاطي"}},
    {"type":"button","style":"secondary","color":"#E0E0E0","height":"sm",
     "action":{"type":"message","label":"صدارة","text":"صدارة"}}
] + FIXED_GAME_BUTTONS  # ألعاب + إيقاف أسفل الشاشة دائمًا

# أزرار نافذة البداية (الثيمات وأوامر البوت)
START_SCREEN_BUTTONS = []  # يمكن إضافة أزرار خاصة بالبداية إذا أردت

# ----------------------
# قواعد ثابتة
# ----------------------
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري @ 2025"
ROUNDS_PER_GAME = 5  # كل لعبة 5 جولات

# ----------------------
# الحروف العربية لتطبيع الإجابات
# ----------------------
ARABIC_NORMALIZATION = {
    "أ":"ا","إ":"ا","آ":"ا","ى":"ي","ئ":"ي","ؤ":"و","ة":"ه"
}

# ----------------------
# أزرار إضافية (إعادة اللعبة)
# ----------------------
REPLAY_BUTTON = [
    {"type":"button","style":"primary","color":"#4CAF50","height":"sm",
     "action":{"type":"message","label":"إعادة","text":"إعادة"}}
]
