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

# Deep micro-tune overlay — instruments rescued by the full behavioural tune (verified live on TV).
# Everything NOT in here is greedy-pass-only (default params) and has not been deep-tuned yet.
DEEP = {
    'PEP': {'pf': 1.595, 'dd': 6.47},
    'TLT': {'pf': 1.232, 'dd': 17.71},
}
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

with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write('/* LIQUIDEX FRAMEWORK — 4H cross-section scan data (50 instruments, greedy-optimised). Auto-generated. */\n')
    fh.write('window.SCAN = ' + json.dumps({'rows':rows,'stats':stats,'pep':pep,'tlt':tlt}, ensure_ascii=False, indent=0) + ';\n')

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
