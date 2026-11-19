"""Timelines and stacks, redrawn from assets/diagrams/03, 12, 06 and 07 (PNG, mixed languages).

Every label is transcribed from the source PNG; nothing is added. English and Russian versions
are separate files. Run through tools/build_diagrams.py.

03 and 12 share one small timeline engine (broken time axis, lanes, staggered labels). Events whose
source gives only a year are drawn as a bar over that year on the lane, never as a point with an
invented month; events with a month only sit at mid-month.
"""
from svgkit import (Canvas, text, wrap, text_width, TEAL, VIOLET, GOLD, GREEN, AMBER, BLUE, MUTED, INK,
                    LINE, PANEL, BG1, FS_SMALL)

OUT = "docs/assets/diagrams/"
W = 1200

MONTHS_RU = ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь",
             "октябрь", "ноябрь", "декабрь"]
MONTHS_RU_GEN = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября",
                 "октября", "ноября", "декабря"]
MONTHS_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def dt(lang, y, m=None, d=None):
    """Date label: (y), (y, m) or (y, m, d) in the given language."""
    if m is None:
        return "%d" % y
    if lang == "en":
        return ("%d %s %d" % (d, MONTHS_EN[m - 1], y)) if d else "%s %d" % (MONTHS_EN[m - 1], y)
    if d:
        return "%d %s %d" % (d, MONTHS_RU_GEN[m - 1], y)
    return "%s %d" % (MONTHS_RU[m - 1].capitalize(), y)


# --- timeline engine --------------------------------------------------------------------------
PLOT_L, PLOT_R = 212, 1176
SEG_A = (6.0, 15.0)      # month index (months since Jan 2017): 15 Aug 2017 .. 1 Apr 2018
SEG_B = (84.0, 114.0)    # 1 Jan 2024 .. 1 Jul 2026
GAP = 40
SCALE = (PLOT_R - PLOT_L - GAP) / ((SEG_A[1] - SEG_A[0]) + (SEG_B[1] - SEG_B[0]))
XA0 = PLOT_L
XA1 = XA0 + (SEG_A[1] - SEG_A[0]) * SCALE
XB0 = XA1 + GAP
XB1 = PLOT_R


def mi(y, m, d=15):
    return (y - 2017) * 12 + (m - 1) + (d - 1) / 30.0


def xpos(m_index):
    if SEG_A[0] <= m_index <= SEG_A[1]:
        return XA0 + (m_index - SEG_A[0]) * SCALE
    if SEG_B[0] <= m_index <= SEG_B[1]:
        return XB0 + (m_index - SEG_B[0]) * SCALE
    raise SystemExit("date outside the drawn axis segments: %r" % m_index)


def ev_x(ev):
    y, m, d = ev["date"]
    if m is None:
        return None  # year only, drawn as a bar
    return xpos(mi(y, m, d if d else 15))


def lay_label(ev, lw, pad=8):
    """(title lines, body lines) wrapped to the label width."""
    inner = lw - 2 * pad
    t = wrap(ev["title"], FS_SMALL, inner, True)
    b = []
    for ln in ev["lines"]:
        b += wrap(ln, FS_SMALL, inner)
    return t, b


def label_h(ev, lw, pad=8):
    t, b = lay_label(ev, lw, pad)
    return pad + 20 * len(t) + 20 * len(b) + pad - 4


def timeline(cv, y0, lanes, lw, bar_note=None, epochs=None, break_note=None, lane_w=176):
    """Draws epoch strip, lanes and axis starting at y0. Returns the y below the axis."""
    y = y0
    lane_layout = []
    # pre-compute label placements per lane
    for lane in lanes:
        evs = sorted(lane["events"], key=lambda e: (e["date"][0], e["date"][1] or 0, e["date"][2] or 0))
        placed = []  # (row, x0, x1, ev, mx)
        for ev in evs:
            x = ev_x(ev)
            if x is None:
                yy = ev["date"][0]
                xa, xb = xpos(mi(yy, 1, 1)), xpos(min(mi(yy, 12, 31), SEG_B[1]))
                mx = (xa + xb) / 2
                ev["_bar"] = (xa, xb)
            else:
                mx = x
            ok = False
            for row in range(4):
                for side in (1, -1):
                    for off in (0, -45, 45, -90, 90, -lw / 2 + 14, lw / 2 - 14):
                        lx0 = mx - lw / 2 + off
                        lx0 = max(PLOT_L, min(PLOT_R - lw, lx0))
                        if not (lx0 + 6 <= mx <= lx0 + lw - 6):
                            continue
                        clash = False
                        for (r2, a0, a1, e2, m2) in placed:
                            sd2, rw2 = (1, r2) if r2 >= 0 else (-1, -r2 - 1)
                            if sd2 != side:
                                continue
                            if rw2 == row and not (lx0 + lw + 8 <= a0 or lx0 >= a1 + 8):
                                clash = True
                            if rw2 < row and a0 - 4 <= mx <= a1 + 4 and abs(m2 - mx) > 1 and not any(abs(q[4] - mx) <= 1 for q in placed):
                                clash = True
                            if rw2 > row and lx0 - 4 <= m2 <= lx0 + lw + 4 and abs(m2 - mx) > 1:
                                clash = True
                        if not clash:
                            placed.append((row if side == 1 else -row - 1, lx0, lx0 + lw, ev, mx))
                            ok = True
                            break
                    if ok:
                        break
                if ok:
                    break
            if not ok:
                raise SystemExit("cannot place label %r" % ev["title"])
        nb = max([p[0] + 1 for p in placed if p[0] >= 0] + [0])
        na = max([-p[0] for p in placed if p[0] < 0] + [0])
        rh = max(label_h(p[3], lw) for p in placed)
        lane_h = 24 + (na + nb) * (rh + 10) + 14
        lane_layout.append((lane, placed, na, nb, rh, lane_h))

    # epoch strip
    if epochs:
        eh = 74
        for (lab, a, b) in epochs:
            cv.box(round(a, 1), y, round(b - a - 4, 1), lab[0], lab[1:], stroke=MUTED, h=eh, title_size=FS_SMALL,
                   pad=4, center=True)
        y += eh + 14
    body_top = y
    total_h = sum(l[5] for l in lane_layout) + 8 * (len(lanes) - 1)
    # epoch tint bands behind lanes
    if epochs:
        for i, (lab, a, b) in enumerate(epochs):
            if i % 2 == 0:
                cv.add("<rect x='%s' y='%s' width='%s' height='%s' fill='%s' fill-opacity='0.55'/>"
                       % (round(a, 1), body_top, round(b - a, 1), total_h, BG1))
    for lane, placed, na, nb, rh, lane_h in lane_layout:
        col = lane["color"]
        cv.box(24, y, lane_w - 8, (lane["glyph"] + " " + lane["name"]).strip(), lane.get("sub", []), stroke=col,
               h=lane_h, title_size=FS_SMALL, pad=10, valign="middle")
        track = y + 12 + na * (rh + 10) + 8
        cv.add("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='%s' stroke-width='2'/>" % (XA0, track, XA1, track, LINE))
        cv.add("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='%s' stroke-width='2'/>" % (XB0, track, XB1, track, LINE))
        boxes = []
        for (row, a0, a1, ev, mx) in placed:
            ly = (track + 16 + row * (rh + 10)) if row >= 0 else (track - 16 - (-row - 1) * (rh + 10) - rh)
            col_e = ev.get("color", col)
            ly_end = (ly - 2) if row >= 0 else (ly + rh + 2)
            cv.add("<line x1='%.1f' y1='%s' x2='%.1f' y2='%s' stroke='%s' stroke-width='1.6' stroke-dasharray='4 4'/>"
                   % (mx, track, mx, ly_end, col_e))
            if "_bar" in ev:
                xa, xb = ev["_bar"]
                cv.add("<rect x='%.1f' y='%s' width='%.1f' height='8' rx='4' fill='%s' fill-opacity='0.7'/>"
                       % (xa, track - 4, xb - xa, col_e))
            same = [q for q in placed if abs(q[4] - mx) <= 1]
            k = same.index((row, a0, a1, ev, mx))
            gx = mx + (k - (len(same) - 1) / 2.0) * 15
            if "_bar" not in ev:
                cv.add(text("%.1f" % gx, track + 7, ev["glyph"], 20, col_e, "middle", 800))
            boxes.append((a0, ly, ev, col_e))
        for a0, ly, ev, col_e in boxes:
            cv.box(round(a0, 1), ly, lw, ev["title"], ev["lines"], stroke=col_e, h=rh, title_size=FS_SMALL, pad=8,
                   valign="top")
        y += lane_h + 8
    y -= 8
    # axis
    ay = y + 10
    cv.add("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='%s' stroke-width='2'/>" % (XA0, ay, XA1, ay, MUTED))
    cv.add("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='%s' stroke-width='2'/>" % (XB0, ay, XB1, ay, MUTED))
    ticks = [(mi(2018, 1, 1), "2018")] + [(mi(yy, 1, 1), str(yy)) for yy in (2024, 2025, 2026)]
    for yy, mm in ((2017, 10), (2018, 4), (2018, 7)):
        pass
    for m_index in [12 + q * 3 for q in range(0, 1)] + [84 + q * 3 for q in range(0, 10)]:
        if m_index > SEG_B[1] or m_index in (84, 96, 108, 12):
            continue
        cv.add("<line x1='%.1f' y1='%s' x2='%.1f' y2='%s' stroke='%s' stroke-width='1.4'/>"
               % (xpos(m_index), ay, xpos(m_index), ay + 6, MUTED))
    for m_index, lab in ticks:
        x = xpos(m_index)
        cv.add("<line x1='%.1f' y1='%s' x2='%.1f' y2='%s' stroke='%s' stroke-width='2.4'/>" % (x, ay - 3, x, ay + 10, INK))
        cv.add(text("%.1f" % x, ay + 28, lab, 14, INK, "middle", 700))
    gx = (XA1 + XB0) / 2
    cv.add("<path d='M%.1f,%s l-6,12 M%.1f,%s l-6,12' stroke='%s' stroke-width='2' fill='none'/>"
           % (gx + 4, ay - 6, gx + 12, ay - 6, MUTED))
    if break_note:
        for i, ln in enumerate(break_note):
            cv.label(gx, ay + 52 + i * 17, ln, FS_SMALL, MUTED, "middle", box=GAP + 150)
    y = ay + 36 + (len(break_note) * 17 + 16 if break_note else 0) + 12
    if bar_note:
        cv.add("<rect x='%s' y='%s' width='40' height='8' rx='4' fill='%s' fill-opacity='0.7'/>" % (24, y - 8, MUTED))
        cv.label(74, y, bar_note, FS_SMALL, MUTED)
        y += 16
    return y


def words(lang, lanes):
    """Plain-language description of every event, for <desc>."""
    parts = []
    for lane in lanes:
        evs = ["%s, %s" % (e["title"], "; ".join(e["lines"])) for e in lane["events"]]
        parts.append("%s: %s." % (lane["name"], " | ".join(evs)))
    return " ".join(parts)


# --- 03 accreditations timeline ---------------------------------------------------------------
def ev3(lang, date, tr, glyph, en, ru):
    """date = (y, m, d); label = date + wording."""
    return {"date": date, "glyph": glyph, "title": dt(lang, *date), "lines": [en if lang == "en" else ru]}


def acc_lanes(lang):
    e = lambda date, gl, en, ru: ev3(lang, date, None, gl, en, ru)
    L = lang == "en"
    return [
        {"name": "Legal entity" if L else "Юр. лицо", "glyph": "■", "color": BLUE, "events": [
            e((2017, 10, 10), "■", "ASRP LLC filed (FL)", "ASRP LLC зарегистрирована"),
            e((2018, 2, 28), "■", "FL LLC name change", "Смена названия FL"),
            e((2024, 1, 27), "■", "KZ TOO filed (Baikonur)", "ТОО зарегистрирована (Байконур)"),
            e((2025, 6, 10), "■", "FL LLC reinstated", "FL LLC восстановлена"),
            e((2026, 2, 28), "■", "FL LLC 2026 report + address change", "Отчёт FL LLC 2026 + смена адреса"),
        ]},
        {"name": "Patent / Copyright" if L else "Патент", "glyph": "▲", "color": VIOLET, "events": [
            e((2024, None, None), "▲", "US Copyright · BFS", "Авт. право США · BFS"),
            e((2024, 11, 27), "▲", "Kazpatent · GFS", "Патент · GFS"),
            e((2025, 9, 20), "▲", "Kazpatent · Inspira-X", "Патент · Inspira-X"),
            e((2025, 11, 8), "▲", "Kazpatent · Fractal + Biophotonic", "Патенты · Fractal + Биофотон."),
            e((2026, None, None), "▲", "Kazpatent · ASRP.art PCT", "Патент · ASRP.art PCT"),
            e((2026, 3, 24), "▲", "Kazpatent · ASRP.drift", "Патент · ASRP.drift"),
        ]},
        {"name": "Paper / preprint" if L else "Статьи", "glyph": "●", "color": TEAL, "events": [
            e((2024, 1, None), "●", "Preprint · Dream Sync", "Препринт · Мнемоника"),
            e((2024, None, None), "●", "Peer-review · ASRP.drift", "Публикация · ASRP.drift"),
            e((2024, 10, None), "●", "Whitepaper · GMS/GFS", "Whitepaper · GMS/GFS"),
            e((2025, 1, None), "●", "Journal pub. · JIBF", "Журнал · JIBF"),
        ]},
        {"name": "Accreditation" if L else "Аккредитации", "glyph": "◆", "color": GOLD, "events": [
            e((2025, 8, 22), "◆", "Tesla Business Program", "Бизнес-программа Tesla"),
            e((2025, 9, 16), "◆", "DARPA BAA accredited", "Аккредитация DARPA BAA"),
        ]},
        {"name": "Event" if L else "Событие", "glyph": "★", "color": GREEN, "events": [
            e((2025, 9, 11), "★", "Theta Hackathon · Berlin", "Хакатон · Берлин"),
            e((2025, 11, None), "★", "AstanaHub · Industry 4.0 Pitch", "AstanaHub · Pitch GFS"),
        ]},
        {"name": "OSF preregistration" if L else "Предрегистрация", "glyph": "○", "color": AMBER, "events": [
            e((2026, 4, None), "○", "OSF · Yeast preregistration", "OSF · Предрегистрация: дрожжи"),
        ]},
    ]


