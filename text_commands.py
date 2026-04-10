import random
import os
from threading import Lock


class TextCommands:
    _data = {}
    _remaining = {}
    _lock = Lock()  # إصلاح: lock لمنع race condition عند الاستخدام المتزامن

    _files = {
        'questions':   'games/questions.txt',
        'challenges':  'games/challenges.txt',
        'confessions': 'games/confessions.txt',
        'mentions':    'games/mentions.txt',
        'quotes':      'games/quotes.txt',
        'situations':  'games/situations.txt',
        'poem':        'games/poem.txt',
        'private':     'games/private.txt',
        'anonymous':   'games/anonymous.txt',
        'advice':      'games/advice.txt'
    }

    @classmethod
    def load_all(cls):
        for key, path in cls._files.items():
            try:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = [line.strip() for line in f if line.strip()]
                    cls._data[key] = lines
                else:
                    cls._data[key] = [f"المحتوى غير متوفر لـ {key}"]
                cls._remaining[key] = cls._data[key].copy()
            except Exception as e:
                cls._data[key] = [f"خطأ في تحميل {key}"]
                cls._remaining[key] = cls._data[key].copy()

    @classmethod
    def get_random(cls, cmd):
        if not cls._data:
            cls.load_all()

        if cmd not in cls._data:
            return "لا يوجد محتوى"

        # إصلاح: lock لضمان أمان الخيوط
        with cls._lock:
            if not cls._remaining.get(cmd):
                cls._remaining[cmd] = cls._data[cmd].copy()

            choice = random.choice(cls._remaining[cmd])
            cls._remaining[cmd].remove(choice)

        return choice
