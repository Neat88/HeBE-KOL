# HeBE KOL Underwriting Desk

A pricing tool for Cambodian beauty KOL buying, built on 105 campaigns HeBE ran across
Dr.Melaxin, Jenny House, Mary&May, MediAnswer and efilow (Oct 2024 – Jun 2026).

Paste a creator's TikTok or Facebook profile link, enter their public numbers, and the tool
returns a forecast reach, a fair fee, a walk-away price, and a book / negotiate / pass verdict
scored against what HeBE has actually paid.

## What the audit found

| Finding | Figure |
|---|---|
| Share of view variance explained by follower count | **12%** (R² = 0.124) |
| Cost efficiency vs. views-per-follower | **Spearman −0.69** |
| Cost efficiency vs. followers | Spearman −0.19 |
| Cost vs. views delivered | Spearman +0.23 |
| Cheapest half of deals: share of budget → share of views | **43% → 91%** |
| Spend on above-median-CPM deals | **$19,150** (1.9M views forgone) |

The market prices on follower count (followers↔cost Spearman +0.40) but follower count barely
moves delivered reach. Views-per-follower does, and it is readable off a public profile before
any money is committed.

**Views-per-follower bands, TikTok:**

| Band | n | Median CPM | Avg fee |
|---|---|---|---|
| < 0.05 | 19 | $48.61 | $453 |
| 0.05 – 0.15 | 26 | $9.28 | $433 |
| 0.15 – 0.40 | 21 | $4.09 | $346 |
| 0.40+ | 16 | **$2.53** | $400 |

Near-identical fees, 19× apart in outcome.

**Facebook runs the other way.** 1M+ pages: $1.31 median CPM, zero blow-ups. Under 100K:
$35.32 median CPM, 68% blow-up rate. Buy small on TikTok, big on Facebook.

## Layout

- `tool/page.html` — the calculator (self-contained; benchmarks embedded)
- `analysis/` — the Python scripts that produced every figure above, in run order:
  `analyze.py` → `corr.py` → `waste.py` → `risk.py` → `weights.py` → `fit.py` → `bench.py` → `blob.py`
- `data/HeBE_KH_KOL_Data.xlsx` — source campaign data
- `data/benchmarks.json` — derived benchmark set consumed by the tool

## Reproducing

```bash
pip install openpyxl
cd analysis && python3 analyze.py && python3 corr.py && python3 waste.py \
  && python3 risk.py && python3 weights.py && python3 fit.py && python3 bench.py && python3 blob.py
```

## Model

`forecast views = median(recent post views) × sponsored reach factor × (1 + cross-post lift)`
`fair fee = forecast views ÷ 1000 × target CPM`

Views-per-follower carries the verdict. Engagement metrics are scored as an authenticity check
against a fitted expectation curve — `log₁₀(comments) = −1.66 + 0.669 × log₁₀(views)` on TikTok —
never as a value driver, because engagement per view runs *against* reach in this dataset
(comment rate correlates +0.45 with a **worse** CPM).

### Limits

- The tool does not scrape profiles; TikTok and Meta both block that from a browser page.
  Numbers are entered by hand from the public profile.
- It forecasts reach, not sales. The source file records no conversion, promo-code or revenue
  data, so cost per view is as far as the evidence goes. Adding a sales column against these
  campaigns is the highest-value extension available.
- The 0.75 sponsored reach factor is a convention, not something this dataset can prove — it
  holds no organic baseline for the same creators. It is exposed as a dial.
- 3 of 105 rows carry no fee; 23 carry no TikTok view count. Those rows sit out of the affected
  benchmarks. One row (V Spring) records 5.7 likes against 36.4K views, almost certainly 5.7K
  mistyped.
