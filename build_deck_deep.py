# Inject the 36-row deep-tuned book into deck.html (between DECK_DEEP markers). Re-runnable.
import json, re

PARAMS = r'C:\Users\sunnf\Desktop\SURGEGURU-FRAMEWORK\deep-params.js'
DECK   = r'C:\Users\sunnf\Desktop\SURGEGURU-FRAMEWORK\deck.html'

t = open(PARAMS, encoding='utf-8').read()
book = json.loads(t.split('window.DEEP_BOOK = ')[1].split('\n;\nwindow.DEEP_STATS')[0]
                  if '\n;\n' in t else t.split('window.DEEP_BOOK = ')[1].split(';\nwindow.DEEP_STATS')[0])

STLABEL = {'re-microtune': 're-microtune', 'walk-forward': 'walk-forward', 'ready': 'ready'}
out = []
for i, r in enumerate(book, 1):
    warn = '<sup>&#9888;</sup>' if r['warn'] else ''
    cls = 'st-remicro' if r['status'] == 're-microtune' else ('st-wf' if r['status'] == 'walk-forward' else 'st-ready')
    out.append(
        f'<tr{" class=\"loss\"" if r["remicro"] else ""}>'
        f'<td class="r num">{i}</td>'
        f'<td class="sym">{r["sym"]}{warn}</td>'
        f'<td>{r["sector"]}</td>'
        f'<td class="r fpf">{r["pf"]:.3f}</td>'
        f'<td class="r num">{r["dd"]:.1f}%</td>'
        f'<td class="r num">{r["win"]:.0f}%</td>'
        f'<td class="r num">{r["n"]}</td>'
        f'<td class="arch">{r["arch"]}</td>'
        f'<td class="{cls}">{STLABEL[r["status"]]}</td>'
        f'</tr>')

SPLIT = 38  # ranks 1-38 on page 4 (carries intro), 39-80 on page 5
r1, r2 = out[:SPLIT], out[SPLIT:]
block1 = '<!--DECK_DEEP_START-->\n    ' + '\n    '.join(r1) + '\n    <!--DECK_DEEP_END-->'
block2 = '<!--DECK_DEEP2_START-->\n    ' + '\n    '.join(r2) + '\n    <!--DECK_DEEP2_END-->'
html = open(DECK, encoding='utf-8').read()
html = re.sub(r'<!--DECK_DEEP_START-->.*?<!--DECK_DEEP_END-->', lambda m: block1, html, flags=re.S)
html = re.sub(r'<!--DECK_DEEP2_START-->.*?<!--DECK_DEEP2_END-->', lambda m: block2, html, flags=re.S)
open(DECK, 'w', encoding='utf-8').write(html)
print(f'Injected {len(r1)} rows (ranks 1-{SPLIT}) + {len(r2)} rows (ranks {SPLIT+1}-{len(out)}). Top {book[0]["sym"]} {book[0]["pf"]}.')
