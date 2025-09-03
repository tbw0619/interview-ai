# 工業高校生向け面接対策AI

音声入力を使った工業高校生向けの面接練習アプリケーションです。Web Speech APIを使用した音声認識とOpenAI APIを活用したAI面接官により、リアルな面接練習を提供します。

## 特徴

- 🎤 **音声入力対応**: ブラウザのWeb Speech APIを使用した無料の音声認識
- 🎓 **2つの面接モード**: 就職面接と進学面接に対応
- 🤖 **AI面接官**: OpenAI APIを使用したインテリジェントなフィードバック
- 💬 **チャット形式UI**: 使いやすい会話インターフェース
- 📱 **レスポンシブデザイン**: モバイル・デスクトップ対応

## プロジェクト構造

```
.
├── backend/
│   ├── server.py          # FastAPI サーバー
│   ├── requirements.txt   # Python 依存関係
│   └── .env              # 環境変数 (OpenAI APIキー)
├── frontend/
│   └── index.html        # フロントエンド (HTML + JavaScript)
└── README.md
```

## セットアップ手順

### 1. 依存関係のインストール

```bash
cd backend
pip install -r requirements.txt
```

### 2. 環境変数の設定

`backend/.env` ファイルを編集し、OpenAI APIキーを設定してください：

```env
OPENAI_API_KEY=your-actual-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

### 3. バックエンドサーバーの起動

```bash
cd backend
python server.py
```

または uvicorn を直接使用：

```bash
cd backend
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

サーバーは `http://localhost:8000` で起動します。

### 4. フロントエンドの起動

`frontend/index.html` をブラウザで開いてください。

**重要**: 音声認識機能を使用するため、HTTPS環境またはlocalhost環境で実行してください。

## 使い方

1. ブラウザで `frontend/index.html` を開く
2. 面接モード（就職面接/進学面接）を選択
3. マイクボタンを押して録音開始
4. 質問に回答（音声で話す）
5. 録音停止後、必要に応じてテキストを編集
6. 「送信」ボタンでAI面接官に送信
7. AI面接官からのフィードバックを確認

## 面接モード

### 就職面接モード
- 製造業・技術職への就職を想定
- 安全・品質・5S を重視した指導
- PREP法による構成指導
- 工業高校生らしい体験談の活用

### 進学面接モード
- 大学・専門学校への進学を想定
- 学修計画・研究関心・将来像の明確化
- 高校での学習と進学先の関連性重視
- より高度な技術学習への意欲評価

## 技術スタック

### フロントエンド
- HTML5 + CSS3 + Vanilla JavaScript
- Web Speech API (音声認識)
- レスポンシブデザイン

### バックエンド
- Python 3.7+
- FastAPI (Web API フレームワーク)
- OpenAI API (gpt-4o-mini)
- uvicorn (ASGI サーバー)

## 注意事項

- OpenAI APIキーが必要です（有料サービス）
- 音声認識にはChrome/Edge等のモダンブラウザが必要
- HTTPSまたはlocalhostでの実行が推奨されます
- インターネット接続が必要です

## トラブルシューティング

### 音声認識が動作しない
- HTTPSまたはlocalhostで実行しているか確認
- ブラウザがマイクアクセスを許可しているか確認
- Chrome/Edge等の対応ブラウザを使用

### AIが応答しない
- OpenAI APIキーが正しく設定されているか確認
- バックエンドサーバーが起動しているか確認
- ネットワーク接続を確認

### CORSエラーが発生する
- バックエンドサーバーでCORSが有効になっているか確認
- フロントエンドのAPIエンドポイントURLが正しいか確認

## ライセンス

MIT License

## 貢献

プルリクエストやイシューの報告を歓迎します。

## サポート

技術的な質問や問題がある場合は、GitHubのIssuesをご利用ください。