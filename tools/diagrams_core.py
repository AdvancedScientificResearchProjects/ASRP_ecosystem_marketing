"""Core ecosystem diagrams, redrawn from assets/diagrams/01, 02 and 18 (PNG, mixed languages).

Every label is transcribed from the source PNG; nothing is added. English and Russian versions
are separate files. Run through tools/build_diagrams.py.
"""
from svgkit import (Canvas, wrap, TEAL, VIOLET, GOLD, GREEN, AMBER, BLUE, MUTED, INK, FS_SMALL)

OUT = "docs/assets/diagrams/"


def right(b):
    return (b[0] + b[2] + 3, b[1] + b[3] / 2)


def left(b):
    return (b[0] - 4, b[1] + b[3] / 2)


def top(b, dx=0):
    return (b[0] + b[2] / 2 + dx, b[1] - 4)


def bottom(b, dx=0):
    return (b[0] + b[2] / 2 + dx, b[1] + b[3] + 3)


# --- 01 taxonomy ------------------------------------------------------------------------------
TAX = {
    "en": {
        "title": "ASRP ecosystem taxonomy",
        "desc": ("Single Sign-On (asrp.tech, arcanum12th) on top, linked to five clusters. Edu and Audience: "
                 "Arcanum12th (school, bot), YouTube @ASRPtech. Content and Media: ASRP.science (journal), "
                 "ASRP.media (news and ads). R&D and Patents: UAP reverse engineering, ASRP.drift (PlayOne), "
                 "ASRP.dance, Hyperbolic Field Studies (plasma, agri, yeast, crystals), Inspira-X, Biophotonic, "
                 "Body Food System. GMS meta-cluster: GFS, Arcanum12th, ASRP.art, ASRP.exchange / ASRP Market "
                 "(/stock planned), Kapusta.money. Commerce and Lifestyle: ASRP.fashion, DAAT Crystal (product), "
                 "ASRPshop planned B2C storefront."),
        "sub": "Main clusters under one account",
        "tag": "ASRP · ECOSYSTEM",
        "sso": ("Single Sign-On", ["one account · asrp.tech · arcanum12th"]),
        "clusters": [
            ("Edu & Audience", GREEN, ["Arcanum12th (school · bot)", "YouTube @ASRPtech"], []),
            ("Content & Media", BLUE, ["ASRP.science (journal)", "ASRP.media (news + ads)"], []),
            ("R&D & Patents", GOLD, ["UAP reverse engineering", "ASRP.drift (PlayOne) · ASRP.dance",
                                     "Hyperbolic Field Studies (plasma, agri, yeast, crystals)",
                                     "Inspira-X · Biophotonic · Body Food System"], []),
            ("GMS meta-cluster", VIOLET, ["GFS · Arcanum12th · ASRP.art", "ASRP.exchange / ASRP Market",
                                          "Kapusta.money"], [("○ PLANNED · /stock", AMBER)]),
            ("Commerce & Lifestyle", AMBER, ["ASRP.fashion · DAAT Crystal (product)"],
             [("○ PLANNED · ASRPshop, B2C storefront", AMBER)]),
        ],
    },
    "ru": {
        "title": "Таксономия экосистемы ASRP",
        "desc": ("Сверху единая авторизация (asrp.tech, arcanum12th), связанная с пятью кластерами. Образование "
                 "и аудитория: Arcanum12th (школа, бот), YouTube @ASRPtech. Контент и медиа: ASRP.science "
                 "(журнал), ASRP.media (СМИ и реклама). R&D и патенты: реверс-инжиниринг UAP, ASRP.drift "
                 "(PlayOne), ASRP.dance, исследования гиперболического поля (плазма, агро, дрожжи, кристаллы), "
                 "Inspira-X, Biophotonic, Body Food System. Мета-кластер GMS: GFS, Arcanum12th, ASRP.art, "
                 "ASRP.exchange / ASRP Market (/stock планируется), Kapusta.money. Коммерция и Lifestyle: "
                 "ASRP.fashion, DAAT Crystal (продукт), ASRPshop — планируемая B2C-витрина."),
        "sub": "Основные кластеры под одним аккаунтом",
        "tag": "ASRP · ЭКОСИСТЕМА",
        "sso": ("Единая авторизация", ["один аккаунт · asrp.tech · arcanum12th"]),
        "clusters": [
            ("Образование и аудитория", GREEN, ["Arcanum12th (школа · бот)", "YouTube @ASRPtech"], []),
            ("Контент и медиа", BLUE, ["ASRP.science (журнал)", "ASRP.media (СМИ + реклама)"], []),
            ("R&D и патенты", GOLD, ["Реверс-инжиниринг UAP", "ASRP.drift (PlayOne) · ASRP.dance",
                                     "Исследования гиперболического поля (плазма, агро, дрожжи, кристаллы)",
                                     "Inspira-X · Biophotonic · Body Food System"], []),
            ("Мета-кластер GMS", VIOLET, ["GFS · Arcanum12th · ASRP.art", "ASRP.exchange / ASRP Market",
                                          "Kapusta.money"], [("○ ПЛАНИРУЕТСЯ · /stock", AMBER)]),
            ("Коммерция и Lifestyle", AMBER, ["ASRP.fashion · DAAT Crystal (продукт)"],
             [("○ ПЛАНИРУЕТСЯ · ASRPshop, B2C-витрина", AMBER)]),
        ],
    },
}


