#!/bin/bash

# 工業高校生向け面接対策AI - 自動デプロイスクリプト

set -e  # エラー時に停止

echo "🚀 工業高校生向け面接対策AI - Heroku デプロイ開始"
echo ""

# 必要なツールの確認
command -v git >/dev/null 2>&1 || { echo "❌ Git がインストールされていません"; exit 1; }
command -v heroku >/dev/null 2>&1 || { echo "❌ Heroku CLI がインストールされていません"; exit 1; }

# Herokuにログインしているか確認
if ! heroku auth:whoami >/dev/null 2>&1; then
    echo "📝 Herokuにログインしてください"
    heroku login
fi

# アプリ名の入力
echo "📝 Herokuアプリ名を入力してください（例: yamada-high-interview-ai）:"
read -p "アプリ名: " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ アプリ名は必須です"
    exit 1
fi

echo "🔧 Herokuアプリを作成中: $APP_NAME"
if heroku create "$APP_NAME" 2>/dev/null; then
    echo "✅ アプリが作成されました"
else
    echo "⚠️  アプリが既に存在するか、別の問題が発生しました"
    echo "📝 既存のアプリを使用しますか？ (y/n)"
    read -p "回答: " USE_EXISTING
    if [ "$USE_EXISTING" != "y" ]; then
        echo "❌ デプロイを中断しました"
        exit 1
    fi
fi

# OpenAI APIキーの設定
echo ""
echo "🔑 OpenAI APIキーを設定してください"
echo "💡 APIキーは https://platform.openai.com で取得できます"
read -s -p "OpenAI APIキー: " OPENAI_API_KEY
echo ""

if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OpenAI APIキーは必須です"
    exit 1
fi

# 環境変数の設定
echo "⚙️ 環境変数を設定中..."
heroku config:set OPENAI_API_KEY="$OPENAI_API_KEY" --app "$APP_NAME"
heroku config:set OPENAI_MODEL=gpt-4o-mini --app "$APP_NAME"
heroku config:set DEBUG=False --app "$APP_NAME"
heroku config:set HOST=0.0.0.0 --app "$APP_NAME"
heroku config:set ALLOWED_ORIGINS="*" --app "$APP_NAME"

echo "✅ 環境変数を設定完了"

# Git設定の確認
if [ ! -d ".git" ]; then
    echo "📝 Gitリポジトリを初期化中..."
    git init
    git add .
    git commit -m "Initial commit: 工業高校生向け面接対策AI"
fi

# Herokuリモートの追加
echo "🔗 Herokuリモートを設定中..."
if git remote get-url heroku >/dev/null 2>&1; then
    git remote remove heroku
fi
heroku git:remote -a "$APP_NAME"

# デプロイ実行
echo "🚀 デプロイを開始中..."
git add .
git commit -m "Deploy to production" || echo "⚠️  変更がないか、既にコミット済みです"
git push heroku main

# デプロイ結果の確認
echo ""
echo "🔍 デプロイ結果を確認中..."
sleep 5

if heroku logs --tail --num 10 --app "$APP_NAME" | grep -q "Uvicorn running"; then
    echo "✅ デプロイ成功！"
    echo ""
    echo "🌐 アプリケーションURL:"
    heroku info --app "$APP_NAME" | grep "Web URL"
    echo ""
    echo "📝 次のステップ:"
    echo "1. frontend/config.js の production.baseURL を上記URLに更新"
    echo "2. GitHub Pages でフロントエンドを公開"
    echo "3. CORS設定を正しいドメインに更新"
    echo ""
    echo "🎉 公開準備完了！"
else
    echo "❌ デプロイに問題があります。ログを確認してください:"
    heroku logs --tail --num 20 --app "$APP_NAME"
fi