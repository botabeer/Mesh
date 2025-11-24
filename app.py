# -*- coding: utf-8 -*-
"""
Bot Mesh - LINE Bot Application (Optimized & LINE Compatible)
Created by: Abeer Aldosari © 2025
"""

import os
import sys
import logging
from datetime import datetime
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
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"

LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

if not LINE_CHANNEL_SECRET or not LINE_CHANNEL_ACCESS_TOKEN:
    raise ValueError("❌ Missing LINE credentials!")

# ============================================================================
# Flask Setup
# ============================================================================
app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ============================================================================
# In-Memory Data
# ============================================================================
registered_users = {}
user_themes = {}
active_games = {}

# ============================================================================
# Themes - Neumorphism Soft Style (LINE Compatible)
# ============================================================================
THEMES = {
    "💜": {
        "primary": "#9F7AEA",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "text": "#44337A",
        "text2": "#6B46C1",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "💚": {
        "primary": "#48BB78",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "text": "#234E52",
        "text2": "#2C7A7B",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🤍": {
        "primary": "#667EEA",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "text": "#2D3748",
        "text2": "#718096",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🖤": {
        "primary": "#667EEA",
        "bg": "#2D3748",
        "card": "#3A4556",
        "text": "#E2E8F0",
        "text2": "#CBD5E0",
        "shadow1": "#1A202C",
        "shadow2": "#414D5F"
    },
    "💙": {
        "primary": "#3182CE",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "text": "#2C5282",
        "text2": "#2B6CB0",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🩶": {
        "primary": "#718096",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "text": "#2D3748",
        "text2": "#4A5568",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🩷": {
        "primary": "#D53F8C",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "text": "#702459",
        "text2": "#97266D",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🧡": {
        "primary": "#DD6B20",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "text": "#7C2D12",
        "text2": "#C05621",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    },
    "🤎": {
        "primary": "#8B4513",
        "bg": "#E0E5EC",
        "card": "#E0E5EC",
        "text": "#5C2E00",
        "text2": "#7A4F1D",
        "shadow1": "#A3B1C6",
        "shadow2": "#FFFFFF"
    }
}

DEFAULT_THEME = "💜"

# ============================================================================
# Game Loading
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
    logger.info(f"✅ تم تحميل {len(AVAILABLE_GAMES)} لعبة")
except Exception as e:
    logger.error(f"❌ خطأ في تحميل الألعاب: {e}")

# ============================================================================
# UI Builder Functions (LINE Compatible)
# ============================================================================

def build_home(theme="💜", username="مستخدم", points=0, is_registered=False):
    """نافذة البداية مع أزرار ثابتة (LINE Compatible)"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    status = "✅ مسجل" if is_registered else "⚠️ غير مسجل"
    
    contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": f"🎮 {BOT_NAME}",
                    "weight": "bold",
                    "size": "xl",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "بوت الألعاب الترفيهية",
                    "size": "xs",
                    "color": colors["text2"],
                    "align": "center"
                },
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"▪️ مرحباً: {username}",
                            "size": "sm",
                            "color": colors["text"]
                        },
                        {
                            "type": "text",
                            "text": f"▪️ الحالة: {status}",
                            "size": "sm",
                            "color": colors["text"]
                        },
                        {
                            "type": "text",
                            "text": f"▪️ نقاطك: {points}",
                            "size": "sm",
                            "color": colors["text"]
                        },
                        {
                            "type": "text",
                            "text": "▪️ اختر ثيمك:",
                            "size": "sm",
                            "weight": "bold",
                            "color": colors["primary"]
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
                            "action": {
                                "type": "message",
                                "label": t,
                                "text": f"ثيم {t}"
                            },
                            "style": "primary" if t == theme else "secondary",
                            "height": "sm",
                            "color": colors["primary"] if t == theme else colors["shadow1"]
                        }
                        for t in list(THEMES.keys())[:3]
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": t,
                                "text": f"ثيم {t}"
                            },
                            "style": "primary" if t == theme else "secondary",
                            "height": "sm",
                            "color": colors["primary"] if t == theme else colors["shadow1"]
                        }
                        for t in list(THEMES.keys())[3:6]
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": t,
                                "text": f"ثيم {t}"
                            },
                            "style": "primary" if t == theme else "secondary",
                            "height": "sm",
                            "color": colors["primary"] if t == theme else colors["shadow1"]
                        }
                        for t in list(THEMES.keys())[6:]
                    ]
                },
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "text",
                    "text": "🕹️ الأزرار الثابتة:",
                    "size": "sm",
                    "weight": "bold",
                    "color": colors["primary"]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "انضم",
                                "text": "انضم"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "انسحب",
                                "text": "انسحب"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "نقاطي",
                                "text": "نقاطي"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "صدارة",
                                "text": "صدارة"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
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
                    "type": "text",
                    "text": "📝 ملاحظة: يمكنك استخدام البوت في الخاص أو القروبات",
                    "size": "xxs",
                    "color": colors["text2"],
                    "align": "center",
                    "wrap": True
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
            "paddingAll": "10px"
        }
    }
    
    return FlexMessage(alt_text="Bot Mesh - البداية", contents=FlexContainer.from_dict(contents))

def build_games_menu(theme="💜"):
    """نافذة المساعدة مع الألعاب وأزرار ثابتة (LINE Compatible)"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": f"🤖 {BOT_NAME} – مساعدة",
                    "weight": "bold",
                    "size": "xl",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "text",
                    "text": "🎮 الألعاب المتاحة:",
                    "weight": "bold",
                    "size": "md",
                    "color": colors["primary"]
                },
                {
                    "type": "text",
                    "text": "ذكاء – رياضيات – لون – أسرع – ترتيب – أغنية\nكلمة – سلسلة – خمن – توافق",
                    "size": "sm",
                    "color": colors["text"],
                    "wrap": True
                },
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "text",
                    "text": "📝 الأوامر أثناء اللعب (كنص):",
                    "weight": "bold",
                    "size": "md",
                    "color": colors["primary"]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "text",
                            "text": "▫️ لمح → تلميح أول حرف وعدد حروف الكلمة",
                            "size": "xs",
                            "color": colors["text"],
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "▫️ جاوب → لإرسال إجابتك",
                            "size": "xs",
                            "color": colors["text"]
                        },
                        {
                            "type": "text",
                            "text": "▫️ إيقاف → لإيقاف اللعبة",
                            "size": "xs",
                            "color": colors["text"]
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
            "spacing": "xs",
            "contents": [
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "text",
                    "text": "⛔ إيقاف",
                    "weight": "bold",
                    "size": "sm",
                    "color": "#FF5555",
                    "align": "center"
                },
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "ذكاء",
                                "text": "لعبة IQ"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "لون",
                                "text": "لعبة لون الكلمة"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "ترتيب",
                                "text": "لعبة كلمة مبعثرة"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "رياضيات",
                                "text": "لعبة رياضيات"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "أسرع",
                                "text": "لعبة كتابة سريعة"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "ضد",
                                "text": "لعبة عكس"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "تكوين",
                                "text": "لعبة حروف وكلمات"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "أغنية",
                                "text": "لعبة أغنية"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "لعبة",
                                "text": "لعبة إنسان حيوان نبات"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "سلسلة",
                                "text": "لعبة سلسلة كلمات"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "خمن",
                                "text": "لعبة تخمين"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "توافق",
                                "text": "لعبة توافق"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        }
                    ]
                },
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "text",
                    "text": "📝 ملاحظة: يمكنك استخدام البوت في الخاص أو القروبات",
                    "size": "xxs",
                    "color": colors["text2"],
                    "align": "center",
                    "wrap": True
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
            "paddingAll": "10px"
        }
    }
    
    return FlexMessage(alt_text="Bot Mesh - مساعدة", contents=FlexContainer.from_dict(contents))

