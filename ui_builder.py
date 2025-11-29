"""
Bot Mesh - UI Builder v11.0 FIXED
Created by: Abeer Aldosari © 2025
✅ إصلاح جميع أخطاء LINE API
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

# البداية
def build_enhanced_home(username, points, is_registered=True, theme=DEFAULT_THEME):
    c = _c(theme)
    status = "✅ مسجل" if is_registered else "⚪ غير مسجل"
    status_color = c["success"] if is_registered else c["text2"]
    
    theme_rows = [{"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_btn(t,f"ثيم {t}","primary" if t==theme else "secondary",c["primary"] if t==theme else None) for t in list(THEMES.keys())[i:i+3]]} for i in range(0,len(THEMES),3)]
    
    # زر الانضمام/الانسحاب
    join_btn = _btn("📝 انضم" if not is_registered else "❌ انسحب", "انضم" if not is_registered else "انسحب","primary",c["primary"])
    games_btn = _btn("🎮 الألعاب","ألعاب","secondary")
    
    bubble = {
        "type":"bubble","size":"mega",
        "body":{
            "type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],
            "contents":[
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":f"🎮 {BOT_NAME}","weight":"bold","size":"xxl","color":c["primary"],"align":"center"},
                    {"type":"text","text":"بوت الألعاب الترفيهية الذكي","size":"sm","color":c["text2"],"align":"center","margin":"xs"}
                ],"spacing":"xs"},
                {"type":"separator","margin":"lg"},
                {"type":"box","layout":"vertical","backgroundColor":c["card"],"cornerRadius":"20px","paddingAll":"20px","margin":"lg","contents":[
                    {"type":"text","text":f"👤 {username}","size":"lg","color":c["text"],"weight":"bold"},
                    {"type":"box","layout":"horizontal","margin":"sm","contents":[
                        {"type":"text","text":status,"size":"sm","color":status_color,"flex":0},
                        {"type":"text","text":f"⭐ {points} نقطة","size":"sm","color":c["primary"],"align":"end"}
                    ]}
                ]},
                {"type":"text","text":"🎨 اختر ثيمك المفضل:","size":"md","weight":"bold","color":c["text"],"margin":"xl"},
                *theme_rows,
                {"type":"separator","margin":"xl"},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[join_btn, games_btn]},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[
                    _btn("⭐ نقاطي","نقاطي","secondary"),
                    _btn("🏆 الصدارة","صدارة","secondary")
                ]},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[
                    _btn("❓ مساعدة","مساعدة","secondary"),
                    _btn("👥 فريقين","فريقين","secondary") if is_registered else _btn("🎨 ثيمات","ثيمات","secondary")
                ]},
                {"type":"separator","margin":"lg"},
                {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text2"],"align":"center"}
            ]
        }
    }
    return attach_quick_reply(_flex("البداية", bubble))

# قائمة الألعاب
def build_games_menu(theme=DEFAULT_THEME):
    c = _c(theme)
    game_rows = [{"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_btn(f"{ic} {nm}",nm,"primary",c["primary"]) for _,nm,ic in GAME_LIST[i:i+3]]} for i in range(0,len(GAME_LIST),3)]
    
    bubble = {
        "type":"bubble","size":"mega",
        "body":{
            "type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],
            "contents":[
                {"type":"text","text":"🎮 الألعاب المتاحة","weight":"bold","size":"xl","color":c["primary"],"align":"center"},
                {"type":"text","text":f"اختر من {len(GAME_LIST)} لعبة مختلفة","size":"sm","color":c["text2"],"align":"center","margin":"xs"},
                {"type":"separator","margin":"lg"},
                *game_rows,
                {"type":"separator","margin":"lg"},
                {"type":"box","layout":"vertical","backgroundColor":c["card"],"cornerRadius":"15px","paddingAll":"15px","margin":"md","contents":[
                    {"type":"text","text":"💡 الأوامر أثناء اللعب:","size":"sm","color":c["text"],"weight":"bold"},
                    {"type":"text","text":"• لمح - للحصول على تلميح\n• جاوب - لكشف الإجابة\n• إيقاف - لإنهاء اللعبة","size":"xs","color":c["text2"],"wrap":True,"margin":"xs"}
                ]},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[
                    _btn("🏠 البداية","بداية","secondary"),
                    _btn("⛔ إيقاف","إيقاف","secondary")
                ]},
                {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text2"],"align":"center","margin":"sm"}
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
            "type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],
            "contents":[
                {"type":"text","text":"⭐ نقاطي","weight":"bold","size":"xl","color":c["primary"],"align":"center"},
                {"type":"separator","margin":"lg"},
                {"type":"text","text":f"👤 {username}","size":"lg","color":c["text"],"weight":"bold","align":"center","margin":"lg"},
                {"type":"box","layout":"vertical","backgroundColor":c["card"],"cornerRadius":"20px","paddingAll":"25px","margin":"lg","contents":[
                    {"type":"text","text":"النقاط الكلية","size":"sm","color":c["text2"],"align":"center"},
                    {"type":"text","text":str(points),"size":"xxl","weight":"bold","color":c["primary"],"align":"center","margin":"sm"}
                ]},
                {"type":"box","layout":"vertical","backgroundColor":c["card"],"cornerRadius":"15px","paddingAll":"15px","margin":"md","contents":[
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
            "type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],
            "contents":[
                {"type":"text","text":"🏆 لوحة الصدارة","weight":"bold","size":"xl","color":c["primary"],"align":"center"},
                {"type":"separator","margin":"lg"},
                {"type":"box","layout":"vertical","backgroundColor":c["card"],"cornerRadius":"20px","paddingAll":"20px","margin":"lg","spacing":"sm","contents":items},
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
    bubble = {"type":"bubble","size":"mega","header":{"type":"box","layout":"vertical","backgroundColor":c["success"],"paddingAll":"25px","contents":[
        {"type":"text","text":"🎉","size":"xxl","align":"center"},
        {"type":"text","text":"مبروك!","size":"xxl","weight":"bold","align":"center","color":"#FFFFFF","margin":"sm"}
    ]},"body":{"type":"box","layout":"vertical","paddingAll":"20px","contents":[
        {"type":"text","text":f"أنهيت لعبة {game_name}","size":"lg","color":c["text"],"align":"center","wrap":True},
        {"type":"box","layout":"vertical","backgroundColor":c["card"],"cornerRadius":"20px","paddingAll":"20px","margin":"lg","contents":[
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
    bubble = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[
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
    return attach_quick_reply(_flex("ثيم", {"type":"bubble","body":{"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[
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
        {"type":"box","layout":"vertical","backgroundColor":c["card"],"cornerRadius":"15px","paddingAll":"20px","margin":"lg","contents":[
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
