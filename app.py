"""
Bot Mesh - LINE Bot Application (Enhanced Edition)
Created by: Abeer Aldosari © 2025

Features:
- Neumorphism Soft Design with 9 themes
- AI-powered question generation with 3 fallback keys
- Smart answer validation
- Performance optimized
- Group-friendly (responds only to registered users)
- Auto-cleanup after 7 days of inactivity
- Theme persistence across all interfaces
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# ============================================================================
# Configuration
# ============================================================================
BOT_NAME = "Bot Mesh"
BOT_VERSION = "2.0.0"
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

# Gemini API Keys (3 keys for intelligent fallback)
GEMINI_API_KEY_1 = os.getenv('GEMINI_API_KEY_1')
GEMINI_API_KEY_2 = os.getenv('GEMINI_API_KEY_2')
GEMINI_API_KEY_3 = os.getenv('GEMINI_API_KEY_3')

if not LINE_CHANNEL_SECRET or not LINE_CHANNEL_ACCESS_TOKEN:
    raise ValueError("❌ Missing LINE credentials!")

# ============================================================================
# Flask Setup
# ============================================================================
app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ============================================================================
# In-Memory Data Storage
# ============================================================================
registered_users = {}  # {user_id: {name, points, is_registered, created_at, last_activity}}
user_themes = {}       # {user_id: theme_emoji}
active_games = {}      # {user_id: game_instance}

# ============================================================================
# Neumorphism Soft Themes (9 Professional Themes)
# ============================================================================
THEMES = {
    "💜": {
        "name": "Purple Dream",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#9F7AEA",
        "secondary": "#B794F4",
        "text": "#44337A",
        "text2": "#6B46C1",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "💚": {
        "name": "Green Nature",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#48BB78",
        "secondary": "#68D391",
        "text": "#234E52",
        "text2": "#2C7A7B",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🤍": {
        "name": "Clean White",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#667EEA",
        "secondary": "#7F9CF5",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🖤": {
        "name": "Dark Mode",
        "bg": "#2D3748",
        "card": "#3A4556",
        "primary": "#667EEA",
        "secondary": "#7F9CF5",
        "text": "#E2E8F0",
        "text2": "#CBD5E0",
        "shadow1": "#1A202C",
        "shadow2": "#414D5F"
    },
    "💙": {
        "name": "Ocean Blue",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#3182CE",
        "secondary": "#4299E1",
        "text": "#2C5282",
        "text2": "#2B6CB0",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🩶": {
        "name": "Silver Gray",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#718096",
        "secondary": "#A0AEC0",
        "text": "#2D3748",
        "text2": "#4A5568",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🩷": {
        "name": "Pink Blossom",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#D53F8C",
        "secondary": "#ED64A6",
        "text": "#702459",
        "text2": "#97266D",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🧡": {
        "name": "Sunset Orange",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#DD6B20",
        "secondary": "#ED8936",
        "text": "#7C2D12",
        "text2": "#C05621",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🤎": {
        "name": "Earth Brown",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "primary": "#8B4513",
        "secondary": "#A0522D",
        "text": "#5C2E00",
        "text2": "#7A4F1D",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    }
}

DEFAULT_THEME = "💜"

# ============================================================================
# AI Integration with Smart Fallback
# ============================================================================
current_gemini_key = 0
gemini_keys = [k for k in [GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3] if k]

def get_next_gemini_key():
    """Get next available Gemini API key with rotation"""
    global current_gemini_key
    if not gemini_keys:
        logger.warning("⚠️ No Gemini API keys available")
        return None
    
    key = gemini_keys[current_gemini_key % len(gemini_keys)]
    current_gemini_key += 1
    logger.info(f"🔑 Using Gemini key #{current_gemini_key % len(gemini_keys) + 1}")
    return key

def ai_generate_question(game_type):
    """Generate question using Gemini AI with fallback"""
    try:
        import google.generativeai as genai
        key = get_next_gemini_key()
        if not key:
            return None
        
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompts = {
            "IQ": "أنشئ لغز ذكاء عربي مع إجابة قصيرة. رد بصيغة JSON: {\"q\": \"السؤال\", \"a\": \"الإجابة\"}",
            "رياضيات": "أنشئ مسألة رياضية بسيطة مع الحل. رد بصيغة JSON: {\"q\": \"المسألة\", \"a\": \"الجواب\"}",
            "عكس": "أعط كلمة عربية وعكسها. رد بصيغة JSON: {\"word\": \"الكلمة\", \"opposite\": \"العكس\"}"
        }
        
        prompt = prompts.get(game_type, prompts["IQ"])
        response = model.generate_content(prompt)
        
        import json
        text = response.text.strip()
        
        # Clean JSON from markdown
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        return json.loads(text.strip())
    except Exception as e:
        logger.error(f"❌ AI generation error: {e}")
        return None

def ai_check_answer(correct_answer, user_answer):
    """Check answer using Gemini AI with smart validation"""
    try:
        import google.generativeai as genai
        key = get_next_gemini_key()
        if not key:
            return False
        
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"هل الإجابة '{user_answer}' صحيحة للجواب '{correct_answer}'? رد فقط بـ 'نعم' أو 'لا'"
        response = model.generate_content(prompt)
        
        answer_text = response.text.strip().lower()
        return 'نعم' in answer_text or 'yes' in answer_text
    except Exception as e:
        logger.error(f"❌ AI check error: {e}")
        return False

# ============================================================================
# Game Loading System
# ============================================================================
AVAILABLE_GAMES = {}

try:
    from games.iq_game import IqGame
    from games.math_game import MathGame
    from games.word_color_game import WordColorGame
    from games.scramble_word_game import ScrambleWordGame
    from games.fast_typing_game import FastTypingGame
    from games.opposite_game import OppositeGame
    from games.letters_words_game import LettersWordsGame
    from games.song_game import SongGame
    from games.human_animal_plant_game import HumanAnimalPlantGame
    from games.chain_words_game import ChainWordsGame
    from games.guess_game import GuessGame
    from games.compatibility_game import CompatibilityGame
    
    AVAILABLE_GAMES = {
        "IQ": IqGame,
        "رياضيات": MathGame,
        "لون الكلمة": WordColorGame,
        "كلمة مبعثرة": ScrambleWordGame,
        "كتابة سريعة": FastTypingGame,
        "عكس": OppositeGame,
        "حروف وكلمات": LettersWordsGame,
        "أغنية": SongGame,
        "إنسان حيوان نبات": HumanAnimalPlantGame,
        "سلسلة كلمات": ChainWordsGame,
        "تخمين": GuessGame,
        "توافق": CompatibilityGame
    }
    logger.info(f"✅ تم تحميل {len(AVAILABLE_GAMES)} لعبة بنجاح")
except Exception as e:
    logger.error(f"❌ خطأ في تحميل الألعاب: {e}")

# ============================================================================
# UI Builder Functions with Enhanced Design
# ============================================================================
def build_home(theme="💜", username="مستخدم", points=0, is_registered=False):
    """نافذة البداية مع تصميم Neumorphism محسّن"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    status = "✅ مسجل" if is_registered else "⚪ غير مسجل"
    status_color = "#48BB78" if is_registered else "#CBD5E0"
    
    # Theme selector buttons (3 rows)
    theme_rows = []
    theme_list = list(THEMES.keys())
    for i in range(0, len(theme_list), 3):
        row_themes = theme_list[i:i+3]
        theme_rows.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": f"{t}", "text": f"ثيم {t}"},
                    "style": "primary" if t == theme else "secondary",
                    "height": "sm",
                    "color": colors["primary"] if t == theme else colors["shadow1"]
                }
                for t in row_themes
            ]
        })
    
    contents = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xl",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎮 Bot Mesh",
                            "weight": "bold",
                            "size": "xxl",
                            "color": colors["primary"],
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": "بوت الألعاب الترفيهية الذكي",
                            "size": "sm",
                            "color": colors["text2"],
                            "align": "center"
                        }
                    ],
                    "spacing": "xs"
                },
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": f"👤 {username}",
                                    "size": "lg",
                                    "color": colors["text"],
                                    "weight": "bold"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": status,
                                            "size": "sm",
                                            "color": status_color,
                                            "flex": 0
                                        },
                                        {
                                            "type": "text",
                                            "text": f"⭐ {points} نقطة",
                                            "size": "sm",
                                            "color": colors["primary"],
                                            "align": "end"
                                        }
                                    ]
                                }
                            ],
                            "backgroundColor": colors["card"],
                            "cornerRadius": "20px",
                            "paddingAll": "20px"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": "🎨 اختر ثيمك المفضل:",
                    "size": "md",
                    "weight": "bold",
                    "color": colors["text"]
                }
            ] + theme_rows,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "📝 انضم", "text": "انضم"},
                            "style": "primary" if not is_registered else "secondary",
                            "height": "sm",
                            "color": colors["primary"] if not is_registered else colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🚪 انسحب", "text": "انسحب"},
                            "style": "secondary",
                            "height": "sm"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"},
                            "style": "secondary",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🏆 صدارة", "text": "صدارة"},
                            "style": "secondary",
                            "height": "sm"
                        }
                    ]
                },
                {
                    "type": "button",
                    "action": {"type": "message", "label": "🎮 الألعاب", "text": "مساعدة"},
                    "style": "primary",
                    "height": "sm",
                    "color": colors["primary"]
                },
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "color": colors["text2"],
                    "align": "center"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(alt_text=f"{BOT_NAME} - البداية", contents=FlexContainer.from_dict(contents))

