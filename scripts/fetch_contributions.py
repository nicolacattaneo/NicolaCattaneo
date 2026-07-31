import json
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USERNAME = "nicolacattaneo"
OUT = Path("data/contributions.json")


def parse_level(class_value: str) -> int:
    for part in class_value.split():
        if part.startswith("ContributionCalendar-day--level-"):
            return int(part.rsplit("-", 1)[1])
    return 0


def main() -> None:
    url = f"https://github.com/users/{USERNAME}/contributions"
    response = requests.get(url, timeout=30, headers={"User-Agent": "profile-readme-svg"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    for rect in soup.select("td.ContributionCalendar-day, tool-tip"):
        if rect.name == "tool-tip":
            continue
        date = rect.get("data-date")
        if not date:
            continue
        count_raw = rect.get("data-count") or "0"
        classes = " ".join(rect.get("class", []))
        days.append(
            {
                "date": date,
                "count": int(count_raw),
                "level": parse_level(classes),
            }
        )

    if not days:
        raise RuntimeError(f"No contribution days found for {USERNAME}. Check the username.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(
            {
                "username": USERNAME,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "days": days[-371:],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
