"""Bot Mesh - UI Builder v19.0 COMPACT | © 2025 Abeer Aldosari"""
from linebot.v3.messaging import FlexMessage, FlexContainer, QuickReply, QuickReplyItem, MessageAction
from constants import GAME_LIST, DEFAULT_THEME, THEMES, BOT_NAME, BOT_RIGHTS, FIXED_GAME_QR

def _c(t=None): return THEMES.get(t or DEFAULT_THEME, THEMES[DEFAULT_THEME])
def _glass(c, t, r="15px", p="15px"): return {"type":"box","layout":"vertical","contents":c,"cornerRadius":r,"paddingAll":p,"borderWidth":"1px","borderColor":_c(t)["border"]}
def _btn(l, tx, s="primary", t=None): return {"type":"button","action":{"type":"message","label":l,"text":tx},"style":s,"height":"sm","color":_c(t)["primary"] if s=="primary" else _c(t)["secondary"]}
def _flex(a, b): return FlexMessage(alt_text=a, contents=FlexContainer.from_dict(b))
def build_games_quick_reply(): return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i["label"], text=i["text"])) for i in FIXED_GAME_QR])
def attach_quick_reply(m): 
    if m and hasattr(m, 'quick_reply'): m.quick_reply = build_games_quick_reply()
    return m

def build_enhanced_home(username, points, is_registered=True, theme=DEFAULT_THEME):
    c = _c(theme)
    status = "مسجل" if is_registered else "غير مسجل"
    themes = list(THEMES.keys())
    rows = [{"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_btn(t,f"ثيم {t}","primary" if t==theme else "secondary",theme) for t in themes[i:i+3]]} for i in range(0,len(themes),3)]
    join = "انسحب" if is_registered else "انضم"
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[
        {"type":"text","text":f" {BOT_NAME}","weight":"bold","size":"xxl","color":c["primary"],"align":"center"},
        {"type":"separator","margin":"lg","color":c["border"]},
        _glass([{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"النقاط","size":"md","color":c["text"],"flex":2,"weight":"bold"},{"type":"text","text":status,"size":"md","color":c["text2"],"align":"end","flex":1}]},{"type":"text","text":str(points),"size":"xxl","color":c["primary"],"margin":"sm","weight":"bold"}],theme,"15px","15px"),
        {"type":"text","text":"اختر الثيم","size":"md","weight":"bold","color":c["text"],"margin":"xl"},
        *rows,
        {"type":"box","layout":"horizontal","spacing":"sm","margin":"xl","contents":[_btn(f"{join}",join,"primary" if is_registered else "secondary",theme),_btn("الألعاب","ألعاب","secondary",theme)]},
        {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_btn("نقاطي","نقاطي","secondary",theme),_btn("الصدارة","صدارة","secondary",theme)]},
        {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_btn("فريقين","فريقين","secondary",theme),_btn("مساعدة","مساعدة","secondary",theme)]},
        {"type":"separator","margin":"lg","color":c["border"]},
        {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center","margin":"md"}
    ]}
    return attach_quick_reply(_flex("البداية",{"type":"bubble","size":"mega","body":body}))

