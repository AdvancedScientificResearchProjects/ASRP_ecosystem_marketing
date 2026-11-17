#!/usr/bin/env python3
"""Generates the showcase visuals (never hand-edit the SVG output; edit this file).

    python3 tools/build_visuals.py

Output
    docs/assets/banner/hero-banner.{en,ru}.svg        generated illustration (not a product screenshot)
    docs/assets/infographics/maturity-map.{en,ru}.svg component names and statuses copied from
                                                       docs/ECOSYSTEM.md (source dated 2026-Q2)
    docs/assets/infographics/ecosystem-flow.{en,ru}.svg  how the clusters feed each other, with statuses
    docs/assets/icons/*.svg                           navigation icons

Rules followed (ASRP visual standard): every SVG has <title>, <desc> and a viewBox; text is
measured and must fit its container (the build fails otherwise); a status is always written as
text and paired with a shape, never carried by colour alone; palette and fonts come from one
token block below. Palette matches the ASRP study repositories.
"""
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"

# --- design tokens ---------------------------------------------------------------------------
BG0, BG1, PANEL, LINE = "#070b18", "#0d1530", "#0b1430", "#2a3b78"
INK, MUTED = "#e6ecff", "#8ea0d6"
TEAL, VIOLET, GOLD, GREEN, AMBER, BLUE = "#4ecdc4", "#a78bfa", "#ffcf5c", "#34d399", "#ffa657", "#6f9bff"
FS_KICKER, FS_BODY, FS_SMALL, FS_MIN = 14, 15, 13, 13  # px; nothing below FS_MIN
RADIUS = 12


def text_width(s, size, bold=False):
    """Conservative width estimate (px) so that no label can be clipped."""
    w = 0.0
    for ch in s:
        if ch == " ":
            w += 0.30
        elif ch in "il.,:;'|!·":
            w += 0.30
        elif ch in "mwMW@ШЩЖМЫЮшщжмыю":
            w += 0.90
        elif ch.isupper() or ch.isdigit():
            w += 0.68
        elif "а" <= ch <= "я" or ch == "ё":
            w += 0.60
        else:
            w += 0.56
    return w * size * (1.07 if bold else 1.0)


def fit(s, size, box, bold=False, spacing=0.0):
    w = text_width(s, size, bold) + spacing * len(s)
    if w > box:
        raise SystemExit("TEXT DOES NOT FIT (%.0f > %.0f px): %r" % (w, box, s))
    return w


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=FS_BODY, fill=INK, anchor="start", weight=400, spacing=0, box=None):
    if size < FS_MIN:
        raise SystemExit("font below minimum: %r" % s)
    if box is not None:
        fit(s, size, box, weight >= 600, spacing)
    ls = " letter-spacing='%s'" % spacing if spacing else ""
    return ("<text x='%s' y='%s' font-family=\"%s\" font-size='%s' fill='%s' text-anchor='%s' "
            "font-weight='%s'%s>%s</text>" % (x, y, FONT, size, fill, anchor, weight, ls, esc(s)))


def svg_open(w, h, title, desc):
    return ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 %d %d\" width=\"%d\" height=\"%d\" "
            "role=\"img\" aria-labelledby=\"t d\">\n<title id=\"t\">%s</title>\n<desc id=\"d\">%s</desc>\n"
            "<defs><linearGradient id='bg' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='%s'/>"
            "<stop offset='1' stop-color='%s'/></linearGradient>"
            "<filter id='glow' x='-50%%' y='-50%%' width='200%%' height='200%%'><feGaussianBlur stdDeviation='3' "
            "result='b'/><feMerge><feMergeNode in='b'/><feMergeNode in='SourceGraphic'/></feMerge></filter></defs>\n"
            "<rect width='%d' height='%d' rx='18' fill='url(#bg)'/>\n"
            % (w, h, w, h, esc(title), esc(desc), BG0, BG1, w, h))


def write(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)
    print("wrote", rel, len(content))


