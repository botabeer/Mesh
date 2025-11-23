"""
Bot Mesh - Rich Menu Manager
أزرار الألعاب الثابتة أسفل الشاشة
Created by: Abeer Aldosari © 2025
"""
import os
import logging
from typing import Dict, List
from PIL import Image, ImageDraw, ImageFont
from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize
from linebot.models.actions import MessageAction

logger = logging.getLogger(__name__)


class PermanentRichMenu:
    """نظام Rich Menu الثابت للألعاب"""
    
    def __init__(self, line_bot_api: LineBotApi):
        self.api = line_bot_api
        
        # 11 لعبة مع معلوماتها
        self.games = {
            'ذكاء': {'emoji': '🧠', 'name': 'اختبار الذكاء', 'color': '#6C8EEF'},
            'لون': {'emoji': '🎨', 'name': 'الكلمة واللون', 'color': '#9F7AEA'},
            'ترتيب': {'emoji': '🔤', 'name': 'ترتيب الحروف', 'color': '#4FD1C5'},
            'تكوين': {'emoji': '✏️', 'name': 'تكوين الكلمات', 'color': '#68D391'},
            'سلسلة': {'emoji': '⛓️', 'name': 'سلسلة الكلمات', 'color': '#FC8181'},
            'أسرع': {'emoji': '⚡', 'name': 'الكتابة السريعة', 'color': '#F687B3'},
            'لعبة': {'emoji': '🎯', 'name': 'إنسان حيوان نبات', 'color': '#63B3ED'},
            'خمن': {'emoji': '🤔', 'name': 'خمن الكلمة', 'color': '#B794F4'},
            'توافق': {'emoji': '💖', 'name': 'نسبة التوافق', 'color': '#FEB2B2'},
            'ضد': {'emoji': '↔️', 'name': 'الأضداد', 'color': '#9AE6B4'},
            'أغنية': {'emoji': '🎵', 'name': 'خمن الأغنية', 'color': '#E9D8FD'},
        }
        
        # أزرار التحكم
        self.control_buttons = {
            'انضم': {'emoji': '🔑', 'color': '#667EEA'},
            'نقاطي': {'emoji': '📊', 'color': '#48BB78'},
            'الصدارة': {'emoji': '🏆', 'color': '#F6AD55'},
            'ثيم': {'emoji': '🎨', 'color': '#9F7AEA'},
            'مساعدة': {'emoji': '❓', 'color': '#63B3ED'},
            'إيقاف': {'emoji': '⏹️', 'color': '#FC8181'}
        }
    
    # ==========================================
    # 📐 تخطيط Rich Menu (Layout)
    # ==========================================
    
    def _create_rich_menu_layout(self) -> RichMenu:
        """
        إنشاء تخطيط Rich Menu
        
        التخطيط:
        - العرض: 2500px
        - الارتفاع: 1686px (حجم mega)
        
        الصف الأول (421px): 6 أزرار تحكم
        الصفوف 2-4: 11 لعبة (3-4 في كل صف)
        """
        
        # المناطق القابلة للنقر
        areas = []
        
        # 1. أزرار التحكم (الصف الأول)
        control_list = list(self.control_buttons.keys())
        button_width = 2500 // 6  # ~417px
        
        for i, cmd in enumerate(control_list):
            areas.append(
                RichMenuArea(
                    bounds=RichMenuBounds(
                        x=i * button_width,
                        y=0,
                        width=button_width,
                        height=421
                    ),
                    action=MessageAction(
                        label=f"{self.control_buttons[cmd]['emoji']} {cmd}",
                        text=cmd
                    )
                )
            )
        
        # 2. الألعاب (3 صفوف × 4 أعمدة = 12 خانة، 11 لعبة)
        game_list = list(self.games.keys())
        game_width = 2500 // 4  # 625px
        game_height = (1686 - 421) // 3  # ~422px
        
        for i, game in enumerate(game_list):
            row = i // 4
            col = i % 4
            
            areas.append(
                RichMenuArea(
                    bounds=RichMenuBounds(
                        x=col * game_width,
                        y=421 + (row * game_height),
                        width=game_width,
                        height=game_height
                    ),
                    action=MessageAction(
                        label=f"{self.games[game]['emoji']} {game}",
                        text=game
                    )
                )
            )
        
        # إنشاء Rich Menu
        rich_menu = RichMenu(
            size=RichMenuSize(width=2500, height=1686),
            selected=True,
            name="Bot Mesh - Permanent Games Menu",
            chat_bar_text="🎮 الألعاب",
            areas=areas
        )
        
        return rich_menu
    
    # ==========================================
    # 🎨 إنشاء صورة Rich Menu
    # ==========================================
    
    def generate_rich_menu_image(self, theme: str = 'soft') -> str:
        """
        إنشاء صورة Rich Menu بستايل Neumorphism
        
        الثيمات المتاحة: soft, dark, ocean, sunset, forest
        """
        
        # ألوان الثيمات
        themes = {
            'soft': {
                'bg': '#E0E5EC',
                'card': '#E0E5EC',
                'shadow_light': '#FFFFFF',
                'shadow_dark': '#A3B1C6',
                'text': '#2C3E50'
            },
            'dark': {
                'bg': '#2C3E50',
                'card': '#2C3E50',
                'shadow_light': '#3A4D63',
                'shadow_dark': '#1A2633',
                'text': '#FFFFFF'
            },
            'ocean': {
                'bg': '#C8D8E8',
                'card': '#C8D8E8',
                'shadow_light': '#FFFFFF',
                'shadow_dark': '#9EB4C8',
                'text': '#0C4A6E'
            },
            'sunset': {
                'bg': '#FFE8D6',
                'card': '#FFE8D6',
                'shadow_light': '#FFFFFF',
                'shadow_dark': '#D4BCA4',
                'text': '#7C2D12'
            },
            'forest': {
                'bg': '#D4E4D4',
                'card': '#D4E4D4',
                'shadow_light': '#FFFFFF',
                'shadow_dark': '#A8C4A8',
                'text': '#064E3B'
            }
        }
        
        colors = themes.get(theme, themes['soft'])
        
        # إنشاء الصورة
        img = Image.new('RGB', (2500, 1686), colors['bg'])
        draw = ImageDraw.Draw(img)
        
        # محاولة تحميل خط عربي
        try:
            font_large = ImageFont.truetype("arial.ttf", 60)
            font_small = ImageFont.truetype("arial.ttf", 40)
        except:
            try:
                font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
                font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
            except:
                font_large = font_small = ImageFont.load_default()
        
        # رسم أزرار التحكم (الصف الأول)
        control_list = list(self.control_buttons.keys())
        button_width = 2500 // 6
        
        for i, cmd in enumerate(control_list):
            x = i * button_width
            y = 0
            w = button_width
            h = 421
            
            self._draw_neumorphism_button(
                draw, x, y, w, h,
                self.control_buttons[cmd]['emoji'],
                cmd,
                self.control_buttons[cmd]['color'],
                colors, font_large, font_small
            )
        
        # رسم أزرار الألعاب (3 صفوف)
        game_list = list(self.games.keys())
        game_width = 2500 // 4
        game_height = (1686 - 421) // 3
        
        for i, game in enumerate(game_list):
            row = i // 4
            col = i % 4
            
            x = col * game_width
            y = 421 + (row * game_height)
            w = game_width
            h = game_height
            
            self._draw_neumorphism_button(
                draw, x, y, w, h,
                self.games[game]['emoji'],
                self.games[game]['name'],
                self.games[game]['color'],
                colors, font_large, font_small
            )
        
        # حفظ الصورة
        os.makedirs("assets", exist_ok=True)
        image_path = f"assets/rich_menu_{theme}.png"
        img.save(image_path, "PNG", quality=95)
        
        logger.info(f"✅ Rich Menu image saved: {image_path}")
        return image_path
    
    def _draw_neumorphism_button(self, draw, x, y, w, h, emoji, text,
                                  color, theme_colors, font_emoji, font_text):
        """رسم زر واحد بتأثير Neumorphism"""
        
        padding = 15
        
        # الخلفية الرئيسية
        draw.rounded_rectangle(
            [x + padding, y + padding, x + w - padding, y + h - padding],
            radius=25,
            fill=theme_colors['card']
        )
        
        # شريط علوي ملون (Accent)
        draw.rounded_rectangle(
            [x + padding, y + padding, x + w - padding, y + padding + 8],
            radius=25,
            fill=color
        )
        
        # النص (الإيموجي + العنوان)
        full_text = f"{emoji}\n{text}"
        
        # حساب موضع النص
        bbox = draw.textbbox((0, 0), full_text, font=font_text)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        text_x = x + (w - text_w) // 2
        text_y = y + (h - text_h) // 2
        
        # رسم النص
        draw.text(
            (text_x, text_y),
            full_text,
            fill=theme_colors['text'],
            font=font_text,
            align="center"
        )
    
    # ==========================================
    # 🚀 تثبيت Rich Menu
    # ==========================================
    
    def setup_permanent_menu(self, theme: str = 'soft') -> bool:
        """
        إعداد Rich Menu الثابت
        
        الخطوات:
        1. حذف القوائم القديمة
        2. إنشاء قائمة جديدة
        3. رفع الصورة
        4. تعيينها كافتراضية
        """
        
        logger.info("🚀 Setting up permanent Rich Menu...")
        
        try:
            # 1. حذف القوائم القديمة
            self._delete_all_menus()
            
            # 2. إنشاء Rich Menu
            rich_menu = self._create_rich_menu_layout()
            rich_menu_id = self.api.create_rich_menu(rich_menu=rich_menu)
            logger.info(f"✅ Rich Menu created: {rich_menu_id}")
            
            # 3. توليد ورفع الصورة
            image_path = self.generate_rich_menu_image(theme)
            
            with open(image_path, 'rb') as f:
                self.api.set_rich_menu_image(rich_menu_id, 'image/png', f)
            logger.info("✅ Image uploaded")
            
            # 4. تعيين كافتراضي
            self.api.set_default_rich_menu(rich_menu_id)
            logger.info("✅ Set as default Rich Menu")
            
            logger.info("🎉 Permanent Rich Menu setup complete!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to setup Rich Menu: {e}")
            return False
    
    def _delete_all_menus(self):
        """حذف جميع Rich Menus الموجودة"""
        try:
            menus = self.api.get_rich_menu_list()
            for menu in menus:
                self.api.delete_rich_menu(menu.rich_menu_id)
                logger.info(f"🗑️ Deleted: {menu.rich_menu_id}")
        except Exception as e:
            logger.warning(f"⚠️ Could not delete old menus: {e}")
    
    # ==========================================
    # 🎨 تغيير الثيم
    # ==========================================
    
    def change_theme(self, theme: str) -> bool:
        """
        تغيير ثيم Rich Menu
        
        Args:
            theme: اسم الثيم (soft, dark, ocean, sunset, forest)
        """
        return self.setup_permanent_menu(theme)
    
    # ==========================================
    # 📊 معلومات Rich Menu
    # ==========================================
    
    def get_menu_info(self) -> Dict:
        """الحصول على معلومات Rich Menu الحالي"""
        try:
            menus = self.api.get_rich_menu_list()
            if menus:
                menu = menus[0]
                return {
                    'id': menu.rich_menu_id,
                    'name': menu.name,
                    'chat_bar_text': menu.chat_bar_text,
                    'areas_count': len(menu.areas),
                    'selected': menu.selected
                }
        except Exception as e:
            logger.error(f"❌ Failed to get menu info: {e}")
        
        return None


