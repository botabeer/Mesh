#!/usr/bin/env python3
"""
Bot Mesh - Rich Menu Creator
Creates permanent buttons at the bottom of LINE chat
Created by: Abeer Aldosari © 2025
"""
import os
import sys
import requests
import json
from PIL import Image, ImageDraw, ImageFont

# LINE Bot credentials
CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_TOKEN_HERE')

def create_rich_menu_image():
    """إنشاء صورة Rich Menu 2500x843"""
    print("🎨 Creating Rich Menu image...")
    
    # الألوان
    bg_color = "#1A1A2E"
    button_colors = [
        "#667EEA",  # انضم
        "#00D9FF",  # ذكاء
        "#68D391",  # لون
        "#F687B3",  # ضد
        "#9F7AEA",  # ثيم
        "#FC8181"   # نقاطي
    ]
    
    # إنشاء الصورة
    img = Image.new('RGB', (2500, 843), bg_color)
    draw = ImageDraw.Draw(img)
    
    # الأزرار
    buttons = [
        {"x": 0, "y": 0, "w": 833, "h": 843, "emoji": "🔑", "text": "انضم", "color": button_colors[0]},
        {"x": 833, "y": 0, "w": 834, "h": 421, "emoji": "🧠", "text": "ذكاء", "color": button_colors[1]},
        {"x": 833, "y": 421, "w": 834, "h": 422, "emoji": "🎨", "text": "لون", "color": button_colors[2]},
        {"x": 1667, "y": 0, "w": 833, "h": 281, "emoji": "↔️", "text": "ضد", "color": button_colors[3]},
        {"x": 1667, "y": 281, "w": 833, "h": 281, "emoji": "🎨", "text": "ثيم", "color": button_colors[4]},
        {"x": 1667, "y": 562, "w": 833, "h": 281, "emoji": "📊", "text": "نقاطي", "color": button_colors[5]}
    ]
    
    # رسم الأزرار
    for btn in buttons:
        padding = 8
        # خلفية الزر
        draw.rounded_rectangle(
            [btn['x'] + padding, btn['y'] + padding, 
             btn['x'] + btn['w'] - padding, btn['y'] + btn['h'] - padding],
            radius=20,
            fill=btn['color']
        )
        
        # النص
        text = f"{btn['emoji']}\n{btn['text']}"
        # استخدام خط افتراضي
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        # حساب موضع النص
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        x = btn['x'] + (btn['w'] - text_w) // 2
        y = btn['y'] + (btn['h'] - text_h) // 2
        
        draw.text((x, y), text, fill="#FFFFFF", font=font, align="center")
    
    # حفظ الصورة
    img.save("rich_menu.png", "PNG")
    print("✅ Image saved: rich_menu.png")
    return "rich_menu.png"

def create_rich_menu():
    """إنشاء Rich Menu عبر LINE API"""
    print("📋 Creating Rich Menu structure...")
    
    url = "https://api.line.me/v2/bot/richmenu"
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    rich_menu = {
        "size": {"width": 2500, "height": 843},
        "selected": True,
        "name": "Bot Mesh Menu",
        "chatBarText": "القائمة 🎮",
        "areas": [
            {
                "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
                "action": {"type": "message", "text": "انضم"}
            },
            {
                "bounds": {"x": 833, "y": 0, "width": 834, "height": 421},
                "action": {"type": "message", "text": "ذكاء"}
            },
            {
                "bounds": {"x": 833, "y": 421, "width": 834, "height": 422},
                "action": {"type": "message", "text": "لون"}
            },
            {
                "bounds": {"x": 1667, "y": 0, "width": 833, "height": 281},
                "action": {"type": "message", "text": "ضد"}
            },
            {
                "bounds": {"x": 1667, "y": 281, "width": 833, "height": 281},
                "action": {"type": "message", "text": "ثيم"}
            },
            {
                "bounds": {"x": 1667, "y": 562, "width": 833, "height": 281},
                "action": {"type": "message", "text": "نقاطي"}
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=rich_menu)
    
    if response.status_code == 200:
        rich_menu_id = response.json()['richMenuId']
        print(f"✅ Rich Menu created: {rich_menu_id}")
        return rich_menu_id
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return None

def upload_rich_menu_image(rich_menu_id, image_path):
    """رفع صورة Rich Menu"""
    print(f"📤 Uploading image for {rich_menu_id}...")
    
    url = f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content"
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "image/png"
    }
    
    with open(image_path, 'rb') as f:
        response = requests.post(url, headers=headers, data=f)
    
    if response.status_code == 200:
        print("✅ Image uploaded successfully")
        return True
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)
        return False

def set_default_rich_menu(rich_menu_id):
    """تعيين Rich Menu كافتراضي"""
    print(f"🔧 Setting {rich_menu_id} as default...")
    
    url = f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}"
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        print("✅ Rich Menu set as default")
        return True
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
        return False

def delete_all_rich_menus():
    """حذف جميع Rich Menus"""
    print("🗑️  Deleting existing Rich Menus...")
    
    url = "https://api.line.me/v2/bot/richmenu/list"
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        menus = response.json().get('richmenus', [])
        for menu in menus:
            menu_id = menu['richMenuId']
            delete_url = f"https://api.line.me/v2/bot/richmenu/{menu_id}"
            requests.delete(delete_url, headers=headers)
            print(f"  Deleted: {menu_id}")
        print(f"✅ Deleted {len(menus)} Rich Menu(s)")
    else:
        print(f"⚠️  Could not fetch existing menus: {response.status_code}")

def main():
    """Main function"""
    print("=" * 50)
    print("🎮 Bot Mesh - Rich Menu Creator")
    print("=" * 50)
    print()
    
    if CHANNEL_ACCESS_TOKEN == 'YOUR_TOKEN_HERE':
        print("❌ Error: Please set LINE_CHANNEL_ACCESS_TOKEN")
        print("   export LINE_CHANNEL_ACCESS_TOKEN='your_token'")
        sys.exit(1)
    
    # 1. حذف القديم
    delete_all_rich_menus()
    print()
    
    # 2. إنشاء الصورة
    image_path = create_rich_menu_image()
    print()
    
    # 3. إنشاء Rich Menu
    rich_menu_id = create_rich_menu()
    if not rich_menu_id:
        sys.exit(1)
    print()
    
    # 4. رفع الصورة
    if not upload_rich_menu_image(rich_menu_id, image_path):
        sys.exit(1)
    print()
    
    # 5. تعيين كافتراضي
    if not set_default_rich_menu(rich_menu_id):
        sys.exit(1)
    
    print()
    print("=" * 50)
    print("🎉 Rich Menu setup complete!")
    print("=" * 50)
    print()
    print("✅ Permanent buttons are now active in your LINE bot")
    print("🔄 Users may need to close and reopen the chat to see them")

if __name__ == "__main__":
    main()