# --- hero banner -----------------------------------------------------------------------------
BANNER = {
    "en": {
        "title": "ASRP Ecosystem",
        "desc": ("Generated illustration, not a product screenshot. Six clusters (Education, Science, Media, "
                 "R&D and Deep Tech, Consciousness Tech, Commerce) linked to one ASRP hub; headline; three "
                 "figures taken from this repository: 8 publications, 6 patent applications plus 1 PCT, "
                 "4 open study repositories."),
        "kicker": "ADVANCED SCIENTIFIC RESEARCH PROJECTS",
        "tag": "MARKETING & MONETIZATION HUB",
        "sub": ["Research, education, media and deep tech", "in one cross-linked system"],
        "nodes": ["Education", "Science", "Media", "R&D / Deep Tech", "Consciousness Tech", "Commerce"],
        "chips": ["8 publications", "6 patent applications + 1 PCT", "4 open study repos"],
    },
    "ru": {
        "title": "Экосистема ASRP",
        "desc": ("Сгенерированная иллюстрация, не скриншот продукта. Шесть кластеров (образование, наука, "
                 "медиа, R&D и deep tech, технологии сознания, коммерция) связаны с одним узлом ASRP; "
                 "заголовок; три числа из этого репозитория: 8 публикаций, 6 патентных заявок плюс 1 PCT, "
                 "4 открытых репозитория исследований."),
        "kicker": "ADVANCED SCIENTIFIC RESEARCH PROJECTS",
        "tag": "ХАБ МАРКЕТИНГА И МОНЕТИЗАЦИИ",
        "sub": ["Исследования, образование, медиа и deep tech", "в одной связанной системе"],
        "nodes": ["Образование", "Наука", "Медиа", "R&D / Deep Tech", "Технологии сознания", "Коммерция"],
        "chips": ["8 публикаций", "6 патентных заявок + 1 PCT", "4 открытых репозитория"],
    },
}
NODE_COLORS = [GOLD, TEAL, VIOLET, GREEN, BLUE, AMBER]


def banner(lang):
    c = BANNER[lang]
    W, H = 1200, 330
    o = [svg_open(W, H, c["title"], c["desc"])]
    cx, cy, rx, ry = 232, 166, 150, 100
    pts = []
    for i in range(6):
        ang = math.radians(-90 + 60 * i)
        pts.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
    # faint outer ring and spokes
    ring = " ".join("%s%.1f,%.1f" % ("M" if i == 0 else "L", x, y) for i, (x, y) in enumerate(pts)) + " Z"
    o.append("<path d='%s' fill='none' stroke='%s' stroke-opacity='0.55'/>" % (ring, LINE))
    for i, (x, y) in enumerate(pts):
        o.append("<line x1='%d' y1='%d' x2='%.1f' y2='%.1f' stroke='%s' stroke-width='1.6' stroke-opacity='0.75' "
                 "stroke-dasharray='5 7'><animate attributeName='stroke-dashoffset' from='24' to='0' dur='%.1fs' "
                 "repeatCount='indefinite'/></line>" % (cx, cy, x, y, NODE_COLORS[i], 2.4 + 0.3 * i))
    o.append("<circle cx='%d' cy='%d' r='36' fill='%s' stroke='%s' stroke-width='2' filter='url(#glow)'/>"
             % (cx, cy, PANEL, TEAL))
    o.append(text(cx, cy + 7, "ASRP", 20, INK, "middle", 800, 1))
    for i, (x, y) in enumerate(pts):
        o.append("<circle cx='%.1f' cy='%.1f' r='9' fill='%s' stroke='%s' stroke-width='2.4'/>"
                 % (x, y, BG0, NODE_COLORS[i]))
        label = c["nodes"][i]
        w = fit(label, FS_SMALL, 2 * min(x, 470 - x) - 8)
        ly = y - 18 if i == 0 else y + 27
        o.append(text("%.1f" % x, "%.1f" % ly, label, FS_SMALL, INK, "middle", 600))
    tx = 520
    box = W - tx - 36
    o.append(text(tx, 66, c["kicker"], FS_KICKER, TEAL, "start", 700, 2, box))
    o.append(text(W - 36, 36, c["tag"], FS_SMALL, MUTED, "end", 700, 2, 420))
    o.append(text(tx, 128, c["title"], 54, INK, "start", 800, 0, box))
    for i, line in enumerate(c["sub"]):
        o.append(text(tx, 170 + 28 * i, line, 21, MUTED, "start", 400, 0, box))
    x = tx
    for i, chip in enumerate(c["chips"]):
        w = text_width(chip, FS_KICKER, True) + 28
        if x + w > W - 30:
            raise SystemExit("chips overflow the banner: %r" % chip)
        col = [GOLD, TEAL, GREEN][i]
        o.append("<rect x='%.1f' y='246' width='%.1f' height='38' rx='19' fill='%s' fill-opacity='0.08' stroke='%s'/>"
                 % (x, w, col, col))
        o.append(text("%.1f" % (x + w / 2), 271, chip, FS_KICKER, INK, "middle", 700))
        x += w + 12
    o.append("</svg>\n")
    return "\n".join(o)


