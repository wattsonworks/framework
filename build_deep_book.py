# Parse BEST_PARAMS_PER_SYMBOL.md -> deep-params.js (window.DEEP_BOOK + window.DEEP_STATS).
# Each symbol: deep-tune result + full per-symbol config nuances + re-tune note + status flags.
# 2026-06 rework: ASSET CLASS is now first-class (equity / crypto / forex) — the cross-asset-class
# invariance is the headline. Crypto is profiled as its own (cleanest) book; EURUSD is the forex baseline.
import re, json

SRC = r'C:\Users\sunnf\Desktop\LIQUIDEX\BEST_PARAMS_PER_SYMBOL.md'
OUT = r'C:\Users\sunnf\Desktop\SURGEGURU-FRAMEWORK\deep-params.js'
STAMP_DISPLAY = '21 Jun 2026'
STAMP_RAW = '2026-06-21T01:45'
EQUITY_UNIVERSE = 50   # the equity cross-section that was scanned end-to-end

txt = open(SRC, encoding='utf-8').read()
blocks = re.split(r'\n(?=## )', txt)
HDR = re.compile(r'^## (\S+)(\s*⚠️)?\s*—\s*PF ([\d.]+) · DD ([\d.]+)% · Win ([\d.]+)% · N (\d+) · (.+?)\s*$', re.M)

CRYPTO = {'BTC', 'ETH', 'ETH-CB', 'SOL'}
SECTOR = {}
for s in 'KLAC NXPI QCOM TXN MCHP MPWR ADI NVDA AMD MRVL ARM LRCX AMAT ASML TSM INTC TSEM MU'.split(): SECTOR[s] = 'Semis'
for s in 'DIA IWM SMH XLF XLK XLI XLE XLV XLP XLY VGT VOO SCHD IGV SOXX SPY QQQ GLD TLT'.split(): SECTOR[s] = 'ETF'
for s in 'JPM KO PEP COST DE ETN ORCL PANW V MA XOM'.split(): SECTOR[s] = 'Single-name'

def asset_class(sym):
    if sym in CRYPTO: return 'crypto'
    if sym == 'EURUSD': return 'forex'
    return 'equity'

def fam_of(arch):
    a = arch.lower()
    if 'trend' in a or 'continuation' in a: return 'trend/continuation'
    return 'fade'

def bullet(block, label):
    m = re.search(r'- \*\*' + re.escape(label) + r':\*\*\s*(.+)', block)
    return m.group(1).strip() if m else ''

rows = []
for b in blocks:
    m = HDR.search(b)
    if not m: continue
    sym, warn, pf, dd, win, n, arch = m.groups()
    pf = float(pf); dd = float(dd); win = float(win); n = int(n)
    cls = asset_class(sym)
    remicro = pf <= 1.5 and cls == 'equity'   # only equities are flagged for re-tune; crypto cells are accepted as-tuned
    rows.append({
        'sym': sym, 'warn': bool(warn), 'pf': pf, 'dd': dd, 'win': win, 'n': n,
        'arch': arch.strip(), 'remicro': remicro,
        'assetClass': cls,
        'sector': 'Crypto' if cls == 'crypto' else SECTOR.get(sym, '—'),
        'family': fam_of(arch),
        'status': 're-microtune' if remicro else ('walk-forward' if warn else 'ready'),
        'date': STAMP_DISPLAY, 'dateRaw': STAMP_RAW,
        'exec': bullet(b, 'Execution'),
        'stops': bullet(b, 'Stops/Targets'),
        'signals': bullet(b, 'Signals'),
        'gates': bullet(b, 'Gates'),
        'note': bullet(b, 'Re-tune note'),
    })

# --- FOREX baseline: EURUSD (the strategy's namesake). User-reported performance export; ---
# --- config/trade-count not captured → kept OUT of the per-config rows (a baseline, not a tuned cell). ---
forex_baseline = {
    'sym': 'EURUSD', 'pf': 1.40, 'dd': 16.74, 'net': 72.65, 'dir': 'both-direction',
    'note': "the strategy's namesake market and its weakest profitable book — PF ~1.40 vs crypto 2.0-2.4; it even trailed EURUSD buy-and-hold. Net +72.65% over ~10yr, both directions.",
}

rows.sort(key=lambda r: -r['pf'])

