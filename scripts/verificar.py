"""Controles automáticos del sitio. Sale con error si algo no cuadra.

Comprueba que las composiciones de datos/comp.js sean coherentes, que las cifras del recuento
que se citan en index.html coincidan con las que salen de los datos, que datos/provincias.js
esté completo y que index.html no tenga ids repetidos. Lo corren las acciones de GitHub.
"""
import json, re, sys
from collections import Counter
from datetime import date
from pathlib import Path

R = Path(__file__).resolve().parents[1]
errores = []
def falla(m): errores.append(m)

# composiciones
s = (R / 'datos/comp.js').read_text(encoding='utf-8')
C = json.loads(re.search(r'var COMP=(\[.*?\]);\n', s).group(1))
F = ['pro', 'ce', 'cc', 'pf', 'kic', 'mas', 'bu', 'cr']
claves = Counter('|'.join(str(c.get(k, {'kic': 'k', 'mas': 'k', 'bu': 'lla', 'cr': 'no'}.get(k))) for k in F) for c in C)
rep = [k for k, n in claves.items() if n > 1]
if rep: falla('composiciones repetidas: %d' % len(rep))
for c in C:
    tot = c['G']['ll'] + sum(o[2] for o in c['O'])
    if abs(tot - 100) > 0.3: falla('la general no suma 100 en %s %s (%.1f)' % (c['t'], c['s'], tot))
    if sum(o[3] for o in c['O']) != 1: falla('sin rival único de balotaje en %s %s' % (c['t'], c['s']))
    if any(o[1] < 0 or o[2] < 0 for o in c['O']): falla('valores negativos en %s %s' % (c['t'], c['s']))

# recuento de 170 casos y cifras citadas en la página
P = [c for c in C if c.get('p')]
def fam(n):
    t = n.lower()
    return 'k' if any(w in t for w in ('kirchner', 'peronismo unido', 'kicillof', 'k duro')) else 'o'
res = []
for c in P:
    g = c['G']['ll']; L = sorted([('LLA', g)] + [(o[0], o[2]) for o in c['O']], key=lambda x: -x[1])
    prim = L[0][1] >= 45 or (L[0][1] >= 40 and L[0][1] - L[1][1] >= 10)
    res.append(dict(first=L[0][0], prim=prim, bal=round(55.4 + c['db'], 1), pro=c['pro']))
bl = [x for x in res if not x['prim']]
cifras = {
    'casos': len(P), 'balotaje': len(bl), 'gana': sum(x['bal'] > 50 for x in bl), 'empata': sum(x['bal'] == 50 for x in bl),
    'pierde': sum(x['bal'] < 50 for x in bl), 'primera': sum(x['first'] == 'LLA' for x in res),
    'kprim': Counter(x['first'] for x in res if x['first'] != 'LLA' and fam(x['first']) == 'k'),
    'juntos': (sum(x['prim'] for x in res if x['pro'] == 'lla'), sum(x['pro'] == 'lla' for x in res)),
    'separados': (sum(x['prim'] for x in res if x['pro'] != 'lla'), sum(x['pro'] != 'lla' for x in res)),
}
h = (R / 'index.html').read_text(encoding='utf-8')
txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h))
k = cifras['kprim']
esperado = [
    '%d de %d casos' % (cifras['balotaje'], cifras['casos']),
    '%d de %d, con transferencias' % (cifras['gana'], cifras['balotaje']),
    'ganaría %d de esos %d, perdería %d y empataría %d' % (cifras['gana'], cifras['balotaje'], cifras['pierde'], cifras['empata']),
    'llega primera en %d' % cifras['primera'],
    '%d con el peronismo unido, %d con el kirchnerismo solo y %d con Kicillof + Massa + peronismo federal' % (k['Peronismo unido'], k['Kirchnerismo'], k['Kicillof + Massa + peronismo federal']),
    '%d de %d balotajes que perdería LLA' % (cifras['pierde'], cifras['balotaje']),
    '%d de %d gana LLA en primera vuelta si va junto al PRO; separados, %d de %d' % (cifras['juntos'] + cifras['separados']),
]
for e in esperado:
    if e not in txt: falla('la página no dice "%s" (cifra calculada con datos/comp.js)' % e)

# provincias
p = (R / 'datos/provincias.js').read_text(encoding='utf-8')
D = json.loads(p[p.index('window.PROV_DATA = ') + 19:].rstrip().rstrip(';'))
for v in D['provincias']:
    n = v['n']
    try: date.fromisoformat(v['fecha'])
    except Exception: falla('fecha inválida en %s' % n)
    if v['estado'] not in 'cae': falla('estado inválido en %s' % n)
    if v['esperado'] not in ('of', 'amb', 'op'): falla('esperado inválido en %s' % n)
    pr = v.get('prob')
    if not pr or sum(pr.values()) != 100: falla('probabilidades que no suman 100 en %s' % n)
    elif max(pr, key=pr.get) != v['esperado']: falla('el resultado más probable de %s no coincide con sus probabilidades' % n)
    if 'real' in v and not all(x in v['real'] for x in ('res', 'ganador', 'pct', 'margen', 'fecha', 'fuente')): falla('resultado real incompleto en %s' % n)
for z in ('ba', 'caba'):
    if sum(D[z]['prob'].values()) != 100: falla('probabilidades de %s que no suman 100' % z)

# opciones del cuadro (outsiders, vice, candidatos) y lo confirmado
o = (R / 'datos/opciones.js').read_text(encoding='utf-8')
def num(x):
    a, _, b = x.partition('/')
    return float(a) / float(b) if b else float(a)
for g in re.findall(r'\b(?:de|a): \{([^}]*)\}', o):
    tot = sum(num(x) for x in re.findall(r':\s*([0-9.]+(?:/[0-9]+)?)', g))
    if abs(tot - 1) > 0.01: falla('reparto que no suma 100 %% en datos/opciones.js: {%s}' % g)
for nombre, v in re.findall(r"n: '([^']+)', v: ([0-9.]+)", o):
    if '%s %s' % (nombre, v.replace('.', ',')) not in h: falla('el valor de %s (%s) no coincide con Metodología' % (nombre, v))
cf = (R / 'datos/confirmados.js').read_text(encoding='utf-8')
for clave, cuerpo in re.findall(r"'([a-z.]+)': \{(v: .*?)\}", cf):
    for campo in ('fuente:', 'url:', 'cargado:'):
        if campo not in cuerpo: falla('al dato confirmado %s le falta %s' % (clave, campo[:-1]))

# página
ids = re.findall(r'\sid="([^"]+)"', h)
dup = [i for i, n in Counter(ids).items() if n > 1]
if dup: falla('ids repetidos en index.html: %s' % dup)
if len(re.findall(r'<h1[\s>]', h)) != 1: falla('index.html debe tener un solo <h1>')
if 'cdnjs' in h or 'fonts.googleapis' in (R / 'css/estilo.css').read_text(): falla('recursos externos en la página')
A = json.loads((R / 'datos/actual.json').read_text())
for kk in ('mes', 'actual', 'proyectado', 'proyectado_eco', 'actualizado'):
    if kk not in A: falla('falta %s en datos/actual.json' % kk)

if errores:
    print('\n'.join('ERROR: ' + e for e in errores)); sys.exit(1)
print('Todo en orden:', cifras['casos'], 'casos,', cifras['balotaje'], 'balotajes,', len(D['provincias']), 'provincias.')