ACC = {
    "en": {
        "title": "ASRP credentials timeline",
        "sub": "Legal entities, patents, papers, accreditations and events",
        "tag": "ASRP · CREDENTIALS",
        "epochs": [(["2017–2018 · Foundation"], XA0, XA1),
                   (["2024 · Science & KZ entity"], XB0, xpos(mi(2025, 1, 1))),
                   (["2025 · Accreditations"], xpos(mi(2025, 1, 1)), xpos(mi(2026, 1, 1))),
                   (["2026 · Patents & preregistrations"], xpos(mi(2026, 1, 1)), XB1)],
        "break": ["2019–2023", "(no events)"],
        "bar": "bar over a year: only the year is given in the source",
    },
    "ru": {
        "title": "Хронология аккредитаций ASRP",
        "sub": "Юр. лица, патенты, статьи, аккредитации и события",
        "tag": "ASRP · АККРЕДИТАЦИИ",
        "epochs": [(["2017–2018 · Основание"], XA0, XA1),
                   (["2024 · Наука и KZ"], XB0, xpos(mi(2025, 1, 1))),
                   (["2025 · Аккредитации"], xpos(mi(2025, 1, 1)), xpos(mi(2026, 1, 1))),
                   (["2026 · Патенты и предрегистрации"], xpos(mi(2026, 1, 1)), XB1)],
        "break": ["2019–2023", "(событий нет)"],
        "bar": "полоса над годом: в источнике указан только год",
    },
}


def accreditations(lang):
    c = ACC[lang]
    lanes = acc_lanes(lang)
    desc = (c["title"] + ". " + words(lang, lanes))
    probe = Canvas(W, 2000, c["title"], desc, c["title"], c["sub"], c["tag"])
    # epochs: wrap the epoch label into box lines
    ep = []
    for (lab, a, b) in c["epochs"]:
        ep.append((lab, a, b))
    end = timeline(probe, 96, lanes, 190, c["bar"], ep, c["break"])
    H = int(end + 20)
    cv = Canvas(W, H, c["title"], desc, c["title"], c["sub"], c["tag"])
    timeline(cv, 96, acc_lanes(lang), 190, c["bar"], ep, c["break"])
    cv.save(OUT + "03-accreditations-timeline.%s.svg" % lang)


