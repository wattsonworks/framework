# Parse BEST_PARAMS_PER_SYMBOL.md -> deep-params.js (window.DEEP_BOOK + window.DEEP_STATS).
# Each symbol: deep-tune result + full per-symbol config nuances + re-tune note + status flags.
import re, json

SRC = r'C:\Users\sunnf\Desktop\LIQUIDEX\BEST_PARAMS_PER_SYMBOL.md'
OUT = r'C:\Users\sunnf\Desktop\SURGEGURU-FRAMEWORK\deep-params.js'
STAMP_DISPLAY = '3:33 pm · 20 Jun 2026'
STAMP_RAW = '2026-06-20T15:33'
UNIVERSE = 52

txt = open(SRC, encoding='utf-8').read()
# split into symbol blocks
blocks = re.split(r'\n(?=## )', txt)
HDR = re.compile(r'^## (\S+)(\s*⚠️)?\s*—\s*PF ([\d.]+) · DD ([\d.]+)% · Win ([\d.]+)% · N (\d+) · (.+?)\s*$', re.M)

SECTOR = {}
for s in 'KLAC NXPI QCOM TXN MCHP MPWR ADI NVDA AMD MRVL ARM LRCX AMAT ASML TSM INTC TSEM MU'.split(): SECTOR[s]='Semis'
for s in 'DIA XLF XLK XLI XLV VOO SCHD SPY QQQ GLD TLT'.split(): SECTOR[s]='ETF'
for s in 'KO PEP COST DE ETN V MA'.split(): SECTOR[s]='Single-name'

def bullet(block, label):
    m = re.search(r'- \*\*' + re.escape(label) + r':\*\*\s*(.+)', block)
    return m.group(1).strip() if m else ''

rows = []
for b in blocks:
    m = HDR.search(b)
    if not m: continue
    sym, warn, pf, dd, win, n, arch = m.groups()
    pf = float(pf); dd = float(dd); win = float(win); n = int(n)
    remicro = pf <= 1.5
    rows.append({
        'sym': sym, 'warn': bool(warn), 'pf': pf, 'dd': dd, 'win': win, 'n': n,
        'arch': arch.strip(), 'remicro': remicro,
        'sector': SECTOR.get(sym, '—'),
        'family': 'continuation' if 'continuation' in arch else 'fade',
        'status': 're-microtune' if remicro else ('walk-forward' if warn else 'ready'),
        'date': STAMP_DISPLAY, 'dateRaw': STAMP_RAW,
        'exec': bullet(b, 'Execution'),
        'stops': bullet(b, 'Stops/Targets'),
        'signals': bullet(b, 'Signals'),
        'gates': bullet(b, 'Gates'),
        'note': bullet(b, 'Re-tune note'),
    })

rows.sort(key=lambda r: -r['pf'])
stats = {
    'count': len(rows), 'universe': UNIVERSE, 'pending': UNIVERSE - len(rows),
    'ready': sum(1 for r in rows if r['status'] == 'ready'),
    'walkfwd': sum(1 for r in rows if r['status'] == 'walk-forward'),
    'remicro': sum(1 for r in rows if r['status'] == 're-microtune'),
    'above15': sum(1 for r in rows if r['pf'] > 1.5),
    'topPF': rows[0]['pf'], 'topSym': rows[0]['sym'],
    'cleanestDD': min(r['dd'] for r in rows), 'cleanestSym': min(rows, key=lambda r: r['dd'])['sym'],
    'fade': sum(1 for r in rows if r['family'] == 'fade'),
    'continuation': sum(1 for r in rows if r['family'] == 'continuation'),
    'date': STAMP_DISPLAY, 'dateRaw': STAMP_RAW,
}
def sect_stat(name):
    g = [r for r in rows if r['sector'] == name]
    best = max(g, key=lambda r: r['pf'])
    return {'n': len(g), 'meanPF': round(sum(r['pf'] for r in g)/len(g), 2),
            'best': best['pf'], 'bestSym': best['sym'],
            'ready': sum(1 for r in g if not r['remicro'])}
stats['sect'] = {s: sect_stat(s) for s in ('ETF', 'Semis', 'Single-name')}

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('/* LIQUIDEX FRAMEWORK — deep-tuned book (36/52 symbols, per-symbol best config). Auto-generated from BEST_PARAMS_PER_SYMBOL.md. */\n')
    fh.write('window.DEEP_BOOK = ' + json.dumps(rows, ensure_ascii=False, indent=0) + ';\n')
    fh.write('window.DEEP_STATS = ' + json.dumps(stats, ensure_ascii=False) + ';\n')

print('=== DEEP BOOK ===')
print(f"{len(rows)} symbols | ready {stats['ready']} · walk-fwd {stats['walkfwd']} · re-microtune {stats['remicro']} | >1.5PF {stats['above15']}")
print(f"top {stats['topSym']} {stats['topPF']} | cleanest DD {stats['cleanestSym']} {stats['cleanestDD']}%")
print('re-microtune (<=1.5):', [r['sym'] for r in rows if r['remicro']])
print('family: fade', stats['fade'], '· continuation', stats['continuation'])
print('sectors:', json.dumps(stats['sect']))
print('WROTE', OUT)
