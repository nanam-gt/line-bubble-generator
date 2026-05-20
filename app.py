import streamlit as st

from image_generator import generate_bubble_image, to_jpeg_bytes, to_png_bytes


SPEAKER_OPTIONS = {
    "自分（緑）": "self",
    "相手（白）": "other",
}


st.set_page_config(
    page_title="LINE風トーク吹き出し画像ジェネレーター",
    page_icon="💬",
    layout="centered",
)

st.title("LINE風トーク吹き出し画像ジェネレーター")
st.write("文章を入力すると、LINE風の吹き出し画像を生成できます。PNGは透明背景、JPEGは白背景で保存されます。")

message = st.text_area(
    "テキスト入力",
    height=150,
    max_chars=1000,
    placeholder="ここにメッセージを入力してください",
)

speaker_label = st.radio(
    "吹き出しタイプ",
    options=list(SPEAKER_OPTIONS.keys()),
    horizontal=True,
)

text = message.strip()

if not text:
    st.warning("メッセージを入力してください。")
elif len(message) > 1000:
    st.warning("1000文字以内で入力してください。")
else:
    image = generate_bubble_image(message, speaker=SPEAKER_OPTIONS[speaker_label])
    png_bytes = to_png_bytes(image)
    jpeg_bytes = to_jpeg_bytes(image)

    st.subheader("プレビュー")
    st.image(png_bytes)

    left, right = st.columns(2)
    with left:
        st.download_button(
            "PNGダウンロード",
            data=png_bytes,
            file_name="line_bubble.png",
            mime="image/png",
            use_container_width=True,
        )
    with right:
        st.download_button(
            "JPEGダウンロード",
            data=jpeg_bytes,
            file_name="line_bubble.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )
