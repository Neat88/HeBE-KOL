# HeBE KOL Underwriting Desk

A pricing tool for Cambodian beauty KOL buying, built on 107 campaigns HeBE ran across
Dr.Melaxin, Jenny House, Mary&May, MediAnswer and efilow (Oct 2024 – Jun 2026).

**Live tool:** https://claude.ai/code/artifact/5bd7e28e-438a-40b9-89fe-294f2288786a

Drop screenshots of a creator's profile, and Claude reads the numbers off them and writes a read on
the account. The desk returns a forecast reach, a fair fee, a walk-away price, and a
book / negotiate / pass verdict scored against what HeBE has actually paid — and, if that creator is
already in the log, their own delivery record.

## Getting the numbers in

No website can turn a bare TikTok or Facebook link into numbers: both platforms block cross-origin
reads, which is exactly why the paid platforms buy API access instead. So the profile comes in as
whatever is already on screen. Four routes:

1. **Screenshots, read by AI.** Drop images of the profile header and post grid. They go to Claude
   through the artifact `sample` capability, which extracts followers, following, per-post views and
   — where an opened post is included — likes, comments and shares. Claude also returns a short
   qualitative read: what the account is about, what language the captions are in, how heavily
   sponsored the feed already looks, and up to five specific buying flags. This is the fastest route
   and the only one that reads *content* rather than just counts.
2. **Copy the page.** Ctrl+A / Ctrl+C on the profile, paste the whole blob. A local parser pulls out
   followers, following and post views; when it comes up short the page asks Claude to parse the text.
3. **One-click button (bookmarklet).** Drag "Grab KOL stats" to the bookmarks bar, open the creator's
   profile, click it. It reads the visible counts in the user's own browser and copies a compact
   `HEBE1|…` line to paste into the Paste tab. Nothing is sent anywhere.
4. **By hand.** Type into the fields, as before.

Every AI affordance hides or disables itself when sampling is unavailable — opened outside a Claude
viewer, or when the viewer declines — and the manual routes still work.

## Have we booked them before?

The strongest evidence about a creator is what they did for HeBE last time. Type a name (the field
autocompletes from the 88 creators in the log, and the profile handle is tried as a fallback) and the
desk opens their record: every campaign, the fee, the views delivered, the CPM, and how each one
graded against the book. It states how the current ask compares with what they last accepted, feeds
that history into the written assessment, and hands it to Claude for the second opinion. Creators with
no record are said to have none, rather than passing silently.

Blended CPM is computed only across campaigns carrying both a fee and a view count — 3 of 107 rows
have no fee and 17 no TikTok view count, and mixing those into the divisor would inflate the figure.

TikTok's grid shows views but not per-post likes, comments or shares, so an auto-filled creator starts
with engagement unmeasured. Gates G6 and G8 report **not measured** rather than failing, and the
audience-response pillar scores neutral (50) instead of zero — a views-only import is never punished
for data it could not see. Add engagement by opening a few posts if the campaign needs it.

## Tabs

| Tab | Job |
|---|---|
| **Evaluate a KOL** | The calculator. Pick a campaign objective, enter the profile numbers, get a graded verdict. |
| **Past KOL data** | All 107 campaigns by brand — summary cards plus a sortable, searchable, filterable log. |
| **How it's calculated** | The six-step chain from profile to fee, with formulas and a worked example. |
| **Metric guide** | The metrics professional teams underwrite on, tiered, with your own benchmarks and red flags. |
| **Benchmarks** | Percentile distributions, follower-tier tables, and the evidence charts. |
| **How the big platforms do it** | What HypeAuditor, Modash, Upfluence, CreatorIQ and Traackr measure, feature-by-feature against this desk, and two published benchmarks your own data contradicts. |

## Scoring

Five pillars, each a percentile against the campaigns in the file, weighted by campaign objective:

| Pillar | Awareness | Engagement | Conversion |
|---|---|---|---|
| Cost efficiency (CPM) | **35** | 20 | 20 |
| Reach power (VFR) | **30** | 20 | 15 |
| Audience response (ER-V, shares) | 5 | **30** | 25 |
| Reliability (min ÷ median post) | 15 | 10 | 10 |
| Trust & fit (bot check + checklist) | 15 | 20 | **30** |

