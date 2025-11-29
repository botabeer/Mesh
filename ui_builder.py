"""
Bot Mesh - UI Builder v11.1 FINAL FIX
Created by: Abeer Aldosari © 2025
✅ إزالة backgroundColor من جميع الـ Flex Messages
✅ متوافق 100% مع LINE API
"""

from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from constants import GAME_LIST, DEFAULT_THEME, THEMES, BOT_NAME, BOT_RIGHTS

# Quick Reply
def build_games_quick_reply():
    return QuickReply(items=[QuickReplyItem(action=MessageAction(label=f"{ic} {nm}", text=nm)) for _, nm, ic in GAME_LIST])

def attach_quick_reply(msg):
    if msg and hasattr(msg, 'quick_reply'): msg.quick_reply = build_games_quick_reply()
    return msg

# Helpers
def _c(theme=None): return THEMES.get(theme or DEFAULT_THEME, THEMES[DEFAULT_THEME])
def _btn(lbl, txt, style="primary", color=None): 
    return {"type":"button","action":{"type":"message","label":lbl,"text":txt},"style":style,"height":"sm","color":color} if color else {"type":"button","action":{"type":"message","label":lbl,"text":txt},"style":style,"height":"sm"}
def _flex(alt, bubble): return FlexMessage(alt_text=alt, contents=FlexContainer.from_dict(bubble))

# البداية - متطابقة مع الصور
def build_enhanced_home(username, points, is_registered=True, theme=DEFAULT_THEME):
    c = _c(theme)
    status_icon = "✅" if is_registered else "⚪"
    status_text = "مسجل" if is_registered else "غير مسجل"
    
    # أزرار الثيمات 3×3
    theme_list = list(THEMES.keys())
    theme_rows = []
    for i in range(0, len(theme_list), 3):
        row_themes = theme_list[i:i+3]
        theme_rows.append({
            "type":"box","layout":"horizontal","spacing":"sm","margin":"sm",
            "contents":[_btn(t,f"ثيم {t}","primary" if t==theme else "secondary") for t in row_themes]
        })
    
    # زر الانضمام/الانسحاب
    join_icon = "✅" if is_registered else "❌"
    join_text = "انسحب" if is_registered else "انضم"
    join_label = f"{join_icon} {join_text}"
    
    bubble = {
        "type":"bubble","size":"mega",
        "body":{
            "type":"box","layout":"vertical","paddingAll":"20px",
            "contents":[
                # العنوان
                {"type":"text","text":f"🎮 {BOT_NAME}","weight":"bold","size":"xxl","color":c["text"],"align":"center"},
                {"type":"separator","margin":"lg"},
                
                # حالة المستخدم
                {"type":"box","layout":"horizontal","margin":"lg","contents":[
                    {"type":"text","text":f"{status_icon} | نقطة","size":"md","color":c["text"],"align":"start","flex":2},
                    {"type":"text","text":status_text,"size":"md","color":c["text2"],"align":"end","flex":1}
                ]},
                {"type":"text","text":str(points),"size":"xxl","color":c["text"],"align":"start","margin":"none"},
                
                # قسم الثيمات
                {"type":"text","text":"🎨 :اختر الثيم","size":"md","weight":"bold","color":c["text"],"margin":"xl","align":"start"},
                *theme_rows,
                
                # الأزرار الرئيسية
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"xl","contents":[
                    _btn(join_label,join_text,"primary" if is_registered else "secondary"),
                    _btn("🎮 الألعاب","ألعاب","secondary")
                ]},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[
                    _btn("⭐ نقاطي","نقاطي","secondary"),
                    _btn("🏆 الصدارة","صدارة","secondary")
                ]},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[
                    _btn("👥 فريقين","فريقين","secondary"),
                    _btn("❓ مساعدة","مساعدة","secondary")
                ]},
                
                # الحقوق
                {"type":"separator","margin":"lg"},
                {"type":"text","text":"© 2025 Abeer Aldosari - All Rights Reserved","size":"xxs","color":c["text2"],"align":"center","margin":"md"}
            ]
        }
    }
    return attach_quick_reply(_flex("البداية", bubble))

