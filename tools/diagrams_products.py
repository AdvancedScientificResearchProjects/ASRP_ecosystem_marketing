"""Product and media diagrams, redrawn from assets/diagrams/08, 09, 10, 11 and 17 (PNG, mixed languages).

Every label is transcribed from the source PNG; nothing is added except the legend entries that
explain dashed arrows. English and Russian versions are separate files.
Run through tools/build_diagrams.py.
"""
from svgkit import (Canvas, wrap, TEAL, VIOLET, GOLD, GREEN, AMBER, BLUE, MUTED, INK, FS_SMALL, FS_KICKER)

OUT = "docs/assets/diagrams/"


def right(b):
    return (b[0] + b[2] + 3, b[1] + b[3] / 2)


def left(b):
    return (b[0] - 4, b[1] + b[3] / 2)


def top(b, dx=0):
    return (b[0] + b[2] / 2 + dx, b[1] - 4)


def bottom(b, dx=0):
    return (b[0] + b[2] / 2 + dx, b[1] + b[3] + 3)


def mh(w, spec):
    """Natural height of a box spec at width w (measured on a scratch canvas)."""
    s = dict(spec)
    s.pop("w", None)
    return Canvas(10, 10, "t", "d").box(0, 0, w, **s)[3]


def pan(cv, x, y, w, title, color, rows, gap=12, pad=12):
    """Titled panel holding rows of boxes. Each box spec is a dict (box kwargs, optional 'w' weight).
    Row height is the tallest box of the row. Returns (panel_rect, [[box_rect, ...], ...])."""
    inner = w - 2 * pad
    tl = wrap(title, FS_KICKER, w - 40, True)
    off = 26 + (len(tl) - 1) * 18 + 14
    plan = []
    for row in rows:
        tot = sum(s.get("w", 1) for s in row)
        avail = inner - gap * (len(row) - 1)
        ws = [avail * s.get("w", 1) / tot for s in row]
        plan.append((ws, max(mh(wi, s) for wi, s in zip(ws, row))))
    h = off + sum(r[1] for r in plan) + gap * (len(rows) - 1) + pad + 2
    cv.panel(x, y, w, h, None, color)
    for i, ln in enumerate(tl):
        cv.label(x + 16, y + 26 + i * 18, ln, FS_KICKER, color, "start", 800, w - 32)
    out, cy = [], y + off
    for row, (ws, rh) in zip(rows, plan):
        cx, rects = x + pad, []
        for wi, s in zip(ws, row):
            s = dict(s)
            s.pop("w", None)
            rects.append(cv.box(round(cx, 1), round(cy, 1), round(wi, 1), h=rh, **s))
            cx += wi + gap
        out.append(rects)
        cy += rh + gap
    return (x, y, w, h), out


# --- 08 cognitive stack -----------------------------------------------------------------------
STACK = {
    "en": {
        "title": "Cognitive Enhancement Stack",
        "tag": "ASRP · PRODUCTS",
        "desc": ("The user feeds four inputs, each leading to the ASRP.drift AI (interpretation + feedback): "
                 "DAAT Crystal (focusing element, worn on chest), Inspira-X (neuro-breath interface), "
                 "Neurointerface (EEG + GSR) and Cognitive commands (mental commands, attention, focus). "
                 "The ASRP.drift AI leads to three outcomes: Working memory up, Mental noise down, "
                 "Attention control up."),
        "user": ("User", []),
        "inp": [("DAAT Crystal", ["focusing element", "(worn on chest)"], VIOLET),
                ("Inspira-X", ["neuro-breath interface"], TEAL),
                ("Neurointerface", ["EEG + GSR"], BLUE),
                ("Cognitive commands", ["mental commands", "attention · focus"], GREEN)],
        "ai": ("ASRP.drift AI", ["interpretation + feedback"]),
        "out": [("Working memory ↑", []), ("Mental noise ↓", []), ("Attention control ↑", [])],
    },
    "ru": {
        "title": "Стек когнитивного усиления",
        "tag": "ASRP · ПРОДУКТЫ",
        "desc": ("Пользователь использует четыре входа, каждый ведёт к ASRP.drift AI (интерпретация и обратная "
                 "связь): DAAT Crystal (фокусирующий элемент, носится на груди), Inspira-X (интерфейс "
                 "управляемого дыхания), Neurointerface (ЭЭГ + КГР) и когнитивные команды (ментальные команды, "
                 "внимание, фокус). ASRP.drift AI ведёт к трём результатам: рабочая память растёт, ментальный "
                 "шум снижается, контроль внимания растёт."),
        "user": ("Пользователь", []),
        "inp": [("DAAT Crystal", ["фокусирующий элемент", "(носится на груди)"], VIOLET),
                ("Inspira-X", ["интерфейс управляемого дыхания"], TEAL),
                ("Neurointerface", ["ЭЭГ + КГР"], BLUE),
                ("Когнитивные команды", ["ментальные команды", "внимание · фокус"], GREEN)],
        "ai": ("ASRP.drift AI", ["интерпретация и обратная связь"]),
        "out": [("Рабочая память ↑", []), ("Ментальный шум ↓", []), ("Контроль внимания ↑", [])],
    },
}


