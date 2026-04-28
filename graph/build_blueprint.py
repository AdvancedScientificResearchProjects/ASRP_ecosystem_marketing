#!/usr/bin/env python3
"""Build a Kumu.io JSON blueprint of the full ASRP marketing-ecosystem graph.

Covers: legal entities, leadership team, projects (live / active-dev / planned),
patents, publications (8 canonical RG works), social channels, outreach tracks,
target institutions, accreditations, funding streams, public events,
scientific-theory anchors.

Output: asrp_kumu.json — drag-and-drop into Kumu to create the map.
"""
import json
from pathlib import Path

elements = []
connections = []

# Emoji icon per element type — appears as a prefix in the visible label.
TYPE_ICONS = {
    "legal-entity":      "🏢",
    "legal-disclosure":  "⚖️",
    "person · team":     "👤",
    "person · external": "👥",
    "project":           "🚀",
    "patent":            "📜",
    "publication":       "📄",
    "channel":           "📡",
    "outreach":          "🤝",
    "institution":       "🏛️",
    "accreditation":     "🏅",
    "funding-source":    "💰",
    "event":             "📅",
    "theory-anchor":     "💡",
    "tooling-class":     "🛠️",
    "cluster":           "🎯",
}


def E(eid, label, etype, label_ru=None, description_ru=None, **kwargs):
    e = {"id": eid, "label": label, "type": etype, "icon": TYPE_ICONS.get(etype, "•")}
    if label_ru:
        e["labelRu"] = label_ru
    if description_ru:
        e["descriptionRu"] = description_ru
    e.update(kwargs)
    elements.append(e)


def C(efrom, eto, ctype="related-to", direction="directed", **kwargs):
    c = {"from": efrom, "to": eto, "type": ctype, "direction": direction}
    c.update(kwargs)
    connections.append(c)


# ────────────────────────────────────────────────────────────────────────────
# 1. Legal entities
# ────────────────────────────────────────────────────────────────────────────
E("le-us", "ASRP LLC (Florida)", "legal-entity",
  description="Advanced Scientific Research Projects LLC · Florida #L17000209665 · "
              "operational/commercial entity (Tesla Business Program, DARPA BAA, USD contracting)",
  jurisdiction="USA · Florida",
  registry="https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResultDetail?inquirytype=EntityName&searchTerm=ADVANCED%20SCIENTIFIC%20RESEARCH%20PROJECTS%20LLC",
  filed="2017-10-10",
  isHub=True)
E("le-kz", "ASRP ТОО ПНИР (Kazakhstan)", "legal-entity",
  description="📌 Why ТОО ПНИР matters. Kazakhstan ТОО (BIN 240140033296, Baikonur, "
              "27 Jan 2024) holds the patent portfolio — 8 patents, 6 Kazpatent + PCT 412362 "
              "+ biophotonic + ASRP.art. This makes IP licensing a distinct revenue route from "
              "operational USD contracting via ASRP LLC (Florida). Kazakhstan jurisdiction is "
              "driven by founder-residency requirements and KZ corporate-regulation specifics. "
              "Phased consolidation — holding companies, shareholder agreements, joint-activity "
              "agreements — is in progress. UBO triad: Ovseannicova · Kapustin · Banchenko.",
  jurisdiction="Kazakhstan · Baikonur",
  registry="https://kyc.kz/search/bin/240140033296",
  isHub=True)
E("le-uk", "ASRP UK entity (reinstatement)", "legal-entity",
  description="Currently undergoing corporate-status reinstatement",
  jurisdiction="United Kingdom",
  status="reinstating")

# UBO
E("ubo-group", "ASRP Group (UBO control)", "legal-disclosure",
  description="Beneficial-ownership and joint strategic control rest with V. Ovseannicova, "
              "M. Kapustin, D. Banchenko regardless of formal jurisdictional registration")

# ────────────────────────────────────────────────────────────────────────────
# 2. Leadership team (7)
# ────────────────────────────────────────────────────────────────────────────
team = [
    ("p-vo",  "Valeria A. Ovseannicova", "Co-Founder & CBE (Chief Biomedical Engineer)",
     "Kishenev, Moldova",   "plasma/agri/yeast protocol authorship + reproduction"),
    ("p-mk",  "Mykhailo M. Kapustin",     "Co-Founder & CTO",
     "Berlin, Germany",     "AI Dream Match Search Model · platform engineering"),
    ("p-vb",  "Vlada Bilovodenko",        "Co-Founder & CRO (Chief Risk Officer)",
     "Berlin, Germany",     "risk + compliance · whitepaper co-author"),
    ("p-is",  "Ivan V. Savelev",          "CSO (Chief Scientific Officer)",
     "Russian Federation",  "Senior Researcher · DNA Resonance Research Foundation"),
    ("p-as",  "Alireza Sepehri",          "CPO (Chief Physics Officer)",
     "Iran",                "physics co-author · whitepaper"),
    ("p-ig",  "Irina V. Grivtsova",       "Founder & CEO of Stress Relief Center «Strategy»",
     "Tomsk, Russia",       "Scientific European Society Hanover member · stress diagnostics"),
    ("p-db",  "Denis Y. Banchenko",       "Founder & CEO of ASRP",
     "Baikonur, Kazakhstan","Banchenko-Technology architect · UAP-adjacent oncology hypothesis"),
]
for pid, label, role, loc, desc in team:
    E(pid, label, "person · team", role=role, location=loc, description=desc)

# UBO links
for pid in ["p-vo", "p-mk", "p-db"]:
    C(pid, "ubo-group", "UBO of")

# Founders / executives
C("p-db", "le-us", "founder & CEO", direction="directed")
C("p-db", "le-kz", "formal sole executive (legal-technical only)", direction="directed")
C("p-vo", "le-us", "co-founder", direction="directed")
C("p-mk", "le-us", "co-founder", direction="directed")
C("p-vb", "le-us", "co-founder", direction="directed")
C("p-is", "le-us", "officer", direction="directed")

# ────────────────────────────────────────────────────────────────────────────
# 3. External persons (outreach + targets)
# ────────────────────────────────────────────────────────────────────────────
ext_persons = [
    ("p-cardillo", "Robert Cardillo",       "Configuration Management (CCMP·CISCM) at NSWC IHD",
     "USA",                  "Posted the 11-case scientist-cluster LinkedIn analysis · April 2026"),
    ("p-nolan",    "Dr. Garry Nolan",       "Stanford · Life Sciences, Bioinformatics, Cancer Research",
     "Stanford, USA",        "UAP-adjacent oncology · *The Phenomenon of Disclosure*"),
    ("p-dalton",   "Calendar admin (Stanford)", "Admin to Dr. Garry Nolan",
     "Stanford, USA",        "Manages Dr. Nolan's calendar; contact provided on request under NDA"),
    ("p-renwick",  "NIH/NCI Contracting Specialist", "NIH/NCI Contracting Specialist",
     "Bethesda MD, USA",     "Contact via official NIH SBIR portal · NCI SBIR FY26 track"),
    ("p-natasha",  "Natasha (Cortical Labs contact)", "Cortical Labs · review lead",
     "Melbourne, Australia", "Communicated 2026-Q2 about active review of ASRP plasma research"),
]
for pid, label, role, loc, desc in ext_persons:
    E(pid, label, "person · external", role=role, location=loc, description=desc)

# ────────────────────────────────────────────────────────────────────────────
# 4. Projects
# ────────────────────────────────────────────────────────────────────────────
projects_live = [
    ("pj-bot",     "Arcanum12th_BOT",         "🟢 live", "Dreams journal + biosensor data → GFS"),
    ("pj-media",   "ASRP.media",              "🟢 live", "Official media + science-popularising content"),
    ("pj-science", "ASRP.science",            "🟢 live", "Peer-review scientific journal"),
    ("pj-tech",    "asrp.tech",               "🟢 live", "Projects & patents portfolio site"),
]
projects_active = [
    ("pj-arc12",   "Arcanum12th.education",   "🟡 active-dev", "Educational platform · raw biological-data source (genetic, EEG, GSR, ANS)"),
    ("pj-art",     "ASRP.art",                "🟡 active-dev", "Neurophysiological art valuation (SPR)"),
    ("pj-drift",   "ASRP.drift (PlayOne)",    "🟡 active-dev", "Neurointegration for team synchronisation"),
    ("pj-gfs",     "GFS — Global Forecasting System", "🟡 active-dev", "Dream + biosensor analysis → forecasts (B2G/B2B)"),
    ("pj-gms",     "Global Mental System (GMS)", "🟡 active-dev", "Cognitive process synchronisation · meta-cluster"),
    ("pj-bfs",     "Body Food System",        "🟡 active-dev", "Genetics-based personalised nutrition"),
    ("pj-inspira", "Inspira-X",               "🟡 active-dev", "Dual-channel pneumograph + ECG · DAAT Crystal stack"),
    ("pj-dance",   "ASRP.dance",              "🟡 active-dev", "Movement neuroscience · cortical activation"),
    ("pj-fashion", "ASRP.fashion",            "🟡 active-dev", "Living biocompatible textiles (plant/bacteria/fungi)"),
    ("pj-daat",    "DAAT Crystal",            "🟡 active-dev", "Premium cognitive-enhancement device · crystal+Inspira-X+neurointerface"),
    ("pj-exch",    "ASRP.exchange / ASRP Market", "🟡 active-dev", "Consciousness-state marketplace"),
    ("pj-kapusta", "Kapusta.money",           "🟡 active-dev", "Rating-system substrate (NOT just a currency) · GFS-patent mechanism"),
]
projects_planned = [
    ("pj-shop",    "ASRPshop",                "🟠 planned", "B2C storefront for DAAT crystals + ASRP.fashion"),
    ("pj-stock",   "stock.asrp.* subdomain",  "🟠 planned", "Mental Objects database, neurointerface ingest"),
    ("pj-crowd",   "Inspira-X crowdfunding",  "🟠 planned", "Kickstarter-class campaign"),
]
research_repos = [
    ("pj-uap",      "UAP_Reverse_Engineering_Study", "🔬 research", "Public reverse-engineering analysis (DoE first-reader)"),
    ("pj-plasma",   "Hyperbolic_Field_BloodPlasma_Study", "🔬 research", "Reproduced by V. Ovseannicova · drove Cortical Labs engagement"),
    ("pj-yeast",    "Hyperbolic_Field_Yeast_Study",  "🔬 research", "Stat. group-2 superiority · April 2026 cohort"),
    ("pj-daat-rs",  "Hyperbolic_Field_DAAT_Crystal_Study", "🔬 research-recruiting", "EEG / HRV / GSR / autonomic measurement protocol"),
    ("pj-plants",   "Hyperbolic Field Plants Study", "🔬 OSF-pending", "Germination + growth kinetics · pre-registration planned 2026-04-22"),
    ("pj-caviar",   "Hyperbolic Field Fish Caviar Study", "🔬 OSF-pending", "Aquaculture embryonic kinetics · pre-registration planned 2026-04-22"),
]
for pid, label, status, desc in projects_live + projects_active + projects_planned + research_repos:
    E(pid, label, "project", status=status, description=desc)

