# セットアップ手順（スナックシーサー SNS自動投稿）

コードの土台はできています。以下は**ユーザー自身のアカウントで行う必要がある作業**です
（本人確認・電話番号認証が絡むため、代行はできません）。

## 1. GitHubリポジトリの準備
1. GitHubでリポジトリを作成（**Public推奨** — Instagram Graph APIが画像を公開URLから取得するため）
2. このフォルダの中身をpush
3. リポジトリの Settings → Secrets and variables → Actions で以下を登録
   - `ANTHROPIC_API_KEY`
   - `IG_USER_ID`
   - `IG_ACCESS_TOKEN`
   - `THREADS_USER_ID`
   - `THREADS_ACCESS_TOKEN`
   - `X_API_KEY`
   - `X_API_SECRET`
   - `X_ACCESS_TOKEN`
   - `X_ACCESS_TOKEN_SECRET`

   ※Public repoにすると、`content/photos/` 内の画像は投稿前でも誰でもURLを知れば閲覧できます。
   気になる場合はプライベート運用に切り替える相談をしてください（構成変更が必要です）。

## 2. Instagram側の準備
1. 新規Instagramアカウントを作成し、「プロアカウント（ビジネス）」に切り替え
2. Facebookページを新規作成し、そのInstagramアカウントと連携
3. https://developers.facebook.com で開発者アカウント登録 → 新規アプリ作成（種類: ビジネス）
4. アプリに「Instagram」プロダクトを追加し、上記IGアカウントを「Instagramテスター」として登録
   （個人の運用のみであれば、Meta審査なしのDevelopment modeのままで投稿可能）
5. Graph API Explorerなどで長期アクセストークン（60日間有効、要定期更新）と `IG_USER_ID` を取得

## 3. Threads側の準備
1. 上記と同じMetaアプリに「Threads API」のユースケースを追加
2. Threadsアカウント設定（アプリの「Threads API」設定画面）で、投稿用のThreadsプロフェッショナルアカウントを紐付け
3. Threads OAuth（`https://threads.net/oauth/authorize` → `https://graph.threads.net/oauth/access_token`）を通じて短期アクセストークンを取得し、
   `https://graph.threads.net/access_token`（`grant_type=th_exchange_token`）で長期アクセストークン（60日間有効、要定期更新）に交換
4. `https://graph.threads.net/v1.0/me?fields=id&access_token=...` で `THREADS_USER_ID` を取得

## 4. X（Twitter）側の準備
1. 新規Xアカウントを作成
2. https://developer.x.com でDeveloperアカウント登録 → プロジェクト・アプリ作成
3. アプリの権限を「Read and Write」に設定
4. API Key/Secret、Access Token/Secretを発行（**権限変更後に再発行**しないと書き込みできない点に注意）

## 5. 動作確認
1. `content/photos/` に写真を追加し、`content/photo_manifest.json` に説明を追記
2. `config/store_profile.json` の店舗情報を正確な内容に修正
3. GitHub Actionsの「SNS自動投稿」ワークフローを手動実行（workflow_dispatch）して動作確認
4. 問題なければ毎日18:00 JSTに自動実行される

## 未確定・要相談事項
- `config/store_profile.json` の住所・料金はInstagramから自動取得した未検証情報。正確な情報に置き換えが必要
- Instagram/Threadsのアクセストークンは60日で失効するため、更新の自動化 or リマインドの仕組みを別途検討
- 投稿頻度・時間帯は `cron` 設定で調整可能