def taxonomy(lang):
    c = TAX[lang]
    W, H = 1200, 496
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], c["sub"], c["tag"])
    sso = cv.box(430, 96, 340, c["sso"][0], c["sso"][1], stroke=TEAL, center=True, title_size=17)
    gap, x0, y0, bh = 14, 24, 232, 236
    bw = (W - 2 * x0 - 4 * gap) / 5
    for i, (name, col, lines, status) in enumerate(c["clusters"]):
        x = x0 + i * (bw + gap)
        b = cv.box(round(x, 1), y0, round(bw, 1), name, lines, status, stroke=col, h=bh, title_size=16, valign="top")
        sx = sso[0] + sso[2] * (i + 1) / 6
        cv.arrow([(sx, sso[1] + sso[3] + 3), (sx, 196), (x + bw / 2, 196), (x + bw / 2, y0 - 4)], color=col)
    cv.save(OUT + "01-taxonomy.%s.svg" % lang)


# --- 02 money flow ----------------------------------------------------------------------------
MONEY = {
    "en": {
        "title": "Money flow: who pays for what",
        "desc": ("Left: clusters that generate value. Right: who pays. R&D and Patents is paid by B2B "
                 "(licensing, R&D contracts) and B2G / Defense (DoD, VA, government forecasts). GMS meta-cluster "
                 "is paid by B2G / Defense and by transaction fees (Kapusta.money). Content and Media is paid by "
                 "Ads and Affiliate (CPM, CPC, Amazon). Edu and Audience and Commerce and Lifestyle are paid by "
                 "B2C (courses, subscriptions, products). One dashed data flow: Arcanum12th_BOT (dream data) "
                 "feeds biosensor data into GMS."),
        "sub": "Clusters on the left, revenue sources on the right",
        "tag": "ASRP · MONEY FLOW",
        "cols": ["WHAT CREATES VALUE", "WHO PAYS"],
        "src": [("Arcanum12th_BOT", ["dream data"]), ("Content & Media", []), ("Edu & Audience", []),
                ("Commerce & Lifestyle", [])],
        "mid": [("R&D & Patents", []), ("GMS", ["meta-cluster"])],
        "pay": [("B2B", ["licensing · R&D contracts"]), ("B2G / Defense", ["DoD · VA · gov forecasts"]),
                ("TX fees", ["transaction fees (Kapusta.money)"]), ("Ads & Affiliate", ["CPM · CPC · Amazon"]),
                ("B2C", ["courses · subs · products"])],
        "feed": "biosensor feed",
        "legend": [("solid", TEAL, "payment flow"), ("dashed", GOLD, "data feed, not a payment")],
    },
    "ru": {
        "title": "Поток денег: кто за что платит",
        "desc": ("Слева кластеры, создающие ценность, справа — кто платит. За R&D и патенты платят B2B "
                 "(лицензии, R&D-контракты) и B2G / оборонка (DoD, VA, госпрогнозы). За мета-кластер GMS платят "
                 "B2G / оборонка и комиссии транзакций (Kapusta.money). За контент и медиа — реклама и "
                 "партнёрка (CPM, CPC, Amazon). За образование и аудиторию и за коммерцию и Lifestyle — B2C "
                 "(курсы, подписки, товары). Один пунктирный поток данных: Arcanum12th_BOT (данные снов) "
                 "передаёт биосенсорные данные в GMS."),
        "sub": "Слева кластеры, справа источники выручки",
        "tag": "ASRP · ПОТОК ДЕНЕГ",
        "cols": ["ЧТО СОЗДАЁТ ЦЕННОСТЬ", "КТО ПЛАТИТ"],
        "src": [("Arcanum12th_BOT", ["данные снов"]), ("Контент и медиа", []), ("Образование и аудитория", []),
                ("Коммерция и Lifestyle", [])],
        "mid": [("R&D и патенты", []), ("GMS", ["мета-кластер"])],
        "pay": [("B2B", ["лицензии · R&D-контракты"]), ("B2G / оборонка", ["DoD · VA · госпрогнозы"]),
                ("Комиссии транзакций", ["Kapusta.money"]), ("Реклама и партнёрка", ["CPM · CPC · Amazon"]),
                ("B2C", ["курсы · подписки · товары"])],
        "feed": "биосенсор",
        "legend": [("solid", TEAL, "поток оплаты"), ("dashed", GOLD, "поток данных, не оплата")],
    },
}