def stack(lang):
    c = STACK[lang]
    W, H = 1200, 560
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], {"en": "Outcomes are targets; full study results are pending", "ru": "Результаты целевые; полные итоги исследования ожидаются"}[lang], c["tag"])
    bh, step, y0 = 96, 116, 96
    ys = [y0 + i * step for i in range(4)]
    mid = ys[0] + (ys[3] + bh - ys[0]) / 2
    user = cv.box(24, mid - 40, 160, c["user"][0], c["user"][1], stroke=INK, h=80, center=True, title_size=16)
    ins = []
    for (t, ln, col), y in zip(c["inp"], ys):
        ins.append(cv.box(250, y, 290, t, ln, stroke=col, h=bh, title_size=16))
    ai = cv.box(640, mid - 55, 250, c["ai"][0], c["ai"][1], stroke=GOLD, h=110, title_size=17, center=True)
    oy = [mid - 130, mid - 40, mid + 50]
    outs = [cv.box(946, y, 230, t, ln, stroke=GREEN, h=80, title_size=15, center=True)
            for (t, ln), y in zip(c["out"], oy)]
    for b in ins:
        cv.arrow([right(user), (217, right(user)[1]), (217, b[1] + b[3] / 2), left(b)])
        cv.arrow([right(b), (590, b[1] + b[3] / 2), (590, ai[1] + ai[3] / 2), left(ai)])
    for b in outs:
        cv.arrow([right(ai), (920, right(ai)[1]), (920, b[1] + b[3] / 2), left(b)])
    cv.save(OUT + "08-cognitive-stack.%s.svg" % lang)


# --- 09 DAAT measurement loop -----------------------------------------------------------------
LOOP = {
    "en": {
        "title": "DAAT Crystal measurement loop",
        "tag": "ASRP · PRODUCTS",
        "desc": ("DAAT Crystal (grown in hyperbolic field) is worn by user. The user is measured by four "
                 "sensors: EEG (gamma / alpha ratio), HRV (heart-brain coherence), GSR (SNS / PNS balance) "
                 "and Inspira-X (respiratory biosensor). All four go into the ASRP.drift AI "
                 "(interpretation), which produces Metrics: plus working memory, minus mental noise, plus "
                 "cognitive load. Metrics lead to Premium B2C + B2B (individuals, executives)."),
        "dc": ("DAAT Crystal", ["grown in hyperbolic field"]),
        "worn": ("Worn by user", []),
        "sens": [("EEG", ["gamma / alpha ratio"], BLUE), ("HRV", ["heart-brain coherence"], BLUE),
                 ("GSR", ["SNS / PNS balance"], BLUE), ("Inspira-X", ["respiratory biosensor"], TEAL)],
        "ai": ("ASRP.drift AI", ["interpretation"]),
        "met": ("Metrics", ["+ working memory", "− mental noise", "+ cognitive load"]),
        "prem": ("Premium B2C + B2B", ["individuals · executives"]),
    },
    "ru": {
        "title": "Измерительная петля DAAT",
        "tag": "ASRP · ПРОДУКТЫ",
        "desc": ("Кристалл DAAT (выращен в гиперболическом поле) носится пользователем. Пользователя измеряют "
                 "четыре датчика: ЭЭГ (гамма / альфа), HRV (когерентность сердце-мозг), КГР (баланс СНС / ПНС) "
                 "и Inspira-X (респираторный биосенсор). Все четыре идут в ASRP.drift AI (интерпретация), "
                 "который выдаёт метрики: плюс рабочая память, минус ментальный шум, плюс когнитивная нагрузка. "
                 "Метрики ведут к премиум B2C + B2B (физлица, топ-менеджмент)."),
        "dc": ("DAAT Crystal", ["выращен в гиперболическом поле"]),
        "worn": ("Носится пользователем", []),
        "sens": [("ЭЭГ", ["гамма / альфа"], BLUE), ("HRV", ["когерентность сердце-мозг"], BLUE),
                 ("КГР", ["баланс СНС / ПНС"], BLUE), ("Inspira-X", ["респираторный биосенсор"], TEAL)],
        "ai": ("ASRP.drift AI", ["интерпретация"]),
        "met": ("Метрики", ["+ рабочая память", "− ментальный шум", "+ когнитивная нагрузка"]),
        "prem": ("Премиум B2C + B2B", ["физлица · топ-менеджмент"]),
    },
}


