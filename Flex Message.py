"""
ملف التصاميم - Neumorphism Soft Style
تصميم عصري بتأثير 3D ناعم وعمق بصري
متوافق مع LINE Bot Games
"""

class FlexStyles:
    """مكتبة التصاميم بأسلوب Neumorphism"""
    
    # الألوان - Neumorphism Soft
    COLORS = {
        'bg': '#E0E5EC',           # خلفية رئيسية
        'primary': '#C3E5E0',      # رمادي فاتح مزرق
        'secondary': '#DADE2',     # أكسنت (أزرق فاتح)
        'dark': '#A3B1C6',         # ظل داكن
        'light': '#FFFFFF',        # ظل فاتح
        'text': '#4A5568',         # نص رئيسي
        'text_light': '#718096',   # نص ثانوي
        'success': '#48BB78',      # نجاح
        'error': '#F56565'         # خطأ
    }
    
    @staticmethod
    def _neomorphism_box(bg_color='#E0E5EC'):
        """صندوق بتأثير Neumorphism"""
        return {
            'backgroundColor': bg_color,
            'cornerRadius': '20px',
            'paddingAll': '20px'
        }
    
    @staticmethod
    def _shadow_effect():
        """تأثير الظل المزدوج"""
        return {
            'offsetTop': '10px',
            'offsetStart': '10px',
            'backgroundColor': '#A3B1C6'
        }
    
    @staticmethod
    def game_start(game_name, question, round_num=1, total_rounds=5):
        """تصميم بداية السؤال - Neumorphism"""
        
        # حساب نسبة التقدم
        progress = round_num / total_rounds
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
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
                                        "text": game_name,
                                        "weight": "bold",
                                        "size": "xl",
                                        "color": FlexStyles.COLORS['text'],
                                        "flex": 1
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": f"{round_num}/{total_rounds}",
                                                "size": "sm",
                                                "color": FlexStyles.COLORS['secondary'],
                                                "align": "center",
                                                "weight": "bold"
                                            }
                                        ],
                                        "backgroundColor": FlexStyles.COLORS['bg'],
                                        "cornerRadius": "15px",
                                        "paddingAll": "8px",
                                        "width": "60px",
                                        "justifyContent": "center"
                                    }
                                ],
                                "spacing": "md"
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
                                                "type": "filler"
                                            }
                                        ],
                                        "height": "8px",
                                        "backgroundColor": FlexStyles.COLORS['secondary'],
                                        "cornerRadius": "4px",
                                        "flex": round_num
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "filler"
                                            }
                                        ],
                                        "height": "8px",
                                        "backgroundColor": FlexStyles.COLORS['dark'],
                                        "cornerRadius": "4px",
                                        "flex": total_rounds - round_num,
                                        "opacity": 0.3
                                    }
                                ],
                                "layout": "horizontal",
                                "spacing": "xs",
                                "margin": "lg",
                                "backgroundColor": FlexStyles.COLORS['bg'],
                                "cornerRadius": "10px",
                                "paddingAll": "4px"
                            }
                        ],
                        **FlexStyles._neomorphism_box()
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": question,
                                "size": "xl",
                                "color": FlexStyles.COLORS['text'],
                                "wrap": True,
                                "weight": "bold",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": FlexStyles.COLORS['light'],
                        "cornerRadius": "25px",
                        "paddingAll": "28px",
                        "margin": "xl"
                    }
                ],
                "spacing": "none",
                "backgroundColor": FlexStyles.COLORS['bg'],
                "paddingAll": "24px"
            }
        }
    
    @staticmethod
    def correct_answer(player_name, points, streak=1):
        """تصميم الإجابة الصحيحة - Neumorphism"""
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "✓",
                                "size": "5xl",
                                "color": FlexStyles.COLORS['success'],
                                "align": "center",
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": FlexStyles.COLORS['bg'],
                        "cornerRadius": "full",
                        "width": "100px",
                        "height": "100px",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "offsetStart": "50%",
                        "margin": "none"
                    },
                    {
                        "type": "text",
                        "text": "إجابة صحيحة! 🎉",
                        "weight": "bold",
                        "size": "xl",
                        "color": FlexStyles.COLORS['text'],
                        "align": "center",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": player_name,
                        "size": "md",
                        "color": FlexStyles.COLORS['text_light'],
                        "align": "center",
                        "margin": "sm"
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
                                        "text": "النقاط",
                                        "size": "sm",
                                        "color": FlexStyles.COLORS['text_light'],
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": f"+{points}",
                                        "size": "xxl",
                                        "color": FlexStyles.COLORS['success'],
                                        "flex": 1,
                                        "align": "end",
                                        "weight": "bold"
                                    }
                                ],
                                "spacing": "md"
                            },
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "🔥 السلسلة",
                                        "size": "sm",
                                        "color": FlexStyles.COLORS['text_light'],
                                        "flex": 1
                                    },
                                    {
                                        "type": "text",
                                        "text": str(streak),
                                        "size": "lg",
                                        "color": FlexStyles.COLORS['secondary'],
                                        "flex": 1,
                                        "align": "end",
                                        "weight": "bold"
                                    }
                                ],
                                "spacing": "md",
                                "margin": "md"
                            } if streak > 1 else {
                                "type": "box",
                                "layout": "vertical",
                                "contents": []
                            }
                        ],
                        "backgroundColor": FlexStyles.COLORS['light'],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "xl"
                    }
                ],
                "backgroundColor": FlexStyles.COLORS['bg'],
                "paddingAll": "32px"
            }
        }
    
    @staticmethod
    def wrong_answer(correct_ans):
        """تصميم الإجابة الخاطئة - Neumorphism"""
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "✕",
                                "size": "5xl",
                                "color": FlexStyles.COLORS['error'],
                                "align": "center",
                                "weight": "bold"
                            }
                        ],
                        "backgroundColor": FlexStyles.COLORS['bg'],
                        "cornerRadius": "full",
                        "width": "100px",
                        "height": "100px",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "offsetStart": "50%",
                        "margin": "none"
                    },
                    {
                        "type": "text",
                        "text": "إجابة خاطئة",
                        "weight": "bold",
                        "size": "xl",
                        "color": FlexStyles.COLORS['text'],
                        "align": "center",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الإجابة الصحيحة:",
                                "size": "sm",
                                "color": FlexStyles.COLORS['text_light'],
                                "align": "center"
                            },
                            {
                                "type": "text",
                                "text": correct_ans,
                                "size": "xl",
                                "color": FlexStyles.COLORS['text'],
                                "align": "center",
                                "weight": "bold",
                                "margin": "md",
                                "wrap": True
                            }
                        ],
                        "backgroundColor": FlexStyles.COLORS['light'],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "xl"
                    }
                ],
                "backgroundColor": FlexStyles.COLORS['bg'],
                "paddingAll": "32px"
            }
        }
    
    @staticmethod
    def game_winner(winner_name, winner_score, players_scores, game_name):
        """تصميم إعلان الفائز - Neumorphism"""
        
        sorted_players = sorted(players_scores.items(), key=lambda x: x[1], reverse=True)
        
        players_list = []
        for i, (name, score) in enumerate(sorted_players[:5], 1):
            is_winner = (i == 1)
            
            # أيقونات المراكز
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            
            player_box = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": medal,
                                "size": "xl" if i <= 3 else "md",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": FlexStyles.COLORS['light'] if is_winner else FlexStyles.COLORS['bg'],
                        "cornerRadius": "15px",
                        "width": "45px",
                        "height": "45px",
                        "justifyContent": "center",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": name,
                        "size": "md" if is_winner else "sm",
                        "color": FlexStyles.COLORS['text'],
                        "flex": 3,
                        "margin": "md",
                        "weight": "bold" if is_winner else "regular",
                        "wrap": True
                    },
                    {
                        "type": "text",
                        "text": f"{score}",
                        "size": "lg" if is_winner else "md",
                        "color": FlexStyles.COLORS['secondary'] if is_winner else FlexStyles.COLORS['text'],
                        "flex": 1,
                        "align": "end",
                        "weight": "bold"
                    }
                ],
                "spacing": "md",
                "paddingAll": "16px",
                "backgroundColor": FlexStyles.COLORS['light'] if is_winner else FlexStyles.COLORS['bg'],
                "cornerRadius": "20px",
                "margin": "sm" if i > 1 else "none"
            }
            players_list.append(player_box)
        
        return {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "👑",
                                "size": "5xl",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": FlexStyles.COLORS['secondary'],
                        "cornerRadius": "full",
                        "width": "110px",
                        "height": "110px",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "offsetStart": "50%"
                    },
                    {
                        "type": "text",
                        "text": "🎮 انتهت اللعبة",
                        "size": "xl",
                        "color": FlexStyles.COLORS['text'],
                        "align": "center",
                        "weight": "bold",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": game_name,
                        "size": "sm",
                        "color": FlexStyles.COLORS['text_light'],
                        "align": "center",
                        "margin": "xs"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "الفائز 🏆",
                                "size": "sm",
                                "color": FlexStyles.COLORS['text_light'],
                                "align": "center",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": winner_name,
                                "size": "xxl",
                                "color": FlexStyles.COLORS['text'],
                                "align": "center",
                                "weight": "bold",
                                "margin": "sm",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "text": f"{winner_score} نقطة",
                                "size": "xl",
                                "color": FlexStyles.COLORS['secondary'],
                                "align": "center",
                                "weight": "bold",
                                "margin": "sm"
                            }
                        ],
                        "backgroundColor": FlexStyles.COLORS['light'],
                        "cornerRadius": "25px",
                        "paddingAll": "24px",
                        "margin": "xl"
                    },
                    {
                        "type": "text",
                        "text": "📊 النتائج النهائية",
                        "size": "md",
                        "color": FlexStyles.COLORS['text'],
                        "weight": "bold",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": players_list,
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "🎮 لعبة جديدة",
                                    "text": game_name
                                },
                                "style": "primary",
                                "color": FlexStyles.COLORS['secondary'],
                                "height": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "🏆 الصدارة",
                                    "text": "الصدارة"
                                },
                                "style": "secondary",
                                "height": "sm"
                            }
                        ],
                        "spacing": "sm",
                        "margin": "xl"
                    }
                ],
                "backgroundColor": FlexStyles.COLORS['bg'],
                "paddingAll": "28px"
            }
        }
    
    @staticmethod
    def hint_message(hint_text):
        """تصميم رسالة التلميح - Neumorphism"""
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "💡",
                                "size": "4xl",
                                "align": "center"
                            }
                        ],
                        "backgroundColor": FlexStyles.COLORS['secondary'],
                        "cornerRadius": "full",
                        "width": "90px",
                        "height": "90px",
                        "justifyContent": "center",
                        "offsetStart": "50%"
                    },
                    {
                        "type": "text",
                        "text": "تلميح",
                        "weight": "bold",
                        "size": "xl",
                        "color": FlexStyles.COLORS['text'],
                        "align": "center",
                        "margin": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": hint_text,
                                "size": "md",
                                "color": FlexStyles.COLORS['text'],
                                "align": "center",
                                "wrap": True
                            }
                        ],
                        "backgroundColor": FlexStyles.COLORS['light'],
                        "cornerRadius": "20px",
                        "paddingAll": "20px",
                        "margin": "lg"
                    }
                ],
                "backgroundColor": FlexStyles.COLORS['bg'],
                "paddingAll": "28px"
            }
        }
    
    @staticmethod
    def game_progress(game_name, scores, current_round, total_rounds):
        """تصميم عرض التقدم - Neumorphism"""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        score_items = []
        for i, (name, score) in enumerate(sorted_scores[:3], 1):
            score_items.append({
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": f"{i}.",
                        "size": "sm",
                        "color": FlexStyles.COLORS['text_light'],
                        "flex": 0,
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": name,
                        "size": "sm",
                        "color": FlexStyles.COLORS['text'],
                        "flex": 2,
                        "wrap": True,
                        "margin": "sm"
                    },
                    {
                        "type": "text",
                        "text": str(score),
                        "size": "sm",
                        "color": FlexStyles.COLORS['secondary'],
                        "flex": 1,
                        "align": "end",
                        "weight": "bold"
                    }
                ],
                "backgroundColor": FlexStyles.COLORS['light'],
                "cornerRadius": "15px",
                "paddingAll": "12px",
                "margin": "xs" if i > 1 else "none"
            })
        
        return {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"🎮 {game_name}",
                        "weight": "bold",
                        "size": "lg",
                        "color": FlexStyles.COLORS['text']
                    },
                    {
                        "type": "text",
                        "text": f"السؤال {current_round} من {total_rounds}",
                        "size": "xs",
                        "color": FlexStyles.COLORS['text_light'],
                        "margin": "xs"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": score_items,
                        "margin": "md"
                    }
                ],
                "backgroundColor": FlexStyles.COLORS['bg'],
                "cornerRadius": "20px",
                "paddingAll": "20px"
            }
        }
