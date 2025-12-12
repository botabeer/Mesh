"""
Bot Mesh Constants Module
الثوابت والثيمات
Created by: Abeer Aldosari - 2025
"""

DEFAULT_THEME = "ابيض"

THEMES = {
    "ابيض": {
        "bg": "#F2F2F7",
        "card": "#FFFFFF",
        "primary": "#007AFF",
        "secondary": "#5AC8FA",
        "success": "#34C759",
        "text": "#000000",
        "text2": "#1C1C1E",
        "text3": "#8E8E93",
        "border": "#D1D1D6",
        "error": "#FF3B30",
        "warning": "#FF9500",
        "info": "#5AC8FA",
        "info_bg": "#EBF4FF",
        "name_ar": "ابيض",
        "name_en": "white"
    },
    "اسود": {
        "bg": "#000000",
        "card": "#1C1C1E",
        "primary": "#0A84FF",
        "secondary": "#64D2FF",
        "success": "#30D158",
        "text": "#FFFFFF",
        "text2": "#E5E5EA",
        "text3": "#8E8E93",
        "border": "#38383A",
        "error": "#FF453A",
        "warning": "#FFD60A",
        "info": "#64D2FF",
        "info_bg": "#1A2B3D",
        "name_ar": "اسود",
        "name_en": "black"
    },
    "ازرق": {
        "bg": "#EBF4FF",
        "card": "#FFFFFF",
        "primary": "#0066CC",
        "secondary": "#3399FF",
        "success": "#28A745",
        "text": "#001F3F",
        "text2": "#003366",
        "text3": "#6699CC",
        "border": "#B3D9FF",
        "error": "#DC3545",
        "warning": "#FFC107",
        "info": "#17A2B8",
        "info_bg": "#D6EAFF",
        "name_ar": "ازرق",
        "name_en": "blue"
    },
    "بنفسجي": {
        "bg": "#F5F0FF",
        "card": "#FFFFFF",
        "primary": "#8B5CF6",
        "secondary": "#A78BFA",
        "success": "#10B981",
        "text": "#3B0764",
        "text2": "#5B21B6",
        "text3": "#A78BFA",
        "border": "#DDD6FE",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "info": "#8B5CF6",
        "info_bg": "#EDE9FE",
        "name_ar": "بنفسجي",
        "name_en": "purple"
    },
    "وردي": {
        "bg": "#FFF1F2",
        "card": "#FFFFFF",
        "primary": "#EC4899",
        "secondary": "#F472B6",
        "success": "#10B981",
        "text": "#831843",
        "text2": "#9F1239",
        "text3": "#F472B6",
        "border": "#FBCFE8",
        "error": "#DC2626",
        "warning": "#F59E0B",
        "info": "#EC4899",
        "info_bg": "#FCE7F3",
        "name_ar": "وردي",
        "name_en": "pink"
    },
    "اخضر": {
        "bg": "#ECFDF5",
        "card": "#FFFFFF",
        "primary": "#059669",
        "secondary": "#10B981",
        "success": "#10B981",
        "text": "#064E3B",
        "text2": "#065F46",
        "text3": "#10B981",
        "border": "#A7F3D0",
        "error": "#DC2626",
        "warning": "#F59E0B",
        "info": "#059669",
        "info_bg": "#D1FAE5",
        "name_ar": "اخضر",
        "name_en": "green"
    },
    "رمادي": {
        "bg": "#F5F5F5",
        "card": "#FFFFFF",
        "primary": "#607D8B",
        "secondary": "#78909C",
        "success": "#66BB6A",
        "text": "#263238",
        "text2": "#37474F",
        "text3": "#90A4AE",
        "border": "#CFD8DC",
        "error": "#F44336",
        "warning": "#FF9800",
        "info": "#607D8B",
        "info_bg": "#ECEFF1",
        "name_ar": "رمادي",
        "name_en": "gray"
    },
    "احمر": {
        "bg": "#FEF2F2",
        "card": "#FFFFFF",
        "primary": "#DC2626",
        "secondary": "#EF4444",
        "success": "#10B981",
        "text": "#7F1D1D",
        "text2": "#991B1B",
        "text3": "#EF4444",
        "border": "#FECACA",
        "error": "#DC2626",
        "warning": "#F59E0B",
        "info": "#DC2626",
        "info_bg": "#FEE2E2",
        "name_ar": "احمر",
        "name_en": "red"
    },
    "بني": {
        "bg": "#F5F1ED",
        "card": "#FFFFFF",
        "primary": "#8B6F47",
        "secondary": "#A68A64",
        "success": "#66BB6A",
        "text": "#3E2723",
        "text2": "#5D4037",
        "text3": "#A1887F",
        "border": "#D7CCC8",
        "error": "#D32F2F",
        "warning": "#F57C00",
        "info": "#8B6F47",
        "info_bg": "#EFEBE9",
        "name_ar": "بني",
        "name_en": "brown"
    }
}

COMMANDS = {
    "navigation": {
        "بداية": ["home", "start"],
        "العاب": ["games"],
        "مساعدة": ["help"],
        "نقاطي": ["points", "stats"],
        "صدارة": ["leaderboard", "ranks"]
    },
    "account": {
        "انضم": ["join", "register"],
        "انسحب": ["leave", "unregister"]
    },
    "game": {
        "لمح": ["hint"],
        "جاوب": ["answer", "reveal"],
        "ايقاف": ["stop", "end"]
    },
    "group": {
        "فريقين": ["teams", "team_mode"],
        "فردي": ["solo", "solo_mode"]
    }
}

RESPONSE_MESSAGES = {
    "errors": {
        "not_registered": "يجب التسجيل اولا\nاكتب: انضم",
        "group_only": "هذه اللعبة للمجموعات فقط",
        "invalid_name": "الاسم غير صالح\nيجب ان يكون من 1-100 حرف",
        "already_registered": "انت مسجل بالفعل",
        "not_in_game": "لا توجد لعبة نشطة",
        "invalid_theme": "ثيم غير موجود\nالثيمات المتاحة: ابيض، اسود، ازرق، بنفسجي، وردي، اخضر، رمادي، احمر، بني"
    },
    "success": {
        "registered": "تم التسجيل بنجاح",
        "unregistered": "تم الانسحاب بنجاح",
        "game_stopped": "تم ايقاف اللعبة",
        "theme_changed": "تم تغيير الثيم",
        "mode_changed_team": "تم تفعيل وضع الفريقين",
        "mode_changed_solo": "تم تفعيل الوضع الفردي"
    },
    "info": {
        "registration_prompt": "ارسل اسمك للتسجيل\nالاسم يجب ان يكون من 1-100 حرف",
        "waiting_answer": "في انتظار الاجابة"
    }
}

GAME_CATEGORIES = {
    "ذهنية": ["ذكاء", "رياضيات", "خمن"],
    "لغوية": ["ترتيب", "تكوين", "ضد", "سلسلة", "لعبة"],
    "ترفيهية": ["روليت", "اغنيه", "لون", "توافق"],
    "سرعة": ["اسرع"],
    "جماعية": ["مافيا"]
}
