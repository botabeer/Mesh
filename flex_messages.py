"""
تصاميم Flex Messages بستايل Neumorphism Soft
تصاميم عصرية وجميلة بتأثير 3D ناعم
"""

class FlexMessages:
    """مكتبة التصاميم الحديثة"""
    
    # الألوان
    BG = '#E0E5EC'
    SHADOW_OUT = '9px 9px 16px rgba(163, 177, 198, 0.6), -9px -9px 16px rgba(255, 255, 255, 0.5)'
    SHADOW_IN = 'inset 5px 5px 10px rgba(163, 177, 198, 0.5), inset -5px -5px 10px rgba(255, 255, 255, 0.7)'
    GRADIENT = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    TEXT_PRIMARY = '#4A5568'
    TEXT_SECONDARY = '#A3B1C6'
    
    @staticmethod
    def main_menu():
        """القائمة الرئيسية - تصميم Neumorphism"""
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Neumorphism Soft 🎮",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center",
                        "color": FlexMessages.TEXT_PRIMARY
                    },
                    {
                        "type": "text",
                        "text": "تأثير 3D - عمق ناعم",
                        "size": "sm",
                        "align": "center",
                        "color": FlexMessages.TEXT_SECONDARY,
                        "margin": "sm"
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    # الألعاب
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            FlexMessages._game_button("🔤", "تكوين الكلمات", "letters"),
                            FlexMessages._game_button("⚡", "أسرع إجابة", "fast"),
                            FlexMessages._game_button("🔀", "ترتيب الحروف", "scramble"),
                            FlexMessages._game_button("🔗", "سلسلة الكلمات", "chain"),
                            FlexMessages._game_button("🧠", "أسئلة ذكاء", "iq")
                        ],
                        "spacing": "md",
                        "margin": "xl"
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    # أزرار إضافية
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "🏆 الصدارة",
                                    "text": "الصدارة"
                                },
                                "style": "secondary",
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "👥 انضم",
                                    "text": "انضم"
                                },
                                "style": "primary",
                                "height": "sm"
                            }
                        ],
                        "spacing": "sm",
                        "margin": "xl"
                    }
                ],
                "backgroundColor": FlexMessages.BG,
                "paddingAll": "24px"
            }
        }
    
    @staticmethod
    def _game_button(emoji, name, game_id):
        """زر لعبة بتصميم Neumorphism"""
        return {
            "type": "box",
            "layout": "horizontal",
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
                    "color": FlexMessages.TEXT_PRIMARY,
                    "flex": 1,
                    "margin": "md",
                    "weight": "bold"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "▶",
                        "text": game_id
                    },
                    "style": "primary",
                    "height": "sm",
                    "flex": 0
                }
            ],
            "spacing": "md",
            "paddingAll": "12px",
            "cornerRadius": "16px",
            "backgroundColor": FlexMessages.BG
        }
    
    @staticmethod
    def game_question(game_name, question, letters=None, round_num=1, total_rounds=5):
        """شاشة السؤال - Neumorphism"""
        contents = [
            # رأس اللعبة
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"■ {game_name}",
                        "weight": "bold",
                        "size": "lg",
                        "color": FlexMessages.TEXT_PRIMARY,
                        "flex": 1
                    },
                    {
                        "type": "text",
                        "text": f"سؤال {round_num} من {total_rounds}",
                        "size": "sm",
                        "color": FlexMessages.TEXT_SECONDARY,
                        "align": "end"
                    }
                ]
            },
            {
                "type": "separator",
                "margin": "lg"
            }
        ]
        
        # الحروف (إذا كانت موجودة)
        if letters:
            letter_boxes = []
            for letter in letters:
                letter_boxes.append({
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": letter,
                            "size": "xl",
                            "color": "#667eea",
                            "align": "center",
                            "weight": "bold"
                        }
                    ],
                    "width": "50px",
                    "height": "50px",
                    "backgroundColor": FlexMessages.BG,
                    "cornerRadius": "12px",
                    "justifyContent": "center"
                })
            
            contents.append({
                "type": "box",
                "layout": "horizontal",
                "contents": letter_boxes,
                "spacing": "sm",
                "margin": "xl",
                "justifyContent": "center",
                "paddingAll": "16px",
                "cornerRadius": "16px",
                "backgroundColor": FlexMessages.BG
            })
        
        # السؤال
        contents.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": question,
                    "size": "md",
                    "color": FlexMessages.TEXT_PRIMARY,
                    "align": "center",
                    "wrap": True
                }
            ],
            "paddingAll": "16px",
            "cornerRadius": "12px",
            "backgroundColor": FlexMessages.BG,
            "margin": "lg"
        })
        
        # الأزرار
        contents.append({
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "الحل",
                        "text": "الحل"
                    },
                    "style": "secondary",
                    "height": "sm"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "message",
                        "label": "تلميح",
                        "text": "تلميح"
                    },
                    "style": "primary",
                    "height": "sm"
                }
            ],
            "spacing": "sm",
            "margin": "xl"
        })
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": contents,
                "backgroundColor": FlexMessages.BG,
                "paddingAll": "24px"
            }
        }
    
    @staticmethod
    def correct_answer(player_name, points):
        """إجابة صحيحة - Neumorphism"""
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # أيقونة النجاح
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "✓",
                                "size": "4xl",
                                "color": "#667eea",
                                "align": "center",
                                "weight": "bold"
                            }
                        ],
                        "width": "80px",
                        "height": "80px",
                        "backgroundColor": FlexMessages.BG,
                        "cornerRadius": "full",
                        "justifyContent": "center",
                        "offsetStart": "50%",
                        "position": "relative"
                    },
                    {
                        "type": "text",
                        "text": "إجابة صحيحة!",
                        "weight": "bold",
                        "size": "xl",
                        "color": FlexMessages.TEXT_PRIMARY,
                        "align": "center",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": player_name,
                        "size": "md",
                        "color": FlexMessages.TEXT_SECONDARY,
                        "align": "center",
                        "margin": "sm"
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": "النقاط",
                                "size": "sm",
                                "color": FlexMessages.TEXT_SECONDARY,
                                "flex": 1
                            },
                            {
                                "type": "text",
                                "text": f"+{points}",
                                "size": "xxl",
                                "color": "#667eea",
                                "flex": 1,
                                "align": "end",
                                "weight": "bold"
                            }
                        ],
                        "margin": "xl"
                    }
                ],
                "backgroundColor": FlexMessages.BG,
                "paddingAll": "28px"
            }
        }
    
    @staticmethod
    def game_over(winner_name, winner_score, all_scores):
        """نهاية اللعبة - Neumorphism"""
        # ترتيب اللاعبين
        sorted_players = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
        
        # قائمة اللاعبين
        players_list = []
        for i, (name, score) in enumerate(sorted_players[:5], 1):
            is_winner = (i == 1)
            
            players_list.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": str(i),
                        "size": "sm",
                        "color": "#667eea" if is_winner else FlexMessages.TEXT_PRIMARY,
                        "align": "center",
                        "weight": "bold",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": name,
                        "size": "md" if is_winner else "sm",
                        "color": FlexMessages.TEXT_PRIMARY,
                        "flex": 3,
                        "margin": "md",
                        "weight": "bold" if is_winner else "regular"
                    },
                    {
                        "type": "text",
                        "text": f"{score} نقطة",
                        "size": "md" if is_winner else "sm",
                        "color": "#667eea" if is_winner else FlexMessages.TEXT_SECONDARY,
                        "flex": 2,
                        "align": "end",
                        "weight": "bold" if is_winner else "regular"
                    }
                ],
                "spacing": "md",
                "paddingAll": "12px",
                "backgroundColor": FlexMessages.BG,
                "cornerRadius": "12px",
                "margin": "sm" if i > 1 else "none"
            })
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # التاج
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "👑",
                                "size": "4xl",
                                "align": "center"
                            }
                        ],
                        "width": "100px",
                        "height": "100px",
                        "backgroundColor": "#667eea",
                        "cornerRadius": "full",
                        "justifyContent": "center",
                        "offsetStart": "50%",
                        "position": "relative"
                    },
                    {
                        "type": "text",
                        "text": "انتهت اللعبة",
                        "size": "xl",
                        "color": FlexMessages.TEXT_PRIMARY,
                        "align": "center",
                        "weight": "bold",
                        "margin": "xl"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                    # بطاقة الفائز
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الفائز",
                                "size": "xs",
                                "color": FlexMessages.TEXT_SECONDARY,
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": winner_name,
                                "size": "xxl",
                                "color": FlexMessages.TEXT_PRIMARY,
                                "align": "center",
                                "weight": "bold",
                                "margin": "sm"
                            },
                            {
                                "type": "text",
                                "text": f"{winner_score} نقطة",
                                "size": "lg",
                                "color": "#667eea",
                                "align": "center",
                                "weight": "bold",
                                "margin": "sm"
                            }
                        ],
                        "backgroundColor": FlexMessages.BG,
                        "cornerRadius": "16px",
                        "paddingAll": "20px",
                        "margin": "lg"
                    },
                    {
                        "type": "separator",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": "النتائج النهائية",
                        "size": "md",
                        "color": FlexMessages.TEXT_PRIMARY,
                        "weight": "bold",
                        "margin": "lg"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": players_list,
                        "margin": "md"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "لعبة جديدة",
                            "text": "القائمة"
                        },
                        "style": "primary",
                        "height": "sm",
                        "margin": "xl"
                    }
                ],
                "backgroundColor": FlexMessages.BG,
                "paddingAll": "24px"
            }
        }
