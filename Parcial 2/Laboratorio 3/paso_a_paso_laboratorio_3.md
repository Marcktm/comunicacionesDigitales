# Laboratorio 3 - Plan de trabajo y guia de aprendizaje

## Objetivo del documento

Este archivo no es la resolucion final del laboratorio. Es una guia de trabajo para ir construyendo la practica paso a paso, entendiendo que hace cada bloque, para que sirve y donde aparece la teoria correspondiente en el libro de Bixio Rimoldi, *Principles of Digital Communication: A Top-Down Approach*.

La idea es que en cada charla avancemos una parte concreta:

- primero entendemos el concepto;
- despues lo conectamos con la consigna;
- luego lo implementamos en notebook;
- finalmente interpretamos las graficas y dejamos escrita una conclusion parcial.

## Material de referencia

- Consigna de la practica: `/Users/marcosreyeros/Downloads/Comunicaciones Digitales 2026 - Primer Semestre_ Consigna de la práctica _ NVA.pdf`
- Libro de la catedra: `/Users/marcosreyeros/Downloads/Bixio Rimoldi-Principles of Digital Communication_ A Top-Down Approach-Cambridge University Press (2016).pdf`
- Laboratorio 1: configuracion de VPN, Jupyter Hub, SDR e IIO Oscilloscope.
- Laboratorio 2: caracterizacion de ruido I/Q cuando el SDR no transmite.
- Simulador del Parcial 2: fuente, encoder, waveform former, canal AWGN, matched filter, correlador, decoder ML y probabilidad de error.

## Relacion general con el Bixio

La practica mezcla tres capas que en el libro aparecen separadas para poder entenderlas mejor:

- Capitulo 2: decision con observaciones discretas, hipotesis, criterio ML, gaussianidad y probabilidad de error.
- Capitulo 3: canal AWGN continuo, observables, estadisticas suficientes, correlador y matched filter.
- Capitulo 5: trenes de pulsos, pulsos rectangulares, PSD, ancho de banda e interpretacion temporal/frecuencial.
- Capitulo 7: comunicacion pasabanda, senales equivalentes en banda base, muestras complejas I/Q, conversion up/down y efectos practicos de SDR.

## Traduccion Bixio -> codigo de laboratorio

Esta seccion es el puente teorico-practico. La usamos para no perder de vista que cada array, grafico o funcion en Python representa una parte del sistema de comunicaciones.

### Hipotesis y senales posibles

En el Capitulo 2, Bixio arranca desde el problema del receptor: el sistema transmite una hipotesis y el receptor debe decidir cual fue. En codigo, una hipotesis deja de ser una idea abstracta y se convierte en un valor dentro de un array.

Cuando escribimos:

```python
i_component = np.where(u_i < ref, -1.0, 1.0)
```

estamos generando una variable aleatoria que puede tomar dos valores. Eso representa una hipotesis binaria. Si `ref = 0.5`, las dos hipotesis son aproximadamente equiprobables. Si `ref` cambia, una hipotesis aparece mas que la otra.

En el laboratorio, esto importa porque antes de transmitir por el SDR necesitamos saber que estamos mandando. Si el histograma de la senal generada no coincide con la probabilidad esperada, cualquier conclusion posterior sobre el canal queda contaminada desde el origen.

### Observacion recibida

En el Capitulo 2, el receptor no ve directamente la hipotesis transmitida. Ve una observacion. En el simulador esa observacion era algo como:

```text
y = c + n
```

En el SDR, la observacion es el array que devuelve:

```python
rx_signal = sdr.rx()
```

Ese array es la version experimental de la observacion del receptor. No es exactamente la senal transmitida: incluye ruido, ganancia, fase, posibles retardos, desbalance I/Q, imperfecciones del hardware y efectos del medio.

Por eso la practica pide graficar, hacer histogramas y mirar frecuencia: son formas de estudiar la observacion antes de decidir algo.

### Muestras complejas I/Q

El Capitulo 7 explica que una senal pasabanda real se puede representar mediante una senal compleja equivalente en banda base. Esa representacion es la que aparece en el SDR como muestras I/Q:

```text
x[n] = I[n] + j Q[n]
```

En Python eso aparece como:

```python
i_component = np.real(rx_signal)
q_component = np.imag(rx_signal)
```

La parte real es la componente en fase, `I`. La parte imaginaria es la componente en cuadratura, `Q`. No son dos senales independientes cualquiera: juntas describen amplitud y fase de la senal equivalente en banda base.

Esto explica por que la consigna insiste en graficar ambas. Si solo miramos `I`, estamos ignorando media informacion del receptor.

### Normalizacion de potencia

Bixio trabaja mucho con energia, distancia y probabilidad de error. En teoria, comparar senales tiene sentido cuando sabemos en que escala estan. En el SDR, la escala recibida puede cambiar por la ganancia de recepcion, atenuacion, distancia, cableado o configuracion interna.

Por eso hacemos:

```python
rx_power = np.mean(np.abs(rx_signal)**2)
rx_norm = rx_signal / np.sqrt(rx_power)
```

Eso fuerza a que la potencia promedio sea aproximadamente 1. La normalizacion no elimina el ruido ni arregla el canal, pero permite comparar capturas distintas con una escala comun.

La idea se conecta con el Capitulo 2 porque el criterio ML depende de distancias entre observacion y senales posibles. Si la escala cambia sin control, esas distancias cambian tambien.

### Histogramas como aproximacion experimental de densidades

En el Capitulo 2 aparecen densidades de probabilidad. En laboratorio no conocemos la densidad exacta del canal; tenemos muestras. Un histograma normalizado es una estimacion experimental de esa densidad.

Cuando escribimos:

```python
plt.hist(i_component, bins=80, density=True)
```

estamos preguntando: "con que frecuencia aparecen valores cerca de cada amplitud?". Si transmitimos niveles discretos y el canal agrega ruido, esperamos ver grupos o picos alrededor de esos niveles.

