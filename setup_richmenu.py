"""
Bot Mesh - Rich Menu Setup Script
Created by: Abeer Aldosari © 2025
"""
import os
from config import LINE_TOKEN
from rich_menu_manager import RichMenuManager
from create_richmenu_image import create_rich_menu_image

def setup_rich_menu():
    """إعداد Rich Menu للبوت"""
    print("🚀 Starting Rich Menu Setup...")
    
    # التحقق من وجود Token
    if not LINE_TOKEN:
        print("❌ LINE_CHANNEL_ACCESS_TOKEN not found in environment")
        return False
    
    # إنشاء الصورة
    print("📸 Creating Rich Menu image...")
    image_path = create_rich_menu_image('rich_menu.png')
    
    # إنشاء Manager
    manager = RichMenuManager(LINE_TOKEN)
    
    # إعداد القائمة الافتراضية
    print("🔧 Setting up default Rich Menu...")
    success = manager.setup_default_menu(image_path)
    
    if success:
        print("✅ Rich Menu setup completed successfully!")
        print("📱 The menu will appear for all new users")
        return True
    else:
        print("❌ Rich Menu setup failed")
        return False

if __name__ == '__main__':
    setup_rich_menu()