# --- 12 company epochs ------------------------------------------------------------------------
def company_lanes(lang):
    L = lang == "en"
    d = lambda *a: dt(lang, *a)
    kz = [
        {"date": (2024, 1, 27), "glyph": "■", "color": BLUE, "title": "■ " + ("Filed" if L else "Регистрация"),
         "lines": ["%s · %s" % (d(2024, 1, 27), "Baikonur" if L else "Байконур")]},
        {"date": (2024, 11, None), "glyph": "★", "color": VIOLET,
         "title": "★ " + ("Kazpatent filing" if L else "Заявка в Казпатент"),
         "lines": ["GFS · %s" % d(2024, 11)]},
        {"date": (2025, 9, None), "glyph": "★", "color": VIOLET,
         "title": "★ " + ("Kazpatent filing" if L else "Заявка в Казпатент"),
         "lines": ["Inspira-X · %s" % d(2025, 9)]},
        {"date": (2025, 11, None), "glyph": "★", "color": VIOLET,
         "title": "★ " + ("Kazpatent filings" if L else "Заявки в Казпатент"),
         "lines": ["Fractal + Biophotonic · %s" % d(2025, 11)]},
        {"date": (2026, None, None), "glyph": "★", "color": VIOLET,
         "title": "★ " + ("Kazpatent" if L else "Казпатент"),
         "lines": ["ASRP.art PCT 412362 · 2026"]},
        {"date": (2026, 3, None), "glyph": "★", "color": VIOLET,
         "title": "★ " + ("Kazpatent filing" if L else "Заявка в Казпатент"),
         "lines": ["ASRP.drift KZ 413554 · %s" % d(2026, 3)]},
    ]
    fl = [
        {"date": (2017, 10, 10), "glyph": "■", "color": BLUE, "title": "■ " + ("Filed" if L else "Регистрация"),
         "lines": [d(2017, 10, 10)]},
        {"date": (2018, 2, 28), "glyph": "◆", "color": GOLD,
         "title": "◆ " + ("Name change" if L else "Смена названия"), "lines": [d(2018, 2, 28)]},
        {"date": (2025, 6, 10), "glyph": "▲", "color": AMBER,
         "title": "▲ " + ("Reinstatement" if L else "Восстановление"), "lines": [d(2025, 6, 10)]},
        {"date": (2025, 6, 10), "glyph": "●", "color": GREEN,
         "title": "● " + ("Annual report" if L else "Годовой отчёт"),
         "lines": ["2024 · %s %s" % ("filed" if L else "подан", d(2025, 6, 10))]},
        {"date": (2025, 6, 10), "glyph": "●", "color": GREEN,
         "title": "● " + ("Annual report" if L else "Годовой отчёт"),
         "lines": ["2025 · %s %s" % ("filed" if L else "подан", d(2025, 6, 10))]},
        {"date": (2026, 2, 28), "glyph": "●", "color": GREEN,
         "title": "● " + ("Annual report" if L else "Годовой отчёт"),
         "lines": ["2026 · %s %s" % ("filed" if L else "подан", d(2026, 2, 28))]},
        {"date": (2026, 2, 28), "glyph": "◐", "color": TEAL,
         "title": "◐ " + ("Address change" if L else "Смена адреса"),
         "lines": ["%s · St. Petersburg, FL" % d(2026, 2, 28)]},
    ]
    return [
        {"name": 'TOO "PNIR" (%s)' % ("Kazakhstan" if L else "Казахстан"), "glyph": "", "color": VIOLET,
         "sub": ["BIN 240140033296"], "events": kz},
        {"name": "ASRP LLC (Florida)" if L else "ASRP LLC (Флорида)", "glyph": "", "color": BLUE,
         "sub": ["Doc L17000209665"], "events": fl},
    ]


EPOCH12 = {
    "en": {"title": "Legal entities: registration epochs",
           "sub": "Two companies, their filings and registry events by date",
           "tag": "ASRP · LEGAL ENTITIES", "break": ["axis break", "2019–2023"],
           "bar": "bar over a year: only the year is given in the source"},
    "ru": {"title": "Юр. лица: хронология регистраций",
           "sub": "Две компании, их подачи и события реестров по датам",
           "tag": "ASRP · ЮР. ЛИЦА", "break": ["разрыв оси", "2019–2023"],
           "bar": "полоса над годом: в источнике указан только год"},
}


def epochs12(lang):
    c = EPOCH12[lang]
    lanes = company_lanes(lang)
    desc = c["title"] + ". " + words(lang, lanes)
    for lane in lanes:
        lane["name"] = lane["name"]
    probe = Canvas(W, 2000, c["title"], desc, c["title"], c["sub"], c["tag"])
    end = timeline(probe, 96, company_lanes(lang), 178, c["bar"], None, c["break"])
    cv = Canvas(W, int(end + 20), c["title"], desc, c["title"], c["sub"], c["tag"])
    timeline(cv, 96, company_lanes(lang), 178, c["bar"], None, c["break"])
    cv.save(OUT + "12-company-epochs.%s.svg" % lang)