# =============================================
# 🧪 اختبار وتشغيل مباشر
# =============================================
if __name__ == "__main__":
    from dotenv import load_dotenv
    import sys
    
    # تحميل المتغيرات
    load_dotenv()
    
    # إعداد Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # الحصول على Token
    token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    if not token:
        print("❌ LINE_CHANNEL_ACCESS_TOKEN not found in .env")
        sys.exit(1)
    
    # إنشاء API
    api = LineBotApi(token)
    
    # إنشاء Rich Menu Manager
    menu_manager = PermanentRichMenu(api)
    
    # اختيار الثيم
    print("\n🎨 اختر الثيم:")
    print("1. soft (الثيم الأساسي الناعم)")
    print("2. dark (داكن)")
    print("3. ocean (محيطي أزرق)")
    print("4. sunset (غروب برتقالي)")
    print("5. forest (طبيعي أخضر)")
    
    choice = input("\nاختيارك (1-5) أو اضغط Enter للثيم الافتراضي: ").strip()
    
    theme_map = {
        '1': 'soft',
        '2': 'dark',
        '3': 'ocean',
        '4': 'sunset',
        '5': 'forest'
    }
    
    theme = theme_map.get(choice, 'soft')
    
    print(f"\n🚀 جاري إعداد Rich Menu بثيم: {theme}")
    print("=" * 50)
    
    # تثبيت Rich Menu
    if menu_manager.setup_permanent_menu(theme):
        print("\n" + "=" * 50)
        print("✅ تم إعداد Rich Menu بنجاح!")
        print("=" * 50)
        print("\n📱 الأزرار الثابتة الآن نشطة في البوت")
        print("🔄 قد يحتاج المستخدمون إلى إعادة فتح المحادثة لرؤيتها")
        print("\n💡 يمكنك تغيير الثيم في أي وقت بتشغيل هذا السكريبت مرة أخرى")
        
        # عرض معلومات Rich Menu
        info = menu_manager.get_menu_info()
        if info:
            print("\n📊 معلومات Rich Menu:")
            print(f"   ID: {info['id']}")
            print(f"   Name: {info['name']}")
            print(f"   عدد الأزرار: {info['areas_count']}")
    else:
        print("\n❌ فشل إعداد Rich Menu")
        print("تحقق من:")
        print("  1. صحة LINE_CHANNEL_ACCESS_TOKEN")
        print("  2. صلاحيات البوت")
        print("  3. الاتصال بالإنترنت")
