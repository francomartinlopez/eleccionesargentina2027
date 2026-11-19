"""Rehace la hoja "Todas las combinaciones" con todas las composiciones de `var COMP` (tablas, Kicillof y Massa, Bullrich)."""
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
H = ['Hoja', 'Escenario', 'PRO', 'Centro (UCR y gobernadores)', 'CC', 'Peronismo federal', 'Kicillof', 'Massa', 'Bullrich',
     'Frente oficialista', 'Oficialismo: PASO', 'Oficialismo: general', 'Oficialismo: balotaje', 'Rival en el balotaje', 'Resultado'] \
    + [n + ': general' for n in nombres] + [n + ': PASO' for n in nombres] \
    + ['Blanco (% padrón): general', 'Nulo (% padrón): general', 'Absentismo (% padrón): general']
filas = []
for c in C:
    if 'km' not in c and 'bid' not in c:
        v = dict(viejo[('Tabla ' + c['t'], c['s'])])
        v['Kicillof'] = LAB['kic']['k']; v['Massa'] = LAB['mas']['k']; v['Bullrich'] = 'En LLA'
        filas.append(v); continue
    O = c['O']; g = c['G']['ll']; bal = round(55.4 + c['db'], 1)
    otros = sorted(O, key=lambda o: -o[2]); riv = next(o for o in O if o[3])
    if g >= 45 or (g >= 40 and g - otros[0][2] >= 10): res = 'Gana LLA en primera vuelta'
    elif g < otros[1][2]: res = 'Balotaje sin LLA: ' + otros[0][0] + ' y ' + otros[1][0]
    else: res = 'Balotaje: gana ' + ('LLA' if bal > 50 else riv[0])
    ids = ' y '.join(x for x in (c.get('bid'), c.get('km')) if x)
    v = {'Hoja': 'Bullrich' if 'bid' in c else 'Kicillof y Massa', 'Escenario': '%s (sobre Tabla %s, 2027 %s)' % (ids, c['t'], c['s']),
         'Bullrich': 'Candidata del PRO' if c.get('bu') == 'pro' else 'En LLA',
         'PRO': LAB['pro'][c['pro']], 'Centro (UCR y gobernadores)': LAB['ce'][c['ce']], 'CC': LAB['cc'][c['cc']],
         'Peronismo federal': LAB['pf'][c['pf']], 'Kicillof': LAB['kic'][c.get('kic', 'k')], 'Massa': LAB['mas'][c.get('mas', 'k')],
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
    ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = 18 if j <= 15 else 14
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
        if isinstance(c.value, str) and 'composiciones del bloque' in c.value and c.value.startswith('Las '):
            c.value = ('Las %s composiciones del bloque "voto del oficialismo según cómo se agrupen las fuerzas" (44 de las Tablas A a L, '
                       'sin las inerciales, y 80 de la Tabla M, más %d variantes con Kicillof y Massa y %d con Bullrich candidata del PRO, '
                       'calculadas sobre ellas), una por fila, con el voto de cada lista en la PASO y la general, el balotaje y el resultado. '
                       'Valores de las tablas, sin el ajuste del ICG.') % (format(len(C), ',').replace(',', '.'),
                       sum('km' in x and 'bid' not in x for x in C), sum('bid' in x for x in C))
wb.save(X)
print(len(filas), 'filas,', len(H), 'columnas')
