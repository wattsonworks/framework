# Parse BEST_PARAMS_PER_SYMBOL.md -> deep-params.js (window.DEEP_BOOK + window.DEEP_STATS + window.DEEP_FOREX).
# 2026-06 rework: ASSET CLASS is first-class (equity / crypto / forex). The full-run book — 50 equities,
# 28 crypto, 3 FX majors — all flow through as cells; rows without a numeric PF (no-data) are skipped.
import re, json

SRC = r'C:\Users\sunnf\Desktop\LIQUIDEX\BEST_PARAMS_PER_SYMBOL.md'
OUT = r'C:\Users\sunnf\Desktop\SURGEGURU-FRAMEWORK\deep-params.js'
STAMP_DISPLAY = '21 Jun 2026'
STAMP_RAW = '2026-06-21T12:00'
EQUITY_UNIVERSE = 50

txt = open(SRC, encoding='utf-8').read()
blocks = re.split(r'\n(?=## )', txt)
HDR = re.compile(r'^## (\S+)(\s*⚠️)?\s*—\s*PF ([\d.]+) · DD ([\d.]+)% · Win ([\d.]+)% · N (\d+) · (.+?)\s*$', re.M)

CRYPTO = set('BTC ETH ETH-CB SOL BNB XRP ADA AVAX LINK DOGE DOT LTC BCH ATOM NEAR INJ FIL RENDER FET ARB OP APT SUI UNI AAVE TRX ICP POL'.split())
FOREX = set('EURUSD GBPUSD USDJPY'.split())
SECTOR = {}
for s in 'KLAC NXPI QCOM TXN MCHP MPWR ADI NVDA AMD MRVL ARM LRCX AMAT ASML TSM INTC TSEM MU ON AVGO'.split(): SECTOR[s] = 'Semis'
for s in 'DIA IWM SMH XLF XLK XLI XLE XLV XLP XLY VGT VOO SCHD IGV SOXX SPY QQQ GLD TLT'.split(): SECTOR[s] = 'ETF'
for s in 'JPM KO PEP COST DE ETN ORCL PANW V MA XOM'.split(): SECTOR[s] = 'Single-name'

def asset_class(sym):
    if sym in CRYPTO: return 'crypto'
    if sym in FOREX: return 'forex'
    return 'equity'

def fam_of(arch):
    a = arch.lower()
    if 'both' in a: return 'both-direction'
    if 'trend' in a or 'continuation' in a: return 'trend/continuation'
    return 'fade'

def bullet(block, label):
    m = re.search(r'- \*\*' + re.escape(label) + r':\*\*\s*(.+)', block)
    return m.group(1).strip() if m else ''

rows = []
for b in blocks:
    m = HDR.search(b)
    if not m: continue            # skips no-data rows (e.g. POL "PF n/a")
    sym, warn, pf, dd, win, n, arch = m.groups()
    pf = float(pf); dd = float(dd); win = float(win); n = int(n)
    cls = asset_class(sym)
    remicro = pf <= 1.5 and cls == 'equity'
    rows.append({
        'sym': sym, 'warn': bool(warn), 'pf': pf, 'dd': dd, 'win': win, 'n': n,
        'arch': arch.strip(), 'remicro': remicro, 'assetClass': cls,
        'sector': ('Crypto' if cls == 'crypto' else 'Forex' if cls == 'forex' else SECTOR.get(sym, '—')),
        'family': fam_of(arch),
        'status': 're-microtune' if remicro else ('walk-forward' if warn else 'ready'),
        'date': STAMP_DISPLAY, 'dateRaw': STAMP_RAW,
        'exec': bullet(b, 'Execution'), 'stops': bullet(b, 'Stops/Targets'),
        'signals': bullet(b, 'Signals'), 'gates': bullet(b, 'Gates'), 'note': bullet(b, 'Re-tune note'),
    })

rows.sort(key=lambda r: -r['pf'])
def cls_rows(c): return [r for r in rows if r['assetClass'] == c]
equity, crypto, forex = cls_rows('equity'), cls_rows('crypto'), cls_rows('forex')

