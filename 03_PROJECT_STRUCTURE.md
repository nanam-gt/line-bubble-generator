# 03. 推奨プロジェクト構成

```text
line-bubble-generator/
├─ app.py
├─ image_generator.py
├─ requirements.txt
├─ README.md
├─ .gitignore
├─ assets/
│  └─ fonts/
│     └─ .gitkeep
├─ output/
│  └─ .gitkeep
└─ docs/
   ├─ 01_SPECIFICATION.md
   ├─ 02_CODEX_INSTRUCTIONS.md
   ├─ 03_PROJECT_STRUCTURE.md
   ├─ 04_IMPLEMENTATION_TASKS.md
   ├─ 05_UI_SPEC.md
   ├─ 06_IMAGE_GENERATION_SPEC.md
   └─ 07_ACCEPTANCE_CRITERIA.md
```

## 各ファイルの役割
### `app.py`
Streamlitアプリ本体。UI表示、入力受け取り、画像生成関数の呼び出し、プレビュー表示、ダウンロードボタンを担当する。

### `image_generator.py`
Pillowによる画像生成処理。自動改行、フォント読み込み、吹き出しサイズ計算、吹き出し描画、テキスト描画、PNG/JPEG変換を担当する。

### `requirements.txt`
```text
streamlit
pillow
```

### `assets/fonts/`
フォント置き場。例: `assets/fonts/NotoSansJP-Regular.ttf`

### `output/`
ローカル保存用の出力先。初期版では必須ではないが、デバッグ用途で用意する。