Si los picos estan muy separados, el receptor podria decidir con pocos errores. Si los picos se mezclan, la probabilidad de error aumenta.

### PSD y mirada frecuencial

El Capitulo 5 introduce la densidad espectral de potencia. La PSD responde una pregunta distinta al histograma:

- el histograma mira que valores toma la senal;
- la PSD mira donde esta la energia en frecuencia.

Cuando usamos:

```python
f, pxx = welch(signal, fs=fs, return_onesided=False)
```

estamos estimando la PSD mediante Welch. No estamos cambiando la senal; solo la estamos observando desde el dominio frecuencial.

Esto es importante en SDR porque una senal puede verse razonable en tiempo pero ocupar demasiado ancho de banda, tener componentes no deseadas o mostrar ruido fuera de la banda esperada.

### Pulso rectangular y filtrado

En el simulador del Parcial 2 usamos una funcion base rectangular:

```text
psi_1(t) = 1 en [0, T]
```

En discreto, con `T = 16 dt`, eso se vuelve:

```python
rect_pulse = np.ones(16)
```

Cuando filtramos:

```python
rx_filtered = lfilter(rect_pulse, 1, rx_norm)
```

estamos aplicando una operacion parecida a acumular energia durante 16 muestras. Esta idea se conecta con el Capitulo 3: el receptor busca una estadistica suficiente, es decir, un numero o conjunto de numeros que conserve la informacion relevante para decidir.

En un caso ideal, el correlador y el matched filter son formas distintas de llegar a esa misma estadistica.

### Potencia transmitida y relacion senal-ruido

Cuando cambiamos:

```python
sdr.tx_hardwaregain_chan0 = -70
```

estamos modificando la potencia efectiva de transmision. En la practica, eso cambia la relacion entre senal y ruido en la recepcion.

Bixio conecta esto con AWGN y probabilidad de error: si la distancia entre las senales posibles crece respecto del ruido, la decision es mas facil. Si el ruido domina, los histogramas se mezclan y el receptor se equivoca mas.

En la notebook, esto deberia verse como histogramas mas o menos separados segun la potencia transmitida.

### Decision ML en lenguaje de laboratorio

En el Capitulo 2, ML significa elegir la hipotesis que hace mas probable la observacion recibida. Para AWGN y senales equiprobables, eso suele equivaler a elegir la senal mas cercana.

En codigo binario simple:

```python
detected_i = np.where(np.real(received_signal) >= 0, 1.0, -1.0)
```

El umbral cero aparece porque los niveles teoricos son `-1` y `+1`. Si el valor recibido cae del lado positivo, decidimos `+1`; si cae del lado negativo, decidimos `-1`.

Para varios niveles, la idea es parecida:

```python
distances = np.abs(values - levels.reshape(1, -1))
nearest_indices = np.argmin(distances, axis=1)
```

Ahi el receptor compara contra todos los niveles posibles y decide el mas cercano. Esa es la version programada de la intuicion ML para niveles discretos con ruido aproximadamente gaussiano.

### Por que puede no tener sentido calcular error directamente

En simulacion, conocemos exactamente que simbolo se envio en cada posicion. En SDR real, puede haber retardo de buffer, transitorios y desalineacion temporal. Entonces comparar:

```python
detected_binary != tx_signal
```

solo tiene sentido si sabemos que ambos arrays estan alineados muestra a muestra. Si no lo estan, la probabilidad de error puede salir enorme aunque el sistema este recibiendo bien.

Esto se relaciona con el Capitulo 7.5: en sistemas reales hay que estimar parametros como sincronismo, fase, frecuencia y escala. La decision ML teorica supone que esas cosas estan controladas o estimadas.

## Punto de partida conceptual

En el simulador del Parcial 2 trabajamos con una cadena idealizada:

```text
hipotesis -> encoder -> waveform former -> canal AWGN -> receptor -> decoder ML
```

En el Laboratorio 3 hacemos algo parecido, pero ahora el canal deja de ser solamente una funcion de Python. La senal se transmite y recibe usando el SDR remoto de la facultad. Eso agrega efectos reales:

- buffers de transmision y recepcion;
- ganancia del receptor;
- atenuacion de transmision;
- muestras complejas I/Q;
- ruido real del hardware y del medio;
- transitorios al iniciar transmision continua;
- necesidad de normalizar la potencia recibida antes de comparar resultados.

## Plan por charlas

### Charla 1 - Preparar carpeta, consigna y mapa de trabajo

Que hacemos:

- crear la carpeta `Laboratorio 3`;
- crear este documento guia;
- leer la consigna y separar los puntos en tareas chicas;
- revisar que partes vienen del Laboratorio 1 y del Laboratorio 2;
- definir que notebook vamos a construir para la entrega.

Para que sirve:

- evita resolver a ciegas;
- nos deja claro que parte es teoria, que parte es SDR y que parte es analisis de datos;
- permite avanzar sin mezclar configuracion, simulacion y conclusiones.

Referencia Bixio:

- Capitulo 1: vision general del sistema de comunicaciones digitales.
- Capitulo 7: ubicacion del SDR dentro de una cadena pasabanda real.

Resultado esperado:

- carpeta creada;
- guia inicial escrita;
- lista de bloques que tendra la notebook.

### Charla 2 - Generar la senal de hipotesis compleja

Que hacemos:

- implementar el codigo que genera la senal binaria compleja de la consigna;
- usar la variable `ref` para modificar la probabilidad de ocurrencia;
- comenzar con `ref = 0.5`;
- separar parte real e imaginaria;
- graficar la senal temporal;
- hacer histogramas de componente en fase e componente en cuadratura;
- graficar la senal en frecuencia.

Para que sirve:

- permite entender que se esta transmitiendo antes de usar el SDR;
- muestra si las hipotesis son equiprobables o sesgadas;
- conecta directamente con el simulador del Parcial 2, donde generabamos hipotesis binarias.

Referencia Bixio:

