# GitHub Profile README Setup

This repository powers the public GitHub profile README for `nicolacattaneo`.
GitHub renders `README.md` on the profile because the repository is public and
named `NicolaCattaneo`, matching the account name.

## What Gets Published

- `README.md` references the generated SVG assets.
- `contrib-heatmap.svg` is rebuilt from the public GitHub contributions page.
- `info-card.svg` is rebuilt from the values in `scripts/make_info_card.py`.
- `profile-ascii.svg` is committed output from a private local photo source.

## Automated Updates

`.github/workflows/update-profile-art.yml` runs every day and can also be run
manually from GitHub Actions. It refreshes:

- `data/contributions.json`
- `contrib-heatmap.svg`
- `info-card.svg`

The portrait is intentionally not rebuilt in CI because `source-prepped.png` is
ignored and should stay local.

## Local Commands

Install the public update dependencies:

```sh
python3 -m pip install -r scripts/requirements.txt
```

Refresh the public generated assets:

```sh
python3 scripts/fetch_contributions.py
python3 scripts/render_heatmap_svg.py
python3 scripts/make_info_card.py
```

To rebuild the portrait from a local image:

```sh
python3 -m pip install -r scripts/requirements-portrait.txt
python3 scripts/prep_photo.py source-photo.jpg
python3 scripts/make_ascii_svg.py
```

`source-photo.*` and `source-prepped.png` are ignored so the private source
image does not get committed.