A creator scoring under 35 is a pass at any price — cheap access to a weak audience is not a bargain.

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

## Gate check — 14 tests

Alongside the pillar scoring, every creator is run through 14 pass/caution/fail gates adapted from a
KOL vetting report supplied by the team, with thresholds recalibrated to HeBE's own campaigns.

| Code | Test | Measure | Catches |
|---|---|---|---|
| G0 | Data sufficiency | posts entered | accounts too thin to judge |
| G1 | Spike ratio | mean ÷ median views | reach carried by one or two viral hits |
| G2 | Floor ratio | p25 ÷ median views | only the wins show |
| G3 | Peak ratio | max ÷ median views | one mega-hit distorting the average |
| G4 | Top-3 share | top 3 ÷ all views | reach concentrated in three posts |
| G5 | View rate **KEY** | median views ÷ followers | vanity follower counts |
| G6 | Engagement rate **KEY** | (likes + comments) ÷ views | watched but ignored |
| G7 | View floor | median views vs tier floor | many followers, dead views |
| G8 | Share rate | shares ÷ views | no organic spread |
| G9 | Cost efficiency | CPM vs tier bar | price above what reach is worth |
| G10 | Follow-back ratio **FRAUD** | following ÷ followers | follow-for-follow padding |
| G11 | Upload consistency | posts in last 30 days | unreliable delivery |
| G12 | Comment-pod signal **FRAUD** | repeat commenters across posts | engagement pods |
| G13 | Category fit (CFR) | beauty posts ÷ last 15 | off-category creator |

G5–G9 bars are set per follower tier from HeBE's own data (view rate: micro 50%, mid 13%, macro 9%,
mega 6%). Structural and fraud tests use standard conventions, since one campaign row per creator
cannot calibrate them.

Output is a two-axis read — **quality** (score and grade) and **price** (great value / good deal /
slightly overpriced / overpriced) shown separately, because they call for different actions — plus a
plain-prose assessment sized for a deal memo.

## Layout

- `tool/page.html` — the calculator (self-contained; benchmarks embedded). Published as an Artifact
  declaring the `sample` capability, which is what lets the page ask Claude to read screenshots.
- `analysis/` — the Python scripts that produced every figure above, in run order:
  `analyze.py` → `corr.py` → `waste.py` → `risk.py` → `weights.py` → `fit.py` → `bench.py` → `blob.py`
- `data/HeBE_KH_KOL_Data.xlsx` — source campaign data
- `data/benchmarks.json` — derived benchmark set consumed by the tool

## Reproducing

```bash
pip install openpyxl
cd analysis
python3 analyze.py && python3 bench.py && python3 brands.py && python3 gates.py \
  && python3 blob.py && python3 blob2.py && python3 blob3.py && python3 inject.py
```

Every script reads `data/HeBE_KH_KOL_Data.xlsx` through `analysis/paths.py` and writes to
`analysis/out/`; `inject.py` writes the rebuilt benchmark blob back into `tool/page.html`. The
supporting analyses (`corr.py`, `waste.py`, `risk.py`, `weights.py`, `fit.py`) print findings and can
be run in any order after `analyze.py`.

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
- 3 of 107 rows carry no fee; 17 carry no TikTok view count. Those rows sit out of the affected
  benchmarks. One row (V Spring) records 5.7 likes against 36.4K views, almost certainly 5.7K
  mistyped.

## Data provenance

`data/HeBE_KH_KOL_Data.xlsx` is the merge of two exports the team supplied. The later template export
contributed two campaigns that were missing (MonyyHang / MediAnswer, Solly / MediAnswer), three
corrected fees (Roi $180→$150, Hong & Hui $400→$350, Marady Tep $300→$350) and seven Mary&May product
names that had been recorded as "Both" or "PDRN". The base file kept the profile-link columns and the
month/year values, which the template export had shifted a column left on 55 older rows.

One month/year caveat: on the rows the two files disagree about, the template export runs exactly one
month earlier than the base file. The base file's values were kept. Month is display-only — it feeds
no score — but if the template's dates are the correct ones, the Month column in the campaign log is
a month late for those rows.
