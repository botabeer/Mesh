"""
Bot Mesh - Achievements System
Created by: Abeer Aldosari © 2025

Features:
- 20+ unique achievements
- Progress tracking
- Point rewards
- Smart unlock detection
- Beautiful Flex UI
"""

from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# ==================== Achievement Definitions ====================

ACHIEVEMENTS = {
    # المبتدئين
    "first_game": {
        "id": "first_game",
        "name": "🎮 أول خطوة",
        "description": "العب أول لعبة",
        "points_reward": 5,
        "icon": "🎮",
        "category": "beginner"
    },
    "first_win": {
        "id": "first_win",
        "name": "🏆 أول فوز",
        "description": "اربح أول لعبة",
        "points_reward": 10,
        "icon": "🏆",
        "category": "beginner"
    },
    "registered": {
        "id": "registered",
        "name": "📝 عضو رسمي",
        "description": "سجل في البوت",
        "points_reward": 5,
        "icon": "📝",
        "category": "beginner"
    },
    
    # النقاط
    "points_50": {
        "id": "points_50",
        "name": "⭐ نجم صاعد",
        "description": "احصل على 50 نقطة",
        "points_reward": 10,
        "icon": "⭐",
        "category": "points"
    },
    "points_100": {
        "id": "points_100",
        "name": "💫 نجم ساطع",
        "description": "احصل على 100 نقطة",
        "points_reward": 20,
        "icon": "💫",
        "category": "points"
    },
    "points_250": {
        "id": "points_250",
        "name": "🌟 نجم لامع",
        "description": "احصل على 250 نقطة",
        "points_reward": 30,
        "icon": "🌟",
        "category": "points"
    },
    "points_500": {
        "id": "points_500",
        "name": "✨ نجم متألق",
        "description": "احصل على 500 نقطة",
        "points_reward": 50,
        "icon": "✨",
        "category": "points"
    },
    
    # السرعة
    "speed_demon": {
        "id": "speed_demon",
        "name": "⚡ سرعة البرق",
        "description": "أكمل لعبة الكتابة السريعة في أقل من 3 ثوانٍ",
        "points_reward": 15,
        "icon": "⚡",
        "category": "speed"
    },
    "fast_thinker": {
        "id": "fast_thinker",
        "name": "🧠 تفكير سريع",
        "description": "أجب على 5 أسئلة صحيحة على التوالي في أقل من دقيقة",
        "points_reward": 20,
        "icon": "🧠",
        "category": "speed"
    },
    
    # الذكاء
    "genius": {
        "id": "genius",
        "name": "🎓 عبقري",
        "description": "أجب على 10 ألغاز IQ صحيحة على التوالي",
        "points_reward": 25,
        "icon": "🎓",
        "category": "intelligence"
    },
    "math_wizard": {
        "id": "math_wizard",
        "name": "🔢 ساحر الأرقام",
        "description": "أكمل 20 لعبة رياضيات بدون أخطاء",
        "points_reward": 30,
        "icon": "🔢",
        "category": "intelligence"
    },
    
    # المثابرة
    "persistent": {
        "id": "persistent",
        "name": "💪 مثابر",
        "description": "العب 10 ألعاب في يوم واحد",
        "points_reward": 20,
        "icon": "💪",
        "category": "persistence"
    },
    "dedicated": {
        "id": "dedicated",
        "name": "🎯 مخلص",
        "description": "العب كل يوم لمدة أسبوع",
        "points_reward": 50,
        "icon": "🎯",
        "category": "persistence"
    },
    "marathon": {
        "id": "marathon",
        "name": "🏃 ماراثون",
        "description": "العب 50 لعبة في المجموع",
        "points_reward": 40,
        "icon": "🏃",
        "category": "persistence"
    },
    
    # التنوع
    "explorer": {
        "id": "explorer",
        "name": "🗺️ مستكشف",
        "description": "جرب جميع الألعاب (12 لعبة)",
        "points_reward": 35,
        "icon": "🗺️",
        "category": "variety"
    },
    "versatile": {
        "id": "versatile",
        "name": "🎨 متعدد المواهب",
        "description": "اربح في 5 ألعاب مختلفة",
        "points_reward": 25,
        "icon": "🎨",
        "category": "variety"
    },
    
    # الدقة
    "perfectionist": {
        "id": "perfectionist",
        "name": "💎 مثالي",
        "description": "احصل على 100% في لعبة كاملة",
        "points_reward": 30,
        "icon": "💎",
        "category": "accuracy"
    },
    "sharp_eye": {
        "id": "sharp_eye",
        "name": "👁️ عين حادة",
        "description": "اربح 10 مرات في لعبة لون الكلمة",
        "points_reward": 20,
        "icon": "👁️",
        "category": "accuracy"
    },
    
    # الاجتماعية
    "social_butterfly": {
        "id": "social_butterfly",
        "name": "🦋 اجتماعي",
        "description": "العب في 3 مجموعات مختلفة",
        "points_reward": 15,
        "icon": "🦋",
        "category": "social"
    },
    "top_player": {
        "id": "top_player",
        "name": "👑 اللاعب الأول",
        "description": "احتل المركز الأول في الصدارة",
        "points_reward": 50,
        "icon": "👑",
        "category": "social"
    },
    
    # الخاصة
    "legend": {
        "id": "legend",
        "name": "🌠 أسطورة",
        "description": "افتح جميع الإنجازات الأخرى",
        "points_reward": 100,
        "icon": "🌠",
        "category": "special"
    }
}


