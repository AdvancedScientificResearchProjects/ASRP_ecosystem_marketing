# Funnel 03: Cold Web → Patron / Investor **/** Воронка 03: Холодный трафик → Меценат / Инвестор

> **Target audience / Целевая аудитория:** High-net-worth individuals (HNWIs), impact investors, family offices, deep-tech VCs, science philanthropists (45–70 y.o.)
>
> **Conversion goal / Цель конверсии:** Patron tier ($100–$100K) / non-equity investor inquiry
>
> **Current traction / Текущий результат:** ~$165K cumulative from 22+ named patrons (lead: $100K from Alexander Ovsyannikov)
>
> **Content inventory used / Использовано контента:** README Paths to Money + Track Record + Legal Entities + whitepapers + Ecosystem Graph + Patron page

---

## 🎭 Audience Profile **/** Профиль аудитории

| Attribute **/** Атрибут | Value **/** Значение |
|-------------------------|----------------------|
| **Who / Кто** | Family offices, impact investors, crypto-wealth HNWIs, deep-tech angels, science philanthropists |
| **Pain / Боль** | "Low-yield in traditional assets", "want asymmetric deep-tech exposure", "funding frontier science that VCs ignore", "tax-advantaged philanthropy" |
| **Primary platform / Платформа** | Google/LLM search → asrp.tech, LinkedIn (referral), industry events |
| **Entry point / Точка входа** | Google search ("consciousness economy", "hyperbolic fields", "lucid dream technology") → asrp.tech or LLM citation |
| **Barrier / Барьер** | Trust ("is this real?"), verification ("can I verify the claims?"), clarity of monetization |

---

## 🏗️ Funnel Architecture **/** Архитектура воронки

```
ToF (Awareness)                MoF (Engagement)              BoF (Conversion)
─────────────────             ─────────────────             ─────────────────
Google / LLM search           asrp.tech deep-dive            Patron tier page
  │                              │                              │
  ├─ Ecosystem Graph            ├─ README Paths to Money       ├─ $100 Individual
  ├─ README (GitHub)            ├─ Track Record / Case Studies ├─ $1K Contributor
  ├─ Whitepapers (RG)           ├─ Legal Entities & UBO        ├─ $5-20K Benefactor
  └─ GitHub repos               └─ Whitepapers (full text)     ├─ $50-100K Philanthropist
       │                              │                        └─ Non-equity Investor
       ▼                              ▼
  ┌──────────────┐           ┌──────────────┐
  │ LLM citation │           │ NDA          │
  │ (AI-SEO)     │           │ conversation │
  └──────────────┘           └──────────────┘
```

---

## 🔗 Sequence A: Search-to-Patron (Self-Serve) **/** Поиск → Меценат (самообслуживание)

**Target:** HNWIs who research independently via Google / LLM
**Conversion goal:** Patron tier ($100-$100K)

