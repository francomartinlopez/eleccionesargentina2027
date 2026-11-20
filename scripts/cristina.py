"""Cristina Kirchner candidata: sensibilidad (paso 4 de los cambios acordados el 19-11-2026).

Supone que pudiera ser candidata (hoy está inhabilitada por la condena firme en la causa
Vialidad). Kicillof y Massa van con ella; el peronismo federal se suma (retiene el 60 %)
o va solo; nadie más se alía. Se combina con las opciones de PRO, centro y CC (Bullrich
la agrega scripts/bullrich.py, que se corre después). Las variantes llevan "cr" con la
intensidad del rechazo y quedan fuera del recuento y de los botones de mejor y peor camino.

Orden si se rehace todo: kicillof_massa.py, cristina.py, bullrich.py, recuento.py, excel_km.py.

Rechazo (un solo parámetro, en puntos del padrón): diferencia de imagen negativa entre
Cristina Kirchner y Kicillof en encuestas nacionales de 2026 (AtlasIntel abril 53/49,
OPSA-UBA agosto 58/54, Giacobbe 52,9/52,9, Pulso Research octubre 51,3/49,1, otra de
agosto 52,8/50,4 y otra de julio 51,1/49): 2,5 puntos en promedio. Leve 1, media 2,5,
fuerte 5.
- General: la lista de Cristina pierde ese voto (pasado a votos afirmativos): 40 % a LLA,
  30 % a la tercera fuerza (si no hay, a LLA) y 30 % a la abstención; recupera el 20 % de
  esa pérdida por movilización del voto kirchnerista duro.
- Peronismo federal con Cristina: retiene el 60 %; la fuga va 58 % a LLA y 42 % a la
  abstención (la misma regla que con Kicillof).
- PASO: cada lista cambia en la misma proporción que en la general (hereda los cocientes).
- Balotaje: de lo que PRO, centro, CC y peronismo federal transferían al rival, se corre
  12 % por punto de rechazo (12, 30 y 60 %), mitad a LLA y mitad a la abstención.
"""
import json, re
from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / 'datos' / 'comp.js'
REF_P, REF_G, REF_B = 33.6, 39.0, 55.4
INT = {'leve': 1.0, 'media': 2.5, 'fuerte': 5.0}
PF_RET = 0.60
FUGA_PF = (0.35 / 0.60, 0.25 / 0.60)
DEST = (0.40, 0.30, 0.30)          # LLA, tercera fuerza, abstención
MOVIL = 0.20
K_BAL = 0.12
TR = {'pro': (.75, .05, .20), 'ce': (.45, .20, .35), 'pf': (.35, .40, .25),
      'cc': (.25, .30, .45), 'iz': (0, .35, .65), 'k': (.05, .40, .55)}
PIEZA = {'PRO': 'pro', 'peronismo federal': 'pf', 'Peronismo federal': 'pf', 'centro': 'ce',
         'Centro': 'ce', 'Centro (UCR y gobernadores)': 'ce', 'CC': 'cc', 'Kirchnerismo': 'k',
         'Izquierda': 'iz', 'Cristina': 'k'}


def comp(n):
    if n == 'Peronismo unido':
        return ['k', 'pf']
    return [PIEZA[x] for x in n.split(' + ')]


def tercera(n):
    cs = comp(n)
    return 'k' not in cs and 'iz' not in cs and cs != ['pf']


def balotaje(L, ll, k=0.0):
    tot = {n: sum(v.values()) for n, v in L.items()}
    riv = max(tot, key=tot.get)
    a, b = ll, tot[riv]
    for n, v in L.items():
        if n == riv: continue
        for c, x in v.items():
            tl, tr, _ = TR[c]
            if k and c in ('pro', 'ce', 'cc', 'pf'):
                tl += tr * k / 2; tr *= 1 - k
            a += x * tl; b += x * tr
    return 100 * a / (a + b), riv


def listas(c, idx, col):
    out = {}
    for o in c['O']:
        n, v = o[0], o[col]
        if n == 'Peronismo unido':
            s = idx[(c['pro'], c['ce'], c['cc'], 'solo')]
            k = next(x[col] for x in s['O'] if x[0] == 'Kirchnerismo')
            p = next(x[col] for x in s['O'] if x[0] == 'Peronismo federal')
            out[n] = {'k': v * k / (k + p), 'pf': v * p / (k + p)}
        else:
            cs = comp(n)
            out[n] = {x: v / len(cs) for x in cs}
    return out


