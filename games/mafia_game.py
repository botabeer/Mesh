"""
لعبة المافيا - Bot Mesh v22.2 PRO 3D
Created by: Abeer Aldosari © 2025
للعب في المجموعات فقط | نقاط للفائزين
"""

from games.base_game import BaseGame
import random
from typing import Dict, Any, Optional, List


class MafiaGame(BaseGame):
    """لعبة المافيا - للمجموعات"""

    def __init__(self, line_bot_api):
        super().__init__(line_bot_api, questions_count=1)
        self.game_name = "مافيا"
        self.supports_hint = False
        self.supports_reveal = False
        
        self.min_players = 4
        self.max_players = 20
        
        self.players = {}
        self.roles = {}
        self.alive_players = set()
        self.dead_players = set()
        
        self.mafia_members = set()
        self.civilians = set()
        self.doctor = None
        self.detective = None
        
        self.game_phase = "waiting"
        self.current_round = 0
        
        self.night_votes = {}
        self.day_votes = {}
        
        self.protected_player = None
        self.investigated_player = None

    def start_game(self):
        """بدء اللعبة"""
        self.game_active = True
        self.game_phase = "joining"
        self.current_round = 0
        return self.get_joining_screen()

    def get_joining_screen(self):
        """شاشة الانضمام"""
        c = self.get_theme_colors()
        
        joined_count = len(self.players)
        
        contents = [
            {
                "type": "text",
                "text": "لعبة المافيا",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "شرح اللعبة",
                        "size": "md",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "لعبة جماعية تنقسم فيها الأدوار بين مافيا ومدنيين",
                        "size": "xs",
                        "color": c["text2"],
                        "wrap": True,
                        "margin": "sm"
                    },
                    {"type": "separator", "margin": "md", "color": c["border"]},
                    {
                        "type": "text",
                        "text": "الأدوار",
                        "size": "sm",
                        "weight": "bold",
                        "color": c["text"],
                        "margin": "md"
                    },
                    {
                        "type": "text",
                        "text": "مافيا: يحاولون قتل المدنيين ليلاً",
                        "size": "xs",
                        "color": c["error"],
                        "wrap": True,
                        "margin": "xs"
                    },
                    {
                        "type": "text",
                        "text": "مدنيين: يصوتون لطرد المشتبهين نهاراً",
                        "size": "xs",
                        "color": c["info"],
                        "wrap": True,
                        "margin": "xs"
                    },
                    {
                        "type": "text",
                        "text": "دكتور: ينقذ لاعب واحد كل ليلة",
                        "size": "xs",
                        "color": c["success"],
                        "wrap": True,
                        "margin": "xs"
                    },
                    {
                        "type": "text",
                        "text": "محقق: يكشف دور لاعب كل ليلة",
                        "size": "xs",
                        "color": c["warning"],
                        "wrap": True,
                        "margin": "xs"
                    }
                ],
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "paddingAll": "16px",
                "borderWidth": "1px",
                "borderColor": c["border"],
                "margin": "md"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "اللاعبون المنضمون",
                                "size": "sm",
                                "weight": "bold",
                                "color": c["text"],
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": f"{joined_count}/{self.max_players}",
                                "size": "lg",
                                "weight": "bold",
                                "color": c["primary"],
                                "flex": 0
                            }
                        ]
                    },
                    {
                        "type": "text",
                        "text": f"الحد الأدنى: {self.min_players} لاعبين",
                        "size": "xs",
                        "color": c["text3"],
                        "margin": "sm"
                    }
                ],
                "backgroundColor": c["info_bg"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "margin": "lg"
            },
            {
                "type": "text",
                "text": "اكتب 'انضم' للانضمام\nاكتب 'ابدأ' لبدء اللعبة",
                "size": "sm",
                "color": c["text2"],
                "align": "center",
                "wrap": True,
                "margin": "lg"
            }
        ]
        
        return self._create_flex_with_buttons(
            self.game_name,
            {
                "type": "bubble",
                "size": "mega",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents,
                    "paddingAll": "24px",
                    "backgroundColor": c["bg"]
                }
            }
        )

    def assign_roles(self):
        """توزيع الأدوار"""
        player_list = list(self.players.keys())
        random.shuffle(player_list)
        
        num_players = len(player_list)
        num_mafia = max(1, num_players // 4)
        
        self.mafia_members = set(player_list[:num_mafia])
        remaining = player_list[num_mafia:]
        
        if len(remaining) >= 2:
            self.doctor = remaining[0]
            self.detective = remaining[1]
            self.civilians = set(remaining[2:])
        else:
            self.civilians = set(remaining)
        
        for player_id in self.mafia_members:
            self.roles[player_id] = "مافيا"
        
        if self.doctor:
            self.roles[self.doctor] = "دكتور"
        if self.detective:
            self.roles[self.detective] = "محقق"
        
        for player_id in self.civilians:
            self.roles[player_id] = "مدني"
        
        self.alive_players = set(player_list)

    def get_night_phase(self):
        """مرحلة الليل"""
        c = self.get_theme_colors()
        
        contents = [
            {
                "type": "text",
                "text": f"الليلة رقم {self.current_round}",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "حان وقت الليل",
                        "size": "lg",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "المافيا: اختر ضحية\nالدكتور: احمِ لاعباً\nالمحقق: تحقق من لاعب",
                        "size": "sm",
                        "color": c["text2"],
                        "align": "center",
                        "wrap": True,
                        "margin": "md"
                    }
                ],
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "paddingAll": "16px",
                "borderWidth": "1px",
                "borderColor": c["border"],
                "margin": "md"
            },
            {
                "type": "text",
                "text": "أرسل اسم اللاعب في الخاص للبوت",
                "size": "xs",
                "color": c["warning"],
                "align": "center",
                "margin": "lg"
            }
        ]
        
        return self._create_flex_with_buttons(
            "الليل",
            {
                "type": "bubble",
                "size": "mega",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents,
                    "paddingAll": "24px",
                    "backgroundColor": c["bg"]
                }
            }
        )

    def get_day_phase(self):
        """مرحلة النهار"""
        c = self.get_theme_colors()
        
        alive_list = [self.players[pid] for pid in self.alive_players]
        
        contents = [
            {
                "type": "text",
                "text": f"النهار رقم {self.current_round}",
                "size": "xxl",
                "weight": "bold",
                "color": c["primary"],
                "align": "center"
            },
            {"type": "separator", "margin": "lg", "color": c["border"]},
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "وقت التصويت",
                        "size": "lg",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": "صوت لطرد المشتبه به\nاكتب اسم اللاعب",
                        "size": "sm",
                        "color": c["text2"],
                        "align": "center",
                        "wrap": True,
                        "margin": "sm"
                    }
                ],
                "backgroundColor": c["card"],
                "cornerRadius": "12px",
                "paddingAll": "16px",
                "borderWidth": "1px",
                "borderColor": c["border"],
                "margin": "md"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "اللاعبون الأحياء",
                        "size": "sm",
                        "weight": "bold",
                        "color": c["text"],
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": " - ".join(alive_list[:10]),
                        "size": "xs",
                        "color": c["text2"],
                        "align": "center",
                        "wrap": True,
                        "margin": "sm"
                    }
                ],
                "backgroundColor": c["info_bg"],
                "cornerRadius": "12px",
                "paddingAll": "12px",
                "margin": "lg"
            }
        ]
        
        return self._create_flex_with_buttons(
            "النهار",
            {
                "type": "bubble",
                "size": "mega",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents,
                    "paddingAll": "24px",
                    "backgroundColor": c["bg"]
                }
            }
        )

    def check_win_condition(self) -> Optional[str]:
        """التحقق من شرط الفوز"""
        alive_mafia = len(self.mafia_members & self.alive_players)
        alive_civilians = len(self.alive_players) - alive_mafia
        
        if alive_mafia == 0:
            return "المدنيون"
        elif alive_mafia >= alive_civilians:
            return "المافيا"
        return None

    def check_answer(self, user_answer: str, user_id: str, display_name: str) -> Optional[Dict[str, Any]]:
        if not self.game_active:
            return None

        normalized = self.normalize_text(user_answer)

        if self.game_phase == "joining":
            if normalized in ["انضم", "join"]:
                if user_id not in self.players and len(self.players) < self.max_players:
                    self.players[user_id] = display_name
                    return {
                        "message": f"{display_name} انضم - العدد: {len(self.players)}",
                        "response": self._create_text_message(f"{display_name} انضم - العدد: {len(self.players)}"),
                        "points": 0
                    }
            
            elif normalized in ["ابدأ", "start", "بدا"]:
                if len(self.players) >= self.min_players:
                    self.assign_roles()
                    self.game_phase = "night"
                    self.current_round = 1
                    return {
                        "message": "بدأت اللعبة",
                        "response": self.get_night_phase(),
                        "points": 0
                    }
                else:
                    return {
                        "message": f"يحتاج {self.min_players - len(self.players)} لاعبين إضافيين",
                        "response": self._create_text_message(f"يحتاج {self.min_players - len(self.players)} لاعبين إضافيين"),
                        "points": 0
                    }

        return None

    def end_game(self) -> Dict[str, Any]:
        """إنهاء اللعبة"""
        winner = self.check_win_condition()
        self.game_active = False
        
        if winner == "المدنيون":
            winners = self.alive_players - self.mafia_members
            message = f"فاز المدنيون\n\nالفائزون:\n" + "\n".join([self.players[pid] for pid in winners])
        else:
            winners = self.mafia_members & self.alive_players
            message = f"فازت المافيا\n\nالفائزون:\n" + "\n".join([self.players[pid] for pid in winners])
        
        return {
            "game_over": True,
            "points": 1,
            "message": message
        }
