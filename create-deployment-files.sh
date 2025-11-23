#!/bin/bash
# إنشاء ملفات النشر المفقودة

echo "📦 إنشاء ملفات النشر..."
echo ""

# ===== .env.example =====
cat > .env.example << 'EOF'
# LINE Bot Credentials (REQUIRED)
LINE_CHANNEL_ACCESS_TOKEN=your_token_here
LINE_CHANNEL_SECRET=your_secret_here

# Database
DB_PATH=data/game.db

# Redis (Optional)
REDIS_ENABLED=false
REDIS_URL=redis://localhost:6379/0

# Cache
CACHE_TTL=3600

# Application
PORT=5000
DEBUG=false
EOF
echo "✅ .env.example"

# ===== .gitignore =====
cat > .gitignore << 'EOF'
# Environment
.env
*.env
!.env.example

# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
.venv/
env/
ENV/

# Database
*.db
*.db-journal
data/

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Logs
*.log
logs/

# Distribution
dist/
build/
*.egg-info/
EOF
echo "✅ .gitignore"

# ===== Procfile (Heroku) =====
cat > Procfile << 'EOF'
web: gunicorn app:app --workers 2 --threads 2 --timeout 60 --bind 0.0.0.0:$PORT
EOF
echo "✅ Procfile"

# ===== Dockerfile =====
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directory
RUN mkdir -p /app/data && chmod 755 /app/data

# Create non-root user
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

USER botuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

EXPOSE 5000

CMD ["python", "app.py"]
EOF
echo "✅ Dockerfile"

# ===== docker-compose.yml =====
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  bot:
    build: .
    container_name: bot-mesh
    ports:
      - "5000:5000"
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  # Redis (Optional)
  redis:
    image: redis:7-alpine
    container_name: bot-mesh-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
EOF
echo "✅ docker-compose.yml"

# ===== .dockerignore =====
cat > .dockerignore << 'EOF'
.git
.gitignore
__pycache__
*.py[cod]
.Python
venv/
.venv/
*.db
data/
.vscode/
.idea/
.DS_Store
*.log
.env
README.md
tests/
*.md
EOF
echo "✅ .dockerignore"

# ===== README.md =====
cat > README.md << 'EOF'
# 🎮 Bot Mesh

بوت LINE للألعاب الترفيهية التفاعلية

## ✨ المميزات

- 12 لعبة تفاعلية متنوعة
- 7 ثيمات جميلة
- نظام نقاط وصدارة
- واجهة Flex Messages احترافية
- دعم المجموعات والدردشات الفردية

## 🎯 الألعاب المتوفرة

1. 🧠 **ذكاء** - ألغاز وأسئلة
2. 🎨 **لون** - تأثير Stroop
3. 🔤 **ترتيب** - ترتيب الحروف
4. 🔢 **رياضيات** - عمليات حسابية
5. ⚡ **أسرع** - كتابة سريعة
6. ↔️ **ضد** - الأضداد
7. ✏️ **تكوين** - تكوين كلمات
8. 🎵 **أغنية** - تخمين المغني
9. 🎯 **لعبة** - إنسان حيوان نبات
10. ⛓️ **سلسلة** - سلسلة الكلمات
11. 🤔 **خمن** - التخمين بالفئات
12. 💖 **توافق** - التوافق بين الأسماء

## 🚀 التثبيت والتشغيل

### المتطلبات
- Python 3.11+
- حساب LINE Developer

### التثبيت

```bash
# Clone the repository
git clone <your-repo>
cd bot-mesh

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your credentials

# Run the bot
python app.py
```

### باستخدام Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 📦 النشر

### Render
1. Push إلى GitHub
2. إنشاء Web Service جديد في Render
3. ربط Repository
4. إضافة Environment Variables

### Railway
```bash
railway login
railway init
railway up
```

### Heroku
```bash
heroku create bot-mesh
git push heroku main
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=xxx
heroku config:set LINE_CHANNEL_SECRET=xxx
```

## 🎨 الثيمات المتوفرة

- ⚪ أبيض (white)
- ⚫ أسود (black)
- ⬜ رمادي (gray)
- 🔵 أزرق (blue)
- 🟣 بنفسجي (purple)
- 💗 وردي (pink)
- 🍃 نعناعي (mint)

## 📝 الأوامر

- `بداية` / `@botmesh` - القائمة الرئيسية
- `نقاطي` - عرض النقاط والإحصائيات
- `الصدارة` - لوحة المتصدرين
- `ثيم` - تغيير الثيم
- `إيقاف` - إيقاف اللعبة الحالية

## 🛠️ التطوير

```bash
# Run tests
pytest

# Format code
black .

# Check types
mypy .
```

## 📄 الترخيص

Created by: Abeer Aldosari © 2025

## 🤝 المساهمة

المساهمات مرحب بها! الرجاء فتح Issue أو Pull Request.
EOF
echo "✅ README.md"

echo ""
echo "═══════════════════════════════════"
echo "✅ تم إنشاء جميع ملفات النشر بنجاح!"
echo "═══════════════════════════════════"
echo ""
echo "📝 الخطوات التالية:"
echo "1. نسخ .env.example إلى .env"
echo "2. إضافة بيانات LINE Bot"
echo "3. تشغيل: python app.py"
echo ""
