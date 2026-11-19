"""Bullrich candidata del PRO (paso 2 de los cambios acordados el 19-11-2026).

Agrega a `var COMP` (index.html) una variante con Bullrich como candidata del PRO por
cada composición con el PRO fuera de LLA y presentándose (las 124 de las tablas y las
variantes de Kicillof y Massa, incluida Massa con el PRO). Con LLA ya está contado.

Orden si se rehace todo: scripts/kicillof_massa.py, después este, después
scripts/excel_km.py. Volver a correr este reemplaza sus variantes anteriores.

Supuesto acordado: el PRO retiene unos 10 puntos más de su bloque, unos 4 puntos de
los votos afirmativos que deja de sacar LLA en la general. En la PASO se pasa la misma
proporción del voto de la lista del PRO (4 puntos × PASO/general de esa lista).
Balotaje: si la lista del PRO queda afuera, esos votos se transfieren con la regla del
PRO (75 % LLA, 5 % rival, 20 % abstención); se recalcula con las mismas transferencias
que el paso 1 y se suma la diferencia.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'index.html'
PTS = 4.0
REF_P, REF_G = 33.6, 39.0
TR = {'pro': (.75, .05, .20), 'ce': (.45, .20, .35), 'pf': (.35, .40, .25),
      'cc': (.25, .30, .45), 'iz': (0, .35, .65), 'k': (0, .80, .20),
      'kic': (0, .80, .20), 'kd': (0, .80, .20), 'mas': (.30, .45, .25)}
PIEZA = {'PRO': 'pro', 'Kicillof': 'kic', 'K duro': 'kd', 'Massa': 'mas', 'peronismo federal': 'pf',
         'Peronismo federal': 'pf', 'centro': 'ce', 'Centro': 'ce', 'Centro (UCR y gobernadores)': 'ce',
         'CC': 'cc', 'Kirchnerismo': 'k', 'Izquierda': 'iz'}


def comp(n):
    if n == 'Peronismo unido':
        return ['k', 'pf']
    return [PIEZA[x] for x in n.split(' + ')]


def balotaje(O, ll, extra=None):
    """O: [[nombre, votos]]; extra: (nombre, votos de PRO agregados)."""
    L = {}
    for n, v in O:
        cs = comp(n)
        L[n] = {k: v / len(cs) for k in cs}
    if extra:
        L[extra[0]] = dict(L[extra[0]])
        L[extra[0]]['pro'] = L[extra[0]].get('pro', 0) + extra[1]
    tot = {n: sum(v.values()) for n, v in L.items()}
    riv = max(tot, key=tot.get)
    a, b = ll, tot[riv]
    for n, v in L.items():
        if n == riv: continue
        for k, x in v.items():
            a += x * TR[k][0]; b += x * TR[k][1]
    return 100 * a / (a + b), riv


def main():
    s = HTML.read_text(encoding='utf-8')
    m = re.search(r'var COMP=(\[.*?\]);\n', s)
    C = [c for c in json.loads(m.group(1)) if 'bid' not in c]
    nuevos = []
    for c in C:
        if c['pro'] in ('lla', 'no'): continue
        pl = next(o for o in c['O'] if o[0].startswith('PRO'))
        dg = PTS
        dp = PTS * pl[1] / pl[2]
        O = [list(o) for o in c['O']]
        for o in O:
            if o[0] == pl[0]:
                o[1] = round(o[1] + dp, 1); o[2] = round(o[2] + dg, 1)
        b0, _ = balotaje([[o[0], o[2]] for o in c['O']], c['G']['ll'])
        b1, riv = balotaje([[o[0], o[2]] for o in c['O']], c['G']['ll'] - dg, (pl[0], dg))
        for o in O:
            o[3] = int(o[0] == riv)
        O.sort(key=lambda o: (o[0] == 'Izquierda', -o[2]))
        G = dict(c['G']); P = dict(c['P'])
        G['ll'] = round(G['ll'] - dg, 1); P['ll'] = round(P['ll'] - dp, 1)
        n = dict(c)
        n.update({'bu': 'pro', 'O': O, 'G': G, 'P': P, 'dg': round(G['ll'] - REF_G, 1),
                  'dp': round(P['ll'] - REF_P, 1), 'db': round(c['db'] + b1 - b0, 1)})
        nuevos.append(n)
    for i, n in enumerate(nuevos, 1):
        n['bid'] = 'BU%d' % i
    todo = C + nuevos
    txt = json.dumps(todo, ensure_ascii=False, separators=(',', ':'))
    HTML.write_text(s[:m.start(1)] + txt + s[m.end(1):], encoding='utf-8')
    print(len(C), 'de partida,', len(nuevos), 'con Bullrich;', len(todo), 'en total')


if __name__ == '__main__':
    main()
