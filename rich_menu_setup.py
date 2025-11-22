"""
Bot Mesh - Rich Menu Setup
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize
from linebot.models.actions import MessageAction
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RichMenuSetup:
    """إعداد Rich Menu كامل"""
    
    def __init__(self, line_bot_api: LineBotApi):
        self.api = line_bot_api
        
        self.games = {
            'ذكاء': {'emoji': '🧠', 'name': 'اختبار الذكاء', 'color': '#667EEA'},
            'لون': {'emoji': '🎨', 'name': 'لعبة الألوان', 'color': '#9F7AEA'},
            'سلسلة': {'emoji': '⛓️', 'name': 'سلسلة الكلمات', 'color': '#4FD1C5'},
            'ترتيب': {'emoji': '🔤', 'name': 'ترتيب الحروف', 'color': '#68D391'},
            'تكوين': {'emoji': '✏️', 'name': 'تكوين الكلمات', 'color': '#FC8181'},
            'أسرع': {'emoji': '⚡', 'name': 'الكتابة السريعة', 'color': '#F687B3'},
            'لعبة': {'emoji': '🎯', 'name': 'إنسان حيوان نبات', 'color': '#63B3ED'},
            'خمن': {'emoji': '🤔', 'name': 'خمن الكلمة', 'color': '#B794F4'},
            'توافق': {'emoji': '💖', 'name': 'نسبة التوافق', 'color': '#FEB2B2'},
            'ضد': {'emoji': '↔️', 'name': 'الأضداد', 'color': '#9AE6B4'},
            'أغنية': {'emoji': '🎵', 'name': 'خمن الأغنية', 'color': '#E9D8FD'},
        }
    
    def create_main_menu(self) -> str:
        rich_menu = RichMenu(
            size=RichMenuSize(width=2500, height=1686),
            selected=True,
            name="Bot Mesh - Games Menu",
            chat_bar_text="🎮 قائمة الألعاب",
            areas=self._create_menu_areas()
        )
        try:
            rich_menu_id = self.api.create_rich_menu(rich_menu=rich_menu)
            logger.info(f"✅ Rich Menu created: {rich_menu_id}")
            return rich_menu_id
        except Exception as e:
            logger.error(f"❌ Failed to create Rich Menu: {e}")
            return None
    
    def _create_menu_areas(self) -> list:
        areas = []
        
        # أزرار التحكم (الصف الأول)
        control_buttons = [
            {'x': 0, 'text': 'انضم', 'label': '🔑 انضم'},
            {'x': 417, 'text': 'نقاطي', 'label': '📊 نقاطي'},
            {'x': 833, 'text': 'الصدارة', 'label': '🏆 الصدارة'},
            {'x': 1250, 'text': 'ثيم', 'label': '🎨 ثيم'},
            {'x': 1667, 'text': 'مساعدة', 'label': '❓ مساعدة'},
            {'x': 2083, 'text': 'إيقاف', 'label': '⏹️ إيقاف'}
        ]
        
        for btn in control_buttons:
            areas.append(
                RichMenuArea(
                    bounds=RichMenuBounds(x=btn['x'], y=0, width=417, height=421),
                    action=MessageAction(label=btn['label'], text=btn['text'])
                )
            )
        
        # أزرار الألعاب (11 لعبة)
        game_positions = [
            {'x': 0, 'y': 421, 'w': 625, 'h': 422, 'game': 'ذكاء'},
            {'x': 625, 'y': 421, 'w': 625, 'h': 422, 'game': 'لون'},
            {'x': 1250, 'y': 421, 'w': 625, 'h': 422, 'game': 'سلسلة'},
            {'x': 1875, 'y': 421, 'w': 625, 'h': 422, 'game': 'ترتيب'},
            {'x': 0, 'y': 843, 'w': 625, 'h': 422, 'game': 'تكوين'},
            {'x': 625, 'y': 843, 'w': 625, 'h': 422, 'game': 'أسرع'},
            {'x': 1250, 'y': 843, 'w': 625, 'h': 422, 'game': 'لعبة'},
            {'x': 1875, 'y': 843, 'w': 625, 'h': 422, 'game': 'خمن'},
            {'x': 0, 'y': 1265, 'w': 833, 'h': 421, 'game': 'توافق'},
            {'x': 833, 'y': 1265, 'w': 834, 'h': 421, 'game': 'ضد'},
            {'x': 1667, 'y': 1265, 'w': 833, 'h': 421, 'game': 'أغنية'},
        ]
        
        for pos in game_positions:
            game = self.games.get(pos['game'], {})
            areas.append(
                RichMenuArea(
                    bounds=RichMenuBounds(
                        x=pos['x'], y=pos['y'],
                        width=pos['w'], height=pos['h']
                    ),
                    action=MessageAction(
                        label=f"{game.get('emoji', '🎮')} {pos['game']}",
                        text=pos['game']
                    )
                )
            )
        
        return areas
    
    def generate_menu_image(self, theme: str = 'white') -> str:
        themes = {
            'white': {'bg': '#E8EBF5', 'card': '#FFFFFF', 'text': '#2C3E50'},
            'black': {'bg': '#0F0F1A', 'card': '#252538', 'text': '#FFFFFF'},
            'blue': {'bg': '#0A1628', 'card': '#0F2744', 'text': '#E0F2FE'}
        }
        colors = themes.get(theme, themes['white'])
        
        img = Image.new('RGB', (2500, 1686), colors['bg'])
        draw = ImageDraw.Draw(img)
        
        try:
            font_large = ImageFont.truetype("arial.ttf", 50)
            font_small = ImageFont.truetype("arial.ttf", 35)
        except:
            font_large = font_small = ImageFont.load_default()
        
        # رسم أزرار التحكم
        control_buttons = [
            {'x': 0, 'emoji': '🔑', 'text': 'انضم', 'color': '#667EEA'},
            {'x': 417, 'emoji': '📊', 'text': 'نقاطي', 'color': '#48BB78'},
            {'x': 833, 'emoji': '🏆', 'text': 'الصدارة', 'color': '#F6AD55'},
            {'x': 1250, 'emoji': '🎨', 'text': 'ثيم', 'color': '#9F7AEA'},
            {'x': 1667, 'emoji': '❓', 'text': 'مساعدة', 'color': '#63B3ED'},
            {'x': 2083, 'emoji': '⏹️', 'text': 'إيقاف', 'color': '#FC8181'}
        ]
        
        for btn in control_buttons:
            self._draw_button(draw, btn['x'], 0, 417, 421,
                             btn['emoji'], btn['text'], btn['color'],
                             colors['card'], colors['text'],
                             font_large, font_small)
        
        # رسم أزرار الألعاب (11 لعبة)
        game_positions = [
            {'x': 0, 'y': 421, 'w': 625, 'h': 422, 'game': 'ذكاء'},
            {'x': 625, 'y': 421, 'w': 625, 'h': 422, 'game': 'لون'},
            {'x': 1250, 'y': 421, 'w': 625, 'h': 422, 'game': 'سلسلة'},
            {'x': 1875, 'y': 421, 'w': 625, 'h': 422, 'game': 'ترتيب'},
            {'x': 0, 'y': 843, 'w': 625, 'h': 422, 'game': 'تكوين'},
            {'x': 625, 'y': 843, 'w': 625, 'h': 422, 'game': 'أسرع'},
            {'x': 1250, 'y': 843, 'w': 625, 'h': 422, 'game': 'لعبة'},
            {'x': 1875, 'y': 843, 'w': 625, 'h': 422, 'game': 'خمن'},
            {'x': 0, 'y': 1265, 'w': 833, 'h': 421, 'game': 'توافق'},
            {'x': 833, 'y': 1265, 'w': 834, 'h': 421, 'game': 'ضد'},
            {'x': 1667, 'y': 1265, 'w': 833, 'h': 421, 'game': 'أغنية'},
        ]
        
        for pos in game_positions:
            game = self.games.get(pos['game'], {})
            self._draw_button(draw, pos['x'], pos['y'], pos['w'], pos['h'],
                             game.get('emoji', '🎮'), game.get('name', pos['game']),
                             game.get('color', '#667EEA'),
                             colors['card'], colors['text'],
                             font_large, font_small)
        
        os.makedirs("assets", exist_ok=True)
        path = "assets/rich_menu.png"
        img.save(path, "PNG")
        logger.info(f"✅ Rich Menu image saved: {path}")
        return path
    
    def _draw_button(self, draw, x, y, w, h, emoji, text, color,
                    card_color, text_color, font_emoji, font_text):
        padding = 15
        draw.rounded_rectangle(
            [x + padding, y + padding, x + w - padding, y + h - padding],
            radius=25, fill=card_color
        )
        draw.rounded_rectangle(
            [x + padding, y + padding, x + w - padding, y + padding + 8],
            radius=25, fill=color
        )
        
        # رسم الإيموجي والنص
        full_text = f"{emoji}\n{text}"
        bbox = draw.textbbox((0, 0), full_text, font=font_text)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        text_x = x + (w - text_w) // 2
        text_y = y + (h - text_h) // 2
        
        draw.text((text_x, text_y), full_text, fill=text_color,
                 font=font_text, align="center")
    
    def upload_image(self, rich_menu_id: str, image_path: str) -> bool:
        try:
            with open(image_path, 'rb') as f:
                self.api.set_rich_menu_image(rich_menu_id, 'image/png', f)
            logger.info(f"✅ Image uploaded")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to upload image: {e}")
            return False
    
    def set_default(self, rich_menu_id: str) -> bool:
        try:
            self.api.set_default_rich_menu(rich_menu_id)
            logger.info(f"✅ Default Rich Menu set")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to set default: {e}")
            return False
    
    def delete_all(self) -> bool:
        try:
            menus = self.api.get_rich_menu_list()
            for menu in menus:
                self.api.delete_rich_menu(menu.rich_menu_id)
                logger.info(f"🗑️ Deleted: {menu.rich_menu_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to delete menus: {e}")
            return False
    
    def setup_complete(self, theme: str = 'white') -> bool:
        logger.info("🚀 Starting Rich Menu setup...")
        
        self.delete_all()
        
        menu_id = self.create_main_menu()
        if not menu_id:
            return False
        
        image_path = self.generate_menu_image(theme)
        if not self.upload_image(menu_id, image_path):
            return False
        
        if not self.set_default(menu_id):
            return False
        
        logger.info("🎉 Rich Menu setup complete!")
        return True


if __name__ == "__main__":
    load_dotenv()
    
    token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    if not token:
        print("❌ LINE_CHANNEL_ACCESS_TOKEN not found")
        exit(1)
    
    api = LineBotApi(token)
    setup = RichMenuSetup(api)
    
    theme = input("اختر الثيم (white/black/blue) [white]: ").strip() or 'white'
    
    if setup.setup_complete(theme):
        print("\n✅ تم إعداد Rich Menu بنجاح!")
    else:
        print("\n❌ فشل إعداد Rich Menu")
