import os,re
from typing import Dict,List,Tuple,Optional
from dotenv import load_dotenv

load_dotenv()

BOT_NAME="Bot Mesh"
BOT_VERSION="23.0 FINAL"
BOT_RIGHTS="تم انشاء هذا البوت بواسطة عبير الدوسري - 2025"

LINE_CHANNEL_SECRET=os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN=os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

def validate_env():
    if not LINE_CHANNEL_SECRET:
        raise ValueError("LINE_CHANNEL_SECRET is not set")
    if not LINE_CHANNEL_ACCESS_TOKEN:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set")

THEMES={
    "أبيض":{"name":"أبيض","bg":"#F2F2F7","card":"#FFFFFF","primary":"#007AFF","primary_hover":"#0051D5",
            "secondary":"#5AC8FA","accent":"#34C759","text":"#000000","text2":"#1C1C1E","text3":"#8E8E93",
            "border":"#D1D1D6","success":"#34C759","success_bg":"#E3F9E5","error":"#FF3B30","error_bg":"#FFEBE9",
            "warning":"#FF9500","info":"#007AFF","info_bg":"#E0F0FF","shadow":"rgba(0,0,0,0.06)",
            "shadow_strong":"rgba(0,0,0,0.12)","button_text":"#FFFFFF","disabled":"#C7C7CC","disabled_bg":"#E5E5EA",
            "gradient_start":"#007AFF","gradient_end":"#5AC8FA","card_shadow":"0 4px 12px rgba(0,0,0,0.08)",
            "button_shadow":"0 2px 8px rgba(0,122,255,0.25)"},
    "أسود":{"name":"أسود","bg":"#000000","card":"#1C1C1E","primary":"#0A84FF","primary_hover":"#409CFF",
            "secondary":"#64D2FF","accent":"#30D158","text":"#FFFFFF","text2":"#E5E5EA","text3":"#8E8E93",
            "border":"#38383A","success":"#30D158","success_bg":"#1A3A24","error":"#FF453A","error_bg":"#3D1A1A",
            "warning":"#FF9F0A","info":"#0A84FF","info_bg":"#1A2D45","shadow":"rgba(255,255,255,0.05)",
            "shadow_strong":"rgba(255,255,255,0.1)","button_text":"#FFFFFF","disabled":"#48484A","disabled_bg":"#2C2C2E",
            "gradient_start":"#0A84FF","gradient_end":"#64D2FF","card_shadow":"0 4px 12px rgba(0,0,0,0.5)",
            "button_shadow":"0 2px 8px rgba(10,132,255,0.4)"},
    "أزرق":{"name":"أزرق","bg":"#EBF4FF","card":"#FFFFFF","primary":"#0066CC","primary_hover":"#004C99",
            "secondary":"#3399FF","accent":"#66B3FF","text":"#001F3F","text2":"#003366","text3":"#6699CC",
            "border":"#B3D9FF","success":"#28A745","success_bg":"#E3F5E7","error":"#DC3545","error_bg":"#F8D7DA",
            "warning":"#FF9500","info":"#0066CC","info_bg":"#D6EAFF","shadow":"rgba(0,102,204,0.08)",
            "shadow_strong":"rgba(0,102,204,0.15)","button_text":"#FFFFFF","disabled":"#CCE5FF","disabled_bg":"#E6F2FF",
            "gradient_start":"#0066CC","gradient_end":"#66B3FF","card_shadow":"0 4px 12px rgba(0,102,204,0.12)",
            "button_shadow":"0 2px 8px rgba(0,102,204,0.3)"},
    "بنفسجي":{"name":"بنفسجي","bg":"#F5F0FF","card":"#FFFFFF","primary":"#8B5CF6","primary_hover":"#7C3AED",
            "secondary":"#A78BFA","accent":"#C4B5FD","text":"#3B0764","text2":"#5B21B6","text3":"#A78BFA",
            "border":"#DDD6FE","success":"#10B981","success_bg":"#D1FAE5","error":"#EF4444","error_bg":"#FEE2E2",
            "warning":"#F59E0B","info":"#8B5CF6","info_bg":"#EDE9FE","shadow":"rgba(139,92,246,0.08)",
            "shadow_strong":"rgba(139,92,246,0.15)","button_text":"#FFFFFF","disabled":"#E9D5FF","disabled_bg":"#F3E8FF",
            "gradient_start":"#8B5CF6","gradient_end":"#C4B5FD","card_shadow":"0 4px 12px rgba(139,92,246,0.12)",
            "button_shadow":"0 2px 8px rgba(139,92,246,0.3)"},
    "وردي":{"name":"وردي","bg":"#FFF1F2","card":"#FFFFFF","primary":"#EC4899","primary_hover":"#DB2777",
            "secondary":"#F472B6","accent":"#F9A8D4","text":"#831843","text2":"#9F1239","text3":"#F472B6",
            "border":"#FBCFE8","success":"#10B981","success_bg":"#D1FAE5","error":"#EF4444","error_bg":"#FEE2E2",
            "warning":"#F59E0B","info":"#EC4899","info_bg":"#FCE7F3","shadow":"rgba(236,72,153,0.08)",
            "shadow_strong":"rgba(236,72,153,0.15)","button_text":"#FFFFFF","disabled":"#FDE2E4","disabled_bg":"#FFF0F3",
            "gradient_start":"#EC4899","gradient_end":"#F9A8D4","card_shadow":"0 4px 12px rgba(236,72,153,0.12)",
            "button_shadow":"0 2px 8px rgba(236,72,153,0.3)"},
    "أخضر":{"name":"أخضر","bg":"#ECFDF5","card":"#FFFFFF","primary":"#059669","primary_hover":"#047857",
            "secondary":"#10B981","accent":"#34D399","text":"#064E3B","text2":"#065F46","text3":"#10B981",
            "border":"#A7F3D0","success":"#10B981","success_bg":"#D1FAE5","error":"#EF4444","error_bg":"#FEE2E2",
            "warning":"#F59E0B","info":"#059669","info_bg":"#D1FAE5","shadow":"rgba(5,150,105,0.08)",
            "shadow_strong":"rgba(5,150,105,0.15)","button_text":"#FFFFFF","disabled":"#BBF7D0","disabled_bg":"#DCFCE7",
            "gradient_start":"#059669","gradient_end":"#34D399","card_shadow":"0 4px 12px rgba(5,150,105,0.12)",
            "button_shadow":"0 2px 8px rgba(5,150,105,0.3)"},
    "رمادي":{"name":"رمادي","bg":"#F5F5F5","card":"#FFFFFF","primary":"#607D8B","primary_hover":"#455A64",
            "secondary":"#78909C","accent":"#90A4AE","text":"#263238","text2":"#37474F","text3":"#90A4AE",
            "border":"#CFD8DC","success":"#66BB6A","success_bg":"#E8F5E9","error":"#EF5350","error_bg":"#FFEBEE",
            "warning":"#FFA726","info":"#607D8B","info_bg":"#ECEFF1","shadow":"rgba(96,125,139,0.08)",
            "shadow_strong":"rgba(96,125,139,0.15)","button_text":"#FFFFFF","disabled":"#B0BEC5","disabled_bg":"#ECEFF1",
            "gradient_start":"#607D8B","gradient_end":"#90A4AE","card_shadow":"0 4px 12px rgba(96,125,139,0.12)",
            "button_shadow":"0 2px 8px rgba(96,125,139,0.3)"},
    "أحمر":{"name":"أحمر","bg":"#FEF2F2","card":"#FFFFFF","primary":"#DC2626","primary_hover":"#B91C1C",
            "secondary":"#EF4444","accent":"#F87171","text":"#7F1D1D","text2":"#991B1B","text3":"#EF4444",
            "border":"#FECACA","success":"#10B981","success_bg":"#D1FAE5","error":"#DC2626","error_bg":"#FEE2E2",
            "warning":"#F59E0B","info":"#DC2626","info_bg":"#FEE2E2","shadow":"rgba(220,38,38,0.08)",
            "shadow_strong":"rgba(220,38,38,0.15)","button_text":"#FFFFFF","disabled":"#FECACA","disabled_bg":"#FEF2F2",
            "gradient_start":"#DC2626","gradient_end":"#F87171","card_shadow":"0 4px 12px rgba(220,38,38,0.12)",
            "button_shadow":"0 2px 8px rgba(220,38,38,0.3)"},
    "بني":{"name":"بني","bg":"#F5F1ED","card":"#FFFFFF","primary":"#8B6F47","primary_hover":"#6B5435",
            "secondary":"#A68A64","accent":"#C4A57B","text":"#3E2723","text2":"#5D4037","text3":"#A1887F",
            "border":"#D7CCC8","success":"#66BB6A","success_bg":"#E8F5E9","error":"#EF5350","error_bg":"#FFEBEE",
            "warning":"#FFA726","info":"#8B6F47","info_bg":"#EFEBE9","shadow":"rgba(139,111,71,0.08)",
            "shadow_strong":"rgba(139,111,71,0.15)","button_text":"#FFFFFF","disabled":"#BCAAA4","disabled_bg":"#EFEBE9",
            "gradient_start":"#8B6F47","gradient_end":"#C4A57B","card_shadow":"0 4px 12px rgba(139,111,71,0.12)",
            "button_shadow":"0 2px 8px rgba(139,111,71,0.3)"}
}