# قائمة الألعاب - متطابقة مع الصورة 3
def build_games_menu(theme=DEFAULT_THEME):
    c = _c(theme)
    
    # ترتيب الألعاب حسب الصورة: 12 لعبة في 4 صفوف × 3 أعمدة
    games_order = [
        ("fast_typing","كتابة سريعة","⚡"),
        ("iq","ذكاء","🧠"),
        ("guess","تخمين","🔮"),
        ("song","أغنية","🎵"),
        ("human_animal_plant","إنسان حيوان نبات","🌿"),
        ("chain_words","سلسلة كلمات","🔗"),
        ("opposite","أضداد","↔️"),
        ("letters_words","تكوين","📝"),
        ("scramble_word","كلمة مبعثرة","🔤"),
        ("compatibility","توافق","💕"),
        ("math","رياضيات","🔢"),
        ("word_color","لون","🎨")
    ]
    
    # نقرأ الأسماء من الترتيب الجديد
    display_names = [
        "أسرع", "ذكاء", "لعبة",
        "أغنية", "خمن", "سلسلة",
        "ترتيب", "تكوين", "ضد",
        "لون", "رياضيا...", "توافق"
    ]
    
    # إنشاء الأزرار 3×4
    game_rows = []
    for i in range(0, 12, 3):
        row = {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[]}
        for j in range(3):
            idx = i + j
            if idx < len(display_names):
                # استخدام الاسم الفعلي من GAME_LIST للأمر
                actual_name = [name for _, name, _ in GAME_LIST][idx]
                row["contents"].append(_btn(display_names[idx], actual_name, "primary"))
        game_rows.append(row)
    
    bubble = {
        "type":"bubble","size":"mega",
        "body":{
            "type":"box","layout":"vertical","paddingAll":"20px",
            "contents":[
                # العنوان
                {"type":"text","text":"🎮 الألعاب المتاحة","weight":"bold","size":"xl","color":"#3B9DD9","align":"center"},
                {"type":"text","text":"عدد الألعاب: 12","size":"sm","color":c["text2"],"align":"center","margin":"xs"},
                {"type":"separator","margin":"lg"},
                
                # الألعاب
                *game_rows,
                
                # قسم الأوامر
                {"type":"box","layout":"vertical","paddingAll":"15px","margin":"lg","contents":[
                    {"type":"text","text":"💡 :أوامر اللعب","size":"sm","color":c["text"],"weight":"bold","align":"start"},
                    {"type":"text","text":"اضغط على اسم اللعبة لبدء اللعب •","size":"xs","color":c["text2"],"wrap":True,"margin":"sm","align":"start"},
                    {"type":"text","text":"اكتب 'لمح' للتلميح •","size":"xs","color":c["text2"],"wrap":True,"margin":"xs","align":"start"},
                    {"type":"text","text":"اكتب 'جاوب' لكشف الإجابة •","size":"xs","color":c["text2"],"wrap":True,"margin":"xs","align":"start"},
                    {"type":"text","text":"اكتب 'إيقاف' لإنهاء اللعبة •","size":"xs","color":c["text2"],"wrap":True,"margin":"xs","align":"start"}
                ]},
                
                # الأزرار السفلية
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[
                    _btn("🏠 البداية","بداية","secondary"),
                    _btn("⛔ إيقاف","إيقاف","secondary")
                ]},
                
                # الحقوق
                {"type":"text","text":"© 2025 Abeer Aldosari - All Rights Reserved","size":"xxs","color":c["text2"],"align":"center","margin":"sm"}
            ]
        }
    }
    return attach_quick_reply(_flex("الألعاب", bubble))

