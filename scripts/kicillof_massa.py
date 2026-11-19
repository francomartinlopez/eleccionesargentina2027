"""Combinaciones con Kicillof y Massa (paso 1 de los cambios acordados el 19-11-2026).

Parte de las 124 composiciones del bloque 3 (`var COMP` en index.html, las que no
tienen `km`) y agrega las variantes en que Kicillof y Massa se separan del
kirchnerismo. Escribe la lista completa de vuelta en index.html.

Uso: python3 scripts/kicillof_massa.py [--solo-mostrar]

Supuestos (acordados con Franco, salvo los marcados "propio"):
- Voto kirchnerista: Kicillof 2/3, Massa 12 %, kirchnerismo duro el resto.
- Al dividirse el kirchnerismo pierde el 7 % de su voto (a la abstención y el blanco).
- Kicillof con el peronismo federal: el peronismo federal retiene el 85 %. La fuga
  sigue la regla de las tablas para el peronismo federal (35 % LLA, 40 % kirchnerismo,
  25 % abstención) sin el kirchnerismo, que no la recibe porque el frente es el suyo:
  58 % LLA, 42 % abstención (propio, sobre la regla de las tablas).
- Massa con el PRO: el PRO pierde el 20 %, que va como cuando el PRO no se presenta
  (75 % LLA, 5 % a la lista de Kicillof, 20 % abstención).
- Massa con el peronismo federal, con Kicillof o con los dos: sin fugas (propio).
- Kirchnerismo duro con el peronismo federal (Kicillof solo): el peronismo federal
  conserva su parte del peronismo unido (propio).
- Balotaje: se recalcula con transferencias (las de las tablas para PRO, centro,
  peronismo federal, CC e izquierda; kirchnerismo, Kicillof y kirchnerismo duro 0/80/20;
  Massa 30/45/25, propio) y se suma la diferencia con la composición de partida.
  Igual para la PASO y la general: diferencia sobre la composición de partida.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'index.html'

REF_P, REF_G, REF_B = 33.6, 39.0, 55.4   # Tabla A, 2027 B (referencia del bloque)
KIC, MAS = 2 / 3, 0.12
PERD_K = 0.07
PF_RET_KIC = 0.85
PRO_PERD_MAS = 0.20
FUGA_PF_KIC = (0.35 / 0.60, 0.25 / 0.60)        # LLA, abstención
FUGA_PRO = (0.75, 0.05, 0.20)                   # LLA, Kicillof, abstención
# transferencias en el balotaje: (LLA, rival, abstención)
TR = {'pro': (.75, .05, .20), 'ce': (.45, .20, .35), 'pf': (.35, .40, .25),
      'cc': (.25, .30, .45), 'iz': (0, .35, .65), 'k': (0, .80, .20),
      'kic': (0, .80, .20), 'kd': (0, .80, .20), 'mas': (.30, .45, .25)}

COMPS = {'Kirchnerismo': ['k'], 'Peronismo unido': ['k', 'pf'], 'Peronismo federal': ['pf'],
         'PRO': ['pro'], 'CC': ['cc'], 'Centro (UCR y gobernadores)': ['ce'], 'Izquierda': ['iz'],
         'CC + centro': ['cc', 'ce'], 'PRO + CC': ['pro', 'cc'], 'PRO + centro': ['pro', 'ce'],
         'PRO + CC + centro': ['pro', 'cc', 'ce'], 'Centro + peronismo federal': ['ce', 'pf'],
         'PRO + peronismo federal': ['pro', 'pf'], 'PRO + centro + peronismo federal': ['pro', 'ce', 'pf']}


def leer():
    s = HTML.read_text(encoding='utf-8')
    m = re.search(r'var COMP=(\[.*?\]);\n', s)
    return s, m, json.loads(m.group(1))


def descomponer(c, idx, col):
    """Listas de c (col 1 = PASO, 2 = general) como {nombre: {componente: votos}}."""
    out = {}
    for o in c['O']:
        n, v = o[0], o[col]
        cs = COMPS[n]
        if n == 'Peronismo unido':
            s = idx[(c['pro'], c['ce'], c['cc'], 'solo')]
            k = next(x[col] for x in s['O'] if x[0] == 'Kirchnerismo')
            p = next(x[col] for x in s['O'] if x[0] == 'Peronismo federal')
            out[n] = {'k': v * k / (k + p), 'pf': v * p / (k + p)}
        elif n == 'PRO + peronismo federal':
            s = idx[('solo', c['ce'], c['cc'], 'solo')]
            a = next(x[col] for x in s['O'] if x[0] == 'PRO')
            p = next(x[col] for x in s['O'] if x[0] == 'Peronismo federal')
            out[n] = {'pro': v * a / (a + p), 'pf': v * p / (a + p)}
        else:
            out[n] = {k: v / len(cs) for k in cs}
    return out


def nombre(comp):
    ks = set(comp)
    if ks <= {'kic', 'kd', 'mas', 'k', 'pf'} and 'pf' in ks and ks & {'k', 'kd'} and 'kic' in ks:
        return 'Peronismo unido'
    if ks == {'kic', 'kd'}:
        return 'Kirchnerismo'
    partes = []
    if 'pro' in ks: partes.append('PRO')
    if 'kic' in ks: partes.append('Kicillof')
    if 'kd' in ks: partes.append('K duro')
    if 'mas' in ks and 'pro' not in ks: partes.append('Massa')
    if 'pf' in ks: partes.append('peronismo federal')
    if 'mas' in ks and 'pro' in ks: partes.append('Massa')
    n = ' + '.join(partes)
    return n[0].upper() + n[1:]


def variante(L, ll, c, kic, mas):
    """Aplica la separación sobre las listas L (una columna). Devuelve listas, LLA, pérdida."""
    L = {n: dict(v) for n, v in L.items()}
    kn = 'Peronismo unido' if 'Peronismo unido' in L else 'Kirchnerismo'
    kblk = L.pop(kn)
    K = kblk.get('k', 0)
    pfu = kblk.get('pf')                    # peronismo federal dentro del peronismo unido
    perd = PERD_K * K
    K *= 1 - PERD_K
    piezas = {'kic': K * KIC, 'mas': K * MAS, 'kd': K * (1 - KIC - MAS)}
    # listas del espacio kirchnerista
    grupos = {'kic': {'kic'}, 'kd': {'kd'}}
    if kic == 'k':
        grupos = {'kic': {'kic', 'kd'}}
    elif kic == 'pf':
        grupos['kic'].add('pf')
    if mas == 'k':
        (grupos['kd'] if 'kd' in grupos else grupos['kic']).add('mas')
    elif mas in ('kic', 'kic_pf'):
        grupos['kic'].add('mas')
    if pfu is not None and kic != 'pf':     # peronismo federal con el kirchnerismo (duro)
        (grupos['kd'] if 'kd' in grupos else grupos['kic']).add('pf')
    pfv = pfu
    if pfv is None and 'Peronismo federal' in L and (kic == 'pf' or mas == 'pf'):
        pfv = L.pop('Peronismo federal')['pf']
    lla = ll
    nuevas = {}
    for g, comp in grupos.items():
        d = {}
        for x in comp:
            if x == 'pf':
                v = pfv
                if kic == 'pf' and g == 'kic':
                    f = v * (1 - PF_RET_KIC); v -= f
                    lla += f * FUGA_PF_KIC[0]; perd += f * FUGA_PF_KIC[1]
                d['pf'] = v
            else:
                d[x] = piezas[x]
        nuevas[nombre(d)] = d
    if mas == 'solo':
        nuevas['Massa'] = {'mas': piezas['mas']}
    elif mas == 'pf':
        nuevas['Massa + peronismo federal'] = {'mas': piezas['mas'], 'pf': pfv}
    elif mas in ('pro', 'pro_pf'):
        pn = 'PRO' if mas == 'pro' else 'PRO + peronismo federal'
        d = L.pop(pn)
        f = d['pro'] * PRO_PERD_MAS
        d['pro'] -= f
        lla += f * FUGA_PRO[0]; perd += f * FUGA_PRO[2]
        kl = next(n for n, v in nuevas.items() if 'kic' in v)
        nuevas[kl]['kic'] += f * FUGA_PRO[1]
        d['mas'] = piezas['mas']
        nuevas[nombre(d)] = d
    out = dict(nuevas)
    out.update(L)
    tot = lla + sum(sum(v.values()) for v in out.values())
    esc = 100 / tot
    out = {n: {k: x * esc for k, x in v.items()} for n, v in out.items()}
    return out, lla * esc, perd * esc


def balotaje(L, ll):
    """% de LLA en el balotaje con transferencias simples, contra la lista más votada."""
    tot = {n: sum(v.values()) for n, v in L.items()}
    riv = max(tot, key=tot.get)
    a, b = ll, tot[riv]
    for n, v in L.items():
        if n == riv: continue
        for k, x in v.items():
            a += x * TR[k][0]; b += x * TR[k][1]
    return 100 * a / (a + b), riv


def armar(base):
    idx = {(c['pro'], c['ce'], c['cc'], c['pf']): c for c in base}
    nuevos = []
    opciones = []
    for kic in ('k', 'solo', 'pf'):
        for mas in ('k', 'solo', 'pf', 'kic', 'kic_pf', 'pro', 'pro_pf'):
            if kic == 'k' and mas == 'k': continue
            if mas == 'kic' and kic != 'solo': continue
            if mas == 'kic_pf' and kic != 'pf': continue
            if mas == 'pf' and kic == 'pf': continue
            if mas == 'pro_pf' and kic == 'pf': continue
            opciones.append((kic, mas))
    for c in base:
        for kic, mas in opciones:
            if kic == 'pf' and c['pf'] != 'k': continue
            if mas == 'pf' and c['pf'] != 'solo': continue
            if mas == 'pro' and c['pro'] != 'solo': continue
            if mas == 'pro_pf' and c['pro'] != 'pf': continue
            if c['pf'] == 'k' and kic == 'k' and mas == 'pf': continue
            res = {}
            for col, key in ((1, 'P'), (2, 'G')):
                L = descomponer(c, idx, col)
                res[key] = variante(L, c[key]['ll'], c, kic, mas)
            Lg, llg, pg = res['G']
            Lp, llp, pp = res['P']
            b0, _ = balotaje(descomponer(c, idx, 2), c['G']['ll'])
            b1, riv = balotaje(Lg, llg)
            bal = REF_B + c['db'] + (b1 - b0)
            pfn = c['pf']
            if kic == 'pf': pfn = 'kic'
            elif mas == 'pf': pfn = 'mas'
            orden = sorted(Lg, key=lambda n: (n == 'Izquierda', -sum(Lg[n].values())))
            O = [[n, round(sum(Lp[n].values()), 1), round(sum(Lg[n].values()), 1), int(n == riv)] for n in orden]
            G = dict(c['G']); P = dict(c['P'])
            G['ll'] = round(llg, 1); P['ll'] = round(llp, 1)
            G['ab'] = round(G['ab'] + pg * (100 - c['G']['bl'] - c['G']['nu'] - c['G']['ab']) / 100, 1)
            P['ab'] = round(P['ab'] + pp * (100 - c['P']['bl'] - c['P']['nu'] - c['P']['ab']) / 100, 1)
            n = {'t': c['t'], 's': c['s'], 'f': c['f'], 'pro': c['pro'], 'ce': c['ce'], 'cc': c['cc'], 'pf': pfn,
                 'kic': kic, 'mas': mas, 'dp': round(llp - REF_P, 1), 'dg': round(llg - REF_G, 1),
                 'db': round(bal - REF_B, 1), 'O': O, 'G': G, 'P': P, 'B': dict(c['B'])}
            nuevos.append(n)
    for i, n in enumerate(nuevos, 1):
        n['km'] = 'KM%d' % i
    return nuevos


if __name__ == '__main__':
    s, m, C = leer()
    base = [c for c in C if 'km' not in c]
    nuevos = armar(base)
    print(len(base), 'de partida,', len(nuevos), 'nuevas')
    if '--solo-mostrar' in sys.argv:
        json.dump(nuevos, open('/tmp/km.json', 'w'), ensure_ascii=False)
        sys.exit()
    todo = base + nuevos
    txt = json.dumps(todo, ensure_ascii=False, separators=(',', ':'))
    HTML.write_text(s[:m.start(1)] + txt + s[m.end(1):], encoding='utf-8')
    print('index.html actualizado:', len(todo), 'composiciones')
