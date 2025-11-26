"""
🎮 Bot Mesh v7.0 - Game Loader
تحميل الألعاب تلقائياً من مجلد games/
"""

import os
import sys
import importlib
import inspect
import logging

logger = logging.getLogger(__name__)

class GameLoader:
    """محمّل الألعاب التلقائي"""

    def __init__(self):
        """تهيئة المحمّل"""
        self.games = {}
        
        # تحديد مسار مجلد games
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.games_dir = os.path.join(current_dir, 'games')
        
        # التحقق من وجود المجلد
        if not os.path.exists(self.games_dir):
            logger.error(f"❌ مجلد games/ غير موجود في: {self.games_dir}")
            return

        # إضافة مجلد games للمسار
        if self.games_dir not in sys.path:
            sys.path.insert(0, self.games_dir)

        # تحميل الألعاب
        self._load_games()

        logger.info(f"✅ تم تحميل {len(self.games)} لعبة")

    def _load_games(self):
        """تحميل جميع الألعاب من مجلد games/"""
        
        # خريطة الألعاب (اسم الملف ← اسم اللعبة في القائمة)
        game_mapping = {
            "iq_game": "ذكاء",
            "math_game": "رياضيات",
            "fast_typing_game": "سرعة",
            "letters_words_game": "تكوين",
            "word_color_game": "ألوان",
            "opposite_game": "أضداد",
            "chain_words_game": "سلسلة",
            "guess_game": "تخمين",
            "song_game": "أغنية",
            "human_animal_plant_game": "إنسان حيوان",
            "compatibility_game": "توافق",
            "scramble_word_game": "كلمات"
        }

        for file_name, game_name in game_mapping.items():
            try:
                # استيراد الوحدة
                module = importlib.import_module(file_name)

                # البحث عن كلاس اللعبة
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # تحقق من أن الكلاس يحتوي على الميثودات المطلوبة
                    if (hasattr(obj, 'start_game') and 
                        hasattr(obj, 'check_answer') and
                        'Game' in name):
                        
                        self.games[game_name] = obj
                        logger.info(f"  ✓ {game_name}")
                        break

            except Exception as e:
                logger.error(f"  ✗ فشل تحميل {game_name}: {e}")

    def create_game(self, game_name: str, line_bot_api=None):
        """
        إنشاء نسخة من اللعبة
        
        Args:
            game_name: اسم اللعبة (مثل "ذكاء")
            line_bot_api: واجهة LINE Bot API (اختياري)
        """
        if game_name not in self.games:
            logger.warning(f"⚠️ لعبة '{game_name}' غير موجودة")
            return None
        
        try:
            GameClass = self.games[game_name]
            
            # إنشاء اللعبة مع تمرير line_bot_api إذا كانت تحتاجه
            if line_bot_api:
                return GameClass(line_bot_api)
            else:
                return GameClass()
                
        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء لعبة {game_name}: {e}")
            return None

    def get_available_games(self) -> list:
        """الحصول على قائمة الألعاب المتاحة"""
        return list(self.games.keys())
    
    def get_game_info(self, game_name: str) -> dict:
        """الحصول على معلومات اللعبة"""
        if game_name not in self.games:
            return None
        
        try:
            GameClass = self.games[game_name]
            # محاولة الحصول على معلومات من الكلاس
            if hasattr(GameClass, 'get_game_info'):
                temp_game = GameClass()
                return temp_game.get_game_info()
            else:
                return {
                    "name": game_name,
                    "available": True
                }
        except:
            return {
                "name": game_name,
                "available": True
            }
```

---

## 3️⃣ هيكل المشروع الصحيح
```
Bot-Mesh/
│
├── app.py                      ← الملف الرئيسي
├── config.py                   ← الإعدادات
├── ui.py                       ← واجهة المستخدم
├── game_loader.py              ← محمّل الألعاب (في الجذر!)
│
├── requirements.txt
├── Procfile
├── Dockerfile
├── docker-compose.yml
├── .env                        ← للتطوير المحلي فقط (لا ترفعه لـ Git)
├── .gitignore
│
└── games/                      ← مجلد الألعاب
    ├── __init__.py
    ├── base_game.py
    ├── iq_game.py
    ├── math_game.py
    ├── fast_typing_game.py
    ├── opposite_game.py
    ├── word_color_game.py
    ├── chain_words_game.py
    ├── guess_game.py
    ├── song_game.py
    ├── human_animal_plant_game.py
    ├── compatibility_game.py
    ├── scramble_word_game.py
    └── letters_words_game.py
```

---

## 4️⃣ خطوات الربط مع LINE (بالتفصيل)

### 🔧 الخطوة 1: إعداد LINE Developers Console

1. **الدخول إلى Console:**
   - اذهب إلى: https://developers.line.biz/console/
   - سجّل دخول بحساب LINE الخاص بك

2. **إنشاء Provider (إذا لم يكن موجود):**
   - اضغط "Create a new provider"
   - أدخل اسم الـ Provider (مثل: "Bot Mesh Games")

3. **إنشاء Channel:**
   - اختر نوع القناة: **Messaging API**
   - املأ المعلومات المطلوبة:
     * Channel name: "Bot Mesh"
     * Channel description: "بوت ألعاب تفاعلي"
     * Category: اختر المناسب
     * Subcategory: اختر المناسب

4. **الحصول على المفاتيح:**
   - **Channel Secret:**
     * اذهب إلى تبويب "Basic settings"
     * انسخ "Channel secret"
   
   - **Channel Access Token:**
     * اذهب إلى تبويب "Messaging API"
     * في قسم "Channel access token (long-lived)"
     * اضغط "Issue" لإنشاء token جديد
     * انسخ الـ Token (لن تتمكن من رؤيته مرة أخرى!)

---

### 🔧 الخطوة 2: ضبط المتغيرات في Render

1. **الدخول إلى Render Dashboard:**
   - اذهب إلى خدمتك (Service)

2. **إضافة Environment Variables:**
   - اذهب إلى "Environment"
   - اضغط "Add Environment Variable"
   - أضف:
```
LINE_CHANNEL_ACCESS_TOKEN = <الصق الـ Token هنا>
LINE_CHANNEL_SECRET = <الصق الـ Secret هنا>
PORT = 10000  (اختياري - Render يحدده تلقائياً)
```

3. **حفظ وإعادة النشر:**
   - اضغط "Save Changes"
   - سيتم إعادة نشر الخدمة تلقائياً

---

### 🔧 الخطوة 3: ضبط Webhook في LINE

1. **في LINE Console:**
   - اذهب إلى قناتك → "Messaging API"
   - ابحث عن "Webhook settings"

2. **ضبط Webhook URL:**
```
   https://mesh-k3ca.onrender.com/callback