# نقاطي
def build_my_points(username, points, stats=None, theme=DEFAULT_THEME):
    c = _c(theme)
    level = "🌱 مبتدئ" if points<50 else "⭐ متوسط" if points<150 else "🔥 متقدم" if points<300 else "👑 محترف"
    level_color = "#48BB78" if points<50 else "#667EEA" if points<150 else "#DD6B20" if points<300 else "#D53F8C"
    
    bubble = {
        "type":"bubble","size":"mega",
        "body":{
            "type":"box","layout":"vertical","paddingAll":"20px",
            "contents":[
                {"type":"text","text":"⭐ نقاطي","weight":"bold","size":"xl","color":c["primary"],"align":"center"},
                {"type":"separator","margin":"lg"},
                {"type":"text","text":f"👤 {username}","size":"lg","color":c["text"],"weight":"bold","align":"center","margin":"lg"},
                {"type":"box","layout":"vertical","cornerRadius":"20px","paddingAll":"25px","margin":"lg","contents":[
                    {"type":"text","text":"النقاط الكلية","size":"sm","color":c["text2"],"align":"center"},
                    {"type":"text","text":str(points),"size":"xxl","weight":"bold","color":c["primary"],"align":"center","margin":"sm"}
                ]},
                {"type":"box","layout":"vertical","cornerRadius":"15px","paddingAll":"15px","margin":"md","contents":[
                    {"type":"text","text":"المستوى الحالي","size":"sm","color":c["text2"],"align":"center"},
                    {"type":"text","text":level,"size":"lg","weight":"bold","color":level_color,"align":"center","margin":"sm"}
                ]},
                {"type":"separator","margin":"lg"},
                {"type":"text","text":"⚠️ سيتم حذف بياناتك بعد 7 أيام من عدم النشاط","size":"xs","color":"#FF5555","wrap":True,"align":"center"},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[
                    _btn("🏠 البداية","بداية","secondary"),
                    _btn("🎮 الألعاب","ألعاب","secondary")
                ]},
                {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text2"],"align":"center","margin":"sm"}
            ]
        }
    }
    return attach_quick_reply(_flex("نقاطي", bubble))

# لوحة الصدارة
def build_leaderboard(top_users, theme=DEFAULT_THEME):
    c = _c(theme)
    medals = ["🥇","🥈","🥉"]
    items = [{"type":"box","layout":"horizontal","spacing":"md","paddingAll":"sm","contents":[
        {"type":"text","text":medals[i-1] if i<=3 else f"{i}.","size":"lg","flex":0,"color":c["primary"] if i<=3 else c["text"]},
        {"type":"text","text":nm,"size":"sm","color":c["text"],"flex":3},
        {"type":"text","text":str(pts),"size":"sm","color":c["primary"],"align":"end","flex":1}
    ]} for i,(nm,pts) in enumerate(top_users[:10],1)] or [{"type":"text","text":"لا يوجد لاعبين مسجلين بعد","size":"sm","color":c["text2"],"align":"center"}]
    
    bubble = {
        "type":"bubble","size":"mega",
        "body":{
            "type":"box","layout":"vertical","paddingAll":"20px",
            "contents":[
                {"type":"text","text":"🏆 لوحة الصدارة","weight":"bold","size":"xl","color":c["primary"],"align":"center"},
                {"type":"separator","margin":"lg"},
                {"type":"box","layout":"vertical","cornerRadius":"20px","paddingAll":"20px","margin":"lg","spacing":"sm","contents":items},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[
                    _btn("🏠 البداية","بداية","secondary"),
                    _btn("⭐ نقاطي","نقاطي","secondary")
                ]},
                {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text2"],"align":"center","margin":"sm"}
            ]
        }
    }
    return attach_quick_reply(_flex("الصدارة", bubble))

# نوافذ مساعدة
def build_registration_required(theme=DEFAULT_THEME):
    c = _c(theme)
    bubble = {"type":"bubble","body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":"⚠️ يجب التسجيل أولاً","weight":"bold","size":"lg","color":c["primary"],"align":"center"},
        {"type":"separator","margin":"lg"},
        {"type":"text","text":"اضغط 'انضم' للتسجيل والبدء باللعب","size":"sm","color":c["text2"],"align":"center","wrap":True,"margin":"md"}
    ]},"footer":{"type":"box","layout":"vertical","paddingAll":"15px","contents":[
        {"type":"box","layout":"horizontal","spacing":"sm","contents":[_btn("📝 انضم","انضم","primary"),_btn("🏠 البداية","بداية","secondary")]}
    ]}}
    return attach_quick_reply(_flex("تسجيل مطلوب", bubble))