# --- maturity map ----------------------------------------------------------------------------
# Component names and stage labels are copied from docs/ECOSYSTEM.md (tables "Live", "Active
# Development", "Planned", "Research Repositories"). Repository visibility was checked through the
# GitHub API on 2026-11-17.
MATURITY = {
    "en": {
        "title": "ASRP ecosystem: what exists and at what stage",
        "desc": ("Four columns with text status labels. Live (4): Arcanum12th_BOT, ASRP.media, ASRP.science, "
                 "asrp.tech. Active development (12): Arcanum12th.education, YouTube @ASRPtech, ASRP.art, "
                 "ASRP.drift (PlayOne), GFS, Global Mental System, Body Food System, Inspira-X, ASRP.dance, "
                 "ASRP.fashion, DAAT Crystal, ASRP.exchange / ASRP Market. Planned (3): ASRPshop, ASRP Market "
                 "/stock subdomain, Inspira-X crowdfunding. Research studies (7): UAP Reverse Engineering, "
                 "Blood Plasma, Agricultural, Yeast, DAAT Crystal Study, Plants Study, Fish Caviar Study, each "
                 "with its stage as stated in the repository."),
        "sub": "ASRP's own status labels (docs/ECOSYSTEM.md, 2026-Q2), not re-verified",
        "tag": "ASRP · ECOSYSTEM",
        "cols": [
            ("LIVE", "4", "●", GREEN, "public services online"),
            ("ACTIVE DEVELOPMENT", "12", "◐", GOLD, "prototype, IP filing or pilot"),
            ("PLANNED", "3", "○", AMBER, "scope defined, launch pending"),
            ("RESEARCH STUDIES", "7", "◆", VIOLET, "repo visibility · stage"),
        ],
        "research": [
            ("UAP Reverse Engineering", "public · NDA-tier materials"),
            ("Blood Plasma", "public · lab results published"),
            ("Agricultural", "public · field trials (Day 4+)"),
            ("Yeast (S. cerevisiae)", "public · OSF registered"),
            ("DAAT Crystal Study", "private · recruitment"),
            ("Plants Study", "OSF preregistration planned"),
            ("Fish Caviar Study", "OSF preregistration planned"),
        ],
        "planned": ["ASRPshop", "ASRP Market /stock", "Inspira-X crowdfunding"],
        "foot": "Active development is not a shipped product. Repos checked 2026-11-17.",
    },
    "ru": {
        "title": "Экосистема ASRP: что есть и на какой стадии",
        "desc": ("Четыре колонки с текстовыми статусами. Работает (4): Arcanum12th_BOT, ASRP.media, "
                 "ASRP.science, asrp.tech. В активной разработке (12): Arcanum12th.education, YouTube @ASRPtech, "
                 "ASRP.art, ASRP.drift (PlayOne), GFS, Global Mental System, Body Food System, Inspira-X, "
                 "ASRP.dance, ASRP.fashion, DAAT Crystal, ASRP.exchange / ASRP Market. Планируется (3): ASRPshop, "
                 "субдомен /stock ASRP Market, краудфандинг Inspira-X. Исследовательские репозитории (7): "
                 "реверс-инжиниринг UAP, плазма крови, агроисследование, дрожжи, исследование DAAT-кристалла, "
                 "исследование растений, исследование икры рыбы, у каждого стадия как указано в репозитории."),
        "sub": "Статусы как в docs/ECOSYSTEM.ru.md (2 кв. 2026), не перепроверялись",
        "tag": "ASRP · ЭКОСИСТЕМА",
        "cols": [
            ("РАБОТАЕТ", "4", "●", GREEN, "публичные сервисы в сети"),
            ("В АКТИВНОЙ РАЗРАБОТКЕ", "12", "◐", GOLD, "прототип, заявка на ИС, пилот"),
            ("ПЛАНИРУЕТСЯ", "3", "○", AMBER, "объём определён, запуск позже"),
            ("ИССЛЕДОВАНИЯ", "7", "◆", VIOLET, "видимость репо · стадия"),
        ],
        "research": [
            ("Реверс-инжиниринг UAP", "публичный · часть под NDA"),
            ("Плазма крови", "публичный · опубликованы"),
            ("Агроисследование", "публичный · полевые (день 4+)"),
            ("Дрожжи (S. cerevisiae)", "публичный · OSF"),
            ("DAAT-кристалл", "закрытый · набор участников"),
            ("Растения", "предрегистрация OSF в плане"),
            ("Икра рыбы", "предрегистрация OSF в плане"),
        ],
        "planned": ["ASRPshop", "ASRP Market /stock", "Краудфандинг Inspira-X"],
        "foot": "Разработка — не готовый продукт. Репозитории проверены 17.11.2026.",
    },
}
LIVE = ["Arcanum12th_BOT", "ASRP.media", "ASRP.science", "asrp.tech"]
ACTIVE = ["Arcanum12th.education", "YouTube @ASRPtech", "ASRP.art", "ASRP.drift (PlayOne)",
          "GFS (forecasting system)", "Global Mental System", "Body Food System", "Inspira-X",
          "ASRP.dance", "ASRP.fashion", "DAAT Crystal", "ASRP.exchange / ASRP Market"]


