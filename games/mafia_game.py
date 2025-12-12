from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional

class MafiaGame(BaseGame):
    """لعبة المافيا الجماعية"""
    
    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = "مافيا"
        self.supports_hint = False
        self.supports_reveal = False
        
        self.min_players = 4
        self.max_players = 20
        
        # اللاعبون والأدوار
        self.players = {}  # {user_id: display_name}
        self.roles = {}  # {user_id: role}
        self.alive_players = set()
        self.dead_players = set()
        
        # الفرق
        self.mafia_members = set()
        self.civilians = set()
        self.doctor = None
        self.detective = None
        
        # حالة اللعبة
        self.game_phase = "waiting"  # waiting, joining, night, day
        self.current_round = 0
        
        # التصويت
        self.night_votes = {}
        self.day_votes = {}
    
    def start_game(self):
        """بدء مرحلة الانضمام"""
        self.game_active = True
        self.game_phase = "joining"
        self.current_round = 0
        self.players.clear()
        
        return self.build_text_message(
            f"{self.game_name}\n\n"
            "مرحلة الانضمام\n\n"
            f"الحد الادنى: {self.min_players} لاعبين\n"
            f"الحد الاقصى: {self.max_players} لاعب\n\n"
            "اكتب: انضم - للانضمام\n"
            "اكتب: ابدأ - لبدء اللعبة"
        )
    
    def join_player(self, user_id: str, display_name: str) -> str:
        """انضمام لاعب"""
        if len(self.players) >= self.max_players:
            return "اكتمل العدد"
        
        if user_id in self.players:
            return "انت منضم بالفعل"
        
        self.players[user_id] = display_name
        return f"{display_name} انضم - العدد: {len(self.players)}/{self.max_players}"
    
    def assign_roles(self):
        """توزيع الأدوار"""
        player_list = list(self.players.keys())
        random.shuffle(player_list)
        
        num_players = len(player_list)
        num_mafia = max(1, num_players // 4)  # 25% مافيا
        
        # توزيع المافيا
        self.mafia_members = set(player_list[:num_mafia])
        remaining = player_list[num_mafia:]
        
        # توزيع الأدوار الخاصة
        if len(remaining) >= 2:
            self.doctor = remaining[0]
            self.detective = remaining[1]
            self.civilians = set(remaining[2:])
        else:
            self.civilians = set(remaining)
        
        # تسجيل الأدوار
        for player_id in self.mafia_members:
            self.roles[player_id] = "مافيا"
        
        if self.doctor:
            self.roles[self.doctor] = "دكتور"
        
        if self.detective:
            self.roles[self.detective] = "محقق"
        
        for player_id in self.civilians:
            self.roles[player_id] = "مواطن"
        
        self.alive_players = set(player_list)
    
    def start_night_phase(self):
        """بدء مرحلة الليل"""
        self.game_phase = "night"
        self.current_round += 1
        self.night_votes.clear()
        
        return self.build_text_message(
            f"الليلة رقم {self.current_round}\n\n"
            "حان وقت الليل\n"
            "الجميع ينام الان\n\n"
            "المافيا: اختاروا ضحية\n"
            "الدكتور: اختر من تحمي\n"
            "المحقق: اختر من تتحقق منه\n\n"
            "ارسل اسم اللاعب في الخاص للبوت"
        )
    
    def start_day_phase(self):
        """بدء مرحلة النهار"""
        self.game_phase = "day"
        self.day_votes.clear()
        
        alive_list = [self.players[pid] for pid in self.alive_players]
        alive_text = "\n- ".join(alive_list[:10])
        
        return self.build_text_message(
            f"النهار رقم {self.current_round}\n\n"
            "وقت التصويت\n"
            "صوت لطرد المشتبه به\n\n"
            f"اللاعبون الاحياء:\n- {alive_text}\n\n"
            "اكتب اسم اللاعب للتصويت"
        )
    
    def check_win_condition(self) -> Optional[str]:
        """التحقق من شرط الفوز"""
        alive_mafia = len(self.mafia_members & self.alive_players)
        alive_civilians = len(self.alive_players) - alive_mafia
        
        if alive_mafia == 0:
            return "المواطنون"
        elif alive_mafia >= alive_civilians:
            return "المافيا"
        
        return None
    
    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        """معالجة الأوامر"""
        if not self.game_active:
            return None
        
        text = user_answer.strip()
        normalized = self.normalize_text(text)
        
        # مرحلة الانضمام
        if self.game_phase == "joining":
            if normalized in ["انضم", "join"]:
                message = self.join_player(user_id, display_name)
                return {
                    'response': self.build_text_message(message),
                    'points': 0
                }
            
            elif normalized in ["ابدأ", "start", "بدا"]:
                if len(self.players) >= self.min_players:
                    self.assign_roles()
                    response = self.start_night_phase()
                    return {
                        'response': response,
                        'points': 0
                    }
                else:
                    needed = self.min_players - len(self.players)
                    return {
                        'response': self.build_text_message(f"يحتاج {needed} لاعبين اضافيين"),
                        'points': 0
                    }
        
        return None
    
    def end_game(self) -> Dict[str, Any]:
        """إنهاء اللعبة"""
        winner = self.check_win_condition()
        self.game_active = False
        
        if winner == "المواطنون":
            winners = self.alive_players - self.mafia_members
            message = f"فاز المواطنون\n\nالفائزون:\n"
            message += "\n".join([self.players[pid] for pid in winners])
        else:
            winners = self.mafia_members & self.alive_players
            message = f"فازت المافيا\n\nالفائزون:\n"
            message += "\n".join([self.players[pid] for pid in winners])
        
        return {
            "game_over": True,
            "points": 1,
            "message": message
        }
