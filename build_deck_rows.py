# Generates the 50-row cross-section table for deck.html from the live CSV + deep-tune overlay.
# Re-runnable: replaces everything between the SCAN_ROWS markers.
import csv, re

CSV  = r'C:\Users\sunnf\Desktop\LIQUIDEX\GREEDY_4H_LOG.csv'
DECK = r'C:\Users\sunnf\Desktop\SURGEGURU-FRAMEWORK\deck.html'
CLS  = {'SEMIS':'Semis','ETF':'ETF','PRIORITY':'Single-name'}
# deep micro-tune result per rescued name: (profit factor, max drawdown %)
DEEP = {'PEP':('1.595','6.47'),'TLT':('1.232','17.71')}

def fl(x):
    try: return float(x)
    except: return None

rows=[]
with open(CSV, newline='', encoding='utf-8-sig') as fh:
    for r in csv.DictReader(fh):
        if not r.get('Symbol'): continue
        base=fl(r['BasePF']); final=fl(r['FinalPF']); dd=fl(r['MaxDD_pct']); tr=int(fl(r['Trades']) or 0)
        rows.append({'sym':r['Symbol'].strip(),'cls':CLS.get(r['Sector'].strip(),r['Sector'].strip()),
                     'fam':r['Family'].strip().capitalize(),'base':base,'final':final,
                     'lift':final/base if base else None,'dd':dd,'tr':tr})

rows.sort(key=lambda r:-r['final'])
out=[]
for i,r in enumerate(rows,1):
    loss = r['final'] < 1.0
    dag = '<sup>&dagger;</sup>' if loss else ''
    deep = DEEP.get(r['sym'])
    mt = (f'&#10003; {deep[0]} &middot; {deep[1]}%') if deep else '&mdash;'
    mtc = ' y' if deep else ''
    lift = f"{r['lift']:.2f}&times;" if r['lift'] is not None else '&mdash;'
    out.append(
        f'<tr{" class=\"loss\"" if loss else ""}>'
        f'<td class="r num">{i}</td>'
        f'<td class="sym">{r["sym"]}{dag}</td>'
        f'<td>{r["cls"]}</td>'
        f'<td>{r["fam"]}</td>'
        f'<td class="r num">{r["base"]:.3f}</td>'
        f'<td class="r fpf">{r["final"]:.3f}</td>'
        f'<td class="r num">{lift}</td>'
        f'<td class="r num">{r["dd"]:.1f}%</td>'
        f'<td class="r num">{r["tr"]}</td>'
        f'<td class="mt{mtc}">{mt}</td>'
        f'</tr>')

SPLIT = 32  # rows 1..SPLIT on page 4, rest on page 5
def block(tag, items):
    return f'<!--SCAN_ROWS_{tag}_START-->\n    ' + '\n    '.join(items) + f'\n    <!--SCAN_ROWS_{tag}_END-->'

html = open(DECK, encoding='utf-8').read()
html = re.sub(r'<!--SCAN_ROWS_A_START-->.*?<!--SCAN_ROWS_A_END-->', block('A', out[:SPLIT]), html, flags=re.S)
html = re.sub(r'<!--SCAN_ROWS_B_START-->.*?<!--SCAN_ROWS_B_END-->', block('B', out[SPLIT:]), html, flags=re.S)
open(DECK, 'w', encoding='utf-8').write(html)
print(f'Injected {len(out)} rows ({SPLIT}+{len(out)-SPLIT}). Top: {rows[0]["sym"]} {rows[0]["final"]:.3f}  | losers:',
      [r["sym"] for r in rows if r["final"]<1.0])