def build_my_points(username, points, theme="💜"):
    """نافذة نقاطي (LINE Compatible)"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": f"{theme} نقاطي",
                    "weight": "bold",
                    "size": "xl",
                    "color": colors["primary"],
                    "align": "center"
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
                            "type": "text",
                            "text": f"👤 الاسم: {username}",
                            "size": "md",
                            "color": colors["text"],
                            "weight": "bold"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "⭐ النقاط",
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
                            "paddingAll": "20px"
                        },
                        {
                            "type": "separator",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "text",
                            "text": "⚠️ تحذير: سيتم حذف بياناتك بعد 7 أيام من عدم النشاط",
                            "size": "xs",
                            "color": "#FF5551",
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
            "spacing": "xs",
            "contents": [
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "بداية",
                                "text": "بداية"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "مساعدة",
                                "text": "مساعدة"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        }
                    ]
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
            "paddingAll": "10px"
        }
    }
    
    return FlexMessage(alt_text="الصدارة", contents=FlexContainer.from_dict(contents))

def send_fixed_buttons(line_bot_api, reply_token, theme="💜"):
    """إرسال الأزرار الثابتة عند منشنة البوت"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": f"🎮 {BOT_NAME}",
                    "weight": "bold",
                    "size": "xxl",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": "بوت الألعاب الترفيهية",
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center"
                },
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "text",
                    "text": "مرحباً بك! اضغط على الأزرار أدناه للبدء 👇",
                    "size": "md",
                    "color": colors["text"],
                    "wrap": True,
                    "align": "center"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "بداية",
                                "text": "بداية"
                            },
                            "style": "primary",
                            "height": "sm",
                            "color": colors["primary"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "مساعدة",
                                "text": "مساعدة"
                            },
                            "style": "primary",
                            "height": "sm",
                            "color": colors["primary"]
                        }
                    ]
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
            "paddingAll": "10px"
        }
    }
    
    flex_message = FlexMessage(alt_text="Bot Mesh - مرحباً!", contents=FlexContainer.from_dict(contents))
    
    try:
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=[flex_message])
        )
    except Exception as e:
        logger.error(f"❌ خطأ في إرسال الأزرار الثابتة: {e}")