def cls_rows(c): return [r for r in rows if r['assetClass'] == c]
equity = cls_rows('equity'); crypto = cls_rows('crypto')

def class_stat(g):
    real = [r for r in g if r['n']]
    return {
        'n': len(g),
        'meanPF': round(sum(r['pf'] for r in g) / len(g), 2) if g else 0,
        'meanDD': round(sum(r['dd'] for r in g) / len(g), 1) if g else 0,
        'topPF': max((r['pf'] for r in g), default=0),
        'topSym': max(g, key=lambda r: r['pf'])['sym'] if g else '',
        'cleanestDD': min((r['dd'] for r in real), default=0),
        'cleanestSym': min(real, key=lambda r: r['dd'])['sym'] if real else '',
    }

stats = {
    'count': len(rows), 'universe': EQUITY_UNIVERSE,
    'equityCount': len(equity), 'cryptoCount': len(crypto), 'forexCount': 1,
    'pending': EQUITY_UNIVERSE - len(equity),
    'ready': sum(1 for r in rows if r['status'] == 'ready'),
    'walkfwd': sum(1 for r in rows if r['status'] == 'walk-forward'),
    'remicro': sum(1 for r in rows if r['status'] == 're-microtune'),
    'above15': sum(1 for r in rows if r['pf'] > 1.5),
    'topPF': rows[0]['pf'], 'topSym': rows[0]['sym'],
    'cleanestDD': min(r['dd'] for r in rows if r['n']),
    'cleanestSym': min((r for r in rows if r['n']), key=lambda r: r['dd'])['sym'],
    'cryptoMeanDD': round(sum(r['dd'] for r in crypto) / len(crypto), 1) if crypto else 0,
    'equityMeanDD': round(sum(r['dd'] for r in equity) / len(equity), 1) if equity else 0,
    'fade': sum(1 for r in rows if r['family'] == 'fade'),
    'date': STAMP_DISPLAY, 'dateRaw': STAMP_RAW,
    'byClass': {'equity': class_stat(equity), 'crypto': class_stat(crypto),
                'forex': {'n': 1, 'meanPF': forex_baseline['pf'], 'meanDD': forex_baseline['dd'],
                          'topPF': forex_baseline['pf'], 'topSym': 'EURUSD',
                          'cleanestDD': forex_baseline['dd'], 'cleanestSym': 'EURUSD', 'net': forex_baseline['net']}},
}
def sect_stat(name):
    g = [r for r in rows if r['sector'] == name]
    if not g: return {'n': 0}
    best = max(g, key=lambda r: r['pf'])
    return {'n': len(g), 'meanPF': round(sum(r['pf'] for r in g) / len(g), 2),
            'best': best['pf'], 'bestSym': best['sym'],
            'ready': sum(1 for r in g if not r['remicro'])}
stats['sect'] = {s: sect_stat(s) for s in ('ETF', 'Semis', 'Single-name', 'Crypto')}

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('/* LIQUIDEX FRAMEWORK — deep-tuned book across asset classes (equity / crypto / forex).\n')
    fh.write('   Auto-generated from BEST_PARAMS_PER_SYMBOL.md + the EURUSD forex baseline. */\n')
    fh.write('window.DEEP_BOOK = ' + json.dumps(rows, ensure_ascii=False, indent=0) + ';\n')
    fh.write('window.DEEP_STATS = ' + json.dumps(stats, ensure_ascii=False) + ';\n')
    fh.write('window.DEEP_FOREX = ' + json.dumps(forex_baseline, ensure_ascii=False) + ';\n')

print('=== DEEP BOOK (cross-asset-class) ===')
print(f"{len(rows)} cells | equity {len(equity)} · crypto {len(crypto)} · forex 1 (EURUSD baseline)")
print(f"ready {stats['ready']} · walk-fwd {stats['walkfwd']} · re-microtune {stats['remicro']} | >1.5PF {stats['above15']}")
print(f"top {stats['topSym']} {stats['topPF']} | cleanest DD {stats['cleanestSym']} {stats['cleanestDD']}%")
print(f"mean DD — equity {stats['equityMeanDD']}% vs crypto {stats['cryptoMeanDD']}%  (crypto = the cleaner book)")
print('byClass:', json.dumps(stats['byClass']))
print('WROTE', OUT)