# --- 06 funding stack -------------------------------------------------------------------------
FUND = {
    "en": {
        "title": "Funding stack",
        "sub": "Seven sources feed Operations and R&D, then Products and Patents",
        "tag": "ASRP · FUNDING",
        "src": [("Patrons", ["(~$165k cumulative)", "● ACTIVE"]), ("Investors", ["(non-equity)", "○ OPEN"]),
                ("Crowdfunding", ["(Inspira-X)", "○ PLANNED"]), ("Government", ["○ TARGET"]),
                ("Research grants", ["◐ IN PIPELINE"]), ("B2B licensing", ["◐ IN PIPELINE"]),
                ("Ads & Affiliate", ["● ACTIVE"])],
        "ops": "Operations & R&D", "prod": "Products & Patents",
        "legend": "dashed arrow: from Products & Patents back to Patrons",
        "desc": ("Seven funding sources: Patrons (~$165k cumulative), Investors (non-equity), Crowdfunding "
                 "(Inspira-X), Government, Research grants, B2B licensing, Ads and Affiliate. All seven feed "
                 "Operations and R&D, which feeds Products and Patents. A dashed arrow leads from Products "
                 "and Patents back to Patrons."),
    },
    "ru": {
        "title": "Стек финансирования",
        "sub": "Семь источников ведут в операции и R&D, затем продукты и патенты",
        "tag": "ASRP · ФИНАНСИРОВАНИЕ",
        "src": [("Меценаты", ["(~$165k накоплено)", "● АКТИВНО"]), ("Инвесторы", ["(без долей)", "○ ОТКРЫТО"]),
                ("Краудфандинг", ["(Inspira-X)", "○ ПЛАНИРУЕТСЯ"]), ("Госзаказы", ["○ ЦЕЛЬ"]),
                ("Научные гранты", ["◐ В РАБОТЕ"]), ("Лицензирование", ["◐ В РАБОТЕ"]),
                ("Реклама и партнёрка", ["● АКТИВНО"])],
        "ops": "Операции и R&D", "prod": "Продукты и патенты",
        "legend": "пунктирная стрелка: от продуктов и патентов обратно к меценатам",
        "desc": ("Семь источников финансирования: меценаты (~$165k накопленно), инвесторы (без долей), "
                 "краудфандинг (Inspira-X), госзаказы, научные гранты, лицензирование, реклама и партнёрка. "
                 "Все семь питают операции и R&D, которые питают продукты и патенты. Пунктирная стрелка "
                 "ведёт от продуктов и патентов обратно к меценатам."),
    },
}


def funding(lang):
    c = FUND[lang]
    H = 900
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], c["sub"], c["tag"])
    sx, sw, bh, gap, y0 = 60, 360, 88, 14, 140
    bus = 500
    ys = []
    for i, (name, body) in enumerate(c["src"]):
        y = y0 + i * (bh + gap)
        # the last body line is the status word (from the funding table in docs/FUNDING.md)
        tone = {"●": GREEN, "◐": GOLD, "○": AMBER}[body[-1][0]]
        cv.box(sx, y, sw, name, body[:-1], [(body[-1], tone)], stroke=BLUE, h=bh, title_size=16, center=True)
        ys.append(y + bh / 2)
        cv.arrow([(sx + sw + 3, y + bh / 2), (bus - 3, y + bh / 2)], color=MUTED)
    cv.add("<line x1='%s' y1='%s' x2='%s' y2='%s' stroke='%s' stroke-width='2'/>" % (bus, ys[0], bus, ys[-1], MUTED))
    mid = (ys[0] + ys[-1]) / 2
    ox, ow, oh = 600, 250, 100
    ops = cv.box(ox, mid - oh / 2, ow, c["ops"], [], stroke=GREEN, h=oh, title_size=17, center=True)
    cv.arrow([(bus, mid), (ox - 4, mid)], color=MUTED)
    px, pw = 930, 240
    prod = cv.box(px, mid - oh / 2, pw, c["prod"], [], stroke=AMBER, h=oh, title_size=17, center=True)
    cv.arrow([(ox + ow + 3, mid), (px - 4, mid)], color=MUTED)
    ry = 106
    cv.arrow([(px + pw / 2, mid - oh / 2 - 4), (px + pw / 2, ry), (sx + sw / 2, ry), (sx + sw / 2, y0 - 4)],
             color=GOLD, dashed=True)
    cv.legend(24, H - 24, [("dashed", GOLD, c["legend"])])
    cv.save(OUT + "06-funding-stack.%s.svg" % lang)