- Capitulo 2.2: hypothesis testing.
- Capitulo 2.4: receiver design for the discrete-time AWGN channel.
- Capitulo 7.2: baseband-equivalent of a passband signal.
- Capitulo 7.9: complex-valued random vectors.

Resultado esperado:

- arrays de muestras complejas;
- graficas temporales de I y Q;
- histogramas normalizados;
- grafica en frecuencia o PSD;
- primera descripcion escrita de lo observado.

### Charla 3 - Conectar al SDR y transmitir/recibir

Que hacemos:

- conectarnos por VPN a la red de la facultad;
- verificar acceso al SDR remoto;
- configurar los parametros principales del dispositivo;
- transmitir la senal usando modo continuo cuando corresponda;
- realizar varias recepciones iniciales para limpiar transitorios y buffers;
- capturar la senal recibida.

Para que sirve:

- lleva el modelo ideal a un sistema fisico;
- permite ver como cambia la senal al pasar por hardware y canal real;
- evita interpretar como resultado valido una captura tomada durante un transitorio.

Referencia Bixio:

- Capitulo 3.6: continuous-time channels revisited.
- Capitulo 3.10: thermal noise.
- Capitulo 3.11: channel modeling, a case study.
- Capitulo 7.3: the third layer.
- Capitulo 7.4: baseband-equivalent channel model.

Resultado esperado:

- senal recibida compleja desde el SDR;
- confirmacion de parametros usados;
- registro claro de cuantas capturas se descartaron antes de analizar.

### Charla 4 - Normalizar potencia y analizar I/Q recibido

Que hacemos:

- normalizar la senal recibida para que tenga potencia unitaria;
- separar componente en fase `I = real(rx)` y cuadratura `Q = imag(rx)`;
- graficar ambas en tiempo;
- generar histogramas normalizados;
- graficar en frecuencia.

Para que sirve:

- la normalizacion permite comparar capturas aunque cambie la ganancia o la potencia recibida;
- las componentes I/Q muestran como el SDR representa en banda base una senal pasabanda;
- los histogramas permiten ver concentraciones, dispersion y posible ruido.

Referencia Bixio:

- Capitulo 2.10: Gaussian random vectors.
- Capitulo 3.2: white Gaussian noise.
- Capitulo 5.3: power spectral density.
- Capitulo 7.2: baseband-equivalent of a passband signal.

Resultado esperado:

- potencia normalizada cercana a 1;
- graficas temporales I/Q;
- histogramas de I/Q;
- descripcion de diferencias entre senal transmitida y recibida.

### Charla 5 - Filtrar con pulso rectangular de `2**4` muestras

Que hacemos:

- construir un pulso rectangular de 16 muestras;
- filtrar la senal recibida con ese pulso;
- graficar la salida temporal;
- generar histogramas de I y Q luego del filtrado.

Para que sirve:

- conecta directamente con el `waveform former` del simulador;
- muestra como una operacion de filtrado acumula energia de varias muestras;
- permite ver si los niveles transmitidos se separan mejor despues del filtrado.

Referencia Bixio:

- Capitulo 3.3: observables and sufficient statistics.
- Capitulo 3.4: transmitter and receiver architecture.
- Capitulo 3.5: alternative receiver structures.
- Capitulo 5.2: ideal lowpass case.
- Capitulo 5.3: power spectral density.

Resultado esperado:

- pulso rectangular implementado;
- senal filtrada;
- comparacion antes/despues del filtrado;
- interpretacion del histograma filtrado.

### Charla 6 - Aumentar potencia transmitida con `TxAtten = -70`

Que hacemos:

- repetir transmision y recepcion cambiando `TxAtten` a `-70`;
- normalizar la senal recibida;
- repetir graficas temporales, frecuencia e histogramas;
- comparar con la captura anterior.

Para que sirve:

- permite observar el efecto de la potencia de transmision sobre la nube de muestras;
- ayuda a distinguir entre ruido dominante y senal dominante;
- muestra una diferencia practica entre simulacion ideal y laboratorio real.

Referencia Bixio:

- Capitulo 3.2: white Gaussian noise.
- Capitulo 3.10: thermal noise.
- Capitulo 7.4: baseband-equivalent channel model.
- Capitulo 7.5: parameter estimation.

Resultado esperado:

- comparacion de histogramas con menor y mayor potencia;
- conclusion parcial sobre separacion de niveles y ruido.

### Charla 7 - Hipotesis equiprobable de varios niveles

Que hacemos:

- modificar el codigo para transmitir hipotesis equiprobables;
- en la consigna aparece una hipotesis del tipo:

```text
H = {-1, -0.3333, +0.3333, +1}
```

- generar la senal correspondiente;
- transmitirla y recibirla con el SDR;
- obtener histograma de la senal recibida;
- comparar la forma del histograma con los niveles esperados.

Para que sirve:

- extiende el caso binario del simulador a una senal multinivel;
- permite ver como el canal y el hardware deforman o dispersan los niveles;
- prepara el camino para discutir decision por regiones, no solo por signo.

Referencia Bixio:

- Capitulo 2.2: hypothesis testing.
- Capitulo 2.4: receiver design for the discrete-time AWGN channel.
- Capitulo 2.5: irrelevance and sufficient statistic.
- Capitulo 4.5: duration, bandwidth, and dimensionality.

Resultado esperado:

- histograma con grupos asociados a los niveles transmitidos;
- analisis de si los niveles se distinguen claramente;
- comparacion con el caso binario.

### Charla 8 - Criterio de decision y probabilidad de error si corresponde

Que hacemos:

- si la consigna o los datos lo permiten, comparar simbolos enviados contra recibidos;
- definir regiones de decision para el caso binario o multinivel;
- estimar errores;
- relacionar la decision experimental con el criterio ML visto en el simulador.

Para que sirve:

- conecta el laboratorio con el Parcial 2;
- muestra que el receptor no solo grafica, sino que decide una hipotesis;
- permite discutir cuando una decision es confiable y cuando no.

