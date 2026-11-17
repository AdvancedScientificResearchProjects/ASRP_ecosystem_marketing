**English | [Русский](CHANGELOG.ru.md)**

[← ASRP Ecosystem](README.md) · [Documentation index](docs/README.md)

# Changelog

## 2026-11-17 — showcase restructuring (branch `marketing-update-2026-11`)

- The single bilingual root README (201 510 bytes) became a showcase in two language versions,
  `README.md` and `README.ru.md`.
- All detail moved, without loss, to 13 page pairs under `docs/` (`NAME.md` + `NAME.ru.md`) with an index.
- The previous README is kept byte-for-byte in `archive/`; the starting point is tagged
  `pre-marketing-update-2026-11`.
- New generated visuals: hero banner, ecosystem flow, maturity map (English and Russian), 17 navigation icons.
- New tools: content inventory, no-loss verification, legacy-anchor map, visual generator; a test in `tests/`.
- The front page shows every area itself (ecosystem map, component tables, patents, accreditations and
  timeline, legal entities, funnels, track record, funding, media, roadmap, team); these parts are pulled
  from the `docs/` pages by a script, so there is no second copy of the text.
- Diagrams are being redrawn as separate English and Russian SVG files in one style
  (`tools/build_diagrams.py`); the original PNG files stay in `assets/diagrams/`.
- Links to the earlier section anchors keep working through invisible anchors at the matching sections.
- Not changed: `whitepaper/`, `graph/`, `assets/diagrams/`.
- Details, evidence and open questions: [reports/MARKETING_UPDATE_REPORT.md](reports/MARKETING_UPDATE_REPORT.md) (in Russian).

## 2026-04-28 — `cfd1940`

- Repository standardised: interactive graph, money flow, monetisation map.

## Earlier

- `dc62b50` Revise README for ASRP Ecosystem Overview.
- `b2869fe` Initial commit.
