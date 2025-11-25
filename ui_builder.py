def game_menu_ui(game_title, description, actions):
    return {
        "type": "bubble",
        "direction": "rtl",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type":"text","text":game_title,"weight":"bold","size":"xl","align":"center","wrap":True},
                {"type":"text","text":description,"size":"md","color":"#555555","align":"center","wrap":True},
                {"type":"box","layout":"vertical","spacing":"sm","margin":"lg",
                 "contents":[
                     {"type":"button","style":"primary","color":"#1E88E5",
                      "action":{"type":"postback","data":act["data"],"label":act["label"]}}
                 for act in actions]}
            ]
        }
    }

def points_ui(username, points, rank):
    return {
        "type":"bubble",
        "direction":"rtl",
        "body":{
            "type":"box",
            "layout":"vertical",
            "spacing":"md",
            "contents":[
                {"type":"text","text":f"🏆 نقاط {username}","weight":"bold","size":"xl","align":"center"},
                {"type":"separator","margin":"md"},
                {"type":"text","text":f"رصيدك الحالي: {points} نقطة","size":"lg","align":"center","color":"#1E88E5"},
                {"type":"text","text":f"الترتيب العام: #{rank}","size":"md","align":"center","color":"#555555"},
            ]
        }
    }



# --- Leaderboard Flex builders (PRO) ---
def leaderboard_flex(ranking, user_id=None, theme='light', top_n=10):
    \"\"\"Builds a Flex message bubble for leaderboard.
    ranking: list of tuples (user_id, points, display_name, avatar_url_optional)
    user_id: int/str of current user to highlight
    theme: 'light'|'dark'|'gold'
    \"\"\"
    from ui.themes import THEMES as _THEMES
    th = _THEMES.get(theme, _THEMES['light'])
    # head
    header = {
        \"type\": \"box\",
        \"layout\": \"vertical\",
        \"contents\": [
            {\"type\":\"text\",\"text\":\"🏆 أعلى اللاعبين\",\"weight\":\"bold\",\"size\":\"lg\",\"align\":\"center\"},
        ]
    }
    # entries
    contents = []
    medals = [\"🥇\",\"🥈\",\"🥉\"]
    for idx, entry in enumerate(ranking[:top_n], start=1):
        try:
            uid, pts = entry[0], entry[1]
            name = entry[2] if len(entry)>2 else f\"مستخدم {uid}\"
            avatar = entry[3] if len(entry)>3 else None
        except Exception:
            uid, pts, name, avatar = entry[0], entry[1], str(entry[0]), None
        left = {\"type\":\"text\",\"text\":(medals[idx-1] if idx<=3 else f\"#{idx}\"),\"size\":\"md\",\"weight\":\"bold\",\"align\":\"start\"}
        mid = {\"type\":\"text\",\"text\":name,\"size\":\"md\",\"align\":\"start\",\"wrap\":True}
        right = {\"type\":\"text\",\"text\":str(pts),\"size\":\"md\",\"align\":\"end\",\"weight\":\"bold\",\"color\":th['primary']}
        row = {\"type\":\"box\",\"layout\":\"baseline\",\"spacing\":\"sm\",\"contents\":[left, {\"type\":\"box\",\"layout\":\"vertical\",\"contents\":[mid]}, right]}
        contents.append(row)
    # user rank
    user_rank = None
    if user_id is not None:
        for i,entry in enumerate(ranking, start=1):
            if str(entry[0])==str(user_id):
                user_rank = (i, entry[1])
                break
    footer = []
    if user_rank:
        footer.append({\"type\":\"separator\"})
        footer.append({\"type\":\"text\",\"text\":f\"أنت: #{user_rank[0]} — {user_rank[1]} نقطة\",\"size\":\"sm\",\"align\":\"center\",\"color\":\"#777777\"})
    bubble = {
        \"type\": \"bubble\",
        \"direction\": \"rtl\",
        \"body\": {
            \"type\": \"box\",
            \"layout\": \"vertical\",
            \"spacing\": \"sm\",
            \"contents\": [header] + contents + footer
        }
    }
    return bubble
# --- end leaderboard builder ---