def loop(lang):
    c = LOOP[lang]
    W, H = 1200, 520
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], {"en": "Metrics are target outcomes; full study results are pending", "ru": "Метрики — целевые результаты; полные итоги исследования ожидаются"}[lang], c["tag"])
    sh, sg, y0 = 90, 14, 96
    ys = [y0 + i * (sh + sg) for i in range(4)]
    mid = y0 + (4 * sh + 3 * sg) / 2
    dc = cv.box(24, mid - 55, 150, c["dc"][0], c["dc"][1], stroke=VIOLET, h=110, center=True, title_size=16)
    worn = cv.box(200, mid - 55, 170, c["worn"][0], c["worn"][1], stroke=INK, h=110, center=True, title_size=16)
    sens = [cv.box(404, y, 215, t, ln, stroke=col, h=sh, title_size=16) for (t, ln, col), y in zip(c["sens"], ys)]
    ai = cv.box(656, mid - 55, 150, c["ai"][0], c["ai"][1], stroke=GOLD, h=110, center=True, title_size=15)
    met = cv.box(840, mid - 85, 140, c["met"][0], c["met"][1], stroke=AMBER, h=170, center=True, title_size=16)
    prem = cv.box(1008, mid - 85, 168, c["prem"][0], c["prem"][1], stroke=GREEN, h=170, center=True, title_size=16)
    cv.arrow([right(dc), left(worn)])
    for b in sens:
        yb = b[1] + b[3] / 2
        cv.arrow([right(worn), (387, right(worn)[1]), (387, yb), left(b)])
        cv.arrow([right(b), (637, yb), (637, mid), left(ai)])
    cv.arrow([right(ai), left(met)])
    cv.arrow([right(met), left(prem)])
    cv.save(OUT + "09-daat-loop.%s.svg" % lang)


# --- 10 Banchenko-Market flow -----------------------------------------------------------------
BANCH = {
    "en": {
        "title": "Banchenko-Market flow",
        "tag": "ASRP · GMS",
        "desc": ("A linear eight-step flow. 1: User in Arcanum12th. 2: Consciousness content (dreams, art, "
                 "forecasts). 3: Objectification (EEG / MEG / fMRI patterns). 4: AI classification (stable "
                 "pattern extraction). 5: Mental Object (new asset class). 6: Tokenization (Kapusta.money "
                 "(QRL), quantum-resistant ledger). 7: ASRP.exchange / ASRP Market (marketplace + /stock DB). "
                 "8: Revenue (TX fees, commissions, premium subs)."),
        "n": [("User in Arcanum12th", [], INK),
              ("Consciousness content", ["dreams · art · forecasts"], VIOLET),
              ("Objectification", ["EEG / MEG / fMRI patterns"], BLUE),
              ("AI classification", ["stable pattern extraction"], TEAL),
              ("Mental Object", ["new asset class"], GOLD),
              ("Tokenization", ["Kapusta.money (QRL)", "quantum-resistant ledger"], VIOLET),
              ("ASRP.exchange / ASRP Market", ["marketplace + /stock DB"], VIOLET),
              ("Revenue", ["TX fees · commissions · premium subs"], GREEN)],
    },
    "ru": {
        "title": "Поток Banchenko-Market",
        "tag": "ASRP · GMS",
        "desc": ("Линейный поток из восьми шагов. 1: пользователь в Arcanum12th. 2: контент сознания (сны, "
                 "искусство, прогнозы). 3: объективизация (нейро-паттерны ЭЭГ / МЭГ / фМРТ). 4: AI-классификация "
                 "(извлечение устойчивого паттерна). 5: Ментальный объект (новый класс активов). 6: токенизация "
                 "(Kapusta.money (QRL), квантово-устойчивый ledger). 7: ASRP.exchange / ASRP Market (биржа + "
                 "база /stock). 8: выручка (комиссии транзакций, комиссии, премиум-подписки)."),
        "n": [("Пользователь в Arcanum12th", [], INK),
              ("Контент сознания", ["сны · искусство · прогнозы"], VIOLET),
              ("Объективизация", ["нейро-паттерны (ЭЭГ / МЭГ / фМРТ)"], BLUE),
              ("AI-классификация", ["извлечение устойчивого паттерна"], TEAL),
              ("Ментальный объект", ["новый класс активов"], GOLD),
              ("Токенизация", ["Kapusta.money (QRL)", "квантово-устойчивый ledger"], VIOLET),
              ("ASRP.exchange / ASRP Market", ["биржа + база /stock"], VIOLET),
              ("Выручка", ["комиссии транзакций · комиссии · премиум-подписки"], GREEN)],
    },
}


