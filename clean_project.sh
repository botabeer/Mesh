#!/bin/bash
# 🎯 Clean Bot Mesh Project
# Created by: Abeer Aldosari © 2025

echo "🚀 بدء تنظيف المشروع..."

# حذف مجلد data بالكامل
if [ -d "data" ]; then
    rm -rf data
    echo "✅ تم حذف مجلد data"
fi

# حذف مجلد utils بالكامل
if [ -d "utils" ]; then
    rm -rf utils
    echo "✅ تم حذف مجلد utils"
fi

# حذف ملفات غير ضرورية في الجذر
rm -f .gitignore Procfile base_game.py clean_games.py database.py \
      flex_messages.py flex_styles.py flex_templates.py game_config.py \
      runtime.txt setup.sh bot.log game_scores.db .env

echo "✅ تم حذف الملفات غير الضرورية"

echo "🎉 مشروعك أصبح نظيف وجاهز!"
