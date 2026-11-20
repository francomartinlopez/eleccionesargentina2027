/* Elecciones provinciales 2027: datos del efecto sobre LLA. Ver js/provincias.js.
   esperado: resultado más probable, of (gana LLA o aliado formal), amb (oficialismo provincial que compite aparte), op (peronismo opositor).
   prob: probabilidad de cada resultado en % (estimación propia; el modo "efecto esperado" pondera con ella).
   efecto: [PASO, general, balotaje] en fracción del máximo. estado de la fecha: c confirmada (decreto o junta electoral), a anunciada, e estimada.
   fuente: {texto, url} de la fecha. paso_prov: PASO provincial. senal_paso: fecha que cuenta para la señal sobre las PASO nacionales.
   Cuando una provincia vota se agrega "real": {"res": "of|amb|op", "ganador": "Nombre (fuerza)", "pct": 45.2, "segundo": "Nombre (fuerza)", "pct2": 30.1, "margen": 15.1, "fecha": "AAAA-MM-DD", "fuente": "escrutinio provisorio|definitivo", "url": "..."}.
   Buenos Aires: "real": {"res": "pc|pa|sa|sc", "texto": "..."}; Ciudad: "real": {"res": "of|amb|op", "texto": "..."}. */
window.PROV_DATA = {
 "actualizado": "2026-11-20",
 "nacionales": {
  "paso": "2027-08-08",
  "general": "2027-10-24",
  "balotaje": "2027-11-21"
 },
 "padron_total": 35771647,
 "fuente_padron": "Padrón por distrito de las elecciones del 26-10-2025 (CNE y DINE), según el detalle publicado por Crónica el 2-10-2025, sin residentes en el exterior. Total oficial de la CNE: 35.987.634.",
 "reglas": {
  "max_con": {
   "P": 1,
   "G": 0.7,
   "B": 0.5
  },
  "max_sin": {
   "G": 1.2,
   "B": 0.5
  },
  "tope_con": {
   "P": 3,
   "G": 2,
   "B": 1.5
  },
  "tope_sin": {
   "G": 2.5,
   "B": 1.5
  },
  "dias_mitad": 92,
  "vuelco": 0.6,
  "racha": 1.5,
  "margen_alto": 10,
  "margen_bajo": 3,
  "f_alto": 1.25,
  "f_bajo": 0.75,
  "icg_posterior": 0.5,
  "racha_min": 3,
  "racha_prop": 0.75,
    "racha_umbral": 0.05
 },
 "ba": {
  "esperado": "pa",
  "padron": 13353974,
  "opciones": {
   "pc": {
    "P": -0.6,
    "G": -1.1,
    "B": -0.7
   },
   "pa": {
    "P": -0.3,
    "G": -0.55,
    "B": -0.35
   },
   "sa": {
    "P": 0.3,
    "G": 0.55,
    "B": 0.35
   },
   "sc": {
    "P": 0.6,
    "G": 1.1,
    "B": 0.7
   }
  },
  "prob": {
   "pc": 20,
   "pa": 40,
   "sa": 30,
   "sc": 10
  }
 },
 "caba": {
  "esperado": "amb",
  "padron": 2520249,
  "efecto": {
   "of": 0.2,
   "amb": 0,
   "op": -0.2
  },
  "prob": {
   "of": 40,
   "amb": 50,
   "op": 10
  }
 },
 "mismo_dia": [
  "Buenos Aires",
  "Ciudad de Buenos Aires",
  "Catamarca",
  "La Rioja"
 ],
 "no_eligen": [
  "Corrientes",
  "Santiago del Estero"
 ],
 "provincias": [
  {
   "n": "Neuquén",
   "fecha": "2027-02-14",
   "estado": "c",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.25,
     -0.25,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 609951,
   "prob": {
    "of": 20,
    "amb": 70,
    "op": 10
   },
   "fuente": {
    "texto": "Decreto 1860/2026 del gobernador Figueroa (9-11-2026)",
    "url": "https://www.c5n.com/politica/neuquen-confirmo-el-desdoblamiento-y-elegira-gobernador-febrero-n253884"
   }
  },
  {
   "n": "Río Negro",
   "fecha": "2027-03-21",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.25,
     -0.25,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 617054,
   "prob": {
    "of": 25,
    "amb": 60,
    "op": 15
   },
   "fuente": {
    "texto": "Estimación propia a partir de elecciones anteriores y notas de prensa (sin anuncio oficial al 20-11-2026)"
   }
  },
  {
   "n": "La Pampa",
   "fecha": "2027-05-16",
   "estado": "e",
   "esperado": "op",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -0.5,
     -0.25,
     -0.25
    ]
   },
   "propio": true,
   "padron": 304693,
   "paso_prov": "2027-03-14",
   "prob": {
    "of": 20,
    "amb": 10,
    "op": 70
   },
   "fuente": {
    "texto": "Estimación propia a partir de elecciones anteriores y notas de prensa (sin anuncio oficial al 20-11-2026)"
   }
  },
  {
   "n": "Misiones",
   "fecha": "2027-05-02",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     -0.5,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 994317,
   "prob": {
    "of": 15,
    "amb": 75,
    "op": 10
   },
   "fuente": {
    "texto": "Sin fecha oficial: el gobernador Passalacqua evalúa abril o mayo",
    "url": "https://www.letrap.com.ar/politica/el-quiebre-politico-misiones-pone-jaque-la-eliminacion-las-paso-n5425780"
   }
  },
  {
   "n": "Tucumán",
   "fecha": "2027-05-09",
   "estado": "c",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.5,
     -0.5,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 1341563,
   "prob": {
    "of": 40,
    "amb": 55,
    "op": 5
   },
   "fuente": {
    "texto": "Decreto de convocatoria del gobernador Jaldo (27-7-2026)",
    "url": "https://www.lagaceta.com.ar/nota/1147211/politica/jaldo-regreso-actividad-confirmo-elecciones-provinciales-seran-9-mayo-2027.html"
   }
  },
  {
   "n": "Salta",
   "fecha": "2027-05-16",
   "estado": "c",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     -0.5,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 1111029,
   "prob": {
    "of": 15,
    "amb": 75,
    "op": 10
   },
   "fuente": {
    "texto": "Decreto 762 del gobernador Sáenz (noviembre de 2026)",
    "url": "https://www.todojujuy.com/salta-confirmo-la-fecha-las-elecciones-2027-votaran-el-16-mayo-n298922"
   }
  },
  {
   "n": "Jujuy",
   "fecha": "2027-05-23",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.5,
     -0.5,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 602380,
   "prob": {
    "of": 30,
    "amb": 60,
    "op": 10
   },
   "fuente": {
    "texto": "Estimación propia a partir de elecciones anteriores y notas de prensa (sin anuncio oficial al 20-11-2026)"
   }
  },
  {
   "n": "Tierra del Fuego",
   "fecha": "2027-05-30",
   "estado": "e",
   "esperado": "of",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -0.5,
     -0.25,
     -0.25
    ]
   },
   "propio": true,
   "padron": 162527,
   "prob": {
    "of": 50,
    "amb": 10,
    "op": 40
   },
   "fuente": {
    "texto": "Estimación propia a partir de elecciones anteriores y notas de prensa (sin anuncio oficial al 20-11-2026)"
   }
  },
  {
   "n": "San Juan",
   "fecha": "2027-05-30",
   "estado": "e",
   "esperado": "of",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": false,
   "padron": 606278,
   "prob": {
    "of": 70,
    "amb": 10,
    "op": 20
   },
   "fuente": {
    "texto": "Estimación propia a partir de elecciones anteriores y notas de prensa (sin anuncio oficial al 20-11-2026)"
   }
  },
  {
   "n": "Córdoba",
   "fecha": "2027-06-06",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -1,
     -0.5,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": false,
   "padron": 3084000,
   "prob": {
    "of": 40,
    "amb": 55,
    "op": 5
   },
   "fuente": {
    "texto": "Estimación propia a partir de elecciones anteriores y notas de prensa (sin anuncio oficial al 20-11-2026)"
   }
  },
  {
   "n": "Santa Fe",
   "fecha": "2027-06-13",
   "estado": "a",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.5,
     -0.5,
     0.5
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": false,
   "padron": 2815453,
   "paso_prov": "2027-04-18",
   "prob": {
    "of": 15,
    "amb": 75,
    "op": 10
   },
   "fuente": {
    "texto": "Cronograma anunciado por el gobernador Pullaro (octubre de 2026); falta el decreto",
    "url": "https://www.letrap.com.ar/politica/asi-sera-el-cronograma-electoral-santa-fe-2027-paso-el-18-abril-y-generales-el-13-junio-n5427251"
   }
  },
  {
   "n": "Entre Ríos",
   "fecha": "2027-06-13",
   "estado": "e",
   "esperado": "of",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": false,
   "padron": 1053652,
   "paso_prov": "2027-04-11",
   "prob": {
    "of": 70,
    "amb": 5,
    "op": 25
   },
   "fuente": {
    "texto": "Estimación propia a partir de elecciones anteriores y notas de prensa (sin anuncio oficial al 20-11-2026)"
   }
  },
  {
   "n": "San Luis",
   "fecha": "2027-06-13",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.25,
     -0.25,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 399321,
   "prob": {
    "of": 20,
    "amb": 70,
    "op": 10
   },
   "fuente": {
    "texto": "Estimación propia a partir de elecciones anteriores y notas de prensa (sin anuncio oficial al 20-11-2026)"
   }
  },
  {
   "n": "Formosa",
   "fecha": "2027-06-27",
   "estado": "e",
   "esperado": "op",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -0.5,
     -0.25,
     -0.25
    ]
   },
   "propio": true,
   "padron": 491565,
   "prob": {
    "of": 10,
    "amb": 5,
    "op": 85
   },
   "fuente": {
    "texto": "Estimación propia a partir de elecciones anteriores y notas de prensa (sin anuncio oficial al 20-11-2026)"
   }
  },
  {
   "n": "Chubut",
   "fecha": "2027-07-25",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.25,
     -0.25,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 453021,
   "prob": {
    "of": 25,
    "amb": 60,
    "op": 15
   },
   "fuente": {
    "texto": "Sin fecha oficial: el gobernador Torres evalúa junio-julio sin PASO nacionales o agosto con PASO",
    "url": "https://cholilaonline.ar/2026/10/torres-respaldo-eliminar-las-paso.html"
   }
  },
  {
   "n": "Santa Cruz",
   "fecha": "2027-08-08",
   "estado": "e",
   "esperado": "amb",
   "efecto": {
    "of": [
     1,
     1,
     0.5
    ],
    "amb": [
     -0.25,
     -0.25,
     0
    ],
    "op": [
     -1,
     -0.5,
     -0.5
    ]
   },
   "propio": true,
   "padron": 288732,
   "prob": {
    "of": 20,
    "amb": 55,
    "op": 25
   },
   "fuente": {
    "texto": "Estimación propia a partir de elecciones anteriores y notas de prensa (sin anuncio oficial al 20-11-2026)"
   }
  },
  {
   "n": "Chaco",
   "fecha": "2027-09-19",
   "estado": "e",
   "esperado": "of",
   "efecto": {
    "of": [
     0.5,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -0.5,
     -1,
     -0.5
    ]
   },
   "propio": false,
   "padron": 1015693,
   "prob": {
    "of": 55,
    "amb": 0,
    "op": 45
   },
   "fuente": {
    "texto": "Desdoblamiento confirmado (art. 90 de la Constitución) y PASO provinciales suspendidas para 2027; fecha posible: segunda quincena de septiembre",
    "url": "https://www.perfil.com/noticias/nea/chaco-suspendio-las-paso-para-2027-con-el-apoyo-clave-de-una-diputada-massista.phtml"
   }
  },
  {
   "n": "Mendoza",
   "fecha": "2027-09-26",
   "estado": "a",
   "esperado": "of",
   "efecto": {
    "of": [
     0.5,
     1,
     0.5
    ],
    "amb": [
     0,
     0,
     0
    ],
    "op": [
     -0.5,
     -1,
     -0.5
    ]
   },
   "propio": false,
   "padron": 1525824,
   "paso_prov": "2027-07-04",
   "senal_paso": "2027-07-04",
   "prob": {
    "of": 75,
    "amb": 5,
    "op": 20
   },
   "fuente": {
    "texto": "El gobernador Cornejo confirmó PASO provinciales en julio; general sin fecha oficial",
    "url": "https://www.losandes.com.ar/politica/alfredo-cornejo-en-mendoza-no-vamos-suspender-las-paso-n5997750"
   }
  }
 ],
 "fuente_padron_url": "https://www.cronica.com.ar/politica/Elecciones-2025-Cuantos-votantes-estan-habilitados-para-acudir-a-las-urnas-en-cada-provincia-20251002-0050.html",
 "sin_paso": {
  "alianzas": "2027-07-05",
  "listas": "2027-08-15"
 }
};
