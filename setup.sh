#!/bin/bash
# Bot Mesh - Setup Script
# Created by: Abeer Aldosari © 2025

set -e

echo "🎮 Bot Mesh - Setup Script"
echo "=========================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Create directory structure
echo -e "${YELLOW}📁 Creating directory structure...${NC}"
mkdir -p bot-mesh/{games,data,monitoring/grafana/provisioning}

cd bot-mesh

# Create main files
echo -e "${YELLOW}📄 Creating main files...${NC}"

# Create .gitignore
cat > .gitignore << 'EOF'
# Environment
.env
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
.Python
venv/
.venv/

# Database
*.db
data/

# IDE
.vscode/
.idea/

# Logs
*.log
logs/

# Docker
.docker/
EOF

# Create README.md
cat > README.md << 'EOF'
# 🎮 Bot Mesh

Professional Gaming Bot for LINE

## Quick Start

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your credentials

# Run with Docker
docker-compose up -d

# Or run locally
pip install -r requirements.txt
python app.py
```

## Created by
Abeer Aldosari © 2025
EOF

echo -e "${GREEN}✅ Basic structure created!${NC}"
echo ""
echo "📝 Next steps:"
echo "1. Copy all Python files to their respective locations"
echo "2. Copy .env.example and rename to .env"
echo "3. Add your LINE Bot credentials"
echo "4. Run: docker-compose up -d"
echo ""
echo "🎉 Setup complete!"
