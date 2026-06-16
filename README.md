# LIQUIDEX Framework — website

A standalone marketing / showcase site for **LIQUIDEX FRAMEWORK** — a proprietary liquidity & market-structure trading system.

## The model: one brain, two eyes
- **LIQUIDEX** — *the brain.* The strategy (5,000+ lines Pine v6) that reads liquidity & market structure and decides the trade (entry · stop · target). The risk logic and sector intelligence are built in.
- **Keeper** — *the eyes on the market.* A companion indicator that ranks the equity universe live (profit factor · momentum · risk).
- **Prophet** — *the eyes on risk.* A companion indicator that shows the risk gate and live position size.
- **Surge Guru** — a crypto-only bonus scanner (not core).

**Delivery:** invite-only on TradingView — the buyer sends their TradingView username, access is granted, and the signals are delivered as alerts (phone / desktop / bot).

## Files
```
index.html          # the page — all sections; English copy lives in the DOM (data-i18n keys)
i18n.js             # Hebrew translations (HE object) + RTL language toggle — keys must stay in sync with index.html
styles.css          # dark trading-terminal theme, fully responsive (CSS variables at top)
app.js              # canvas backdrop, counters, scroll reveals, live ticker (vanilla JS, no deps)
deck.html           # 7-page A4 product brief — print to PDF
framework-deck.pdf  # the brief (regenerated from deck.html)
.nojekyll           # tells GitHub Pages to serve as-is
```
No build step, no dependencies. Open `index.html` in any browser to preview.

## Deploy (GitHub Pages)
Live at `https://wattsonworks.github.io/framework/` — repo `wattsonworks/framework`, Settings → Pages → Source = `main` / root.

## Editing
- **Brand:** `LIQUIDEX` + `FRAMEWORK` in `.brand-text` and the footer of `index.html`.
- **Copy:** English lives in `index.html` (the `data-i18n` elements); Hebrew lives in the `HE` object in `i18n.js`. **Every `data-i18n` key must have a matching `HE` entry** or it falls back to English in Hebrew mode.
- **Backtest tables:** the `#results` `<table>` rows. Keep the historical/hypothetical disclaimer.
- **PDF:** edit `deck.html`, then re-export to `framework-deck.pdf` — browser Print → Save as PDF (A4, no margins, background graphics ON), or headless: `msedge --headless=new --no-pdf-header-footer --print-to-pdf="framework-deck.pdf" "http://localhost:PORT/deck.html"`.
- **Colors:** CSS variables at the top of `styles.css` (`--mint`, `--cyan`, `--amber`, `--grad`).

## Notes
- **No Pine source is published here** — the site shows architecture, features and validated results only. The proprietary `.txt` source stays private.
- All performance figures are historical, hypothetical backtest results, labelled as hypothetical / not financial advice.
