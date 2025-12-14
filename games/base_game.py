# ===================================================================
# BaseGame - Unified Game Contract
# BOT MESH 2025
# ===================================================================

from typing import Optional, Dict, Any
from linebot.v3.messaging import TextMessage, FlexMessage

class BaseGame:
    """
    العقد الأساسي الذي يجب أن تلتزم به جميع الألعاب.
    أي لعبة لا تلتزم بهذا العقد ستُعتبر غير مستقرة.
    """

    # اسم اللعبة (يُستخدم في النقاط والإحصائيات)
    game_name: str = "base"

    # عدد اللاعبين (حالياً 1، قابل للتوسعة)
    max_players: int = 1

    def __init__(self, messaging_api):
        self.messaging_api = messaging_api
        self.db = None
        self.theme = "light"
        self.is_active = True

    # ---------------------------------------------------------------
    # Dependency Injection
    # ---------------------------------------------------------------

    def set_database(self, database) -> None:
        self.db = database

    def set_theme(self, theme: str) -> None:
        self.theme = theme or "light"

    # ---------------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------------

    def start_game(self):
        """
        يجب أن يبدأ اللعبة.
        المسموح إرجاعه:
        - TextMessage
        - FlexMessage
        """
        raise NotImplementedError("start_game() must be implemented")

    def check_answer(
        self,
        text: str,
        user_id: str,
        display_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        معالجة إدخال المستخدم.

        يجب أن تُرجع dict بالشكل التالي (أي مفتاح اختياري):
        {
            "message": str,
            "response": TextMessage | FlexMessage,
            "points": int,
            "game_over": bool
        }

        أو None إذا لا يوجد رد.
        """
        raise NotImplementedError("check_answer() must be implemented")

    # ---------------------------------------------------------------
    # Safety Helpers (تُستخدم من GameEngine)
    # ---------------------------------------------------------------

    @staticmethod
    def normalize_result(result: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        توحيد ناتج اللعبة لمنع الأخطاء.
        """
        if result is None:
            return {
                "message": "",
                "points": 0,
                "game_over": False
            }

        if not isinstance(result, dict):
            return {
                "message": "",
                "points": 0,
                "game_over": False
            }

        result.setdefault("message", "")
        result.setdefault("points", 0)
        result.setdefault("game_over", False)

        return result

    # ---------------------------------------------------------------
    # Optional Hooks
    # ---------------------------------------------------------------

    def on_game_over(self) -> None:
        """
        يُستدعى عند انتهاء اللعبة (اختياري).
        """
        self.is_active = False
