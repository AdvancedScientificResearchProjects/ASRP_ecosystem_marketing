"""Step-funnel diagrams, redrawn from assets/diagrams/04, 13, 14, 15 and 16 (PNG, mixed languages).

One grammar for all five: numbered stage cards, arrows between them, the final outcome stage with a
gold outline, long chains wrapped onto a second row. Labels are transcribed from the source PNG;
nothing is added. English and Russian are separate files. Run through tools/build_diagrams.py.
"""
from svgkit import Canvas, text, TEAL, VIOLET, GOLD, AMBER, INK, PANEL, BG0, FS_SMALL, FS_KICKER, RADIUS

OUT = "docs/assets/diagrams/"
W = 1200
M = 24


def right(b):
    return (b[0] + b[2] + 3, b[1] + b[3] / 2)


def left(b):
    return (b[0] - 4, b[1] + b[3] / 2)


def top(b, dx=0):
    return (b[0] + b[2] / 2 + dx, b[1] - 4)


def bottom(b, dx=0):
    return (b[0] + b[2] / 2 + dx, b[1] + b[3] + 3)


def badge(cv, b, n, color):
    """Small numbered disc sitting on the top-left corner of a stage card."""
    cx, cy = b[0] + 22, b[1]
    cv.add("<circle cx='%s' cy='%s' r='13' fill='%s' stroke='%s' stroke-width='1.6'/>" % (cx, cy, BG0, color))
    cv.add(text(cx, cy + 5, n, FS_SMALL, INK, "middle", 800))


def stage(cv, x, y, w, h, n, title, lines=(), status=(), final=False):
    col = GOLD if final else TEAL
    b = cv.box(x, y, w, title, lines, status, stroke=col, h=h, title_size=15, center=True)
    badge(cv, b, n, col)
    return b


def chain(cv, stages, per_row, y0, h, gap, rowgap):
    """Numbered stage cards, `per_row` per row; the last card is the outcome. Returns the boxes."""
    w = (W - 2 * M - (per_row - 1) * gap) / per_row
    boxes = []
    for i, (n, title, lines, status) in enumerate(stages):
        r, c = divmod(i, per_row)
        boxes.append(stage(cv, round(M + c * (w + gap), 1), y0 + r * (h + rowgap), round(w, 1), h, n, title,
                           lines, status, final=(i == len(stages) - 1)))
    for i in range(len(boxes) - 1):
        a, b = boxes[i], boxes[i + 1]
        if (i + 1) % per_row:
            cv.arrow([right(a), left(b)])
        else:
            ym = a[1] + a[3] + rowgap / 2
            cv.arrow([bottom(a), (a[0] + a[2] / 2, ym), (b[0] + b[2] / 2, ym), top(b)])
    return boxes


def dashed_panel(cv, x, y, w, h, label, color):
    cv.add("<rect x='%s' y='%s' width='%s' height='%s' rx='%d' fill='%s' fill-opacity='1' stroke='%s' "
           "stroke-dasharray='7 6'/>" % (x, y, w, h, RADIUS + 2, PANEL, color))
    cv.add(text(x + 16, y + 28, label, FS_KICKER, color, "start", 800, 0.6, w - 32))


LEG_STEP = {"en": ("next step", "final stage (outcome)"), "ru": ("следующий шаг", "финальная стадия (результат)")}


def legend(cv, lang, y, extra=()):
    a, b = LEG_STEP[lang]
    cv.legend(M, y, [("solid", TEAL, a), ("dot", GOLD, b)] + list(extra))


# --- 04 UAP ----------------------------------------------------------------------------------
UAP = {
    "en": {
        "title": "UAP Reverse Engineering → Defense Contracts",
        "tag": "ASRP · FUNNEL",
        "desc": ("Five-step funnel. 1 Open reverse-engineering on GitHub. 2 Scientific publication (ASRP.science). "
                 "3 LinkedIn visibility. 4 Prime-contractor inbound. 5 Sub-contract / R&D grant "
                 "(DoD, VA, DARPA-class), the final stage."),
        "st": [("Open reverse-engineering", ["on GitHub"]), ("Scientific publication", ["(ASRP.science)"]),
               ("LinkedIn visibility", []), ("Prime-contractor inbound", []),
               ("Sub-contract / R&D grant", ["(DoD · VA · DARPA-class)"])],
    },
    "ru": {
        "title": "Реверс UAP → Оборонные подряды",
        "tag": "ASRP · ВОРОНКА",
        "desc": ("Воронка из пяти шагов. 1 Открытый реверс на GitHub. 2 Научная публикация (ASRP.science). "
                 "3 Видимость в LinkedIn. 4 Входящие от крупных подрядчиков. 5 Субконтракт / R&D-грант "
                 "(DoD, VA, уровня DARPA) — финальная стадия."),
        "st": [("Открытый реверс", ["на GitHub"]), ("Научная публикация", ["(ASRP.science)"]),
               ("Видимость в LinkedIn", []), ("Входящие от крупных подрядчиков", []),
               ("Субконтракт / R&D-грант", ["(DoD · VA · уровня DARPA)"])],
    },
}


