# 🚀 Heroku + GitHub Pages デプロイ手順書

## 📋 事前準備

### 必要なアカウント
1. **OpenAI アカウント** - [platform.openai.com](https://platform.openai.com)
2. **Heroku アカウント** - [heroku.com](https://heroku.com) （無料プランあり）
3. **GitHub アカウント** - [github.com](https://github.com) （無料）

### 必要なツール
1. **Git** - バージョン管理
2. **Heroku CLI** - [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

---

## 🔑 ステップ1: OpenAI APIキーを取得

1. [OpenAI Platform](https://platform.openai.com) にログイン
2. 「API keys」セクションに移動
3. 「Create new secret key」をクリック
4. 生成されたキーをコピー（後で使用）

**💡 重要**: APIキーは一度しか表示されないため、安全な場所に保存してください。

---

## 📤 ステップ2: GitHubリポジトリを作成

### 1. GitHubでリポジトリ作成
```bash
# GitHubでリポジトリを作成後、以下のコマンドを実行

git init
git add .
git commit -m "Initial commit: 工業高校生向け面接対策AI"
git branch -M main
git remote add origin https://github.com/yourusername/interview-ai.git
git push -u origin main
```

### 2. `.env`ファイルの設定確認
```bash
# .envファイルがGitに追加されていないことを確認
git status
# .envが表示されなければOK（.gitignoreで除外済み）
```

---

## 🚀 ステップ3: Herokuにバックエンドをデプロイ

### 1. Heroku CLIでログイン
```bash
heroku login
```

### 2. Herokuアプリを作成
```bash
heroku create your-interview-ai
# 例: heroku create yamada-high-interview-ai
```

### 3. 環境変数を設定
```bash
# OpenAI APIキーを設定
heroku config:set OPENAI_API_KEY=sk-your-actual-api-key-here

# その他の設定
heroku config:set OPENAI_MODEL=gpt-4o-mini
heroku config:set DEBUG=False
heroku config:set HOST=0.0.0.0
heroku config:set ALLOWED_ORIGINS="*"

# 設定確認
heroku config
```

### 4. デプロイ実行
```bash
git push heroku main
```

### 5. アプリの起動確認
```bash
# ログ確認
heroku logs --tail

# アプリを開く
heroku open
# ブラウザで {"message": "工業高校生向け面接対策API"} が表示されればOK
```

---

## 📱 ステップ4: GitHub Pagesでフロントエンドを公開

### 1. フロントエンド設定を更新
```bash
# frontend/config.js の production.baseURL を更新
# 'https://your-app-name.herokuapp.com' を実際のHerokuアプリのURLに変更
```

### 2. GitHub Pages設定
1. GitHubリポジトリのページに移動
2. **Settings** タブをクリック
3. 左メニューの **Pages** をクリック
4. **Source** を「Deploy from a branch」に設定
5. **Branch** を「main」、**Folder** を「/frontend」に設定
6. **Save** をクリック

### 3. 公開確認
- 5-10分後に `https://yourusername.github.io/interview-ai/` でアクセス可能
- 面接対策AIが正常に動作することを確認

---

## 🔧 ステップ5: 最終設定と動作確認

### 1. CORS設定の更新
```bash
# HerokuアプリのCORS設定を更新
heroku config:set ALLOWED_ORIGINS="https://yourusername.github.io"
```

### 2. 動作テスト
1. GitHub Pagesのサイトにアクセス
2. マイク権限を許可
3. 「模擬面接を開始する」をクリック
4. 音声入力でテスト回答
5. AIからのフィードバックを確認

---

## 📊 運用とメンテナンス

### 利用状況の監視
```bash
# Herokuのメトリクス確認
heroku metrics

# ログの確認
heroku logs --tail

# OpenAI API使用量の確認
# https://platform.openai.com/usage でAPI使用量を定期チェック
```

### アップデート手順
```bash
# コード修正後
git add .
git commit -m "Update: 機能改善"
git push origin main
git push heroku main  # バックエンドの更新

# フロントエンドは自動的に更新されます（GitHub Pages）
```

---

## 🎯 完成！アクセス情報

### 📱 生徒向けアクセスURL
```
https://yourusername.github.io/interview-ai/
```

### 🖥️ 管理者向け（バックエンドAPI）
```
https://your-app-name.herokuapp.com/
```

---

## ❓ トラブルシューティング

### よくある問題

#### 1. 「CORS エラー」が発生
```bash
# Herokuの環境変数を確認
heroku config:get ALLOWED_ORIGINS

# 正しいドメインを設定
heroku config:set ALLOWED_ORIGINS="https://yourusername.github.io"
```

#### 2. 「OpenAI API エラー」が発生
```bash
# APIキーを確認
heroku config:get OPENAI_API_KEY

# OpenAI Platform で使用量と課金設定を確認
```

#### 3. 「アプリがスリープ状態」
- Heroku無料プランは30分間アクセスがないとスリープ
- 初回アクセス時に数秒の起動時間が必要（正常です）

#### 4. 「音声認識が動かない」
- HTTPSでアクセスしているか確認
- ブラウザの設定でマイクアクセスを許可
- Chrome/Edgeなど対応ブラウザを使用

---

## 💰 料金について

### Heroku
- **無料プラン**: 月550時間まで無料（1日約18時間）
- **有料プラン**: $7/月〜（24時間稼働）

### OpenAI API
- **gpt-4o-mini**: 非常に安価
- **目安**: 1回の面接練習で1-2円程度
- **月100人利用**: 約1,000-2,000円

### GitHub Pages
- **完全無料**: 容量制限あり（通常問題なし）

---

## 🔒 セキュリティ注意事項

- [ ] `.env`ファイルをGitにコミットしない
- [ ] OpenAI APIキーを公開しない
- [ ] 定期的にAPI使用量をチェック
- [ ] 本番環境でDEBUG=Falseに設定

---

**🎉 デプロイ完了！生徒の皆さんの面接練習に活用してください！**