def build_games_menu(theme="💜"):
    """نافذة الألعاب مع تصميم محسّن"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    game_buttons = [
        {"icon": "🧠", "label": "ذكاء", "text": "لعبة IQ"},
        {"icon": "🎨", "label": "لون", "text": "لعبة لون الكلمة"},
        {"icon": "🔤", "label": "ترتيب", "text": "لعبة كلمة مبعثرة"},
        {"icon": "🔢", "label": "رياضيات", "text": "لعبة رياضيات"},
        {"icon": "⚡", "label": "أسرع", "text": "لعبة كتابة سريعة"},
        {"icon": "↔️", "label": "ضد", "text": "لعبة عكس"},
        {"icon": "🔠", "label": "تكوين", "text": "لعبة حروف وكلمات"},
        {"icon": "🎵", "label": "أغنية", "text": "لعبة أغنية"},
        {"icon": "🌍", "label": "لعبة", "text": "لعبة إنسان حيوان نبات"},
        {"icon": "🔗", "label": "سلسلة", "text": "لعبة سلسلة كلمات"},
        {"icon": "🔮", "label": "خمّن", "text": "لعبة تخمين"},
        {"icon": "💕", "label": "توافق", "text": "لعبة توافق"}
    ]
    
    # تقسيم الأزرار إلى صفوف (3 في كل صف)
    rows = []
    for i in range(0, len(game_buttons), 3):
        row = {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "message", "label": f"{btn['icon']} {btn['label']}", "text": btn["text"]},
                    "style": "secondary",
                    "height": "sm",
                    "color": colors["primary"]
                }
                for btn in game_buttons[i:i+3]
            ]
        }
        rows.append(row)
    
    contents = {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "🎮 الألعاب المتاحة",
                    "weight": "bold",
                    "size": "xl",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"اختر من {len(AVAILABLE_GAMES)} لعبة مختلفة",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center"
                },
                {"type": "separator", "color": colors["shadow1"]}
            ] + rows + [
                {"type": "separator", "color": colors["shadow1"]},
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "text",
                            "text": "💡 الأوامر أثناء اللعب:",
                            "size": "sm",
                            "color": colors["text"],
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "• لمح - للحصول على تلميح\n• جاوب - لكشف الإجابة\n• إيقاف - لإنهاء اللعبة",
                            "size": "xs",
                            "color": colors["text2"],
                            "wrap": True
                        }
                    ],
                    "backgroundColor": colors["card"],
                    "cornerRadius": "15px",
                    "paddingAll": "15px"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🏠 بداية", "text": "بداية"},
                            "style": "secondary",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "⛔ إيقاف", "text": "إيقاف"},
                            "style": "primary",
                            "height": "sm",
                            "color": "#FF5555"
                        }
                    ]
                },
                {"type": "separator", "color": colors["shadow1"]},
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "color": colors["text2"],
                    "align": "center"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(alt_text=f"{BOT_NAME} - الألعاب", contents=FlexContainer.from_dict(contents))

def build_my_points(username, points, theme="💜"):
    """نافذة نقاطي مع تصميم محسّن"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    # تحديد المستوى بناءً على النقاط
    if points < 50:
        level = "🌱 مبتدئ"
        level_color = "#48BB78"
    elif points < 150:
        level = "⭐ متوسط"
        level_color = "#667EEA"
    elif points < 300:
        level = "🔥 متقدم"
        level_color = "#DD6B20"
    else:
        level = "👑 محترف"
        level_color = "#D53F8C"
    
    contents = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xl",
            "contents": [
                {
                    "type": "text",
                    "text": "⭐ نقاطي",
                    "weight": "bold",
                    "size": "xl",
                    "color": colors["primary"],
                    "align": "center"
                },
                {"type": "separator", "color": colors["shadow1"]},
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "lg",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"👤 {username}",
                            "size": "lg",
                            "color": colors["text"],
                            "weight": "bold",
                            "align": "center"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "النقاط الكلية",
                                    "size": "sm",
                                    "color": colors["text2"],
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": f"{points}",
                                    "size": "xxl",
                                    "weight": "bold",
                                    "color": colors["primary"],
                                    "align": "center"
                                }
                            ],
                            "backgroundColor": colors["card"],
                            "cornerRadius": "20px",
                            "paddingAll": "25px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "المستوى الحالي",
                                    "size": "sm",
                                    "color": colors["text2"],
                                    "align": "center"
                                },
                                {
                                    "type": "text",
                                    "text": level,
                                    "size": "lg",
                                    "weight": "bold",
                                    "color": level_color,
                                    "align": "center"
                                }
                            ],
                            "backgroundColor": colors["card"],
                            "cornerRadius": "15px",
                            "paddingAll": "15px"
                        },
                        {"type": "separator", "color": colors["shadow1"]},
                        {
                            "type": "text",
                            "text": "⚠️ سيتم حذف بياناتك بعد 7 أيام من عدم النشاط",
                            "size": "xs",
                            "color": "#FF5555",
                            "wrap": True,
                            "align": "center"
                        }
                    ]
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🏠 بداية", "text": "بداية"},
                            "style": "secondary",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🎮 ألعاب", "text": "مساعدة"},
                            "style": "secondary",
                            "height": "sm"
                        }
                    ]
                },
                {"type": "separator", "color": colors["shadow1"]},
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "color": colors["text2"],
                    "align": "center"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(contents))