Referencia Bixio:

- Capitulo 2.3: Q function.
- Capitulo 2.4: receiver design for the discrete-time AWGN channel.
- Capitulo 2.6: error probability bounds.
- Capitulo 3.3: sufficient statistics.

Resultado esperado:

- detector simple documentado;
- si hay referencia temporal confiable, probabilidad de error estimada;
- si no hay referencia confiable, explicacion de por que no se calcula.

### Charla 9 - Conclusiones finales de la notebook

Que hacemos:

- ordenar resultados;
- revisar que cada punto de la consigna tenga grafica y comentario;
- escribir conclusiones parciales;
- cerrar con una conclusion general.

Para que sirve:

- transforma la notebook de una coleccion de graficos a un informe entendible;
- deja explicito que se observo, por que tiene sentido y que limitaciones tuvo el experimento.

Referencia Bixio:

- Capitulo 1: sistema completo y objetivos.
- Capitulo 3: canal y receptor.
- Capitulo 5: interpretacion en frecuencia.
- Capitulo 7: implementacion pasabanda/IQ en SDR.

Resultado esperado:

- notebook final entregable;
- conclusiones claras;
- parametros usados registrados;
- resultados reproducibles dentro de lo posible.

## Codigo sugerido por charla

Esta seccion esta pensada para usarla como guia cuando armemos la notebook. La idea no es copiar sin pensar: primero ejecutamos, despues miramos que salio, y finalmente escribimos una interpretacion con palabras propias.

Como analogia con programacion orientada a objetos: cada bloque de codigo funciona como un metodo de una clase grande llamada "experimento". Tiene entradas, hace una tarea concreta, y devuelve un resultado que usa el siguiente bloque.

## Primer arranque recomendado

Para empezar de forma ordenada, la primera notebook deberia avanzar solamente hasta generar y analizar la senal antes del SDR. Eso nos permite validar el transmisor sin depender todavia de la VPN.

En la primera sesion de codigo conviene ejecutar estas celdas:

- imports y parametros;
- generacion de hipotesis binarias complejas con `ref = 0.5`;
- grafica temporal de I y Q;
- histogramas de I y Q;
- PSD de la senal generada.

Cuando esas celdas funcionen, recien pasamos al SDR. Asi separamos dos problemas:

- si falla la senal generada, el problema esta en nuestro codigo local;
- si falla la recepcion, el problema puede estar en VPN, SDR, buffers, configuracion o canal.

La primera conclusion parcial que deberia quedar escrita en la notebook es algo como:

```text
Con ref = 0.5, las componentes I y Q toman valores aproximadamente equiprobables en {-1,+1}. Los histogramas muestran dos grupos principales por componente. La grafica temporal confirma que la senal generada es discreta y binaria en cada rama I/Q. La PSD permite observar la distribucion espectral de la secuencia antes de pasar por el SDR.
```

### Charla 1 - Celda inicial de imports y parametros

Codigo sugerido:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, lfilter

plt.style.use("seaborn-v0_8-whitegrid")

seed = 20260527
rng = np.random.default_rng(seed)

num_symbols = 2**14
samples_per_symbol = 2**4
ref = 0.5

fs = 1_000_000
center_freq = 2_400_000_000
rx_buffer_size = 2**20

print("Semilla:", seed)
print("Cantidad de simbolos:", num_symbols)
print("Muestras por simbolo:", samples_per_symbol)
print("ref:", ref)
print("Frecuencia de muestreo:", fs)
```

Que hace este codigo:

- `import numpy as np` carga NumPy, que usamos para trabajar con arrays numericos.
- `import matplotlib.pyplot as plt` carga la herramienta de graficos.
- `welch` sirve para estimar la PSD, es decir, como se reparte la potencia en frecuencia.
- `lfilter` sirve para aplicar filtros, por ejemplo el pulso rectangular.
- `rng` es el generador de numeros aleatorios; pensalo como un objeto que sabe generar muestras aleatorias.
- `num_symbols` define cuantas muestras/simbolos vamos a generar.
- `samples_per_symbol = 2**4` indica que cada hipotesis se repite 16 veces para formar un tren de pulsos.
- `ref` controla la probabilidad de ocurrencia de una de las hipotesis.
- `fs`, `center_freq` y `rx_buffer_size` son parametros que despues se usan con el SDR.

Que deberias ver al ejecutarlo:

- no deberia aparecer ningun grafico todavia;
- deberias ver impresos los parametros principales;
- si falla en `scipy`, falta instalar/importar dependencias en el entorno de Jupyter.

Relacion con Bixio:

- Capitulo 1: define el sistema completo.
- Capitulo 7: `fs` y `center_freq` pertenecen a la implementacion pasabanda/IQ del SDR.

### Charla 2 - Generar hipotesis binarias complejas

Codigo sugerido:

```python
def generate_repeated_complex_binary_signal(num_symbols, samples_per_symbol, ref, rng):
    z = rng.uniform(size=num_symbols)
    x = np.array([1 if z_i > ref else 0 for z_i in z])

    pulse_train = 2 * np.repeat(x, samples_per_symbol) - 1
    signal = pulse_train + 1j * pulse_train
    return signal, x, z


tx_signal, tx_bits, z = generate_repeated_complex_binary_signal(
    num_symbols,
    samples_per_symbol,
    ref,
    rng,
)

