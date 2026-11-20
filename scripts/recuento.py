"""Marca en `var COMP` los casos del recuento ("p":1) y muestra sus cifras.

Recuento (opción 2, acordada el 19-11-2026): las 44 composiciones de las Tablas A a L
(sin las inerciales) con tres arreglos de Kicillof y Massa (todos juntos; Kicillof se
separa con Massa y el kirchnerismo duro va aparte; Kicillof + Massa + peronismo federal)
y, donde el PRO va fuera de LLA, con Bullrich en LLA o como candidata del PRO.
Las demás combinaciones (Tabla M, Massa solo o con el PRO, etc.) solo dan rango.
Correr al final: después de kicillof_massa.py y bullrich.py.
"""
import json, re
from collections import Counter
from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / 'datos' / 'comp.js'
PROB = [('k', 'k'), ('solo', 'kic'), ('pf', 'kic_pf')]


def prob(c):
    return c['t'] != 'M' and (c.get('kic', 'k'), c.get('mas', 'k')) in PROB


def res(c):
    g = c['G']['ll']
    L = sorted([('LLA', g)] + [(o[0], o[2]) for o in c['O']], key=lambda x: -x[1])
    p, s = L[0], L[1]
    bal = 55.4 + c['db']
    riv = next(o[0] for o in c['O'] if o[3])
    prim = p[1] >= 45 or (p[1] >= 40 and p[1] - s[1] >= 10)
    if prim:
        return dict(prim=True, win=p[0], first=p[0], g=g)
    return dict(prim=False, win='LLA' if bal > 50 else riv, first=p[0], riv=riv, bal=bal, g=g)


def fam(n):
    t = n.lower()
    if n == 'LLA': return 'LLA'
    if any(w in t for w in ('kirchner', 'peronismo unido', 'kicillof', 'k duro')): return 'kirchnerismo'
    return 'otra'


if __name__ == '__main__':
    s = HTML.read_text(encoding='utf-8')
    m = re.search(r'var COMP=(\[.*?\]);\n', s)
    C = json.loads(m.group(1))
    for c in C:
        c.pop('p', None)
        if prob(c): c['p'] = 1
    HTML.write_text(s[:m.start(1)] + json.dumps(C, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):], encoding='utf-8')
    R = [c for c in C if 'p' in c]
    X = [res(c) for c in R]
    bl = [x for x in X if not x['prim']]
    print('casos', len(R), '| balotaje', len(bl), '| LLA gana balotaje', sum(x['win'] == 'LLA' for x in bl))
    print('sin balotaje', sum(x['prim'] for x in X), 'ganados por LLA', sum(x['prim'] and x['win'] == 'LLA' for x in X))
    print('primero', Counter(fam(x['first']) for x in X), '| frentes kirchneristas primeros:', Counter(x['first'] for x in X if fam(x['first']) == 'kirchnerismo'))
    print('balotajes: LLA gana', sum(x['win'] == 'LLA' and x['bal'] > 50 for x in bl), '| empates en 50,0:', sum(round(x['bal'], 1) == 50.0 for x in bl),
          '| pierde', sum(round(x['bal'], 1) < 50.0 for x in bl), '| definidos por 1 punto o menos:', sum(abs(x['bal'] - 50) <= 1.0 for x in bl))
    print('rival', Counter(fam(x['riv']) for x in bl), '| pierde contra', Counter(x['win'] for x in bl if x['win'] != 'LLA'))
    print('juntos sin balotaje', sum(x['prim'] for c, x in zip(R, X) if c['pro'] == 'lla'), 'de', sum(c['pro'] == 'lla' for c in R),
          '| separados', sum(x['prim'] for c, x in zip(R, X) if c['pro'] != 'lla'), 'de', sum(c['pro'] != 'lla' for c in R))
    T = [c for c in C if 'cr' not in c]
    print('rango sin Cristina', len(T), ': LLA general', min(c['G']['ll'] for c in T), '-', max(c['G']['ll'] for c in T),
          '| balotaje', round(min(55.4 + c['db'] for c in T), 1), '-', round(max(55.4 + c['db'] for c in T), 1))
    # sensibilidad: Cristina candidata sobre las composiciones centrales (sin Tabla M)
    for niv in ('leve', 'media', 'fuerte'):
        S = [c for c in C if c.get('cr') == niv and c['t'] != 'M']
        Y = [res(c) for c in S]
        b = [y for y in Y if not y['prim']]
        print('Cristina', niv, len(S), '| sin balotaje', sum(y['prim'] for y in Y), '| LLA primera', sum(y['first'] == 'LLA' for y in Y),
              '| LLA gana balotaje', sum(y['win'] == 'LLA' for y in b), 'de', len(b),
              '| bal LLA', round(min(y['bal'] for y in b), 1), '-', round(max(y['bal'] for y in b), 1))