# Per-project revenue route — answers "how does this project make money?"
# Format: WHO pays for WHAT via WHICH-CHANNEL · STATUS-EMOJI
PROJECT_REVENUE = {
    "pj-uap": (
        "DoD primes + DARPA + DoE + VA pay for reverse-engineering subcontracts via LinkedIn + open-repo timing · target ~$2M/yr entry R&D · 🎯 target",
        "Подрядчики DoD + DARPA + DoE + VA платят за субконтракты по реверс-инжинирингу через LinkedIn и публикации репозиториев · цель ~$2 млн/год входной R&D · 🎯 цель"),
    "pj-plasma": (
        "Biocomputing (Cortical Labs Q2 2026) + medcentres + pharma license hyperbolic-field plasma protocols via LinkedIn engagement playbook · 🔄 active talks",
        "Биокомпьютинг (Cortical Labs Q2 2026) + медцентры + фарма лицензируют протоколы плазмы через LinkedIn-плейбук аутрича · 🔄 активные переговоры"),
    "pj-agri": (
        "UA/MD post-conflict soil-restoration grants + agri-holdings pay for hyperbolic-field germination/yield protocols via grant proposals → pilots → royalty · 🔄 pipeline",
        "Гранты UA/MD на восстановление почв + агрохолдинги платят за протоколы гиперболического поля по всхожести/урожайности через гранты → пилоты → роялти · 🔄 pipeline"),
    "pj-gfs": (
        "Governments + private desks + B2C bettors pay for forecasts via B2G direct + B2B API + ASRP.exchange UI · 🟡 active-dev",
        "Государства + частные дески + B2C-ставочники платят за прогнозы через B2G-канал + B2B API + UI ASRP.exchange · 🟡 active-dev"),
    "pj-art": (
        "Artists → galleries → collectors → auction houses pay for SPR scoring; bottom-up to top-tier auction houses (Phase-4 targets); paid SPR certification 3-6mo · 🟡 active-dev",
        "Художники → галереи → коллекционеры → аукционные дома платят за SPR-оценку; bottom-up к аукционным домам высшего эшелона (Phase-4); платная SPR-сертификация 3-6 мес · 🟡 active-dev"),
    "pj-drift": (
        "Clinical research + sports science + defense augmentation programs pay for resonant neurointegration via institutional partnerships post-validation · 🟡 active-dev",
        "Клинические исследования + спортивная наука + оборонные программы усиления платят за резонансную нейроинтеграцию через институциональные партнёрства после валидации · 🟡 active-dev"),
    "pj-media": (
        "Advertisers + Amazon affiliates pay via CPM/CPC banners + deep-links; neurointerface sale already realised · ✅ realised",
        "Рекламодатели + Amazon-партнёрки платят через CPM/CPC-баннеры и deep-link; продажа нейроинтерфейса уже реализована · ✅ реализовано"),
    "pj-arc12": (
        "B2C learners pay $9–499 courses + $5–50/mo subs + $29–99 certs; 30–70% rev-share with authors · email + YouTube + bot upsell · 🟡 active-dev",
        "B2C-ученики платят $9–499 за курсы + $5–50/мес подписки + $29–99 сертификаты; 30–70% rev-share с авторами · email + YouTube + апсейл из бота · 🟡 active-dev"),
    "pj-dance": (
        "Neuro/rehab clinics + high-perf sports + wellness studios + cog-neuro labs pay for movement-cortex protocols via institutional pilots → whitelabel + Arcanum12th cert · 🟡 active-dev",
        "Неврологические/реабилитационные клиники + спорт высоких достижений + wellness-студии + лаборатории когнитивной нейронауки платят за моторно-кортикальные протоколы через институциональные пилоты → whitelabel + сертификация Arcanum12th · 🟡 active-dev"),
    "pj-fashion": (
        "Premium fashion + wellness retail + medical textiles (anti-thrombosis) + space/defense R&D pay for living biocompatible textiles via designer pilots → bio-fabric licensing · 🟡 active-dev",
        "Премиум-fashion + wellness-ритейл + медтекстиль (антитромбоз) + космический/оборонный R&D платят за живые биосовместимые ткани через дизайнерские пилоты → лицензирование биотканей · 🟡 active-dev"),
    "pj-daat": (
        "Premium B2C + B2B corporate-wellness pay for crystal+Inspira-X+neurointerface+ASRP.drift stack via asrp.tech / ASRPshop / Arcanum12th community · ✅ realised (founder-disclosed pilots)",
        "Премиум B2C + корпоративный wellness платят за стек кристалл+Inspira-X+нейроинтерфейс+ASRP.drift через asrp.tech / ASRPshop / сообщество Arcanum12th · ✅ реализовано (пилоты со слов основателя)"),
    "pj-gms": (
        "End-users + content platforms + GMS-program enterprises pay tx fees on Kapusta.money + exchange commissions + Arcanum12th cert fees + premium subs · 🟡 active-dev",
        "Конечные пользователи + контент-платформы + корпорации с GMS-программами платят комиссии транзакций Kapusta.money + комиссии биржи + комиссии за сертификацию Arcanum12th + премиум-подписки · 🟡 active-dev"),
    "pj-exch": (
        "Bettors + Mental-Object holders + governments pay forecast/stake fees + listing/cert + B2G subscriptions; settled in Kapusta.money · 🟡 active-dev",
        "Ставочники + держатели Ментальных Объектов + государства платят за прогнозы/ставки + листинг/сертификацию + B2G-подписки; расчёты в Kapusta.money · 🟡 active-dev"),
    "pj-shop": (
        "Premium B2C buyers pay direct for DAAT crystals + ASRP.fashion items via own storefront — domain reportedly acquired · 🟠 planned",
        "Премиум B2C-покупатели платят напрямую за DAAT-кристаллы + изделия ASRP.fashion через собственную витрину — домен предположительно приобретён · 🟠 planned"),
    "pj-crowd": (
        "Backers pre-pay for Inspira-X dual-channel pneumograph+ECG via Kickstarter-class campaign; donate link live at asrp.tech/ru/donate/asrp · 🟡 in preparation",
        "Бэкеры предоплачивают Inspira-X (двухканальный пневмограф + ЭКГ) через кампанию Kickstarter-уровня; донат-линк уже работает на asrp.tech/ru/donate/asrp · 🟡 в подготовке"),
    "pj-inspira": (
        "Backers + B2C wellness + B2B clinics pay for Inspira-X biofeedback device + DAAT-stack component via crowdfunding launch + direct sales · 🟡 active-dev",
        "Бэкеры + B2C wellness + B2B-клиники платят за прибор биообратной связи Inspira-X + компонент DAAT-стека через краудфандинг и прямые продажи · 🟡 active-dev"),
}
_proj_index = {el["id"]: el for el in elements if el.get("type") == "project"}
for _pid, (_en, _ru) in PROJECT_REVENUE.items():
    if _pid in _proj_index:
        _proj_index[_pid]["revenueSummary"] = _en
        _proj_index[_pid]["revenueSummaryRu"] = _ru

# Project relationships
C("pj-bot", "pj-gfs", "feeds biosensor data to")
C("pj-arc12", "pj-gfs", "feeds raw biological data to (genetic / EEG / GSR / ANS)")
C("pj-arc12", "pj-bot", "courses + bot are dual data sources")
C("pj-bot", "pj-gms", "feeds dreams + biosensor → analytical layer")
C("pj-arc12", "pj-gms", "feeds biological data → analytical layer")
C("pj-gfs", "pj-exch", "publishes forecasts on")
C("pj-gfs", "pj-kapusta", "rating substrate · accuracy ↑/↓ ↔ Kapusta credit")
C("pj-kapusta", "pj-bot", "motivates biological sensors", direction="directed")
C("pj-kapusta", "pj-arc12", "promotes accurate contributors", direction="directed")
C("pj-daat", "pj-inspira", "bundle component (respiratory biosensor)")
C("pj-daat", "pj-drift", "AI interpretation layer")
C("pj-daat", "pj-shop", "sold via")
C("pj-fashion", "pj-shop", "sold via")
C("pj-art", "pj-gms", "objectifies SPR-certified states as Mental Objects")
C("pj-exch", "pj-stock", "uses subdomain for Mental Objects DB")
C("pj-exch", "pj-kapusta", "settles transactions in")
C("pj-inspira", "pj-crowd", "campaign target product")
C("pj-arc12", "pj-tech", "presented on the projects portfolio")
# merged with the cross-promo edge added below in section 14b
C("pj-media", "pj-tech", "directs traffic to portfolio")

# ────────────────────────────────────────────────────────────────────────────
# 5. Patents (6 Kazpatent + 1 PCT + 1 US Copyright)
# ────────────────────────────────────────────────────────────────────────────
patents = [
    ("pat-fbhfs",   "KZ 2025/1095.1 — Fractal Biomedical Hyperbolic Field System (FBHFS)",
     "Kazpatent · scientific base for DAAT Crystal + ASRP.fashion + plasma study"),
    ("pat-inspira", "KZ 2025/0914.1 (No. 399693) — Inspira-X Respiratory Analysis",
     "Kazpatent · formal exam done · substantive pending"),
    ("pat-drift",   "KZ 413554 — ASRP.drift Neurointegration",
     "Kazpatent · ASRP.drift AI peer-reviewed publication"),
    ("pat-gfs",     "GFS — Global Forecasting System (Kazpatent)",
     "Kazpatent · documents Kapusta rating-substrate mechanism"),
    ("pat-gms",     "GMS — Global Mental System (Kazpatent)",
     "Kazpatent · meta-cluster architecture"),
    ("pat-banchenko-tech", "Banchenko-Technology Set (Kazpatent)",
     "Kazpatent · combined methods (dream-sync, mnemonic sync, GFS, market)"),
    ("pat-bfs-us",  "US Copyright TXu002116250 — Body Food System",
     "US Copyright Office · Body Food System personalised-nutrition methodology"),
]
# pat-pct removed — its content (PCT 412362) is now folded into pat-art
for pid, label, desc in patents:
    E(pid, label, "patent", description=desc)

# Patent → project linkage
C("pat-fbhfs",   "pj-daat",    "covers", direction="directed")
C("pat-fbhfs",   "pj-fashion", "covers", direction="directed")
C("pat-fbhfs",   "pj-plasma",  "scientific base", direction="directed")
C("pat-inspira", "pj-inspira", "covers", direction="directed")
C("pat-drift",   "pj-drift",   "covers", direction="directed")
C("pat-gfs",     "pj-gfs",     "covers", direction="directed")
C("pat-gms",     "pj-gms",     "covers", direction="directed")
C("pat-bfs-us",  "pj-bfs",     "covers", direction="directed")
C("pat-banchenko-tech", "pj-bot", "covers")

# Patents owned by KZ entity
for pid in ["pat-fbhfs", "pat-inspira", "pat-drift", "pat-gfs", "pat-gms", "pat-banchenko-tech"]:
    C("le-kz", pid, "owns", direction="directed")
C("le-us", "pat-bfs-us", "owns", direction="directed")

# ────────────────────────────────────────────────────────────────────────────
# 6. Publications (8 canonical RG works)
# ────────────────────────────────────────────────────────────────────────────
publications = [
    ("pub-1", "Inspira-X Clinical Validation — Methodology for Correcting Breathing Patterns via Biofeedback",
     "✅ Article", "https://www.researchgate.net/publication/404163473"),
    ("pub-2", "BCI Systems and Neural Interfaces — ASRP Research Group Technical Review",
     "🟡 Technical Report (journal article in preparation)", "https://www.researchgate.net/publication/396126506"),
    ("pub-3", "Technological Transformations — GMS / GFS architectural whitepaper",
     "✅ Article (Journal of Investment Banking and Finance, Jan 2025) · DOI 10.17605/OSF.IO/P9KHU",
     "https://www.researchgate.net/publication/388438082"),
    ("pub-4", "Grivtsova stress diagnostics & management",
     "✅ Article (American Journal of Medical and Clinical Research & Reviews, Jul-Aug 2024)",
     "https://www.researchgate.net/publication/394039715"),
    ("pub-5", "Forecasting Social, Geopolitical and Economic Events — Banchenko-Technology",
     "✅ Article · July 2024 · DOI 10.33425/2690-8077.1119 · 14 authors",
     "https://www.researchgate.net/publication/381995064"),
    ("pub-6", "Banchenko's Mnemonic Dream Synchronization Method (Blokhin Cell Concept)",
     "✅ Article (after preprint 377492383)", "https://www.researchgate.net/publication/378492219"),
    ("pub-7", "Banchenko-Market — Funding for Fundamental Science via Blockchain",
     "✅ Article (journal accepted nonstandard framing after KZ/UA/US/UK rejections)",
     "https://www.researchgate.net/publication/378492156"),
    ("pub-8", "Research on methods of inducing lucid dreaming (Banchenko Algorithm)",
     "✅ Article (2023)", "https://www.researchgate.net/publication/370913525"),
]
for pid, label, status, url in publications:
    E(pid, label, "publication", status=status, url=url,
      description=f"ResearchGate: {url} · status: {status}")

