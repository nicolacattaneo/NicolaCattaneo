from pathlib import Path


OUT = Path("info-card.svg")
USERNAME = "nicolacattaneo"

LINES = [
    ("name", "Nicola"),
    ("current", "CS + Mathematics @ Virginia Tech"),
    ("previous", "Software Engineering Intern @ UFINET"),
    ("stack", "Python · Java · Pandas · APIs · SQL"),
    ("building", "Automation tools and backend systems"),
    ("interests", "Software Engineering · Quant · Startups"),
    ("location", "Guatemala / Blacksburg, VA"),
    ("github", f"github.com/{USERNAME}"),
]


def main() -> None:
    rows = []
    y = 74
    for i, (key, value) in enumerate(LINES):
        delay = 0.25 + i * 0.16
        rows.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.25s" fill="freeze"/>'
            f'<text x="34" y="{y}" fill="#7ee787" font-weight="700">{key}</text>'
            f'<text x="126" y="{y}" fill="#c9d1d9">{value}</text>'
            f'</g>'
        )
        y += 28

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="520" height="330" viewBox="0 0 520 330" role="img" aria-label="Profile information card">
  <rect width="100%" height="100%" rx="10" fill="#0d1117"/>
  <rect x="12" y="12" width="496" height="306" rx="8" fill="none" stroke="#30363d"/>
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