def build_leaderboard(top_users, theme="💜"):
    """نافذة الصدارة مع تصميم محسّن"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    leaderboard_contents = []
    medals = ["🥇", "🥈", "🥉"]
    
    for i, (name, points) in enumerate(top_users[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        medal_color = colors["primary"] if i <= 3 else colors["text"]
        
        leaderboard_contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": medal,
                    "size": "lg",
                    "flex": 0,
                    "color": medal_color
                },
                {
                    "type": "text",
                    "text": name,
                    "size": "sm",
                    "color": colors["text"],
                    "flex": 3
                },
                {
                    "type": "text",
                    "text": f"{points}",
                    "size": "sm",
                    "color": colors["primary"],
                    "align": "end",
                    "flex": 1
                }
            ],
            "spacing": "md",
            "paddingAll": "sm"
        })
    
    if not leaderboard_contents:
        leaderboard_contents.append({
            "type": "text",
            "text": "لا يوجد لاعبين مسجلين بعد",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        })
    
    contents = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": "🏆 لوحة الصدارة",
                    "weight": "bold",
                    "size": "xl",
                    "color": colors["primary"],
                    "align": "center"
                },
                {"type": "separator", "color": colors["shadow1"]},
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": leaderboard_contents,
                    "backgroundColor": colors["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "20px"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "🏠 بداية", "text": "بداية"},
                            "style": "secondary",
                            "height": "sm"
                        },
                        {
                            "type": "button",
                            "action": {"type": "message", "label": "⭐ نقاطي", "text": "نقاطي"},
                            "style": "secondary",
                            "height": "sm"
                        }
                    ]
                },
                {"type": "separator", "color": colors["shadow1"]},
                {
                    "type": "text",
                    "text": BOT_RIGHTS,
                    "size": "xxs",
                    "color": colors["text2"],
                    "align": "center"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "styles": {
            "body": {"backgroundColor": colors["bg"]},
            "footer": {"backgroundColor": colors["bg"]}
        }
    }
    
    return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(contents))

# ============================================================================
# Helper Functions
# ============================================================================
def get_username(profile):
    """Get username from LINE profile safely"""
    try:
        return profile.display_name if profile.display_name else "مستخدم"
    except:
        return "مستخدم"

def update_user_activity(user_id):
    """Update last activity timestamp"""
    if user_id in registered_users:
        registered_users[user_id]['last_activity'] = datetime.now()

def cleanup_inactive_users():
    """Remove users inactive for 7 days"""
    cutoff = datetime.now() - timedelta(days=7)
    inactive = [
        uid for uid, data in registered_users.items() 
        if data.get('last_activity', datetime.now()) < cutoff
    ]
    
    for uid in inactive:
        if uid in registered_users:
            del registered_users[uid]
        if uid in user_themes:
            del user_themes[uid]
        if uid in active_games:
            del active_games[uid]
    
    if inactive:
        logger.info(f"🧹 تنظيف {len(inactive)} مستخدم غير نشط")

def is_group_chat(event):
    """Check if message is from a group"""
    return hasattr(event.source, 'group_id')

# ============================================================================
# Flask Routes
# ============================================================================
@app.route("/callback", methods=['POST'])
def callback():
    """LINE webhook callback"""
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("❌ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Callback error: {e}")
        abort(500)
    
    return 'OK'

@app.route("/", methods=['GET'])
def home():
    """Bot status page"""
    cleanup_inactive_users()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{BOT_NAME} v{BOT_VERSION}</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            
            .container {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 30px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                text-align: center;
            }}
            
            h1 {{
                font-size: 3em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }}
            
            .version {{
                font-size: 0.9em;
                opacity: 0.8;
                margin-bottom: 30px;
            }}
            
            .status {{
                font-size: 1.3em;
                margin: 30px 0;
                padding: 20px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 20px;
            }}
            
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            
            .stat-card {{
                background: rgba(255, 255, 255, 0.2);
                padding: 20px;
                border-radius: 20px;
            }}
            
            .stat-value {{
                font-size: 2.5em;
                font-weight: bold;
                margin: 10px 0;
            }}
            
            .stat-label {{
                font-size: 0.9em;
                opacity: 0.9;
            }}
            
            .footer {{
                margin-top: 30px;
                font-size: 0.85em;
                opacity: 0.7;
            }}
            
            .pulse {{
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.6; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 {BOT_NAME}</h1>
            <div class="version">Version {BOT_VERSION}</div>
            
            <div class="status pulse">
                ✅ Bot is running smoothly
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{len(registered_users)}</div>
                    <div class="stat-label">👥 المستخدمين</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(AVAILABLE_GAMES)}</div>
                    <div class="stat-label">🎮 الألعاب</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(active_games)}</div>
                    <div class="stat-label">⚡ نشط الآن</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(gemini_keys)}</div>
                    <div class="stat-label">🤖 AI Keys</div>
                </div>
            </div>
            
            <div class="footer">
                {BOT_RIGHTS}
            </div>
        </div>
    </body>
    </html>
    """

