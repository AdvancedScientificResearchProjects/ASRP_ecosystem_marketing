**English | [Русский](README.ru.md)**

[← ASRP Ecosystem](../README.md) · [Documentation index](../docs/README.md)

<div align="center">

# ASRP Ecosystem — Interactive Graph

</div>

> Statuses and figures on this page are as of 2026-Q2 unless a date is given, and are stated by the project; they have not been independently re-verified.

---

> 🌐 **Live URL:** **<https://asrp-graph.surge.sh/preview.html>** — open on any device, no signup.
>
> 147 entities · 256 connections · bilingual EN ⇄ RU · 16 entity types · fcose label-aware layout · per-type emoji icons · type filter / search / PNG export.

> 💛 **Like the graph? Support the work behind it:** **<https://asrp.tech/en/patrons>** · **<https://asrp.tech/ru/patrons>**

## What's inside

```
asrp_kumu.json     — the graph data (Kumu blueprint format)
preview.html       — self-hosted interactive viewer (no signup needed)
build_blueprint.py — Python source that generates asrp_kumu.json
libs/              — vendored cytoscape.js + fcose + cose-bilkent (~700 KB)
README.md          — this file
```

## Option 1 — Open the live deploy

**<https://asrp-graph.surge.sh/preview.html>**

Hosted on Surge.sh free tier (24/7, unlimited bandwidth, HTTPS, CDN edge in 10 cities). No account required to view.

## Option 2 — Run locally

```bash
cd graph/
python3 -m http.server 8765
# then open http://localhost:8765/preview.html in a browser
```

**What you can do in the preview:**
- Click any node → see all fields + connections (in/out arrows + relationship type)
- Type-filter chips (top-right) → toggle whole categories on/off
- Search box → highlights matching nodes + their immediate neighbours
- Three layouts: `cose` (force-directed), `concentric` (hubs in centre), `tree`
- **PNG export** button → saves a 2× resolution screenshot of the current view
- Drag, zoom, pan the canvas
- All 16 entity types colour-coded (see legend in the panel)

## Option 3 — Import into Kumu.io for a hosted, shareable map

Step-by-step:

1. Sign up for Kumu (free for public projects): https://kumu.io/signup
2. New Project → name it e.g. *ASRP Marketing Ecosystem* → choose **Public** (free) or Private (trial)
3. Click the green **+** at the bottom of the empty map → **Import** → **Advanced** → **Import JSON file** → upload `asrp_kumu.json`
4. Kumu auto-renders the graph. You can:
   - Use the legend / decorate panel to set per-type colours and shapes
   - Add custom fields, view filters, perspectives
   - Get a public shareable URL (any browser, no Kumu account needed by viewers)
   - Export to PNG/SVG/PDF directly from Kumu's download menu
5. Re-import workflow: edit `build_blueprint.py`, regenerate `asrp_kumu.json`, drag-drop the new file into the Kumu project (Kumu deduplicates by `id`)

## Graph structure

| Type | Count | What it is |
|---|---:|---|
| `project` | 26 | All ASRP products: live (4), active-dev (13), planned (3), research repos (6) |
| `channel` | 24 | Social channels — TikTok / YouTube / Telegram / LinkedIn / Facebook / X / IG / RG |
| `institution` | 21 | DARPA, Tesla, NIH/NCI, DoE/LANL, Stanford, Cortical Labs, NSWC IHD, VA, Boeing, JINR Dubna, etc. |
| `person · external` | 11 | Cardillo, Nolan, Dalton, Renwick, Natasha |
| `person · team` | 10 | Leadership team (Ovseannicova, Kapustin, Bilovodenko, Savelev, Sepehri, Grivtsova, Banchenko) |
| `patent` | 9 | 6 Kazpatent + 1 PCT + 1 US Copyright |
| `publication` | 8 | All 8 canonical ASRP works on ResearchGate (Inspira-X, BCI report, GMS/GFS, Grivtsova, Forecasting, Dream-sync, Banchenko-Market, Lucid-dream induction) |
| `outreach` | 8 | Cortical Labs, NSWC IHD (Cardillo), Stanford/Nolan, NCI SBIR, DoE first-read, investor log |
| `funding-source` | 7 | Patrons, investors, crowdfunding, gov-contracts, grants, affiliate, direct sales |
| `theory-anchor` | 5 | Temporal-desync hypothesis, 3D-Time framework, Channel-19/21 taxonomy, hyperbolic-dispersion paper |
| `cluster` | 5 | Target-company groups: cultured-meat, big-pharma / functional foods, bioreactor / algae producers, seeds & agri-inputs, sports nutrition |
| `event` | 4 | Theta Hackathon Berlin, AstanaHub Pitch Battle, ECP-2026-04-04 |
| `legal-entity` | 3 | US LLC (Florida) + KZ ТОО ПНИР + UK reinstatement |
| `tooling-class` | 3 | Classes of content-factory tooling: AI video production, multi-platform publishing, Pinterest hourly automation |
| `accreditation` | 2 | DARPA BAA portal access + Tesla Business Program |
| `legal-disclosure` | 1 | UBO clause |

Counts computed from `asrp_kumu.json` on 17 November 2026.

**Total: 147 entities, 256 connections, average degree 3.5.**

Top hubs (most-connected nodes): ASRP LLC (Florida) (23), ASRP ТОО ПНИР (Kazakhstan) (21), DAAT Crystal (17), Denis Y. Banchenko (14), UAP_Reverse_Engineering_Study (14), ASRP.media (13), GFS — Global Forecasting System (11), Arcanum12th.education (10).

## Updating the graph

Edit `build_blueprint.py` (Python — adds entities + connections via two helper functions `E()` and `C()`), then run:

```bash
python3 build_blueprint.py
```

Re-imports keep IDs stable, so Kumu / preview pick up only the deltas.

## What this is good for

- **Investor / partner walk-throughs**: open the preview, click on Cortical Labs → see plasma study → see Valeria as reproducer → see GMS/GFS whitepaper → see Banchenko-Market commercial layer → all in one screen.
- **OSINT-style exploration**: filter to just `outreach` + `person · external` + `institution` → see the engagement web (Cortical Labs / Stanford-Nolan / NSWC IHD / DoE / NCI).
- **Coverage check**: filter to `patent` and verify each patent links to its product project.
- **Data completeness**: filter to `publication` and check authorship lines — every paper has at least Denis as co-author, plus the right team members.

## Notes / open items

- **JINR Dubna + element 115** entity is included as institutional context for the UAP work, but the full UAP-repo graph (Lazar timeline, Chernobrov archive, Kazatomprom, etc.) deliberately lives in the separate `UAP_Reverse_Engineering_Study` repo per Denis's routing. This graph references the institution but does not duplicate the UAP-internal entity web.
- **Two LinkedIn companies + project groups**: the second company page and additional project groups (`ASRP.fashion` / `ASRP.drift` / `Arcanum12th`) are skeletons; populate when you confirm the live URLs.
- **Investor outreach log**: the placeholder node is in the graph; populate once Denis sends the source list of fund/individual contacts.
- **Mewery Brno**: included as a placeholder pending Denis's confirmation that the Czech cultured-meat partner can be named publicly.

---

## Support

If this graph helps you understand or evaluate ASRP — investor walk-throughs, OSINT work, partner pitches — please support the work behind it. The patron tiers fund the labs, the open-source tooling, and keep this graph maintained and bilingual.

→ **<https://asrp.tech/en/patrons>** · **<https://asrp.tech/ru/patrons>** · **<https://asrp.tech/ru/donate/asrp>** (Inspira-X pre-launch)
