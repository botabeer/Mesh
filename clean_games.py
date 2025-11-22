import os

# المجلد الأساسي للألعاب
GAMES_DIR = "games"

# الملفات الصحيحة التي تريد الاحتفاظ بها (snake_case)
VALID_FILES = {
    "iq_game.py",
    "word_color_game.py",
    "chain_words_game.py",
    "scramble_word_game.py",
    "letters_words_game.py",
    "fast_typing_game.py",
    "human_animal_plant_game.py",
    "guess_game.py",
    "compatibility_game.py",
    "math_game.py",
    "memory_game.py",
    "riddle_game.py",
    "opposite_game.py",
    "emoji_game.py",
    "song_game.py",
    "__init__.py"
}

def clean_games_folder():
    print("🔍 Starting cleanup...")

    if not os.path.isdir(GAMES_DIR):
        print("❌ Folder 'games/' not found!")
        return

    for filename in os.listdir(GAMES_DIR):
        full_path = os.path.join(GAMES_DIR, filename)

        # تخطّي المجلدات
        if os.path.isdir(full_path):
            continue

        # حذف أي ملف غير موجود ضمن القائمة الصحيحة
        if filename not in VALID_FILES:
            print(f"🗑️ Deleting: {filename}")
            os.remove(full_path)

    print("\n✅ Cleanup completed! Folder is now clean and correct.")

if __name__ == "__main__":
    clean_games_folder()