print("Primeros 20 bits generados:")
print(tx_bits[:20])
print("Primeras 40 muestras complejas del tren de pulsos:")
print(tx_signal[:40])
print("Longitud de la secuencia binaria:", len(tx_bits))
print("Longitud del tren de pulsos:", len(tx_signal))
print("Valores posibles en I:", np.unique(np.real(tx_signal)))
print("Valores posibles en Q:", np.unique(np.imag(tx_signal)))
```

Que hace este codigo:

- La funcion `generate_repeated_complex_binary_signal` implementa la idea del codigo de la consigna.
- `z = rng.uniform(size=num_symbols)` genera numeros aleatorios uniformes entre 0 y 1.
- `x = np.array([1 if z_i > ref else 0 for z_i in z])` convierte esos numeros en hipotesis binarias `0` o `1`.
- Esta linea usa una lista por comprension de Python: es parecida a un `for` que va armando una lista.
- `np.repeat(x, samples_per_symbol)` repite cada bit 16 veces.
- `2 * ... - 1` transforma los bits `0` y `1` en niveles antipodales `-1` y `+1`.
- `pulse_train + 1j * pulse_train` arma una senal compleja donde I y Q tienen el mismo tren de pulsos.
- `tx_bits` guarda la secuencia binaria original y `tx_signal` guarda el tren de pulsos complejo listo para transmitir.

Que deberias ver al ejecutarlo:

- una secuencia `tx_bits` con ceros y unos;
- muestras complejas como `1+1j` o `-1-1j`;
- bloques repetidos de 16 muestras iguales;
- la longitud de `tx_signal` deberia ser `num_symbols * samples_per_symbol`;
- en I deberian aparecer los valores `[-1.  1.]`;
- en Q tambien deberian aparecer `[-1.  1.]`;
- con `ref = 0.5`, aproximadamente la mitad de los bits deberia ser `0` y la otra mitad `1`.

Relacion con Bixio:

- Capitulo 2.2: las hipotesis son los valores posibles que puede tomar la senal.
- Capitulo 7.2: una muestra compleja representa una senal equivalente en banda base.
- Capitulo 7.9: las muestras complejas pueden pensarse como vectores aleatorios complejos.

### Charla 2 - Graficas de la senal generada

Codigo sugerido:

```python
def plot_iq_time(signal, title, n_preview=200):
    n = np.arange(n_preview)
    i_component = np.real(signal[:n_preview])
    q_component = np.imag(signal[:n_preview])

    fig, axes = plt.subplots(2, 1, figsize=(12, 6), constrained_layout=True)

    axes[0].step(n, i_component, where="post")
    axes[0].set_title(title + " - componente I")
    axes[0].set_xlabel("Indice de muestra")
    axes[0].set_ylabel("I[n]")
    axes[0].grid(True)

    axes[1].step(n, q_component, where="post", color="C1")
    axes[1].set_title(title + " - componente Q")
    axes[1].set_xlabel("Indice de muestra")
    axes[1].set_ylabel("Q[n]")
    axes[1].grid(True)

    plt.show()


plot_iq_time(tx_signal, "Senal transmitida generada")
```

Que hace este codigo:

- Define una funcion reutilizable para graficar I y Q.
- `np.real(signal)` toma la parte real de la senal compleja.
- `np.imag(signal)` toma la parte imaginaria.
- `plt.subplots(2, 1)` crea dos graficos, uno arriba del otro.
- `step` dibuja escalones, que queda mejor para simbolos discretos.

Que deberias ver al ejecutarlo:

- dos graficas temporales;
- ambas deberian saltar entre `-1` y `+1`;
- si `ref = 0.5`, no deberia verse un nivel mucho mas frecuente que el otro.

Relacion con Bixio:

- Capitulo 2: observaciones discretas.
- Capitulo 7: representacion I/Q en banda base.

### Charla 2 - Histogramas y frecuencia de la senal generada

Codigo sugerido:

```python
def plot_iq_histograms(signal, title, bins=40):
    i_component = np.real(signal)
    q_component = np.imag(signal)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)

    axes[0].hist(i_component, bins=bins, density=True, alpha=0.75, edgecolor="black")
    axes[0].set_title(title + " - histograma I")
    axes[0].set_xlabel("I")
    axes[0].set_ylabel("Densidad")
    axes[0].grid(True)

    axes[1].hist(q_component, bins=bins, density=True, alpha=0.75, edgecolor="black", color="C1")
    axes[1].set_title(title + " - histograma Q")
    axes[1].set_xlabel("Q")
    axes[1].set_ylabel("Densidad")
    axes[1].grid(True)

    plt.show()


def plot_psd(signal, fs, title):
    f, pxx = welch(signal, fs=fs, nperseg=1024, return_onesided=False)
    f_shift = np.fft.fftshift(f)
    pxx_shift = np.fft.fftshift(pxx)

    plt.figure(figsize=(12, 4))
    plt.semilogy(f_shift, pxx_shift)
    plt.title(title)
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("PSD")
    plt.grid(True)
    plt.show()


plot_iq_histograms(tx_signal, "Senal transmitida")
plot_psd(tx_signal, fs, "PSD de la senal transmitida")
```

Que hace este codigo:

- `hist(..., density=True)` normaliza el histograma para que el area sea 1.
- Los histogramas muestran cuantas muestras caen cerca de cada valor.
- `welch` estima la densidad espectral de potencia.
- `return_onesided=False` es importante porque la senal es compleja y queremos frecuencias positivas y negativas.
- `fftshift` reordena el eje para que la frecuencia cero quede en el centro.

Que deberias ver al ejecutarlo:

- histogramas con picos alrededor de `-1` y `+1`;
- una PSD con energia distribuida segun la secuencia generada;
- si cambias `ref`, los picos del histograma dejan de tener alturas parecidas.

Relacion con Bixio:

- Capitulo 5.3: power spectral density.
- Capitulo 7.2: senal equivalente en banda base compleja.

### Charla 3 - Configurar el SDR

Codigo sugerido:

```python
import adi

uri = "ip:192.168.1.32"

sdr = adi.Pluto(uri)

sdr.sample_rate = int(fs)
sdr.rx_lo = int(center_freq)
sdr.tx_lo = int(center_freq)
sdr.rx_buffer_size = int(rx_buffer_size)

sdr.tx_cyclic_buffer = True
sdr.gain_control_mode_chan0 = "manual"
sdr.rx_hardwaregain_chan0 = 70
sdr.tx_hardwaregain_chan0 = -80

