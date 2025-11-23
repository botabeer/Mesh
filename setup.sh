#!/bin/bash
# Bot Mesh - Final Setup Script
# Created by: Abeer Aldosari © 2025

set -e

echo "╔════════════════════════════════════╗"
echo "║   🎮 Bot Mesh - Final Setup       ║"
echo "║   Created by: Abeer Aldosari      ║"
echo "╚════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# ===== 1. إنشاء المجلدات =====
echo -e "${BLUE}📁 إنشاء المجلدات...${NC}"
mkdir -p data games
echo -e "${GREEN}✅ data/ و games/ جاهزة${NC}"
echo ""

# ===== 2. إنشاء .env =====
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}📝 إنشاء ملف .env...${NC}"
    cat > .env << 'EOF'
# LINE Bot Credentials (REQUIRED)
LINE_CHANNEL_ACCESS_TOKEN=your_token_here
LINE_CHANNEL_SECRET=your_secret_here

# Database
DB_PATH=data/game.db

# Redis (Optional)
REDIS_ENABLED=false
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600

# Application
PORT=5000
DEBUG=false
EOF
    echo -e "${GREEN}✅ .env${NC}"
    echo -e "${RED}⚠️  لا تنسَ تعديل LINE_CHANNEL_ACCESS_TOKEN و LINE_CHANNEL_SECRET${NC}"
else
    echo -e "${GREEN}✅ .env موجود${NC}"
fi
echo ""

# ===== 3. إنشاء .gitignore =====
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

# Database
*.db
*.db-journal
data/

# IDE
.vscode/
.idea/
*.swp
.DS_Store

# Logs
*.log
logs/

# Distribution
dist/
build/
*.egg-info/
EOF
echo -e "${GREEN}✅ .gitignore${NC}"

# ===== 4. إنشاء runtime.txt =====
echo "python-3.11.7" > runtime.txt
echo -e "${GREEN}✅ runtime.txt (Python 3.11.7)${NC}"

# ===== 5. إنشاء Procfile =====
cat > Procfile << 'EOF'
web: gunicorn app:app --workers 2 --threads 2 --timeout 60 --bind 0.0.0.0:$PORT
EOF
echo -e "${GREEN}✅ Procfile${NC}"

# ===== 6. تحديث render.yaml =====
cat > render.yaml << 'EOF'
services:
  - type: web
    name: bot-mesh
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 60
    envVars:
      - key: LINE_CHANNEL_ACCESS_TOKEN
        sync: false
      - key: LINE_CHANNEL_SECRET
        sync: false
      - key: DB_PATH
        value: data/game.db
      - key: PYTHON_VERSION
        value: 3.11.7
    healthCheckPath: /health
EOF
echo -e "${GREEN}✅ render.yaml${NC}"

# ===== 7. إنشاء Dockerfile =====
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data && chmod 755 /app/data

RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

USER botuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

EXPOSE 5000

CMD ["python", "app.py"]
EOF
echo -e "${GREEN}✅ Dockerfile${NC}"

# ===== 8. إنشاء docker-compose.yml =====
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

volumes:
  data:
EOF
echo -e "${GREEN}✅ docker-compose.yml${NC}"

# ===== 9. إنشاء .dockerignore =====
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
EOF
echo -e "${GREEN}✅ .dockerignore${NC}"

# ===== 10. فحص الملفات الأساسية =====
echo ""
echo -e "${BLUE}🔍 فحص الملفات الأساسية...${NC}"

required_files=(
    "app.py"
    "config.py"
    "database.py"
    "game_manager.py"
    "flex_builder.py"
    "cache.py"
    "requirements.txt"
    "games/__init__.py"
    "games/base_game.py"
)

missing_files=()

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅${NC} $file"
    else
        echo -e "${RED}❌${NC} $file"
        missing_files+=("$file")
    fi
done

# ===== 11. النتيجة النهائية =====
echo ""
echo "════════════════════════════════════"

if [ ${#missing_files[@]} -eq 0 ]; then
    echo -e "${GREEN}🎉 الإعداد مكتمل بنجاح!${NC}"
    echo "════════════════════════════════════"
    echo ""
    echo -e "${BLUE}📋 الخطوات التالية:${NC}"
    echo ""
    echo "1️⃣  تعديل .env وإضافة بيانات LINE Bot:"
    echo "   nano .env"
    echo ""
    echo "2️⃣  تثبيت المتطلبات (اختياري للاختبار المحلي):"
    echo "   python3.11 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    echo ""
    echo "3️⃣  اختبار محلي:"
    echo "   python app.py"
    echo "   # ثم استخدم ngrok:"
    echo "   ngrok http 5000"
    echo ""
    echo "4️⃣  النشر على Render:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git push origin main"
    echo "   # ثم اربط في Render Dashboard"
    echo ""
    echo -e "${YELLOW}💡 نصيحة: استخدم Render للنشر المجاني والسهل${NC}"
else
    echo -e "${RED}⚠️  بعض الملفات مفقودة:${NC}"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo ""
    echo "الرجاء التأكد من وجود جميع الملفات"
fi

echo ""
echo "════════════════════════════════════"
echo -e "${BLUE}Created by: Abeer Aldosari © 2025${NC}"
echo "════════════════════════════════════"
