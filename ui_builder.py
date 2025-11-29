"""
Bot Mesh - Complete Game System v13.0 FINAL
Created by: Abeer Aldosari © 2025
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from constants import DEFAULT_THEME

BOT_NAME = "Bot Mesh"
BOT_RIGHTS = "تم إنشاء هذا البوت بواسطة عبير الدوسري © 2025"
GAMES_WITH_HINTS = ["ذكاء", "رياضيات", "تحدي", "ألوان", "تكوين", "سلسلة", "خمن", "أغنية", "حروف"]
GAMES_WITHOUT_HINTS = ["سرعة", "لعبة"]
SPECIAL_GAME = "توافق"
OFFICIAL_GAMES = ["ذكاء", "سرعة", "رياضيات", "تحدي", "ألوان", "تكوين", "سلسلة", "خمن", "أغنية", "حروف", "لعبة", "توافق"]

def build_games_quick_reply():
    return QuickReply(items=[QuickReplyItem(action=MessageAction(label=g, text=g)) for g in OFFICIAL_GAMES])

def _btn(label, text, style="primary", color=None):
    b = {"type": "button", "action": {"type": "message", "label": label, "text": text}, "style": style, "height": "sm"}
    if color: b["color"] = color
    return b

def _build_progress_bar(current, total):
    """عداد بصري احترافي للجولات"""
    bars = []
    for i in range(1, total + 1):
        if i < current:
            bars.append({"type": "box", "layout": "vertical", "width": "30px", "height": "8px", "backgroundColor": "#48BB78", "cornerRadius": "4px"})
        elif i == current:
            bars.append({"type": "box", "layout": "vertical", "width": "30px", "height": "8px", "backgroundColor": "#4299E1", "cornerRadius": "4px"})
        else:
            bars.append({"type": "box", "layout": "vertical", "width": "30px", "height": "8px", "backgroundColor": "#E2E8F0", "cornerRadius": "4px"})
        if i < total:
            bars.append({"type": "box", "layout": "vertical", "width": "4px", "height": "8px", "backgroundColor": "#FFFFFF"})
    
    return {"type": "box", "layout": "horizontal", "margin": "lg", "contents": [
        {"type": "box", "layout": "horizontal", "contents": bars, "cornerRadius": "4px", "backgroundColor": "#F7FAFC", "paddingAll": "4px"}
    ]}

def _build_timer(seconds):
    """عرض الوقت المتبقي احترافي"""
    color = "#48BB78" if seconds > 20 else "#F6AD55" if seconds > 10 else "#F56565"
    progress = int((seconds / 30) * 100)
    return {"type": "box", "layout": "vertical", "margin": "md", "contents": [
        {"type": "box", "layout": "horizontal", "contents": [
            {"type": "text", "text": "⏱️", "size": "xs", "flex": 0, "margin": "none"},
            {"type": "text", "text": f"{seconds}s", "size": "xs", "weight": "bold", "color": color, "margin": "xs", "flex": 0}
        ]},
        {"type": "box", "layout": "vertical", "height": "4px", "backgroundColor": "#E2E8F0", "cornerRadius": "2px", "margin": "xs", "contents": [
            {"type": "box", "layout": "vertical", "width": f"{progress}%", "height": "4px", "backgroundColor": color, "cornerRadius": "2px"}
        ]}
    ]}

def build_enhanced_home(username, points, is_registered=True, theme=DEFAULT_THEME):
    themes = [["رمادي", "أسود", "أبيض"], ["وردي", "بنفسجي", "أزرق"], ["بني", "برتقالي", "أخضر"]]
    theme_rows = [{"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                   "contents": [_btn(t, t, "primary" if t == "رمادي" else "secondary") for t in row]} for row in themes]
    
    bubble = {"type": "bubble", "size": "mega",
        "header": {"type": "box", "layout": "vertical", "backgroundColor": "#F7FAFC", "paddingAll": "20px", "contents": [
            {"type": "text", "text": f"🎮 {BOT_NAME}", "size": "xxl", "weight": "bold", "align": "center", "color": "#4A5568"}
        ]},
        "body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "backgroundColor": "#FFFFFF", "contents": [
            {"type": "box", "layout": "vertical", "backgroundColor": "#EDF2F7", "cornerRadius": "10px", "paddingAll": "12px", "margin": "md", "contents": [
                {"type": "text", "text": f"{points} نقطة | {'✅' if is_registered else '⭕'} مسجل", "align": "center", "size": "md", "color": "#2D3748"}
            ]},
            {"type": "text", "text": "🎨 اختر الثيم:", "size": "lg", "weight": "bold", "margin": "xl", "color": "#2D3748"},
            *theme_rows,
            {"type": "separator", "margin": "xl"},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "lg", "contents": [
                _btn("✅ انضم" if not is_registered else "❌ انسحب", "انضم" if not is_registered else "انسحب", "primary", "#48BB78" if not is_registered else "#F56565"),
                _btn("🎮 الألعاب", "الألعاب")
            ]},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                _btn("⭐ نقاطي", "نقاطي", "secondary"), _btn("🏆 الصدارة", "الصدارة", "secondary")
            ]},
            {"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm", "contents": [
                _btn("فريقين", "فريقين", "secondary", "#A0AEC0"), _btn("❓ مساعدة", "مساعدة", "secondary")
            ]}
        ]},
        "footer": {"type": "box", "layout": "vertical", "backgroundColor": "#F7FAFC", "paddingAll": "10px", "contents": [
            {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "align": "center", "color": "#A0AEC0"}
        ]}
    }
    return FlexMessage("البداية", FlexContainer.from_dict(bubble))

def build_games_menu(theme=DEFAULT_THEME):
    games = [["لعبة", "ذكاء", "أسرع"], ["سلسلة", "خمن", "أغنية"], ["ضد", "تكوين", "ترتيب"], ["توافق", "رياضيا...", "لون"]]
    game_rows = [{"type": "box", "layout": "horizontal", "spacing": "sm", "margin": "sm",
                  "contents": [_btn(g, g, "primary", "#4299E1") for g in row]} for row in games]
    
    bubble = {"type": "bubble", "size": "mega",
        "header": {"type": "box", "layout": "vertical", "backgroundColor": "#EBF8FF", "paddingAll": "18px", "contents": [
            {"type": "text", "text": f"🎮 الألعاب المتاحة", "size": "xl", "weight": "bold", "align": "center", "color": "#2B6CB0"},
            {"type": "text", "text": f"عدد الألعاب: 12", "size": "sm", "align": "center", "color": "#4A5568", "margin": "sm"}
        ]},
        "body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "backgroundColor": "#FFFFFF", "contents": [
            *game_rows,
            {"type": "separator", "margin": "lg"},
            {"type": "box", "layout": "vertical", "backgroundColor": "#F7FAFC", "cornerRadius": "8px", "paddingAll": "12px", "margin": "lg", "contents": [
                {"type": "text", "text": "💡 أوامر اللعب:", "size": "sm", "weight": "bold", "color": "#2D3748"},
                *[{"type": "text", "text": t, "size": "xs", "color": "#718096", "margin": "xs", "wrap": True} 
                  for t in ["• اضغط على اسم اللعبة لبدء اللعب", "• اكتب 'لمح' للتلميح", "• اكتب 'جاوب' لكشف الإجابة", "• اكتب 'إيقاف' لإنهاء اللعبة"]]
            ]}
        ]},
        "footer": {"type": "box", "layout": "vertical", "paddingAll": "15px", "backgroundColor": "#F7FAFC", "contents": [
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                _btn("🏠 البداية", "بداية", "secondary"), _btn("⛔ إيقاف", "إيقاف", "secondary")
            ]},
            {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "align": "center", "color": "#A0AEC0", "margin": "md"}
        ]}
    }
    return FlexMessage("الألعاب المتاحة", FlexContainer.from_dict(bubble), quick_reply=build_games_quick_reply())

def build_question_with_hints(game_name, question, round_num, total_rounds, previous_qa=None, time_remaining=30, theme=DEFAULT_THEME):
    """للألعاب التي فيها لمح وجاوب"""
    contents = []
    if previous_qa:
        contents.append({"type": "box", "layout": "vertical", "backgroundColor": "#F0FFF4", "cornerRadius": "8px", "paddingAll": "10px", "margin": "md", "contents": [
            {"type": "text", "text": "📝 السؤال السابق:", "size": "xs", "weight": "bold", "color": "#2D3748"},
            {"type": "text", "text": previous_qa['question'], "size": "xs", "color": "#718096", "margin": "xs", "wrap": True},
            {"type": "text", "text": f"✅ الإجابة: {previous_qa['answer']}", "size": "xs", "color": "#48BB78", "margin": "xs", "wrap": True}
        ]})
    
    contents.extend([
        _build_progress_bar(round_num, total_rounds),
        _build_timer(time_remaining),
        {"type": "separator", "margin": "lg"},
        {"type": "text", "text": f"🧩 {question}", "size": "lg", "weight": "bold", "align": "center", "color": "#2D3748", "margin": "lg", "wrap": True},
        {"type": "box", "layout": "vertical", "backgroundColor": "#F7FAFC", "cornerRadius": "8px", "paddingAll": "12px", "margin": "lg", "contents": [
            {"type": "text", "text": "💡 اكتب 'لمح' للتلميح أو 'جاوب' للإجابة", "size": "xs", "color": "#718096", "align": "center", "wrap": True}
        ]}
    ])
    
    bubble = {"type": "bubble", "size": "mega",
        "header": {"type": "box", "layout": "vertical", "backgroundColor": "#FFF5F7", "paddingAll": "18px", "contents": [
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": f"🧠 {game_name}", "size": "xl", "weight": "bold", "color": "#2B6CB0", "flex": 3},
                {"type": "text", "text": f"جولة {round_num}/{total_rounds}", "size": "sm", "color": "#718096", "align": "end", "flex": 1}
            ]}
        ]},
        "body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "backgroundColor": "#FFFFFF", "contents": contents},
        "footer": {"type": "box", "layout": "vertical", "spacing": "sm", "paddingAll": "15px", "backgroundColor": "#F7FAFC", "contents": [
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                _btn("💡 لمح", "لمح", "secondary"), _btn("🔍 جاوب", "جاوب", "secondary")
            ]},
            _btn("⛔ إيقاف", "إيقاف", "primary", "#F56565")
        ]}
    }
    return FlexMessage(game_name, FlexContainer.from_dict(bubble))

def build_question_without_hints(game_name, question, round_num, total_rounds, previous_qa=None, time_remaining=30, theme=DEFAULT_THEME):
    """للألعاب سرعة ولعبة (بدون لمح وجاوب)"""
    contents = []
    if previous_qa:
        contents.append({"type": "box", "layout": "vertical", "backgroundColor": "#F0FFF4", "cornerRadius": "8px", "paddingAll": "10px", "margin": "md", "contents": [
            {"type": "text", "text": "📝 السؤال السابق:", "size": "xs", "weight": "bold", "color": "#2D3748"},
            {"type": "text", "text": previous_qa['question'], "size": "xs", "color": "#718096", "margin": "xs", "wrap": True},
            {"type": "text", "text": f"✅ الإجابة: {previous_qa['answer']}", "size": "xs", "color": "#48BB78", "margin": "xs", "wrap": True}
        ]})
    
    contents.extend([
        _build_progress_bar(round_num, total_rounds),
        _build_timer(time_remaining),
        {"type": "separator", "margin": "lg"},
        {"type": "text", "text": f"⚡ {question}", "size": "lg", "weight": "bold", "align": "center", "color": "#2D3748", "margin": "lg", "wrap": True},
        {"type": "box", "layout": "vertical", "backgroundColor": "#FFF5E6", "cornerRadius": "8px", "paddingAll": "12px", "margin": "lg", "contents": [
            {"type": "text", "text": "⚡ اكتب إجابتك مباشرة!", "size": "xs", "color": "#F6AD55", "align": "center", "weight": "bold"}
        ]}
    ])
    
    bubble = {"type": "bubble", "size": "mega",
        "header": {"type": "box", "layout": "vertical", "backgroundColor": "#FFF5F7", "paddingAll": "18px", "contents": [
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": f"⚡ {game_name}", "size": "xl", "weight": "bold", "color": "#F6AD55", "flex": 3},
                {"type": "text", "text": f"جولة {round_num}/{total_rounds}", "size": "sm", "color": "#718096", "align": "end", "flex": 1}
            ]}
        ]},
        "body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "backgroundColor": "#FFFFFF", "contents": contents},
        "footer": {"type": "box", "layout": "vertical", "paddingAll": "15px", "backgroundColor": "#F7FAFC", "contents": [
            _btn("⛔ إيقاف", "إيقاف", "primary", "#F56565")
        ]}
    }
    return FlexMessage(game_name, FlexContainer.from_dict(bubble))

def build_compatibility_game(user1_name, user2_name=None, compatibility_score=None, theme=DEFAULT_THEME):
    """لعبة التوافق - جولة واحدة فقط"""
    if compatibility_score is None:
        bubble = {"type": "bubble", "size": "mega",
            "header": {"type": "box", "layout": "vertical", "backgroundColor": "#FFF0F5", "paddingAll": "18px", "contents": [
                {"type": "text", "text": "💕 لعبة التوافق", "size": "xl", "weight": "bold", "align": "center", "color": "#EC4899"}
            ]},
            "body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "backgroundColor": "#FFFFFF", "contents": [
                {"type": "text", "text": "💭 اكتب اسم الشخص الثاني", "size": "lg", "align": "center", "color": "#2D3748", "margin": "lg", "wrap": True},
                {"type": "box", "layout": "vertical", "backgroundColor": "#FFF5F7", "cornerRadius": "8px", "paddingAll": "15px", "margin": "lg", "contents": [
                    {"type": "text", "text": "سيتم حساب نسبة التوافق بينكما", "size": "sm", "color": "#718096", "align": "center", "wrap": True}
                ]}
            ]},
            "footer": {"type": "box", "layout": "vertical", "paddingAll": "15px", "backgroundColor": "#F7FAFC", "contents": [_btn("⛔ إلغاء", "إيقاف", "secondary")]}
        }
    else:
        emoji = "🔥" if compatibility_score >= 80 else "💖" if compatibility_score >= 60 else "💛" if compatibility_score >= 40 else "💙"
        status = "توافق ممتاز!" if compatibility_score >= 80 else "توافق جيد" if compatibility_score >= 60 else "توافق متوسط" if compatibility_score >= 40 else "توافق ضعيف"
        
        bubble = {"type": "bubble", "size": "mega",
            "header": {"type": "box", "layout": "vertical", "backgroundColor": "#FFF0F5", "paddingAll": "25px", "contents": [
                {"type": "text", "text": emoji, "size": "xxl", "align": "center"},
                {"type": "text", "text": "💕 نتيجة التوافق", "size": "xl", "weight": "bold", "align": "center", "color": "#EC4899", "margin": "sm"}
            ]},
            "body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "backgroundColor": "#FFFFFF", "alignItems": "center", "contents": [
                {"type": "text", "text": f"{user1_name} ❤️ {user2_name}", "size": "md", "align": "center", "color": "#2D3748", "margin": "md", "wrap": True},
                {"type": "separator", "margin": "lg"},
                {"type": "text", "text": "نسبة التوافق", "size": "sm", "align": "center", "color": "#718096", "margin": "lg"},
                {"type": "text", "text": f"{compatibility_score}%", "size": "xxl", "weight": "bold", "align": "center", "color": "#EC4899", "margin": "sm"},
                {"type": "text", "text": status, "size": "md", "align": "center", "color": "#48BB78", "margin": "sm"},
                {"type": "separator", "margin": "lg"},
                {"type": "box", "layout": "vertical", "backgroundColor": "#FFF5F7", "cornerRadius": "8px", "paddingAll": "12px", "margin": "lg", "contents": [
                    {"type": "text", "text": "هذه النتيجة للتسلية فقط 😊", "size": "xs", "color": "#A0AEC0", "align": "center", "wrap": True}
                ]}
            ]},
            "footer": {"type": "box", "layout": "vertical", "spacing": "sm", "paddingAll": "15px", "backgroundColor": "#F7FAFC", "contents": [
                _btn("🔄 إعادة اللعبة", "توافق", "primary", "#EC4899"),
                {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                    _btn("🎮 الألعاب", "الألعاب", "secondary"), _btn("🏠 البداية", "بداية", "secondary")
                ]},
                {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "align": "center", "color": "#A0AEC0", "margin": "md"}
            ]}
        }
    return FlexMessage("لعبة التوافق", FlexContainer.from_dict(bubble))

def build_hint_display(game_name, question, hint, first_letter, letter_count, round_num, total_rounds, time_remaining=25, theme=DEFAULT_THEME):
    """عرض التلميح مع أول حرف وعدد الحروف"""
    bubble = {"type": "bubble", "size": "mega",
        "header": {"type": "box", "layout": "vertical", "backgroundColor": "#FFF5F7", "paddingAll": "18px", "contents": [
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": f"🧠 {game_name}", "size": "xl", "weight": "bold", "color": "#2B6CB0", "flex": 3},
                {"type": "text", "text": f"جولة {round_num}/{total_rounds}", "size": "sm", "color": "#718096", "align": "end", "flex": 1}
            ]}
        ]},
        "body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "backgroundColor": "#FFFFFF", "contents": [
            _build_progress_bar(round_num, total_rounds),
            _build_timer(time_remaining),
            {"type": "separator", "margin": "lg"},
            {"type": "text", "text": f"🧩 {question}", "size": "md", "align": "center", "color": "#2D3748", "margin": "lg", "wrap": True},
            {"type": "box", "layout": "vertical", "backgroundColor": "#FFF9E6", "cornerRadius": "10px", "paddingAll": "15px", "margin": "lg", "contents": [
                {"type": "text", "text": "💡 التلميح:", "size": "sm", "weight": "bold", "color": "#2D3748"},
                {"type": "text", "text": hint, "size": "sm", "color": "#718096", "margin": "sm", "wrap": True},
                {"type": "separator", "margin": "md"},
                {"type": "text", "text": f"الحرف الأول: {first_letter}", "size": "sm", "color": "#F6AD55", "margin": "sm", "weight": "bold"},
                {"type": "text", "text": f"عدد الحروف: {letter_count}", "size": "sm", "color": "#F6AD55", "margin": "xs", "weight": "bold"}
            ]}
        ]},
        "footer": {"type": "box", "layout": "vertical", "spacing": "sm", "paddingAll": "15px", "backgroundColor": "#F7FAFC", "contents": [
            _btn("🔍 جاوب", "جاوب", "secondary"),
            _btn("⛔ إيقاف", "إيقاف", "primary", "#F56565")
        ]}
    }
    return FlexMessage("تلميح", FlexContainer.from_dict(bubble))

def build_winner_announcement(username, game_name, points=10, total_points=90, theme=DEFAULT_THEME):
    bubble = {"type": "bubble", "size": "mega",
        "header": {"type": "box", "layout": "vertical", "backgroundColor": "#FFF5F7", "paddingAll": "25px", "contents": [
            {"type": "text", "text": "🎉", "size": "xxl", "align": "center"},
            {"type": "text", "text": "إتهانينا!", "size": "xxl", "weight": "bold", "align": "center", "color": "#2B6CB0", "margin": "sm"},
            {"type": "text", "text": f"أنهيت لعبة {game_name}", "size": "sm", "align": "center", "color": "#4A5568", "margin": "sm", "wrap": True}
        ]},
        "body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "backgroundColor": "#FFFFFF", "alignItems": "center", "contents": [
            {"type": "box", "layout": "vertical", "width": "80px", "height": "80px", "cornerRadius": "100px", "backgroundColor": "#E2E8F0", "justifyContent": "center", "alignItems": "center", "margin": "lg"},
            {"type": "text", "text": "النقاط المكتسبة", "size": "md", "align": "center", "color": "#718096", "margin": "xl"},
            {"type": "text", "text": f"+{points}", "size": "xxl", "weight": "bold", "align": "center", "color": "#48BB78", "margin": "sm"},
            {"type": "separator", "margin": "xl"},
            {"type": "text", "text": f"⭐ إجمالي النقاط                {total_points}", "size": "md", "color": "#2D3748", "margin": "lg"}
        ]},
        "footer": {"type": "box", "layout": "vertical", "spacing": "sm", "paddingAll": "15px", "backgroundColor": "#F7FAFC", "contents": [
            _btn("🔄 إعادة نفس اللعبة", game_name, "primary", "#4299E1"),
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                _btn("🎮 الألعاب", "الألعاب", "secondary"), _btn("🏠 البداية", "بداية", "secondary")
            ]},
            {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "align": "center", "color": "#A0AEC0", "margin": "md"}
        ]}
    }
    return FlexMessage("فوز", FlexContainer.from_dict(bubble))

def build_my_points(username, total_points=215, stats=None, theme=DEFAULT_THEME):
    bubble = {"type": "bubble", "size": "mega",
        "header": {"type": "box", "layout": "vertical", "backgroundColor": "#FFF5F7", "paddingAll": "18px", "contents": [
            {"type": "text", "text": "⭐ نقاطي", "size": "xl", "weight": "bold", "align": "center", "color": "#2B6CB0"}
        ]},
        "body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "backgroundColor": "#FFFFFF", "alignItems": "center", "contents": [
            {"type": "box", "layout": "vertical", "width": "80px", "height": "80px", "cornerRadius": "100px", "backgroundColor": "#E2E8F0", "justifyContent": "center", "alignItems": "center", "margin": "lg"},
            {"type": "separator", "margin": "xl"},
            {"type": "text", "text": "النقاط الكلية", "size": "md", "align": "center", "color": "#718096", "margin": "lg"},
            {"type": "text", "text": str(total_points), "size": "xxl", "weight": "bold", "align": "center", "color": "#2D3748", "margin": "sm"},
            {"type": "separator", "margin": "xl"},
            {"type": "text", "text": "المستوى الحالي", "size": "md", "align": "center", "color": "#718096", "margin": "lg"},
            {"type": "text", "text": "🔥 متقدم", "size": "xl", "weight": "bold", "align": "center", "color": "#F56565", "margin": "sm"},
            {"type": "separator", "margin": "xl"},
            {"type": "box", "layout": "vertical", "backgroundColor": "#FFF5F5", "cornerRadius": "8px", "paddingAll": "12px", "margin": "lg", "contents": [
                {"type": "text", "text": "⚠️ سيتم حذف بياناتك بعد 7 أيام من عدم النشاط", "size": "xs", "color": "#E53E3E", "wrap": True, "align": "center"}
            ]}
        ]},
        "footer": {"type": "box", "layout": "vertical", "paddingAll": "15px", "backgroundColor": "#F7FAFC", "contents": [
            {"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
                _btn("🏠 البداية", "بداية", "secondary"), _btn("🎮 الألعاب", "الألعاب", "primary", "#4299E1")
            ]},
            {"type": "text", "text": BOT_RIGHTS, "size": "xxs", "align": "center", "color": "#A0AEC0", "margin": "md"}
        ]}
    }
    return FlexMessage("نقاطي", FlexContainer.from_dict(bubble))

def
build_leaderboard(top_users=None, user_rank=7, user_points=215, theme=DEFAULT_THEME):
bubble = {"type": "bubble", "size": "mega",
"header": {"type": "box", "layout": "vertical", "backgroundColor": "#FFF9E6", "paddingAll": "18px", "contents": [
{"type": "text", "text": "🏆 لوحة الصدارة", "size": "xl", "weight": "bold", "align": "center", "color": "#2B6CB0"}
]},
"body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "backgroundColor": "#FFFFFF", "contents": [
{"type": "box", "layout": "horizontal", "backgroundColor": "#E6FFFA", "cornerRadius": "12px", "paddingAll": "15px", "margin": "md", "contents": [
{"type": "box", "layout": "vertical", "width": "50px", "contents": [
{"type": "text", "text": "🥇", "size": "xl", "align": "center"},
{"type": "text", "text": str(user_rank), "size": "sm", "align": "center", "color": "#718096"}
]},
{"type": "box", "layout": "vertical", "flex": 1, "justifyContent": "center", "contents": [
{"type": "text", "text": str(user_points), "size": "xxl", "weight": "bold", "align": "end", "color": "#2D3748"}
]}
]}
]},
"footer": {"type": "box", "layout": "vertical", "paddingAll": "15px", "backgroundColor": "#F7FAFC", "contents": [
{"type": "box", "layout": "horizontal", "spacing": "sm", "contents": [
_btn("🏠 البداية", "بداية", "secondary"), _btn("⭐ نقاطي", "نقاطي", "primary", "#F6AD55")
]},
{"type": "text", "text": BOT_RIGHTS, "size": "xxs", "align": "center", "color": "#A0AEC0", "margin": "md"}
]}
}
return FlexMessage("لوحة الصدارة", FlexContainer.from_dict(bubble))
def build_help_window(theme=DEFAULT_THEME):
bubble = {"type": "bubble", "size": "mega",
"header": {"type": "box", "layout": "vertical", "backgroundColor": "#EBF8FF", "paddingAll": "18px", "contents": [
{"type": "text", "text": "❓ المساعدة", "size": "xl", "weight": "bold", "align": "center", "color": "#2B6CB0"}
]},
"body": {"type": "box", "layout": "vertical", "paddingAll": "20px", "backgroundColor": "#FFFFFF", "contents": [
{"type": "text", "text": "🎮 أنواع الألعاب:", "weight": "bold", "margin": "md", "color": "#2D3748"},
*[{"type": "text", "text": t, "size": "sm", "color": "#718096", "margin": "xs" if i > 0 else "sm", "wrap": True}
for i, t in enumerate(["• ألعاب مع لمح وجاوب (9 ألعاب)", "• ألعاب سريعة بدون لمح (2 لعبة)", "• لعبة التوافق (جولة واحدة)"])],
{"type": "separator", "margin": "lg"},
{"type": "text", "text": "⏱️ نظام التوقيت:", "weight": "bold", "margin": "lg", "color": "#2D3748"},
*[{"type": "text", "text": t, "size": "sm", "color": "#718096", "margin": "xs" if i > 0 else "sm", "wrap": True}
for i, t in enumerate(["• كل سؤال له 30 ثانية", "• 5 جولات لكل لعبة (عدا التوافق)"])],
{"type": "separator", "margin": "lg"},
{"type": "text", "text": "💰 نظام النقاط:", "weight": "bold", "margin": "lg", "color": "#2D3748"},
*[{"type": "text", "text": t, "size": "sm", "color": "#718096", "margin": "xs" if i > 0 else "sm", "wrap": True}
for i, t in enumerate(["• +10 نقاط للإجابة الصحيحة", "• +5 نقاط بعد استخدام لمحة"])]
]},
"footer": {"type": "box", "layout": "vertical", "spacing": "sm", "paddingAll": "15px", "backgroundColor": "#F7FAFC", "contents": [_btn("🏠 البداية", "بداية")]}
}
return FlexMessage("المساعدة", FlexContainer.from_dict(bubble))
def has_hints(game_name):
"""تحقق إذا كانت اللعبة تدعم لمح وجاوب"""
return game_name in GAMES_WITH_HINTS
def is_special_game(game_name):
"""تحقق إذا كانت لعبة التوافق"""
return game_name == SPECIAL_GAME
def get_total_rounds(game_name):
"""عدد الجولات حسب اللعبة"""
return 1 if is_special_game(game_name) else 5
