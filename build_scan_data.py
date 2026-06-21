# Reads the live 4H greedy scan, computes summary stats, emits scan-data.js for the site.
import csv, json

SRC = r'C:\Users\sunnf\Desktop\LIQUIDEX\GREEDY_4H_LOG.csv'
OUT = r'C:\Users\sunnf\Desktop\SURGEGURU-FRAMEWORK\scan-data.js'

def fl(x):
    try: return float(x)
    except: return None

SECTOR_LABEL = {'SEMIS':'Semis','ETF':'ETF','PRIORITY':'Single-name'}
TOG = [('Shorts','dir'),('Breaker','Breaker'),('CascStop','Cascade-stop'),
       ('WallTP_Room','Wall-TP'),('LQX','LQX gate'),('Velo','Risk-velocity'),
       ('Iceberg','Iceberg'),('BSL_SSL','BSL/SSL')]

rows = []
with open(SRC, newline='', encoding='utf-8-sig') as fh:
    for r in csv.DictReader(fh):
        if not r.get('Symbol'): continue
        base = fl(r['BasePF']); final = fl(r['FinalPF']); dd = fl(r['MaxDD_pct'])
        win = fl(r['Win_pct']); trades = int(fl(r['Trades']) or 0)
        conf = []
        if r['Shorts'].strip()=='on': conf.append('Long+Short')
        else: conf.append('Long-only')
        for key,label in TOG[1:]:
            if r[key].strip()=='Y': conf.append(label)
        rows.append({
            'sym': r['Symbol'].strip(), 'sector': r['Sector'].strip(),
            'sectorLabel': SECTOR_LABEL.get(r['Sector'].strip(), r['Sector'].strip()),
            'family': r['Family'].strip(),
            'base': round(base,3), 'pf': round(final,3),
            'lift': round(final/base,2) if base else None,
            'dd': round(dd,2), 'win': round(win,1), 'trades': trades,
            'conf': conf,
        })

# Deep micro-tune overlay — the FULL behavioural book (verified live on TV), read from DEEP_4H_LOG.csv.
# Equities overlay onto the greedy scan; crypto + forex are separate asset-class books (below).
DEEP_SRC = r'C:\Users\sunnf\Desktop\LIQUIDEX\DEEP_4H_LOG.csv'
CRYPTO_SYMS = set('BTC ETH ETH-CB SOL BNB XRP ADA AVAX LINK DOGE DOT LTC BCH ATOM NEAR INJ FIL RENDER FET ARB OP APT SUI UNI AAVE TRX ICP POL PEPE ENA TIA SEI JUP LDO RUNE WIF ONDO MKR'.split())
FOREX_SYMS = set('EURUSD GBPUSD USDJPY USDCHF AUDJPY NZDUSD USDCAD AUDUSD GBPJPY EURJPY EURGBP'.split())
CRYPTO_FEED = {'BTC': 'Bitstamp', 'ETH': 'Bitstamp', 'ETH-CB': 'Coinbase'}  # rest default to Binance
DEEP = {}
crypto = []
forex = []
with open(DEEP_SRC, newline='', encoding='utf-8-sig') as fh:
    for d in csv.DictReader(fh):
        sym = (d.get('Symbol') or '').strip()
        if not sym: continue
        dpf = fl(d['DeepPF']); ddd = fl(d['MaxDD_pct'])
        rec = {'sym': sym.replace('-CB', ''), 'pf': round(dpf, 3) if dpf else None,
               'dd': round(ddd, 2) if ddd is not None else None, 'win': fl(d['Win_pct']),
               'trades': int(fl(d['Trades']) or 0),
               'dir': 'Long+Short' if d['Shorts'].strip() == 'on' else 'Long-only',
               'family': d['Family'].strip()}
        if sym in CRYPTO_SYMS:
            if dpf is None: continue   # skip no-data (POL)
            rec['feed'] = CRYPTO_FEED.get(sym, 'Binance'); crypto.append(rec)
        elif sym in FOREX_SYMS:
            if dpf is None: continue
            rec['feed'] = 'OANDA'; forex.append(rec)
        elif dpf is not None and ddd is not None:
            DEEP[sym] = {'pf': dpf, 'dd': ddd}
crypto.sort(key=lambda r: -(r['pf'] or 0))
forex.sort(key=lambda r: -(r['pf'] or 0))
for r in rows:
    d = DEEP.get(r['sym'])
    r['tuned'] = bool(d)
    r['deepPF'] = d['pf'] if d else None
    r['deepDD'] = d['dd'] if d else None

n = len(rows)
prof = [r for r in rows if r['pf']>=1.0]
los = [r for r in rows if r['pf']<1.0]
flipped = [r for r in rows if r['base']<1.0 and r['pf']>=1.0]
safe = sorted([r for r in rows if r['dd']<=15 and r['pf']>=1.3], key=lambda r:-(r['pf']/(1+r['dd']/100)))
mean_base = sum(r['base'] for r in rows)/n
mean_final = sum(r['pf'] for r in rows)/n
fam = {}
for f in ('fade','continuation'):
    g = [r for r in rows if r['family']==f]
    fam[f] = {'n':len(g), 'meanPF':round(sum(x['pf'] for x in g)/len(g),3), 'meanDD':round(sum(x['dd'] for x in g)/len(g),1)}
