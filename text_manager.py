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
        self.challenges = self._load_file("challenges.txt")
        self.confessions = self._load_file("confessions.txt")
        self.mentions = self._load_file("mentions.txt")
        self.personality = self._load_file("personality.txt")
        self.questions = self._load_file("questions.txt")
        self.quotes = self._load_file("quotes.txt")
        self.situations = self._load_file("situations.txt")
        
        # ربط الأوامر بالمحتوى
        self.cmd_mapping = {
            "تحدي": self.challenges,
            "اعتراف": self.confessions,
            "منشن": self.mentions,
            "شخصيه": self.personality,
            "شخصية": self.personality,
            "سؤال": self.questions,
            "حكمه": self.quotes,
            "حكمة": self.quotes,
            "موقف": self.situations
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
        إرجاع محتوى عشوائي بناءً على الأمر.
        """
        content_list = self.cmd_mapping.get(cmd)
        if content_list:
            return random.choice(content_list)
        print(f"[Warning] الأمر '{cmd}' غير موجود في cmd_mapping")
        return None
