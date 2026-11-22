// Lo confirmado del cuadro de escenarios (acordado el 22-11-2026). El cuadro arranca en estos valores;
// el resto queda en los valores por defecto. Se puede cambiar todo para ver qué hubiera pasado.
// Cuenta como confirmado: lanzamiento formal o inscripción de una candidatura, inscripción de un
// frente electoral, ley sancionada (PASO). No cuentan rumores ni encuestas.
// Claves: pro, ce, cc, pf, kic, mas, bu, cr (botones del cuadro); out (outsider), vice, paso,
// cand.pro, cand.ce, cand.cc, cand.pf, cand.kf (candidato de cada fuerza; cand.kf es el rival
// interno del frente kirchnerista en la PASO).
// Cada dato: v (valor), fuente, url, fecha (del hecho, si se conoce) y cargado (cuándo se cargó).
// Lo actualiza la revisión semanal de los lunes (ver CLAUDE.md).
var CONF = {
  actualizado: '2026-11-22',
  datos: {
    'cand.pro': {v: 'Lacunza', fuente: 'Lacunza se lanzó como precandidato presidencial del PRO, con el aval de Macri', url: 'https://www.lacapitalmdp.com/lacunza-se-lanzo-para-2027-reivindico-al-pro-y-marco-diferencias-con-milei/', fecha: '2026', cargado: '2026-11-22'},
    'cand.kf': {v: 'Uñac', fuente: 'Uñac lanzó su candidatura presidencial dentro del peronismo y pidió internas', url: 'https://www.ambito.com/sergio-unac-confirmo-que-jugara-las-elecciones-2027-soy-candidato-presidente-n6276940', fecha: '2026-05-12', cargado: '2026-11-22'}
  }
};