sect = {}
for s in ('SEMIS','ETF','PRIORITY'):
    g = [r for r in rows if r['sector']==s]
    best = max(g, key=lambda r:r['pf'])
    sect[s] = {'n':len(g), 'meanPF':round(sum(x['pf'] for x in g)/len(g),3),
               'bestSym':best['sym'], 'bestPF':best['pf'],
               'profitable':len([r for r in g if r['pf']>=1.0])}
# toggle frequency among all
tfreq = {}
for key,label in TOG[1:]:
    cnt = sum(1 for r in rows if (r['sym'] and label in r['conf']))
    tfreq[label] = cnt
longonly = sum(1 for r in rows if 'Long-only' in r['conf'])

stats = {
    'n': n, 'profitable': len(prof), 'losers': len(los),
    'loserSyms': [r['sym'] for r in los],
    'flipped': len(flipped),
    'meanBase': round(mean_base,3), 'meanFinal': round(mean_final,3),
    'meanLift': round(mean_final/mean_base,2),
    'topPF': max(r['pf'] for r in rows),
    'topSym': max(rows, key=lambda r:r['pf'])['sym'],
    'cleanestDD': min(r['dd'] for r in safe),
    'cleanestSym': min(safe, key=lambda r:r['dd'])['sym'],
    'safeCount': len(safe), 'safeSyms':[r['sym'] for r in safe],
    'fam': fam, 'sect': sect, 'tfreq': tfreq, 'longonly': longonly,
    'tunedSyms': [r['sym'] for r in rows if r['tuned']],
    'tunedCount': sum(1 for r in rows if r['tuned']),
    'pendingCount': sum(1 for r in rows if not r['tuned']),
}

# PEP micro-tuning case — the patient staple (deep-tuned reproduction, verified live)
pep = {
    'base': 0.749,         # clean engine, default
    'greedy': 0.849,       # Stage-1 toggle-only greedy — a loser
    'tuned': 1.595,        # deep behavioural micro-tune (verified live on TV)
    'dd': 6.47, 'win': 48.6, 'wins': 52, 'trades': 107,
    'toggles': 11, 'params': 6,
}
# TLT micro-tuning case — the fragile macro vehicle; the edge lives in the Partial-TP values
tlt = {
    'base': 0.653,         # clean engine, default
    'greedy': 0.809,       # Stage-1 greedy — still dead
    'tuned': 1.232,        # deep behavioural micro-tune (verified live on TV)
    'dd': 17.71, 'win': 47.44, 'wins': 102, 'trades': 215, 'pnl': 15.73,
    'partialBank': 60, 'partialNear': 0.66,  # the hero levers
}

stats['assetClass'] = {
    'equity': {'n': n, 'meanPF': round(mean_final, 2), 'meanDD': round(sum(r['dd'] for r in rows) / n, 1)},
    'crypto': {'n': len(crypto),
               'meanPF': round(sum(c['pf'] for c in crypto) / len(crypto), 2) if crypto else 0,
               'meanDD': round(sum(c['dd'] for c in crypto) / len(crypto), 1) if crypto else 0,
               'cleanestDD': min((c['dd'] for c in crypto), default=0),
               'cleanestSym': min(crypto, key=lambda c: c['dd'])['sym'] if crypto else ''},
    'forex': {'n': len(forex),
              'meanPF': round(sum(f['pf'] for f in forex) / len(forex), 2) if forex else 0,
              'meanDD': round(sum(f['dd'] for f in forex) / len(forex), 1) if forex else 0,
              'topPF': max((f['pf'] for f in forex), default=0),
              'topSym': max(forex, key=lambda f: f['pf'])['sym'] if forex else ''},
}

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('/* LIQUIDEX FRAMEWORK — cross-asset-class scan data: 50 equities (greedy + full deep overlay), 27 crypto cells, 3 FX-major cells. Auto-generated. */\n')
    fh.write('window.SCAN = ' + json.dumps({'rows': rows, 'stats': stats, 'pep': pep, 'tlt': tlt, 'crypto': crypto, 'forex': forex}, ensure_ascii=False, indent=0) + ';\n')

print('=== SUMMARY ===')
print(f"n={n} profitable={len(prof)} losers={len(los)} {stats['loserSyms']}")
print(f"flipped <1 -> >=1: {len(flipped)}")
print(f"mean base={mean_base:.3f} mean final={mean_final:.3f} lift={mean_final/mean_base:.2f}x")
print(f"top {stats['topSym']} {stats['topPF']}  cleanest {stats['cleanestSym']} {stats['cleanestDD']}%")
print(f"safe book ({len(safe)}): {[r['sym'] for r in safe]}")
print('families:', fam)
print('sectors:', sect)
print('toggle freq:', tfreq, 'long-only:', longonly)
print('deep-tuned:', stats['tunedSyms'], '| pending micro-tune:', stats['pendingCount'])
print('WROTE', OUT)
