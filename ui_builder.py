from linebot.v3.messaging import FlexMessage,FlexContainer,QuickReply,QuickReplyItem,MessageAction,TextMessage
from constants import GAME_LIST,DEFAULT_THEME,THEMES,BOT_NAME,BOT_RIGHTS,QUICK_REPLY_BUTTONS

def _c(t=None):
    return THEMES.get(t or DEFAULT_THEME,THEMES[DEFAULT_THEME])

def _3d_card(contents,theme=None,padding="20px"):
    c=_c(theme)
    return {"type":"box","layout":"vertical","contents":contents,"backgroundColor":c["card"],"cornerRadius":"16px",
            "paddingAll":padding,"borderWidth":"1px","borderColor":c["border"],"margin":"md","offsetBottom":"4px"}

def _gradient_header(text,theme=None):
    c=_c(theme)
    return {"type":"box","layout":"vertical","contents":[{"type":"text","text":text,"size":"xxl","weight":"bold",
            "color":c["primary"],"align":"center","gravity":"center"}],"height":"60px","backgroundColor":c["card"],
            "cornerRadius":"16px","borderWidth":"1px","borderColor":c["border"],"paddingAll":"md","offsetBottom":"4px"}

def _premium_button(label,text,style="primary",theme=None):
    c=_c(theme)
    btn_color=c["primary"]if style=="primary"else c["secondary"]
    return {"type":"box","layout":"vertical","contents":[{"type":"text","text":label,"size":"sm","weight":"bold",
            "color":c["button_text"],"align":"center","gravity":"center"}],"backgroundColor":btn_color,
            "cornerRadius":"12px","paddingAll":"12px","action":{"type":"message","text":text},"height":"44px",
            "offsetBottom":"3px","borderWidth":"1px","borderColor":btn_color}

def _separator_3d(theme=None):
    c=_c(theme)
    return {"type":"separator","margin":"lg","color":c["border"]}

def _stat_box(label,value,color_key="primary",theme=None):
    c=_c(theme)
    return {"type":"box","layout":"vertical","contents":[
            {"type":"text","text":label,"size":"xs","color":c["text3"],"align":"center","weight":"bold"},
            {"type":"text","text":str(value),"size":"xxl","weight":"bold","color":c[color_key],"align":"center","margin":"sm"}],
            "backgroundColor":c["card"],"cornerRadius":"16px","paddingAll":"16px","borderWidth":"1px",
            "borderColor":c["border"],"flex":1,"offsetBottom":"4px"}

def _flex(alt_text,body):
    return FlexMessage(alt_text=alt_text,contents=FlexContainer.from_dict(body))

def build_quick_reply():
    return QuickReply(items=[QuickReplyItem(action=MessageAction(label=btn["label"],text=btn["text"]))for btn in QUICK_REPLY_BUTTONS])

def attach_quick_reply(m):
    if m and hasattr(m,'quick_reply'):
        m.quick_reply=build_quick_reply()
    return m

def build_custom_registration(theme=DEFAULT_THEME):
    return attach_quick_reply(TextMessage(text="ارسل اسمك للتسجيل\n\nيمكنك استخدام:\n- حروف عربية وانجليزية\n- ارقام\n- رموز ومسافات\n- حد اقصى 100 حرف"))