def money(lang):
    c = MONEY[lang]
    W, H = 1200, 600
    cv = Canvas(W, H, c["title"], c["desc"], c["title"], c["sub"], c["tag"])
    cv.label(40, 108, c["cols"][0], FS_SMALL, MUTED, "start", 800)
    cv.label(W - 40, 108, c["cols"][1], FS_SMALL, GOLD, "end", 800)
    bw, bh = 270, 70
    ys_pay = [124, 206, 288, 370, 452]
    pay = [cv.box(W - 40 - 300, ys_pay[i], 300, t, ln, stroke=GOLD, h=bh, title_size=16) for i, (t, ln) in enumerate(c["pay"])]
    rd = cv.box(450, 150, bw, c["mid"][0][0], c["mid"][0][1], stroke=TEAL, h=bh, title_size=16)
    gms = cv.box(450, 262, bw, c["mid"][1][0], c["mid"][1][1], stroke=VIOLET, h=bh, title_size=16)
    bot = cv.box(40, 262, bw, c["src"][0][0], c["src"][0][1], stroke=GREEN, h=bh, title_size=16)
    media = cv.box(40, 370, bw, c["src"][1][0], c["src"][1][1], stroke=BLUE, h=bh, title_size=16)
    edu = cv.box(40, 432 + 14, bw, c["src"][2][0], c["src"][2][1], stroke=GREEN, h=56, title_size=16)
    com = cv.box(40, 512, bw, c["src"][3][0], c["src"][3][1], stroke=AMBER, h=56, title_size=16)
    for a, b in ((rd, pay[0]), (rd, pay[1]), (gms, pay[1]), (gms, pay[2]), (media, pay[3]), (edu, pay[4]), (com, pay[4])):
        cv.arrow([right(a), left(b)], color=TEAL)
    cv.arrow([right(bot), left(gms)], color=GOLD, dashed=True, label=c["feed"], label_color=GOLD)
    cv.legend(450, H - 22, c["legend"])
    cv.save(OUT + "02-money-flow.%s.svg" % lang)