def maturity(lang):
    c = MATURITY[lang]
    W, H = 1200, 600
    o = [svg_open(W, H, c["title"], c["desc"])]
    o.append(text(24, 46, c["title"], 26, INK, "start", 700, 0, 860))
    o.append(text(24, 72, c["sub"], FS_KICKER, MUTED, "start", 400, 0, W - 48))
    o.append(text(W - 24, 46, c["tag"], FS_KICKER, TEAL, "end", 700, 2, 280))
    gap, x0, y0 = 16, 24, 94
    cw = (W - 2 * x0 - 3 * gap) / 4
    ch = H - y0 - 50
    inner = cw - 36
    active = [n.replace("(forecasting system)", "(прогнозирование)") if lang == "ru" else n for n in ACTIVE]
    lists = [[(n, None) for n in LIVE], [(n, None) for n in active],
             [(n, None) for n in c["planned"]], c["research"]]
    for i, (name, count, mark, col, hint) in enumerate(c["cols"]):
        x = x0 + i * (cw + gap)
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='%d' rx='%d' fill='%s' stroke='%s'/>"
                 % (x, y0, cw, ch, RADIUS, PANEL, LINE))
        o.append("<rect x='%.1f' y='%d' width='%.1f' height='5' rx='2.5' fill='%s'/>" % (x + 18, y0 + 14, cw - 36, col))
        o.append(text("%.1f" % (x + 14), y0 + 47, "%s %s · %s" % (mark, name, count), FS_MIN, col, "start", 800, 0, cw - 26))
        o.append(text("%.1f" % (x + 18), y0 + 69, hint, FS_SMALL, MUTED, "start", 400, 0, inner))
        o.append("<line x1='%.1f' y1='%d' x2='%.1f' y2='%d' stroke='%s'/>" % (x + 18, y0 + 84, x + cw - 18, y0 + 84, LINE))
        y = y0 + 110
        for item, subline in lists[i]:
            o.append("<circle cx='%.1f' cy='%.1f' r='3' fill='%s'/>" % (x + 22, y - 5, col))
            o.append(text("%.1f" % (x + 30), y, item, FS_KICKER, INK, "start", 600, 0, cw - 44))
            if subline:
                o.append(text("%.1f" % (x + 30), y + 18, subline, FS_SMALL, MUTED, "start", 400, 0, cw - 44))
                y += 49
            else:
                y += 29
        if y - 20 > y0 + ch:
            raise SystemExit("column %d overflows its card" % i)
    o.append(text(24, H - 20, c["foot"], FS_SMALL, MUTED, "start", 400, 0, W - 48))
    o.append("</svg>\n")
    return "\n".join(o)


