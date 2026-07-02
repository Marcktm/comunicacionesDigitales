# Plan de desarrollo - App Streamlit Comunicaciones Digitales

Fecha de corte: 2026-07-02

## Objetivo general

Construir una app didactica en Streamlit para la materia Comunicaciones Digitales
(FCEFyN, UNC), organizada por unidades, con teoria paso a paso, graficas
interactivas y ejercicios/bonus con SDR cuando corresponda.

La app debe poder usarse sin hardware para estudiar teoria y simulaciones, y debe
activar el flujo SDR solo como extension practica cuando haya VPN y ADALM-Pluto
disponible.

## Criterio de pagina terminada

Cada tema se considera terminado cuando incluye:

- Teoria en Markdown/LaTeX, con derivacion completa y referencias al temario.
- Grafica o simulacion interactiva que permita variar parametros relevantes.
- Explicacion de interpretacion de resultados dentro de la pagina.
- Seccion Bonus SDR, aunque sea para aclarar que el tema es puramente simulado.
- Tests de las funciones numericas puras usadas por la pagina.

## Fase 0 - Relevamiento y base tecnica

Estado: completa.

Realizado:

- Se relevaron notebooks, apuntes y material existente del repositorio.
- Se definio una arquitectura separada por responsabilidades:
  - `core/`: funciones numericas y DSP puro.
  - `sdr/`: conexion, disponibilidad y estado del ADALM-Pluto.
  - `ui/`: paginas, componentes visuales y contenido teorico.
  - `tests/`: validacion automatizada del nucleo.
- Se agregaron archivos de entorno:
  - `requirements.txt` para instalacion con pip.
  - `environment.yml` para entorno conda completo.

Pendiente:

- Documentar matriz exacta de versiones probadas en macOS/Linux/Windows.

## Fase 1 - Andamiaje de la app y primer flujo completo

Estado: completa.

Realizado:

- Se creo el entrypoint `streamlit_app/app.py`.
- Se configuro navegacion por unidades con `st.navigation`.
- Se agrego pagina de inicio con estructura de la materia y uso del SDR.
- Se agrego sidebar global para:
  - chequear disponibilidad de los cinco SDR del laboratorio;
  - elegir SDR activo;
  - persistir la seleccion durante la navegacion.
- Se implemento el registro de SDR:
  - `SDR-1`: `192.168.1.31`
  - `SDR-2`: `192.168.1.32`
  - `SDR-3`: `192.168.1.33`
  - `SDR-4`: `192.168.1.34`
  - `SDR-5`: `192.168.1.35`
- Se implemento chequeo TCP contra `iiod` en el puerto `30431`.
- Se implemento la pagina de referencia "Unidad 2 - Criterio MAP y ML":
  - teoria MAP/ML para hipotesis binaria;
  - umbral optimo;
  - probabilidades de error condicionales y total;
  - grafica interactiva de regiones de decision;
  - verificacion Monte Carlo;
  - curva de probabilidad de error con funcion Q.
- Se agregaron componentes reutilizables:
  - renderizado de teoria desde Markdown;
  - graficas Plotly;
  - diagramas SVG/HTML testeables.
- Se agregaron tests para:
  - funcion Q;
  - cotas de funcion Q;
  - umbral MAP/ML;
  - probabilidad de error;
  - decision por vecino mas cercano;
  - simulacion Monte Carlo;
  - diagramas principales.

Pendiente:

- Ejecutar una validacion visual manual completa en navegador para todos los
  tamanos de pantalla esperados.
- Agregar capturas de referencia si se quiere documentar el estado visual.

## Fase 2 - Completar Unidad 1 y expandir Unidad 2

Estado: en progreso.

Realizado:

- Se agregaron paginas de Unidad 1:
  - repaso de probabilidad;
  - valor esperado y correlacion;
  - vectores gaussianos.
- Se agregaron paginas adicionales de Unidad 2:
  - prueba de hipotesis;
  - hipotesis M-aria;
  - probabilidad de error;
  - funcion Q;
  - receptor AWGN discreto;
  - observacion escalar;
  - observaciones vectoriales;
  - m-PAM y m-QAM;
  - estadistica suficiente.
- Se agrego contenido teorico asociado en `ui/content/*.md`.
- Se extendio `core/` con:
  - distribuciones gaussianas/laplacianas;
  - variables y vectores aleatorios;
  - constelaciones PAM, PSK y QAM;
  - cotas y aproximaciones de probabilidad de error;
  - helpers de senales de laboratorio.
