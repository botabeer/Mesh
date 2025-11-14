import os

GAMES_FOLDER = "games"  # مجلد الألعاب

def clean_file(file_path):
    """إزالة أي حرف خفي U+200F من الملف"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    cleaned_content = content.replace("\u200f", "")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cleaned_content)
    print(f"✅ تم تنظيف: {file_path}")

def clean_all_games(folder):
    """تنظيف جميع ملفات .py في المجلد"""
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                clean_file(path)

if __name__ == "__main__":
    clean_all_games(GAMES_FOLDER)
    print("🎉 تم تنظيف جميع ملفات الألعاب بنجاح!")
