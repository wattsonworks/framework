# SurgeGuru — Proprietary Trading Framework (website)

A standalone marketing/showcase site that unifies the whole trading ecosystem under one brand:

- **LIQUIDEX** — Liquidity Engine (institutional liquidity scanner, 5,000+ lines Pine v6)
- **Surge Guru** — Market Scanner (real-time crypto surge scanner)
- **Risk Engine (LRE)** — directional risk scoring layer
- **Web3 Surge & Risk Engine (SRE)** — cross-sectional sector intelligence
- **Validation Layer** — multi-asset backtesting framework

## Files
```
index.html     # the page (all content/sections)
styles.css     # dark trading-terminal theme, fully responsive
app.js         # canvas backdrop, counters, scroll reveals, live ticker (vanilla JS, no deps)
.nojekyll      # tells GitHub Pages to serve as-is
```
No build step, no dependencies. Open `index.html` in any browser to preview.

## Deploy to GitHub Pages
1. Create a new repo (suggested: `wattsonworks/framework` — do **not** overwrite an existing product repo).
2. Push these files to the `main` branch root.
3. Repo → Settings → Pages → Source = `main` / root.
4. Live at `https://wattsonworks.github.io/framework/`.

> Custom domain optional: add a `CNAME` file with your domain and configure DNS.

## Editing
- **Brand name:** search `SURGE<b>GURU` in `index.html` (and `SURGEGURU` in README) to rename the umbrella.
- **Product links:** the LIQUIDEX / SG / LRE URLs live in the engine cards, pricing cards and footer of `index.html`.
- **Backtest table:** edit the `#backtests` `<table>` rows. Keep the historical/hypothetical disclaimer.
- **Colors:** all theming via CSS variables at the top of `styles.css` (`--mint`, `--cyan`, `--red`, `--grad`).

## Notes
- **No Pine source is published here** — the site shows architecture, features and line counts only. The proprietary `.txt` source stays private.
- All performance figures are historical backtest results and are labelled as hypothetical / not financial advice.
