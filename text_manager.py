import random
import os
import re

class TextManager:
    def __init__(self):
        self.base_path = "games"

        # تعريف الملفات والبادئات المراد إزالتها
        self.files_config = {
            "challenges.txt": "تحدي ",
            "confessions.txt": "اعتراف ",
            "mentions.txt": "منشن ",
            "personality.txt": "شخصية ",
            "questions.txt": "سؤال ",
            "quotes.txt": "حكمة ",
            "situations.txt": "موقف "
        }

        # تحميل الملفات وتنظيفها
        self.original_content = {}  # المحتوى الأصلي لكل ملف
        for file in self.files_config:
            self.original_content[file] = self._load_file(file)

        # محتوى متبقي لكل أمر لتجنب التكرار
        self.remaining_content = {
            "تحدي": self.original_content["challenges.txt"].copy(),
            "اعتراف": self.original_content["confessions.txt"].copy(),
            "منشن": self.original_content["mentions.txt"].copy(),
            "شخصيه": self.original_content["personality.txt"].copy(),
            "شخصية": self.original_content["personality.txt"].copy(),
            "سؤال": self.original_content["questions.txt"].copy(),
            "حكمه": self.original_content["quotes.txt"].copy(),
            "حكمة": self.original_content["quotes.txt"].copy(),
            "موقف": self.original_content["situations.txt"].copy()
        }

    def _load_file(self, filename):
        """
        قراءة الملف وإرجاع قائمة الأسطر بعد إزالة البادئة وتجاهل الرموز غير النصية.
        """
        path = os.path.join(self.base_path, filename)
        remove_prefix = self.files_config.get(filename, None)
        lines = []

        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue  # تجاهل الأسطر الفارغة
                    if remove_prefix and line.startswith(remove_prefix):
                        line = line[len(remove_prefix):]  # إزالة البادئة
                    # تجاهل الأسطر التي تحتوي فقط على رموز غير نصية
                    if not re.search(r'\w', line, re.UNICODE):
                        continue
                    lines.append(line)

            if not lines:
                print(f"[Warning] {filename} فارغ أو يحتوي أسطر غير صالحة، سيتم استخدام رسالة افتراضية")
                return ["المحتوى غير متوفر"]

            print(f"[Info] تم تحميل {len(lines)} أسطر صالحة من {filename}")
            return lines

        except Exception as e:
            print(f"[Error] لم يتم تحميل {filename}: {e}")
            return ["المحتوى غير متوفر"]

    def get_content(self, cmd):
        """
        إرجاع محتوى عشوائي من الأمر بدون تكرار حتى يتم استنفاد كل المحتوى.
        عند استنفاد المحتوى، يتم إعادة تعبئة القائمة تلقائيًا.
        """
        if cmd not in self.remaining_content:
            print(f"[Warning] الأمر '{cmd}' غير موجود في cmd_mapping")
            return None

        # إعادة تعبئة القائمة إذا انتهت
        if not self.remaining_content[cmd]:
            original_file = {
                "تحدي": "challenges.txt",
                "اعتراف": "confessions.txt",
                "منشن": "mentions.txt",
                "شخصيه": "personality.txt",
                "شخصية": "personality.txt",
                "سؤال": "questions.txt",
                "حكمه": "quotes.txt",
                "حكمة": "quotes.txt",
                "موقف": "situations.txt"
            }[cmd]
            self.remaining_content[cmd] = self.original_content[original_file].copy()
            print(f"[Info] تم إعادة تعبئة قائمة '{cmd}' بعد استنفادها")

        # اختيار عنصر عشوائي وإزالته من القائمة
        choice = random.choice(self.remaining_content[cmd])
        self.remaining_content[cmd].remove(choice)
        return choice