# Publication authorship (lead authors only — Denis on every; others where named in repo)
for pub_id in [p[0] for p in publications]:
    C("p-db", pub_id, "co-author")
for pub_id in ["pub-3", "pub-7"]:  # whitepapers
    for p in ["p-vo", "p-mk", "p-vb", "p-is", "p-ig"]:
        C(p, pub_id, "co-author")
C("p-as", "pub-3", "co-author")
C("p-ig", "pub-4", "first author")
C("p-mk", "pub-4", "co-author")
C("p-mk", "pub-6", "co-author (Kapustin Dream Match Search AI Model)")

# Publications cover projects
C("pub-1", "pj-inspira", "validates")
C("pub-2", "pj-drift",   "reviews")
C("pub-3", "pj-gms",     "describes")
C("pub-3", "pj-gfs",     "describes")
C("pub-4", "pj-arc12",   "method used in")
C("pub-5", "pj-gfs",     "founding methodology")
C("pub-6", "pj-bot",     "founding method (mnemonic dream sync)")
C("pub-7", "pj-exch",    "economic model")
C("pub-7", "pj-kapusta", "blockchain-funding architecture")
C("pub-8", "pj-bot",     "early lucid-dream methodology")

# ────────────────────────────────────────────────────────────────────────────
# 7. Distribution channels
# ────────────────────────────────────────────────────────────────────────────
channels = [
    # TikTok
    ("ch-tt-tech",    "TikTok @asrp.tech",     "tiktok",   "6014 followers · 51.4K likes",   "https://www.tiktok.com/@asrp.tech"),
    ("ch-tt-media",   "TikTok @asrp.media",    "tiktok",   "325 followers · 2499 likes",     "https://www.tiktok.com/@asrp.media"),
    ("ch-tt-science", "TikTok @asrp.science",  "tiktok",   "20 followers · 353 likes",       "https://www.tiktok.com/@asrp.science"),
    ("ch-tt-art",     "TikTok @asrp.art",      "tiktok",   "12 followers · 34 likes",        "https://www.tiktok.com/@asrp.art"),
    ("ch-tt-arc",     "TikTok @arcanum12th",   "tiktok",   "new",                            "https://www.tiktok.com/@arcanum12th"),
    ("ch-tt-vo",      "TikTok @ovseannikova",  "tiktok",   "personal (V. Ovseannicova)",     "https://www.tiktok.com/@ovseannikova"),
    # YouTube
    ("ch-yt-tech",    "YouTube @ASRPtech",     "youtube",  "447 subs · 22 videos · 27K views (since Jan 2018)", "https://www.youtube.com/@ASRPtech"),
    ("ch-yt-art",     "YouTube @ASRPart",      "youtube",  "active",                         "https://www.youtube.com/@ASRPart"),
    ("ch-yt-media",   "YouTube @ASRPmedia",    "youtube",  "18 subs",                        "https://www.youtube.com/@ASRPmedia"),
    ("ch-yt-fashion", "YouTube @ASRPfashion",  "youtube",  "active",                         "https://www.youtube.com/@ASRPfashion"),
    ("ch-yt-arc",     "YouTube @Arcanum12th",  "youtube",  "active",                         "https://www.youtube.com/@Arcanum12th"),
    # Telegram
    ("ch-tg-tech",    "Telegram @ASRPtech",    "telegram", "main announcements channel",     "https://t.me/ASRPtech"),
    ("ch-tg-elec",    "Telegram @electronics_MD", "telegram", "engineering updates",         "https://t.me/electronics_MD"),
    # LinkedIn — 2 companies + per-project groups
    ("ch-li-co",      "LinkedIn — ADVANCED SCIENTIFIC RESEARCH PROJECTS LLC", "linkedin", "company page · 50+ followers", ""),
    ("ch-li-co2",     "LinkedIn — ASRP (second company)",  "linkedin", "second company page", ""),
    ("ch-li-art",     "LinkedIn group — ASRP.art",     "linkedin", "per-project group", ""),
    ("ch-li-science", "LinkedIn group — ASRP.science", "linkedin", "per-project group", ""),
    # Other
    ("ch-fb",         "Facebook /asrp.tech/",  "facebook", "ASRP. AI technologies",          "https://www.facebook.com/asrp.tech/"),
    ("ch-x",          "X (Twitter) @ASRPtech", "x",        "news & announcements",           "https://x.com/ASRPtech"),
    ("ch-ig",         "Instagram @asrp.media", "instagram", "media content (login-gated)",   "https://www.instagram.com/asrp.media/"),
    ("ch-rg",         "ResearchGate Lab",      "researchgate", "academic profile",
     "https://www.researchgate.net/lab/Advanced-Scientific-Research-Projects-Denis-Banchenko"),
]
for cid, label, ctype, reach, url in channels:
    E(cid, label, "channel", subtype=ctype, reach=reach, url=url,
      description=f"{ctype} · {reach}")

# Channel → project mappings (publishes-via). Channels operated by
# revenue-bearing projects (ASRP.media affiliate, Arcanum12th courses,
# asrp.tech / ASRPshop) carry moneyEdge=True — they're the monetisation
# funnels that drive the realised affiliate + direct-sales revenue.
C("pj-tech",    "ch-tt-tech",    "publishes via", moneyEdge=True)
C("pj-tech",    "ch-yt-tech",    "publishes via", moneyEdge=True)
C("pj-tech",    "ch-tg-tech",    "publishes via", moneyEdge=True)
C("pj-media",   "ch-tt-media",   "publishes via", moneyEdge=True)
C("pj-media",   "ch-yt-media",   "publishes via", moneyEdge=True)
C("pj-media",   "ch-fb",         "publishes via", moneyEdge=True)
C("pj-media",   "ch-ig",         "publishes via", moneyEdge=True)
C("pj-science", "ch-tt-science", "publishes via")
C("pj-art",     "ch-tt-art",     "publishes via")
C("pj-art",     "ch-yt-art",     "publishes via")
C("pj-art",     "ch-li-art",     "publishes via")
C("pj-arc12",   "ch-tt-arc",     "publishes via", moneyEdge=True)
C("pj-arc12",   "ch-yt-arc",     "publishes via", moneyEdge=True)
C("pj-fashion", "ch-yt-fashion", "publishes via")
C("p-vo",       "ch-tt-vo",      "personal channel of")
C("le-us",      "ch-li-co",      "company page", direction="directed")
C("le-us",      "ch-li-co2",     "second company page", direction="directed")
C("ch-rg",      "p-db",          "lab page hosted by", direction="directed")

# ────────────────────────────────────────────────────────────────────────────
# 8. Outreach tracks
# ────────────────────────────────────────────────────────────────────────────
outreach = [
    ("or-cortical",  "Cortical Labs — active negotiations (2026-Q2)", "🟢 active",
     "Outreach playbook: capability built (Valeria reproduces) → repo published → "
     "LinkedIn content during DishBrain hype window → inbound → review (Q2 2026)"),
    ("or-nswc",      "NSWC IHD — Cardillo LinkedIn engagement", "🟢 active",
     "April 2026 · Cardillo posted 11-case scientist-cluster analysis · ASRP responded with "
     "UAP + plasma repos · feedback received"),
    ("or-stanford",  "Stanford / Nolan Lab — admin handoff (Feb 2026)", "🟢 active",
     "Feb 4 2026 LinkedIn DM · Nolan replied 'Sounds interesting' · directed to admin Dyan Dalton · "
     "detailed letter sent + plasma fibrin photo with T₊/T₀/T₋ legend"),
    ("or-nci",       "NCI SBIR FY26 — submission then systemic cancellation", "🟡 cancelled (not merit-based)",
     "Submitted 22 Aug 2025 (Notice 75N91025R00005) · NCI cancelled October 2025 due to "
     "SBIR/STTR statutory-authorization expiry · materials retained for re-submission"),
    ("or-doe",       "DoE / Los Alamos — first-reader event", "✅ tracked",
     "U.S. Department of Energy / Los Alamos National Laboratory segment was the first federal "
     "reader of the UAP_Reverse_Engineering_Study repo within hours of publication"),
    ("or-investors", "Investor outreach log — pending material", "🟠 pending",
     "Approximately ten interested investors / family offices in conversation; deck prevents close. "
     "Source list to be shared by founder."),
]
for oid, label, status, desc in outreach:
    E(oid, label, "outreach", status=status, description=desc)

# Outreach → people / institutions
C("or-cortical", "p-natasha",   "primary contact")
C("or-stanford", "p-nolan",     "target")
C("or-stanford", "p-dalton",    "operational contact (admin)")
C("or-nci",      "p-renwick",   "submission contact")
C("or-nswc",     "p-cardillo",  "engaged participant")

# Outreach → projects (subject of)
C("or-cortical", "pj-plasma",   "subject of engagement")
C("or-cortical", "pj-uap",      "secondary subject")
C("or-stanford", "pj-plasma",   "subject of letter (with T₊/T₀/T₋ photo)")
C("or-stanford", "pj-uap",      "scientific framing")
C("or-doe",      "pj-uap",      "first-read event on the repo")
C("or-nci",      "pj-daat",     "novel therapeutic technology submitted")

# ────────────────────────────────────────────────────────────────────────────
# 9. External institutions / target organisations
# ────────────────────────────────────────────────────────────────────────────
institutions = [
    ("inst-darpa",   "DARPA",                   "U.S. Defense Advanced Research Projects Agency"),
    ("inst-tesla",   "Tesla Inc.",              "Tesla Business Program · corporate enterprise accreditation"),
    ("inst-nih",     "NIH / NCI",               "National Institutes of Health · National Cancer Institute"),
    ("inst-doe",     "U.S. Department of Energy / LANL", "Los Alamos National Laboratory · UAP-adjacent reverse-engineering history"),
    ("inst-stanford","Stanford University",     "Garry Nolan Lab — UAP-adjacent oncology research"),
    ("inst-cortical","Cortical Labs",           "Melbourne biocomputing pioneer (DishBrain · neuron-silicon)"),
    ("inst-nswc",    "NSWC IHD / NAVSEA",       "Naval Surface Warfare Center Indian Head Division · DoD RDT&E"),
    ("inst-va",      "U.S. Department of Veterans Affairs", "Gulf War Syndrome veterans programmes"),
    ("inst-boeing",  "Boeing",                  "DoD prime · congressional disclosures on reverse-engineering spend"),
    ("inst-jinr",    "JINR Dubna",              "Joint Institute for Nuclear Research · international (~31 member countries) · element-115 synthesis · institutional context"),
    ("inst-osf",     "Open Science Framework (OSF)", "Pre-registration platform for ASRP studies"),
    ("inst-kazpatent","Kazpatent",              "Kazakhstan patent office"),
    ("inst-uspto",   "USPTO / U.S. Copyright Office", "U.S. patent and copyright registry"),
    ("inst-mewery",  "Czech cellular-meat partner (name withheld)",           "Czech cultured-meat partner (placeholder pending public confirmation)"),
]
for iid, label, desc in institutions:
    E(iid, label, "institution", description=desc)

