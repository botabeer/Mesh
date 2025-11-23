#!/bin/bash
# إصلاح تعارض نسخة Python

echo "🔧 إصلاح نسخة Python..."

# تحديث runtime.txt
echo "python-3.11.7" > runtime.txt
echo "✅ runtime.txt محدّث"

# تحديث render.yaml
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
echo "✅ render.yaml محدّث"

echo ""
echo "🎉 تم التوحيد على Python 3.11.7"