def uap(lang):
    c = UAP[lang]
    H = 300
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], None, c["tag"])
    chain(cv, [(str(i + 1), t, l, []) for i, (t, l) in enumerate(c["st"])], 5, 120, 112, 40, 0)
    legend(cv, lang, H - 26)
    cv.save(OUT + "04-uap-funnel.%s.svg" % lang)


# --- 13 plasma --------------------------------------------------------------------------------
PLASMA = {
    "en": {
        "title": "Blood Plasma / Hyperbolic Biomed → Medical Centers",
        "tag": "ASRP · FUNNEL",
        "desc": ("Three steps in a row, then three parallel outcomes. 1 Blood plasma study (reproduced by "
                 "V. Ovseannicova). 2 Open repo + analysis (ASRP.science, LinkedIn). 3 LinkedIn content in hype "
                 "peaks. Step 3 leads to three outcomes: 4a Cortical Labs engaged (status: active negotiations), "
                 "4b Stanford-class medical centers (top-tier medical centers, pharma), 4c Biocomputing companies."),
        "st": [("Blood plasma study", ["(reproduced by V. Ovseannicova)"]),
               ("Open repo + analysis", ["(ASRP.science · LinkedIn)"]),
               ("LinkedIn content in hype peaks", [])],
        "out": [("4a", "Cortical Labs engaged", [], [("● active negotiations", GOLD)]),
                ("4b", "Stanford-class medical centers", ["top-tier medical centers · pharma"], []),
                ("4c", "Biocomputing companies", [], [])],
    },
    "ru": {
        "title": "Плазма крови / Hyperbolic Biomed → Медцентры",
        "tag": "ASRP · ВОРОНКА",
        "desc": ("Три шага подряд, затем три параллельных результата. 1 Исследование плазмы крови "
                 "(воспроизведено В. Овсянниковой). 2 Открытый репо + анализ (ASRP.science, LinkedIn). "
                 "3 LinkedIn-контент в пики хайпа. Шаг 3 ведёт к трём результатам: 4a Cortical Labs вышла на "
                 "связь (статус: активные переговоры), 4b Медцентры класса Stanford (медцентры топ-уровня, "
                 "фарма), 4c Биокомпьютерные компании."),
        "st": [("Исследование плазмы крови", ["(воспроизведено В. Овсянниковой)"]),
               ("Открытый репо + анализ", ["(ASRP.science · LinkedIn)"]),
               ("LinkedIn-контент в пики хайпа", [])],
        "out": [("4a", "Cortical Labs вышла на связь", [], [("● активные переговоры", GOLD)]),
                ("4b", "Медцентры класса Stanford", ["Медцентры топ-уровня · фарма"], []),
                ("4c", "Биокомпьютерные компании", [], [])],
    },
}


def plasma(lang):
    c = PLASMA[lang]
    H = 480
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], None, c["tag"])
    w, h, gap = 244, 110, 44
    ymid = 275
    boxes = []
    for i, (t, l) in enumerate(c["st"]):
        boxes.append(stage(cv, M + i * (w + gap), ymid - h / 2, w, h, str(i + 1), t, l))
    for a, b in zip(boxes, boxes[1:]):
        cv.arrow([right(a), left(b)])
    ow, oh, ox = 300, 98, W - M - 300
    last = boxes[-1]
    for k, (n, t, l, s) in enumerate(c["out"]):
        oy = 108 + k * (oh + 20)
        o = stage(cv, ox, oy, ow, oh, n, t, l, s, final=True)
        cy = oy + oh / 2
        sx = last[0] + last[2] + 3
        bus = (sx + ox) / 2
        cv.arrow([(sx, ymid), (bus, ymid), (bus, cy), (ox - 4, cy)] if abs(cy - ymid) > 1 else [(sx, ymid), (ox - 4, ymid)])
    legend(cv, lang, H - 26)
    cv.save(OUT + "13-plasma-funnel.%s.svg" % lang)


