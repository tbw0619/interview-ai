# 工業高校生向け面接対策AI - デプロイメント手順書

## 🌐 公開方法の選択肢

### 1. Heroku + GitHub Pages（推奨・無料）

#### バックエンド（Heroku）
```bash
# 1. Heroku CLIをインストール
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Herokuアプリを作成
heroku create your-interview-ai-backend

# 3. 環境変数を設定
heroku config:set OPENAI_API_KEY=your-actual-api-key
heroku config:set OPENAI_MODEL=gpt-4o-mini
heroku config:set DEBUG=False
heroku config:set ALLOWED_ORIGINS=https://yourusername.github.io

# 4. デプロイ
git add .
git commit -m "Deploy to production"
git push heroku main
```

#### フロントエンド（GitHub Pages）
```bash
# 1. GitHubリポジトリを作成
# 2. frontend/index.htmlでAPIエンドポイントを更新
# const response = await fetch('https://your-interview-ai-backend.herokuapp.com/chat', {

# 3. GitHub Pagesを有効化
# リポジトリ Settings > Pages > Source: Deploy from a branch > main/frontend
```

### 2. Docker + VPS

```bash
# 1. サーバーにDocker、Docker Composeをインストール

# 2. 環境変数ファイルを作成
cp backend/.env.example backend/.env
# .envファイルを編集してAPIキーを設定

# 3. アプリケーションを起動
docker-compose up -d

# 4. ファイアウォール設定
sudo ufw allow 3000  # フロントエンド
sudo ufw allow 8000  # バックエンド
```

### 3. 学校サーバー（内部公開）

```bash
# 1. Pythonとnpmがインストールされていることを確認
python --version  # 3.11以上
npm --version

# 2. 依存関係をインストール
cd backend
pip install -r requirements.txt

# 3. 環境変数を設定
cp .env.example .env
# .envファイルを編集

# 4. サーバー起動
python server.py

# 5. Webサーバー（Apache/Nginx）でfrontendを配信
# frontend/index.htmlのAPIエンドポイントを学校サーバーのIPに変更
```

## 🔐 セキュリティチェックリスト

### 本番公開前の必須設定

- [ ] OpenAI APIキーを環境変数で管理
- [ ] `.env`ファイルを`.gitignore`に追加
- [ ] CORS設定を適切なドメインに限定
- [ ] HTTPS通信を使用
- [ ] セキュリティヘッダーを設定
- [ ] ログレベルを適切に設定

### 環境変数設定例
```env
OPENAI_API_KEY=sk-your-actual-openai-api-key
OPENAI_MODEL=gpt-4o-mini
HOST=0.0.0.0
PORT=8000
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com,https://anotherdomain.com
```

## 💰 コスト概算

### OpenAI API利用料金
- **gpt-4o-mini**: 
  - Input: $0.15 / 1M tokens
  - Output: $0.6 / 1M tokens
- **1回の面接練習**: 約$0.01-0.02
- **月100人利用**: 約$10-20

### ホスティング料金
- **Heroku**: 無料枠あり（制限あり）
- **GitHub Pages**: 完全無料
- **VPS**: 月$5-20
- **学校サーバー**: 無料（既存インフラ利用）

## 🚀 推奨デプロイメント方法

### 小規模（クラス単位）
**Heroku + GitHub Pages**
- コスト: 無料〜月$10
- セットアップ: 簡単
- 管理: 最小限

### 中規模（学校全体）
**VPS + Docker**
- コスト: 月$10-30
- セットアップ: 中程度
- 管理: 定期的なメンテナンス

### 大規模（複数校）
**AWS/GCP**
- コスト: 従量課金
- セットアップ: 複雑
- 管理: 専門知識必要

## 🔧 トラブルシューティング

### よくある問題と解決方法

1. **CORS エラー**
   ```
   解決: ALLOWED_ORIGINSにフロントエンドのドメインを追加
   ```

2. **OpenAI API エラー**
   ```
   解決: APIキーが正しく設定されているか確認
   ```

3. **音声認識が動かない**
   ```
   解決: HTTPS環境で実行する（HTTP不可）
   ```

4. **VOICEVOX音声が再生されない**
   ```
   解決: VOICEVOXを別途起動する（オプション機能）
   ```

## 📝 メンテナンス

### 定期的な作業
- [ ] OpenAI API使用量の監視
- [ ] サーバーのリソース使用状況確認
- [ ] セキュリティアップデートの適用
- [ ] ログの確認とクリーンアップ

### 監視項目
- API応答時間
- エラー率
- 同時接続数
- ディスク使用量

## 📞 サポート

技術的な問題や追加機能の要望があれば、GitHub Issuesまたは直接お問い合わせください。

---

**注意**: 本番公開前に必ずテスト環境で動作確認を行い、OpenAI APIキーなどの機密情報が公開されていないことを確認してください。