# 06. 画像生成仕様

## 1. 基本方針
Pillowを使って、透明背景上にLINE風の吹き出しを描画する。

## 2. 入力
```python
text: str
speaker: str  # "self" or "other"
output_format: str  # "PNG" or "JPEG"
```

## 3. 出力
Pillow Imageオブジェクト。
- PNG: RGBA、透明背景
- JPEG: RGB、白背景

## 4. 色指定
| 要素 | 色 |
|---|---|
| 自分側吹き出し | `#95EC69` |
| 相手側吹き出し | `#FFFFFF` |
| 相手側枠線 | `#E5E5E5` |
| テキスト | `#000000` |
| PNG背景 | 透明 |
| JPEG背景 | `#FFFFFF` |

## 5. 推奨値
```python
FONT_SIZE = 42
PADDING_X = 36
PADDING_Y = 24
RADIUS = 32
TAIL_WIDTH = 22
TAIL_HEIGHT = 24
OUTER_MARGIN = 8
MAX_CHARS_PER_LINE = 22
LINE_SPACING = 10
```

## 6. 自動改行
MVPでは文字数ベース。
- ユーザー入力の改行を尊重する
- 各行が `MAX_CHARS_PER_LINE` を超えたら分割する
- 日本語は1文字単位で分割してよい

疑似コード:
```python
def wrap_text(text, max_chars):
    result = []
    for paragraph in text.split("\n"):
        while len(paragraph) > max_chars:
            result.append(paragraph[:max_chars])
            paragraph = paragraph[max_chars:]
        result.append(paragraph)
    return result
```

## 7. 吹き出しサイズ計算
幅:
```text
最大行テキスト幅 + 左右padding
```

高さ:
```text
行数分のテキスト高さ + 行間 + 上下padding
```

画像全体の幅:
```text
bubble_width + tail_width + outer_margin * 2
```

画像全体の高さ:
```text
bubble_height + outer_margin * 2
```

## 8. しっぽ描画
MVPでは三角形で実装する。

### 自分側
- 吹き出し右側に右向き三角形
- 吹き出し本体と同じ緑色

### 相手側
- 吹き出し左側に左向き三角形
- 吹き出し本体と同じ白色
- 必要に応じて枠線を描画

## 9. アンチエイリアス
MVPでは通常描画でよい。将来的に高品質化する場合は2倍または4倍サイズで描画し、最後に縮小する。

## 10. JPEG変換
透明PNGを白背景に合成してRGB変換する。

```python
background = Image.new("RGB", image.size, "white")
background.paste(image, mask=image.getchannel("A"))
```

## 11. 注意点
- Pillow標準フォントでは日本語が表示できないことがある
- 必ず日本語フォントを指定する
- 白吹き出しは透明背景上で見えづらいため、薄い枠線を推奨する
