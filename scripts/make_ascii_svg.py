from pathlib import Path

from PIL import Image


SOURCES = [Path("source-avatar.png"), Path("source-prepped.png")]
OUT = Path("profile-ascii.svg")
RAMP = " .`:-=+*cs#%@"
COLS = 64
ROWS = 45


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
    source = next((candidate for candidate in SOURCES if candidate.exists()), None)
    if source is None:
        if OUT.exists():
            print(f"No source image found; keeping existing {OUT}.")
            return
        raise FileNotFoundError(
            f"{SOURCES[-1]} is required to create {OUT}. Run scripts/prep_photo.py first."
        )

    image = Image.open(source).convert("L")
    if source.name.startswith("source-avatar"):
        width, height = image.size
        crop_w = round(min(width, height) * 0.68)
        crop_h = round(crop_w * 1.1)
        left = (width - crop_w) // 2
        top = round(height * 0.10)
        image = image.crop((left, top, left + crop_w, top + crop_h))

    char_w = 7
    line_h = 10

    # Monospace character cells aren't square, so a naive aspect-preserving
    # resize onto a COLS x ROWS character grid squashes the image. Compensate
    # by deriving the row count from the cell aspect ratio so the rendered
    # ASCII block matches the source image's proportions.
    cols = COLS
    rows = max(1, round(cols * char_w * image.height / image.width / line_h))
    image = image.resize((cols, rows), Image.Resampling.LANCZOS)

    pixels = list(image.getdata())
    lines = []
    for row in range(rows):
        chars = []
        for col in range(cols):
            value = pixels[row * cols + col]
            idx = round((255 - value) / 255 * (len(RAMP) - 1))
            chars.append(RAMP[idx])
        lines.append("".join(chars).rstrip())

    pad = 16
    width = pad * 2 + cols * char_w
    height = pad * 2 + rows * line_h
    rows = []
    for i, line in enumerate(lines):
        y = pad + 10 + i * line_h
        clip_id = f"clip-{i}"
        dur = 0.42
        delay = i * 0.045
        rows.append(
            f'<clipPath id="{clip_id}"><rect x="{pad}" y="{y - 10}" width="0" height="{line_h + 2}">'
            f'<animate attributeName="width" from="0" to="{COLS * char_w}" begin="{delay:.3f}s" dur="{dur}s" fill="freeze"/>'
            f'</rect></clipPath>'
            f'<text x="{pad}" y="{y}" clip-path="url(#{clip_id})">{escape(line)}</text>'
            f'<rect x="{pad}" y="{y - 9}" width="7" height="{line_h}" fill="#c9d1d9" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" begin="{delay:.3f}s" dur="{dur}s" fill="freeze"/>'
            f'<animate attributeName="x" from="{pad}" to="{pad + COLS * char_w}" begin="{delay:.3f}s" dur="{dur}s" fill="freeze"/>'
            f'</rect>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Animated ASCII portrait">
  <rect width="100%" height="100%" rx="10" fill="#0d1117"/>
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 9px; fill: #c9d1d9; white-space: pre; }}
  </style>
  {"".join(rows)}
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
