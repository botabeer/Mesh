"""
Bot Mesh - Rich Menu Setup
Created by: Abeer Aldosari © 2025

هذا الملف لإنشاء Rich Menu (الأزرار الثابتة أسفل المحادثة)
"""
import os
import json
import logging
from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize
from linebot.models.actions import MessageAction

logger = logging.getLogger(__name__)


class RichMenuManager:
    """مدير Rich Menu"""
    
    def __init__(self, line_bot_api: LineBotApi):
        self.api = line_bot_api
    
    def create_rich_menu(self) -> str:
        """إنشاء Rich Menu جديد"""
        
        rich_menu = RichMenu(
            size=RichMenuSize(width=2500, height=843),
            selected=True,
            name="Bot Mesh Menu",
            chat_bar_text="القائمة 🎮",
            areas=[
                # زر انضم
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=625, height=843),
                    action=MessageAction(label="انضم", text="انضم")
                ),
                # زر ابدأ
                RichMenuArea(
                    bounds=RichMenuBounds(x=625, y=0, width=625, height=843),
                    action=MessageAction(label="ابدأ", text="ابدأ")
                ),
                # زر نقاطي
                RichMenuArea(
                    bounds=RichMenuBounds(x=1250, y=0, width=625, height=421),
                    action=MessageAction(label="نقاطي", text="نقاطي")
                ),
                # زر الصدارة
                RichMenuArea(
                    bounds=RichMenuBounds(x=1250, y=421, width=625, height=422),
                    action=MessageAction(label="الصدارة", text="الصدارة")
                ),
                # زر ثيم
                RichMenuArea(
                    bounds=RichMenuBounds(x=1875, y=0, width=625, height=421),
                    action=MessageAction(label="ثيم", text="ثيم")
                ),
                # زر مساعدة
                RichMenuArea(
                    bounds=RichMenuBounds(x=1875, y=421, width=625, height=422),
                    action=MessageAction(label="مساعدة", text="مساعدة")
                )
            ]
        )
        
        try:
            rich_menu_id = self.api.create_rich_menu(rich_menu=rich_menu)
            logger.info(f"✅ Rich Menu created: {rich_menu_id}")
            return rich_menu_id
        except Exception as e:
            logger.error(f"❌ Failed to create Rich Menu: {e}")
            return None
    
    def upload_image(self, rich_menu_id: str, image_path: str) -> bool:
        """رفع صورة Rich Menu"""
        try:
            with open(image_path, 'rb') as f:
                self.api.set_rich_menu_image(rich_menu_id, 'image/png', f)
            logger.info(f"✅ Image uploaded for Rich Menu: {rich_menu_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to upload image: {e}")
            return False
    
    def set_default(self, rich_menu_id: str) -> bool:
        """تعيين Rich Menu كافتراضي"""
        try:
            self.api.set_default_rich_menu(rich_menu_id)
            logger.info(f"✅ Default Rich Menu set: {rich_menu_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to set default: {e}")
            return False
    
    def delete_all(self) -> bool:
        """حذف جميع Rich Menus"""
        try:
            menus = self.api.get_rich_menu_list()
            for menu in menus:
                self.api.delete_rich_menu(menu.rich_menu_id)
                logger.info(f"🗑️ Deleted Rich Menu: {menu.rich_menu_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to delete menus: {e}")
            return False
    
    def setup(self, image_path: str = "assets/rich_menu.png") -> bool:
        """إعداد Rich Menu كامل"""
        # حذف القديم
        self.delete_all()
        
        # إنشاء جديد
        menu_id = self.create_rich_menu()
        if not menu_id:
            return False
        
        # رفع الصورة
        if os.path.exists(image_path):
            if not self.upload_image(menu_id, image_path):
                return False
        else:
            logger.warning(f"⚠️ Image not found: {image_path}")
            logger.info("📝 Create a 2500x843 PNG image with 6 buttons")
        
        # تعيين كافتراضي
        return self.set_default(menu_id)


def generate_rich_menu_image():
    """
    توليد صورة Rich Menu باستخدام PIL
    الحجم: 2500 x 843 بكسل
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        logger.error("❌ PIL not installed. Run: pip install Pillow")
        return None
    
    # الألوان
    bg_color = "#1A1A2E"
    button_color = "#16213E"
    accent_color = "#00D9FF"
    text_color = "#FFFFFF"
    
    # إنشاء الصورة
    img = Image.new('RGB', (2500, 843), bg_color)
    draw = ImageDraw.Draw(img)
    
    # محاولة تحميل خط عربي
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        font = ImageFont.load_default()
        font_small = font
    
    # تعريف الأزرار
    buttons = [
        {"x": 0, "y": 0, "w": 625, "h": 843, "emoji": "🔑", "text": "انضم", "color": "#667EEA"},
        {"x": 625, "y": 0, "w": 625, "h": 843, "emoji": "🎮", "text": "ابدأ", "color": "#00D9FF"},
        {"x": 1250, "y": 0, "w": 625, "h": 421, "emoji": "📊", "text": "نقاطي", "color": "#48BB78"},
        {"x": 1250, "y": 421, "w": 625, "h": 422, "emoji": "🏆", "text": "الصدارة", "color": "#F6AD55"},
        {"x": 1875, "y": 0, "w": 625, "h": 421, "emoji": "🎨", "text": "ثيم", "color": "#9F7AEA"},
        {"x": 1875, "y": 421, "w": 625, "h": 422, "emoji": "❓", "text": "مساعدة", "color": "#FC8181"}
    ]
    
    # رسم الأزرار
    for btn in buttons:
        # خلفية الزر
        padding = 10
        draw.rounded_rectangle(
            [btn['x'] + padding, btn['y'] + padding, 
             btn['x'] + btn['w'] - padding, btn['y'] + btn['h'] - padding],
            radius=20,
            fill=btn['color']
        )
        
        # النص في المنتصف
        text = f"{btn['emoji']}\n{btn['text']}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        x = btn['x'] + (btn['w'] - text_w) // 2
        y = btn['y'] + (btn['h'] - text_h) // 2
        
        draw.text((x, y), text, fill=text_color, font=font, align="center")
    
    # حفظ الصورة
    os.makedirs("assets", exist_ok=True)
    img.save("assets/rich_menu.png", "PNG")
    logger.info("✅ Rich Menu image saved: assets/rich_menu.png")
    
    return "assets/rich_menu.png"


# =============================================
# تشغيل مباشر لإنشاء Rich Menu
# =============================================
if __name__ == "__main__":
    import sys
    
    # تحميل المتغيرات
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    if not token:
        print("❌ LINE_CHANNEL_ACCESS_TOKEN not found in .env")
        sys.exit(1)
    
    api = LineBotApi(token)
    manager = RichMenuManager(api)
    
    # توليد الصورة
    print("🎨 Generating Rich Menu image...")
    image_path = generate_rich_menu_image()
    
    if image_path:
        # إعداد Rich Menu
        print("📋 Setting up Rich Menu...")
        if manager.setup(image_path):
            print("✅ Rich Menu setup complete!")
        else:
            print("❌ Rich Menu setup failed")
    else:
        print("❌ Failed to generate image")
