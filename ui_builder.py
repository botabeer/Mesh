from linebot.v3.messaging import FlexMessage,FlexContainer,QuickReply,QuickReplyItem,MessageAction,TextMessage
from constants import GAME_LIST,DEFAULT_THEME,THEMES,BOT_NAME,BOT_RIGHTS,FIXED_GAME_QR

def _c(t=None):return THEMES.get(t or DEFAULT_THEME,THEMES[DEFAULT_THEME])

def _3d_card(contents,theme=None,padding="20px"):
    c = _c(theme)
    return {"type":"box","layout":"vertical","contents":contents,"backgroundColor":c["card"],"cornerRadius":"20px","paddingAll":padding,"borderWidth":"2px","borderColor":c["border"],"margin":"md"}

def _gradient_header(text,theme=None):
    c = _c(theme)
    return {"type":"box","layout":"horizontal","contents":[{"type":"text","text":text,"size":"xxl","weight":"bold","color":c["primary"],"flex":1,"align":"center"}],"paddingBottom":"lg"}

def _premium_button(label,text,style="primary",theme=None):
    c = _c(theme)
    return {"type":"button","action":{"type":"message","label":label,"text":text},"style":style,"height":"sm","color":c["primary"] if style == "primary" else c["secondary"]}

def _separator_3d(theme=None):
    c = _c(theme)
    return {"type":"separator","margin":"lg","color":c["border"]}

def _stat_box(label,value,color_key="primary",theme=None):
    c = _c(theme)
    return _3d_card([{"type":"text","text":label,"size":"sm","color":c["text2"],"align":"center"},{"type":"text","text":str(value),"size":"xxl","weight":"bold","color":c[color_key],"align":"center","margin":"sm"}],theme,"15px")

def _flex(alt_text,body):return FlexMessage(alt_text=alt_text,contents=FlexContainer.from_dict(body))

def build_games_quick_reply():return QuickReply(items=[QuickReplyItem(action=MessageAction(label=i["label"],text=i["text"])) for i in FIXED_GAME_QR])

def attach_quick_reply(m):
    if m and hasattr(m,'quick_reply'):m.quick_reply = build_games_quick_reply()
    return m

def build_enhanced_home(username,points,is_registered=True,theme=DEFAULT_THEME,mode_label="فردي"):
    c = _c(theme)
    status = "مسجل" if is_registered else "غير مسجل"
    join_text = "انسحب" if is_registered else "انضم"
    themes_list = list(THEMES.keys())
    theme_buttons = []
    for i in range(0,len(themes_list),3):
        row = {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_premium_button(t,f"ثيم {t}","primary" if t == theme else "secondary",theme) for t in themes_list[i:i+3]]}
        theme_buttons.append(row)
    body = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[_gradient_header(BOT_NAME,theme),_separator_3d(theme),_3d_card([{"type":"box","layout":"horizontal","contents":[{"type":"box","layout":"vertical","contents":[{"type":"text","text":username,"size":"lg","weight":"bold","color":c["text"]},{"type":"text","text":status,"size":"sm","color":c["success"] if is_registered else c["text3"]}],"flex":1}]},{"type":"separator","margin":"md","color":c["border"]},{"type":"box","layout":"horizontal","contents":[{"type":"text","text":"النقاط","size":"md","color":c["text2"],"flex":1},{"type":"text","text":str(points),"size":"xxl","weight":"bold","color":c["primary"],"flex":0}],"margin":"md"}],theme),{"type":"text","text":"اختر الثيم","size":"lg","weight":"bold","color":c["text"],"margin":"xl"},*theme_buttons,_separator_3d(theme),{"type":"text","text":f"الوضع الحالي: {mode_label}","size":"md","weight":"bold","color":c["info"],"align":"center","margin":"md"},{"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[_premium_button(join_text,join_text,"primary" if is_registered else "secondary",theme),_premium_button("الألعاب","ألعاب","secondary",theme)]},{"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_premium_button("نقاطي","نقاطي","secondary",theme),_premium_button("الصدارة","صدارة","secondary",theme)]},{"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_premium_button(mode_label,"فريقين" if mode_label=="فردي" else "فردي","primary",theme),_premium_button("مساعدة","مساعدة","secondary",theme)]},_separator_3d(theme),{"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center","wrap":True,"margin":"md"}],"paddingAll":"24px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("البداية",body))