print("SDR conectado en:", uri)
print("sample_rate:", sdr.sample_rate)
print("rx_lo:", sdr.rx_lo)
print("tx_lo:", sdr.tx_lo)
print("rx_buffer_size:", sdr.rx_buffer_size)
print("tx_cyclic_buffer:", sdr.tx_cyclic_buffer)
```

Que hace este codigo:

- `import adi` carga la libreria `pyadi-iio`, que permite hablar con el SDR.
- `adi.Pluto(uri)` crea un objeto SDR conectado a la IP indicada.
- `sdr.sample_rate` define cuantas muestras por segundo usa el equipo.
- `rx_lo` y `tx_lo` definen la frecuencia central de recepcion y transmision.
- `rx_buffer_size` define cuantas muestras trae cada captura.
- `tx_cyclic_buffer = True` hace que el SDR repita continuamente la senal transmitida.
- `gain_control_mode_chan0 = "manual"` evita que el SDR cambie solo la ganancia.
- `rx_hardwaregain_chan0` define ganancia de recepcion.
- `tx_hardwaregain_chan0` define potencia/atenuacion de transmision.

Que deberias ver al ejecutarlo:

- si estas conectado por VPN y el SDR esta disponible, deberia imprimir los parametros;
- si falla con error de conexion, revisar VPN, IP o que otro usuario no este usando el SDR;
- si falla en `import adi`, falta instalar `pyadi-iio` o estas en un entorno incorrecto.

Relacion con Bixio:

- Capitulo 7.3: tercera capa, implementacion fisica con conversion de frecuencia.
- Capitulo 7.5: parametros que en la practica hay que estimar o configurar.

### Charla 3 - Transmitir y recibir evitando transitorios

Codigo sugerido:

```python
def normalize_for_sdr(signal, scale=2**14):
    signal = signal / np.max(np.abs(signal))
    return signal * scale


tx_for_sdr = normalize_for_sdr(tx_signal)

sdr.tx_destroy_buffer()
sdr.tx(tx_for_sdr)

for _ in range(5):
    _ = sdr.rx()

rx_signal = sdr.rx()

print("Muestras recibidas:", len(rx_signal))
print("Primeras 10 muestras recibidas:")
print(rx_signal[:10])
```

Que hace este codigo:

- `normalize_for_sdr` escala la senal para que el SDR pueda transmitirla con buena amplitud.
- `np.max(np.abs(signal))` busca la mayor magnitud de la senal.
- Dividir por ese valor evita saturar.
- Multiplicar por `2**14` lleva la senal a una escala usual para el Pluto/ADI.
- `tx_destroy_buffer()` borra el buffer de transmision anterior.
- `sdr.tx(tx_for_sdr)` envia la senal al transmisor.
- El bucle `for _ in range(5)` descarta varias recepciones iniciales.
- `rx_signal = sdr.rx()` guarda la captura que vamos a analizar.

Que deberias ver al ejecutarlo:

- un array complejo recibido;
- la longitud deberia ser cercana a `rx_buffer_size`;
- las primeras capturas descartadas no se grafican porque pueden venir contaminadas por estados transitorios o buffers viejos.

Relacion con Bixio:

- Capitulo 3.6: el canal real se observa a traves de muestras.
- Capitulo 7.4: el canal pasabanda se analiza mediante su equivalente banda base.

### Charla 4 - Normalizar potencia recibida

Codigo sugerido:

```python
def average_power(signal):
    return np.mean(np.abs(signal)**2)


rx_power = average_power(rx_signal)
rx_norm = rx_signal / np.sqrt(rx_power)

print("Potencia antes de normalizar:", rx_power)
print("Potencia despues de normalizar:", average_power(rx_norm))
```

Que hace este codigo:

- `np.abs(signal)` calcula la magnitud de cada muestra compleja.
- `np.abs(signal)**2` calcula potencia instantanea.
- `np.mean(...)` calcula potencia promedio.
- `rx_signal / np.sqrt(rx_power)` divide por la raiz de la potencia para que la nueva potencia sea aproximadamente 1.

Que deberias ver al ejecutarlo:

- la potencia antes puede ser cualquier valor;
- la potencia despues deberia quedar muy cerca de `1.0`;
- si aparece `nan` o infinito, probablemente `rx_signal` esta vacia o tiene potencia cero.

Relacion con Bixio:

- Capitulo 2.4: las decisiones dependen de distancias y energia.
- Capitulo 7.4: el canal equivalente puede cambiar escala y fase de la senal.

### Charla 4 - Graficar I/Q recibido e histogramas

Codigo sugerido:

```python
plot_iq_time(rx_norm, "Senal recibida normalizada", n_preview=500)
plot_iq_histograms(rx_norm, "Senal recibida normalizada", bins=80)
plot_psd(rx_norm, fs, "PSD de la senal recibida normalizada")
```

Que hace este codigo:

- Reutiliza funciones que ya definimos.
- Grafica la parte real e imaginaria de la senal recibida.
- Muestra histogramas de I y Q.
- Calcula la PSD de la captura recibida.

Que deberias ver al ejecutarlo:

- la senal recibida no deberia verse tan limpia como la transmitida;
- los histogramas pueden tener picos ensanchados por ruido y canal;
- la PSD puede mostrar energia concentrada y tambien ruido de fondo.

Relacion con Bixio:

- Capitulo 3.2: ruido blanco gaussiano.
- Capitulo 5.3: PSD.
- Capitulo 7.2: representacion I/Q.

### Charla 5 - Filtrar con pulso rectangular de 16 muestras

Codigo sugerido:

```python
Ns = 2**4
rect_pulse = np.ones(Ns)

rx_filtered = lfilter(rect_pulse, 1, rx_norm)

print("Longitud del pulso rectangular:", len(rect_pulse))
print("Primeras muestras del pulso:", rect_pulse)

