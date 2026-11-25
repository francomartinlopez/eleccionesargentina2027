"""Genera datos-informe.json para la web de informes de Plexum (especificación «Datos que cada
web publica», v1.2, apartado 7: Elecciones 2027).

Publica solo lo que el sitio ya muestra:
- indicadores: ICG nacional y voto del oficialismo con el ICG corregido (último mes);
- novedades: la última encuesta (ICG de la Di Tella), con la fecha de campo;
- agenda: calendario electoral 2027 de los próximos 60 días (elecciones provinciales con fecha
  confirmada o anunciada, PASO provinciales, cierres de alianzas y listas, PASO, general y balotaje);
- faltantes: indicadores que esta vez no se pudieron publicar.

Si el contenido no cambió (salvo «generado»), no reescribe el archivo. Se corre en la acción
mensual del ICG, en la acción diaria «Datos para informes» y en las revisiones.
"""
import json, re, subprocess, calendar
from datetime import datetime, date, timedelta, timezone
from pathlib import Path

R = Path(__file__).resolve().parent.parent
SITIO = 'https://eleccionesargentina2027.netlify.app/'
ART = timezone(timedelta(hours=-3))
HOY = datetime.now(ART).date()
NAC = {'nivel': 'nacional', 'provincia': '', 'localidad': '', 'pais': 'Argentina'}
PROV_NOMBRE = {'Ciudad de Buenos Aires': 'CABA'}
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre',
         'octubre', 'noviembre', 'diciembre']


def num(x):
    return f'{x:.1f}'.replace('.', ',')


def fecha_txt(f):
    d = date.fromisoformat(f)
    return f'{d.day} de {MESES[d.month - 1]}'


