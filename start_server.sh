#!/bin/bash

# 工業高校生向け面接対策AI - バックエンドサーバー起動スクリプト

echo "=== 工業高校生向け面接対策AI サーバー起動 ==="

# backend ディレクトリに移動
cd backend

# 依存関係がインストールされているかチェック
if [ ! -d "venv" ]; then
    echo "仮想環境を作成しています..."
    python -m venv venv
fi

# 仮想環境をアクティベート
echo "仮想環境をアクティベートしています..."
source venv/bin/activate || source venv/Scripts/activate 2>/dev/null

# 依存関係をインストール
echo "依存関係をインストールしています..."
pip install -r requirements.txt

# 環境変数ファイルの存在チェック
if [ ! -f ".env" ]; then
    echo "⚠️  警告: .env ファイルが見つかりません"
    echo "backend/.env ファイルを作成し、OpenAI APIキーを設定してください："
    echo "OPENAI_API_KEY=your-api-key-here"
    echo "OPENAI_MODEL=gpt-4o-mini"
    exit 1
fi

# サーバー起動
echo "サーバーを起動しています..."
echo "サーバーURL: http://localhost:8000"
echo "フロントエンド: frontend/index.html をブラウザで開いてください"
echo ""
echo "停止するには Ctrl+C を押してください"
echo ""

python server.py