plot_iq_time(rx_filtered, "Senal recibida filtrada con pulso rectangular", n_preview=500)
plot_iq_histograms(rx_filtered, "Senal recibida filtrada", bins=80)
plot_psd(rx_filtered, fs, "PSD de la senal recibida filtrada")
```

Que hace este codigo:

- `Ns = 2**4` define 16 muestras.
- `np.ones(Ns)` crea un pulso rectangular: un array de 16 unos.
- `lfilter(rect_pulse, 1, rx_norm)` aplica el filtro a la senal recibida.
- En terminos simples, el filtro va sumando bloques cercanos de muestras.

Que deberias ver al ejecutarlo:

- la senal filtrada suele tener amplitudes mas grandes porque acumula energia;
- los histogramas pueden mostrar grupos mas separados si la senal esta bien sincronizada;
- tambien puede aparecer mayor suavizado temporal.

Relacion con Bixio:

- Capitulo 3.3: estadisticas suficientes.
- Capitulo 3.5: matched filter y estructuras alternativas.
- Capitulo 5.2: tren de pulsos e ideal lowpass.

### Charla 6 - Repetir con mayor potencia transmitida

Codigo sugerido:

```python
sdr.tx_destroy_buffer()
sdr.tx_hardwaregain_chan0 = -70
sdr.tx(tx_for_sdr)

for _ in range(5):
    _ = sdr.rx()

rx_signal_high_power = sdr.rx()
rx_high_power_norm = rx_signal_high_power / np.sqrt(average_power(rx_signal_high_power))

plot_iq_time(rx_high_power_norm, "Senal recibida con TxAtten = -70", n_preview=500)
plot_iq_histograms(rx_high_power_norm, "Senal recibida con TxAtten = -70", bins=80)
plot_psd(rx_high_power_norm, fs, "PSD con TxAtten = -70")
```

Que hace este codigo:

- Borra el buffer anterior.
- Cambia la ganancia/atenuacion de transmision a `-70`.
- Transmite la misma senal.
- Descarta capturas iniciales para evitar transitorios.
- Normaliza la nueva recepcion.
- Repite graficas para comparar.

Que deberias ver al ejecutarlo:

- los histogramas pueden mostrar niveles mas definidos;
- puede verse mejor separacion entre grupos de muestras;
- si aparece saturacion, la nube se deforma y los histogramas pueden cortarse o aplastarse.

Relacion con Bixio:

- Capitulo 3.10: ruido termico y relacion senal/ruido.
- Capitulo 7.4: ganancia, escala y canal equivalente.

### Charla 7 - Hipotesis equiprobable multinivel

Codigo sugerido:

```python
def generate_multilevel_signal(num_symbols, rng):
    levels = np.array([-1.0, -1.0/3.0, 1.0/3.0, 1.0])
    indices_i = rng.integers(0, len(levels), num_symbols)
    indices_q = rng.integers(0, len(levels), num_symbols)

    i_component = levels[indices_i]
    q_component = levels[indices_q]

    signal = i_component + 1j * q_component
    return signal, levels


tx_multilevel, levels = generate_multilevel_signal(num_symbols, rng)

print("Niveles posibles:", levels)
print("Primeras 10 muestras multinivel:")
print(tx_multilevel[:10])

plot_iq_time(tx_multilevel, "Senal multinivel generada", n_preview=200)
plot_iq_histograms(tx_multilevel, "Senal multinivel generada", bins=80)
plot_psd(tx_multilevel, fs, "PSD de la senal multinivel generada")
```

Que hace este codigo:

- `levels` guarda los cuatro valores posibles de la hipotesis.
- `rng.integers(0, len(levels), num_symbols)` elige indices aleatorios entre 0 y 3.
- Usar indices permite seleccionar valores del array `levels`.
- Se genera una componente I multinivel y una componente Q multinivel.
- Se combinan como muestra compleja `I + jQ`.

Que deberias ver al ejecutarlo:

- los valores de I y Q deberian pertenecer a `-1`, `-0.3333`, `0.3333`, `1`;
- los histogramas deberian tener cuatro grupos principales;
- si la cantidad de muestras es grande, los grupos deberian tener alturas parecidas.

Relacion con Bixio:

- Capitulo 2.2: hipotesis multiples.
- Capitulo 2.4: decision en AWGN.
- Capitulo 4.5: dimension, duracion y compromiso de diseno.

### Charla 7 - Transmitir la senal multinivel

Codigo sugerido:

```python
tx_multilevel_for_sdr = normalize_for_sdr(tx_multilevel)

sdr.tx_destroy_buffer()
sdr.tx_hardwaregain_chan0 = -70
sdr.tx(tx_multilevel_for_sdr)

for _ in range(5):
    _ = sdr.rx()

rx_multilevel = sdr.rx()
rx_multilevel_norm = rx_multilevel / np.sqrt(average_power(rx_multilevel))

plot_iq_time(rx_multilevel_norm, "Senal multinivel recibida", n_preview=500)
plot_iq_histograms(rx_multilevel_norm, "Senal multinivel recibida", bins=100)
plot_psd(rx_multilevel_norm, fs, "PSD de la senal multinivel recibida")
```

Que hace este codigo:

- Escala la senal multinivel para transmitirla con el SDR.
- Borra buffers anteriores.
- Transmite con `TxAtten = -70`.
- Descarta capturas transitorias.
- Captura la senal recibida.
- Normaliza potencia y grafica.

Que deberias ver al ejecutarlo:

- los histogramas deberian tender a mostrar cuatro regiones por componente;
- en el SDR real los niveles pueden desplazarse, rotarse o ensancharse;
- si el canal esta muy ruidoso, los cuatro grupos pueden mezclarse.

Relacion con Bixio:

- Capitulo 2.4: decision entre varias hipotesis.
- Capitulo 7.5: estimacion de parametros practicos como escala y fase.

### Charla 8 - Decision simple y probabilidad de error si hay alineacion

Codigo sugerido para caso binario:

```python
def binary_ml_decoder_iq(received_signal):
    detected_i = np.where(np.real(received_signal) >= 0, 1.0, -1.0)
    detected_q = np.where(np.imag(received_signal) >= 0, 1.0, -1.0)
    return detected_i + 1j * detected_q


