"""Rehace la hoja "Todas las combinaciones" con las 836 composiciones de `var COMP`."""
import json, re, copy
from pathlib import Path
import openpyxl
ROOT = Path(__file__).resolve().parents[1]
s = (ROOT / 'index.html').read_text(encoding='utf-8')
C = json.loads(re.search(r'var COMP=(\[.*?\]);\n', s).group(1))
X = ROOT / 'datos/escenarios-2027.xlsx'
wb = openpyxl.load_workbook(X)
ws = wb['Todas las combinaciones']
hdr = [c.value for c in ws[1]]
viejo = {}
for r in ws.iter_rows(min_row=2, values_only=True):
    viejo[(r[0], r[1])] = dict(zip(hdr, r))
LAB = {'pro': {'lla': 'Con LLA', 'solo': 'Solo', 'centro': 'Con el centro', 'cc': 'Con la CC', 'cc_centro': 'Con la CC y el centro',
               'pf': 'Con el peronismo federal', 'centro_pf': 'Con el centro y el peronismo federal', 'no': 'No se presenta'},
       'ce': {'no': 'No se presenta', 'solo': 'Solo', 'lla': 'Con LLA', 'pro': 'Con el PRO', 'cc': 'Con la CC', 'pf': 'Con el peronismo federal'},
       'cc': {'sola': 'Sola', 'no': 'No se presenta', 'pro': 'Con el PRO', 'centro': 'Con el centro'},
       'pf': {'solo': 'Solo', 'k': 'Con el kirchnerismo', 'lla': 'Con LLA', 'pro': 'Con el PRO', 'centro': 'Con el centro',
              'kic': 'Con Kicillof', 'mas': 'Con Massa', 'no': 'No se presenta'},
       'kic': {'k': 'Dentro del kirchnerismo', 'solo': 'Solo', 'pf': 'Con el peronismo federal'},
       'mas': {'k': 'Dentro del kirchnerismo', 'solo': 'Solo', 'pf': 'Con el peronismo federal', 'kic': 'Con Kicillof',
               'kic_pf': 'Con Kicillof y el peronismo federal', 'pro': 'Con el PRO', 'pro_pf': 'Con el PRO y el peronismo federal'}}
nombres = sorted({o[0] for c in C for o in c['O'] if o[0] != 'Izquierda'}) + ['Izquierda']
H = ['Hoja', 'Escenario', 'PRO', 'Centro (UCR y gobernadores)', 'CC', 'Peronismo federal', 'Kicillof', 'Massa',
     'Frente oficialista', 'Oficialismo: PASO', 'Oficialismo: general', 'Oficialismo: balotaje', 'Rival en el balotaje', 'Resultado'] \
    + [n + ': general' for n in nombres] + [n + ': PASO' for n in nombres] \
    + ['Blanco (% padrón): general', 'Nulo (% padrón): general', 'Absentismo (% padrón): general']
filas = []
for c in C:
    if 'km' not in c:
        v = dict(viejo[('Tabla ' + c['t'], c['s'])])
        v['Kicillof'] = LAB['kic']['k']; v['Massa'] = LAB['mas']['k']
        filas.append(v); continue
    O = c['O']; g = c['G']['ll']; bal = round(55.4 + c['db'], 1)
    otros = sorted(O, key=lambda o: -o[2]); riv = next(o for o in O if o[3])
    if g >= 45 or (g >= 40 and g - otros[0][2] >= 10): res = 'Gana LLA en primera vuelta'
    elif g < otros[1][2]: res = 'Balotaje sin LLA: ' + otros[0][0] + ' y ' + otros[1][0]
    else: res = 'Balotaje: gana ' + ('LLA' if bal > 50 else riv[0])
    v = {'Hoja': 'Kicillof y Massa', 'Escenario': '%s (sobre Tabla %s, 2027 %s)' % (c['km'], c['t'], c['s']),
         'PRO': LAB['pro'][c['pro']], 'Centro (UCR y gobernadores)': LAB['ce'][c['ce']], 'CC': LAB['cc'][c['cc']],
         'Peronismo federal': LAB['pf'][c['pf']], 'Kicillof': LAB['kic'][c['kic']], 'Massa': LAB['mas'][c['mas']],
         'Frente oficialista': c['f'], 'Oficialismo: PASO': round(c['P']['ll'] / 100, 3), 'Oficialismo: general': round(g / 100, 3),
         'Oficialismo: balotaje': round(bal / 100, 3), 'Rival en el balotaje': riv[0], 'Resultado': res,
         'Blanco (% padrón): general': c['G']['bl'] / 100, 'Nulo (% padrón): general': c['G']['nu'] / 100,
         'Absentismo (% padrón): general': c['G']['ab'] / 100}
    for o in O:
        v[o[0] + ': general'] = round(o[2] / 100, 3); v[o[0] + ': PASO'] = round(o[1] / 100, 3)
    filas.append(v)
st_h = copy.copy(ws.cell(1, 1)._style); st_t = copy.copy(ws.cell(2, 1)._style); st_p = copy.copy(ws.cell(2, 8)._style)
i = wb.sheetnames.index(ws.title); wb.remove(ws); ws = wb.create_sheet('Todas las combinaciones', i)
for j, h in enumerate(H, 1):
    c = ws.cell(1, j, h); c._style = copy.copy(st_h)
    ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = 18 if j <= 14 else 14
ws.row_dimensions[1].height = 60
for r, v in enumerate(filas, 2):
    for j, h in enumerate(H, 1):
        x = v.get(h)
        c = ws.cell(r, j, x)
        c._style = copy.copy(st_p if isinstance(x, float) else st_t)
ws.freeze_panes = 'C2'
ws.auto_filter.ref = 'A1:%s%d' % (openpyxl.utils.get_column_letter(len(H)), len(filas) + 1)
ix = wb['Índice']
for row in ix.iter_rows():
    for c in row:
        if isinstance(c.value, str) and 'Las 124 composiciones del bloque' in c.value:
            c.value = c.value.replace('Las 124 composiciones del bloque', 'Las 836 composiciones del bloque').replace(
                'y 80 de la Tabla M)', 'y 80 de la Tabla M, más 712 variantes con Kicillof y Massa calculadas sobre ellas)')
wb.save(X)
print(len(filas), 'filas,', len(H), 'columnas')