| # | Content | Platform | Inbound | Outbound Forward | Escape Hatch | Conversion Exit |
|---|---------|----------|---------|-----------------|--------------|-----------------|
| 1 | **Google / LLM search** (query: "consciousness economy", "hyperbolic fields ASRP", "lucid dream technology company") | Google, ChatGPT, Perplexity | Cold search | Ecosystem Graph [node 2], README [node 3] | — | — |
| 2 | **Interactive Ecosystem Graph** (147 entities, 245 connections) | `asrp-graph.surge.sh` | Node 1 | Whitepapers [node 4], Track Record [node 5], README [node 3] | Product pages (DAAT, GFS) | — |
| 3 | **README: Full Ecosystem Documentation** (963 lines) | GitHub | Node 1, Node 2 | Paths to Money [node 6], Legal Entities [node 7] | Whitepapers [node 4] | — |
| 4 | **GMS/GFS architectural whitepaper** (pub-3) + **Banchenko-Market** (pub-7) | ResearchGate | Node 2, Node 3 | Track Record [node 5], Banchenko-Market [node 8] | Per-product whitepapers | — |
| 5 | **Track Record & Case Studies** (8 case studies: DoE, Cortical Labs, Nolan, DAAT pilots, NCI SBIR) | README § | Nodes 2-4 | Patron page [node 9], Investor page [node 10] | Per-project funnels | — |
| 6 | **Paths to Money** (7 monetization routes with diagrams) | README § | Node 3, Node 5 | Patron page [node 9], Investor page [node 10] | Specific product funnels | — |
| 7 | **Legal Entities & Registry Verification** (FL LLC, KZ ТОО, UK reinstatement, UBO triad) | README § | Node 3 | DARPA/Tesla Accreditations [node 11], UBO disclosure | — | **Trust signal** |
| 8 | **Banchenko-Market economic whitepaper** | ResearchGate | Node 4 | ASRP.exchange page, Patron page [node 9] | GFS page | — |
| 9 | **Patron Tiers Page** (7 tiers, live names, photos) | asrp.tech/ru/patrons | Nodes 5-8 | **Patron conversion [CONVERSION]** | Donate page, Investor page [node 10] | **$100-$100K** |
| 10 | **Investor Page** (non-equity models) | asrp.tech/ru/investors | Nodes 5, 6 | **Investor inquiry [CONVERSION]** | Patron page [node 9] | **Contact** |
| 11 | **Accreditations** (DARPA BAA, Tesla Business Program) | README § | Node 7 | Patron page [node 9], Investor page [node 10] | — | **Trust signal** |
| 12 | **Money Flow one-pager** (MONEY_FLOW.md) | GitHub | Node 6, Node 5 | Patron page [node 9], Direct sales proof | — | **Revenue clarity** |

### Dead-End Audit **/** Проверка тупиков

- ✅ Node 1: outbound → [node 2, node 3]
- ✅ Node 2: outbound → [node 4, node 5, node 3], escape → product pages
- ✅ Node 3: outbound → [node 6, node 7], escape → [node 4]
- ✅ Node 4: outbound → [node 5, node 8], escape → per-product papers
- ✅ Node 5: outbound → [node 9, node 10], escape → per-project funnels
- ✅ Node 6: outbound → [node 9, node 10], escape → product funnels
- ⚠️ Node 7: outbound → [node 11, UBO], escape → none — **limited forward edges**. Fix: add link to Paths to Money [node 6] or whitepapers [node 4]
- ✅ Node 8: outbound → [ASRP.exchange, node 9]
- ✅ Node 9: outbound → [patron conversion, donate, node 10]
- ✅ Node 10: outbound → [investor conversion, node 9]
- ✅ Node 11: outbound → [node 9, node 10]
- ✅ Node 12: outbound → [node 9, DAAT pilots]

---

## 🔗 Sequence B: LLM-Driven Discovery (AI-SEO) **/** Открытие через LLM (AI-SEO)

**Target:** Users who discover ASRP through AI assistants (ChatGPT, Perplexity, Gemini, Claude)
**Conversion goal:** asrp.tech visit → README → patron

| # | Content | Platform | Inbound | Outbound Forward | Escape Hatch | Conversion Exit |
|---|---------|----------|---------|-----------------|--------------|-----------------|
| 1 | **LLM cites ASRP research** ("What companies work on lucid dreaming economy?", "hyperbolic fields applications") | ChatGPT, Perplexity, Gemini, Claude | User query | asrp.tech link [node 2], ResearchGate papers [node 3] | — | — |
| 2 | **asrp.tech landing page** | asrp.tech | Node 1 | Ecosystem Graph [Sequence A node 2], README [Seq A node 3] | Product pages | — |
| 3 | **ResearchGate publications** (8 canonical papers) | ResearchGate | Node 1, Google Scholar | README [Seq A node 3], Patron page [Seq A node 9] | — | — |
| 4 | **GitHub README / Ecosystem repo** | GitHub | Node 2, Node 3 | Paths to Money [Seq A node 6], Track Record [Seq A node 5] | Whitepapers | — |