# --- 14 agri ----------------------------------------------------------------------------------
AGRI = {
    "en": {
        "title": "Agricultural Study → Agri Grants & Food Security",
        "head": "Agricultural Study", "sub": "→ Agri Grants & Food Security",
        "tag": "ASRP · FUNNEL",
        "desc": ("Six-step funnel in two rows. 1 Field trials (double-blind activation). 2 Day-4+ volume delta "
                 "vs control. 3 Grant proposals (UA / MD post-conflict soil restoration). 4 Pilot with "
                 "agri-holding. 5 Agri-holdings & food-security funds. 6 Royalty model, the final stage."),
        "st": [("Field trials", ["(double-blind activation)"]), ("Day-4+ volume delta", ["vs control"]),
               ("Grant proposals", ["(UA / MD post-conflict soil restoration)"]),
               ("Pilot with agri-holding", []), ("Agri-holdings & food-security funds", []),
               ("Royalty model", [])],
    },
    "ru": {
        "title": "Агро-исследование → Гранты и продовольственная безопасность",
        "head": "Агро-исследование", "sub": "→ Гранты и продовольственная безопасность",
        "tag": "ASRP · ВОРОНКА",
        "desc": ("Воронка из шести шагов в два ряда. 1 Полевые испытания (двойная слепая активация). 2 Дельта "
                 "объёма 4-й день+ к контролю. 3 Грантовые заявки (UA / MD, восстановление почв после "
                 "конфликта). 4 Пилот с агрохолдингом. 5 Агрохолдинги и фонды продовольственной безопасности. "
                 "6 Роялти-модель — финальная стадия."),
        "st": [("Полевые испытания", ["(двойная слепая активация)"]), ("Дельта объёма 4-й день+", ["к контролю"]),
               ("Грантовые заявки", ["(UA / MD: восстановление почв после конфликта)"]),
               ("Пилот с агрохолдингом", []), ("Агрохолдинги · фонды продовольственной безопасности", []),
               ("Роялти-модель", [])],
    },
}


def agri(lang):
    c = AGRI[lang]
    H = 450
    cv = Canvas(W, H, c["title"], c["desc"], c["head"], c["sub"], c["tag"])
    chain(cv, [(str(i + 1), t, l, []) for i, (t, l) in enumerate(c["st"])], 3, 112, 98, 60, 62)
    legend(cv, lang, H - 26)
    cv.save(OUT + "14-agri-funnel.%s.svg" % lang)


# --- 15 GFS with funding ----------------------------------------------------------------------
GFS = {
    "en": {
        "title": "GFS — forecasts + funding inflows",
        "tag": "ASRP · FUNNEL",
        "desc": ("Main chain: Arcanum12th_BOT (dream ingest) feeds the geo-tagged biosensor dataset, which feeds "
                 "the GFS model. The GFS model produces forecasts, which go to two buyer groups: government "
                 "buyers and private buyers. Funding inflows, shown as a separate dashed group, flow into the "
                 "GFS model: patrons (asrp.tech/ru/patrons, about $165k cumulative), investors, non-equity "
                 "(asrp.tech/ru/investors), grants and foundations (research grants), occasional donations "
                 "(asrp.tech/ru/donate/asrp)."),
        "bot": ("Arcanum12th_BOT", ["dream ingest"]), "ds": ("Geo-tagged biosensor dataset", []),
        "model": ("GFS model", []), "fc": ("Forecasts", []),
        "buy": [("Government buyers", []), ("Private buyers", [])],
        "panel": "FUNDING INFLOWS",
        "fund": [("Patrons", ["asrp.tech/ru/patrons", "(~$165k cumulative)"]),
                 ("Investors (non-equity)", ["asrp.tech/ru/investors"]),
                 ("Grants & foundations", ["research grants"]),
                 ("Occasional donations", ["asrp.tech/ru/donate/asrp"])],
        "leg": "funding inflow into the model",
    },
    "ru": {
        "title": "GFS — прогнозы и приток финансирования",
        "tag": "ASRP · ВОРОНКА",
        "desc": ("Основная цепочка: Arcanum12th_BOT (ингест снов) поставляет геодатасет биодатчиков, который "
                 "питает модель GFS. Модель GFS выдаёт прогнозы, которые идут двум группам покупателей: "
                 "госзаказчикам и частным покупателям. Приток финансирования — отдельная пунктирная группа — "
                 "поступает в модель GFS: меценаты (asrp.tech/ru/patrons, накоплено около $165k), инвесторы без "
                 "долей (asrp.tech/ru/investors), гранты и фонды (научные гранты), разовые донаты "
                 "(asrp.tech/ru/donate/asrp)."),
        "bot": ("Arcanum12th_BOT", ["ингест снов"]), "ds": ("Геодатасет биодатчиков", []),
        "model": ("Модель GFS", []), "fc": ("Прогнозы", []),
        "buy": [("Госзаказчики", []), ("Частные покупатели", [])],
        "panel": "ПРИТОК ФИНАНСИРОВАНИЯ",
        "fund": [("Меценаты", ["asrp.tech/ru/patrons", "(накоплено ~$165k)"]),
                 ("Инвесторы (без долей)", ["asrp.tech/ru/investors"]),
                 ("Гранты и фонды", ["научные гранты"]),
                 ("Разовые донаты", ["asrp.tech/ru/donate/asrp"])],
        "leg": "приток финансирования в модель",
    },
}