def banchenko(lang):
    c = BANCH[lang]
    W, H = 1200, 400
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], None, c["tag"])
    bw, bh, gap = 252, 110, 48
    rows = (100, 270)
    bs = []
    for i, (t, ln, col) in enumerate(c["n"]):
        x, y = 24 + (i % 4) * (bw + gap), rows[i // 4]
        bs.append(cv.box(x, y, bw, t, ln, stroke=col, h=bh, center=True, title_size=16))
    for i in range(7):
        if i == 3:
            a, b = bs[3], bs[4]
            yb = 236
            cv.arrow([bottom(a), (a[0] + a[2] / 2, yb), (b[0] + b[2] / 2, yb), top(b)])
        else:
            cv.arrow([right(bs[i]), left(bs[i + 1])])
    cv.save(OUT + "10-banchenko-market.%s.svg" % lang)


# --- 11 cross-promotion -----------------------------------------------------------------------
PROMO = {
    "en": {
        "title": "Cross-Promotion money path",
        "tag": "ASRP · PRODUCTS",
        "desc": ("Content (article, interview, video, course; ASRP.science, ASRP.media, YouTube, Arcanum12th) "
                 "carries a banner from the Banner layer, which has two kinds. Internal banner: our product "
                 "(direct sale; ASRPshop, Inspira-X, DAAT, courses), leading to Direct purchase and then to "
                 "100% revenue. External affiliate: partner product (% commission; Amazon, protein, "
                 "equipment), leading to Partner purchase and then to a % affiliate fee."),
        "content": ("Content", ["article · interview · video · course",
                                "(ASRP.science · ASRP.media · YouTube · Arcanum12th)"]),
        "layer": "Banner layer (two kinds)",
        "int": ("Internal banner", ["our product (direct sale)", "(ASRPshop · Inspira-X · DAAT · courses)"]),
        "ext": ("External affiliate", ["partner product (% commission)", "(Amazon · protein · equipment)"]),
        "buy": ("Direct purchase", []), "pbuy": ("Partner purchase", []),
        "rev": ("100% revenue", []), "fee": ("% affiliate fee", []),
    },
    "ru": {
        "title": "Кросс-промо: путь денег",
        "tag": "ASRP · ПРОДУКТЫ",
        "desc": ("Контент (статья, интервью, видео, курс; ASRP.science, ASRP.media, YouTube, Arcanum12th) "
                 "несёт баннер из слоя баннеров двух видов. Внутренний баннер: собственный продукт (прямая "
                 "продажа; ASRPshop, Inspira-X, DAAT, курсы) ведёт к прямой покупке, затем к 100% дохода. "
                 "Внешний партнёрский баннер: партнёрский продукт (% комиссии; Amazon, протеин, оборудование) "
                 "ведёт к покупке у партнёра, затем к партнёрскому проценту."),
        "content": ("Контент", ["статья · интервью · видео · курс",
                                "(ASRP.science · ASRP.media · YouTube · Arcanum12th)"]),
        "layer": "Слой баннеров (два вида)",
        "int": ("Внутренний баннер", ["собственный продукт (прямая продажа)",
                                      "(ASRPshop · Inspira-X · DAAT · курсы)"]),
        "ext": ("Внешний партнёрский баннер", ["партнёрский продукт (% комиссии)",
                                               "(Amazon · протеин · оборудование)"]),
        "buy": ("Прямая покупка", []), "pbuy": ("Покупка у партнёра", []),
        "rev": ("100% дохода", ["весь доход наш"]), "fee": ("Партнёрский процент (%)", []),
    },
}


def promo(lang):
    c = PROMO[lang]
    W, H = 1200, 440
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], None, c["tag"])
    cv.panel(350, 96, 340, 320, c["layer"], VIOLET)
    cont = cv.box(24, 190, 290, c["content"][0], c["content"][1], stroke=BLUE, h=140, title_size=16)
    ib = cv.box(366, 150, 308, c["int"][0], c["int"][1], stroke=GREEN, h=110, title_size=16)
    eb = cv.box(366, 290, 308, c["ext"][0], c["ext"][1], stroke=AMBER, h=110, title_size=16)
    yi, ye = ib[1] + ib[3] / 2, eb[1] + eb[3] / 2
    buy = cv.box(740, yi - 40, 200, c["buy"][0], c["buy"][1], stroke=TEAL, h=80, title_size=16, center=True)
    pbuy = cv.box(740, ye - 40, 200, c["pbuy"][0], c["pbuy"][1], stroke=TEAL, h=80, title_size=16, center=True)
    rev = cv.box(980, yi - 40, 196, c["rev"][0], c["rev"][1], stroke=GOLD, h=80, title_size=16, center=True)
    fee = cv.box(980, ye - 40, 196, c["fee"][0], c["fee"][1], stroke=GOLD, h=80, title_size=16, center=True)
    cy = cont[1] + cont[3] / 2
    cv.arrow([right(cont), (332, cy), (332, yi), left(ib)])
    cv.arrow([right(cont), (332, cy), (332, ye), left(eb)])
    cv.arrow([right(ib), left(buy)])
    cv.arrow([right(eb), left(pbuy)])
    cv.arrow([right(buy), left(rev)])
    cv.arrow([right(pbuy), left(fee)])
    cv.save(OUT + "11-cross-promo.%s.svg" % lang)