# --- 18 data flow -----------------------------------------------------------------------------
DATA = {
    "en": {
        "title": "ASRP data flow: raw biosignals → analytics → outputs",
        "desc": ("Raw-data sources: Arcanum12th courses (extrasensory perception, expanded cognitive "
                 "perception, TORO, bodybuilding, etc.; students upload on enrolment genetic analysis, EEG, "
                 "electrodermal GSR, parasympathetic / ANS, medical workup) and Arcanum12th_BOT (dream journal, "
                 "biosensor stream, geo-distributed, users worldwide). They send raw biological data and the "
                 "dream and biosensor stream to the analytical layer (AI classification, pattern matching, "
                 "Kapustin Dream Match Search AI Model, Banchenko Algorithm Extended). Downstream outputs: "
                 "scientific publications (ResearchGate and journal articles, 8 canonical works), GFS forecasts "
                 "(geopolitical, markets, geophysical events; sold B2G, B2B, B2C via ASRP Market) and GMS tokens "
                 "(Mental Objects on QRL, stable neural patterns EEG / MEG / fMRI, tokenised consciousness "
                 "states; traded on ASRP.exchange / ASRP Market / stock.asrp.*). Prediction outcomes go to the "
                 "Kapusta rating substrate (motivation, stimulation, filtering), which feeds back: promotes "
                 "contributors, filters low-quality forecasts, motivates biosensors. Documented in the GFS patent."),
        "head": "ASRP data flow", "sub": "Raw biosignals → analytics → outputs",
        "tag": "ASRP · DATA FLOW",
        "p_src": "RAW DATA", "p_out": "OUTPUTS", "p_kap": "KAPUSTA RATINGS",
        "courses": ("Arcanum12th — courses", ["Extrasensory perception · Expanded cognitive perception · TORO · bodybuilding · etc.",
                                              "Students upload on enrolment:",
                                              "Genetic analysis · EEG · Electrodermal (GSR) · Parasympathetic / ANS · Medical workup"]),
        "bot": ("Arcanum12th_BOT", ["Dream journal · Biosensor stream · Geo-distributed", "Users worldwide"]),
        "layer": ("Analytical layer", ["AI classification", "Pattern matching", "Kapustin Dream Match Search AI Model",
                                       "Banchenko Algorithm Extended"]),
        "pubs": ("Scientific publications", ["ResearchGate + journal articles (see Complete publication list — 8 canonical works)"]),
        "gfs": ("GFS forecasts", ["Geopolitical · Markets · Geophysical events", "Sold B2G, B2B, B2C via ASRP Market"]),
        "gms": ("GMS tokens", ["Mental Objects on QRL · Stable neural patterns (EEG / MEG / fMRI) · Tokenised consciousness states",
                               "Traded on ASRP.exchange / ASRP Market / stock.asrp.*"]),
        "kap": ("Rating substrate: motivation + stimulation + filtering", ["Forecast accuracy ↑ → contributor status ↑, more Kapusta credited",
                                                         "Forecast accuracy ↓ → contributor status ↓",
                                                         "Documented in the GFS patent"]),
        "e": ["raw biological data", "dream + biosensor stream", "paper drafts", "forecast candidates",
              "objectified states", "prediction outcomes", "promotes contributors", "filters low-quality forecasts",
              "motivates biosensors"],
        "legend": [("solid", TEAL, "data and results"), ("dashed", VIOLET, "rating feedback loop")],
    },
    "ru": {
        "title": "Поток данных ASRP: сырые биосигналы → аналитика → результаты",
        "desc": ("Источники сырых данных: курсы Arcanum12th (экстрасенсорное восприятие, расширенное "
                 "когнитивное восприятие, ТОРО, бодибилдинг и т. д.; студенты загружают при записи генетику, "
                 "ЭЭГ, КГР, показатели ВНС, анализы) и Arcanum12th_BOT (дневник снов, биосенсорный поток, "
                 "гео-распределённый, пользователи по всему миру). Сырые биоданные и поток снов и биосенсоров "
                 "идут в аналитический слой (AI-классификация, поиск паттернов, Kapustin Dream Match Search AI "
                 "Model, Banchenko Algorithm Extended). Результаты: научные публикации (ResearchGate и "
                 "журнальные статьи, 8 канонических работ), прогнозы GFS (геополитика, рынки, геофизические "
                 "события; продаются B2G, B2B, B2C через ASRP Market) и GMS-токены (ментальные объекты на QRL, "
                 "устойчивые нейропаттерны ЭЭГ / МЭГ / фМРТ, токенизированные состояния сознания; торгуются на "
                 "ASRP.exchange / ASRP Market / stock.asrp.*). Результаты прогнозов поступают в субстрат "
                 "рейтингов Kapusta (мотивация, стимуляция, фильтрация), который даёт обратную связь: "
                 "продвижение контрибьюторов, фильтрация прогнозов, мотивация биодатчиков. Документировано в "
                 "патенте GFS."),
        "head": "Поток данных ASRP", "sub": "Сырые биосигналы → аналитика → результаты",
        "tag": "ASRP · ПОТОК ДАННЫХ",
        "p_src": "СЫРЫЕ ДАННЫЕ", "p_out": "РЕЗУЛЬТАТЫ", "p_kap": "РЕЙТИНГИ KAPUSTA",
        "courses": ("Arcanum12th — курсы", ["Экстрасенсорное восприятие · Расширенное когнитивное восприятие · ТОРО · бодибилдинг · и т. д.",
                                            "Студенты загружают при записи:",
                                            "Генетика · ЭЭГ · КГР · ВНС · Анализы"]),
        "bot": ("Arcanum12th_BOT", ["Дневник снов · Биосенсорный поток · Гео-распределённый", "Пользователи по всему миру"]),
        "layer": ("Аналитический слой", ["AI-классификация", "Поиск паттернов", "Kapustin Dream Match Search AI Model",
                                         "Banchenko Algorithm Extended"]),
        "pubs": ("Научные публикации", ["ResearchGate + журнальные статьи (см. полный список публикаций — 8 канонических работ)"]),
        "gfs": ("Прогнозы GFS", ["Геополитика · Рынки · Геофизические события", "Продаются B2G, B2B, B2C через ASRP Market"]),
        "gms": ("GMS-токены", ["Ментальные объекты на QRL · Устойчивые нейропаттерны (ЭЭГ / МЭГ / фМРТ) · Токенизированные состояния сознания",
                               "Торгуются на ASRP.exchange / ASRP Market / stock.asrp.*"]),
        "kap": ("Субстрат рейтингов: мотивация + стимуляция + фильтрация", ["Точность прогноза ↑ → статус контрибьютора ↑, больше Kapusta",
                                                        "Точность прогноза ↓ → статус контрибьютора ↓",
                                                        "Документировано в патенте GFS"]),
        "e": ["сырые биоданные", "сны + биосенсоры", "черновики статей", "кандидаты в прогнозы",
              "объективизированные состояния", "результаты прогнозов", "продвижение контрибьюторов",
              "фильтрация прогнозов", "мотивация биодатчиков"],
        "legend": [("solid", TEAL, "данные и результаты"), ("dashed", VIOLET, "обратная связь рейтинга")],
    },
}