def build_games_menu(theme=DEFAULT_THEME):
    c = _c(theme)
    order = ["ذكاء","رياضيات","خمن","أغنيه","ترتيب","تكوين","ضد","لعبة","أسرع","سلسلة","لون","توافق"]
    game_buttons = []
    for i in range(0,len(order),3):
        row = {"type":"box","layout":"horizontal","spacing":"sm","margin":"sm","contents":[_premium_button(order[i+j],order[i+j],"primary",theme) for j in range(3) if i+j < len(order)]}
        game_buttons.append(row)
    body = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[_gradient_header("الألعاب المتاحة",theme),{"type":"text","text":"Bot Mesh","size":"sm","color":c["text2"],"align":"center"},_separator_3d(theme),*game_buttons,_3d_card([{"type":"text","text":"أوامر اللعب","size":"md","weight":"bold","color":c["text"]},{"type":"text","text":"اضغط على اسم اللعبة للبدء\nلمح للتلميح | جاوب للكشف\nإيقاف لإنهاء اللعبة","size":"xs","color":c["text2"],"wrap":True,"margin":"sm"}],theme,"15px"),{"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[_premium_button("البداية","بداية","secondary",theme),_premium_button("إيقاف","إيقاف","secondary",theme)]},_separator_3d(theme),{"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center","wrap":True}],"paddingAll":"24px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("الألعاب",body))

def build_help_window(theme=DEFAULT_THEME):
    c = _c(theme)
    body = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[_gradient_header("المساعدة",theme),_separator_3d(theme),_3d_card([{"type":"text","text":"أوامر التنقل","size":"md","weight":"bold","color":c["primary"]},{"type":"text","text":"بداية | ألعاب | نقاطي | صدارة","size":"sm","color":c["text"],"wrap":True,"margin":"sm"}],theme,"15px"),_3d_card([{"type":"text","text":"أوامر اللعب","size":"md","weight":"bold","color":c["primary"]},{"type":"text","text":"لمح | جاوب | إيقاف","size":"sm","color":c["text"],"wrap":True,"margin":"sm"}],theme,"15px"),_3d_card([{"type":"text","text":"نظام النقاط","size":"md","weight":"bold","color":c["primary"]},{"type":"text","text":"نقطة واحدة لكل إجابة صحيحة","size":"sm","color":c["text"],"wrap":True,"margin":"sm"}],theme,"15px"),_3d_card([{"type":"text","text":"وضع الفريقين","size":"md","weight":"bold","color":c["primary"]},{"type":"text","text":"1. اكتب انضم\n2. اكتب فريقين\n3. اختر اللعبة\n4. تقسيم تلقائي","size":"sm","color":c["text"],"wrap":True,"margin":"sm"}],theme,"15px"),{"type":"box","layout":"horizontal","spacing":"sm","margin":"xl","contents":[_premium_button("البداية","بداية","primary",theme),_premium_button("الألعاب","ألعاب","secondary",theme)]},_separator_3d(theme),{"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center","wrap":True}],"paddingAll":"24px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("المساعدة",body))

def build_my_points(username,points,stats=None,theme=DEFAULT_THEME):
    c = _c(theme)
    if points < 50:level,level_color = "مبتدئ",c["text2"]
    elif points < 150:level,level_color = "متوسط",c["info"]
    elif points < 300:level,level_color = "متقدم",c["warning"]
    else:level,level_color = "محترف",c["success"]
    body = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[_gradient_header("إحصائياتي",theme),_separator_3d(theme),_3d_card([{"type":"text","text":username,"size":"xl","weight":"bold","color":c["text"],"align":"center"},{"type":"box","layout":"horizontal","contents":[_stat_box("النقاط",points,"primary",theme),{"type":"box","layout":"vertical","contents":[{"type":"text","text":"المستوى","size":"sm","color":c["text2"],"align":"center"},{"type":"text","text":level,"size":"lg","weight":"bold","color":level_color,"align":"center","margin":"sm"}],"backgroundColor":c["card"],"cornerRadius":"20px","paddingAll":"15px","borderWidth":"2px","borderColor":c["border"],"margin":"md","flex":1}],"spacing":"sm","margin":"md"}],theme),{"type":"box","layout":"horizontal","spacing":"sm","margin":"xl","contents":[_premium_button("البداية","بداية","secondary",theme),_premium_button("الصدارة","صدارة","primary",theme)]},_separator_3d(theme),{"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center"}],"paddingAll":"24px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("نقاطي",body))

def build_leaderboard(top_users,theme=DEFAULT_THEME):
    c = _c(theme)
    podium = []
    for i,(name,pts,is_registered) in enumerate(top_users[:3] if len(top_users) >= 3 else top_users,1):
        rank_display,rank_color = (["الأول","الثاني","الثالث"][i-1],[c["primary"],c["accent"],c["secondary"]][i-1])
        podium.append({"type":"box","layout":"vertical","contents":[{"type":"box","layout":"horizontal","contents":[{"type":"box","layout":"vertical","contents":[{"type":"text","text":rank_display,"size":"sm","color":rank_color,"align":"center","weight":"bold"},{"type":"text","text":str(i),"size":"xxl" if i == 1 else "xl","weight":"bold","color":rank_color,"align":"center"}],"flex":0,"width":"70px"},{"type":"box","layout":"vertical","contents":[{"type":"text","text":name[:20],"size":"lg" if i == 1 else "md","weight":"bold","color":c["text"],"wrap":True},{"type":"text","text":"نشط" if is_registered else "غير نشط","size":"xs","color":c["success"] if is_registered else c["text3"]}],"flex":1,"margin":"md"},{"type":"box","layout":"vertical","contents":[{"type":"text","text":str(pts),"size":"xl" if i == 1 else "lg","weight":"bold","color":c["primary"],"align":"center"},{"type":"text","text":"نقطة","size":"xs","color":c["text2"],"align":"center"}],"flex":0,"width":"70px"}]}],"backgroundColor":c["card"],"cornerRadius":"15px","paddingAll":"15px","borderWidth":"3px" if i == 1 else "2px","borderColor":rank_color,"margin":"sm"})
    rest_items = []
    for i,(name,pts,is_registered) in enumerate(top_users[3:10],4):
        rest_items.append({"type":"box","layout":"horizontal","contents":[{"type":"text","text":f"{i}","size":"md","weight":"bold","color":c["text"],"flex":0,"align":"center"},{"type":"text","text":name[:25],"size":"sm","color":c["text"],"flex":3,"margin":"md","wrap":True},{"type":"text","text":str(pts),"size":"md","weight":"bold","color":c["primary"],"align":"end","flex":1}],"paddingAll":"10px","backgroundColor":c["card"],"cornerRadius":"10px","borderWidth":"1px","borderColor":c["border"],"margin":"xs"})
    body_contents = [_gradient_header("لوحة الصدارة",theme),{"type":"text","text":"أفضل اللاعبين","size":"md","color":c["text2"],"align":"center","margin":"sm"},_separator_3d(theme),{"type":"text","text":"المراكز الأولى","size":"sm","color":c["text"],"weight":"bold","margin":"md"}]
    body_contents.extend(podium)
    if rest_items:body_contents.extend([_separator_3d(theme),{"type":"text","text":"بقية المتسابقين","size":"sm","color":c["text"],"weight":"bold","margin":"md"},{"type":"box","layout":"vertical","contents":rest_items,"margin":"sm"}])
    body_contents.extend([_separator_3d(theme),{"type":"text","text":"نشط = مسجل | غير نشط = ألغى التسجيل","size":"xxs","color":c["text3"],"align":"center","wrap":True},{"type":"box","layout":"horizontal","spacing":"sm","margin":"lg","contents":[_premium_button("البداية","بداية","secondary",theme),_premium_button("نقاطي","نقاطي","primary",theme)]},_separator_3d(theme),{"type":"text","text":BOT_RIGHTS,"size":"xxs","color":c["text3"],"align":"center"}])
    body = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":body_contents,"paddingAll":"24px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("الصدارة",body))

