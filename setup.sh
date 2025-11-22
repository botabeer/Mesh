#!/bin/bash
# Bot Mesh - Auto Setup Script
# Created by: Abeer Aldosari © 2025
# يُنشئ جميع الملفات المطلوبة تلقائياً

set -e

echo "🎮 Bot Mesh - Auto Setup"
echo "=========================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if running in correct directory
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Error: app.py not found${NC}"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo -e "${YELLOW}📁 Creating missing files...${NC}"
echo ""

# ===== Dockerfile =====
if [ ! -f "Dockerfile" ]; then
    echo -e "${YELLOW}Creating Dockerfile...${NC}"
    cat > Dockerfile << 'DOCKERFILE_EOF'
# Bot Mesh - Optimized Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data && chmod 755 /app/data

RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

EXPOSE 5000

CMD ["python", "app.py"]
DOCKERFILE_EOF
    echo -e "${GREEN}✅ Dockerfile created${NC}"
else
    echo -e "${GREEN}✅ Dockerfile exists${NC}"
fi

# ===== .dockerignore =====
if [ ! -f ".dockerignore" ]; then
    echo -e "${YELLOW}Creating .dockerignore...${NC}"
    cat > .dockerignore << 'DOCKERIGNORE_EOF'
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
DOCKERIGNORE_EOF
    echo -e "${GREEN}✅ .dockerignore created${NC}"
else
    echo -e "${GREEN}✅ .dockerignore exists${NC}"
fi

# ===== .gitignore =====
if [ ! -f ".gitignore" ]; then
    echo -e "${YELLOW}Creating .gitignore...${NC}"
    cat > .gitignore << 'GITIGNORE_EOF'
# Environment
.env
*.env
!.env.example

# Python
__pycache__/
*.py[cod]
.Python
venv/
.venv/

# Database
*.db
data/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store

# Logs
*.log
logs/
GITIGNORE_EOF
    echo -e "${GREEN}✅ .gitignore created${NC}"
else
    echo -e "${GREEN}✅ .gitignore exists${NC}"
fi

# ===== Procfile (for Heroku) =====
if [ ! -f "Procfile" ]; then
    echo -e "${YELLOW}Creating Procfile...${NC}"
    cat > Procfile << 'PROCFILE_EOF'
web: gunicorn app:app --workers 2 --timeout 60 --bind 0.0.0.0:$PORT
PROCFILE_EOF
    echo -e "${GREEN}✅ Procfile created${NC}"
else
    echo -e "${GREEN}✅ Procfile exists${NC}"
fi

# ===== runtime.txt (for Heroku) =====
if [ ! -f "runtime.txt" ]; then
    echo -e "${YELLOW}Creating runtime.txt...${NC}"
    echo "python-3.11.7" > runtime.txt
    echo -e "${GREEN}✅ runtime.txt created${NC}"
else
    echo -e "${GREEN}✅ runtime.txt exists${NC}"
fi

# ===== requirements.txt check =====
if [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}Creating requirements.txt...${NC}"
    cat > requirements.txt << 'REQUIREMENTS_EOF'
line-bot-sdk==3.5.0
Flask==3.0.0
gunicorn==21.2.0
google-generativeai==0.3.2
redis==5.0.1
python-dotenv==1.0.0
Pillow==10.1.0
prometheus-client==0.19.0
REQUIREMENTS_EOF
    echo -e "${GREEN}✅ requirements.txt created${NC}"
else
    echo -e "${GREEN}✅ requirements.txt exists${NC}"
fi

# ===== .env.example check =====
if [ ! -f ".env.example" ]; then
    echo -e "${YELLOW}Creating .env.example...${NC}"
    cat > .env.example << 'ENV_EOF'
# LINE Bot Credentials (REQUIRED)
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_CHANNEL_SECRET=your_channel_secret_here

# Google Gemini AI Keys (Optional)
GEMINI_API_KEY_1=your_gemini_api_key_1
GEMINI_API_KEY_2=
GEMINI_API_KEY_3=

# Redis (Optional)
REDIS_URL=redis://redis:6379/0
REDIS_ENABLED=false

# Database
DB_PATH=data
DB_NAME=game_scores.db

# Application
DEBUG=false
PORT=5000

# Monitoring
ENABLE_METRICS=true
ENV_EOF
    echo -e "${GREEN}✅ .env.example created${NC}"
else
    echo -e "${GREEN}✅ .env.example exists${NC}"
fi

# ===== Create .env if not exists =====
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env and add your LINE Bot credentials!${NC}"
else
    echo -e "${GREEN}✅ .env exists${NC}"
fi

# ===== Create data directory =====
if [ ! -d "data" ]; then
    echo -e "${YELLOW}Creating data directory...${NC}"
    mkdir -p data
    echo -e "${GREEN}✅ data/ created${NC}"
else
    echo -e "${GREEN}✅ data/ exists${NC}"
fi

# ===== Check games directory =====
if [ ! -d "games" ]; then
    echo -e "${RED}❌ Error: games/ directory not found${NC}"
    echo "Please create the games directory with all game files"
    exit 1
else
    echo -e "${GREEN}✅ games/ exists${NC}"
fi

# ===== Check games/__init__.py =====
if [ ! -f "games/__init__.py" ]; then
    echo -e "${YELLOW}Creating games/__init__.py...${NC}"
    cat > games/__init__.py << 'INIT_EOF'
"""Bot Mesh - Games Package | Abeer Aldosari © 2025"""
import os,sys,logging,importlib

__version__='2.0.0'
__author__='Abeer Aldosari'
__all__=[]

logger=logging.getLogger(__name__)
current_dir=os.path.dirname(__file__)

try:
    from .base_game import BaseGame
    __all__.append('BaseGame')
except ImportError as e:
    logger.error(f"❌ BaseGame: {e}")
    sys.exit(1)

for f in os.listdir(current_dir):
    if f.endswith("_game.py")and f!="base_game.py":
        m=f[:-3]
        try:
            module=importlib.import_module(f".{m}",package=__name__)
            __all__.append(m)
            logger.debug(f"✅ {m}")
        except Exception as e:
            logger.warning(f"⚠️ {m}: {e}")

logger.info(f"📦 Loaded: {len(__all__)} modules")
INIT_EOF
    echo -e "${GREEN}✅ games/__init__.py created${NC}"
else
    echo -e "${GREEN}✅ games/__init__.py exists${NC}"
fi

# ===== Summary =====
echo ""
echo "================================"
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo "================================"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Edit .env file with your LINE Bot credentials:"
echo "   nano .env"
echo ""
echo "2. Test locally:"
echo "   docker-compose up --build"
echo ""
echo "3. Or deploy to Railway:"
echo "   git add ."
echo "   git commit -m 'Add missing files'"
echo "   git push origin main"
echo ""
echo "4. Or deploy to Heroku:"
echo "   git push heroku main"
echo ""
echo -e "${YELLOW}⚠️  Don't forget to add your LINE credentials in .env!${NC}"
echo ""