# --- 17 media strategy ------------------------------------------------------------------------
MEDIA = {
    "en": {
        "title": "ASRP Media Strategy — Unified Content Factory",
        "tag": "ASRP · MEDIA",
        "desc": ("Raw assets (1 research event, 1 shoot, 1 publication: research event, product release, "
                 "milestone / shoot) are ingested by the AI production layer (Vidrush-class): text prompt, "
                 "script, footage, voice + SFX, edit-via-chat timeline. It produces for the Multi-platform "
                 "publisher (DOHOO-class): 1 source asset to about 11 platform-specific units (7 video-class "
                 "plus 4 text-class, automated). Video-class fan-out, 7 units: Pinterest Video, YouTube Shorts, "
                 "Instagram Reels, Threads Video, LinkedIn Video, Facebook Reels, TikTok. Text-class fan-out, "
                 "4 units via Video-to-Text and ChatGPT: Facebook posts and groups, Telegram, Threads text "
                 "posts, WordPress project blogs. Parallel human-curated tracks, not part of the automated "
                 "fan-out, are fed by the raw assets: YouTube and VK Video long-form video; Medium, "
                 "ASRP.science, X (Twitter) and VK long-form text; LinkedIn long-form posts. Fan-out units "
                 "and the parallel tracks feed the Discovery layer: Pinterest automation, Platform discovery, "
                 "Classical SEO, AI-SEO (LLMs). Discovery leads to the Monetisation funnel: asrp.tech and "
                 "project subdomains, ASRPshop (planned B2C storefront), Arcanum12th paid courses and "
                 "certification, ASRP.media affiliate banners, ASRP.exchange / ASRP Market / stock.asrp.*, "
                 "B2B / B2G direct pipelines. LinkedIn long-form posts also go to the funnel as B2B direct."),
        "raw": ("Raw assets (1 research event · 1 shoot · 1 publication)",
                [dict(lines=["Research event", "Product release", "Milestone / shoot"])]),
        "ai": ("AI production layer (Vidrush-class)",
               [dict(lines=["Text prompt → script → footage → voice + SFX → edit-via-chat timeline"])]),
        "pub": ("Multi-platform publisher (DOHOO-class)",
                [dict(lines=["1 source asset → ≈11 platform-specific units (7 video-class + 4 text-class, "
                             "automated)"])]),
        "par": ("Parallel human-curated tracks (not part of automated fan-out)",
                [dict(title="YouTube · VK Video", lines=["long-form video", "(@ASRPtech and per-project)"]),
                 dict(title="Medium · ASRP.science", lines=["X (Twitter) · VK", "long-form text"]),
                 dict(title="LinkedIn long-form posts", lines=["2 companies + project groups",
                                                               "(ASRP.art · ASRP.science · ...)"])]),
        "vid": ("Video-class fan-out — 7 units",
                [[dict(title="Pinterest Video", lines=["@asrp.art · @asrp.fashion"]),
                  dict(title="YouTube Shorts", lines=["@ASRPtech · @ASRPart · @ASRPmedia · @ASRPfashion · "
                                                      "@Arcanum12th"]),
                  dict(title="Instagram Reels", lines=["@asrp.media · per-project"])],
                 [dict(title="Threads Video", lines=["per-project"]),
                  dict(title="LinkedIn Video", lines=["2 company pages + project groups"]),
                  dict(title="Facebook Reels", lines=["per-project pages"])],
                 [dict(title="TikTok", lines=["@asrp.tech · @asrp.media · @asrp.science",
                                              "@asrp.art · @arcanum12th · @ovseannikova"])]]),
        "txt": ("Text-class fan-out — 4 units (via Video-to-Text → ChatGPT)",
                [[dict(title="Facebook", lines=["posts + groups"]),
                  dict(title="Telegram", lines=["@ASRPtech · @electronics_MD · per-project channels"], w=1.4),
                  dict(title="Threads", lines=["text posts"]),
                  dict(title="WordPress", lines=["project blogs"])]]),
        "dis": ("Discovery layer",
                [[dict(title="Pinterest automation", lines=["hourly cron · SEO-keywords → AI image gen → "
                                                            "3 boards parallel", "≈15-day US-traffic ramp-up"]),
                  dict(title="Platform discovery", lines=["TikTok FYP · YouTube recs"])],
                 [dict(title="Classical SEO", lines=["Google · Yandex", "site-map + cross-links"]),
                  dict(title="AI-SEO (LLMs)", lines=["ChatGPT · Perplexity · Gemini · Claude cite ASRP"])]]),
        "fun": ("Monetisation funnel",
                [dict(lines=["asrp.tech + project subdomains", "Arcanum12th paid courses + certification",
                             "ASRP.media affiliate banners (Amazon etc.)",
                             "ASRP.exchange / ASRP Market / stock.asrp.*",
                             "B2B / B2G direct pipelines", "(defense · pharma · corporate-wellness · agri)"],
                      status=[("○ PLANNED: ASRPshop (B2C storefront)", AMBER)], center=True)]),
        "ingest": "ingest", "produce": "produce", "b2b": "B2B direct",
        "leg": ["dashed: feeds the discovery layer", "dashed: manual track, outside the fan-out",
                "solid: pipeline step"],
    },
    "ru": {
        "title": "Медиа-стратегия ASRP — единый контент-завод",
        "tag": "ASRP · МЕДИА",
        "desc": ("Исходные ассеты (1 исследовательское событие, 1 съёмка, 1 публикация: исследовательское "
                 "событие, релиз продукта, веха / съёмка) поступают в слой AI-производства (класс Vidrush): "
                 "текстовый промпт, сценарий, футаж, голос + SFX, таймлайн монтажа через чат. Он передаёт "
                 "результат мультиплатформенному паблишеру (класс DOHOO): 1 исходный ассет превращается в "
                 "≈11 платформенных единиц (7 видеокласса + 4 текстового, автоматически). Видеоединицы, "
                 "7 штук: Pinterest Video, YouTube Shorts, Instagram Reels, Threads Video, LinkedIn Video, "
                 "Facebook Reels, TikTok. Текстовые, 4 штуки через Video-to-Text и ChatGPT: посты и группы "
                 "Facebook, Telegram, текстовые посты Threads, блоги проектов на WordPress. Параллельные "
                 "треки с ручной курацией, не входящие в автоматический веер, получают исходные ассеты: "
                 "длинное видео на YouTube и VK Video; длинные тексты на Medium, ASRP.science, X (Twitter) "
                 "и VK; длинные посты LinkedIn. Единицы веера и параллельные треки питают слой открытия: "
                 "автоматизация Pinterest, открытие на платформах, классическое SEO, AI-SEO (LLM). Открытие "
                 "ведёт в воронку монетизации: asrp.tech и поддомены проектов, ASRPshop (планируемая "
                 "B2C-витрина), платные курсы Arcanum12th и сертификация, партнёрские баннеры ASRP.media, "
                 "ASRP.exchange / ASRP Market / stock.asrp.*, прямые B2B / B2G-каналы. Длинные посты LinkedIn "
                 "идут в воронку и напрямую как B2B direct."),
        "raw": ("Исходные ассеты (1 исследовательское событие · 1 съёмка · 1 публикация)",
                [dict(lines=["Исследовательское событие", "Релиз продукта", "Веха / съёмка"])]),
        "ai": ("Слой AI-производства (класс Vidrush)",
               [dict(lines=["Текстовый промпт → сценарий → футаж → голос + SFX → таймлайн монтажа через чат"])]),
        "pub": ("Мультиплатформенный паблишер (класс DOHOO)",
                [dict(lines=["1 исходный ассет → ≈11 платформенных единиц (7 видеокласса + 4 текстового, "
                             "автоматически)"])]),
        "par": ("Параллельные треки с ручной курацией (не входят в автоматический веер)",
                [dict(title="YouTube · VK Video", lines=["длинное видео", "(@ASRPtech и по проектам)"]),
                 dict(title="Medium · ASRP.science", lines=["X (Twitter) · VK", "длинные тексты"]),
                 dict(title="Длинные посты LinkedIn", lines=["2 компании + группы проектов",
                                                             "(ASRP.art · ASRP.science · ...)"])]),
        "vid": ("Видеоединицы — 7 штук",
                [[dict(title="Pinterest Video", lines=["@asrp.art · @asrp.fashion"]),
                  dict(title="YouTube Shorts", lines=["@ASRPtech · @ASRPart · @ASRPmedia · @ASRPfashion · "
                                                      "@Arcanum12th"]),
                  dict(title="Instagram Reels", lines=["@asrp.media · по проектам"])],
                 [dict(title="Threads Video", lines=["по проектам"]),
                  dict(title="LinkedIn Video", lines=["2 страницы компаний + группы проектов"]),
                  dict(title="Facebook Reels", lines=["страницы по проектам"])],
                 [dict(title="TikTok", lines=["@asrp.tech · @asrp.media · @asrp.science",
                                              "@asrp.art · @arcanum12th · @ovseannikova"])]]),
        "txt": ("Текстовые — 4 штуки (через Video-to-Text → ChatGPT)",
                [[dict(title="Facebook", lines=["посты + группы"]),
                  dict(title="Telegram", lines=["@ASRPtech · @electronics_MD · каналы по проектам"], w=1.4),
                  dict(title="Threads", lines=["текстовые посты"]),
                  dict(title="WordPress", lines=["блоги проектов"])]]),
        "dis": ("Слой открытия",
                [[dict(title="Автоматизация Pinterest", lines=["почасовой cron · SEO-ключевые слова → "
                                                               "генерация AI-изображений → 3 доски параллельно",
                                                               "разгон ≈15 дней до трафика из США"]),
                  dict(title="Открытие на платформах", lines=["TikTok FYP · рекомендации YouTube"])],
                 [dict(title="Классическое SEO", lines=["Google · Yandex", "карта сайта + перекрёстные ссылки"]),
                  dict(title="AI-SEO (LLM)", lines=["ChatGPT · Perplexity · Gemini · Claude цитируют ASRP"])]]),
        "fun": ("Воронка монетизации",
                [dict(lines=["asrp.tech + поддомены проектов", "Платные курсы Arcanum12th + сертификация",
                             "Партнёрские баннеры ASRP.media (Amazon и др.)",
                             "ASRP.exchange / ASRP Market / stock.asrp.*",
                             "Прямые B2B / B2G-каналы", "(оборонка · фарма · корпоративный wellness · агро)"],
                      status=[("○ ПЛАНИРУЕТСЯ: ASRPshop (B2C-витрина)", AMBER)], center=True)]),
        "ingest": "приём", "produce": "производство", "b2b": "B2B direct",
        "leg": ["пунктир: питает слой открытия", "пунктир: ручной трек вне веера", "сплошная: шаг конвейера"],
    },
}