# Project / outreach → institution
C("or-cortical", "inst-cortical", "engaged with", direction="directed")
C("or-stanford", "inst-stanford", "engaged with", direction="directed")
C("or-nci",      "inst-nih",      "submitted to", direction="directed")
C("or-doe",      "inst-doe",      "first-read by", direction="directed")
C("or-nswc",     "inst-nswc",     "tracked at", direction="directed")
C("le-kz",       "inst-kazpatent","files at", direction="directed")
C("le-us",       "inst-uspto",    "files at", direction="directed")
C("pj-uap",      "inst-jinr",     "institutional context (element-115 synthesis)")

# ────────────────────────────────────────────────────────────────────────────
# 10. Accreditations
# ────────────────────────────────────────────────────────────────────────────
E("acc-darpa",  "DARPA BAA proposal-portal access", "accreditation",
  status="active", granted="2025-09-16",
  description="Authenticated extranet account for BAA proposal submission · "
              "NOT a merit-based award — explicitly clarified")
E("acc-tesla",  "Tesla Business Program accreditation", "accreditation",
  status="active", granted="2025-08-22",
  description="Corporate-enterprise accreditation")

C("inst-darpa", "acc-darpa", "granted")
C("inst-tesla", "acc-tesla", "granted")
C("le-us", "acc-darpa", "holds")
C("le-us", "acc-tesla", "holds")

# ────────────────────────────────────────────────────────────────────────────
# 11. Funding sources
# ────────────────────────────────────────────────────────────────────────────
funding = [
    ("fund-patrons",  "Patrons (≈$165k cumulative)",     "✅ active",
     "Recurring philanthropic contributions across 7 tiers on asrp.tech/ru/patrons "
     "(Principal Philanthropist → Individual Contributor); cumulative confirmed ≈$165k; "
     "lead patron Alexander Ovsyannikov $100k; tradition-anchored on Medici / Carnegie / "
     "Rockefeller patronage references"),
    ("fund-investors","Investors (non-equity)",          "✅ open",
     "Non-equity co-operation models — joint-activity agreements, advance-against-deliverable, "
     "structured loans — published on asrp.tech/ru/investors; deliberately preserves UBO control "
     "across the multi-jurisdiction group"),
    ("fund-crowd",    "Crowdfunding (Inspira-X)",        "🟡 planned",
     "Kickstarter-class crowdfunding campaign in preparation for Inspira-X dual-channel "
     "pneumograph+ECG; pre-launch donate link already live at asrp.tech/ru/donate/asrp; "
     "pre-orders feed device manufacturing run"),
    ("fund-gov",      "Government contracts",            "🎯 target",
     "U.S. and partner-jurisdiction civilian and defense tenders — DoD primes (Boeing-class "
     "subcontracts), VA (Gulf War Syndrome programmes), DARPA-class R&D (BAA portal active), "
     "NCI SBIR FY26 ready for re-submission post-statutory restoration"),
    ("fund-grants",   "Research grants",                 "🔄 pipeline",
     "Research grants pipeline — UA/MD post-conflict soil-restoration grants for the agricultural "
     "study, royalty-model pilots with agri-holdings, foundation outbound (MJFF for "
     "neurodegenerative, cultured-meat foundations); structured as proposals → pilot → royalty"),
    ("fund-affiliate","Affiliate / commission",          "✅ realised",
     "Realised affiliate / commission income via the cross-promotion pattern — ASRP.media + "
     "ASRP.science + Arcanum12th + YouTube banner placements; canonical worked example: "
     "neurointerface affiliate sale through ASRP.media banner (reader clicked, purchased, "
     "ASRP received commission)"),
    ("fund-direct",   "Direct sales (DAAT crystals)",    "✅ realised",
     "Realised direct B2C/B2B sales — DAAT crystals (premium tier) sold via asrp.tech + "
     "(forthcoming) ASRPshop + Arcanum12th community; pilot signals: bank top-management "
     "cohort acquired the device, individual wearers include Forbes-list persons "
     "(founder-disclosed; institution and names not disclosed)"),
]
for fid, label, status, desc in funding:
    E(fid, label, "funding-source", status=status, description=desc)

C("fund-direct",    "pj-daat",  "revenue from", direction="directed", moneyEdge=True)
C("fund-affiliate", "pj-media", "revenue from", direction="directed", moneyEdge=True)
C("fund-crowd",     "pj-inspira", "campaign for", direction="directed", moneyEdge=True)
C("fund-grants",    "pj-plants",  "potential funder", direction="directed", moneyEdge=True)
C("fund-grants",    "pj-caviar",  "potential funder", direction="directed", moneyEdge=True)
C("fund-gov",       "pj-uap",     "B2G target via DARPA/DoD", direction="directed", moneyEdge=True)
C("fund-gov",       "pj-gfs",     "B2G target", direction="directed", moneyEdge=True)

# ────────────────────────────────────────────────────────────────────────────
# 12. Public events
# ────────────────────────────────────────────────────────────────────────────
events = [
    ("ev-theta",   "Theta Network Hackathon — Berlin", "2025-09-11",
     "GFS presented at European conference and hackathon"),
    ("ev-astana",  "AstanaHub / Digital Bridge 2025 — Industry 4.0 Pitch Battle", "2025",
     "GFS submitted; did not pass selection stage"),
    ("ev-ecp",     "ECP-2026-04-04 session", "2026-04-04",
     "Internal session producing the dataset later cited in plasma study"),
]
for eid, label, date, desc in events:
    E(eid, label, "event", date=date, description=desc)

C("ev-theta",  "pj-gfs",   "presented")
C("ev-astana", "pj-gfs",   "submitted to")
C("ev-ecp",    "pj-plasma", "produced data for")

# ────────────────────────────────────────────────────────────────────────────
# 13. Theory anchors (shapes the science framing)
# ────────────────────────────────────────────────────────────────────────────
theory = [
    ("th-temporal",  "Temporal-desynchronization hypothesis", "ASRP-internal",
     "Primary pathogenic factor in UAP-adjacent oncology = temporal desynchronization "
     "of biological processes (NOT classical mutagenic damage); therapy = correction "
     "of process kinetics, not cytotoxic intervention"),
    ("th-3dt",       "Three-Dimensional Time framework", "external",
     "World Scientific · DOI 10.1142/S2424942425500045 · mathematical formalism extending "
     "physical time from one to three dimensions; provides theoretical backbone for ASRP's "
     "T₊/T₀/T₋ kinetics notation"),
    ("th-channels",  "Channel-19 / Channel-21 taxonomy", "ASRP-internal",
     "Channel-19 = acceleration kinetics (T₊, Δt > 0) · Channel-21 = deceleration kinetics "
     "(T₋, Δt < 0) · used internally; T-notation used in external correspondence (e.g. Nolan)"),
    ("th-hyperbolic","Hyperbolic Dispersion Materials for Cancer Detection", "external",
     "External peer-reviewed paper supporting the hyperbolic-fields × oncology framing"),
]
for tid, label, scope, desc in theory:
    E(tid, label, "theory-anchor", scope=scope, description=desc)

C("th-temporal", "pj-plasma", "underpins")
C("th-temporal", "pj-daat",   "underpins (cancer therapeutic)")
C("th-3dt",      "th-temporal", "formal backbone for")
C("th-3dt",      "th-channels", "formal backbone for")
C("th-channels", "pj-plasma", "applied in")
C("th-hyperbolic","pj-plasma", "external support for")
C("th-hyperbolic","pj-uap",    "external support for")

# Stanford outreach uses the theory
C("or-stanford", "th-temporal", "communicated to Nolan as core hypothesis")
C("or-stanford", "th-channels", "communicated as plasma-fibrin T-notation")

# ────────────────────────────────────────────────────────────────────────────
# 14. New entities — patents, patrons, team, tooling, channels, outreach,
#     auction-house targets, theory anchors, agricultural project.
#     (Added per the 2026-04-26 graph audit.)
# ────────────────────────────────────────────────────────────────────────────

# Missing patents
E("pat-biophoton", "KZ 2025/1097.1 — Biophotonic Neurodiagnostic System", "patent",
  description="Kazpatent · Formal exam done → Substantive · public repo at "
              "github.com/denisbanchenko/Kazpatent_Biophotonic_Neurodiagnostic_System_Patent")
E("pat-art", "KZ 2025/0592.1 + PCT 412362 — Axionetic Sensing Reactions Platform in Art (ASRP.art)", "patent",
  description="Kazpatent + PCT international · Substantive exam stage · scientific base for SPR (Sensing Platform of Reactions)")

C("le-kz", "pat-biophoton", "owns", direction="directed")
C("le-kz", "pat-art",       "owns", direction="directed")
C("pat-biophoton", "pj-inspira", "covers (neurodiagnostic complement)", direction="directed")
C("pat-art", "pj-art", "covers", direction="directed")

# Lead patron + double-evidenced co-author/patrons
E("p-aovs", "Alexander Ovsyannikov", "person · external",
  role="Principal Philanthropist (lead patron, $100k)",
  description="Lead patron of ASRP — likely family relation to V. Ovseannicova",
  label_ru="Александр Овсянников")
E("p-burilova", "Tatyana Burilova", "person · external",
  role="Co-author on pub-5 + pub-6 · patron ($5k)",
  description="Whitepaper co-author (Banchenko-Technology + dream-sync) AND patron tier $5k",
  label_ru="Татьяна Бурилова")
E("p-shishkin", "Lev Shishkin", "person · external",
  role="Co-author on pub-6 · patron ($1k)",
  description="Dream-synchronisation paper co-author + patron",
  label_ru="Лев Шишкин")
E("p-mutsalkhanova", "Olena Mutsalkhanova-Yushchenko", "person · external",
  role="Co-author on pub-5 · patron ($1k)",
  description="Banchenko-Technology forecasting paper co-author + patron",
  label_ru="Олена Муцальханова-Ющенко")

C("p-aovs", "fund-patrons", "lead patron", direction="directed", amountUsd=100000, moneyEdge=True)
C("p-burilova", "fund-patrons", "patron",   direction="directed", amountUsd=5000, moneyEdge=True)
C("p-shishkin", "fund-patrons", "patron",   direction="directed", amountUsd=1000, moneyEdge=True)
C("p-mutsalkhanova", "fund-patrons", "patron", direction="directed", moneyEdge=True)
C("p-vb", "fund-patrons", "patron",         direction="directed", amountUsd=10000, moneyEdge=True)
C("p-ig", "fund-patrons", "patron",         direction="directed", amountUsd=200, moneyEdge=True)

# Operational team members (from README Leadership)
E("p-kz", "Kyryl Zmiienko", "person · team",
  role="SAIE (Senior AI Engineer)",
  description="Research analysis · plasma-data analyst · repositories · AI pipelines",
  label_ru="Кирилл Змиенко")
E("p-ak", "Andrii Kryliuk", "person · team",
  role="LFED (Lead Front-End Developer)",
  label_ru="Андрей Крылюк")
E("p-ag", "Aleksandr Gromyko", "person · team",
  role="LBED (Lead Back-End Developer)",
  label_ru="Александр Громыко")

C("p-kz", "le-us", "officer", direction="directed")
C("p-ak", "le-us", "officer", direction="directed")
C("p-ag", "le-us", "officer", direction="directed")
C("p-kz", "pj-plasma", "data analysis (sole analyst on raw set)")
C("p-kz", "pj-uap",    "data analysis & repository")

# Tooling-class entities (reference examples for media-strategy)
E("tool-vidrush", "Vidrush — AI production class", "tooling-class",
  description="Text-prompt → full documentary video; reference example for ASRP content factory's AI production layer")