detected_binary = binary_ml_decoder_iq(rx_norm[:len(tx_signal)])
reference_binary = tx_signal[:len(detected_binary)]

symbol_errors = np.sum(detected_binary != reference_binary)
symbol_error_probability = symbol_errors / len(reference_binary)

print("Errores simbolicos:", symbol_errors)
print("Probabilidad de error simbolica:", symbol_error_probability)
```

Que hace este codigo:

- Decide cada componente usando umbral cero.
- Si I recibida es positiva, decide `+1`; si es negativa, decide `-1`.
- Hace lo mismo con Q.
- Reconstruye una muestra compleja decidida.
- Compara contra la senal transmitida.

Que deberias ver al ejecutarlo:

- solo tiene sentido si la senal recibida esta alineada con la transmitida;
- si no hay sincronismo, puede dar muchos errores aunque el receptor funcione;
- si el canal rota la constelacion, tambien puede fallar porque el umbral cero ya no alcanza.

Relacion con Bixio:

- Capitulo 2.4: criterio ML para AWGN.
- Capitulo 3.3: estadistica suficiente antes de decidir.
- Capitulo 7.5: necesidad de estimar fase, escala y sincronismo.

Codigo sugerido para caso multinivel:

```python
def nearest_level_decoder(values, levels):
    values = values.reshape(-1, 1)
    distances = np.abs(values - levels.reshape(1, -1))
    nearest_indices = np.argmin(distances, axis=1)
    return levels[nearest_indices]


detected_i = nearest_level_decoder(np.real(rx_multilevel_norm[:len(tx_multilevel)]), levels)
detected_q = nearest_level_decoder(np.imag(rx_multilevel_norm[:len(tx_multilevel)]), levels)
detected_multilevel = detected_i + 1j * detected_q

reference_multilevel = tx_multilevel[:len(detected_multilevel)]

multilevel_errors = np.sum(detected_multilevel != reference_multilevel)
multilevel_error_probability = multilevel_errors / len(reference_multilevel)

print("Errores multinivel:", multilevel_errors)
print("Probabilidad de error multinivel:", multilevel_error_probability)
```

Que hace este codigo:

- Para cada valor recibido busca cual nivel teorico esta mas cerca.
- `reshape(-1, 1)` convierte el array en columna para comparar todos contra todos.
- `np.argmin` devuelve el indice del nivel con menor distancia.
- Luego compara contra la secuencia enviada.

Que deberias ver al ejecutarlo:

- si hay sincronismo y buena recepcion, la probabilidad de error deberia ser baja;
- si no hay alineacion temporal, la comparacion no es confiable;
- si los histogramas muestran niveles mezclados, la probabilidad de error sube.

Relacion con Bixio:

- Capitulo 2.2: decision entre hipotesis.
- Capitulo 2.6: probabilidad de error.

### Charla 9 - Celda de conclusiones guiadas

Codigo sugerido:

```python
print("Resumen para redactar conclusiones")
print("--------------------------------")
print("ref usado:", ref)
print("Cantidad de simbolos:", num_symbols)
print("Frecuencia de muestreo:", fs)
print("Frecuencia central:", center_freq)
print("Buffer RX:", rx_buffer_size)
print("Potencia RX normalizada:", average_power(rx_norm))

if "symbol_error_probability" in globals():
    print("Probabilidad de error binaria:", symbol_error_probability)

if "multilevel_error_probability" in globals():
    print("Probabilidad de error multinivel:", multilevel_error_probability)
```

Que hace este codigo:

- Junta los parametros principales en una salida corta.
- Evita que al final de la notebook queden datos importantes dispersos.
- `globals()` pregunta si una variable existe en la notebook antes de imprimirla.

Que deberias ver al ejecutarlo:

- un resumen de parametros;
- si calculaste errores, tambien deberian aparecer;
- este resumen sirve como base para escribir la conclusion final.

Relacion con Bixio:

- Capitulo 1: interpretar el sistema completo.
- Capitulos 2, 3, 5 y 7: unir decision, canal, espectro e implementacion SDR.

## Estructura sugerida de la notebook

La notebook del Laboratorio 3 deberia quedar con una estructura parecida a esta:

```text
1. Introduccion y objetivos
2. Configuracion de parametros
3. Generacion de hipotesis complejas
4. Graficas de la senal transmitida
5. Configuracion SDR
6. Transmision y recepcion
7. Normalizacion de potencia
8. Analisis temporal I/Q
9. Analisis frecuencial / PSD
10. Histogramas normalizados
11. Filtrado rectangular de 16 muestras
12. Comparacion con mayor potencia transmitida
13. Hipotesis equiprobable multinivel
14. Analisis de decision si corresponde
15. Conclusiones
```

## Checklist de aprendizaje

Antes de considerar terminada la practica, deberiamos poder responder:

- Que representa una muestra compleja I/Q.
- Por que el SDR entrega una senal en banda base equivalente.
- Que cambia entre una senal simulada y una senal recibida por hardware real.
- Por que se normaliza la potencia recibida.
- Que informacion aporta un histograma.
- Que informacion aporta una grafica en frecuencia o PSD.
- Que efecto tiene filtrar con un pulso rectangular de 16 muestras.
- Que cambia al aumentar la potencia transmitida.
- Como se relaciona una hipotesis binaria/multinivel con una regla de decision.
- En que parte del Bixio esta la teoria que justifica cada bloque.

## Notas pendientes para completar durante la practica

- Confirmar la IP final del SDR y los parametros reales usados en la sesion.
- Confirmar si el punto 5 de la consigna tiene texto adicional que no quedo claro al extraer el PDF.
- Registrar capturas descartadas por transitorios.
- Guardar siempre los valores de `TxAtten`, ganancia RX, frecuencia central, frecuencia de muestreo y tamano de buffer.
- Escribir conclusiones con observaciones propias, no solo con frases teoricas.
