import random
import os
import re
import logging

logger = logging.getLogger(__name__)

class TextManager:
    def __init__(self):
        self.base_path = "games"
        
        self.files_config = {
            "challenges.txt": "تحدي ",
            "confessions.txt": "اعتراف ",
            "mentions.txt": "منشن ",
            "personality.txt": "شخصية ",
            "questions.txt": "سؤال ",
            "quotes.txt": "حكمة ",
            "situations.txt": "موقف "
        }
        
        self.original_content = {}
        for file in self.files_config:
            self.original_content[file] = self._load_file(file)
        
        self.cmd_mapping = {
            "تحدي": "challenges.txt",
            "اعتراف": "confessions.txt",
            "منشن": "mentions.txt",
            "شخصيه": "personality.txt",
            "شخصية": "personality.txt",
            "سؤال": "questions.txt",
            "حكمه": "quotes.txt",
            "حكمة": "quotes.txt",
            "موقف": "situations.txt"
        }
        
        self.remaining_content = {}
        for cmd in self.cmd_mapping:
            file = self.cmd_mapping[cmd]
            self.remaining_content[cmd] = self.original_content[file].copy()

    def _load_file(self, filename):
        path = os.path.join(self.base_path, filename)
        remove_prefix = self.files_config.get(filename, None)
        lines = []

        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if remove_prefix and line.startswith(remove_prefix):
                        line = line[len(remove_prefix):]
                    if not re.search(r'\w', line, re.UNICODE):
                        continue
                    lines.append(line)

            if not lines:
                logger.warning(f"{filename} empty or contains invalid lines")
                return ["المحتوى غير متوفر"]

            logger.info(f"Loaded {len(lines)} lines from {filename}")
            return lines

        except Exception as e:
            logger.error(f"Failed to load {filename}: {e}")
            return ["المحتوى غير متوفر"]

    def get_content(self, cmd):
        if cmd not in self.remaining_content:
            logger.warning(f"Command '{cmd}' not found")
            return None

        if not self.remaining_content[cmd]:
            file = self.cmd_mapping[cmd]
            self.remaining_content[cmd] = self.original_content[file].copy()
            logger.info(f"Refilled content list for '{cmd}'")

        choice = random.choice(self.remaining_content[cmd])
        self.remaining_content[cmd].remove(choice)
        return choice