### Dead-End Audit

- ✅ Node 1: outbound → [node 2, node 3]
- ✅ Node 2: outbound → [Seq A node 2, Seq A node 3], escape → product pages
- ✅ Node 3: outbound → [Seq A node 3, Seq A node 9]
- ✅ Node 4: outbound → [Seq A node 6, Seq A node 5], escape → whitepapers

---

## 🔗 Sequence C: Referral → Direct Conversation (Warm) **/** Реферал → Прямой разговор (Тёплый)

**Target:** Warm introductions from existing patrons, team, or network
**Conversion goal:** Non-equity investment or major patron tier

| # | Content | Platform | Inbound | Outbound Forward | Escape Hatch | Conversion Exit |
|---|---------|----------|---------|-----------------|--------------|-----------------|
| 1 | **Warm intro** (from patron, team member, or mutual contact) | Email / LinkedIn / in-person | Referral | Curated README section [node 2], Whitepaper [node 3] | — | — |
| 2 | **Curated README: Paths to Money + Track Record + Legal** | README (selected sections) | Node 1 | NDA conversation [node 4], Investor page [Seq A node 10] | Ecosystem Graph | — |
| 3 | **Key whitepaper** (GMS/GFS or Banchenko-Market, based on interest) | ResearchGate | Node 1 | Node 2, Investor page [Seq A node 10] | — | — |
| 4 | **NDA → detailed discussion** | Private documents | Node 2 | **Investment / Patron conversion [CONVERSION]** | — | **$100K-$1M+** |

### Dead-End Audit

- ✅ Node 1: outbound → [node 2, node 3]
- ✅ Node 2: outbound → [node 4, Seq A node 10], escape → Ecosystem Graph
- ✅ Node 3: outbound → [node 2, Seq A node 10]
- ✅ Node 4: outbound → [conversion]

---

## 📊 Funnel Metrics **/** Метрики воронки

| Stage | Metric **/** Метрика | Current baseline **/** Текущий | Target **/** Цель |
|-------|---------------------|:-----------------------------:|:-----------------:|
| **ToF** | GitHub repo stars | Not disclosed | → 100 |
| **ToF** | LLM citation count | Not tracked | → "Appears in top-3 for 5 key queries" |
| **MoF** | Ecosystem graph visits | Not tracked | → 1K/mo |
| **MoF** | Whitepaper downloads (RG) | 0 tracked publicly | → 500/mo per paper |
| **MoF** | README full reads | Not tracked | → 500/mo |
| **BoF** | Patron conversions / quarter | ~5-6/quarter (estimate) | → 10/quarter |
| **BoF** | Investor inquiries / quarter | Not disclosed | → 3/quarter |
| **Revenue** | Cumulative patron funding | ~$165K | → $500K |

---

## 🧪 Gaps / Пробелы

| # | Gap **/** Пробел | Impact **/** Влияние | Suggested fix **/** Предложение |
|---|------------------|----------------------|--------------------------------|
| 1 | **No private investor deck** | Family offices expect a deck before serious conversation | Create 20-slide deck from README content |
| 2 | **No patron tier comparison table** on one page | Users have to scroll to compare | Add comparison matrix on patron page |
| 3 | **No "Capital at Work" page** | Patrons want to see where money goes | Publish transparent funds-allocation report |
| 4 | **No community/updates for patrons** | Retention risk after first donation | Monthly patron-only AMA with founding team |
| 5 | **No tax-benefit documentation** (for US donors) | US HNWIs need tax deduction path | Clarify 501(c)(3) status or fiscal sponsor |
| 6 | **Node 7 (Legal Entities)** has weak forward edges | Trust signal with no next step | Add direct link to Paths to Money and Investor page |