# --- ecosystem flow --------------------------------------------------------------------------
# Statuses are the project's own labels (docs/ECOSYSTEM.md, docs/FUNDING.md). Solid arrow = flow
# that runs today, dashed arrow = target; the line style is explained in the legend in words.
FLOW = {
    "en": {
        "title": "How the pieces fit",
        "desc": ("Flow diagram with a text status in every box. Education and audience (Telegram bot: live; "
                 "Arcanum12th courses: pilot) sends data and attention to R&D and deep tech (studies, patent "
                 "applications: in development), which sends results to Science and media (papers, open repos, "
                 "ASRP.media: live). Dashed target arrows: trust and reach from Science and media to Commerce "
                 "(B2B / B2G, products, licensing: planned) and revenue from Commerce back to R&D. Funding "
                 "(patrons: active; grants: in pipeline; investors: open) flows into R&D."),
        "sub": "The project's own model. Every box states its status in words.",
        "tag": "ASRP · ECOSYSTEM",
        "boxes": [
            ("Education and audience", ["Telegram bot · Arcanum12th"], [("● LIVE · bot", GREEN), ("◐ PILOT · courses", GOLD)]),
            ("R&D and deep tech", ["studies", "patent applications"], [("◐ IN DEVELOPMENT", GOLD)]),
            ("Science and media", ["papers · open repositories", "ASRP.media"], [("● LIVE", GREEN)]),
            ("Commerce", ["B2B / B2G · products", "licensing"], [("○ PLANNED", AMBER)]),
        ],
        "fund": ("Funding", [("● ACTIVE · patrons", GREEN), ("◐ IN PIPELINE · grants", GOLD), ("○ OPEN · investors", VIOLET)]),
        "edges": ["data and attention", "results", "trust and reach (target)", "revenue (target)", "funding"],
        "legend": ["solid arrow: runs today", "dashed arrow: target, loop not closed yet"],
    },
    "ru": {
        "title": "Как связаны части",
        "desc": ("Схема потоков, в каждом блоке статус написан словами. Образование и аудитория (Telegram-бот: "
                 "работает; курсы Arcanum12th: пилот) передаёт данные и внимание в R&D и deep tech "
                 "(исследования, патентные заявки: в разработке), оттуда результаты идут в Науку и медиа "
                 "(статьи, открытые репозитории, ASRP.media: работает). Пунктирные целевые стрелки: доверие и "
                 "охват от Науки и медиа к Коммерции (B2B / B2G, продукты, лицензирование: планируется) и "
                 "выручка от Коммерции обратно в R&D. Финансирование (меценаты: активно; гранты: в работе; "
                 "инвесторы: открыто) поступает в R&D."),
        "sub": "Модель самого проекта. В каждом блоке статус написан словами.",
        "tag": "ASRP · ЭКОСИСТЕМА",
        "boxes": [
            ("Образование и аудитория", ["Telegram-бот · Arcanum12th"], [("● РАБОТАЕТ · бот", GREEN), ("◐ ПИЛОТ · курсы", GOLD)]),
            ("R&D и deep tech", ["исследования", "патентные заявки"], [("◐ В РАЗРАБОТКЕ", GOLD)]),
            ("Наука и медиа", ["статьи · репозитории", "ASRP.media"], [("● РАБОТАЕТ", GREEN)]),
            ("Коммерция", ["B2B / B2G · продукты", "лицензирование"], [("○ ПЛАНИРУЕТСЯ", AMBER)]),
        ],
        "fund": ("Финансирование", [("● АКТИВНО · меценаты", GREEN), ("◐ В РАБОТЕ · гранты", GOLD), ("○ ОТКРЫТО · инвесторы", VIOLET)]),
        "edges": ["данные и внимание", "результаты", "доверие и охват (цель)", "выручка (цель)", "финансирование"],
        "legend": ["сплошная стрелка: работает сегодня", "пунктирная стрелка: цель, контур ещё не замкнут"],
    },
}


