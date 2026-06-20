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

block = '<!--DECK_DEEP_START-->\n    ' + '\n    '.join(out) + '\n    <!--DECK_DEEP_END-->'
html = open(DECK, encoding='utf-8').read()
html = re.sub(r'<!--DECK_DEEP_START-->.*?<!--DECK_DEEP_END-->', block, html, flags=re.S)
open(DECK, 'w', encoding='utf-8').write(html)
print(f'Injected {len(out)} deep-book rows. Top {book[0]["sym"]} {book[0]["pf"]}.')