def variante(c, idx, gap):
    L = listas(c, idx, 2)
    afirm = (100 - c['G']['bl'] - c['G']['nu'] - c['G']['ab']) / 100
    ll = c['G']['ll']; abst = 0.0
    kn = 'Peronismo unido' if 'Peronismo unido' in L else 'Kirchnerismo'
    blk = L.pop(kn)
    cr = {'k': blk['k']}
    if 'pf' in blk:
        f = blk['pf'] * (1 - PF_RET)
        cr['pf'] = blk['pf'] - f
        ll += f * FUGA_PF[0]; abst += f * FUGA_PF[1]
    nom = 'Cristina + peronismo federal' if 'pf' in cr else 'Cristina'
    perd = min(gap / afirm, 0.5 * sum(cr.values()))
    neto = perd * (1 - MOVIL)
    fac = 1 - neto / sum(cr.values())
    cr = {x: v * fac for x, v in cr.items()}
    ter = [n for n in L if tercera(n)]
    ll += perd * DEST[0]
    if ter:
        tt = sum(sum(L[n].values()) for n in ter)
        for n in ter:
            w = sum(L[n].values()) / tt
            L[n] = {x: v * (1 + perd * DEST[1] * w / sum(L[n].values())) for x, v in L[n].items()}
    else:
        ll += perd * DEST[1]
    abst += perd * DEST[2] - perd * MOVIL
    nuevas = {nom: cr}
    nuevas.update(L)
    tot = ll + sum(sum(v.values()) for v in nuevas.values())
    esc = 100 / tot
    nuevas = {n: {x: v * esc for x, v in d.items()} for n, d in nuevas.items()}
    return nuevas, ll * esc, abst * esc, kn, nom, afirm


def armar(base):
    idx = {(c['pro'], c['ce'], c['cc'], c['pf']): c for c in base}
    out = []
    for c in base:
        if c['pf'] not in ('solo', 'k'):
            continue
        for niv, gap in INT.items():
            Lg, llg, ab, kn, nom, afirm = variante(c, idx, gap)
            # PASO: misma proporción que en la general
            gen0 = {o[0]: o[2] for o in c['O']}
            pas0 = {o[0]: o[1] for o in c['O']}
            pas = {}
            for n, d in Lg.items():
                src = kn if n == nom else n
                pas[n] = pas0[src] * sum(d.values()) / gen0[src]
            llp = c['P']['ll'] * llg / c['G']['ll']
            t = llp + sum(pas.values())
            pas = {n: v * 100 / t for n, v in pas.items()}; llp *= 100 / t
            b0, _ = balotaje(listas(c, idx, 2), c['G']['ll'])
            b1, riv = balotaje(Lg, llg, K_BAL * gap)
            orden = sorted(Lg, key=lambda n: (n == 'Izquierda', -sum(Lg[n].values())))
            O = [[n, round(pas[n], 1), round(sum(Lg[n].values()), 1), int(n == riv)] for n in orden]
            G = dict(c['G']); P = dict(c['P'])
            G['ll'] = round(llg, 1); P['ll'] = round(llp, 1)
            G['ab'] = round(G['ab'] + ab * afirm, 1)
            P['ab'] = round(P['ab'] + ab * (100 - P['bl'] - P['nu'] - P['ab']) / 100, 1)
            n = {'t': c['t'], 's': c['s'], 'f': c['f'], 'pro': c['pro'], 'ce': c['ce'], 'cc': c['cc'],
                 'pf': 'cfk' if c['pf'] == 'k' else 'solo', 'kic': 'cfk', 'mas': 'cfk', 'cr': niv,
                 'dp': round(llp - REF_P, 1), 'dg': round(llg - REF_G, 1),
                 'db': round(c['db'] + b1 - b0, 1), 'O': O, 'G': G, 'P': P, 'B': dict(c['B'])}
            out.append(n)
    for i, n in enumerate(out, 1):
        n['cid'] = 'CR%d' % i
    return out


if __name__ == '__main__':
    s = HTML.read_text(encoding='utf-8')
    m = re.search(r'var COMP=(\[.*?\]);\n', s)
    C = [c for c in json.loads(m.group(1)) if 'cr' not in c and 'bid' not in c]
    base = [c for c in C if 'km' not in c]
    nuevos = armar(base)
    todo = C + nuevos
    s = s[:m.start(1)] + json.dumps(todo, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
    HTML.write_text(s, encoding='utf-8')
    print(len(nuevos), 'variantes con Cristina;', len(todo), 'sin las de Bullrich: correr bullrich.py')
