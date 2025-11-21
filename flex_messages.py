"""
flex_messages.py - تصاميم Flex Messages بستايل Neumorphism Soft
"""

from config import Config

class FlexDesign:
    """تصاميم Neumorphism الحديثة"""
    
    BG = Config.BG_COLOR
    TEXT_PRIMARY = Config.TEXT_PRIMARY
    TEXT_SECONDARY = Config.TEXT_SECONDARY
    ACCENT = Config.ACCENT_COLOR
    
    @staticmethod
    def main_menu():
        """القائمة الرئيسية"""
        return {
            "type": "bubble", "size": "mega",
            "body": {
                "type": "box", "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "🎮 Neumorphism Soft", "weight": "bold", "size": "xl", "align": "center", "color": FlexDesign.TEXT_PRIMARY},
                    {"type": "text", "text": "تأثير 3D - عمق ناعم", "size": "sm", "align": "center", "color": FlexDesign.TEXT_SECONDARY, "margin": "sm"},
                    {"type": "separator", "margin": "xl"},
                    {"type": "box", "layout": "vertical", "contents": [
                        FlexDesign._game_button("🔤", "تكوين الكلمات", "letters"),
                        FlexDesign._game_button("⚡", "أسرع إجابة", "fast"),
                        FlexDesign._game_button("🔀", "ترتيب الحروف", "scramble"),
                        FlexDesign._game_button("🔗", "سلسلة الكلمات", "chain"),
                        FlexDesign._game_button("🧠", "أسئلة ذكاء", "iq")
                    ], "spacing": "md", "margin": "xl"},
                    {"type": "separator", "margin": "xl"},
                    {"type": "box", "layout": "horizontal", "contents": [
                        {"type": "button", "action": {"type": "message", "label": "🏆 الصدارة", "text": "الصدارة"}, "style": "secondary", "height": "sm"},
                        {"type": "button", "action": {"type": "message", "label": "👥 انضم", "text": "انضم"}, "style": "primary", "height": "sm", "color": FlexDesign.ACCENT}
                    ], "spacing": "sm", "margin": "xl"}
                ], "backgroundColor": FlexDesign.BG, "paddingAll": "24px"
            }
        }
    
    @staticmethod
    def _game_button(emoji, name, game_id):
        """زر لعبة"""
        return {
            "type": "box", "layout": "horizontal",
            "contents": [
                {"type": "text", "text": emoji, "size": "xl", "flex": 0},
                {"type": "text", "text": name, "size": "md", "color": FlexDesign.TEXT_PRIMARY, "flex": 1, "margin": "md", "weight": "bold"},
                {"type": "button", "action": {"type": "message", "label": "▶", "text": game_id}, "style": "primary", "height": "sm", "flex": 0, "color": FlexDesign.ACCENT}
            ], "spacing": "md", "paddingAll": "12px", "cornerRadius": "16px", "backgroundColor": FlexDesign.BG
        }
    
    @staticmethod
    def game_screen(game_name, question, letters=None, round_num=1, total_rounds=5):
        """شاشة اللعبة"""
        contents = [
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": f"■ {game_name}", "weight": "bold", "size": "lg", "color": FlexDesign.TEXT_PRIMARY, "flex": 1},
                {"type": "text", "text": f"سؤال {round_num}/{total_rounds}", "size": "sm", "color": FlexDesign.TEXT_SECONDARY, "align": "end"}
            ]},
            {"type": "separator", "margin": "lg"}
        ]
        
        if letters:
            letter_boxes = [{"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": l, "size": "xxl", "color": FlexDesign.ACCENT, "align": "center", "weight": "bold"}
            ], "width": "60px", "height": "60px", "backgroundColor": FlexDesign.BG, "cornerRadius": "16px", "justifyContent": "center"} for l in letters]
            contents.append({"type": "box", "layout": "horizontal", "contents": letter_boxes, "spacing": "sm", "margin": "xl", "justifyContent": "center", "paddingAll": "20px", "cornerRadius": "20px", "backgroundColor": FlexDesign.BG})
        
        contents.extend([
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": question, "size": "md", "color": FlexDesign.TEXT_PRIMARY, "align": "center", "wrap": True}
            ], "paddingAll": "20px", "cornerRadius": "16px", "backgroundColor": FlexDesign.BG, "margin": "lg"},
            {"type": "box", "layout": "horizontal", "contents": [
                {"type": "button", "action": {"type": "message", "label": "الحل", "text": "الحل"}, "style": "secondary", "height": "sm"},
                {"type": "button", "action": {"type": "message", "label": "تلميح", "text": "تلميح"}, "style": "primary", "height": "sm", "color": FlexDesign.ACCENT}
            ], "spacing": "sm", "margin": "xl"}
        ])
        
        return {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": contents, "backgroundColor": FlexDesign.BG, "paddingAll": "24px"}}
    
    @staticmethod
    def correct_answer(player_name, points):
        """إجابة صحيحة"""
        return {
            "type": "bubble",
            "body": {"type": "box", "layout": "vertical", "contents": [
                {"type": "box", "layout": "vertical", "contents": [
                    {"type": "text", "text": "✓", "size": "4xl", "color": FlexDesign.ACCENT, "align": "center", "weight": "bold"}
                ], "width": "80px", "height": "80px", "backgroundColor": FlexDesign.BG, "cornerRadius": "full", "justifyContent": "center", "offsetStart": "50%", "position": "relative"},
                {"type": "text", "text": "إجابة صحيحة!", "weight": "bold", "size": "xl", "color": FlexDesign.TEXT_PRIMARY, "align": "center", "margin": "xl"},
                {"type": "text", "text": player_name, "size": "md", "color": FlexDesign.TEXT_SECONDARY, "align": "center", "margin": "sm"},
                {"type": "separator", "margin": "xl"},
                {"type": "box", "layout": "horizontal", "contents": [
                    {"type": "text", "text": "النقاط", "size": "sm", "color": FlexDesign.TEXT_SECONDARY, "flex": 1},
                    {"type": "text", "text": f"+{points}", "size": "xxl", "color": FlexDesign.ACCENT, "flex": 1, "align": "end", "weight": "bold"}
                ], "margin": "xl"}
            ], "backgroundColor": FlexDesign.BG, "paddingAll": "28px"}
        }
    
    @staticmethod
    def leaderboard(leaders):
        """لوحة الصدارة"""
        players = []
        for i, (name, score) in enumerate(leaders, 1):
            is_top = i <= 3
            players.append({"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": str(i), "size": "sm", "color": FlexDesign.ACCENT if is_top else FlexDesign.TEXT_PRIMARY, "align": "center", "weight": "bold", "flex": 0},
                {"type": "text", "text": name, "size": "md" if is_top else "sm", "color": FlexDesign.TEXT_PRIMARY, "flex": 3, "margin": "md", "weight": "bold" if is_top else "regular"},
                {"type": "text", "text": f"{score} نقطة", "size": "md" if is_top else "sm", "color": FlexDesign.ACCENT if is_top else FlexDesign.TEXT_SECONDARY, "flex": 2, "align": "end", "weight": "bold" if is_top else "regular"}
            ], "spacing": "md", "paddingAll": "12px", "backgroundColor": FlexDesign.BG, "cornerRadius": "12px", "margin": "sm" if i > 1 else "none"})
        
        return {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": [
            {"type": "text", "text": "🏆 لوحة الصدارة", "weight": "bold", "size": "xl", "color": FlexDesign.TEXT_PRIMARY, "align": "center"},
            {"type": "separator", "margin": "lg"},
            {"type": "box", "layout": "vertical", "contents": players, "margin": "lg"}
        ], "backgroundColor": FlexDesign.BG, "paddingAll": "24px"}}
    
    @staticmethod
    def game_over(winner_name, winner_score, all_scores):
        """نهاية اللعبة"""
        sorted_players = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        players = []
        for i, (name, score) in enumerate(sorted_players, 1):
            is_winner = i == 1
            players.append({"type": "box", "layout": "horizontal", "contents": [
                {"type": "text", "text": str(i), "size": "sm", "color": FlexDesign.ACCENT if is_winner else FlexDesign.TEXT_PRIMARY, "align": "center", "weight": "bold", "flex": 0},
                {"type": "text", "text": name, "size": "md" if is_winner else "sm", "color": FlexDesign.TEXT_PRIMARY, "flex": 3, "margin": "md", "weight": "bold" if is_winner else "regular"},
                {"type": "text", "text": f"{score} نقطة", "size": "md" if is_winner else "sm", "color": FlexDesign.ACCENT if is_winner else FlexDesign.TEXT_SECONDARY, "flex": 2, "align": "end", "weight": "bold" if is_winner else "regular"}
            ], "spacing": "md", "paddingAll": "12px", "backgroundColor": FlexDesign.BG, "cornerRadius": "12px", "margin": "sm" if i > 1 else "none"})
        
        return {"type": "bubble", "size": "mega", "body": {"type": "box", "layout": "vertical", "contents": [
            {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "👑", "size": "4xl", "align": "center"}], "width": "100px", "height": "100px", "backgroundColor": "#667eea", "cornerRadius": "full", "justifyContent": "center", "offsetStart": "50%", "position": "relative"},
            {"type": "text", "text": "انتهت اللعبة", "size": "xl", "color": FlexDesign.TEXT_PRIMARY, "align": "center", "weight": "bold", "margin": "xl"},
            {"type": "separator", "margin": "lg"},
            {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": "الفائز", "size": "xs", "color": FlexDesign.TEXT_SECONDARY, "align": "center"},
                {"type": "text", "text": winner_name, "size": "xxl", "color": FlexDesign.TEXT_PRIMARY, "align": "center", "weight": "bold", "margin": "sm"},
                {"type": "text", "text": f"{winner_score} نقطة", "size": "lg", "color": "#667eea", "align": "center", "weight": "bold", "margin": "sm"}
            ], "backgroundColor": FlexDesign.BG, "cornerRadius": "16px", "paddingAll": "20px", "margin": "lg"},
            {"type": "text", "text": "النتائج النهائية", "size": "md", "color": FlexDesign.TEXT_PRIMARY, "weight": "bold", "margin": "lg"},
            {"type": "box", "layout": "vertical", "contents": players, "margin": "md"},
            {"type": "button", "action": {"type": "message", "label": "لعبة جديدة", "text": "القائمة"}, "style": "primary", "height": "sm", "margin": "xl"}
        ], "backgroundColor": FlexDesign.BG, "paddingAll": "24px"}}
