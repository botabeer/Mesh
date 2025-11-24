import os
import json
import random
import unicodedata
from datetime import datetime, timedelta

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ----------------------
# normalize Arabic letters for checking answers
# ----------------------
def normalize_answer(text):
    replacements = {
        "أ":"ا","إ":"ا","آ":"ا","ى":"ي","ئ":"ي","ؤ":"و","ة":"ه"
    }
    text = text.strip().lower()
    for k,v in replacements.items():
        text = text.replace(k,v)
    text = unicodedata.normalize("NFKD", text)
    return text

# ----------------------
# load questions from local files
# ----------------------
def load_local_questions(game_name):
    file_path = os.path.join("games", f"{game_name}.json")
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------
# save user answer (temporary DB)
# ----------------------
def save_user_answer(user_id, user_name, game_name, answer, correct):
    file_path = os.path.join(DATA_DIR, f"{user_id}.json")
    data = {}
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    now = datetime.now().isoformat()
    data[game_name] = {"name": user_name, "answer": answer, "correct": correct, "time": now}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ----------------------
# get user stats
# ----------------------
def get_user_stats(user_id):
    file_path = os.path.join(DATA_DIR, f"{user_id}.json")
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------
# clean old data (>7 أيام)
# ----------------------
def clean_old_data():
    cutoff = datetime.now() - timedelta(days=7)
    for filename in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, filename)
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    # تحقق من التاريخ لكل لعبة
                    keep = False
                    for g in data.values():
                        t = datetime.fromisoformat(g.get("time", datetime.now().isoformat()))
                        if t > cutoff:
                            keep = True
                    if not keep:
                        os.remove(path)
                except:
                    os.remove(path)
