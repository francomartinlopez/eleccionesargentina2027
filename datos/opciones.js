// Opciones del cuadro de escenarios que se aplican sobre cada escenario en el navegador:
// outsiders, vice de Milei y candidato de cada fuerza (acordado el 22-11-2026).
// No cambiar valores, escala ni repartos sin pedido expreso de Franco.
// Los valores de los outsiders son intención de voto en encuestas (con indecisos);
// se llevan a votos afirmativos multiplicando por `afirm`.
var OPC = {
  actualizado: '2026-11-22',
  afirm: 1.2,
  // Efecto sobre la fuerza, en puntos de votos afirmativos en la general.
  escala: {suma: 3, suma_algo: 1.5, neutro_suma: 0.75, neutro: 0, neutro_resta: -0.75, resta_algo: -1.5, resta: -3},
  // Parte del voto que se mueve que sale de (o va a) la abstención, el blanco y el nulo.
  abst: {mucho: 0.4, algo: 0.2, poco: 0.1, casi_nada: 0.05},
  // Fuerzas: lla, pro, ce (centro), cc, pf (peronismo federal), kf (frente kirchnerista: kirchnerismo,
  // Kicillof, K duro, Massa), per (kirchnerismo y peronismo federal), iz (izquierda).
  // "X e Y": partes iguales; "sobre todo X, algo Y": 0,7 y 0,3.
  outsiders: [
    {k: 'villarruel', n: 'Villarruel', v: 5.2, de: {lla: 0.7, pro: 0.3}, ab: 'poco',
     fuente: 'Sondeo nacional citado por Crónica (5,2 %)', url: 'https://www.cronica.com.ar/politica/milei-lidera-la-intencion-de-voto-pero-aun-no-alcanza-para-ganar-en-primera-vuelta-en-2027/'},
    {k: 'gebel', n: 'Gebel', v: 2.1, de: {per: 0.5, lla: 0.5}, ab: 'mucho',
     fuente: 'Promedio de Trends (3 %), otro sondeo nacional (1,6 %) y la primera medición de diciembre (1,8 %)', url: 'https://www.letrap.com.ar/politica/sin-lugar-otro-fenomeno-milei-dante-gebel-jorge-brito-y-hadad-no-superan-el-3-intencion-voto-n5426859'},
    {k: 'hadad', n: 'Hadad', v: 2.5, de: {ce: 1/3, pro: 1/3, lla: 1/3}, ab: 'poco',
     fuente: 'Promedio de Trends (3 %) y otro sondeo nacional (2,1 %)', url: 'https://www.letrap.com.ar/politica/sin-lugar-otro-fenomeno-milei-dante-gebel-jorge-brito-y-hadad-no-superan-el-3-intencion-voto-n5426859'},
    {k: 'brito', n: 'Brito', v: 2.3, de: {pf: 0.5, ce: 0.5}, ab: 'casi_nada',
     fuente: 'Promedio de Trends (2 %) y otro sondeo nacional (2,6 %)', url: 'https://www.letrap.com.ar/politica/sin-lugar-otro-fenomeno-milei-dante-gebel-jorge-brito-y-hadad-no-superan-el-3-intencion-voto-n5426859'},
    {k: 'melconian', n: 'Melconian', v: 1.7, est: 1, de: {pro: 1/3, ce: 1/3, lla: 1/3}, ab: 'casi_nada',
     fuente: 'Estimado: 4,3 % en una encuesta solo de outsiders × 0,4 (relación de Hadad y Brito)', url: 'https://www.perfil.com/noticias/politica/encuesta-sobre-outsiders-galperin-lidera-entre-los-nombres-elegidos-pero-la-mayoria-aun-no-define-una-alternativa.phtml'},
    {k: 'galperin', n: 'Galperin', v: 4.8, est: 1, de: {pro: 0.5, lla: 0.5}, ab: 'poco',
     fuente: 'Estimado: 12,1 % en una encuesta solo de outsiders × 0,4 (relación de Hadad y Brito)', url: 'https://www.perfil.com/noticias/politica/encuesta-sobre-outsiders-galperin-lidera-entre-los-nombres-elegidos-pero-la-mayoria-aun-no-define-una-alternativa.phtml'},
    {k: 'grabois', n: 'Grabois', v: 2.5, de: {kf: 0.7, iz: 0.3}, ab: 'algo',
     fuente: 'Entre 2 % (Isasi Burdman) y 6,7 % (CB); se toma 2,5, cerca del promedio de varios estudios', url: 'https://diariojornada.com.ar/420812/politica/elecciones_2027_un_macri_candidato_complicaria_la_reeleccion_de_milei'}
  ],
  // Candidato de cada fuerza, contra un candidato genérico. org: fuerzas de origen (para la afinidad
  // en frentes); sin org, no pertenece a ninguna (outsider dentro de la fuerza) y no hay pérdida por distancia.
  // a: adónde van los votos si resta (sin a, a las demás listas en proporción a su tamaño).
  // paso: solo cuenta en la PASO (rival interno), y solo con PASO.
  candidatos: {
    pro: [
      {n: 'Macri', e: 'suma', de: {lla: 1}, ab: 'casi_nada', org: ['pro']},
      {n: 'Lacunza', e: 'neutro', ab: 'casi_nada', org: ['pro']},
      {n: 'Galperin', e: 'suma_algo', de: {lla: 1}, ab: 'poco'},
      {n: 'Melconian', e: 'neutro', ab: 'casi_nada'}
    ],
    ce: [
      {n: 'Pullaro', e: 'neutro', ab: 'casi_nada', org: ['ce']},
      {n: 'Llaryora', e: 'neutro_resta', ab: 'casi_nada', org: ['ce']},
      {n: 'Torres', e: 'neutro', ab: 'casi_nada', org: ['ce']},
      {n: 'Schiaretti', e: 'suma_algo', de: {pf: 1}, ab: 'casi_nada', org: ['ce', 'pf']},
      {n: 'Manes', e: 'suma_algo', de: {pro: 0.5, ce: 0.5}, ab: 'poco'},
      {n: 'Melconian', e: 'neutro', ab: 'casi_nada'},
      {n: 'Hadad', e: 'suma_algo', de: {pro: 0.5, lla: 0.5}, ab: 'poco'},
      {n: 'Brito', e: 'neutro_suma', de: {pf: 1}, ab: 'casi_nada'},
      {n: 'Gebel', e: 'suma', de: {per: 0.5, lla: 0.5}, ab: 'mucho'}
    ],
    cc: [
      {n: 'Ferraro', e: 'resta_algo', ab: 'casi_nada', org: ['cc']}
    ],
    pf: [
      {n: 'Sáenz', e: 'neutro', ab: 'casi_nada', org: ['pf']},
      {n: 'Schiaretti', e: 'suma_algo', de: {ce: 1}, ab: 'casi_nada', org: ['ce', 'pf']},
      {n: 'Brito', e: 'neutro', ab: 'casi_nada'}
    ],
    kf: [
      {n: 'Grabois', e: 'suma', de: {iz: 1}, ab: 'algo', paso: 1, org: ['kf']},
      {n: 'Uñac', e: 'suma_algo', de: {pf: 1}, ab: 'casi_nada', paso: 1, org: ['kf']}
    ]
  },
  vice: [
    {k: 'otro', n: 'Otro', d: 'sin peso propio: Pettovello, Menem u otro'},
    {k: 'bullrich', n: 'Bullrich', e: 'suma', de: {pro: 0.7, ce: 0.3}, ab: 'poco'},
    {k: 'karina', n: 'Karina Milei', e: 'resta', a: {pro: 1/3, ce: 1/3, villarruel: 1/3}, ab: 0.7}
  ],
  // Afinidad: cuánto retiene el socio de un frente cuando el candidato viene de la otra fuerza.
  retiene: {cercana: 0.95, media: 0.85, lejana: 0.7, muy_lejana: 0.6},
  distancia: {'cc-pro': 'cercana', 'cc-ce': 'cercana', 'ce-pro': 'media', 'ce-pf': 'media', 'pf-pro': 'lejana', 'cc-pf': 'lejana'},
  distancia_otra: 'media',
  // Fuerza más cercana fuera del frente, para la parte de la fuga que iría al rival.
  cercana: {pro: ['cc', 'ce', 'pf'], ce: ['cc', 'pro', 'pf'], cc: ['ce', 'pro'], pf: ['ce', 'pro'], kf: ['pf']}
};
