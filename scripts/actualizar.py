"""Recalcula los bloques 2027 con el último ICG publicado por la Di Tella.

Uso: python scripts/actualizar.py fuentes/icg.dta [fuentes/historico.xls]
Lee los microdatos (.dta), calcula el ICG por región y mes, y escribe
datos/icg_mensual.json y datos/actual.json. Los parámetros calibrados
(datos/parametros.json) no cambian de mes a mes: solo se recalibran tras una elección.
"""
import json, sys, statistics
from datetime import date
from pathlib import Path
import numpy as np, pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
P = json.loads((RAIZ / 'datos/parametros.json').read_text())
b, T, w = P['b'], P['T'], P['w']
MESES = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']

def icg_por_region(dta):
    df = pd.read_stata(dta, convert_categoricals=False, columns=['año','mes','Ciudad','ICG','ponderacion_UTDT'])
    c2r = {c: r for r, cs in P['regiones'].items() for c in cs}
    df['reg'] = df.Ciudad.map(c2r)
    df = df[df.ICG.notna()]
    out = {}
    for (y, m), g in df.groupby(['año', 'mes']):
        k = f'{int(y)}-{int(m):02d}'
        pw = g.ponderacion_UTDT.fillna(1)
        out[k] = {'nacional': round(float(np.average(g.ICG, weights=pw)), 3), 'n': int(len(g))}
        for r, gr in g.groupby('reg'):
            out[k][r] = [round(float(np.average(gr.ICG, weights=gr.ponderacion_UTDT.fillna(1))), 3), int(len(gr)),
                         round(float(gr.ICG.std() / np.sqrt(len(gr))), 3)]
    return dict(sorted(out.items()))

def valor(i, tipo):
    if tipo == 'PASO': return i + b[2] * max(0, T - i) + b[4]
    if tipo == 'P': return i + b[0] * max(0, T - i)
    return i + b[3] * max(0, 50 - i)

def suma(icg_reg, tipo):
    s = 0
    for r in w:
        v = valor(icg_reg[r] * 20, tipo)
        if tipo == 'PASO': v += P['adjPASO'][r]
        s += w[r] * v
    return s

def bloque(paso, gen, bal):
    R = P['rango']; r1 = lambda x: round(x, 1)
    cont = P.get('continuidad', {})
    paso += cont.get('paso', 0); gen += cont.get('gen', 0); bal += cont.get('bal', 0)
    return {'paso': [r1(paso), r1(paso + R['paso'][0]), r1(paso + R['paso'][1])],
            'gen': [r1(gen), r1(gen + R['gen'][0]), r1(gen + R['gen'][1])],
            'bal': [r1(bal), r1(bal + R['bal'][0]), r1(bal + R['bal'][1])],
            'sin': [r1((paso + gen) / 2), r1(min(paso, gen)), r1(max(paso, gen))]}

def traj(v, k):
    if k == 'pes': return min(v)
    if k == 'opt': return max(v)
    return statistics.median(v) if len(v) > 2 else statistics.mean(v)

def main(dta):
    M = icg_por_region(dta)
    (RAIZ / 'datos/icg_mensual.json').write_text(json.dumps(M))
    ult = list(M)[-1]; U = M[ult]
    reg = {r: U[r][0] for r in w}
    act = bloque(suma(reg, 'PASO'), suma(reg, 'P'), suma(reg, 'B'))
    seis = list(M)[-6:]
    ratio = {r: np.mean([M[m][r][0] for m in seis]) / np.mean([M[m]['nacional'] for m in seis]) for r in w}
    base = U['nacional']; proy = {}
    for ref, R in P['ref'].items():
        for k in ('pes', 'cen', 'opt'):
            icg = {m: base * traj(R[m], k) for m in R}
            rr = lambda m: {r: icg[m] * ratio[r] for r in w}
            p = bloque(suma(rr('jul'), 'PASO'), suma(rr('sep'), 'P'), suma(rr('oct'), 'B'))
            p['icg'] = {m: round(v, 2) for m, v in icg.items()}
            proy[f'{ref}_{k}'] = p
    eco = json.loads((RAIZ / 'datos/economia.json').read_text())['ajuste'] if (RAIZ / 'datos/economia.json').exists() else {}
    proy_eco = {}
    for esc in ('pesimista', 'central', 'optimista'):
        for ref, R in P['ref'].items():
            aj = eco.get(f'{esc}_{ref}')
            if not aj: continue
            for k in ('pes', 'cen', 'opt'):
                icg = {m: base * traj(R[m], k) for m in R}
                rr = lambda m: {r: max(0.05, icg[m] * ratio[r] + aj[r][m]) for r in w}
                p = bloque(suma(rr('jul'), 'PASO'), suma(rr('sep'), 'P'), suma(rr('oct'), 'B'))
                p['icg'] = {m: round(sum(w[r] * rr(m)[r] for r in w), 2) for m in R}
                proy_eco[f'{esc}_{ref}_{k}'] = p
    y, m = ult.split('-')
    out = {'mes': ult, 'mes_texto': f'{MESES[int(m)-1]} de {y}', 'icg_nacional': round(base, 2),
           'icg_regiones': {r: round(reg[r], 2) for r in w}, 'casos': U['n'],
           'ratios': {r: round(float(v), 2) for r, v in ratio.items()}, 'meses_ratio': [seis[0], seis[-1]],
           'actual': act, 'proyectado': proy, 'proyectado_eco': proy_eco,
           'mapa2027': {'reg': {r: [U[r][1], round(U[r][2] * 20 * 1.96, 1), round(reg[r] * 20, 1),
                                    round(valor(reg[r] * 20, 'P') + P.get('continuidad', {}).get('gen', 0), 1),
                                    round(valor(reg[r] * 20, 'P') + P.get('continuidad', {}).get('gen', 0), 1), None] for r in w},
                        'nac': [act['gen'][0], act['gen'][0], None]},
           }
    destino = RAIZ / 'datos/actual.json'
    previo = json.loads(destino.read_text()) if destino.exists() else {}
    if {k: v for k, v in previo.items() if k != 'actualizado'} == json.loads(json.dumps(out)):
        print('Sin cambios: el último mes ya estaba procesado.')
        return
    out['actualizado'] = date.today().isoformat()
    destino.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(ult, 'ICG', round(base, 3), {k: v[0] for k, v in act.items()}, 'central', {k: proy['todos_cen'][k][0] for k in ('paso','gen','bal','sin')})

if __name__ == '__main__':
    main(sys.argv[1])