DEFAULT_THEME="أبيض"

GAME_CONFIG={
    "ذكاء":{"display":"ذكاء","hint":True,"reveal":True,"timer":0},
    "روليت":{"display":"روليت","hint":True,"reveal":True,"timer":0},
    "خمن":{"display":"خمن","hint":True,"reveal":True,"timer":0},
    "أغنيه":{"display":"أغنيه","hint":True,"reveal":True,"timer":0},
    "ترتيب":{"display":"ترتيب","hint":True,"reveal":True,"timer":0},
    "تكوين":{"display":"تكوين","hint":True,"reveal":True,"timer":0},
    "ضد":{"display":"ضد","hint":True,"reveal":True,"timer":0},
    "لعبة":{"display":"لعبة","hint":True,"reveal":True,"timer":0},
    "أسرع":{"display":"أسرع","hint":False,"reveal":False,"timer":20},
    "سلسلة":{"display":"سلسلة","hint":False,"reveal":False,"timer":0},
    "لون":{"display":"لون","hint":True,"reveal":True,"timer":0},
    "رياضيات":{"display":"رياضيات","hint":True,"reveal":True,"timer":0},
    "توافق":{"display":"توافق","hint":False,"reveal":False,"timer":0},
    "مافيا":{"display":"مافيا","hint":False,"reveal":False,"timer":0}
}