def flow(lang):
    c = FLOW[lang]
    W, H = 1200, 470
    o = [svg_open(W, H, c["title"], c["desc"])]
    o.append("<defs><marker id='as' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='8' markerHeight='8' orient='auto'>"
             "<path d='M0,0 L10,5 L0,10z' fill='%s'/></marker><marker id='ad' viewBox='0 0 10 10' refX='9' refY='5' "
             "markerWidth='8' markerHeight='8' orient='auto'><path d='M0,0 L10,5 L0,10z' fill='%s'/></marker></defs>"
             % (TEAL, AMBER))
    o.append(text(24, 46, c["title"], 26, INK, "start", 700, 0, 700))
    o.append(text(24, 72, c["sub"], FS_KICKER, MUTED, "start", 400, 0, W - 48))
    o.append(text(W - 24, 46, c["tag"], FS_KICKER, TEAL, "end", 700, 2, 280))
    bw, bh, gap, x0, y0 = 244, 136, 44, 46, 128
    xs = [x0 + i * (bw + gap) for i in range(4)]
    strokes = [GREEN, GOLD, GREEN, AMBER]
    for i, (title, body, stat) in enumerate(c["boxes"]):
        x = xs[i]
        o.append("<rect x='%d' y='%d' width='%d' height='%d' rx='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
                 % (x, y0, bw, bh, RADIUS, PANEL, strokes[i]))
        o.append(text(x + 16, y0 + 34, title, 15, INK, "start", 700, 0, bw - 28))
        y = y0 + 60
        for line in body:
            o.append(text(x + 16, y, line, FS_SMALL, MUTED, "start", 400, 0, bw - 28))
            y += 24
        for line, col in stat:
            o.append(text(x + 16, y, line, FS_MIN, col, "start", 800, 0, bw - 28))
            y += 24
    ym = y0 + bh / 2
    for i in range(3):
        xa, xb = xs[i] + bw + 4, xs[i + 1] - 5
        dashed = i == 2
        label = c["edges"][i]
        fit(label, FS_SMALL, 200)
        if dashed:
            o.append("<line x1='%d' y1='%.0f' x2='%d' y2='%.0f' stroke='%s' stroke-width='2.2' stroke-dasharray='7 6' "
                     "marker-end='url(#ad)'><animate attributeName='stroke-dashoffset' from='26' to='0' dur='1.6s' "
                     "repeatCount='indefinite'/></line>" % (xa, ym, xb, ym, AMBER))
        else:
            o.append("<line x1='%d' y1='%.0f' x2='%d' y2='%.0f' stroke='%s' stroke-width='2.2' marker-end='url(#as)'/>"
                     % (xa, ym, xb, ym, TEAL))
        o.append(text("%.0f" % ((xa + xb) / 2), y0 - 14, label, FS_SMALL, AMBER if dashed else INK, "middle", 600))
        o.append("<line x1='%.0f' y1='%d' x2='%.0f' y2='%.0f' stroke='%s' stroke-opacity='0.6'/>"
                 % ((xa + xb) / 2, y0 - 8, (xa + xb) / 2, ym - 6, LINE))
    # funding box under the first column, elbow arrow into R&D
    fx, fy, fh = xs[0], y0 + bh + 44, 122
    title, stat = c["fund"]
    o.append("<rect x='%d' y='%d' width='%d' height='%d' rx='%d' fill='%s' stroke='%s' stroke-width='1.6'/>"
             % (fx, fy, bw, fh, RADIUS, PANEL, VIOLET))
    o.append(text(fx + 16, fy + 32, title, 15, INK, "start", 700, 0, bw - 28))
    y = fy + 58
    for line, col in stat:
        o.append(text(fx + 16, y, line, FS_MIN, col, "start", 800, 0, bw - 28))
        y += 24
    bx_in = xs[1] + 100
    yf = fy + 46
    o.append("<path d='M%d,%d H%d V%d' fill='none' stroke='%s' stroke-width='2.2' marker-end='url(#as)'/>"
             % (fx + bw + 4, yf, bx_in, y0 + bh + 6, TEAL))
    o.append(text(fx + bw + 12, yf - 10, c["edges"][4], FS_SMALL, INK, "start", 600, 0, bx_in - fx - bw - 8))
    # revenue (target): Commerce back to R&D
    rx_out, rx_in, yr = xs[3] + bw / 2, xs[1] + bw - 70, y0 + bh + 78
    o.append("<path d='M%.0f,%d V%d H%d V%d' fill='none' stroke='%s' stroke-width='2.2' stroke-dasharray='7 6' "
             "marker-end='url(#ad)'><animate attributeName='stroke-dashoffset' from='26' to='0' dur='1.6s' "
             "repeatCount='indefinite'/></path>" % (rx_out, y0 + bh + 4, yr, rx_in, y0 + bh + 6, AMBER))
    o.append(text("%.0f" % ((rx_out + rx_in) / 2), yr - 10, c["edges"][3], FS_SMALL, AMBER, "middle", 600, 0, 300))
    # legend, in words
    lx, ly = xs[1] + 40, H - 34
    o.append("<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='2.2' marker-end='url(#as)'/>"
             % (lx, ly - 4, lx + 44, ly - 4, TEAL))
    o.append(text(lx + 54, ly, c["legend"][0], FS_SMALL, MUTED, "start", 400, 0, 300))
    lx2 = lx + 54 + text_width(c["legend"][0], FS_SMALL) + 36
    o.append("<line x1='%.0f' y1='%d' x2='%.0f' y2='%d' stroke='%s' stroke-width='2.2' stroke-dasharray='7 6' "
             "marker-end='url(#ad)'/>" % (lx2, ly - 4, lx2 + 44, ly - 4, AMBER))
    o.append(text("%.0f" % (lx2 + 54), ly, c["legend"][1], FS_SMALL, MUTED, "start", 400, 0, W - lx2 - 80))
    o.append("</svg>\n")
    return "\n".join(o)



