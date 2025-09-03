@echo off
chcp 65001 >nul
echo === 工業高校生向け面接対策AI サーバー起動 ===
echo.

cd backend

if not exist "venv" (
    echo 仮想環境を作成しています...
    python -m venv venv
)

echo 仮想環境をアクティベートしています...
call venv\Scripts\activate.bat

echo 依存関係をインストールしています...
pip install -r requirements.txt

if not exist ".env" (
    echo.
    echo ⚠️  警告: .env ファイルが見つかりません
    echo backend\.env ファイルを作成し、OpenAI APIキーを設定してください：
    echo OPENAI_API_KEY=your-api-key-here
    echo OPENAI_MODEL=gpt-4o-mini
    echo.
    pause
    exit /b 1
)

echo.
echo サーバーを起動しています...
echo サーバーURL: http://localhost:8000
echo フロントエンド: frontend\index.html をブラウザで開いてください
echo.
echo 停止するには Ctrl+C を押してください
echo.

python server.py
pause