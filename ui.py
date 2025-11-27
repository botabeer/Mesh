"""
🎨 Bot Mesh v7.0 - UI System
نظام الواجهات المحسّن مع دعم الثيمات
Created by: Abeer Aldosari © 2025
"""

from linebot.v3.messaging import TextMessage
from typing import Dict, Any, List


class UI:
    """نظام الواجهات المحسّن"""
    
    # ثيمات احترافية
    THEMES = {
        "أزرق": {
            "primary": "#0EA5E9",
            "secondary": "#38BDF8",
            "bg": "#F0F9FF",
            "card": "#E0F2FE",
            "text": "#0C4A6E",
            "text2": "#075985",
            "success": "#10B981",
            "error": "#EF4444"
        },
        "أسود": {
            "primary": "#60A5FA",
            "secondary": "#818CF8",
            "bg": "#0F172A",
            "card": "#1E293B",
            "text": "#F1F5F9",
            "text2": "#CBD5E1",
            "success": "#34D399",
            "error": "#F87171"
        },
        "بنفسجي": {
            "primary": "#A78BFA",
            "secondary": "#C4B5FD",
            "bg": "#FAF5FF",
            "card": "#F3E8FF",
            "text": "#5B21B6",
            "text2": "#7C3AED",
            "success": "#10B981",
            "error": "#EF4444"
        },
        "وردي": {
            "primary": "#EC4899",
            "secondary": "#F472B6",
            "bg": "#FFF1F2",
            "card": "#FFE4EC",
            "text": "#831843",
            "text2": "#9D174D",
            "success": "#10B981",
            "error": "#EF4444"
        },
        "أخضر": {
            "primary": "#10B981",
            "secondary": "#34D399",
            "bg": "#F0FDF4",
            "card": "#D1FAE5",
            "text": "#064E3B",
            "text2": "#065F46",
            "success": "#059669",
            "error": "#EF4444"
        }
    }
    
    def __init__(self):
        """تهيئة نظام الواجهات"""
        pass
    
    def get_theme_colors(self, theme_name: str = "أزرق") -> Dict[str, str]:
        """الحصول على ألوان الثيم"""
        return self.THEMES.get(theme_name, self.THEMES["أزرق"])
    
    def build_home(self, username: str, points: int, theme: str = "أزرق") -> TextMessage:
        """بناء الصفحة الرئيسية"""
        text = f"""🎮 مرحباً {username}!

📊 إحصائياتك:
• النقاط: {points}
• الحالة: نشط

📝 القوائم المتاحة:
• العاب - لعرض قائمة الألعاب
• نقاطي - لعرض إحصائياتك
• صدارة - لعرض لوحة الصدارة
• مساعدة - للمساعدة

🎯 لبدء لعبة:
اكتب: لعبة [اسم اللعبة]
مثال: لعبة ذكاء

✨ Bot Mesh v7.0
Created by: Abeer Aldosari © 2025"""
        
        return TextMessage(text=text)
    
    def build_games_menu(self, theme: str = "أزرق") -> TextMessage:
        """بناء قائمة الألعاب"""
        text = """🎮 الألعاب المتاحة:

🧠 لعبة ذكاء - ألغاز ذكية
🔢 لعبة رياضيات - أسئلة حسابية
⚡ لعبة سرعة - كتابة سريعة
🔤 لعبة كلمات - كلمات مبعثرة
🎨 لعبة ألوان - لون الكلمة
↔️ لعبة أضداد - أضداد الكلمات
🔗 لعبة سلسلة - سلسلة كلمات
🔮 لعبة تخمين - تخمين الكلمات
🎵 لعبة أغنية - تخمين الأغاني
📝 لعبة تكوين - تكوين الكلمات
🎯 لعبة إنسان حيوان - إنسان حيوان نبات
🖤 لعبة توافق - اختبار التوافق

📝 للعب:
اكتب: لعبة [اسم اللعبة]
مثال: لعبة ذكاء"""
        
        return TextMessage(text=text)
    
    def build_user_stats(self, username: str, user_data: Dict, rank: int, theme: str = "أزرق") -> TextMessage:
        """بناء إحصائيات المستخدم"""
        win_rate = 0
        if user_data.get('games_played', 0) > 0:
            win_rate = (user_data.get('wins', 0) / user_data['games_played']) * 100
        
        text = f"""📊 إحصائيات {username}

🏆 الترتيب: #{rank}
⭐ النقاط: {user_data.get('points', 0)}
🎮 الألعاب: {user_data.get('games_played', 0)}
✅ الانتصارات: {user_data.get('wins', 0)}
📈 نسبة الفوز: {win_rate:.1f}%
🎨 الثيم: {user_data.get('theme', 'أزرق')}

💪 استمر في اللعب لزيادة نقاطك!"""
        
        return TextMessage(text=text)
    
    def build_leaderboard(self, leaderboard: List[Dict], theme: str = "أزرق") -> TextMessage:
        """بناء لوحة الصدارة"""
        if not leaderboard:
            return TextMessage(text="📊 لوحة الصدارة فارغة حالياً")
        
        text = "🏆 لوحة الصدارة\n\n"
        
        medals = ["🥇", "🥈", "🥉"]
        
        for i, player in enumerate(leaderboard, 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            name = player.get('display_name', 'مستخدم')
            points = player.get('points', 0)
            games = player.get('games_played', 0)
            wins = player.get('wins', 0)
            
            text += f"{medal} {name}\n"
            text += f"   • النقاط: {points}\n"
            text += f"   • الألعاب: {games} | الفوز: {wins}\n\n"
        
        return TextMessage(text=text)
    
    def build_help(self, theme: str = "أزرق") -> TextMessage:
        """بناء صفحة المساعدة"""
        text = """📖 دليل استخدام Bot Mesh

🎮 كيفية اللعب:
1️⃣ اكتب 'العاب' لعرض قائمة الألعاب
2️⃣ اكتب 'لعبة [اسم]' لبدء لعبة
   مثال: لعبة ذكاء
3️⃣ أجب على الأسئلة

⌨️ الأوامر المتاحة:
• بداية - الصفحة الرئيسية
• العاب - قائمة الألعاب
• نقاطي - إحصائياتك
• صدارة - لوحة الصدارة
• مساعدة - هذه الصفحة

🎯 أثناء اللعب:
• لمح - للحصول على تلميح
• جاوب - لكشف الإجابة
• إيقاف - لإيقاف اللعبة

🎨 تغيير الثيم:
اكتب: ثيم [اسم]
الثيمات: أزرق، أسود، بنفسجي، وردي، أخضر

💡 نصائح:
• كل إجابة صحيحة = 10 نقاط
• حاول الإجابة بسرعة
• تنافس مع الأصدقاء

✨ Bot Mesh v7.0
Created by: Abeer Aldosari © 2025"""
        
        return TextMessage(text=text)
    
    def build_game_question(
        self, 
        game_name: str, 
        question_text: str, 
        round_num: int, 
        total_rounds: int, 
        theme: str = "أزرق"
    ) -> TextMessage:
        """بناء سؤال اللعبة"""
        text = f"""🎮 {game_name}

📝 جولة {round_num}/{total_rounds}

{question_text}

💡 أوامر متاحة:
• لمح - للحصول على تلميح
• جاوب - لكشف الإجابة
• إيقاف - لإيقاف اللعبة"""
        
        return TextMessage(text=text)
    
    def build_game_result(self, game_name: str, points: int, theme: str = "أزرق") -> TextMessage:
        """بناء نتيجة اللعبة"""
        if points > 40:
            emoji = "🏆"
            status = "ممتاز!"
        elif points > 20:
            emoji = "⭐"
            status = "جيد!"
        elif points > 0:
            emoji = "👍"
            status = "حاول مرة أخرى"
        else:
            emoji = "💪"
            status = "لا تستسلم!"
        
        text = f"""🎮 انتهت اللعبة!

{emoji} {status}

📊 النتيجة:
• اللعبة: {game_name}
• النقاط: {points}

🎯 لعب مرة أخرى:
اكتب: لعبة {game_name}

📝 لقائمة الألعاب:
اكتب: العاب"""
        
        return TextMessage(text=text)
    
    def build_error_message(self, error_text: str) -> TextMessage:
        """بناء رسالة خطأ"""
        text = f"""❌ خطأ

{error_text}

💡 للمساعدة اكتب: مساعدة"""
        
        return TextMessage(text=text)
