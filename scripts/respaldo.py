"""Actualiza en index.html los valores de respaldo (los que se ven si no carga datos/actual.json)."""
import json, re
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
A = json.loads((RAIZ / 'datos/actual.json').read_text())
s = (RAIZ / 'index.html').read_text()
f = lambda x: ('%.1f' % x).replace('.', ',')
def get(p):
    o = A
    for k in p.split('.'):
        o = o[int(k)] if isinstance(o, list) else o[k]
    return o
def span(m):
    attrs, txt = m.group(1), m.group(2)
    k = re.search(r'data-v="([^"]+)"', attrs).group(1)
    try: v = get(k)
    except Exception: return m.group(0)
    if isinstance(v, list):
        if 'data-r' in attrs:
            sep = ' y ' if ' y ' in txt else '-'
            t = f(v[1]) + sep + f(v[2])
        else: t = f(v[0])
    else:
        d = re.search(r'data-d="(\d)"', attrs); t = ('%.' + (d.group(1) if d else '1') + 'f') % v; t = t.replace('.', ',')
    return '<span' + attrs + '>' + t + '</span>'
s = re.sub(r'<span( data-v="[^"]+"[^>]*)>([^<]*)</span>', span, s)
NB = ' '
c = lambda v, big: '<td class="g" style="padding-left:4px;padding-right:2px"><strong style="white-space:nowrap' + (';color:var(--accent)' if big else '') + '">' + f(v[1]) + NB + '%–' + f(v[2]) + NB + '%</strong></td>'
hd = lambda t: '<tr><td colspan="3" style="text-align:left;border-bottom:none;padding-bottom:0;font-size:.9em;color:var(--ink2)"><strong>' + t + '</strong></td></tr>'
a = A['actual']
i = s.index('<tbody id="aRows">') + len('<tbody id="aRows">'); k = s.index('</tbody>', i)
s = s[:i] + '\n' + hd('Con PASO') + '<tr>' + c(a['paso'], 0) + c(a['gen'], 1) + c(a['bal'], 0) + '</tr>\n' + hd('Sin PASO') + '<tr><td class="g" style="text-align:center">—</td>' + c(a['sin'], 1) + c(a['bal'], 0) + '</tr>\n' + s[k:]
s = re.sub(r'var PD=\{.*?\};var PDE=', lambda m: 'var PD=' + json.dumps(A['proyectado'], separators=(',', ':')) + ';var PDE=', s, count=1, flags=re.S)
s = re.sub(r'var PDE=\{.*?\};var st=', lambda m: 'var PDE=' + json.dumps(A['proyectado_eco'], separators=(',', ':')) + ';var st=', s, count=1, flags=re.S)
s = re.sub(r'"2027 P \(proy\.\)":\{"reg":\{.*?\},"nac":\[[^\]]*\]\}', lambda m: '"2027 P (proy.)":' + json.dumps(A['mapa2027'], separators=(',', ':')).replace('NaN', 'null'), s, count=1, flags=re.S)
(RAIZ / 'index.html').write_text(s)
print('respaldo actualizado')
