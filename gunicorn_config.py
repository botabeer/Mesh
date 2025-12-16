import os
import multiprocessing

# ==== الإعدادات الأساسية ====
PORT = int(os.getenv("PORT", 8080))
ENV = os.getenv("ENV", "production")

bind = f"0.0.0.0:{PORT}"
workers = 1 if ENV == "development" else min(multiprocessing.cpu_count() * 2 + 1, 8)
threads = 2 if ENV == "development" else 4

# ==== وقت الاستجابة والتحكم بالطلبات ====
timeout = 60               # المهلة لكل طلب
graceful_timeout = 30      # مهلة الإغلاق
keepalive = 5              # الاحتفاظ بالاتصال

max_requests = 2000        # إعادة تشغيل العامل بعد عدد معين من الطلبات
max_requests_jitter = 100  # عشوائية لتجنب الإغلاق المتزامن للعمال

# ==== السجلات ====
loglevel = "info"
accesslog = "-"            # السجل يظهر على stdout
errorlog = "-"

# ==== خيارات إضافية ====
preload_app = True         # تحميل التطبيق قبل إنشاء العمال
reload = ENV == "development"  # إعادة التحميل التلقائي في التطوير
worker_class = "gthread"   # استخدام خيوط Gthread للطلبات المتعددة

proc_name = "bot-mesh"
daemon = False
