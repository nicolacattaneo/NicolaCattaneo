import json
from datetime import date, timedelta
from pathlib import Path


DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def main() -> None:
    if DATA.exists():
        payload = json.loads(DATA.read_text(encoding="utf-8"))
    else:
        start = date.today() - timedelta(days=370)
        payload = {
            "username": "nicolacattaneo",
            "days": [
                {"date": (start + timedelta(days=i)).isoformat(), "count": 0, "level": 0}
                for i in range(371)
            ],
        }
    days = payload["days"][-371:]
    size = 11
    gap = 4
    left = 28
    top = 28
    width = left + 53 * (size + gap) + 20
    height = top + 7 * (size + gap) + 34

    rects = []
    for i, day in enumerate(days):
        week = i // 7
        weekday = i % 7
        x = left + week * (size + gap)
        y = top + weekday * (size + gap)
        delay = (week + weekday) * 0.018
        color = COLORS[max(0, min(4, int(day["level"])))]
        rects.append(
            f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="2.5" fill="{color}" '
            f'opacity="0" transform="translate(-8 8)">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.18s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="-8 8" to="0 0" '
            f'begin="{delay:.3f}s" dur="0.18s" fill="freeze"/>'
            f'<title>{day["date"]}: {day["count"]} contributions</title>'
            f'</rect>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{payload["username"]} contribution heatmap">
  <rect width="100%" height="100%" rx="10" fill="#0d1117"/>
  <text x="{left}" y="18" fill="#8b949e" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12">{payload["username"]} / contributions</text>
  {"".join(rects)}
  <text x="{left}" y="{height - 12}" fill="#8b949e" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10">less</text>
  <rect x="{left + 32}" y="{height - 21}" width="9" height="9" rx="2" fill="{COLORS[0]}"/>
  <rect x="{left + 46}" y="{height - 21}" width="9" height="9" rx="2" fill="{COLORS[1]}"/>
  <rect x="{left + 60}" y="{height - 21}" width="9" height="9" rx="2" fill="{COLORS[2]}"/>
  <rect x="{left + 74}" y="{height - 21}" width="9" height="9" rx="2" fill="{COLORS[3]}"/>
  <rect x="{left + 88}" y="{height - 21}" width="9" height="9" rx="2" fill="{COLORS[4]}"/>
  <text x="{left + 104}" y="{height - 12}" fill="#8b949e" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10">more</text>
</svg>
'''
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