def gfs(lang):
    c = GFS[lang]
    H, cardh, fh = 700, 72, 88
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], None, c["tag"])
    # main chain
    bot = stage(cv, M, 100, 260, cardh, "1", c["bot"][0], c["bot"][1])
    ds = stage(cv, 520, 100, 300, cardh, "2", c["ds"][0], c["ds"][1])
    cv.arrow([right(bot), left(ds)])
    # funding group (dashed panel), 4 cards with straight arrows into the tall model card
    py, ph = 204, 452
    dashed_panel(cv, M, py, 424, ph, c["panel"], AMBER)
    fy = []
    for i, (t, l) in enumerate(c["fund"]):
        y = py + 48 + i * (fh + 12)
        b = cv.box(M + 16, y, 392, t, l, (), stroke=AMBER, h=fh, title_size=15, center=True)
        fy.append(b)
    my, mh = fy[0][1], fy[-1][1] + fy[-1][3] - fy[0][1]
    model = stage(cv, 520, my, 200, mh, "3", c["model"][0], c["model"][1])
    cv.arrow([(670, ds[1] + ds[3] + 3), (670, my - 4)])
    for b in fy:
        cv.arrow([right(b), (model[0] - 4, b[1] + b[3] / 2)], color=AMBER, dashed=True)
    fc = stage(cv, 770, my + mh / 2 - cardh / 2, 150, cardh, "4", c["fc"][0], c["fc"][1])
    cv.arrow([right(model), left(fc)])
    bw, bx = 200, W - M - 200
    cy = my + mh / 2
    for k, (t, l) in enumerate(c["buy"]):
        by = cy - 14 - cardh + k * (cardh + 28)
        b = stage(cv, bx, by, bw, cardh, "5a" if k == 0 else "5b", t, l, final=True)
        bus = (fc[0] + fc[2] + bx) / 2
        cv.arrow([right(fc), (bus, cy), (bus, by + cardh / 2), (bx - 4, by + cardh / 2)])
    legend(cv, lang, H - 22, [("dashed", AMBER, c["leg"])])
    cv.save(OUT + "15-gfs-with-funding.%s.svg" % lang)