# --- 07 frequency ladder ----------------------------------------------------------------------
LAD = {
    "en": {
        "title": "Frequency ladder of content",
        "sub": "From a journal paper down to short-form video, bot and course",
        "tag": "ASRP · CONTENT LADDER",
        "rungs": [("ASRP.science", ["Peer-reviewed paper", "~1K readers"], BLUE),
                  ("ASRP.media", ["Science-popularising article", "~100K readers"], BLUE),
                  ("YouTube @ASRPtech", ["Explainer video", "~1M viewers"], GREEN),
                  ("TikTok / Shorts / Reels", ["30-sec hook", "~10M views"], GREEN),
                  ("Arcanum12th_BOT", ["Funnel entry"], GREEN),
                  ("Arcanum12th.education", ["Course"], AMBER)],
        "aff": ("Affiliate sale", []), "aff_lab": ["Amazon affiliate", "banners"],
        "legend": "dashed arrow: affiliate banners lead to an affiliate sale",
    },
    "ru": {
        "title": "Частотная лестница контента",
        "sub": "От статьи в журнале вниз до короткого видео, бота и курса",
        "tag": "ASRP · ЛЕСТНИЦА КОНТЕНТА",
        "rungs": [("ASRP.science", ["Рецензируемая статья", "1K читателей"], BLUE),
                  ("ASRP.media", ["Научпоп-статья", "100K читателей"], BLUE),
                  ("YouTube @ASRPtech", ["Видео-разбор", "1M зрителей"], GREEN),
                  ("TikTok / Shorts / Reels", ["30-сек хук", "10M просмотров"], GREEN),
                  ("Arcanum12th_BOT", ["Вход в воронку"], GREEN),
                  ("Arcanum12th.education", ["Курс"], AMBER)],
        "aff": ("Партнёрская продажа", []), "aff_lab": ["Партнёрские баннеры", "Amazon"],
        "legend": "пунктир: партнёрские баннеры ведут к партнёрской продаже",
    },
}


def ladder(lang):
    c = LAD[lang]
    r = c["rungs"]
    desc = (c["title"] + ". " + "; ".join("%s: %s" % (n, ", ".join(b)) for n, b, _ in r) + ". "
            + c["aff"][0] + " (" + " ".join(c["aff_lab"]) + ").")
    bw, bh, step, gap, y0 = 420, 92, 120, 30, 110
    H = y0 + len(r) * bh + (len(r) - 1) * gap + 70
    cv = Canvas(W, H, c["title"], desc, c["title"], c["sub"], c["tag"])
    boxes = []
    for i, (name, body, col) in enumerate(r):
        x = 40 + i * step
        y = y0 + i * (bh + gap)
        boxes.append(cv.box(x, y, bw, name, body, stroke=col, h=bh, title_size=16, center=True))
    for i in range(len(r) - 1):
        a, b = boxes[i], boxes[i + 1]
        ax = b[0] + 60
        cv.arrow([(ax, a[1] + a[3] + 3), (ax, b[1] - 4)], color=MUTED)
    m = boxes[1]
    ax_x = m[0] + m[2] + 160
    aff = cv.box(ax_x, m[1], 300, c["aff"][0], c["aff"][1], stroke=AMBER, h=bh, title_size=16, center=True)
    cv.arrow([(m[0] + m[2] + 3, m[1] + m[3] / 2), (ax_x - 4, m[1] + m[3] / 2)], color=GOLD, dashed=True)
    for i, ln in enumerate(c["aff_lab"]):
        cv.label(m[0] + m[2] + 80, m[1] + m[3] / 2 - 26 + i * 17, ln, FS_SMALL, INK, "middle", 600, 190)
    cv.legend(24, H - 22, [("dashed", GOLD, c["legend"])])
    cv.save(OUT + "07-frequency-ladder.%s.svg" % lang)


def build():
    for lang in ("en", "ru"):
        accreditations(lang)
        epochs12(lang)
        funding(lang)
        ladder(lang)
