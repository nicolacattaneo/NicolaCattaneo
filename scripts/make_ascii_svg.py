from pathlib import Path

from PIL import Image


SOURCE = Path("source-prepped.png")
OUT = Path("profile-ascii.svg")
RAMP = " .`:-=+*cs#%@"
COLS = 92
ROWS = 54
Y_SCALE = 0.76


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
    if not SOURCE.exists():
        if OUT.exists():
            print(f"{SOURCE} not found; keeping existing {OUT}.")
            return
        raise FileNotFoundError(
            f"{SOURCE} is required to create {OUT}. Run scripts/prep_photo.py first."
        )

    image = Image.open(SOURCE).convert("L")
    image.thumbnail((COLS, ROWS), Image.Resampling.LANCZOS)
    canvas = Image.new("L", (COLS, ROWS), 255)
    xoff = (COLS - image.width) // 2
    yoff = (ROWS - image.height) // 2
    canvas.paste(image, (xoff, yoff))

    pixels = list(canvas.getdata())
    lines = []
    for row in range(ROWS):
        chars = []
        for col in range(COLS):
            value = pixels[row * COLS + col]
            idx = round((255 - value) / 255 * (len(RAMP) - 1))
            chars.append(RAMP[idx])
        lines.append("".join(chars).rstrip())

    char_w = 8
    line_h = 11
    pad = 18
    width = pad * 2 + COLS * char_w
    height = round(pad * 2 + ROWS * line_h * Y_SCALE)
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
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 10px; fill: #c9d1d9; white-space: pre; }}
  </style>
  <g transform="translate(0 {pad}) scale(1 {Y_SCALE}) translate(0 {-pad})">
    {"".join(rows)}
  </g>
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
