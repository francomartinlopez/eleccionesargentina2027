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
s = re.sub(r'var ACT=\{.*?\};var COMP=', lambda m: 'var ACT=' + json.dumps(A['actual'], separators=(',', ':')) + ';var COMP=', s, count=1, flags=re.S)

def lectura(a):
    g, si, b = a['gen'], a['sin'], a['bal']
    def pv(r, q):
        if r[1] >= 45: return q + 'todo el rango supera el 45 %: el oficialismo ganaría en primera vuelta. '
        if r[1] >= 40: return q + 'todo el rango supera el 40 %: el oficialismo ganaría en primera vuelta si le saca más de 10 puntos al segundo' + (', o sin condiciones en la parte alta, por encima del 45 %. ' if r[2] >= 45 else '. ')
        if r[2] >= 40: return q + 'el rango cruza el 40 %: iría a balotaje salvo en la parte alta, y aun ahí necesitaría 10 puntos de ventaja. '
        return q + 'todo el rango queda debajo del 40 %: iría a balotaje. '
    t = pv(g, 'con PASO, ') + pv(si, 'Sin PASO, ')
    if b[2] < 50: t += 'En los dos casos, un balotaje hoy lo perdería' + (' por poco' if b[2] >= 48 else '') + ': todo el rango queda debajo del 50 %.'
    elif b[1] >= 50: t += 'En los dos casos, un balotaje hoy lo ganaría: todo el rango supera el 50 %.'
    else: t += 'En los dos casos, un balotaje hoy quedaría abierto: el rango cruza el 50 %.'
    return t
s = re.sub(r'(<li id="aLectura"><strong>Lectura:</strong> )[^<]*(</li>)', lambda m: m.group(1) + lectura(A['actual']) + m.group(2), s, count=1)
(RAIZ / 'index.html').write_text(s)
print('respaldo actualizado')