def gap_label(cv, cx, y_bottom, s, width, color=INK):
    """Wrapped edge label centred on cx whose last line sits just above y_bottom."""
    lines = wrap(s, FS_SMALL, width)
    for i, ln in enumerate(lines):
        cv.label("%.1f" % cx, "%.1f" % (y_bottom - 8 - (len(lines) - 1 - i) * 16), ln, FS_SMALL, color, "middle", 600)


def data_flow(lang):
    c = DATA[lang]
    W, H = 1200, 800
    cv = Canvas(W, H, c["title"], c["desc"], c["head"], c["sub"], c["tag"])
    cv.panel(24, 96, 244, 500, c["p_src"], GREEN)
    cv.panel(722, 96, 232, 560, c["p_out"], GOLD)
    cv.panel(966, 250, 210, 330, c["p_kap"], VIOLET)
    courses = cv.box(30, 136, 232, c["courses"][0], c["courses"][1], stroke=GREEN)
    bot = cv.box(30, courses[1] + courses[3] + 16, 232, c["bot"][0], c["bot"][1], stroke=GREEN)
    layer = cv.box(378, 250, 178, c["layer"][0], c["layer"][1], stroke=TEAL, title_size=16)
    pubs = cv.box(728, 136, 220, c["pubs"][0], c["pubs"][1], stroke=GOLD)
    gfs = cv.box(728, pubs[1] + pubs[3] + 16, 220, c["gfs"][0], c["gfs"][1], stroke=GOLD)
    gms = cv.box(728, gfs[1] + gfs[3] + 16, 220, c["gms"][0], c["gms"][1], stroke=GOLD)
    kap = cv.box(972, 292, 198, c["kap"][0], c["kap"][1], stroke=VIOLET, title_size=13)
    for box, panel_bottom in ((bot, 596), (gms, 656), (kap, 580)):
        if box[1] + box[3] + 8 > panel_bottom:
            raise SystemExit("panel too short for its boxes (%d > %d)" % (box[1] + box[3] + 8, panel_bottom))
    e = c["e"]
    lt, lb = layer[1], layer[1] + layer[3]
    # sources -> analytical layer (labels sit in the gap, above each arrow)
    ya, yb = lt + 34, lb - 34
    cv.arrow([(courses[0] + courses[2] + 3, ya), (layer[0] - 4, ya)])
    gap_label(cv, 323, ya, e[0], 104)
    ybot = bot[1] + bot[3] / 2
    cv.arrow([(bot[0] + bot[2] + 3, ybot), (323, ybot), (323, yb), (layer[0] - 4, yb)])
    gap_label(cv, 323, ybot + 46, e[1], 104)
    # analytical layer -> outputs
    bus = 566
    for box, lab, y1 in ((pubs, e[2], lt + 26), (gfs, e[3], (lt + lb) / 2), (gms, e[4], lb - 26)):
        y2 = box[1] + box[3] / 2
        cv.arrow([(layer[0] + layer[2] + 3, y1), (bus, y1), (bus, y2), (box[0] - 4, y2)])
        gap_label(cv, (bus + box[0]) / 2 - 2, y2, lab, 154)
    # GFS forecasts -> Kapusta ratings
    yk = gfs[1] + gfs[3] / 2
    cv.arrow([(gfs[0] + gfs[2] + 3, yk), (960, yk), (960, kap[1] + 30), (kap[0] - 4, kap[1] + 30)], color=VIOLET, dashed=True)
    cv.label(1071, 240, e[5], FS_SMALL, VIOLET, "middle", 600, 206)
    # feedback lanes from Kapusta back to the left
    kb = kap[1] + kap[3] + 3
    lanes = ((-60, 690, [(8, 690), (8, courses[1] + 40), (courses[0] - 4, courses[1] + 40)], e[6]),
             (0, 716, [(layer[0] + layer[2] / 2, 716), (layer[0] + layer[2] / 2, lb + 3)], e[7]),
             (60, 742, [(bot[0] + 116, 742), (bot[0] + 116, bot[1] + bot[3] + 3)], e[8]))
    for dx, yl, tail, lab in lanes:
        x = kap[0] + kap[2] / 2 + dx
        cv.arrow([(x, kb), (x, yl)] + tail, color=VIOLET, dashed=True)
        cv.label(950, yl - 7, lab, FS_SMALL, VIOLET, "end", 600, 320)
    cv.legend(24, H - 16, c["legend"])
    cv.save(OUT + "18-data-flow.%s.svg" % lang)


def build():
    for lang in ("en", "ru"):
        taxonomy(lang)
        money(lang)
        data_flow(lang)