E("tool-dohoo", "DOHOO — multi-platform publisher class", "tooling-class",
  description="Cross-platform auto-posting with Video-to-Text + ChatGPT per-platform adaptation")
E("tool-pinterest", "Pinterest hourly-automation — SEO discovery class", "tooling-class",
  description="Hourly cron · 3 boards parallel · ≈15-day ramp-up to first US traffic")

C("tool-vidrush",   "pj-media", "AI production layer for", direction="directed")
C("tool-dohoo",     "pj-media", "fan-out publisher for",   direction="directed")
C("tool-pinterest", "pj-media", "SEO discovery for",       direction="directed")

# Channels in scope but not yet launched (Pinterest / Medium / VK)
E("ch-pinterest", "Pinterest boards (planned)", "channel",
  subtype="pinterest", reach="planned per-project for asrp.art / asrp.fashion",
  description="Per-project Pinterest boards · SEO automation engine via Pinterest hourly cron")
E("ch-medium", "Medium (planned per-project)", "channel",
  subtype="medium", reach="planned",
  description="Per-project long-form text publications")
E("ch-vk", "VK (planned)", "channel",
  subtype="vk", reach="planned RU-speaking",
  description="VK Clips + VK Video + VK Notes — RU-speaking audience for all projects")

C("pj-art",     "ch-pinterest", "publishes via", direction="directed")
C("pj-fashion", "ch-pinterest", "publishes via", direction="directed")
C("tool-pinterest", "ch-pinterest", "operates", direction="directed")
C("pj-science", "ch-medium", "publishes via", direction="directed")
C("pj-tech",    "ch-medium", "publishes via", direction="directed")
C("pj-tech",    "ch-vk",     "publishes via", direction="directed")
C("pj-media",   "ch-vk",     "publishes via", direction="directed")

# Auction-house institutional targets (for ASRP.art Phase-4)
E("inst-auction-tier1", "Top-tier auction house A (Phase-4)", "institution",
  description="Top-tier international auction house · ASRP.art Phase-4 institutional partnership target · name withheld pre-contact",
  label_ru="Аукционный дом высшего эшелона A (Phase-4) — имя не раскрывается до контакта")
E("inst-auction-tier2",  "Top-tier auction house B (Phase-4)",  "institution",
  description="Top-tier international auction house · ASRP.art Phase-4 target · name withheld pre-contact",
  label_ru="Аукционный дом высшего эшелона B (Phase-4) — имя не раскрывается до контакта")
E("inst-saatchi",   "Saatchi (Gallery + Art)", "institution",
  description="Saatchi Gallery (London brick-and-mortar) and Saatchi Art (online platform) · ASRP.art Phase-4 target · NOT the Saatchi & Saatchi advertising agency",
  label_ru="Saatchi — Gallery (Лондон) + Saatchi Art (онлайн-платформа)")

C("pj-art", "inst-auction-tier1", "Phase-4 partnership target", direction="directed")
C("pj-art", "inst-auction-tier2", "Phase-4 partnership target", direction="directed")
C("pj-art", "inst-saatchi",   "Phase-4 partnership target", direction="directed")

# Cognitive-stack target partners (Phase-4)
E("inst-koniku", "Koniku", "institution",
  description="Biohybrid neural-silicon systems · Phase-4 ASRP.drift / DAAT cognitive-stack target")
E("inst-neurable", "Neurable", "institution",
  description="Consumer-grade neurointerface vendor · Phase-4 target")
E("inst-paradromics", "Paradromics", "institution",
  description="High-bandwidth BCI implant vendor · Phase-4 target")

C("pj-daat",  "inst-koniku",      "Phase-4 cognitive-stack partner target", direction="directed")
C("pj-drift", "inst-neurable",    "Phase-4 partner target",                 direction="directed")
C("pj-drift", "inst-paradromics", "Phase-4 partner target",                 direction="directed")

# Outreach: cultured-meat track (currently pending naming)
E("or-cmeat", "Cultured-meat outreach (private)", "outreach",
  status="🟡 internal",
  description="Track to FDA/EU-accredited and scaling cultured-meat producers; "
              "entry pitch: biological response modulation → shorter doubling time → lower media cost per kg")
C("or-cmeat", "inst-mewery", "primary contact (Czech pizza-meat partner)")
C("or-cmeat", "pj-bfs",      "supports BFS synergy")

# Outreach: MJFF
E("inst-mjff", "Michael J. Fox Foundation", "institution",
  description="Neurodegenerative-disease research foundation",
  label_ru="Фонд Майкла Дж. Фокса")
E("or-mjff", "MJFF — neurodegenerative outreach (private)", "outreach",
  status="🟡 tracked-private",
  description="Feb 28 / Mar 2 2026 correspondence dates · no public signal yet")
C("or-mjff", "inst-mjff",    "engaged with",  direction="directed")
C("or-mjff", "fund-grants",  "grant target",  direction="directed", moneyEdge=True)

# Public Telegram broadcast event (Forbes wearers)
E("ev-tg-forbes", "Telegram broadcast 2026-04-20 — Forbes-list wearers", "event",
  date="2026-04-20",
  description="Founder broadcast post (views:288 · forwards:2) — named DAAT Crystal individual wearers from Forbes list (names not disclosed)")
C("ev-tg-forbes", "pj-daat",     "publicised B2C wearers of", direction="directed")
C("ev-tg-forbes", "ch-tg-tech",  "broadcast via",             direction="directed")

# Theory anchor: QRL
E("th-qrl", "Quantum Resistant Ledger (QRL)", "theory-anchor",
  scope="external",
  description="Quantum-resistant blockchain for secure transmission and storage of Mental Objects · "
              "substrate for Kapusta.money settlement layer")
C("th-qrl", "pj-kapusta", "substrate for", direction="directed")
C("th-qrl", "pj-exch",    "settlement substrate for", direction="directed")

# Hyperbolic Field Agricultural — separate from the planned plants OSF study
E("pj-agri", "Hyperbolic_Field_Agricultural_Study", "project",
  status="🔬 active field trials (Day 4+)",
  description="Live agricultural field trials, Day-4+ measurements; double-blind activation")
C("pat-fbhfs",   "pj-agri", "scientific base", direction="directed")
C("th-channels", "pj-agri", "applied in",      direction="directed")
C("fund-grants", "pj-agri", "potential funder",direction="directed", moneyEdge=True)

# ────────────────────────────────────────────────────────────────────────────
# 14b. Missing connections audit (per 2026-04-26 graph audit)
# ────────────────────────────────────────────────────────────────────────────

# Inspira-X is also an ASRP.drift module
C("pj-inspira", "pj-drift", "module of")

# DAAT product ↔ DAAT research validation
C("pj-daat-rs", "pj-daat", "validates")

# UAP funnel direct institutional engagement targets
C("pj-uap", "inst-boeing", "DoD prime engagement target (~$40M reverse-engineering benchmark)")
C("pj-uap", "inst-va",     "Gulf War Syndrome track target")
C("pj-uap", "inst-doe",    "engagement target (institutional)")

# Stanford ↔ VA adjacency (Gulf War Syndrome)
C("inst-stanford", "inst-va", "Gulf War Syndrome programme adjacency")

# pub-1 (Inspira-X validation) → DAAT (where Inspira-X serves as biosensor)
C("pub-1", "pj-daat", "validates respiratory biosensor in DAAT stack")

# Missing co-authors (per whitepaper README author lists)
C("p-ig", "pub-5", "co-author")
C("p-mk", "pub-5", "co-author")
C("p-is", "pub-5", "co-author")
C("p-vb", "pub-5", "co-author")
C("p-is", "pub-4", "co-author")
C("p-burilova", "pub-5", "co-author")
C("p-burilova", "pub-6", "co-author")
C("p-shishkin", "pub-6", "co-author")
C("p-mutsalkhanova", "pub-5", "co-author")

# Funding → operating entity (US LLC = USD contracting)
C("fund-affiliate", "le-us", "revenue routes via", direction="directed", moneyEdge=True)
C("fund-direct",    "le-us", "USD contracting through", direction="directed", moneyEdge=True)
C("fund-gov",       "le-us", "B2G contracting through", direction="directed", moneyEdge=True)
C("fund-grants",    "le-us", "grant disbursements via", direction="directed", moneyEdge=True)
C("fund-crowd",     "le-us", "campaign proceeds to",   direction="directed", moneyEdge=True)

# Cross-promotion: media → DAAT and ASRPshop banners (revenue-bearing funnels)
C("pj-media", "pj-daat", "cross-promo affiliate banners → product",   moneyEdge=True)
C("pj-media", "pj-shop", "cross-promo affiliate banners → storefront", moneyEdge=True)

# UBO group → UK entity
C("ubo-group", "le-uk", "Group includes (UK reinstatement entity)", direction="directed")
C("p-db",      "le-uk", "executive (group level)",                  direction="directed")

# LinkedIn companies channel of all 3 outreach tracks
C("ch-li-co", "or-cortical", "channel of", direction="directed")
C("ch-li-co", "or-nswc",     "channel of", direction="directed")
C("ch-li-co", "or-stanford", "channel of", direction="directed")

# Tesla accreditation → DAAT B2B context
C("acc-tesla", "pj-daat", "B2B executive-wellness pitch context")

# Theory: 3D-Time backbone cited in pub-3 (the GMS/GFS architectural whitepaper)
C("th-3dt", "pub-3", "theoretical backbone cited in")

# ────────────────────────────────────────────────────────────────────────────
# 14c. Second-pass audit additions (2026-04-26 re-audit)
# ────────────────────────────────────────────────────────────────────────────

# UAP research lineage — Chernobrov (Kosmopoisk archive) + Lazar
E("p-chernobrov", "Vadim Chernobrov", "person · external",
  role="Kosmopoisk founder · field-data archive (post-landing measurements, quartz-resonator deviations)",
  description="Field-research lineage referenced inside the UAP study (chernobrov-archive)",
  label_ru="Вадим Чернобров")
E("p-lazar", "Bob Lazar", "person · external",
  role="UAP reverse-engineering historical anchor",
  description="Historical lineage anchor for UAP reverse-engineering claims (S-4, element-115)",
  label_ru="Боб Лазар")
C("p-chernobrov", "pj-uap", "archive cross-reference (chernobrov-archive)")
C("p-lazar",      "pj-uap", "research lineage anchor (S-4, element-115)")

# Cardillo → NSWC IHD employment edge
C("p-cardillo", "inst-nswc", "employed at", direction="directed")

# UBO covers all three entities (currently only le-uk linked)
C("ubo-group", "le-us", "Group includes (US operational entity)", direction="directed")
C("ubo-group", "le-kz", "Group includes (KZ patent-holding entity)", direction="directed")

# NCI submission — wire properly (currently only or-nci -> p-renwick exists)
C("or-nci", "fund-grants", "submitted to programme")
C("or-nci", "inst-nih",    "submission to authority", direction="directed")

# Investor outreach — Denis owns the pipeline
C("p-db", "or-investors", "owner of pipeline", direction="directed")

# ────────────────────────────────────────────────────────────────────────────
# 14d. Target-company clusters (option B — collapse named lists into 5 nodes)
# ────────────────────────────────────────────────────────────────────────────
E("cluster-cmeat", "Cultured-meat target cluster", "cluster",
  description="UPSIDE Foods · GOOD Meat · BlueNalu · Mosa Meat · Aleph Farms · Meatly · MIRAI Foods · Czech cellular-meat partner (name withheld) — pitch: biological-response modulation → shorter doubling time → lower media cost per kg",
  label_ru="Кластер целевых компаний по cultured meat")