# ============================================================================
# Message Handler - Smart & Group-Friendly
# ============================================================================
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """Handle incoming messages with smart logic"""
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        if not text:
            return
        
        # Check if in group - only respond to registered users
        in_group = is_group_chat(event)
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            # Get user profile
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
            except:
                username = "مستخدم"
            
            # Check mention for groups
            if in_group and "@" not in text.lower():
                # In groups, only respond if user is registered and playing
                if user_id not in registered_users or not registered_users[user_id].get('is_registered'):
                    return
                # Also check if they have an active game
                if user_id not in active_games:
                    return
            
            # Register new user
            if user_id not in registered_users:
                registered_users[user_id] = {
                    "name": username,
                    "points": 0,
                    "is_registered": False,
                    "created_at": datetime.now(),
                    "last_activity": datetime.now()
                }
                logger.info(f"👤 مستخدم جديد: {username}")
                
                current_theme = user_themes.get(user_id, DEFAULT_THEME)
                welcome = build_home(current_theme, username, 0, False)
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[welcome])
                )
                return
            
            # Update activity
            update_user_activity(user_id)
            
            # Get user data
            current_theme = user_themes.get(user_id, DEFAULT_THEME)
            user_data = registered_users[user_id]
            reply = None
            
            text_lower = text.lower()
            
            # Commands handling
            if text_lower == "بداية" or "@" in text_lower:
                reply = build_home(current_theme, username, user_data['points'], user_data['is_registered'])
            
            elif text_lower == "مساعدة":
                reply = build_games_menu(current_theme)
            
            elif text.startswith("ثيم "):
                theme = text.replace("ثيم ", "").strip()
                if theme in THEMES:
                    user_themes[user_id] = theme
                    reply = build_home(theme, username, user_data['points'], user_data['is_registered'])
            
            elif text == "انضم":
                registered_users[user_id]["is_registered"] = True
                reply = build_home(current_theme, username, user_data['points'], True)
            
            elif text == "انسحب":
                registered_users[user_id]["is_registered"] = False
                reply = build_home(current_theme, username, user_data['points'], False)
            
            elif text == "نقاطي":
                reply = build_my_points(username, user_data['points'], current_theme)
            
            elif text == "صدارة":
                sorted_users = sorted(
                    [(u["name"], u["points"]) for u in registered_users.values() if u.get("is_registered")],
                    key=lambda x: x[1],
                    reverse=True
                )
                reply = build_leaderboard(sorted_users, current_theme)
            
            elif text == "إيقاف":
                if user_id in active_games:
                    del active_games[user_id]
                    reply = build_games_menu(current_theme)
            
            elif text.startswith("لعبة "):
                if not user_data.get("is_registered"):
                    colors = THEMES[current_theme]
                    msg_content = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "⚠️ يجب التسجيل أولاً",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": colors["primary"],
                                    "align": "center"
                                },
                                {"type": "separator"},
                                {
                                    "type": "text",
                                    "text": "اضغط 'انضم' للتسجيل والبدء باللعب",
                                    "size": "sm",
                                    "color": colors["text2"],
                                    "align": "center",
                                    "wrap": True
                                }
                            ],
                            "backgroundColor": colors["bg"],
                            "paddingAll": "20px"
                        }
                    }
                    reply = FlexMessage(alt_text="تسجيل مطلوب", contents=FlexContainer.from_dict(msg_content))
                else:
                    game_name = text.replace("لعبة ", "").strip()
                    if game_name in AVAILABLE_GAMES:
                        GameClass = AVAILABLE_GAMES[game_name]
                        
                        # Create game instance with AI support
                        if game_name in ["IQ", "رياضيات", "عكس"]:
                            game_instance = GameClass(line_bot_api)
                            # Pass AI functions if available
                            if hasattr(game_instance, 'ai_generate_question'):
                                game_instance.ai_generate_question = lambda: ai_generate_question(game_name)
                            if hasattr(game_instance, 'ai_check_answer'):
                                game_instance.ai_check_answer = ai_check_answer
                        else:
                            game_instance = GameClass(line_bot_api)
                        
                        game_instance.set_theme(current_theme)
                        active_games[user_id] = game_instance
                        reply = game_instance.start_game()
                        
                        logger.info(f"🎮 {username} بدأ لعبة {game_name}")
            
            else:
                # Game answer handling
                if user_id in active_games:
                    game_instance = active_games[user_id]
                    result = game_instance.check_answer(text, user_id, username)
                    
                    if result:
                        # Update points
                        if result.get('points', 0) > 0:
                            registered_users[user_id]['points'] += result['points']
                        
                        # End game if over
                        if result.get('game_over'):
                            del active_games[user_id]
                        
                        reply = result.get('response')
                else:
                    # No active game - show home
                    reply = build_home(current_theme, username, user_data['points'], user_data['is_registered'])
            
            # Send reply
            if reply:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[reply])
                )
                
    except Exception as e:
        logger.error(f"❌ Error in handle_message: {e}", exc_info=True)

# ============================================================================
# Run Application
# ============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {BOT_NAME} v{BOT_VERSION}")
    logger.info(f"📦 Loaded {len(AVAILABLE_GAMES)} games successfully")
    logger.info(f"🤖 AI Keys available: {len(gemini_keys)}")
    logger.info(f"🎨 Themes available: {len(THEMES)}")
    logger.info(f"🌐 Server starting on port {port}")
    logger.info("=" * 60)
    
    app.run(host="0.0.0.0", port=port, debug=False)