GAME_LIST=[(k,v["display"])for k,v in GAME_CONFIG.items()]
GAME_NAMES={k:v["display"]for k,v in GAME_CONFIG.items()}
DISPLAY_TO_CLASS={v["display"]:k for k,v in GAME_CONFIG.items()}
GAME_COMMANDS=set(DISPLAY_TO_CLASS.keys())

QUICK_REPLY_BUTTONS=[
    {"label":"بداية","text":"بداية"},
    {"label":"العاب","text":"ألعاب"},
    {"label":"مساعدة","text":"مساعدة"},
    {"label":"تسجيل","text":"انضم"},
    {"label":"انسحب","text":"انسحب"},
    {"label":"نقاطي","text":"نقاطي"},
    {"label":"صدارة","text":"صدارة"},
    {"label":"ايقاف","text":"إيقاف"}
]

PRIVACY_SETTINGS={"auto_delete_inactive_days":90,"cache_timeout_minutes":10,"cleanup_interval_hours":24,
                 "max_sessions_per_user":5,"session_timeout_minutes":45}

SECURITY_SETTINGS={"rate_limit_requests":30,"rate_limit_window_seconds":60,"max_message_length":1000,
                  "max_game_duration_minutes":20,"enable_sql_injection_protection":True,
                  "enable_xss_protection":True,"enable_csrf_protection":True,"enable_rate_limiting":True}