def media(lang):
    c = MEDIA[lang]
    W = 1200
    cv = Canvas(W, 1300, c["title"], c["desc"], c["title"], None, c["tag"])
    LX, LW, RX, RW = 24, 300, 356, 770
    y = 90

    raw, rb = pan(cv, LX, y, LW, c["raw"][0], MUTED, [c["raw"][1]])
    ai_y = raw[1] + raw[3] + 40
    ai, ab = pan(cv, LX, ai_y, LW, c["ai"][0], BLUE, [c["ai"][1]])
    pub_y = ai[1] + ai[3] + 40
    pub, pb = pan(cv, LX, pub_y, LW, c["pub"][0], AMBER, [c["pub"][1]])
    par_y = pub[1] + pub[3] + 40
    par, qb = pan(cv, LX, par_y, LW, c["par"][0], MUTED, [[s] for s in c["par"][1]])
    # raw -> AI, AI -> publisher
    cx = LX + LW / 2
    cv.arrow([(cx, raw[1] + raw[3] + 3), (cx, ai[1] - 4)], label=c["ingest"], label_at=(cx + 12, raw[1] + raw[3] + 25),
             anchor="start", label_color=MUTED, label_box=120)
    cv.arrow([(cx, ai[1] + ai[3] + 3), (cx, pub[1] - 4)], label=c["produce"],
             label_at=(cx + 12, ai[1] + ai[3] + 25), anchor="start", label_color=MUTED, label_box=130)
    # raw -> parallel tracks (manual): left margin lane
    cv.arrow([(LX - 3, raw[1] + 40), (11, raw[1] + 40), (11, par[1] + 60), (LX - 4, par[1] + 60)],
             color=MUTED, dashed=True)

    vid, vb = pan(cv, RX, 90, RW, c["vid"][0], GREEN, c["vid"][1])
    txt, tb = pan(cv, RX, vid[1] + vid[3] + 34, RW, c["txt"][0], AMBER, c["txt"][1])
    dis, db = pan(cv, RX, txt[1] + txt[3] + 34, RW, c["dis"][0], VIOLET, c["dis"][1])
    # publisher -> fan-outs
    py = pub[1] + pub[3] / 2
    bx = LX + LW + 16
    for tgt in (vid, txt):
        ty = tgt[1] + tgt[3] / 2
        cv.arrow([(LX + LW + 3, py), (bx, py), (bx, ty), (RX - 4, ty)])
    # fan-outs -> discovery
    cv.arrow([(txt[0] + txt[2] / 2, txt[1] + txt[3] + 3), (txt[0] + txt[2] / 2, dis[1] - 4)], color=VIOLET, dashed=True)
    ry = RX + RW + 24
    vy = vid[1] + vid[3] / 2
    dy = dis[1] + dis[3] / 2
    cv.arrow([(RX + RW + 3, vy), (ry, vy), (ry, dy), (RX + RW + 4, dy)], color=VIOLET, dashed=True)
    cv.arrow([(LX + LW + 3, dy), (RX - 4, dy)], color=VIOLET, dashed=True)
    # funnel
    fy = max(par[1] + par[3], dis[1] + dis[3]) + 44
    fun, fb = pan(cv, LX, fy, W - 2 * LX, c["fun"][0], AMBER, [c["fun"][1]])
    qx = LX + LW / 2
    cv.arrow([(qx, qb[2][0][1] + qb[2][0][3] + 3), (qx, fun[1] - 4)], color=AMBER, label=c["b2b"],
             label_at=(qx + 12, par[1] + par[3] + 28), anchor="start", label_color=AMBER, label_box=110)
    cv.arrow([(dis[0] + dis[2] / 2, dis[1] + dis[3] + 3), (dis[0] + dis[2] / 2, fun[1] - 4)], color=AMBER)
    ly = fun[1] + fun[3] + 34
    H = int(ly + 20)
    cv.h = H
    cv.o[0] = cv.o[0].replace('viewBox="0 0 1200 1300"', 'viewBox="0 0 1200 %d"' % H).replace(
        'height="1300"', 'height="%d"' % H).replace("height='1300'", "height='%d'" % H)
    cv.legend(24, H - 16, [("dashed", VIOLET, c["leg"][0]), ("dashed", MUTED, c["leg"][1]), ("solid", TEAL, c["leg"][2])])
    cv.save(OUT + "17-media-strategy.%s.svg" % lang)


def build():
    for lang in ("en", "ru"):
        stack(lang)
        loop(lang)
        banchenko(lang)
        promo(lang)
        media(lang)