def build_games_menu(theme=DEFAULT_THEME):
    c = _c(theme)
    order = ["أسرع","ذكاء","لعبة","أغنيه","خمن","سلسلة","ترتيب","تكوين","ضد","لون","رياضيات","توافق"]
    rows = [{"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_btn(order[i+j],order[i+j],"primary",theme) for j in range(3) if i+j<12]} for i in range(0,12,3)]
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[
        {"type":"text","text":"الألعاب المتاحة","weight":"bold","size":"xl","color":c["primary"],"align":"center"},
        {"type":"text","text":"عدد الألعاب: 12","size":"sm","color":c["text2"],"align":"center","margin":"xs"},
        {"type":"separator","margin":"lg","color":c["border"]},
        *rows,
        _glass([{"type":"text","text":"أوامر اللعب","size":"sm","color":c["text"],"weight":"bold"},{"type":"text","text":"• اضغط على اسم اللعبة","size":"xs","color":c["text2"],"wrap":True,"margin":"sm"},{"type":"text","text":"• لمح للتلميح | جاوب للكشف","size":"xs","color":c["text2"],"wrap":True,"margin":"xs"},{"type":"text","text":"• إيقاف لإنهاء اللعبة","size":"xs","color":c["text2"],"wrap":True,"margin":"xs"}],theme,"15px","15px"),
        {"type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[_btn("البداية","بداية","secondary",theme),_btn("إيقاف","إيقاف","secondary",theme)]},
        {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center","margin":"sm"}
    ]}
    return attach_quick_reply(_flex("الألعاب",{"type":"bubble","size":"mega","body":body}))

def build_my_points(username, points, stats=None, theme=DEFAULT_THEME):
    c = _c(theme)
    level = "مبتدئ" if points<50 else "متوسط" if points<150 else "متقدم" if points<300 else "🏆 محترف"
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[
        {"type":"text","text":"نقاطي","weight":"bold","size":"xl","color":c["primary"],"align":"center"},
        {"type":"separator","margin":"lg","color":c["border"]},
        {"type":"text","text":f"{username}","size":"lg","color":c["text"],"weight":"bold","align":"center","margin":"lg"},
        _glass([{"type":"text","text":"النقاط الكلية","size":"sm","color":c["text2"],"align":"center"},{"type":"text","text":str(points),"size":"xxl","weight":"bold","color":c["primary"],"align":"center","margin":"sm"}],theme,"20px","25px"),
        _glass([{"type":"text","text":"المستوى الحالي","size":"sm","color":c["text2"],"align":"center"},{"type":"text","text":level,"size":"lg","weight":"bold","color":c["success"],"align":"center","margin":"sm"}],theme,"15px","15px"),
        {"type":"separator","margin":"lg","color":c["border"]},
        {"type":"text","text":"سيتم حذف بياناتك بعد 30 يوم من عدم النشاط","size":"xs","color":c["error"],"wrap":True,"align":"center"},
        {"type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[_btn("البداية","بداية","secondary",theme),_btn("الألعاب","ألعاب","secondary",theme)]},
        {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center","margin":"sm"}
    ]}
    return attach_quick_reply(_flex("نقاطي",{"type":"bubble","size":"mega","body":body}))

def build_leaderboard(top_users, theme=DEFAULT_THEME):
    c = _c(theme)
    medals = ["🥇","🥈","🥉"]
    items = [{"type":"box","layout":"vertical","spacing":"xs","paddingAll":"sm","borderWidth":"1px","borderColor":c["border"],"cornerRadius":"10px","margin":"sm","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"text","text":medals[i-1] if i<=3 else f"{i}.","size":"lg","flex":0,"color":c["primary"] if i<=3 else c["text"],"weight":"bold"},{"type":"text","text":name,"size":"sm","color":c["text"],"flex":3,"margin":"sm","weight":"bold"},{"type":"text","text":str(pts),"size":"sm","color":c["primary"],"align":"end","flex":1,"weight":"bold"}]},{"type":"text","text":"متصل الآن" if is_online else "غير متصل","size":"xxs","color":c["success"] if is_online else c["text3"],"align":"start","margin":"xs"}]} for i,(name,pts,is_online) in enumerate(top_users[:10],1)]
    if not items: items = [{"type":"text","text":"لا يوجد لاعبين مسجلين بعد","size":"sm","color":c["text2"],"align":"center"}]
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[
        {"type":"text","text":"🏆 لوحة الصدارة","weight":"bold","size":"xl","color":c["primary"],"align":"center"},
        {"type":"separator","margin":"lg","color":c["border"]},
        {"type":"box","layout":"vertical","contents":items,"margin":"lg"},
        {"type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[_btn("البداية","بداية","secondary",theme),_btn("نقاطي","نقاطي","secondary",theme)]},
        {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center","margin":"sm"}
    ]}
    return attach_quick_reply(_flex("الصدارة",{"type":"bubble","size":"mega","body":body}))

def build_help_window(theme=DEFAULT_THEME):
    c = _c(theme)
    cards = []
    for title, content in [
        ("المساعدة",[("أوامر التنقل","بداية | ألعاب | نقاطي | صدارة"),("أوامر اللعب","[اسم] للبدء | لمح | جاوب | إيقاف")]),
        ("نظام النقاط",[("كسب النقاط","1 نقطة لكل إجابة صحيحة"),("المستويات","0-49: مبتدئ | 50-149: متوسط | 150+: متقدم")]),
        ("وضع الفريقين",[("كيفية اللعب","1. فريقين → 2. انضم → 3. اختر اللعبة"),("الميزات","تقسيم تلقائي | نقاط منفصلة | بدون لمح")])
    ]: cards.append({"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[{"type":"text","text":title,"weight":"bold","size":"xl","color":c["primary"],"align":"center"},{"type":"separator","margin":"md","color":c["border"]}]+[_glass([{"type":"text","text":h,"weight":"bold","color":c["text"],"size":"sm"},{"type":"text","text":d,"size":"xs","color":c["text2"],"wrap":True,"margin":"sm"}],theme,"12px","12px") for h,d in content]}})
    return attach_quick_reply(_flex("المساعدة",{"type":"carousel","contents":cards}))

def build_registration_required(theme=DEFAULT_THEME):
    c = _c(theme)
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[{"type":"text","text":"يجب التسجيل أولاً","weight":"bold","size":"lg","color":c["warning"],"align":"center"},{"type":"separator","margin":"lg","color":c["border"]},_glass([{"type":"text","text":"اضغط 'انضم' للتسجيل والبدء باللعب","size":"sm","color":c["text2"],"align":"center","wrap":True}],theme,"15px","15px"),{"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[_btn("انضم","انضم","primary",theme),_btn("البداية","بداية","secondary",theme)]}]}
    return attach_quick_reply(_flex("تسجيل",{"type":"bubble","size":"mega","body":body}))

def build_winner_announcement(username, game_name, round_points, total_points, theme=DEFAULT_THEME):
    c = _c(theme)
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[{"type":"text","text":"🏆 مبروك!","size":"xxl","weight":"bold","align":"center","color":c["success"]},{"type":"separator","margin":"lg","color":c["border"]},{"type":"text","text":f"أنهيت لعبة {game_name}","size":"lg","color":c["text"],"align":"center","wrap":True,"margin":"md","weight":"bold"},_glass([{"type":"text","text":"النقاط المكتسبة","size":"sm","color":c["text2"],"align":"center"},{"type":"text","text":f"+{round_points}","size":"xxl","weight":"bold","color":c["success"],"align":"center","margin":"sm"}],theme,"20px","20px"),{"type":"text","text":f"إجمالي: {total_points}","size":"md","color":c["text"],"align":"center","margin":"md","weight":"bold"},{"type":"box","layout":"vertical","spacing":"sm","margin":"lg","contents":[_btn(f"{game_name}",game_name,"primary",theme),{"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_btn("الألعاب","ألعاب","secondary",theme),_btn("البداية","bداية","secondary",theme)]}]}]}
    return attach_quick_reply(_flex("فوز",{"type":"bubble","size":"mega","body":body}))

def build_theme_selector(theme=DEFAULT_THEME):
    c = _c(theme)
    rows = [{"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_btn(t,f"ثيم {t}","primary" if t==theme else "secondary",theme) for t in list(THEMES.keys())[i:i+3]]} for i in range(0,len(THEMES),3)]
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[{"type":"text","text":"اختر الثيم","size":"xl","weight":"bold","color":c["primary"],"align":"center"},{"type":"separator","margin":"lg","color":c["border"]},*rows,_btn("البداية","بداية","secondary",theme)]}
    return attach_quick_reply(_flex("الثيمات",{"type":"bubble","size":"mega","body":body}))

def build_multiplayer_help_window(theme=DEFAULT_THEME):
    c = _c(theme)
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[{"type":"text","text":"وضع الفريقين","size":"xl","weight":"bold","color":c["primary"],"align":"center"},{"type":"separator","margin":"lg","color":c["border"]},_glass([{"type":"text","text":"1. اكتب 'انضم'","size":"sm","color":c["text2"],"weight":"bold"},{"type":"text","text":"2. اختر اللعبة","size":"sm","color":c["text2"],"margin":"sm","weight":"bold"},{"type":"text","text":"3. تقسيم تلقائي","size":"sm","color":c["text2"],"margin":"sm","weight":"bold"}],theme,"15px","15px"),_btn("انضم","انضم","primary",theme)]}
    return attach_quick_reply(_flex("فريقين",{"type":"bubble","size":"mega","body":body}))

def build_join_confirmation(username, theme=DEFAULT_THEME):
    c = _c(theme)
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[{"type":"text","text":"انضممت","size":"lg","weight":"bold","color":c["success"],"align":"center"},{"type":"text","text":"انتظر اللعبة","size":"sm","color":c["text2"],"align":"center","margin":"md"}]}
    return attach_quick_reply(_flex("انضمام",{"type":"bubble","size":"mega","body":body}))

def build_error_message(error_text, theme=DEFAULT_THEME):
    c = _c(theme)
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[{"type":"text","text":error_text,"size":"md","color":c["error"],"align":"center","wrap":True,"weight":"bold"},_btn("البداية","بداية","secondary",theme)]}
    return attach_quick_reply(_flex("خطأ",{"type":"bubble","size":"mega","body":body}))

def build_game_stopped(game_name, theme=DEFAULT_THEME):
    c = _c(theme)
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[{"type":"text","text":"تم إيقاف اللعبة","size":"lg","weight":"bold","color":c["error"],"align":"center"},{"type":"text","text":f"لعبة {game_name}","size":"sm","color":c["text2"],"align":"center","margin":"sm"},{"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[_btn("الألعاب","ألعاب","primary",theme),_btn("البداية","بداية","secondary",theme)]}]}
    return attach_quick_reply(_flex("إيقاف",{"type":"bubble","size":"mega","body":body}))

def build_team_game_end(team_points, theme=DEFAULT_THEME):
    c = _c(theme)
    t1, t2 = team_points.get("team1",0), team_points.get("team2",0)
    winner = "الفريق الأول 🥇" if t1>t2 else "الفريق الثاني 🥈" if t2>t1 else "تعادل"
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[{"type":"text","text":"🏆 انتهت اللعبة!","size":"xl","weight":"bold","color":c["primary"],"align":"center"},{"type":"separator","margin":"lg","color":c["border"]},_glass([{"type":"box","layout":"horizontal","contents":[{"type":"text","text":f"الفريق 1\n{t1}","size":"lg","color":c["primary"],"align":"center","flex":1,"weight":"bold"},{"type":"text","text":"VS","size":"sm","color":c["text2"],"align":"center","flex":0,"weight":"bold"},{"type":"text","text":f"الفريق 2\n{t2}","size":"lg","color":c["primary"],"align":"center","flex":1,"weight":"bold"}]},{"type":"text","text":f"الفائز: {winner}","size":"md","weight":"bold","color":c["success"],"align":"center","margin":"md"}],theme,"20px","20px"),{"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[_btn("الألعاب","ألعاب","primary",theme),_btn("البداية","بداية","secondary",theme)]}]}
    return attach_quick_reply(_flex("نتيجة",{"type":"bubble","size":"mega","body":body}))

def build_answer_feedback(message, theme=DEFAULT_THEME):
    c = _c(theme)
    body = {"type":"box","layout":"vertical","paddingAll":"20px","backgroundColor":c["bg"],"contents":[{"type":"text","text":message,"size":"md","color":c["text"],"align":"center","wrap":True,"weight":"bold"}]}
    return attach_quick_reply(_flex("إجابة",{"type":"bubble","size":"mega","body":body}))

__all__ = ['build_enhanced_home','build_games_menu','build_my_points','build_leaderboard','build_help_window','build_registration_required','build_winner_announcement','build_theme_selector','build_multiplayer_help_window','attach_quick_reply','build_join_confirmation','build_error_message','build_game_stopped','build_team_game_end','build_answer_feedback']
