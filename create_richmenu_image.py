"""
Bot Mesh - Rich Menu Image Generator
Created by: Abeer Aldosari © 2025
إنشاء صورة Rich Menu بأبعاد 2500x1686
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_rich_menu_image(output_path='rich_menu.png'):
    """إنشاء صورة Rich Menu"""
    
    # الأبعاد المطلوبة
    width = 2500
    height = 1686
    
    # إنشاء الصورة
    img = Image.new('RGB', (width, height), color='#E0E5EC')
    draw = ImageDraw.Draw(img)
    
    # محاولة تحميل خط عربي
    try:
        # للويندوز
        font_large = ImageFont.truetype("arial.ttf", 80)
        font_small = ImageFont.truetype("arial.ttf", 50)
    except:
        try:
            # للينكس
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 80)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
        except:
            # افتراضي
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # تعريف الألعاب مع الإيموجي
    games = [
        # الصف الأول
        [("🧠", "ذكاء"), ("🎨", "لون"), ("abc", "ترتيب")],
        # الصف الثاني
        [("🔢", "رياضيات"), ("⚡", "أسرع"), ("↔️", "ضد")],
        # الصف الثالث
        [("✏️", "تكوين"), ("🎵", "أغنية"), ("🎯", "لعبة")],
        # الصف الرابع
        [("🔗", "سلسلة"), ("🤔", "خمن"), ("💕", "توافق")]
    ]
    
    # أبعاد الخلايا
    cell_width = 833
    cell_height = 421
    
    # رسم الألعاب (3 صفوف)
    for row_idx, row in enumerate(games[:3]):
        y = row_idx * cell_height
        for col_idx, (emoji, name) in enumerate(row):
            x = col_idx * cell_width
            
            # رسم الخلفية
            color = '#D1D9E6' if (row_idx + col_idx) % 2 == 0 else '#C5CDD8'
            draw.rectangle([x, y, x + cell_width, y + cell_height], fill=color, outline='#667EEA', width=3)
            
            # رسم الإيموجي والنص
            text = f"{emoji}\n{name}"
            bbox = draw.textbbox((0, 0), text, font=font_large)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = x + (cell_width - text_width) // 2
            text_y = y + (cell_height - text_height) // 2
            draw.text((text_x, text_y), text, fill='#2C3E50', font=font_large, align='center')
    
    # الصف الرابع (3 ألعاب + 2 أزرار)
    y = 3 * cell_height
    
    # 3 ألعاب أصغر
    small_cell_width = 625
    for col_idx, (emoji, name) in enumerate(games[3]):
        x = col_idx * small_cell_width
        
        color = '#D1D9E6' if col_idx % 2 == 0 else '#C5CDD8'
        draw.rectangle([x, y, x + small_cell_width, y + cell_height], fill=color, outline='#667EEA', width=3)
        
        text = f"{emoji}\n{name}"
        bbox = draw.textbbox((0, 0), text, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x + (small_cell_width - text_width) // 2
        text_y = y + (cell_height - text_height) // 2
        draw.text((text_x, text_y), text, fill='#2C3E50', font=font_small, align='center')
    
    # زر انسحب
    x = 3 * small_cell_width
    button_width = 312
    draw.rectangle([x, y, x + button_width, y + cell_height], fill='#F59E0B', outline='#D97706', width=3)
    text = "🚪\nانسحب"
    bbox = draw.textbbox((0, 0), text, font=font_small)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = x + (button_width - text_width) // 2
    text_y = y + (cell_height - text_height) // 2
    draw.text((text_x, text_y), text, fill='#FFFFFF', font=font_small, align='center')
    
    # زر إيقاف
    x = 3 * small_cell_width + button_width
    draw.rectangle([x, y, x + button_width, y + cell_height], fill='#EF4444', outline='#DC2626', width=3)
    text = "🛑\nإيقاف"
    bbox = draw.textbbox((0, 0), text, font=font_small)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = x + (button_width - text_width) // 2
    text_y = y + (cell_height - text_height) // 2
    draw.text((text_x, text_y), text, fill='#FFFFFF', font=font_small, align='center')
    
    # حفظ الصورة
    img.save(output_path)
    print(f"✅ Rich menu image created: {output_path}")
    print(f"📐 Dimensions: {width}x{height}")
    return output_path

if __name__ == '__main__':
    create_rich_menu_image()