class AchievementManager:
    """مدير نظام الإنجازات"""
    
    def __init__(self, database):
        self.db = database
        self._init_achievements()
    
    def _init_achievements(self):
        """تهيئة الإنجازات في قاعدة البيانات"""
        for achievement in ACHIEVEMENTS.values():
            self.db.create_achievement(
                achievement_id=achievement["id"],
                name=achievement["name"],
                description=achievement["description"],
                points_reward=achievement["points_reward"],
                icon=achievement["icon"]
            )
        logger.info(f"✅ Initialized {len(ACHIEVEMENTS)} achievements")
    
    def check_and_unlock(self, user_id: str, trigger: str, data: Dict = None) -> List[Dict]:
        """التحقق من الإنجازات وفتح ما ينطبق"""
        unlocked = []
        
        # الحصول على بيانات المستخدم
        user = self.db.get_user(user_id)
        if not user:
            return unlocked
        
        points = user['points']
        user_stats = self.db.get_user_game_stats(user_id)
        total_games = sum(user_stats.values())
        
        # التحقق من كل trigger
        if trigger == "game_played":
            # أول لعبة
            if total_games == 1:
                if self._unlock(user_id, "first_game"):
                    unlocked.append(ACHIEVEMENTS["first_game"])
        
        elif trigger == "game_won":
            # أول فوز
            if self._is_first_win(user_id):
                if self._unlock(user_id, "first_win"):
                    unlocked.append(ACHIEVEMENTS["first_win"])
        
        elif trigger == "registered":
            # التسجيل
            if self._unlock(user_id, "registered"):
                unlocked.append(ACHIEVEMENTS["registered"])
        
        elif trigger == "points_updated":
            # إنجازات النقاط
            if points >= 50 and self._unlock(user_id, "points_50"):
                unlocked.append(ACHIEVEMENTS["points_50"])
            if points >= 100 and self._unlock(user_id, "points_100"):
                unlocked.append(ACHIEVEMENTS["points_100"])
            if points >= 250 and self._unlock(user_id, "points_250"):
                unlocked.append(ACHIEVEMENTS["points_250"])
            if points >= 500 and self._unlock(user_id, "points_500"):
                unlocked.append(ACHIEVEMENTS["points_500"])
        
        elif trigger == "speed_record" and data:
            # سرعة البرق
            if data.get('time', 999) < 3.0 and data.get('game') == 'كتابة سريعة':
                if self._unlock(user_id, "speed_demon"):
                    unlocked.append(ACHIEVEMENTS["speed_demon"])
        
        elif trigger == "perfect_score":
            # مثالي
            if self._unlock(user_id, "perfectionist"):
                unlocked.append(ACHIEVEMENTS["perfectionist"])
        
        elif trigger == "games_count":
            # المثابرة
            if total_games >= 10:
                if self._unlock(user_id, "persistent"):
                    unlocked.append(ACHIEVEMENTS["persistent"])
            if total_games >= 50:
                if self._unlock(user_id, "marathon"):
                    unlocked.append(ACHIEVEMENTS["marathon"])
            
            # المستكشف
            if len(user_stats) >= 12:
                if self._unlock(user_id, "explorer"):
                    unlocked.append(ACHIEVEMENTS["explorer"])
        
        elif trigger == "leaderboard_top":
            # اللاعب الأول
            rank = self.db.get_user_rank(user_id)
            if rank == 1:
                if self._unlock(user_id, "top_player"):
                    unlocked.append(ACHIEVEMENTS["top_player"])
        
        # التحقق من إنجاز الأسطورة
        if self._check_legend(user_id):
            if self._unlock(user_id, "legend"):
                unlocked.append(ACHIEVEMENTS["legend"])
        
        return unlocked
    
    def _unlock(self, user_id: str, achievement_id: str) -> bool:
        """محاولة فتح إنجاز"""
        success = self.db.unlock_achievement(user_id, achievement_id)
        if success:
            achievement = ACHIEVEMENTS[achievement_id]
            logger.info(f"🏆 Achievement unlocked: {achievement['name']} for user {user_id}")
        return success
    
    def _is_first_win(self, user_id: str) -> bool:
        """التحقق من أول فوز"""
        # يمكن تحسينها بإضافة جدول للفوزات في قاعدة البيانات
        return True
    
    def _check_legend(self, user_id: str) -> bool:
        """التحقق من إنجاز الأسطورة"""
        user_achievements = self.db.get_user_achievements(user_id)
        total_achievements = len(ACHIEVEMENTS) - 1  # بدون الأسطورة نفسها
        return len(user_achievements) >= total_achievements
    
    def get_user_progress(self, user_id: str) -> Dict:
        """الحصول على تقدم المستخدم في الإنجازات"""
        user_achievements = self.db.get_user_achievements(user_id)
        unlocked_ids = {a['achievement_id'] for a in user_achievements}
        
        categories = {}
        for achievement in ACHIEVEMENTS.values():
            category = achievement['category']
            if category not in categories:
                categories[category] = {
                    'total': 0,
                    'unlocked': 0,
                    'achievements': []
                }
            
            categories[category]['total'] += 1
            is_unlocked = achievement['id'] in unlocked_ids
            if is_unlocked:
                categories[category]['unlocked'] += 1
            
            categories[category]['achievements'].append({
                **achievement,
                'unlocked': is_unlocked
            })
        
        return {
            'total_achievements': len(ACHIEVEMENTS),
            'unlocked_achievements': len(user_achievements),
            'categories': categories,
            'progress_percentage': round(len(user_achievements) / len(ACHIEVEMENTS) * 100, 1)
        }
    
    def get_next_achievements(self, user_id: str, limit: int = 3) -> List[Dict]:
        """الحصول على الإنجازات القريبة من الفتح"""
        user = self.db.get_user(user_id)
        if not user:
            return []
        
        user_achievements = self.db.get_user_achievements(user_id)
        unlocked_ids = {a['achievement_id'] for a in user_achievements}
        
        # الإنجازات غير المفتوحة
        locked = [a for a in ACHIEVEMENTS.values() if a['id'] not in unlocked_ids]
        
        # ترتيب حسب الأولوية (يمكن تحسينها بناءً على إحصائيات اللاعب)
        priority_order = ['beginner', 'points', 'persistence', 'speed', 'intelligence', 'variety', 'accuracy', 'social', 'special']
        locked.sort(key=lambda x: priority_order.index(x['category']) if x['category'] in priority_order else 999)
        
        return locked[:limit]


