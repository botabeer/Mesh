class FlexMessages:
    BG = "#E0E5EC"
    TEXT_PRIMARY = "#4A5568"
    TEXT_SECONDARY = "#A3B1C6"
    ACCENT = "#667eea"

    @staticmethod
    def main_menu():
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "20px",
                "backgroundColor": FlexMessages.BG,
                "contents": [
                    {
                        "type": "text",
                        "text": "القائمة الرئيسية",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": FlexMessages.TEXT_PRIMARY
                    },
                    {
                        "type": "text",
                        "text": "اختر لعبتك 🎮",
                        "size": "sm",
                        "align": "center",
                        "color": FlexMessages.TEXT_SECONDARY,
                        "margin": "sm"
                    },
                    {"type": "separator", "margin": "lg"},

                    # ألعاب
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "margin": "lg",
                        "contents": [
                            FlexMessages._game_button("🔤", "تكوين الكلمات", "letters"),
                            FlexMessages._game_button("⚡", "أسرع إجابة", "fast"),
                            FlexMessages._game_button("🔀", "ترتيب الحروف", "scramble"),
                            FlexMessages._game_button("🔗", "سلسلة الكلمات", "chain"),
                            FlexMessages._game_button("🧠", "أسئلة ذكاء", "iq"),
                        ]
                    },

                    {"type": "separator", "margin": "xl"},

                    # أزرار إضافية
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "margin": "lg",
                        "contents": [
                            {
                                "type": "button",
                                "style": "secondary",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "🏆 الصدارة",
                                    "text": "الصدارة"
                                }
                            },
                            {
                                "type": "button",
                                "style": "primary",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "👥 انضم",
                                    "text": "انضم"
                                }
                            }
                        ]
                    }
                ]
            }
        }

    @staticmethod
    def _game_button(emoji, name, game_id):
        return {
            "type": "box",
            "layout": "horizontal",
            "cornerRadius": "10px",
            "paddingAll": "12px",
            "backgroundColor": FlexMessages.BG,
            "contents": [
                {
                    "type": "text",
                    "text": emoji,
                    "size": "xl",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": name,
                    "size": "md",
                    "flex": 1,
                    "margin": "md",
                    "weight": "bold",
                    "color": FlexMessages.TEXT_PRIMARY
                },
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "flex": 0,
                    "action": {"type": "message", "label": "▶", "text": game_id}
                }
            ]
        }

    @staticmethod
    def game_question(game_name, question, letters=None, round_num=1, total_rounds=5):
        contents = [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"■ {game_name}",
                        "weight": "bold",
                        "size": "lg",
                        "flex": 1,
                        "color": FlexMessages.TEXT_PRIMARY
                    },
                    {
                        "type": "text",
                        "text": f"سؤال {round_num}/{total_rounds}",
                        "size": "sm",
                        "align": "end",
                        "color": FlexMessages.TEXT_SECONDARY
                    }
                ]
            },
            {"type": "separator", "margin": "lg"},
        ]

        # الحروف
        if letters:
            box_letters = []
            for l in letters:
                box_letters.append({
                    "type": "box",
                    "layout": "vertical",
                    "width": "45px",
                    "height": "45px",
                    "cornerRadius": "10px",
                    "backgroundColor": FlexMessages.BG,
                    "justifyContent": "center",
                    "contents": [
                        {
                            "type": "text",
                            "text": l,
                            "align": "center",
                            "color": FlexMessages.ACCENT,
                            "weight": "bold",
                            "size": "lg"
                        }
                    ]
                })

            contents.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "margin": "lg",
                "justifyContent": "center",
                "contents": box_letters
            })

        # السؤال
        contents.append({
            "type": "box",
            "layout": "vertical",
            "cornerRadius": "12px",
            "backgroundColor": FlexMessages.BG,
            "paddingAll": "16px",
            "margin": "lg",
            "contents": [
                {
                    "type": "text",
                    "text": question,
                    "align": "center",
                    "wrap": True,
                    "color": FlexMessages.TEXT_PRIMARY
                }
            ]
        })

        # أزرار
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "margin": "xl",
            "contents": [
                {
                    "type": "button",
                    "style": "secondary",
                    "height": "sm",
                    "action": {"type": "message", "label": "الحل", "text": "الحل"}
                },
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "action": {"type": "message", "label": "تلميح", "text": "تلميح"}
                }
            ]
        })

        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "20px",
                "backgroundColor": FlexMessages.BG,
                "contents": contents
            }
        }

    @staticmethod
    def correct_answer(player_name, points):
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "20px",
                "backgroundColor": FlexMessages.BG,
                "contents": [
                    {
                        "type": "text",
                        "text": "✓",
                        "size": "xxl",
                        "align": "center",
                        "weight": "bold",
                        "color": FlexMessages.ACCENT
                    },
                    {
                        "type": "text",
                        "text": "إجابة صحيحة!",
                        "size": "lg",
                        "align": "center",
                        "weight": "bold",
                        "margin": "md",
                        "color": FlexMessages.TEXT_PRIMARY
                    },
                    {
                        "type": "text",
                        "text": player_name,
                        "align": "center",
                        "color": FlexMessages.TEXT_SECONDARY
                    },
                    {"type": "separator", "margin": "lg"},
                    {
                        "type": "text",
                        "text": f"+{points} نقطة",
                        "size": "xl",
                        "align": "center",
                        "weight": "bold",
                        "color": FlexMessages.ACCENT,
                        "margin": "lg"
                    }
                ]
            }
        }

    @staticmethod
    def game_over(winner_name, winner_score, all_scores):
        players_sorted = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)

        rows = []
        for i, (name, score) in enumerate(players_sorted[:5], start=1):
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "paddingAll": "10px",
                "cornerRadius": "10px",
                "backgroundColor": FlexMessages.BG,
                "contents": [
                    {
                        "type": "text",
                        "text": str(i),
                        "size": "sm",
                        "weight": "bold",
                        "color": FlexMessages.ACCENT if i == 1 else FlexMessages.TEXT_PRIMARY,
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": name,
                        "size": "md",
                        "flex": 2,
                        "color": FlexMessages.TEXT_PRIMARY
                    },
                    {
                        "type": "text",
                        "text": f"{score} نقطة",
                        "size": "sm",
                        "align": "end",
                        "flex": 1,
                        "color": FlexMessages.ACCENT if i == 1 else FlexMessages.TEXT_SECONDARY
                    }
                ]
            })

        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "paddingAll": "20px",
                "backgroundColor": FlexMessages.BG,
                "contents": [
                    {
                        "type": "text",
                        "text": "👑 الفائز",
                        "align": "center",
                        "size": "xl",
                        "weight": "bold",
                        "color": FlexMessages.ACCENT
                    },
                    {
                        "type": "text",
                        "text": winner_name,
                        "align": "center",
                        "size": "lg",
                        "color": FlexMessages.TEXT_PRIMARY,
                        "margin": "sm",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": f"{winner_score} نقطة",
                        "align": "center",
                        "size": "md",
                        "color": FlexMessages.TEXT_SECONDARY
                    },
                    {"type": "separator", "margin": "lg"},
                    {
                        "type": "text",
                        "text": "النتائج النهائية",
                        "weight": "bold",
                        "size": "md",
                        "color": FlexMessages.TEXT_PRIMARY,
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": rows
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "margin": "lg",
                        "action": {"type": "message", "label": "لعبة جديدة", "text": "القائمة"}
                    }
                ]
            }
        }