# ============================================================================
# Helper Functions
# ============================================================================

def get_username(profile):
    """Get username from LINE profile"""
    try:
        return profile.display_name
    except:
        return "مستخدم"

def update_user_activity(user_id):
    """Update last activity"""
    if user_id in registered_users:
        registered_users[user_id]['last_activity'] = datetime.now()

# ============================================================================
# Flask Routes
# ============================================================================

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("⚠️ Invalid signature")
        abort(400)
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        abort(500)
    
    return 'OK'

@app.route("/", methods=['GET'])
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{BOT_NAME}</title>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                max-width: 600px;
                text-align: center;
            }}
            h1 {{ font-size: 2.5em; margin-bottom: 20px; }}
            .status {{ font-size: 1.2em; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 {BOT_NAME}</h1>
            <div class="status">✅ Bot is running</div>
            <p>Users: {len(registered_users)} | Games: {len(AVAILABLE_GAMES)} | Active: {len(active_games)}</p>
            <p style="font-size: 0.8em; opacity: 0.7; margin-top: 20px;">{BOT_RIGHTS}</p>
        </div>
    </body>
    </html>
    """

# ============================================================================
# Message Handler
# ============================================================================

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    try:
        user_id = event.source.user_id
        text = event.message.text.strip()
        
        if not text:
            return
        
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            
            try:
                profile = line_bot_api.get_profile(user_id)
                username = get_username(profile)
            except:
                username = "مستخدم"
            
            # التحقق من المنشن - إرسال الأزرار الثابتة
            if "@" in text and "bot mesh" in text.lower():
                current_theme = user_themes.get(user_id, DEFAULT_THEME)
                send_fixed_buttons(line_bot_api, event.reply_token, current_theme)
                return
            
            # New user registration
            if user_id not in registered_users:
                registered_users[user_id] = {
                    "name": username,
                    "points": 0,
                    "is_registered": False,
                    "created_at": datetime.now(),
                    "last_activity": datetime.now()
                }
                logger.info(f"✅ New user: {username}")
                
                current_theme = user_themes.get(user_id, DEFAULT_THEME)
                welcome_reply = build_home(current_theme, username, 0, False)
                
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[welcome_reply])
                )
                return
            
            update_user_activity(user_id)
            
            current_theme = user_themes.get(user_id, DEFAULT_THEME)
            user_data = registered_users[user_id]
            reply = None
            
            text_lower = text.lower()
            
            # Commands
            if text_lower == "بداية" or text_lower == "home":
                reply = build_home(current_theme, username, user_data['points'], user_data['is_registered'])
            elif text_lower == "مساعدة" or text_lower == "games":
                reply = build_games_menu(current_theme)
            elif text.startswith("ثيم "):
                theme = text.replace("ثيم ", "").strip()
                if theme in THEMES:
                    user_themes[user_id] = theme
                    reply = build_home(theme, username, user_data['points'], user_data['is_registered'])
            elif text == "انضم":
                registered_users[user_id]["is_registered"] = True
                reply = TextMessage(text=f"✅ مرحباً {username}! تم تسجيلك بنجاح")
            elif text == "انسحب":
                registered_users[user_id]["is_registered"] = False
                reply = TextMessage(text=f"👋 {username} تم إلغاء تسجيلك")
            elif text == "نقاطي":
                reply = build_my_points(username, user_data['points'], current_theme)
            elif text == "صدارة":
                sorted_users = sorted(
                    [(u["name"], u["points"]) for u in registered_users.values() if u.get("is_registered")],
                    key=lambda x: x[1], reverse=True
                )
                reply = build_leaderboard(sorted_users, current_theme)
            elif text == "إيقاف":
                if user_id in active_games:
                    del active_games[user_id]
                    reply = TextMessage(text="⛔ تم إيقاف اللعبة")
            elif text.startswith("لعبة "):
                if not user_data.get("is_registered"):
                    reply = TextMessage(text="⚠️ يجب التسجيل أولاً")
                else:
                    game_name = text.replace("لعبة ", "").strip()
                    if game_name in AVAILABLE_GAMES:
                        GameClass = AVAILABLE_GAMES[game_name]
                        game_instance = GameClass(line_bot_api)
                        game_instance.set_theme(current_theme)
                        active_games[user_id] = game_instance
                        reply = game_instance.start_game()
            else:
                if user_id in active_games:
                    game_instance = active_games[user_id]
                    result = game_instance.check_answer(text, user_id, username)
                    if result:
                        if result.get('points', 0) > 0:
                            registered_users[user_id]['points'] += result['points']
                        if result.get('game_over'):
                            del active_games[user_id]
                        reply = result.get('response')
                else:
                    reply = TextMessage(text=f"مرحباً {username}! 👋\nاضغط على 'بداية' للبدء أو 'مساعدة' لعرض الألعاب 🎮")
            
            if reply:
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=[reply])
                )
                
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)

# ============================================================================
# Run
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    logger.info(f"🚀 Starting {BOT_NAME} on port {port}")
    logger.info(f"📦 Loaded {len(AVAILABLE_GAMES)} games")
    app.run(host="0.0.0.0", port=port, debug=False)
                                "text": "مساعدة"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        }
                    ]
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
            "paddingAll": "10px"
        }
    }
    
    return FlexMessage(alt_text="نقاطي", contents=FlexContainer.from_dict(contents))

def build_leaderboard(top_users, theme="💜"):
    """نافذة الصدارة (LINE Compatible)"""
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    leaderboard_contents = []
    medals = ["🥇", "🥈", "🥉"]
    
    for i, (name, points) in enumerate(top_users[:10], 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        leaderboard_contents.append({
            "type": "text",
            "text": f"{medal} {name}: {points} نقطة",
            "size": "sm",
            "color": colors["text"]
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
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "🏆 لوحة الصدارة",
                    "weight": "bold",
                    "size": "xl",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": leaderboard_contents,
                    "backgroundColor": colors["card"],
                    "cornerRadius": "20px",
                    "paddingAll": "15px"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
                {
                    "type": "separator",
                    "color": colors["shadow1"]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "xs",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "بداية",
                                "text": "بداية"
                            },
                            "style": "secondary",
                            "height": "sm",
                            "color": colors["shadow1"]
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "مساعدة",