def build_enhanced_home(username,points,is_registered=True,theme=DEFAULT_THEME,mode_label="فردي"):
    c=_c(theme)
    status="مسجل"if is_registered else"غير مسجل"
    status_color=c["success"]if is_registered else c["text3"]
    join_text="انسحب"if is_registered else"تسجيل"
    next_mode="فردي"if mode_label=="فريقين"else"فريقين"
    themes_list=list(THEMES.keys())
    theme_buttons=[]
    for i in range(0,len(themes_list),3):
        row_themes=themes_list[i:i+3]
        theme_buttons.append({"type":"box","layout":"horizontal","spacing":"sm","margin":"sm",
            "contents":[_premium_button(t,f"ثيم {t}","primary"if t==theme else"secondary",theme)for t in row_themes]})
    body={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[
                _gradient_header(BOT_NAME,theme),
                {"type":"text","text":"يمكنك استخدام البوت في الخاص او المجموعات","size":"xs","color":c["text2"],"align":"center","margin":"xs"},
                _separator_3d(theme),
                _3d_card([{"type":"box","layout":"horizontal","contents":[{"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":username[:30],"size":"lg","weight":"bold","color":c["text"],"wrap":True},
                            {"type":"text","text":status,"size":"sm","color":status_color,"margin":"xs"}],"flex":1}]},
                    {"type":"separator","margin":"md","color":c["border"]},
                    {"type":"box","layout":"horizontal","contents":[
                        {"type":"text","text":"النقاط","size":"md","color":c["text2"],"flex":1},
                        {"type":"text","text":str(points),"size":"xxl","weight":"bold","color":c["primary"],"flex":0}],"margin":"md"}],theme,"18px"),
                {"type":"text","text":"اختر الثيم","size":"md","weight":"bold","color":c["text"],"margin":"lg","align":"center"},
                *theme_buttons,_separator_3d(theme),
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":f"الوضع: {mode_label}","size":"sm","weight":"bold","color":c["info"],"align":"center"}],
                    "backgroundColor":c["info_bg"],"cornerRadius":"12px","paddingAll":"10px","margin":"md"},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[
                    _premium_button(join_text,join_text if is_registered else"انضم","primary"if is_registered else"secondary",theme),
                    _premium_button("الالعاب","ألعاب","secondary",theme)]},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[
                    _premium_button("نقاطي","نقاطي","secondary",theme),
                    _premium_button("الصدارة","صدارة","secondary",theme)]},
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[
                    _premium_button(next_mode,next_mode,"primary",theme),
                    _premium_button("مساعدة","مساعدة","secondary",theme)]},
                _separator_3d(theme),
                {"type":"text","text":"استخدم الازرار الثابتة في الاسفل للتنقل السريع","size":"xxs","color":c["info"],"align":"center","wrap":True,"margin":"sm"},
                {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center","wrap":True,"margin":"xs"}],
            "paddingAll":"20px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("البداية",body))

def build_games_menu(theme=DEFAULT_THEME,top_games=None):
    c=_c(theme)
    default_order=["أسرع","ذكاء","لعبة","خمن","أغنيه","سلسلة","ترتيب","تكوين","ضد","لون","رياضيات","توافق","مافيا"]
    order=(top_games+[g for g in default_order if g not in top_games])if top_games and len(top_games)>0 else default_order
    order=order[:13]
    game_buttons=[]
    for i in range(0,len(order),3):
        game_buttons.append({"type":"box","layout":"horizontal","spacing":"sm","margin":"sm",
            "contents":[_premium_button(order[i+j],order[i+j],"primary",theme)for j in range(3)if i+j<len(order)]})
    body={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[
                _gradient_header("الالعاب",theme),
                {"type":"text","text":"مرتبة حسب الاكثر استخداما","size":"xs","color":c["text3"],"align":"center","margin":"sm"},
                _separator_3d(theme),*game_buttons,
                _3d_card([{"type":"text","text":"اوامر اللعب","size":"sm","weight":"bold","color":c["text"],"align":"center"},
                    {"type":"text","text":"اضغط اسم اللعبة - لمح - جاوب - ايقاف","size":"xs","color":c["text2"],"wrap":True,"margin":"sm","align":"center"}],theme,"14px"),
                _separator_3d(theme),
                {"type":"text","text":"لعبة المافيا للمجموعات فقط","size":"xs","color":c["warning"],"align":"center","wrap":True},
                {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center","wrap":True,"margin":"md"}],
            "paddingAll":"20px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("الالعاب",body))

def build_help_window(theme=DEFAULT_THEME):
    c=_c(theme)
    body={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[
                _gradient_header("Bot Mesh",theme),
                {"type":"text","text":"دليل استخدام البوت","size":"sm","color":c["text2"],"align":"center","margin":"sm"},
                _separator_3d(theme),
                {"type":"box","layout":"vertical","contents":[
                    {"type":"box","layout":"horizontal","contents":[
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"1","size":"xl","color":c["primary"],"weight":"bold"}],"flex":0,"gravity":"center","paddingEnd":"md"},
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"الازرار الثابتة","size":"sm","weight":"bold","color":c["text"]},
                            {"type":"text","text":"استخدم الازرار في الاسفل للتنقل السريع بين القوائم","size":"xs","color":c["text2"],"wrap":True,"margin":"xs"}],"flex":1}],"margin":"md"},
                    {"type":"separator","margin":"md","color":c["border"]},
                    {"type":"box","layout":"horizontal","contents":[
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"2","size":"xl","color":c["primary"],"weight":"bold"}],"flex":0,"gravity":"center","paddingEnd":"md"},
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"بدء اللعب","size":"sm","weight":"bold","color":c["text"]},
                            {"type":"text","text":"اضغط اسم اللعبة للبدء مباشرة","size":"xs","color":c["text2"],"wrap":True,"margin":"xs"}],"flex":1}],"margin":"md"},
                    {"type":"separator","margin":"md","color":c["border"]},
                    {"type":"box","layout":"horizontal","contents":[
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"3","size":"xl","color":c["primary"],"weight":"bold"}],"flex":0,"gravity":"center","paddingEnd":"md"},
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"التسجيل","size":"sm","weight":"bold","color":c["text"]},
                            {"type":"text","text":"تسجيل - انسحب - نقاطي - صدارة","size":"xs","color":c["text2"],"wrap":True,"margin":"xs"}],"flex":1}],"margin":"md"},
                    {"type":"separator","margin":"md","color":c["border"]},
                    {"type":"box","layout":"horizontal","contents":[
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"4","size":"xl","color":c["primary"],"weight":"bold"}],"flex":0,"gravity":"center","paddingEnd":"md"},
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"المساعدة","size":"sm","weight":"bold","color":c["text"]},
                            {"type":"text","text":"لمح - جاوب - ايقاف","size":"xs","color":c["text2"],"wrap":True,"margin":"xs"}],"flex":1}],"margin":"md"},
                    {"type":"separator","margin":"md","color":c["border"]},
                    {"type":"box","layout":"horizontal","contents":[
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"5","size":"xl","color":c["primary"],"weight":"bold"}],"flex":0,"gravity":"center","paddingEnd":"md"},
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"الثيمات","size":"sm","weight":"bold","color":c["text"]},
                            {"type":"text","text":"9 ثيمات متاحة - ثيم [اسم الثيم]","size":"xs","color":c["text2"],"wrap":True,"margin":"xs"}],"flex":1}],"margin":"md"},
                    {"type":"separator","margin":"md","color":c["border"]},
                    {"type":"box","layout":"horizontal","contents":[
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"6","size":"xl","color":c["primary"],"weight":"bold"}],"flex":0,"gravity":"center","paddingEnd":"md"},
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"وضع الفريقين","size":"sm","weight":"bold","color":c["text"]},
                            {"type":"text","text":"فريقين - فردي (في المجموعات فقط)","size":"xs","color":c["text2"],"wrap":True,"margin":"xs"}],"flex":1}],"margin":"md"}],
                    "backgroundColor":c["card"],"cornerRadius":"16px","paddingAll":"16px","borderWidth":"1px","borderColor":c["border"],"margin":"md","offsetBottom":"4px"},
                _3d_card([{"type":"text","text":"ملاحظة","size":"xs","weight":"bold","color":c["info"],"align":"center"},
                    {"type":"text","text":"لعبة توافق متاحة للجميع بدون تسجيل","size":"xs","color":c["text2"],"align":"center","margin":"xs"}],theme,"12px"),
                _separator_3d(theme),
                {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center","wrap":True}],
            "paddingAll":"20px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("المساعدة",body))

def build_my_points(username,points,stats=None,theme=DEFAULT_THEME):
    c=_c(theme)
    if points<50:
        level,level_color="مبتدئ",c["text2"]
    elif points<150:
        level,level_color="متوسط",c["info"]
    elif points<300:
        level,level_color="متقدم",c["warning"]
    else:
        level,level_color="محترف",c["success"]
    body={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[
                _gradient_header("احصائياتي",theme),_separator_3d(theme),
                _3d_card([{"type":"text","text":username[:30],"size":"xl","weight":"bold","color":c["text"],"align":"center","wrap":True},
                    {"type":"box","layout":"horizontal","contents":[
                        _stat_box("النقاط",points,"primary",theme),
                        {"type":"box","layout":"vertical","contents":[
                            {"type":"text","text":"المستوى","size":"xs","color":c["text3"],"align":"center","weight":"bold"},
                            {"type":"text","text":level,"size":"lg","weight":"bold","color":level_color,"align":"center","margin":"sm"}],
                            "backgroundColor":c["card"],"cornerRadius":"16px","paddingAll":"16px","borderWidth":"1px",
                            "borderColor":c["border"],"margin":"md","flex":1,"offsetBottom":"4px"}],"spacing":"sm","margin":"md"}],theme,"18px"),
                _separator_3d(theme),
                {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center"}],
            "paddingAll":"20px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("نقاطي",body))

def build_leaderboard(top_users,theme=DEFAULT_THEME):
    c=_c(theme)
    table_rows=[]
    medals=["1","2","3"]
    for i,(name,pts,is_registered)in enumerate(top_users[:20],1):
        status_icon="مسجل"if is_registered else"زائر"
        status_color=c["success"]if is_registered else c["text3"]
        if i<=3:
            rank_text=medals[i-1]
            rank_color=[c["primary"],c["accent"],c["secondary"]][i-1]
            border_width="2px"
            rank_size="xl"
        else:
            rank_text=str(i)
            rank_color=c["text2"]
            border_width="1px"
            rank_size="md"
        display_name=name[:20]if name else"مستخدم"
        table_rows.append({"type":"box","layout":"horizontal","contents":[
                {"type":"text","text":rank_text,"size":rank_size,"weight":"bold","color":rank_color,"flex":0,"align":"center","gravity":"center"},
                {"type":"separator","margin":"md","color":c["border"]},
                {"type":"text","text":display_name,"size":"md"if i<=3 else"sm","color":c["text"],"flex":4,"margin":"md","wrap":True,"weight":"bold"if i<=3 else"regular"},
                {"type":"separator","margin":"md","color":c["border"]},
                {"type":"text","text":str(pts),"size":"lg"if i<=3 else"md","weight":"bold","color":c["primary"],"align":"center","flex":1},
                {"type":"separator","margin":"md","color":c["border"]},
                {"type":"text","text":status_icon,"size":"xs","color":status_color,"flex":1,"align":"center"}],
            "paddingAll":"12px","backgroundColor":c["card"],"cornerRadius":"12px",
            "borderWidth":border_width,"borderColor":rank_color if i<=3 else c["border"],
            "margin":"xs","offsetBottom":"3px"if i<=3 else"2px"})
    table_header={"type":"box","layout":"horizontal","contents":[
            {"type":"text","text":"#","size":"xs","weight":"bold","color":c["button_text"],"flex":0,"align":"center"},
            {"type":"separator","margin":"md","color":c["button_text"]},
            {"type":"text","text":"اللاعب","size":"xs","weight":"bold","color":c["button_text"],"flex":4,"margin":"md"},
            {"type":"separator","margin":"md","color":c["button_text"]},
            {"type":"text","text":"النقاط","size":"xs","weight":"bold","color":c["button_text"],"align":"center","flex":1},
            {"type":"separator","margin":"md","color":c["button_text"]},
            {"type":"text","text":"الحالة","size":"xs","weight":"bold","color":c["button_text"],"flex":1,"align":"center"}],
        "paddingAll":"12px","backgroundColor":c["primary"],"cornerRadius":"12px","margin":"md","offsetBottom":"4px"}
    body={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[
                _gradient_header("لوحة الصدارة",theme),
                {"type":"text","text":"افضل 20 لاعب","size":"sm","color":c["text2"],"align":"center","margin":"sm"},
                _separator_3d(theme),table_header,
                {"type":"box","layout":"vertical","contents":table_rows,"margin":"sm"},
                _separator_3d(theme),
                {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center"}],
            "paddingAll":"20px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("الصدارة",body))

def build_winner_announcement(username,game_name,round_points,total_points,theme=DEFAULT_THEME):
    c=_c(theme)
    body={"type":"bubble","size":"kilo","body":{"type":"box","layout":"vertical","contents":[
                {"type":"text","text":"مبروك","size":"xl","weight":"bold","align":"center","color":c["success"],"margin":"md"},
                {"type":"text","text":username[:30],"size":"lg","weight":"bold","color":c["text"],"align":"center","margin":"sm","wrap":True},
                _separator_3d(theme),
                {"type":"box","layout":"vertical","contents":[
                    {"type":"text","text":"النقاط","size":"xs","color":c["text3"],"align":"center","weight":"bold"},
                    {"type":"text","text":f"+{round_points}","size":"xxl","weight":"bold","color":c["primary"],"align":"center","margin":"sm"}],
                    "backgroundColor":c["card"],"cornerRadius":"16px","paddingAll":"16px","margin":"md","borderWidth":"1px","borderColor":c["border"],"offsetBottom":"4px"},
                {"type":"text","text":f"الاجمالي: {total_points}","size":"sm","color":c["text2"],"align":"center","margin":"md"},
                _separator_3d(theme),
                {"type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[
                    _premium_button("اعادة",game_name,"primary",theme),
                    _premium_button("ايقاف","إيقاف","secondary",theme)]}],
            "paddingAll":"20px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("فوز",body))

def build_team_game_end(team_points,theme=DEFAULT_THEME):
    c=_c(theme)
    t1,t2=team_points.get("team1",0),team_points.get("team2",0)
    winner="الفريق الاول"if t1>t2 else"الفريق الثاني"if t2>t1 else"تعادل"
    body={"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[
                _gradient_header("انتهت اللعبة",theme),_separator_3d(theme),
                _3d_card([{"type":"box","layout":"horizontal","contents":[
                        {"type":"text","text":f"الفريق 1\n{t1}","size":"xl","weight":"bold","color":c["primary"],"align":"center","flex":1},
                        {"type":"text","text":"VS","size":"lg","color":c["text2"],"align":"center","flex":0,"weight":"bold"},
                        {"type":"text","text":f"الفريق 2\n{t2}","size":"xl","weight":"bold","color":c["primary"],"align":"center","flex":1}]},
                    {"type":"text","text":f"الفائز: {winner}","size":"lg","weight":"bold","color":c["success"],"align":"center","margin":"lg"}],theme,"18px"),
                _separator_3d(theme),
                {"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center"}],
            "paddingAll":"20px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("نتيجة",body))

def build_registration_status(username,points,theme=DEFAULT_THEME):
    return attach_quick_reply(TextMessage(text=f"تم التسجيل بنجاح\n\nالاسم: {username}\nالنقاط: {points}"))

def build_registration_required(theme=DEFAULT_THEME):
    return attach_quick_reply(TextMessage(text="يجب التسجيل اولا\n\nاستخدم زر التسجيل في الاسفل"))

def build_unregister_confirmation(username,points,theme=DEFAULT_THEME):
    return attach_quick_reply(TextMessage(text=f"تم الانسحاب\n\nالاسم: {username}\nنقاطك: {points}"))

def build_error_message(error_text,theme=DEFAULT_THEME):
    return attach_quick_reply(TextMessage(text=f"خطا: {error_text}"))

def build_game_stopped(game_name,theme=DEFAULT_THEME):
    return attach_quick_reply(TextMessage(text=f"تم ايقاف {game_name}"))

__all__=['build_enhanced_home','build_games_menu','build_my_points','build_leaderboard','build_help_window',
         'build_registration_status','build_registration_required','build_unregister_confirmation',
         'build_winner_announcement','attach_quick_reply','build_error_message','build_game_stopped',
         'build_team_game_end','build_custom_registration']