# --- icons -----------------------------------------------------------------------------------
def icon(col, body, title):
    return ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 64 64\" width=\"64\" height=\"64\" role=\"img\">\n"
            "<title>%s</title>\n<desc>Navigation icon: %s.</desc>\n<rect x=\"2\" y=\"2\" width=\"60\" height=\"60\" rx=\"12\" fill=\"#101826\" "
            "stroke=\"%s\" stroke-width=\"3\"/>\n<g fill='none' stroke='%s' stroke-width='2.6' stroke-linecap='round' "
            "stroke-linejoin='round'>%s</g>\n</svg>\n" % (title, title, col, col, body))


ICONS = {
    "ecosystem": (TEAL, "<circle cx='32' cy='32' r='6'/><circle cx='32' cy='14' r='4'/><circle cx='48' cy='41' r='4'/>"
                        "<circle cx='16' cy='41' r='4'/><path d='M32 26V18M37 35l8 4M27 35l-8 4'/>", "ecosystem"),
    "research": (GREEN, "<path d='M26 14h12M28 14v14L18 46a3 3 0 0 0 3 4h22a3 3 0 0 0 3-4L36 28V14'/><path d='M23 40h18'/>",
                 "research and patents"),
    "team": (BLUE, "<circle cx='24' cy='25' r='6'/><circle cx='42' cy='27' r='5'/><path d='M12 48c1-8 6-12 12-12s11 4 12 12"
                   "M38 38c7-1 12 3 13 10'/>", "team"),
    "legal": (GOLD, "<path d='M32 14v36M22 50h20M16 22h32M16 22l-6 14h12zM48 22l-6 14h12z'/>", "legal entities"),
    "money": (GOLD, "<circle cx='32' cy='32' r='17'/><path d='M38 25c-2-3-12-3-12 2s12 3 12 9-10 5-13 2M32 19v26'/>",
              "paths to money"),
    "products": (AMBER, "<path d='M32 12l18 9v22l-18 9-18-9V21z'/><path d='M14 21l18 9 18-9M32 30v22'/>", "products"),
    "track": (GREEN, "<circle cx='32' cy='32' r='18'/><path d='M23 33l6 6 12-14'/>", "track record"),
    "outreach": (VIOLET, "<circle cx='32' cy='36' r='4'/><path d='M22 26a14 14 0 0 1 20 0M15 19a24 24 0 0 1 34 0M32 40v10'/>",
                 "outreach"),
    "funding": (GOLD, "<path d='M32 49S13 38 13 25a9 9 0 0 1 19-4 9 9 0 0 1 19 4c0 13-19 24-19 24z'/>", "funding"),
    "media": (VIOLET, "<rect x='12' y='17' width='40' height='28' rx='5'/><path d='M28 25v12l10-6z'/><path d='M24 51h16'/>",
              "media and channels"),
    "markets": (TEAL, "<circle cx='32' cy='32' r='18'/><circle cx='32' cy='32' r='10'/><circle cx='32' cy='32' r='2.5'/>",
                "target markets"),
    "roadmap": (AMBER, "<path d='M18 52V12M18 14h26l-6 8 6 8H18'/>", "roadmap"),
    "terms": (BLUE, "<path d='M20 12h18l8 8v32H20z'/><path d='M38 12v8h8M26 30h14M26 37h14M26 44h9'/>", "contacts and terms"),
    "graph": (TEAL, "<circle cx='18' cy='20' r='5'/><circle cx='46' cy='18' r='5'/><circle cx='22' cy='46' r='5'/>"
                    "<circle cx='46' cy='44' r='5'/><path d='M23 20h18M19 25l2 16M27 46h14M46 23v16M22 24l20 17'/>",
              "interactive graph"),
    "whitepaper": (GREEN, "<path d='M16 14h14a6 6 0 0 1 2 4 6 6 0 0 1 2-4h14v34H34a4 4 0 0 0-2 2 4 4 0 0 0-2-2H16z'/>"
                          "<path d='M32 18v30'/>", "whitepapers"),
    "report": (AMBER, "<rect x='16' y='14' width='32' height='38' rx='4'/><path d='M25 14v-3h14v3M23 28l4 4 7-8M23 42h18M38 28h4'/>",
               "verification report"),
    "archive": (MUTED, "<rect x='12' y='14' width='40' height='11' rx='3'/><path d='M16 25v25h32V25M26 34h12'/>", "archive"),
}


def main():
    for lang in ("en", "ru"):
        write("docs/assets/banner/hero-banner.%s.svg" % lang, banner(lang))
        write("docs/assets/infographics/maturity-map.%s.svg" % lang, maturity(lang))
        write("docs/assets/infographics/ecosystem-flow.%s.svg" % lang, flow(lang))
    for name, (col, body, title) in ICONS.items():
        write("docs/assets/icons/%s.svg" % name, icon(col, body, title))


if __name__ == "__main__":
    main()