def provincias():
    js = (R / 'datos/provincias.js').read_text(encoding='utf-8')
    out = subprocess.run(['node', '-e', 'global.window={};eval(require("fs").readFileSync(0,"utf8"));'
                          'process.stdout.write(JSON.stringify(window.PROV_DATA))'],
                         input=js, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def main():
    act = json.loads((R / 'datos/actual.json').read_text(encoding='utf-8'))
    mens = json.loads((R / 'datos/icg_mensual.json').read_text(encoding='utf-8'))
    destino = R / 'datos-informe.json'
    previo = json.loads(destino.read_text(encoding='utf-8')) if destino.exists() else None
    prev_ind = {i['id']: i for i in (previo or {}).get('indicadores', [])}
    prev_act = None
    if not previo:  # primera vez: valores del mes anterior desde el historial de git, si está
        try:
            log = subprocess.run(['git', 'log', '--format=%H', '--', 'datos/actual.json'], cwd=R,
                                 capture_output=True, text=True).stdout.split()
            for h in log:
                o = json.loads(subprocess.run(['git', 'show', f'{h}:datos/actual.json'], cwd=R,
                                              capture_output=True, text=True).stdout)
                if o.get('mes') != json.loads((R / 'datos/actual.json').read_text(encoding='utf-8'))['mes']:
                    prev_act = o; break
        except Exception:
            prev_act = None

    mes = act['mes']
    meses = sorted(mens)
    ult = mens.get(mes, {})
    campo = ult.get('campo')
    y, m = map(int, mes.split('-'))
    # fecha del dato: fin del trabajo de campo de la encuesta (si no está, último día del mes)
    fdato = campo[1] if campo else f'{mes}-{calendar.monthrange(y, m)[1]:02d}'
    mes_txt = f'{MESES[m - 1]} de {y}'

    ind, falt = [], []

    def agregar(id_, nombre, valor, unidad, fuente, url, anterior=None, unidad_var='p. p.'):
        if valor is None:
            p = prev_ind.get(id_)
            falt.append({'id': id_, 'nombre': nombre, 'motivo': 'El cálculo del último mes no dio este valor',
                         'ultimo_dato': p['fecha_dato'] if p else None})
            return
        r = {'id': id_, 'nombre': nombre, 'valor': valor, 'unidad': unidad}
        p = prev_ind.get(id_)
        if anterior is None and not p and prev_act and id_ in PREV:
            anterior = PREV[id_](prev_act)
        if anterior is None and p and p.get('periodo') != mes and isinstance(p.get('valor'), (int, float)):
            anterior = p['valor']
        elif anterior is None and p and p.get('periodo') == mes and p.get('variacion'):
            r['variacion'] = p['variacion']
        if anterior is not None:
            r['variacion'] = {'valor': round(valor - anterior, 2 if unidad_var == 'puntos' else 1),
                              'unidad': unidad_var, 'contra': 'mes anterior'}
        r.update({'fecha_dato': fdato, 'periodo': mes, 'fuente_original': fuente, 'eje': 'Política nacional',
                  'alcance': NAC, 'rubros': [], 'subrubros': [], 'exposicion': [], 'url': url})
        ind.append(r)

    PREV = {'voto-oficialismo-paso': lambda o: o['actual']['paso'][0],
            'voto-oficialismo-general-con-paso': lambda o: o['actual']['gen'][0],
            'voto-oficialismo-general-sin-paso': lambda o: o['actual']['sin'][0],
            'voto-oficialismo-balotaje': lambda o: o['actual']['bal'][0],
            'voto-oficialismo-general-proyectado': lambda o: o['proyectado']['todos_cen']['gen'][0]}
    i_ant = meses.index(mes) - 1 if mes in meses else -1
    icg_ant = round(mens[meses[i_ant]]['nacional'], 2) if i_ant >= 0 else None
    agregar('icg-nacional', 'Índice de Confianza en el Gobierno (Di Tella)', act.get('icg_nacional'),
            'puntos (escala de 0 a 5)', 'Universidad Torcuato Di Tella', SITIO + '#p2027', icg_ant, 'puntos')
    a = act.get('actual', {})
    fte = 'Universidad Torcuato Di Tella (ICG); cálculo propio con el ICG corregido'
    for k, n in (('paso', 'Voto del oficialismo en la PASO 2027 según el ICG corregido'),
                 ('gen', 'Voto del oficialismo en la general 2027 con PASO según el ICG corregido'),
                 ('sin', 'Voto del oficialismo en la general 2027 sin PASO según el ICG corregido'),
                 ('bal', 'Voto del oficialismo en el balotaje 2027 según el ICG corregido')):
        v = a.get(k)
        agregar('voto-oficialismo-' + {'paso': 'paso', 'gen': 'general-con-paso', 'sin': 'general-sin-paso',
                                       'bal': 'balotaje'}[k], n, v[0] if v else None,
                '% de los votos afirmativos', fte, SITIO + '#p2027')
    pc = act.get('proyectado', {}).get('todos_cen', {}).get('gen')
    agregar('voto-oficialismo-general-proyectado', 'Voto del oficialismo en la general 2027 con PASO, '
            'proyectado a la elección (trayectoria central del ICG)', pc[0] if pc else None,
            '% de los votos afirmativos', fte, SITIO + '#p2027proy')

    # novedad: la última encuesta (el ICG del último mes)
    nov = []
    if campo and (HOY - date.fromisoformat(fdato)).days <= 90:
        g = a.get('gen')
        icg_txt = f'{act["icg_nacional"]:.2f}'.replace('.', ',')
        res = (f'La Di Tella relevó {ult.get("n", "")} casos entre el {fecha_txt(campo[0])} y el '
               f'{fecha_txt(campo[1])}. El índice quedó en {icg_txt}')
        if icg_ant is not None:
            d = act['icg_nacional'] - icg_ant
            res += f' ({"+" if d >= 0 else "−"}' + f'{abs(d):.2f}'.replace('.', ',') + ' contra el mes anterior)'
        if g:
            res += (f'. Con el índice corregido, el oficialismo obtendría entre {num(g[1])} y {num(g[2])} % '
                    f'en la general con PASO.')
        nov.append({'id': f'{mes}-icg-di-tella', 'fecha_dato': fdato,
                    'titulo': f'Índice de Confianza en el Gobierno de {mes_txt}',
                    'resumen': res, 'tipo': 'encuesta', 'eje': 'Política nacional', 'alcance': NAC,
                    'rubros': [], 'subrubros': [], 'exposicion': [], 'url': SITIO + '#p2027'})

    # agenda: próximos 60 días
    pv = provincias()
    hasta = HOY + timedelta(days=60)
    ag = []

    def evento(f, texto, alcance, url):
        if f and HOY <= date.fromisoformat(f) <= hasta:
            ag.append({'fecha': f, 'evento': texto, 'eje': 'Política nacional', 'alcance': alcance,
                       'rubros': [], 'url': url})

    nac = pv.get('nacionales', {})
    evento(nac.get('paso'), 'PASO presidenciales 2027', NAC, SITIO + '#p2027')
    evento(nac.get('general'), 'Elección presidencial 2027 (general)', NAC, SITIO + '#p2027')
    evento(nac.get('balotaje'), 'Balotaje presidencial 2027', NAC, SITIO + '#p2027')
    sp = pv.get('sin_paso', {})
    evento(sp.get('alianzas'), 'Cierre de alianzas para la elección presidencial (si no hay PASO)', NAC, SITIO + '#met-provincias')
    evento(sp.get('listas'), 'Cierre de listas para la elección presidencial (si no hay PASO)', NAC, SITIO + '#met-provincias')
    for p in pv.get('provincias', []):
        if p.get('estado') not in ('c', 'a'):
            continue  # las fechas estimadas no van a la agenda
        prov = PROV_NOMBRE.get(p['n'], p['n'])
        alc = {'nivel': 'provincia', 'provincia': prov, 'localidad': '', 'pais': 'Argentina'}
        url = (p.get('fuente') or {}).get('url') or SITIO + '#met-provincias'
        marca = '' if p['estado'] == 'c' else ' (fecha anunciada, sin decreto)'
        evento(p.get('paso_prov'), f'PASO provinciales en {p["n"]}{marca}', alc, url)
        evento(p.get('fecha'), f'Elección de gobernador en {p["n"]}{marca}', alc, url)
    ag.sort(key=lambda e: (e['fecha'], e['evento']))

    datos = {'web': 'Elecciones 2027', 'version': '1.0', 'generado': '', 'indicadores': ind,
             'novedades': nov, 'agenda': ag, 'faltantes': falt}
    if previo:
        comp = dict(previo); comp['generado'] = ''
        if comp == datos:
            print('datos-informe.json sin cambios')
            return
    datos['generado'] = datetime.now(ART).replace(microsecond=0).isoformat()
    destino.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'datos-informe.json: {len(ind)} indicadores, {len(nov)} novedades, {len(ag)} eventos, {len(falt)} faltantes')


if __name__ == '__main__':
    main()
