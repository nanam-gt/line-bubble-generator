# LINE風トーク吹き出し画像ジェネレーター 開発ドキュメント

このZIPは、VS CodeのCodexで開発を進めるためのMarkdownドキュメント一式です。

## アプリ概要
文章を入力すると、その文章が入ったLINE風のトーク吹き出し画像を生成し、PNG/JPEG形式でダウンロードできるWebアプリケーションです。

## MVP方針
- 1画像につき1吹き出し
- 自分側（緑）/ 相手側（白）を選択
- 背景なし
- PNGは透明背景
- JPEGは白背景に変換
- 画像サイズは吹き出しに合わせた最小サイズ
- しっぽあり
- 日本語対応
- 自動改行対応

## 推奨開発環境
- macOS Sequoia 15.4.1
- MacBook Pro 16inch 2019
- Python 3.12
- VS Code
- Streamlit
- Pillow

## ドキュメント構成
| ファイル | 内容 |
|---|---|
| `01_SPECIFICATION.md` | 仕様書 |
| `02_CODEX_INSTRUCTIONS.md` | Codexへの実装指示 |
| `03_PROJECT_STRUCTURE.md` | 推奨ディレクトリ構成 |
| `04_IMPLEMENTATION_TASKS.md` | 実装タスク一覧 |
| `05_UI_SPEC.md` | 画面仕様 |
| `06_IMAGE_GENERATION_SPEC.md` | 画像生成仕様 |
| `07_ACCEPTANCE_CRITERIA.md` | 受け入れ条件 |
| `08_PROMPTS_FOR_CODEX.md` | Codexに投げるプロンプト例 |
| `09_SETUP_GUIDE.md` | セットアップ手順 |

まずは `08_PROMPTS_FOR_CODEX.md` の「初回実装プロンプト」をCodexに渡してください。

## ローカル起動方法

1. 依存パッケージをインストールします。

```bash
pip install -r requirements.txt
```

2. Streamlitアプリを起動します。

```bash
streamlit run app.py
```

3. ブラウザで表示されたURLを開きます。

通常は `http://localhost:8501` で起動します。

## フォントについて

日本語表示用に、`assets/fonts/NotoSansJP-Regular.ttf` または `assets/fonts/NotoSansJP-Regular.otf` を配置できます。
未配置の場合は、macOS標準の日本語フォントを自動で探して使用します。

Streamlit Community CloudではLinux環境で動作するため、`packages.txt` に `fonts-noto-cjk` を指定しています。
これにより、クラウド上でも日本語を表示できるNoto CJKフォントがインストールされます。

## Streamlit Community Cloudで公開する方法

1. GitHubで新しいリポジトリを作成します。

例:

```text
line-bubble-generator
```

2. このフォルダをGitHubへpushします。

```bash
git init
git add .
git commit -m "Initial Streamlit app"
git branch -M main
git remote add origin https://github.com/あなたのユーザー名/line-bubble-generator.git
git push -u origin main
```

3. Streamlit Community Cloudにアクセスします。

```text
https://share.streamlit.io
```

4. `Create app` から以下を指定してデプロイします。

```text
Repository: GitHubで作成したリポジトリ
Branch: main
Main file path: app.py
```

5. デプロイ完了後、発行された `https://...streamlit.app` のURLを共有します。

以後はGitHubにpushすると、Streamlit Community Cloud側にも自動で反映されます。
