# 02. Codex実装指示

## 目的
VS CodeのCodexを使って、Python + Streamlit + PillowでLINE風吹き出し画像ジェネレーターを実装する。

## 実装方針
初期版では「最小限で動くMVP」を優先する。

やること:
- StreamlitでWeb UIを作る
- Pillowで吹き出し画像を生成する
- PNG/JPEGでダウンロードできるようにする

やらないこと:
- ログイン
- データ保存
- 複数吹き出し
- 背景画像
- 本物LINEの完全再現
- 外部API連携
- データベース

## 技術指定
- Python 3.12
- Streamlit
- Pillow

## 必須ファイル
```text
app.py
image_generator.py
requirements.txt
README.md
```

## 実装上の注意
### 日本語フォント
Pillowで日本語を描画するため、Noto Sans JPを使う。`assets/fonts/` にフォントファイルを配置する想定。ただし、フォントがない場合はシステムフォントを探すフォールバック処理を入れる。

### 透明PNG
PNGはRGBA画像として生成する。

```python
Image.new("RGBA", (width, height), (255, 255, 255, 0))
```

### JPEG
JPEGは透明背景に対応しないため、白背景に合成してRGBへ変換する。

### 自動改行
MVPでは文字数ベースでよい。
- 20〜25文字程度で改行
- ユーザー入力の改行も維持する

### 白吹き出し
相手側の白吹き出しは透明背景だと境界が見えづらいため、薄い枠線を描画する。

### 画像サイズ
固定サイズではなく、吹き出しサイズに合わせた最小画像サイズにする。外側余白は5〜10px程度のみ。

## コーディング方針
- 関数を分ける
- 画像生成処理は `image_generator.py` に切り出す
- Streamlitの画面処理は `app.py` に置く
- マジックナンバーはなるべく定数化する
- 例外処理を入れる
- 空文字入力時は画像生成しない

## 推奨関数
```python
def generate_bubble_image(text: str, speaker: str, output_format: str = "PNG") -> Image.Image:
    ...
```

補助関数例:
```python
def wrap_text(text: str, max_chars_per_line: int) -> list[str]: ...
def load_font(size: int) -> ImageFont.FreeTypeFont: ...
def calculate_bubble_size(lines: list[str], font: ImageFont.FreeTypeFont) -> tuple[int, int]: ...
def draw_bubble(draw: ImageDraw.ImageDraw, ...): ...
```

## Streamlit UI要件
- タイトル表示
- テキストエリア
- 吹き出し種類ラジオボタン
- プレビュー表示
- PNGダウンロードボタン
- JPEGダウンロードボタン

## 完了条件
`streamlit run app.py` でブラウザから利用できること。