E("cluster-pharma", "Big-pharma / functional-foods cluster", "cluster",
  description="Nestlé Health Science · Danone · Abbott · DSM-Firmenich · Chr. Hansen · BASF · Glanbia — Phase-3 functional-drinks + Phase-5 pharma adjunct targets",
  label_ru="Кластер big-pharma / функциональных продуктов")
E("cluster-bioreactor", "Bioreactor / algae-producers cluster", "cluster",
  description="AlgaTech · Cyanotech · Earthrise — bioreactor and algae-production partners for Phase-3 scale-up of FBHFS biological products",
  label_ru="Кластер биореакторов / производителей водорослей")
E("cluster-seeds", "Seeds & agri-inputs cluster", "cluster",
  description="Syngenta · Bayer · Corteva · Limagrain · AeroFarms · Monterey Bay Mushrooms · Promyc · MycoTech — Phase-3 large-scale agri pilots for FBHFS",
  label_ru="Кластер семян и агро-инпутов")
E("cluster-sports", "Sports-nutrition cluster", "cluster",
  description="Sports-nutrition brands as B2B targets for Inspira-X biofeedback + DAAT cognitive-stack adjunct positioning",
  label_ru="Кластер спортивного питания")

C("cluster-cmeat",      "pj-bfs",     "Phase-3/4 BFS target cluster")
C("cluster-cmeat",      "or-cmeat",   "outreach pipeline")
C("cluster-cmeat",      "inst-mewery","includes (named contact)")
C("cluster-pharma",     "pj-bfs",     "Phase-3/5 BFS / functional-foods target")
C("cluster-pharma",     "fund-grants","grant pipeline target")
C("cluster-bioreactor", "pj-agri",    "Phase-3 production scale-up")
C("cluster-bioreactor", "pat-fbhfs",  "applies under FBHFS protocols")
C("cluster-seeds",      "pj-agri",    "Phase-3 agri pilots")
C("cluster-seeds",      "pj-plants",  "Phase-3 large-scale field partners")
C("cluster-sports",     "pj-inspira", "biofeedback adjunct B2B target")
C("cluster-sports",     "pj-daat",    "cognitive-stack adjunct positioning")

# ────────────────────────────────────────────────────────────────────────────
# 15. Orphan-node fix-up (legacy block — kept for the fixes that still apply)
# ────────────────────────────────────────────────────────────────────────────
C("pj-dance", "pj-arc12", "taught at")
C("pj-dance", "pj-daat", "parallel cognitive-enhancement track (movement vs crystal)")
C("pj-yeast", "pj-arc12", "lab study by", direction="directed")
C("pj-yeast", "pj-plasma", "same hyperbolic-field protocol family")
C("pj-daat-rs", "pj-daat", "research backing the product")
C("pj-daat-rs", "pat-fbhfs", "scientific basis under FBHFS patent")
C("ch-tg-elec", "pj-tech", "engineering channel for technical audience")
C("ch-li-science", "pj-science", "publishes via")
C("ch-x", "pj-tech", "publishes via")
C("ch-x", "pj-media", "broadcasts via", direction="directed")
C("or-investors", "fund-investors", "feeds into")
C("inst-va", "or-stanford", "Gulf War Syndrome programmes — cancer-treatment pathway target")
C("inst-va", "pj-uap", "VA veterans-care funnel for UAP-adjacent oncology")
C("inst-boeing", "pj-uap", "DoD reverse-engineering benchmark (~$40M illustrative)")
C("inst-osf", "pj-plants", "preregistration platform")
C("inst-osf", "pj-caviar", "preregistration platform")
# inst-mewery polarity is fixed in section 14 above (or-cmeat -> inst-mewery)
C("fund-patrons", "le-us", "funds", amountUsd=165000, moneyEdge=True)
C("fund-investors", "le-us", "investor inflows (when activated)", moneyEdge=True)

# ────────────────────────────────────────────────────────────────────────────
# 14e. IP-licensing transitive edges — owner (le-kz / le-us) → project,
#       computed from patent ownership × patent coverage
# ────────────────────────────────────────────────────────────────────────────
PATENT_OWNER = {}
for c in connections:
    if c["type"] == "owns" and c["from"] in ("le-kz", "le-us"):
        PATENT_OWNER[c["to"]] = c["from"]

_seen_ip = set()
for c in list(connections):
    if c["type"] in ("covers", "scientific base", "scientific base for") and c["from"] in PATENT_OWNER:
        owner = PATENT_OWNER[c["from"]]
        key = (owner, c["to"])
        if key in _seen_ip:
            continue
        _seen_ip.add(key)
        C(owner, c["to"], "IP licensed via", direction="directed",
          via=c["from"], moneyEdge=True, ipLicense=True,
          ipFromKz=(owner == "le-kz"))

# ────────────────────────────────────────────────────────────────────────────
# 15. Russian labels & descriptions — bilingual toggle support
# ────────────────────────────────────────────────────────────────────────────
RU_LABELS = {
    # legal entities
    "le-us":         "ASRP LLC (Флорида)",
    "le-kz":         "ASRP ТОО ПНИР (Казахстан)",
    "le-uk":         "ASRP — UK-юрлицо (на восстановлении)",
    "ubo-group":     "Группа ASRP (UBO-контроль / конечный бенефициар)",
    # team
    "p-vo":          "Овсянникова Валерия Александровна",
    "p-mk":          "Капустин Михаил Михайлович",
    "p-vb":          "Биловоденко Влада",
    "p-is":          "Савельев Иван Викторович",
    "p-as":          "Алиреза Сепехри",
    "p-ig":          "Гривцова Ирина Владимировна",
    "p-db":          "Банченко Денис Юрьевич",
    # external persons
    "p-cardillo":    "Роберт Кардилло",
    "p-nolan":       "Д-р Гарри Нолан",
    "p-dalton":      "Дайан Долтон",
    "p-renwick":     "Д-р Таня Ренвик",
    "p-natasha":     "Наташа (Cortical Labs)",
    "p-aovs":        "Александр Овсянников (ведущий меценат, $100k)",
    "p-burilova":    "Татьяна Бурилова (соавтор pub-5/6 + меценат)",
    "p-shishkin":    "Лев Шишкин (соавтор pub-6 + меценат)",
    "p-mutsalkhanova":"Олена Муцальханова-Ющенко (соавтор pub-5 + меценат)",
    "p-kz":          "Кирилл Змиенко (SAIE, AI-инженер)",
    "p-ak":          "Андрей Крылюк (LFED)",
    "p-ag":          "Александр Громыко (LBED)",
    "p-chernobrov":  "Вадим Чернобров (Космопоиск)",
    "p-lazar":       "Боб Лазар",
    # patents
    "pat-fbhfs":     "KZ 2025/1095.1 — Фрактальная биомедицинская система гиперболических полей (FBHFS)",
    "pat-inspira":   "KZ 2025/0914.1 — Inspira-X (анализ дыхания)",
    "pat-drift":     "KZ 413554 — ASRP.drift (нейроинтеграция)",
    "pat-gfs":       "Патент GFS (Казпатент)",
    "pat-gms":       "Патент GMS (Казпатент)",
    "pat-banchenko-tech": "Патент Banchenko-Technology Set",
    "pat-bfs-us":    "US Copyright TXu002116250 — система Body Food System",
    "pat-biophoton": "KZ 2025/1097.1 — Биофотонная нейродиагностическая система",
    "pat-art":       "KZ 2025/0592.1 + PCT 412362 — Платформа Axionetic Sensing Reactions для искусства",
    # publications
    "pub-1":  "Inspira-X — клиническая валидация (статья)",
    "pub-2":  "Технический обзор BCI и нейроинтерфейсов (отчёт ASRP)",
    "pub-3":  "Архитектурная статья GMS / GFS",
    "pub-4":  "Гривцова — диагностика и управление стрессом",
    "pub-5":  "Прогнозирование социально-геополитических событий — Banchenko-Technology",
    "pub-6":  "Метод мнемонической синхронизации сновидений Банченко",
    "pub-7":  "Banchenko-Market — финансирование фундаментальной науки на блокчейне",
    "pub-8":  "Методы инициации осознанных сновидений (алгоритм Банченко)",
    # projects
    "pj-bot":        "Arcanum12th_BOT — дневник снов",
    "pj-media":      "ASRP.media — официальное СМИ",
    "pj-science":    "ASRP.science — рецензируемый журнал",
    "pj-tech":       "asrp.tech — портфолио проектов и патентов",
    "pj-arc12":      "Arcanum12th.education — образовательная платформа",
    "pj-art":        "ASRP.art — нейрофизиологическая оценка искусства",
    "pj-drift":      "ASRP.drift (PlayOne) — нейроинтеграция",
    "pj-gfs":        "GFS — Глобальная система прогнозирования",
    "pj-gms":        "Global Mental System (GMS) — мета-кластер",
    "pj-bfs":        "Body Food System — персональное питание по генетике",
    "pj-inspira":    "Inspira-X — двухканальный пневмограф + ЭКГ",
    "pj-dance":      "ASRP.dance — нейронаука движений",
    "pj-fashion":    "ASRP.fashion — живые биосовместимые ткани",
    "pj-daat":       "DAAT Crystal — премиум-устройство когнитивного усиления",
    "pj-exch":       "ASRP.exchange / ASRP Market — биржа состояний сознания",
    "pj-kapusta":    "Kapusta.money — субстрат рейтинговой системы",
    "pj-shop":       "ASRPshop — B2C-витрина",
    "pj-stock":      "stock.asrp.* — БД ментальных объектов",
    "pj-crowd":      "Inspira-X — краудфандинг",
    "pj-uap":        "UAP_Reverse_Engineering_Study — публичное исследование с реверс-инжинирингом",
    "pj-plasma":     "Hyperbolic_Field_BloodPlasma_Study — исследование плазмы крови (гиперб. поле)",
    "pj-yeast":      "Hyperbolic_Field_Yeast_Study — дрожжи",
    "pj-daat-rs":    "Hyperbolic_Field_DAAT_Crystal_Study — исследование кристалла",
    "pj-plants":     "Hyperbolic Field Plants Study — растения (OSF)",
    "pj-caviar":     "Hyperbolic Field Fish Caviar Study — икра рыбы (OSF)",
    # channels — Russian explainer suffix
    "ch-tt-tech":    "TikTok @asrp.tech — техно-канал",
    "ch-tt-media":   "TikTok @asrp.media — медиа",
    "ch-tt-science": "TikTok @asrp.science — наука",
    "ch-tt-art":     "TikTok @asrp.art — искусство",
    "ch-tt-arc":     "TikTok @arcanum12th — Arcanum12th",
    "ch-tt-vo":      "TikTok @ovseannikova — личный канал В. Овсянниковой",
    "ch-yt-tech":    "YouTube @ASRPtech — инжен. канал",
    "ch-yt-art":     "YouTube @ASRPart — арт-канал",
    "ch-yt-media":   "YouTube @ASRPmedia — медиа",
    "ch-yt-fashion": "YouTube @ASRPfashion — мода",
    "ch-yt-arc":     "YouTube @Arcanum12th — Arcanum12th",
    "ch-tg-tech":    "Telegram @ASRPtech — техно-канал",
    "ch-tg-elec":    "Telegram @electronics_MD — электроника",
    "ch-fb":         "Facebook /asrp.tech/ — корп. страница",
    "ch-x":          "X (Twitter) @ASRPtech — новости",
    "ch-ig":         "Instagram @asrp.media — медиа",
    "ch-rg":         "ResearchGate Lab — академический профиль",
    "ch-li-co":      "LinkedIn — компания ASRP LLC",
    "ch-li-co2":     "LinkedIn — вторая компания ASRP",
    "ch-li-art":     "LinkedIn-группа — ASRP.art",
    "ch-li-science": "LinkedIn-группа — ASRP.science",
    # outreach
    "or-cortical":   "Cortical Labs — активные переговоры (Q2 2026)",
    "or-nswc":       "NSWC IHD — взаимодействие через Cardillo (LinkedIn)",
    "or-stanford":   "Stanford / лаборатория Nolan — передача админу (фев. 2026)",
    "or-nci":        "NCI SBIR FY26 — подача и системная отмена",
    "or-doe":        "DoE / Лос-Аламос — событие первого читателя",
    "or-investors":  "Журнал аутрича к инвесторам — ожидает материалов",
    # institutions
    "inst-darpa":    "DARPA — Агентство передовых оборонных исследований США",
    "inst-tesla":    "Tesla Inc. — Tesla Business Program",
    "inst-nih":      "NIH / NCI — Национальный институт здравоохранения / онкологии",
    "inst-doe":      "Минэнерго США / Лос-Аламосская национальная лаборатория",
    "inst-stanford": "Стэнфордский университет",
    "inst-cortical": "Cortical Labs — биокомпьютинг (Мельбурн)",
    "inst-nswc":    "NSWC IHD / NAVSEA — центр R&D ВМС США",
    "inst-va":       "Министерство по делам ветеранов США",
    "inst-boeing":   "Boeing — DoD prime",
    "inst-jinr":     "ОИЯИ Дубна — Объединённый институт ядерных исследований",
    "inst-osf":      "Open Science Framework (OSF) — предрегистрация",
    "inst-kazpatent":"Казпатент — патентное ведомство Казахстана",
    "inst-uspto":    "USPTO / Бюро авторских прав США",
    "inst-mewery":   "Чешский партнёр по клеточному мясу (имя не раскрывается)",
    # accreditations
    "acc-darpa":     "Доступ к порталу подачи заявок DARPA BAA",
    "acc-tesla":     "Аккредитация Tesla Business Program",
    # funding
    "fund-patrons":  "Меценаты (≈$165 тыс. накоплено)",
    "fund-investors":"Инвесторы (без долей)",
    "fund-crowd":    "Краудфандинг (Inspira-X)",
    "fund-gov":      "Госконтракты",
    "fund-grants":   "Научные гранты",
    "fund-affiliate":"Партнёрские комиссии",
    "fund-direct":   "Прямые продажи (DAAT-кристаллы)",
    # events
    "ev-theta":      "Theta Network Hackathon — Берлин",
    "ev-astana":     "AstanaHub / Digital Bridge 2025 — питч-баттл Industry 4.0",
    "ev-ecp":        "Сессия ECP-2026-04-04",
    # theory
    "th-temporal":   "Гипотеза темпоральной десинхронизации",
    "th-3dt":        "Three-Dimensional Time — математический формализм",
    "th-channels":   "Внутренняя таксономия Channel-19 / Channel-21",
    "th-hyperbolic": "Гиперболические дисперсные материалы для детекции рака",
    "th-qrl":        "Quantum Resistant Ledger (QRL) — квантово-устойчивый блокчейн",
    "pj-agri":       "Hyperbolic_Field_Agricultural_Study — агро-полевые испытания (Day 4+)",
    "or-cmeat":      "Аутрич по cultured-meat (приватный)",
    "or-mjff":       "Аутрич MJFF — нейродегенеративные заболевания (приватный)",
    "ev-tg-forbes":  "Telegram-broadcast 20.04.2026 — носители DAAT из Forbes",
    "ch-pinterest":  "Pinterest boards (планируется)",
    "ch-medium":     "Medium (планируется по проектам)",
    "ch-vk":         "VK (планируется)",
    "tool-vidrush":  "Vidrush — класс AI-производства",
    "tool-dohoo":    "DOHOO — класс мульти-платформенного паблишера",
    "tool-pinterest":"Pinterest почасовая автоматизация — класс SEO discovery",
}