def build_winner_announcement(username, game_name, round_points, total_points, theme=DEFAULT_THEME):
    c = _c(theme)
    bubble = {"type":"bubble","size":"mega","header":{"type":"box","layout":"vertical","paddingAll":"25px","contents":[
        {"type":"text","text":"🎉","size":"xxl","align":"center"},
        {"type":"text","text":"مبروك!","size":"xxl","weight":"bold","align":"center","color":"#FFFFFF","margin":"sm"}
    ]},"body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":f"أنهيت لعبة {game_name}","size":"lg","color":c["text"],"align":"center","wrap":True},
        {"type":"box","layout":"vertical","cornerRadius":"20px","paddingAll":"20px","margin":"lg","contents":[
            {"type":"text","text":"النقاط المكتسبة","size":"sm","color":c["text2"],"align":"center"},
            {"type":"text","text":f"+{round_points}","size":"xxl","weight":"bold","color":c["success"],"align":"center","margin":"sm"}
        ]},
        {"type":"text","text":f"⭐ إجمالي: {total_points}","size":"md","color":c["text"],"align":"center","margin":"md"}
    ]},"footer":{"type":"box","layout":"vertical","paddingAll":"15px","contents":[
        _btn(f"🔄 {game_name}",game_name,"primary"),
        {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_btn("🎮 الألعاب","ألعاب","secondary"),_btn("🏠 البداية","بداية","secondary")]}
    ]}}
    return attach_quick_reply(_flex("فوز", bubble))

def build_help_window(theme=DEFAULT_THEME):
    c = _c(theme)
    bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":"❓ المساعدة","weight":"bold","size":"xl","color":c["primary"],"align":"center"},
        {"type":"separator","margin":"lg"},
        {"type":"text","text":"🎮 الأوامر:","weight":"bold","color":c["text"],"margin":"md"},
        {"type":"text","text":"• بداية\n• ألعاب\n• نقاطي\n• صدارة\n• انضم","size":"sm","color":c["text2"],"wrap":True,"margin":"sm"},
        {"type":"separator","margin":"lg"},
        {"type":"text","text":"🎯 أثناء اللعب:","weight":"bold","color":c["text"],"margin":"md"},
        {"type":"text","text":"• لمح\n• جاوب\n• إيقاف","size":"sm","color":c["text2"],"wrap":True,"margin":"sm"},
        _btn("🏠 البداية","بداية","primary")
    ]}}
    return attach_quick_reply(_flex("المساعدة", bubble))

def build_theme_selector(theme=DEFAULT_THEME):
    c = _c(theme)
    rows = [{"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_btn(t,f"ثيم {t}") for t in list(THEMES.keys())[i:i+3]]} for i in range(0,len(THEMES),3)]
    bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":"🎨 اختر الثيم","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
        {"type":"separator","margin":"lg"},*rows,_btn("🏠 البداية","بداية","secondary")
    ]}}
    return attach_quick_reply(_flex("الثيمات", bubble))

def build_multiplayer_help_window(theme=DEFAULT_THEME):
    c = _c(theme)
    bubble = {"type":"bubble","body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":"👥 وضع الفريقين","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
        {"type":"separator","margin":"lg"},
        {"type":"text","text":"1. اكتب 'انضم'\n2. اختر اللعبة\n3. تقسيم تلقائي","size":"sm","color":c["text2"],"wrap":True,"margin":"md"},
        _btn("✅ انضم","انضم","primary")
    ]}}
    return attach_quick_reply(_flex("فريقين", bubble))

# نوافذ صغيرة
def build_join_confirmation(username, theme=DEFAULT_THEME):
    c = _c(theme)
    return attach_quick_reply(_flex("انضمام", {"type":"bubble","body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":"✅ انضممت","size":"lg","weight":"bold","color":c["success"],"align":"center"},
        {"type":"text","text":"انتظر اللعبة","size":"sm","color":c["text2"],"align":"center","margin":"md"}
    ]}}))

