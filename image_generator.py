from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


FONT_SIZE = 42
PADDING_X = 36
PADDING_Y = 24
RADIUS = 32
TAIL_WIDTH = 22
TAIL_HEIGHT = 24
OUTER_MARGIN = 8
MAX_CHARS_PER_LINE = 16
LINE_SPACING = 10

SELF_BUBBLE_COLOR = "#95EC69"
OTHER_BUBBLE_COLOR = "#FFFFFF"
OTHER_BORDER_COLOR = "#E5E5E5"
TEXT_COLOR = "#000000"


FONT_CANDIDATES = (
    "assets/fonts/NotoSansJP-Regular.ttf",
    "assets/fonts/NotoSansJP-Regular.otf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansJP-Regular.ttf",
    "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
)


def load_font(size: int = FONT_SIZE) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for font_path in FONT_CANDIDATES:
        path = Path(font_path)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)

    return ImageFont.load_default()


def wrap_text(text: str, max_chars: int = MAX_CHARS_PER_LINE) -> list[str]:
    lines: list[str] = []

    for paragraph in text.splitlines() or [""]:
        if paragraph == "":
            lines.append("")
            continue

        while len(paragraph) > max_chars:
            lines.append(paragraph[:max_chars])
            paragraph = paragraph[max_chars:]
        lines.append(paragraph)

    return lines


def _line_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    if text == "":
        bbox = draw.textbbox((0, 0), "あ", font=font)
        return 0, bbox[3] - bbox[1]

    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def _measure_lines(lines: list[str], font: ImageFont.ImageFont) -> tuple[int, int, list[int]]:
    measurement_image = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(measurement_image)

    widths: list[int] = []
    heights: list[int] = []
    for line in lines:
        width, height = _line_size(draw, line, font)
        widths.append(width)
        heights.append(height)

    text_width = max(widths, default=0)
    text_height = sum(heights) + LINE_SPACING * max(len(lines) - 1, 0)
    return text_width, text_height, heights


def generate_bubble_image(text: str, speaker: str = "self") -> Image.Image:
    if speaker not in {"self", "other"}:
        raise ValueError("speaker must be 'self' or 'other'")

    font = load_font()
    lines = wrap_text(text)
    text_width, text_height, line_heights = _measure_lines(lines, font)

    bubble_width = max(text_width + PADDING_X * 2, RADIUS * 2)
    bubble_height = max(text_height + PADDING_Y * 2, RADIUS * 2)
    image_width = bubble_width + TAIL_WIDTH + OUTER_MARGIN * 2
    image_height = bubble_height + OUTER_MARGIN * 2

    image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    is_self = speaker == "self"
    bubble_color = SELF_BUBBLE_COLOR if is_self else OTHER_BUBBLE_COLOR
    outline = None if is_self else OTHER_BORDER_COLOR

    if is_self:
        bubble_box = (
            OUTER_MARGIN,
            OUTER_MARGIN,
            OUTER_MARGIN + bubble_width,
            OUTER_MARGIN + bubble_height,
        )
        tail_points = [
            (bubble_box[2] - 2, OUTER_MARGIN + RADIUS),
            (bubble_box[2] + TAIL_WIDTH, OUTER_MARGIN + RADIUS + TAIL_HEIGHT // 2),
            (bubble_box[2] - 2, OUTER_MARGIN + RADIUS + TAIL_HEIGHT),
        ]
    else:
        bubble_box = (
            OUTER_MARGIN + TAIL_WIDTH,
            OUTER_MARGIN,
            OUTER_MARGIN + TAIL_WIDTH + bubble_width,
            OUTER_MARGIN + bubble_height,
        )
        tail_points = [
            (bubble_box[0] + 2, OUTER_MARGIN + RADIUS),
            (OUTER_MARGIN, OUTER_MARGIN + RADIUS + TAIL_HEIGHT // 2),
            (bubble_box[0] + 2, OUTER_MARGIN + RADIUS + TAIL_HEIGHT),
        ]

    draw.rounded_rectangle(bubble_box, radius=RADIUS, fill=bubble_color, outline=outline, width=2)
    draw.polygon(tail_points, fill=bubble_color)

    if not is_self:
        draw.line([tail_points[0], tail_points[1], tail_points[2]], fill=OTHER_BORDER_COLOR, width=2)

    text_x = bubble_box[0] + PADDING_X
    text_y = bubble_box[1] + PADDING_Y
    for index, line in enumerate(lines):
        draw.text((text_x, text_y), line, fill=TEXT_COLOR, font=font)
        text_y += line_heights[index] + LINE_SPACING

    return image


def to_png_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def to_jpeg_bytes(image: Image.Image) -> bytes:
    background = Image.new("RGB", image.size, "white")
    background.paste(image, mask=image.getchannel("A"))

    buffer = BytesIO()
    background.save(buffer, format="JPEG", quality=95)
    return buffer.getvalue()
