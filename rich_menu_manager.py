"""
Bot Mesh - Rich Menu Manager
Created by: Abeer Aldosari © 2025
إدارة القوائم الثابتة (الأزرار السفلية)
"""
import logging
import requests
import json

logger = logging.getLogger(__name__)


class RichMenuManager:
    def __init__(self, channel_access_token):
        self.token = channel_access_token
        self.base_url = "https://api.line.me/v2/bot/richmenu"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def create_rich_menu(self):
        """إنشاء Rich Menu مع 12 لعبة + أزرار التحكم"""
        rich_menu_data = {
            "size": {
                "width": 2500,
                "height": 1686
            },
            "selected": True,
            "name": "Bot Mesh Games Menu",
            "chatBarText": "🎮 الألعاب",
            "areas": [
                # الصف الأول - 3 ألعاب
                {"bounds": {"x": 0, "y": 0, "width": 833, "height": 421}, "action": {"type": "message", "text": "ذكاء"}},
                {"bounds": {"x": 834, "y": 0, "width": 833, "height": 421}, "action": {"type": "message", "text": "لون"}},
                {"bounds": {"x": 1667, "y": 0, "width": 833, "height": 421}, "action": {"type": "message", "text": "ترتيب"}},
                
                # الصف الثاني - 3 ألعاب
                {"bounds": {"x": 0, "y": 422, "width": 833, "height": 421}, "action": {"type": "message", "text": "رياضيات"}},
                {"bounds": {"x": 834, "y": 422, "width": 833, "height": 421}, "action": {"type": "message", "text": "أسرع"}},
                {"bounds": {"x": 1667, "y": 422, "width": 833, "height": 421}, "action": {"type": "message", "text": "ضد"}},
                
                # الصف الثالث - 3 ألعاب
                {"bounds": {"x": 0, "y": 843, "width": 833, "height": 421}, "action": {"type": "message", "text": "تكوين"}},
                {"bounds": {"x": 834, "y": 843, "width": 833, "height": 421}, "action": {"type": "message", "text": "أغنية"}},
                {"bounds": {"x": 1667, "y": 843, "width": 833, "height": 421}, "action": {"type": "message", "text": "لعبة"}},
                
                # الصف الرابع - 3 ألعاب + أزرار
                {"bounds": {"x": 0, "y": 1264, "width": 625, "height": 422}, "action": {"type": "message", "text": "سلسلة"}},
                {"bounds": {"x": 626, "y": 1264, "width": 625, "height": 422}, "action": {"type": "message", "text": "خمن"}},
                {"bounds": {"x": 1251, "y": 1264, "width": 625, "height": 422}, "action": {"type": "message", "text": "توافق"}},
                {"bounds": {"x": 1876, "y": 1264, "width": 312, "height": 422}, "action": {"type": "message", "text": "انسحب"}},
                {"bounds": {"x": 2188, "y": 1264, "width": 312, "height": 422}, "action": {"type": "message", "text": "إيقاف"}}
            ]
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(rich_menu_data)
            )
            
            if response.status_code == 200:
                rich_menu_id = response.json()['richMenuId']
                logger.info(f"✅ Rich menu created: {rich_menu_id}")
                return rich_menu_id
            else:
                logger.error(f"❌ Failed to create rich menu: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error creating rich menu: {e}")
            return None
    
    def upload_rich_menu_image(self, rich_menu_id, image_path=None):
        """رفع صورة للـ Rich Menu"""
        # إذا لم تكن هناك صورة، نستخدم صورة افتراضية بسيطة
        # يمكنك إنشاء صورة 2500x1686 بكسل باستخدام أي برنامج تصميم
        
        if not image_path:
            logger.warning("⚠️ No image provided for rich menu")
            return False
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            url = f"{self.base_url}/{rich_menu_id}/content"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "image/png"
            }
            
            response = requests.post(url, headers=headers, data=image_data)
            
            if response.status_code == 200:
                logger.info(f"✅ Rich menu image uploaded for: {rich_menu_id}")
                return True
            else:
                logger.error(f"❌ Failed to upload image: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error uploading rich menu image: {e}")
            return False
    
    def link_rich_menu_to_user(self, user_id, rich_menu_id):
        """ربط Rich Menu بمستخدم محدد"""
        try:
            url = f"https://api.line.me/v2/bot/user/{user_id}/richmenu/{rich_menu_id}"
            response = requests.post(url, headers=self.headers)
            
            if response.status_code == 200:
                logger.info(f"✅ Rich menu linked to user: {user_id}")
                return True
            else:
                logger.error(f"❌ Failed to link rich menu: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error linking rich menu: {e}")
            return False
    
    def set_default_rich_menu(self, rich_menu_id):
        """تعيين Rich Menu كافتراضي لجميع المستخدمين"""
        try:
            url = f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}"
            response = requests.post(url, headers=self.headers)
            
            if response.status_code == 200:
                logger.info(f"✅ Default rich menu set: {rich_menu_id}")
                return True
            else:
                logger.error(f"❌ Failed to set default: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error setting default rich menu: {e}")
            return False
    
    def get_rich_menu_list(self):
        """الحصول على قائمة Rich Menus"""
        try:
            response = requests.get(self.base_url, headers=self.headers)
            
            if response.status_code == 200:
                menus = response.json().get('richmenus', [])
                logger.info(f"📋 Found {len(menus)} rich menus")
                return menus
            else:
                logger.error(f"❌ Failed to get rich menus: {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error getting rich menus: {e}")
            return []
    
    def delete_rich_menu(self, rich_menu_id):
        """حذف Rich Menu"""
        try:
            url = f"{self.base_url}/{rich_menu_id}"
            response = requests.delete(url, headers=self.headers)
            
            if response.status_code == 200:
                logger.info(f"✅ Rich menu deleted: {rich_menu_id}")
                return True
            else:
                logger.error(f"❌ Failed to delete: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error deleting rich menu: {e}")
            return False
    
    def create_and_link_rich_menu(self, user_id, image_path=None):
        """إنشاء وربط Rich Menu بمستخدم (دالة شاملة)"""
        # التحقق من وجود Rich Menu مسبقاً
        menus = self.get_rich_menu_list()
        
        if menus:
            # استخدام أول Rich Menu موجود
            rich_menu_id = menus[0]['richMenuId']
            logger.info(f"📋 Using existing rich menu: {rich_menu_id}")
        else:
            # إنشاء Rich Menu جديد
            rich_menu_id = self.create_rich_menu()
            if not rich_menu_id:
                return False
            
            # رفع الصورة إذا كانت متاحة
            if image_path:
                self.upload_rich_menu_image(rich_menu_id, image_path)
        
        # ربط بالمستخدم
        return self.link_rich_menu_to_user(user_id, rich_menu_id)
    
    def setup_default_menu(self, image_path=None):
        """إعداد Rich Menu الافتراضي لجميع المستخدمين"""
        # حذف القوائم القديمة
        old_menus = self.get_rich_menu_list()
        for menu in old_menus:
            self.delete_rich_menu(menu['richMenuId'])
        
        # إنشاء قائمة جديدة
        rich_menu_id = self.create_rich_menu()
        if not rich_menu_id:
            return False
        
        # رفع الصورة
        if image_path:
            self.upload_rich_menu_image(rich_menu_id, image_path)
        
        # تعيين كافتراضي
        return self.set_default_rich_menu(rich_menu_id)
