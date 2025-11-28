# games/base_game.py
"""
Bot Mesh v7.3 - Base Game System EXTENDED
- Adds team-mode, per-round timer, persistent leaderboard hooks
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from linebot.v3.messaging import FlexMessage, FlexContainer, TextMessage
import re
import threading
import sqlite3
import os

class BaseGame:
    """BaseGame extended with team-mode and timer"""
    game_name = "لعبة"
    game_icon = ""
    supports_hint = True
    supports_reveal = True

    # (THEMES kept unchanged - omitted here for brevity; reuse your THEMES)
    THEMES = {
        # ... copy your THEMES dict here unchanged ...
    }

    def __init__(self, line_bot_api=None, questions_count: int = 5):
        self.line_bot_api = line_bot_api
        self.questions_count = questions_count
        self.current_question = 0
        self.current_answer = None
        self.previous_question = None
        self.previous_answer = None
        self.scores: Dict[str, Dict[str, Any]] = {}  # user_id -> {name, score}
        self.answered_users = set()
        self.game_active = False
        self.game_start_time: Optional[datetime] = None
        self.current_theme = "أبيض"

        # --- Team mode ---
        self.team_mode = False            # if True, scoring is per-team
        self.teams = {"A": {"name": "فريق 1", "members": set(), "score": 0},
                      "B": {"name": "فريق 2", "members": set(), "score": 0}}
        self.player_team: Dict[str, str] = {}  # user_id -> "A"/"B"

        # --- Timer ---
        self.round_duration = None        # seconds or None
        self.round_end_time: Optional[datetime] = None
        self._timer_thread = None
        self._timer_lock = threading.Lock()
        self.on_timer_expire = None       # optional callback

    # ---------------- Team management ----------------
    def enable_team_mode(self, enable: bool = True):
        self.team_mode = enable

    def join_team(self, user_id: str, display_name: str, team_key: str) -> bool:
        """join user to team_key = 'A' or 'B'"""
        if team_key not in self.teams:
            return False
        # remove from other team
        prev = self.player_team.get(user_id)
        if prev:
            self.teams[prev]["members"].discard(user_id)
        self.teams[team_key]["members"].add(user_id)
        self.player_team[user_id] = team_key
        # ensure user present in scores map for display
        if user_id not in self.scores:
            self.scores[user_id] = {"name": display_name, "score": 0}
        return True

    def leave_team(self, user_id: str):
        prev = self.player_team.get(user_id)
        if prev:
            self.teams[prev]["members"].discard(user_id)
        self.player_team.pop(user_id, None)

    def is_user_in_team(self, user_id: str) -> bool:
        return user_id in self.player_team

    def get_user_team(self, user_id: str) -> Optional[str]:
        return self.player_team.get(user_id)

    # ---------------- Timer management ----------------
    def start_round_timer(self, seconds: int, on_expire_callback=None):
        """Start per-round timer (non-blocking)"""
        with self._timer_lock:
            self.round_duration = seconds
            self.round_end_time = datetime.now() + timedelta(seconds=seconds)
            self.on_timer_expire = on_expire_callback
            if self._timer_thread and self._timer_thread.is_alive():
                # existing timer will check end time
                return
            self._timer_thread = threading.Thread(target=self._timer_worker, daemon=True)
            self._timer_thread.start()

    def cancel_round_timer(self):
        with self._timer_lock:
            self.round_end_time = None
            self.round_duration = None
            self.on_timer_expire = None

    def _timer_worker(self):
        while True:
            with self._timer_lock:
                if not self.round_end_time:
                    return
                now = datetime.now()
                if now >= self.round_end_time:
                    cb = self.on_timer_expire
                    # clear before calling to avoid re-entrance
                    self.round_end_time = None
                    self.round_duration = None
                    self.on_timer_expire = None
                    if cb:
                        try:
                            cb()
                        except Exception:
                            pass
                    return
            # sleep small interval
            import time
            time.sleep(0.5)

    def get_time_left(self) -> Optional[int]:
        if not self.round_end_time:
            return None
        left = (self.round_end_time - datetime.now()).total_seconds()
        return max(0, int(left))

    # ---------------- Scoring ----------------
    def add_score(self, user_id: str, display_name: str, points: int = 1) -> int:
        """
        Adds points. If team_mode: adds to team and optionally to player record.
        Returns points actually awarded to the player (0 if already answered).
        """
        # if user already answered this round -> ignore
        if user_id in self.answered_users:
            return 0

        # Ensure basic user record
        if user_id not in self.scores:
            self.scores[user_id] = {"name": display_name, "score": 0}

        if self.team_mode:
            team = self.get_user_team(user_id)
            if not team:
                # user not joined -> ignore (in team mode only joined users count)
                return 0
            # add to team aggregate
            self.teams[team]["score"] += points
            # optionally add to individual (still store)
            self.scores[user_id]["score"] += points
        else:
            # normal single-player scoring
            self.scores[user_id]["score"] += points

        # mark as answered this round
        self.answered_users.add(user_id)
        return points

    # ---------------- lifecycle ----------------
    def start_game(self):
        """Start game (overrides)"""
        self.current_question = 0
        self.scores.clear()
        self.answered_users.clear()
        self.previous_question = None
        self.previous_answer = None
        self.game_active = True
        self.game_start_time = datetime.now()
        # reset teams if team mode
        for k in self.teams:
            self.teams[k]["members"].clear()
            self.teams[k]["score"] = 0
        self.player_team.clear()
        return self.get_question()

    def end_game(self) -> Dict[str, Any]:
        """End game and return winner info"""
        self.game_active = False
        # determine winner: in team mode, compare teams. else best player
        if self.team_mode:
            a = self.teams["A"]["score"]
            b = self.teams["B"]["score"]
            return {"game_over": True, "team_scores": {"A": a, "B": b}, "message": f"انتهت اللعبة • {self.teams['A']['name']} {a} - {b} {self.teams['B']['name']}"}
        else:
            if not self.scores:
                return {"game_over": True, "points": 0, "message": "انتهت اللعبة"}
            max_score = max(s["score"] for s in self.scores.values())
            return {"game_over": True, "points": max_score, "message": f"انتهت اللعبة • النقاط: {max_score}"}

    # ---------------- Helpers (unchanged) ----------------
    def normalize_text(self, text: str) -> str:
        if not text:
            return ""
        text = text.strip().lower()
        replacements = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي', 'ة': 'ه', 'ؤ': 'و', 'ئ': 'ي'}
        for old, new in replacements.items():
            text = text.replace(old, new)
        return re.sub(r'[\u064B-\u065F\u0670]', '', text)

    def _create_text_message(self, text: str):
        return TextMessage(text=text)

    def _create_flex_with_buttons(self, alt_text: str, flex_content: dict):
        return FlexMessage(alt_text=alt_text, contents=FlexContainer.from_dict(flex_content))

    # you can reuse your original build_question_flex method (copy it here)
    # ...