def build_registration_success(username, theme=DEFAULT_THEME):
    c = _c(theme)
    return attach_quick_reply(_flex("تسجيل", {"type":"bubble","body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":"✅ تم التسجيل","size":"lg","weight":"bold","color":c["success"],"align":"center"},
        {"type":"text","text":f"مرحباً {username}","size":"md","color":c["text"],"align":"center","margin":"md"},
        _btn("🎮 ابدأ","ألعاب","primary")
    ]}}))

def build_theme_change_success(theme_name, theme=DEFAULT_THEME):
    c = _c(theme_name)
    return attach_quick_reply(_flex("ثيم", {"type":"bubble","body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":"✅ تم تغيير الثيم","size":"lg","weight":"bold","color":c["primary"],"align":"center"},
        {"type":"text","text":f"الثيم: {theme_name}","size":"sm","color":c["text"],"align":"center","margin":"md"},
        _btn("🏠 البداية","بداية","primary")
    ]}}))

def build_error_message(error_text, theme=DEFAULT_THEME):
    c = _c(theme)
    return attach_quick_reply(_flex("خطأ", {"type":"bubble","body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":error_text,"size":"md","color":c["error"],"align":"center","wrap":True},
        _btn("🏠 البداية","بداية","secondary")
    ]}}))

def build_game_stopped(game_name, theme=DEFAULT_THEME):
    c = _c(theme)
    return attach_quick_reply(_flex("إيقاف", {"type":"bubble","body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":"⛔ تم إيقاف اللعبة","size":"lg","weight":"bold","color":c["error"],"align":"center"},
        {"type":"text","text":f"لعبة {game_name}","size":"sm","color":c["text2"],"align":"center","margin":"sm"},
        {"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[_btn("🎮 الألعاب","ألعاب","primary"),_btn("🏠 البداية","بداية","secondary")]}
    ]}}))

def build_answer_feedback(message, theme=DEFAULT_THEME):
    c = _c(theme)
    return attach_quick_reply(_flex("إجابة", {"type":"bubble","body":{"type":"box","layout":"vertical","paddingAll":"15px","contents":[
        {"type":"text","text":message,"size":"md","color":c["text"],"align":"center","wrap":True}
    ]}}))

def build_team_game_end(team_points, theme=DEFAULT_THEME):
    c = _c(theme)
    t1 = team_points.get("team1",0)
    t2 = team_points.get("team2",0)
    winner = "الفريق الأول 🥇" if t1>t2 else "الفريق الثاني 🥈" if t2>t1 else "تعادل ⚖️"
    return attach_quick_reply(_flex("نتيجة", {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":"🏆 انتهت اللعبة!","size":"xl","weight":"bold","color":c["primary"],"align":"center"},
        {"type":"separator","margin":"lg"},
        {"type":"box","layout":"vertical","cornerRadius":"15px","paddingAll":"20px","margin":"lg","contents":[
            {"type":"box","layout":"horizontal","margin":"md","contents":[
                {"type":"text","text":f"الفريق 1\n{t1}","size":"lg","color":c["primary"],"align":"center","flex":1},
                {"type":"text","text":"VS","size":"sm","color":c["text2"],"align":"center","flex":0},
                {"type":"text","text":f"الفريق 2\n{t2}","size":"lg","color":c["primary"],"align":"center","flex":1}
            ]},
            {"type":"text","text":f"الفائز: {winner}","size":"md","weight":"bold","color":c["success"],"align":"center","margin":"md"}
        ]},
        {"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[_btn("🎮 الألعاب","ألعاب","primary"),_btn("🏠 البداية","بداية","secondary")]}
    ]}}))

__all__ = [
    'build_enhanced_home','build_games_menu','build_my_points','build_leaderboard',
    'build_help_window','build_registration_required','build_winner_announcement',
    'build_theme_selector','build_multiplayer_help_window','attach_quick_reply','build_games_quick_reply',
    'build_join_confirmation','build_registration_success','build_theme_change_success',
    'build_error_message','build_game_stopped','build_answer_feedback','build_team_game_end'
]