# EURUSD user-reported baseline (separate from the tuned EURUSD cell) — kept for the honest footnote.
forex_baseline = {'sym': 'EURUSD', 'pf': 1.40, 'dd': 16.74, 'net': 72.65,
                  'note': "the namesake forex baseline (user-reported) trailed buy-and-hold; the tuned both-direction FX cells (GBPUSD 3.41, USDJPY 3.03) far exceed it."}

def class_stat(g):
    if not g: return {'n': 0}
    return {'n': len(g), 'meanPF': round(sum(r['pf'] for r in g) / len(g), 2),
            'meanDD': round(sum(r['dd'] for r in g) / len(g), 1),
            'topPF': max(r['pf'] for r in g), 'topSym': max(g, key=lambda r: r['pf'])['sym'],
            'cleanestDD': min(r['dd'] for r in g), 'cleanestSym': min(g, key=lambda r: r['dd'])['sym'],
            'edges': sum(1 for r in g if r['pf'] >= 1.0 and r['n'] >= 30)}

EDGE = [r for r in rows if r['pf'] >= 1.0 and r['n'] >= 30]
BOTH = [r for r in rows if r['family'] == 'both-direction' and r['pf'] >= 1.0 and r['n'] >= 30]
stats = {
    'count': len(rows), 'universe': EQUITY_UNIVERSE,
    'equityCount': len(equity), 'cryptoCount': len(crypto), 'forexCount': len(forex),
    'edges': len(EDGE), 'bothDirEdges': len(BOTH),
    'ready': sum(1 for r in rows if r['status'] == 'ready'),
    'walkfwd': sum(1 for r in rows if r['status'] == 'walk-forward'),
    'remicro': sum(1 for r in rows if r['status'] == 're-microtune'),
    'above15': sum(1 for r in rows if r['pf'] > 1.5),
    'topPF': rows[0]['pf'], 'topSym': rows[0]['sym'],
    'cleanestDD': min(r['dd'] for r in rows), 'cleanestSym': min(rows, key=lambda r: r['dd'])['sym'],
    'cryptoMeanDD': round(sum(r['dd'] for r in crypto) / len(crypto), 1) if crypto else 0,
    'equityMeanDD': round(sum(r['dd'] for r in equity) / len(equity), 1) if equity else 0,
    'date': STAMP_DISPLAY, 'dateRaw': STAMP_RAW,
    'byClass': {'equity': class_stat(equity), 'crypto': class_stat(crypto), 'forex': class_stat(forex)},
}
def sect_stat(name):
    g = [r for r in rows if r['sector'] == name]
    if not g: return {'n': 0}
    best = max(g, key=lambda r: r['pf'])
    return {'n': len(g), 'meanPF': round(sum(r['pf'] for r in g) / len(g), 2),
            'best': best['pf'], 'bestSym': best['sym'], 'ready': sum(1 for r in g if not r['remicro'])}
stats['sect'] = {s: sect_stat(s) for s in ('ETF', 'Semis', 'Single-name', 'Crypto', 'Forex')}

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('/* LIQUIDEX FRAMEWORK — deep-tuned book across asset classes (equity / crypto / forex). Auto-generated. */\n')
    fh.write('window.DEEP_BOOK = ' + json.dumps(rows, ensure_ascii=False, indent=0) + ';\n')
    fh.write('window.DEEP_STATS = ' + json.dumps(stats, ensure_ascii=False) + ';\n')
    fh.write('window.DEEP_FOREX = ' + json.dumps(forex_baseline, ensure_ascii=False) + ';\n')

print('=== DEEP BOOK (cross-asset-class, full run) ===')
print(f"{len(rows)} cells | equity {len(equity)} · crypto {len(crypto)} · forex {len(forex)} | edges {len(EDGE)} | both-dir edges {len(BOTH)}")
print(f"top {stats['topSym']} {stats['topPF']} | cleanest DD {stats['cleanestSym']} {stats['cleanestDD']}%")
print(f"mean DD — equity {stats['equityMeanDD']}% vs crypto {stats['cryptoMeanDD']}%")
print('byClass:', json.dumps(stats['byClass']))
print('WROTE', OUT)