# ────────────────────────────────────────────────────────────────────────────
# 16. Russian descriptions — bilingual side-panel support
# ────────────────────────────────────────────────────────────────────────────
RU_DESCRIPTIONS = {
    # Legal entities
    "le-us":  "Advanced Scientific Research Projects LLC · Florida #L17000209665 · операционная/коммерческая компания (Tesla Business Program, DARPA BAA, USD-контрактация)",
    "le-kz":  "📌 Почему ТОО ПНИР важно. Казахстанское ТОО (БИН 240140033296, Байконыр, 27 янв. 2024) держит патентный портфель — 8 патентов, 6 Казпатент + PCT 412362 + биофотонный + ASRP.art. Это делает IP-лицензирование отдельным каналом выручки, не пересекающимся с операционным USD-контрактингом через ASRP LLC (Флорида). KZ-юрисдикция обусловлена требованиями к резидентности учредителей и спецификой корпоративного регулирования РК. Поэтапная консолидация — холдинги, акционерные соглашения, договоры о совместной деятельности — идёт. UBO-треугольник: Овсянникова · Капустин · Банченко.",
    "le-uk":  "На стадии восстановления корпоративного статуса (reinstatement)",
    "ubo-group": "Бенефициарное владение и совместный стратегический контроль — В. Овсянникова, М. Капустин, Д. Банченко, независимо от формальной регистрации в юрисдикциях",
    # Team
    "p-vo":  "Главный биомедицинский инженер — авторство и воспроизведение протоколов плазмы крови / агро / дрожжей",
    "p-mk":  "AI Dream Match Search Model · платформенная инженерия",
    "p-vb":  "Риски + комплаенс · соавтор whitepaper",
    "p-is":  "Старший исследователь · Фонд DNA Resonance Research",
    "p-as":  "Соавтор по физике · whitepaper",
    "p-ig":  "Член Scientific European Society Hanover · диагностика и управление стрессом",
    "p-db":  "Архитектор Banchenko-Technology · автор гипотезы темпоральной десинхронизации в UAP-смежной онкологии",
    "p-kz":  "Анализ исследований · аналитик данных по плазме крови · репозитории · AI-пайплайны",
    "p-ak":  "Lead Front-End Developer",
    "p-ag":  "Lead Back-End Developer",
    "p-chernobrov": "Линия полевых исследований, упоминаемая внутри UAP-репо (chernobrov-archive)",
    "p-lazar": "Историческая линия для заявлений по реверс-инжинирингу UAP (S-4, элемент-115)",
    # External persons
    "p-cardillo": "Опубликовал в LinkedIn анализ кластера 11 учёных · апрель 2026",
    "p-nolan": "UAP-смежная онкология · фильм «The Phenomenon of Disclosure»",
    "p-dalton": "Управляет календарём д-ра Nolan; контакт по запросу под NDA",
    "p-renwick": "Контакт через официальный портал NIH SBIR · трек NCI SBIR FY26",
    "p-natasha": "Сообщила в Q2 2026 о текущем рассмотрении плазма-исследования ASRP",
    "p-aovs": "Ведущий меценат ASRP — вероятная семейная связь с В. Овсянниковой",
    "p-burilova": "Соавтор whitepaper (Banchenko-Technology + dream-sync) И меценат уровня $5k",
    "p-shishkin": "Соавтор статьи по синхронизации сновидений + меценат",
    "p-mutsalkhanova": "Соавтор Banchenko-Technology forecasting + меценат",
    # Patents
    "pat-fbhfs": "Казпатент · научная база DAAT Crystal + ASRP.fashion + плазменного исследования",
    "pat-inspira": "Казпатент · формальная экспертиза пройдена · ожидает substantive",
    "pat-drift": "Казпатент · рецензируемая публикация ASRP.drift AI",
    "pat-gfs": "Казпатент · документирует механизм Kapusta как rating-substrate",
    "pat-gms": "Казпатент · архитектура мета-кластера",
    "pat-banchenko-tech": "Казпатент · комбинированные методы (dream-sync, мнемоническая синхронизация, GFS, market)",
    "pat-bfs-us": "Бюро авторских прав США · методология персонализированного питания Body Food System",
    "pat-biophoton": "Казпатент · формальная экспертиза пройдена → substantive · публичный репо: github.com/denisbanchenko/Kazpatent_Biophotonic_Neurodiagnostic_System_Patent",
    "pat-art": "Казпатент + PCT international · стадия substantive экспертизы · научная база для SPR (Sensing Platform of Reactions)",
    # Publications
    "pub-1": "ResearchGate: 404163473 · опубликована в журнале",
    "pub-2": "ResearchGate: 396126506 · технический отчёт (готовится статья)",
    "pub-3": "ResearchGate: 388438082 · Journal of Investment Banking and Finance, январь 2025",
    "pub-4": "ResearchGate: 394039715 · American Journal of Medical and Clinical Research & Reviews, июль-август 2024",
    "pub-5": "ResearchGate: 381995064 · июль 2024 · DOI 10.33425/2690-8077.1119 · 14 авторов",
    "pub-6": "ResearchGate: 378492219 · опубликованная статья (после препринта 377492383)",
    "pub-7": "ResearchGate: 378492156 · журнал, согласившийся с нестандартной рамкой после отказов KZ/UA/US/UK",
    "pub-8": "ResearchGate: 370913525 · опубликована (2023)",
    # Projects
    "pj-bot":     "Дневник снов + биосенсорные данные → GFS",
    "pj-media":   "Официальное СМИ + научпоп-контент",
    "pj-science": "Рецензируемый научный журнал",
    "pj-tech":    "Сайт-портфолио проектов и патентов",
    "pj-arc12":   "Образовательная платформа · источник сырых биологических данных (генетика, ЭЭГ, GSR, ANS)",
    "pj-art":     "Нейрофизиологическая оценка искусства (SPR)",
    "pj-drift":   "Нейроинтеграция для синхронизации команд",
    "pj-gfs":     "Анализ снов + биосенсоров → прогнозы (B2G/B2B)",
    "pj-gms":     "Синхронизация когнитивных процессов · мета-кластер",
    "pj-bfs":     "Персональное питание на основе генетики",
    "pj-inspira": "Двухканальный пневмограф + ЭКГ · стек DAAT Crystal",
    "pj-dance":   "Нейронаука движений · активация коры через сложные движения",
    "pj-fashion": "Живые биосовместимые ткани (растения/бактерии/грибы)",
    "pj-daat":    "Премиум-устройство когнитивного усиления · кристалл + Inspira-X + нейроинтерфейс",
    "pj-exch":    "Биржа состояний сознания",
    "pj-kapusta": "Субстрат системы рейтингов (НЕ просто валюта) · механизм описан в патенте GFS",
    "pj-shop":    "B2C-витрина для DAAT-кристаллов + изделий ASRP.fashion",
    "pj-stock":   "База данных Ментальных Объектов · ингест через нейроинтерфейс",
    "pj-crowd":   "Kickstarter-класс кампания",
    "pj-uap":     "Публичное реверс-инжиниринг исследование (DoE — первый читатель)",
    "pj-plasma":  "Воспроизведено В. Овсянниковой · вызвало вовлечение Cortical Labs",
    "pj-yeast":   "Стат. превосходство 2-й группы · апрель 2026",
    "pj-daat-rs": "Протокол измерений ЭЭГ / HRV / GSR / автономной нервной системы",
    "pj-plants":  "Прорастание + кинетика роста · предрегистрация запланирована 22.04.2026",
    "pj-caviar":  "Эмбриональная кинетика в аквакультуре · предрегистрация запланирована 22.04.2026",
    "pj-agri":    "Активные полевые испытания, измерения Day-4+ · double-blind активация",
    # Channels (RU descriptions for the most-shown ones)
    "ch-tt-tech":    "TikTok · 6014 подписчиков · 51,4K лайков",
    "ch-tt-media":   "TikTok · 325 подписчиков · 2499 лайков",
    "ch-tt-science": "TikTok · 20 подписчиков · 353 лайка",
    "ch-tt-art":     "TikTok · 12 подписчиков · 34 лайка",
    "ch-tt-arc":     "TikTok · новый",
    "ch-tt-vo":      "TikTok · личный (В. Овсянникова)",
    "ch-yt-tech":    "YouTube · 447 подписчиков · 22 видео · 27K просмотров (с янв. 2018)",
    "ch-yt-art":     "YouTube · активный",
    "ch-yt-media":   "YouTube · 18 подписчиков",
    "ch-yt-fashion": "YouTube · активный",
    "ch-yt-arc":     "YouTube · активный",
    "ch-tg-tech":    "Telegram · главный канал анонсов",
    "ch-tg-elec":    "Telegram · инженерные апдейты",
    "ch-li-co":      "LinkedIn · корпоративная страница · 50+ подписчиков",
    "ch-li-co2":     "LinkedIn · вторая корпоративная страница",
    "ch-li-art":     "LinkedIn-группа по проекту",
    "ch-li-science": "LinkedIn-группа по проекту",
    "ch-fb":         "Facebook · «ASRP. AI-технологии»",
    "ch-x":          "X (Twitter) · новости и анонсы",
    "ch-ig":         "Instagram · кросс-постинг медиа-контента (превью только после входа)",
    "ch-rg":         "ResearchGate · научный профиль",
    "ch-pinterest":  "По-проектные Pinterest-доски · SEO-движок через hourly cron",
    "ch-medium":     "Long-form публикации по проектам",
    "ch-vk":         "VK Clips + VK Video + VK Notes — русскоязычная аудитория",
    # Outreach
    "or-cortical":  "Playbook аутрича: компетенция выстроена (Валерия воспроизводит) → репо опубликован → LinkedIn-контент в окно хайпа DishBrain → входящий → review (Q2 2026)",
    "or-nswc":      "Апрель 2026 · Cardillo опубликовал анализ кластера 11 учёных · ASRP ответили UAP + плазма репозиториями · обратная связь получена",
    "or-stanford":  "4 февраля 2026 · LinkedIn-DM · Nolan ответил «Sounds interesting» в течение 3 минут · направил к админу Дайан Долтон · отправлено развёрнутое письмо + фото фибрина с легендой T₊/T₀/T₋",
    "or-nci":       "Подача 22 августа 2025 (Notice 75N91025R00005) · NCI отменил конкурс в октябре 2025 из-за истечения авторизации SBIR/STTR · материалы сохранены для повторной подачи",
    "or-doe":       "Сегмент Минэнерго США / Лос-Аламосской национальной лаборатории стал первым федеральным читателем UAP_Reverse_Engineering_Study репозитория в течение нескольких часов после публикации",
    "or-investors": "≈десяток заинтересованных инвесторов / семейных офисов в переговорах; deck блокирует закрытие · список будет передан CEO",
    "or-cmeat":     "Аутрич к FDA/EU-аккредитованным и масштабирующим производителям cultured meat · pitch: модуляция биологического отклика → меньшее время удвоения → ниже стоимость среды на кг",
    "or-mjff":      "Корреспонденция 28 фев / 2 мар 2026 · публичного сигнала пока нет",
    # Institutions
    "inst-darpa":   "U.S. Defense Advanced Research Projects Agency",
    "inst-tesla":   "Tesla Business Program · корпоративная аккредитация",
    "inst-nih":     "National Institutes of Health · National Cancer Institute",
    "inst-doe":     "Лос-Аламосская национальная лаборатория · историческая линия UAP-adjacent reverse-engineering",
    "inst-stanford":"Лаборатория Гарри Нолана — UAP-смежные онкологические исследования",
    "inst-cortical":"Пионер биокомпьютинга в Мельбурне (DishBrain · нейрон-кремниевая платформа)",
    "inst-nswc":    "Naval Surface Warfare Center Indian Head Division · центр R&D ВМС США",
    "inst-va":      "Программы по Gulf War Syndrome для ветеранов",
    "inst-boeing":  "DoD prime · парламентские раскрытия о расходах на reverse-engineering",
    "inst-jinr":    "Объединённый институт ядерных исследований (~31 страна-член) · синтез 115-го элемента · институциональный контекст",
    "inst-osf":     "Платформа предрегистрации для исследований ASRP",
    "inst-kazpatent":"Патентное ведомство Казахстана",
    "inst-uspto":   "Патентное и авторско-правовое ведомство США",
    "inst-mewery":  "Чешский партнёр по cultured meat (placeholder, ожидает публичного подтверждения)",
    "inst-mjff":    "Фонд исследования нейродегенеративных заболеваний",
    "inst-auction-tier1":"Аукционный дом высшего эшелона · цель Фазы 4 для ASRP.art · имя не раскрывается",
    "inst-auction-tier2":"Аукционный дом высшего эшелона · цель Фазы 4 для ASRP.art · имя не раскрывается",
    "inst-saatchi": "Saatchi Gallery (Лондон) и Saatchi Art (онлайн-платформа) · цель Фазы 4 · НЕ рекламное агентство Saatchi & Saatchi",
    "inst-koniku":  "Биогибридные нейрон-кремниевые системы · цель Фазы 4 для ASRP.drift / DAAT",
    "inst-neurable":"Потребительский нейроинтерфейс · цель Фазы 4",
    "inst-paradromics":"Высокоскоростной BCI-имплант · цель Фазы 4",
    # Accreditations
    "acc-darpa": "Аутентифицированный экстранет-аккаунт для подачи BAA-предложений · НЕ merit-based награда — явно уточнено",
    "acc-tesla": "Корпоративная аккредитация",
    # Funding
    "fund-patrons":   "Регулярные меценатские взносы по 7 уровням на asrp.tech/ru/patrons (от Главного Филантропа до Индивидуального Вкладчика); накоплено подтверждено ≈$165 тыс.; ведущий меценат Александр Овсянников — $100 тыс.; традиция отсылает к Медичи / Карнеги / Рокфеллеру",
    "fund-investors": "Модели сотрудничества без передачи долей — договоры о совместной деятельности, авансы под deliverable, структурные займы — опубликованы на asrp.tech/ru/investors; намеренно сохраняют UBO-контроль в группе из нескольких юрисдикций",
    "fund-crowd":     "Кампания краудфандинга Kickstarter-уровня готовится под Inspira-X (двухканальный пневмограф + ЭКГ); предлончевый донат-линк уже работает на asrp.tech/ru/donate/asrp; предзаказы финансируют производственный тираж",
    "fund-gov":       "Гражданские и оборонные тендеры в США и партнёрских юрисдикциях — подрядчики DoD (Boeing-класс), VA (программы Gulf War Syndrome), R&D уровня DARPA (портал BAA активен), NCI SBIR FY26 готов к повторной подаче после восстановления авторизации",
    "fund-grants":    "Пайплайн научных грантов — гранты UA/MD на восстановление почв после конфликта под агроисследование, роялти-пилоты с агрохолдингами, аутбаунд в фонды (MJFF по нейродегенеративным, фонды клеточного мяса); схема: заявка → пилот → роялти",
    "fund-affiliate": "Реализованный партнёрский / комиссионный доход через паттерн кросс-промо — баннерные размещения в ASRP.media + ASRP.science + Arcanum12th + YouTube; канонический рабочий пример — партнёрская продажа нейроинтерфейса через баннер в ASRP.media (читатель перешёл, купил, ASRP получила комиссию)",
    "fund-direct":    "Реализованные прямые продажи B2C/B2B — DAAT-кристаллы (премиум-категория) через asrp.tech + (готовится) ASRPshop + сообщество Arcanum12th; пилотные сигналы: топ-менеджмент банка приобрёл устройство, среди индивидуальных носителей — люди из списка Forbes (со слов основателя; название учреждения и имена не раскрываются)",
    # Events
    "ev-theta":  "GFS представлен на европейской конференции и хакатоне",
    "ev-astana": "GFS подан на питчинг; не прошёл отборочный этап",
    "ev-ecp":    "Внутренняя сессия, давшая датасет для последующего плазма-исследования",
    "ev-tg-forbes": "Broadcast-пост основателя (просмотры:288 · форварды:2) · названы индивидуальные носители DAAT Crystal из списка Forbes (имена не раскрыты)",
    # Theory anchors
    "th-temporal": "Первичный патогенный фактор в UAP-смежной онкологии = темпоральная десинхронизация биологических процессов (НЕ классическое мутагенное повреждение); терапия = коррекция кинетики процессов, не цитотоксическое воздействие",
    "th-3dt":      "World Scientific · DOI 10.1142/S2424942425500045 · математический формализм, расширяющий физическое время с одной размерности до трёх; даёт теоретическую основу для нотации T₊/T₀/T₋ кинетики",
    "th-channels": "Channel-19 = ускоренная кинетика (T₊, Δt > 0) · Channel-21 = замедленная кинетика (T₋, Δt < 0) · внутреннее обозначение; T-нотация — для внешней переписки (например, с Nolan)",
    "th-hyperbolic":"Внешняя рецензируемая статья, поддерживающая связку «гиперболические поля × онкология»",
    "th-qrl":       "Квантово-устойчивый блокчейн для безопасной передачи и хранения Ментальных Объектов · субстрат для расчётного слоя Kapusta.money",
    # Tooling classes
    "tool-vidrush":  "Текстовый prompt → полное документальное видео; референсный пример для слоя AI-производства контент-завода ASRP",
    "tool-dohoo":    "Кросс-платформенный авто-постинг с Video-to-Text + ChatGPT адаптацией под платформу",
    "tool-pinterest":"Hourly cron · 3 доски параллельно · ≈15-дневный ramp-up до первого US-трафика",
    # Clusters
    "cluster-cmeat":      "UPSIDE Foods · GOOD Meat · BlueNalu · Mosa Meat · Aleph Farms · Meatly · MIRAI Foods · Czech cellular-meat partner (name withheld) — pitch: модуляция биологического отклика → меньшее время удвоения → ниже стоимость среды на кг",
    "cluster-pharma":     "Nestlé Health Science · Danone · Abbott · DSM-Firmenich · Chr. Hansen · BASF · Glanbia — цели Фазы 3 (functional drinks) + Фазы 5 (фарма-адъюванты)",
    "cluster-bioreactor": "AlgaTech · Cyanotech · Earthrise — биореакторы и производители водорослей · партнёры Фазы 3 для масштабирования биопродуктов FBHFS",
    "cluster-seeds":      "Syngenta · Bayer · Corteva · Limagrain · AeroFarms · Monterey Bay Mushrooms · Promyc · MycoTech — крупномасштабные агро-пилоты Фазы 3 для FBHFS",
    "cluster-sports":     "Бренды спортивного питания как B2B-цели для biofeedback-комплемента Inspira-X + позиционирование когнитивного стека DAAT",
}

for el in elements:
    if el["id"] in RU_LABELS:
        el["labelRu"] = RU_LABELS[el["id"]]
    if el["id"] in RU_DESCRIPTIONS:
        el["descriptionRu"] = RU_DESCRIPTIONS[el["id"]]
    el.setdefault("tags", [el["type"]])

# ────────────────────────────────────────────────────────────────────────────
# Output
# ────────────────────────────────────────────────────────────────────────────
out = {
    "elements": elements,
    "connections": connections,
}

dst = Path(__file__).parent / "asrp_kumu.json"
dst.write_text(json.dumps(out, indent=2, ensure_ascii=False))

print(f"wrote {dst}")
print(f"  elements:    {len(elements)}")
print(f"  connections: {len(connections)}")
types = {}
for el in elements:
    types[el["type"]] = types.get(el["type"], 0) + 1
for k, v in sorted(types.items(), key=lambda x: -x[1]):
    print(f"    {k}: {v}")