def build_winner_announcement(username,game_name,round_points,total_points,theme=DEFAULT_THEME):
    c = _c(theme)
    body = {"type":"bubble","size":"kilo","body":{"type":"box","layout":"vertical","contents":[{"type":"text","text":"مبروك","size":"xl","weight":"bold","align":"center","color":c["success"]},{"type":"text","text":username,"size":"lg","weight":"bold","color":c["text"],"align":"center","margin":"md"},_separator_3d(theme),{"type":"box","layout":"horizontal","contents":[{"type":"box","layout":"vertical","contents":[{"type":"text","text":"النقاط","size":"xs","color":c["text2"],"align":"center"},{"type":"text","text":f"+{round_points}","size":"xxl","weight":"bold","color":c["primary"],"align":"center"}],"backgroundColor":c["card"],"cornerRadius":"15px","paddingAll":"15px","flex":1}],"margin":"md"},{"type":"text","text":f"الإجمالي: {total_points}","size":"sm","color":c["text2"],"align":"center","margin":"md"},_separator_3d(theme),{"type":"box","layout":"horizontal","spacing":"sm","margin":"md","contents":[_premium_button("إعادة",game_name,"primary",theme),_premium_button("إيقاف","إيقاف","secondary",theme)]}],"paddingAll":"20px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("فوز",body))

def build_theme_selector(theme=DEFAULT_THEME):return build_enhanced_home("مستخدم",0,True,theme,"فردي")
def build_registration_status(username,points,theme=DEFAULT_THEME):return TextMessage(text=f"تم التسجيل\nالاسم: {username}\nالنقاط: {points}")
def build_registration_required(theme=DEFAULT_THEME):return TextMessage(text="التسجيل مطلوب\nاكتب: انضم")
def build_unregister_confirmation(username,points,theme=DEFAULT_THEME):return TextMessage(text=f"تم الانسحاب\nنقاطك: {points}")
def build_multiplayer_help_window(theme=DEFAULT_THEME):return TextMessage(text="وضع الفريقين\n1. اكتب: انضم\n2. اكتب: فريقين\n3. اختر اللعبة\n4. تقسيم تلقائي")
def build_join_confirmation(username,theme=DEFAULT_THEME):return TextMessage(text="انضممت للفريق")
def build_error_message(error_text,theme=DEFAULT_THEME):return TextMessage(text=f"خطأ: {error_text}")
def build_game_stopped(game_name,theme=DEFAULT_THEME):return TextMessage(text=f"تم إيقاف {game_name}")

def build_team_game_end(team_points,theme=DEFAULT_THEME):
    c = _c(theme)
    t1,t2 = team_points.get("team1",0),team_points.get("team2",0)
    winner = "الفريق الأول" if t1 > t2 else "الفريق الثاني" if t2 > t1 else "تعادل"
    body = {"type":"bubble","size":"mega","body":{"type":"box","layout":"vertical","contents":[_gradient_header("انتهت اللعبة",theme),_separator_3d(theme),_3d_card([{"type":"box","layout":"horizontal","contents":[{"type":"text","text":f"الفريق 1\n{t1}","size":"xl","weight":"bold","color":c["primary"],"align":"center","flex":1},{"type":"text","text":"VS","size":"lg","color":c["text2"],"align":"center","flex":0,"weight":"bold"},{"type":"text","text":f"الفريق 2\n{t2}","size":"xl","weight":"bold","color":c["primary"],"align":"center","flex":1}]},{"type":"text","text":f"الفائز: {winner}","size":"lg","weight":"bold","color":c["success"],"align":"center","margin":"lg"}],theme),{"type":"box","layout":"horizontal","spacing":"sm","margin":"xl","contents":[_premium_button("الألعاب","ألعاب","primary",theme),_premium_button("البداية","بداية","secondary",theme)]}],"paddingAll":"24px","backgroundColor":c["bg"]}}
    return attach_quick_reply(_flex("نتيجة",body))

def build_answer_feedback(message,theme=DEFAULT_THEME):return TextMessage(text=message)

__all__ = ['build_enhanced_home','build_games_menu','build_my_points','build_leaderboard','build_help_window','build_registration_status','build_registration_required','build_unregister_confirmation','build_winner_announcement','build_theme_selector','build_multiplayer_help_window','attach_quick_reply','build_join_confirmation','build_error_message','build_game_stopped','build_team_game_end','build_answer_feedback']
