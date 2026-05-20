# 09. セットアップガイド

## 1. プロジェクト作成
```bash
mkdir line-bubble-generator
cd line-bubble-generator
```

## 2. 仮想環境作成
```bash
python -m venv venv
source venv/bin/activate
```

## 3. ライブラリインストール
```bash
pip install -r requirements.txt
```

`requirements.txt` がまだない場合:
```bash
pip install streamlit pillow
pip freeze > requirements.txt
```

## 4. 起動
```bash
streamlit run app.py
```

## 5. フォント配置
Noto Sans JPを使用する場合:
```text
assets/fonts/NotoSansJP-Regular.ttf
```
に配置する。

## 6. Git管理
```bash
git init
git add .
git commit -m "Initial commit"
```

## 7. `.gitignore` 例
```text
venv/
__pycache__/
*.pyc
.DS_Store
output/*
!output/.gitkeep
.streamlit/
```
