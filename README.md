# Mesh-main (محسّن)
مشروع ألعاب Python/Flask (أو تطبيق خفيف) — قمت بإجراء تحسينات بنيوية أولية:
- تنظيف ملفات النص من نهايات الأسطر الزائدة
- تأكدت من صلاحية الملفات (syntax OK)
- أضفت هذا README وتعليمات تشغيل أساسية

### تشغيل محلي (تقريبي)
1. إنشاء بيئة افتراضية: `python -m venv venv && source venv/bin/activate`  
2. تثبيت المتطلبات: `pip install -r requirements.txt`  
3. تشغيل التطبيق: `python app.py` أو `gunicorn app:app`

### ملاحظات
- راجع `Dockerfile` و`render.yaml` للنشر في خدمات الحاويات.  
- الملف الأصلي الذي استلمته: `/mnt/data/Mesh-main 37.zip`


---
## نشر المشروع (Docker)

1. إنشاء ملف متغيرات البيئة `.env` بالاعتماد على `.env.example` وملء القيم الحقيقية.
2. بناء الصورة (من نفس مجلد المشروع):
   ```bash
   docker build -t mesh-main:latest .
   ```
3. تشغيل الحاوية محليًا (مُرَبِط بالمنفذ 8080):
   ```bash
   docker run --env-file .env -p 8080:8080 mesh-main:latest
   ```
4. بدلاً من ذلك، يمكنك استخدام `docker-compose` أو نشرها على أي مزود يدعم Docker (Render, Heroku container registry, AWS ECS, DigitalOcean App Platform).
\n\n---\n\n## نقاط وLeaderboard - الاستخدام السريع\n
مثال: استخدام PointsEngine وLeaderboard داخل app أو ألعاب:\n\n```python\nfrom core.points import PointsEngine\nfrom core.leaderboard import Leaderboard\npe = PointsEngine()\nlb = Leaderboard()\npe.add(user_id=123, amount=50, reason='win')\nlb.update_user(123)\nprint(lb.top(10))\n```


---

## نشر مع Redis (محليًا باستخدام docker-compose)

1. قم بملء ملف `.env` بالقيم اللازمة.
2. شغّل:

```
docker-compose up --build -d
```

3. الخدمة ستكون متاحة على http://localhost:8080

4. Leaderboard سيستخدم Redis إذا كانت `REDIS_URL` معرفّة في `.env` أو عند تشغيل docker-compose.

