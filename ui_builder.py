# ============================================================================
# GLASS GAME PLAY UI - Unified for All Games
# ============================================================================

def build_game_play_window(
    game_name: str,
    question_text: str,
    progress: float,   # قيمة بين 0.0 و 1.0
    theme: str = DEFAULT_THEME
) -> FlexMessage:
    """🎮 شاشة اللعب الزجاجية الموحدة لكل الألعاب"""

    colors = _safe_get_colors(theme)
    bar_width = int(progress * 100)

    bubble = {
        "type": "bubble",
        "size": "mega",
        "styles": {
            "body": {
                "backgroundColor": colors["glass"],
                "borderColor": colors["border"],
                "borderWidth": "1px"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "18px",
            "contents": [

                # عنوان اللعبة
                {
                    "type": "text",
                    "text": f"🎮 {game_name}",
                    "size": "lg",
                    "weight": "bold",
                    "align": "center",
                    "color": colors["primary"]
                },

                {"type": "separator", "margin": "md"},

                # السؤال
                {
                    "type": "box",
                    "layout": "vertical",
                    "paddingAll": "16px",
                    "cornerRadius": "18px",
                    "backgroundColor": colors["card"],
                    "contents": [
                        {
                            "type": "text",
                            "text": question_text,
                            "size": "md",
                            "align": "center",
                            "wrap": True,
                            "color": colors["text"]
                        }
                    ]
                },

                # شريط التقدم الزجاجي
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "height": "10px",
                    "backgroundColor": colors["border"],
                    "cornerRadius": "10px",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "height": "10px",
                            "width": f"{bar_width}%",
                            "backgroundColor": colors["primary"],
                            "cornerRadius": "10px",
                            "contents": []
                        }
                    ]
                },

                # أزرار التحكم الثابتة
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "md",
                    "margin": "xl",
                    "contents": [

                        # إيقاف
                        {
                            "type": "button",
                            "style": "secondary",
                            "height": "sm",
                            "action": {
                                "type": "message",
                                "label": "⛔ إيقاف",
                                "text": "إيقاف"
                            }
                        },

                        # تخطي
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "color": colors["warning"],
                            "action": {
                                "type": "message",
                                "label": "⏭ تخطي",
                                "text": "تخطي"
                            }
                        },

                        # لمحة
                        {
                            "type": "button",
                            "style": "primary",
                            "height": "sm",
                            "color": colors["secondary"],
                            "action": {
                                "type": "message",
                                "label": "💡 لمحة",
                                "text": "لمح"
                            }
                        }
                    ]
                }
            ]
        }
    }

    return attach_quick_reply(
        FlexMessage(
            alt_text=f"🎮 {game_name}",
            contents=FlexContainer.from_dict(bubble)
        )
    )

# ============================================================================
# FEEDBACK EFFECTS (VIBRATION & FLASH SIMULATION)
# ============================================================================

def build_game_feedback_effect(
    message: str,
    success: bool,
    theme: str = DEFAULT_THEME
) -> FlexMessage:
    """💥 مؤثر وهمي (اهتزاز / وميض)"""

    colors = _safe_get_colors(theme)
    bg = colors["success"] if success else colors["error"]
    icon = "⚡" if success else "📳"

    bubble = {
        "type": "bubble",
        "size": "kilo",
        "styles": {
            "body": {
                "backgroundColor": bg
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "20px",
            "contents": [
                {"type": "text", "text": icon, "size": "xxl", "align": "center", "color": "#FFFFFF"},
                {
                    "type": "text",
                    "text": message,
                    "size": "lg",
                    "weight": "bold",
                    "align": "center",
                    "margin": "md",
                    "color": "#FFFFFF",
                    "wrap": True
                }
            ]
        }
    }

    return FlexMessage(
        alt_text=message,
        contents=FlexContainer.from_dict(bubble)
    )

# ============================================================================
# EXPORT ADDITIONS
# ============================================================================

__all__.extend([
    "build_game_play_window",
    "build_game_feedback_effect"
])