# ==================== UI Builder for Achievements ====================

def build_achievements_ui(user_id: str, achievement_manager: AchievementManager, theme: str = "أبيض"):
    """بناء واجهة الإنجازات"""
    from constants import THEMES, DEFAULT_THEME, BOT_RIGHTS
    from linebot.v3.messaging import FlexMessage, FlexContainer
    
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    progress = achievement_manager.get_user_progress(user_id)
    
    # محتوى الرأس
    header_contents = [
        {
            "type": "text",
            "text": "🏆 الإنجازات",
            "weight": "bold",
            "size": "xl",
            "color": colors["primary"],
            "align": "center"
        },
        {
            "type": "text",
            "text": f"فتحت {progress['unlocked_achievements']} من {progress['total_achievements']} ({progress['progress_percentage']}%)",
            "size": "sm",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    # محتوى الجسم
    body_contents = []
    
    for category_name, category_data in progress['categories'].items():
        # عنوان الفئة
        body_contents.append({
            "type": "text",
            "text": f"📂 {category_name}",
            "size": "md",
            "weight": "bold",
            "color": colors["text"],
            "margin": "lg"
        })
        
        # الإنجازات
        for achievement in category_data['achievements'][:3]:  # أول 3 فقط
            body_contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": achievement['icon'],
                        "size": "xl",
                        "flex": 0
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": achievement['name'],
                                "size": "sm",
                                "weight": "bold",
                                "color": colors["success"] if achievement['unlocked'] else colors["text2"]
                            },
                            {
                                "type": "text",
                                "text": achievement['description'],
                                "size": "xs",
                                "color": colors["text2"],
                                "wrap": True
                            }
                        ],
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": "✅" if achievement['unlocked'] else "🔒",
                        "size": "lg",
                        "flex": 0
                    }
                ],
                "backgroundColor": colors["card"],
                "cornerRadius": "15px",
                "paddingAll": "12px",
                "margin": "sm"
            })
    
    # Footer
    footer_contents = [
        {
            "type": "button",
            "action": {"type": "message", "label": "🏠 البداية", "text": "بداية"},
            "style": "secondary",
            "height": "sm"
        },
        {"type": "separator", "color": colors["shadow1"]},
        {
            "type": "text",
            "text": BOT_RIGHTS,
            "size": "xxs",
            "color": colors["text2"],
            "align": "center"
        }
    ]
    
    # بناء البطاقة
    card = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": header_contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": body_contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_contents,
            "backgroundColor": colors["bg"],
            "paddingAll": "15px"
        }
    }
    
    return FlexMessage(alt_text="الإنجازات", contents=FlexContainer.from_dict(card))


def build_achievement_unlock_notification(achievement: Dict, theme: str = "أبيض"):
    """إشعار فتح إنجاز"""
    from constants import THEMES, DEFAULT_THEME
    from linebot.v3.messaging import FlexMessage, FlexContainer
    
    colors = THEMES.get(theme, THEMES[DEFAULT_THEME])
    
    card = {
        "type": "bubble",
        "size": "kilo",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🎉 إنجاز جديد!",
                    "weight": "bold",
                    "size": "xl",
                    "color": colors["success"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": achievement['icon'],
                    "size": "xxl",
                    "align": "center",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": achievement['name'],
                    "size": "lg",
                    "weight": "bold",
                    "color": colors["primary"],
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": achievement['description'],
                    "size": "sm",
                    "color": colors["text2"],
                    "align": "center",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": f"+{achievement['points_reward']} نقطة",
                    "size": "md",
                    "color": colors["success"],
                    "align": "center",
                    "weight": "bold",
                    "margin": "md"
                }
            ],
            "backgroundColor": colors["bg"],
            "paddingAll": "20px"
        }
    }
    
    return FlexMessage(alt_text="🎉 إنجاز جديد!", contents=FlexContainer.from_dict(card))
