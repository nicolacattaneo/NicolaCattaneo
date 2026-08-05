from pathlib import Path


OUT = Path("info-card.svg")
USERNAME = "nicolacattaneo"
WIDTH = 520
TOP = 74
ROW_GAP = 28
BOTTOM_PAD = 26
BORDER_PAD = 12

LINES = [
    ("name", "Nicola"),
    ("current", "CS + Mathematics @ Virginia Tech"),
    ("previous", "Engineering Intern @ UFINET"),
    ("stack", "Python · Java · Pandas · APIs · SQL"),
    ("building", "Automation tools and backend systems"),
    ("interests", "Software Engineering · Quant · Startups"),
    ("location", "Blacksburg, VA"),
    ("github", f"github.com/{USERNAME}"),
    ("linkedIn", "linkedin.com/in/nicolacattaneo06"),
    ("email", "nicolacatdal@gmail.com")
]


def main() -> None:
    rows = []
    y = TOP
    for i, (key, value) in enumerate(LINES):
        rows.append(
            f'<g>'
            f'<text x="34" y="{y}" fill="#7ee787" font-weight="700">{key}</text>'
            f'<text x="126" y="{y}" fill="#c9d1d9">{value}</text>'
            f'</g>'
        )
        y += ROW_GAP

    height = y + BOTTOM_PAD
    inner_width = WIDTH - BORDER_PAD * 2
    inner_height = height - BORDER_PAD * 2

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="Profile information card">
  <rect width="100%" height="100%" rx="10" fill="#0d1117"/>
  <rect x="{BORDER_PAD}" y="{BORDER_PAD}" width="{inner_width}" height="{inner_height}" rx="8" fill="none" stroke="#30363d"/>
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 15px; }}
  </style>
  <text x="34" y="42" fill="#58a6ff" font-size="18" font-weight="700">{USERNAME}@github</text>
  <text x="34" y="48" fill="#30363d">____________________________</text>
  {"".join(rows)}
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