ALLOWED_COMMANDS={"مساعدة","help","بداية","home","الرئيسية","start","ألعاب","games","العاب","نقاطي","points",
                 "نقاط","صدارة","leaderboard","مستوى","انضم","join","تسجيل","انسحب","leave","خروج",
                 "فريقين","teams","فرق","فردي","solo","ثيمات","themes","مظهر","لمح","hint","جاوب","reveal",
                 "answer","إيقاف","ايقاف","stop"}

def normalize_text(text:str)->str:
    if not text or not isinstance(text,str):
        return ""
    text=text[:SECURITY_SETTINGS["max_message_length"]].strip().lower()
    for old,new in {'أ':'ا','إ':'ا','آ':'ا','ى':'ي','ة':'ه','ؤ':'و','ئ':'ي'}.items():
        text=text.replace(old,new)
    text=re.sub(r'[\u064B-\u065F\u0670]','',text)
    return text

def sanitize_input(text:str)->str:
    if not text:
        return ""
    if SECURITY_SETTINGS["enable_sql_injection_protection"]:
        for pattern in [r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b',r'--',r'/\*',r'\*/']:
            if re.search(pattern,text,re.IGNORECASE):
                return ""
    return text[:SECURITY_SETTINGS["max_message_length"]]

def get_theme_colors(theme_name:Optional[str]=None)->Dict[str,str]:
    return THEMES.get(theme_name or DEFAULT_THEME,THEMES[DEFAULT_THEME])

def validate_theme(theme_name:str)->str:
    return theme_name if theme_name in THEMES else DEFAULT_THEME

def get_username(profile)->str:
    try:
        name=profile.display_name if hasattr(profile,'display_name')else"مستخدم"
        if not name or not isinstance(name,str):
            return"مستخدم"
        name=sanitize_input(name)
        return name[:50]if name else"مستخدم"
    except:
        return"مستخدم"

def get_game_display_name(internal_name:str)->str:
    return GAME_NAMES.get(internal_name,internal_name)

def get_game_class_name(display_name:str)->str:
    return DISPLAY_TO_CLASS.get(display_name,display_name)

def get_game_config(game_name:str)->Dict:
    return GAME_CONFIG.get(game_name,{})

def is_valid_game(game_name:str)->bool:
    return game_name in GAME_NAMES.values()or game_name in GAME_CONFIG.keys()

def is_allowed_command(text:str)->bool:
    if not text or not isinstance(text,str):
        return False
    lowered=text.lower().strip()
    return lowered in ALLOWED_COMMANDS or text.strip()in GAME_COMMANDS or lowered.startswith("ثيم ")

__all__=['BOT_NAME','BOT_VERSION','BOT_RIGHTS','LINE_CHANNEL_SECRET','LINE_CHANNEL_ACCESS_TOKEN','THEMES','DEFAULT_THEME',
         'GAME_CONFIG','GAME_LIST','GAME_NAMES','QUICK_REPLY_BUTTONS','DISPLAY_TO_CLASS','PRIVACY_SETTINGS','SECURITY_SETTINGS',
         'ALLOWED_COMMANDS','GAME_COMMANDS','validate_env','normalize_text','sanitize_input','get_theme_colors',
         'validate_theme','get_username','get_game_display_name','get_game_class_name','get_game_config',
         'is_valid_game','is_allowed_command']
