import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from requests import RequestException
from bs4 import BeautifulSoup


USERNAME = "nicolacattaneo"
OUT = Path("data/contributions.json")
GRAPHQL_URL = "https://api.github.com/graphql"
LEVELS = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}


def parse_level(class_value: str) -> int:
    for part in class_value.split():
        if part.startswith("ContributionCalendar-day--level-"):
            return int(part.rsplit("-", 1)[1])
    return 0


def parse_count(text: str) -> int:
    match = re.search(r"(\d+)\s+contribution", text)
    return int(match.group(1)) if match else 0


def fetch_with_graphql(token: str) -> list[dict] | None:
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
                contributionLevel
              }
            }
          }
        }
      }
    }
    """
    response = requests.post(
        GRAPHQL_URL,
        json={"query": query, "variables": {"login": USERNAME}},
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "profile-readme-svg",
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("errors"):
        return None

    calendar = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = []
    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            days.append(
                {
                    "date": day["date"],
                    "count": int(day["contributionCount"]),
                    "level": LEVELS.get(day["contributionLevel"], 0),
                }
            )
    return days


def fetch_from_public_html() -> list[dict]:
    url = f"https://github.com/users/{USERNAME}/contributions"
    response = requests.get(url, timeout=30, headers={"User-Agent": "profile-readme-svg"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tooltips = {
        tooltip.get("for"): tooltip.get_text(" ", strip=True)
        for tooltip in soup.select("tool-tip[for]")
    }
    days = []
    for rect in soup.select("td.ContributionCalendar-day[data-date]"):
        date = rect.get("data-date")
        tooltip = tooltips.get(rect.get("id"), "")
        classes = " ".join(rect.get("class", []))
        days.append(
            {
                "date": date,
                "count": parse_count(tooltip),
                "level": int(rect.get("data-level") or parse_level(classes)),
            }
        )
    return days


def main() -> None:
    token = (
        os.getenv("PROFILE_README_GITHUB_TOKEN")
        or os.getenv("GH_TOKEN")
        or os.getenv("GITHUB_TOKEN")
    )
    days = None
    if token:
        try:
            days = fetch_with_graphql(token)
        except (KeyError, RequestException):
            days = None
    if days is None:
        days = fetch_from_public_html()

    if not days:
        raise RuntimeError(f"No contribution days found for {USERNAME}. Check the username.")

    days.sort(key=lambda day: day["date"])
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