# --- 16 engagement ----------------------------------------------------------------------------
ENG = {
    "en": {
        "title": "ASRP engagement strategy — open research → LinkedIn → negotiation",
        "head": "ASRP engagement strategy", "sub": "Open research → LinkedIn → negotiation",
        "tag": "ASRP · FUNNEL",
        "desc": ("Eight-step funnel in two rows. 1 Reverse engineering (internal competence). 2 Open scientific "
                 "repo (GitHub + ResearchGate). 3 Peer-preprint publication (preprint / journal). 4 LinkedIn "
                 "content wave (aligned with target hype). 5 Comment / direct outreach (on target's post). "
                 "6 Feedback / inbound (visible signal). 7 Bilateral messaging. 8 Negotiation / contract, the "
                 "final stage. Two logged cases sit at their current stage, shown as dashed links. Case NSWC IHD "
                 "(Cardillo), April 2026, LinkedIn comment, feedback pending, at step 6. Case Cortical Labs, "
                 "2025-2026, Blood Plasma study, active negotiations, at step 7."),
        "st": [("Reverse engineering", ["(internal competence)"]), ("Open scientific repo", ["(GitHub + ResearchGate)"]),
               ("Peer-preprint publication", ["(preprint / journal)"]),
               ("LinkedIn content wave", ["(aligned with target hype)"]),
               ("Comment / direct outreach", ["(on target's post)"]), ("Feedback / inbound", ["(visible signal)"]),
               ("Bilateral messaging", []), ("Negotiation / contract", [])],
        "cur": "current stage",
        "case6": ("CASE · NSWC IHD (Cardillo)", ["Apr 2026 · LinkedIn comment"], [("○ feedback pending", AMBER)]),
        "case7": ("CASE · Cortical Labs", ["2025–2026 · Blood Plasma study"], [("● active negotiations", GOLD)]),
        "leg": "logged case at its current stage",
    },
    "ru": {
        "title": "Стратегия аутрича ASRP — открытое исследование → LinkedIn → переговоры",
        "head": "Стратегия аутрича ASRP", "sub": "Открытое исследование → LinkedIn → переговоры",
        "tag": "ASRP · ВОРОНКА",
        "desc": ("Воронка из восьми шагов в два ряда. 1 Реверс-инжиниринг (внутренняя компетенция). 2 Открытый "
                 "научный репозиторий (GitHub + ResearchGate). 3 Научная публикация (препринт / журнал). "
                 "4 Волна контента в LinkedIn (в момент хайпа цели). 5 Комментарий / прямой аутрич (под постом "
                 "цели). 6 Отклик / входящее (видимый сигнал). 7 Двусторонняя переписка. 8 Переговоры / "
                 "контракт — финальная стадия. Два зафиксированных кейса показаны на текущей стадии "
                 "пунктирными связями. Кейс NSWC IHD (Cardillo), апрель 2026, комментарий в LinkedIn, отклик "
                 "ожидается, на шаге 6. Кейс Cortical Labs, 2025–2026, исследование плазмы крови, активные "
                 "переговоры, на шаге 7."),
        "st": [("Реверс-инжиниринг", ["(внутренняя компетенция)"]),
               ("Открытый научный репозиторий", ["(GitHub + ResearchGate)"]),
               ("Научная публикация", ["(препринт / журнал)"]),
               ("Волна контента в LinkedIn", ["(в момент хайпа цели)"]),
               ("Комментарий / прямой аутрич", ["(под постом цели)"]), ("Отклик / входящее", ["(видимый сигнал)"]),
               ("Двусторонняя переписка", []), ("Переговоры / контракт", [])],
        "cur": "текущая стадия",
        "case6": ("КЕЙС · NSWC IHD (Cardillo)", ["Апр 2026 · комментарий в LinkedIn"], [("○ отклик ожидается", AMBER)]),
        "case7": ("КЕЙС · Cortical Labs", ["2025–2026 · исследование плазмы крови"], [("● активные переговоры", GOLD)]),
        "leg": "зафиксированный кейс на текущей стадии",
    },
}


def engagement(lang):
    c = ENG[lang]
    H = 610
    cv = Canvas(W, H, c["title"], c["desc"], c["head"], c["sub"], c["tag"])
    boxes = chain(cv, [(str(i + 1), t, l, []) for i, (t, l) in enumerate(c["st"])], 4, 112, 100, 42, 54)
    ch = 112
    for idx, key in ((5, "case6"), (6, "case7")):
        s = boxes[idx]
        t, l, st = c[key]
        cb = cv.box(s[0], s[1] + s[3] + 62, s[2], t, l, st, stroke=VIOLET, h=ch, title_size=15, center=True)
        x = s[0] + s[2] / 2
        cv.arrow([(x, s[1] + s[3] + 3), (x, cb[1] - 4)], color=VIOLET, dashed=True)
        cv.label(x + 12, s[1] + s[3] + 36, c["cur"], FS_SMALL, INK, "start", 600, 200)
    legend(cv, lang, H - 24, [("dashed", VIOLET, c["leg"])])
    cv.save(OUT + "16-engagement-funnel.%s.svg" % lang)


def build():
    for lang in ("en", "ru"):
        uap(lang)
        plasma(lang)
        agri(lang)
        gfs(lang)
        engagement(lang)
