## Lab 3 — Muestreo, aliasing y filtrado

> **Referencias.** Notebooks `laboratorio3.ipynb` / `laboratorio3_sdr.ipynb` del repo; teorema
> de muestreo en Bixio §5.2 (**págs. 160–163**). El lado práctico del teorema: qué pasa cuando
> **no** se cumple.

---

### 1. El teorema, del lado del que muestrea

Para reconstruir una señal limitada a $[-B,B]$ hacen falta muestras cada
$T\le\tfrac{1}{2B}$, es decir una **tasa** $F_s\ge 2B$ (la *tasa de Nyquist*). En el SDR esto es
literal: `sample_rate` define qué ancho de banda podés representar; el AD9363 filtra
(analógico + FIR) antes del ADC justamente para que a éste no le llegue nada fuera de banda.

---

### 2. Aliasing: la frecuencia disfrazada

Si muestreás un tono de frecuencia $F_c$ con $F_s<2F_c$, las muestras son **indistinguibles** de
las de otro tono de menor frecuencia. Formalmente, muestrear pliega el eje de frecuencias módulo
$F_s$: el tono aparece en

$$
F_{\text{alias}}=\big|\,F_c-k\,F_s\,\big|\quad\text{con }k=\operatorname{round}(F_c/F_s),
$$

siempre dentro de $[0,F_s/2]$. **Una vez muestreado, el daño es irreversible**: ningún
procesamiento posterior distingue el alias del tono verdadero — por eso el filtro
**anti-alias va antes** del muestreo.

---

### 3. Filtrado digital: qué hace un pasa-bajos con una señal "cuadrada"

Una onda cuadrada de período $T_0$ tiene armónicos impares en $f_0,3f_0,5f_0,\dots$
($f_0=1/T_0$) con amplitudes $\propto 1/n$. Un filtro pasa-bajos con corte entre $f_0$ y $3f_0$
deja pasar sólo el **fundamental**: la cuadrada sale **senoidal**. Con corte más alto pasan
$3f_0, 5f_0,\dots$ y la forma se va "cuadrando" (con las ondulaciones de Gibbs en los flancos).
Es el experimento clásico del Lab 3 para *ver* qué hace un filtro.

---

### 4. En el SDR real

El Lab 3 con hardware repite estas ideas sobre el Pluto: transmitir un tono cerca de $F_s/2$ y
ver el alias al bajar `sample_rate`; transmitir la cuadrada y ver cómo los filtros de la cadena
(RF bandwidth, FIR) redondean los flancos. La página del **diagrama de ojo** ya usa esta
infraestructura; acá el foco es muestreo/filtros.

---

### 5. Para el pizarrón

1. Reconstrucción exige $F_s\ge 2B$ (Nyquist).
2. Submuestreo ⇒ alias en $|F_c-kF_s|\in[0,F_s/2]$; irreversible ⇒ anti-alias **antes** del ADC.
3. Cuadrada = armónicos impares $\propto 1/n$; el pasa-bajos elige cuántos sobreviven.
4. En el Pluto: `sample_rate` y `rf_bandwidth` son estas dos ideas hechas registro.