- Se agregaron tests para modulacion, vectores aleatorios y diagramas.

Pendiente:

- Revisar cada pagina de Unidad 1 y 2 contra los capitulos/apuntes originales.
- Homogeneizar nivel de detalle: que todas las paginas alcancen el mismo estandar
  de la pagina MAP/ML.
- Agregar ejercicios guiados o preguntas de autoevaluacion por tema.
- Completar notas de interpretacion para graficas donde todavia esten breves.

## Fase 3 - Unidad 3: canal AWGN de tiempo continuo

Estado: pendiente.

Alcance propuesto:

- Energia de senal y espacio de producto interno.
- Ruido gaussiano blanco `N(t)` y covarianza.
- Estadistica suficiente y canal discreto equivalente.
- Arquitectura transmisor/receptor.
- Casos de modulacion:
  - PPM;
  - FSK;
  - espectro expandido;
  - PAM/PSK/QAM en tiempo continuo.
- Filtro apareado:
  - correlador;
  - matched filter;
  - equivalencia entre ambas implementaciones.

Entregables esperados:

- Paginas completas reemplazando placeholders de Unidad 3.
- Simulaciones de senales base y proyecciones.
- Diagramas del receptor y del espacio de senales.
- Tests para energia, correlacion, ortogonalidad y matched filter.

## Fase 4 - Unidad 4: SDR y laboratorios 1/2

Estado: pendiente.

Alcance propuesto:

- Introduccion practica al SDR y ADALM-Pluto.
- Configuracion del hardware y conexion por VPN.
- Integracion controlada con `pyadi-iio`.
- Caracterizacion de ruido del receptor.
- Comparacion entre muestras reales del SDR y modelo gaussiano.

Entregables esperados:

- Paginas completas para introduccion, configuracion y ruido.
- Flujo de conexion robusto con mensajes de error claros.
- Experimentos que funcionen en modo:
  - simulado, sin hardware;
  - real, con SDR disponible.
- Tests unitarios con mocks/fakes para no depender del hardware.

Pendiente tecnico:

- Definir interfaz fake para `PlutoSDR`.
- Manejar timeouts y fallas de VPN sin bloquear la app.
- Documentar permisos, drivers y pasos por sistema operativo.

## Fase 5 - Unidad 5: tren de pulsos, Nyquist, ISI y ojo

Estado: pendiente.

Alcance propuesto:

- Tren de pulsos y teorema de muestreo.
- Densidad espectral de potencia.
- Criterio de Nyquist.
- Coseno realzado y raiz de coseno realzado.
- ISI y diagrama de ojo.
- Muestreo, aliasing y filtrado.
- Simulador BPSK + AWGN extremo a extremo.
- Sincronizacion de simbolo.

Entregables esperados:

- Paginas completas reemplazando placeholders de Unidad 5.
- Graficas interactivas de PSD, respuesta temporal y ojo.
- Simulador end-to-end con BER vs SNR.
- Reutilizacion de notebooks de Parcial 2 y Laboratorio 4.
- Tests para filtros, pulsos, muestreo y BER teorica/simulada.

## Fase 6 - Pulido, calidad y publicacion

Estado: pendiente.

Tareas:

- Revisar redaccion tecnica completa.
- Unificar estilo visual, captions y nombres de variables.
- Revisar responsividad en pantallas chicas.
- Agregar guia de contribucion minima.
- Agregar comandos de validacion en README.
- Evaluar despliegue:
  - local con Streamlit;
  - Streamlit Community Cloud si no requiere SDR;
  - entorno interno si se quiere acceso a SDR por VPN.
- Preparar changelog o bitacora por version.

## Riesgos y decisiones abiertas

- El hardware SDR depende de VPN, disponibilidad del laboratorio y drivers locales.
- Algunas dependencias de SDR pueden ser mas fragiles que el nucleo didactico; por
  eso deben mantenerse opcionales siempre que sea posible.
- El contenido teorico debe validarse contra bibliografia y apuntes para evitar que
  una simplificacion visual introduzca errores conceptuales.
- Las simulaciones Monte Carlo requieren balance entre precision y tiempo de
  ejecucion dentro de Streamlit.

## Proximo bloque recomendado

1. Ejecutar tests automatizados del estado actual.
2. Revisar visualmente la app en navegador.
3. Cerrar Unidad 2 con el mismo nivel de detalle que MAP/ML.
4. Implementar Unidad 4 con modo simulado antes de depender del SDR real.
5. Avanzar Unidad 5 aprovechando los notebooks existentes de Nyquist, RRC e ISI.
