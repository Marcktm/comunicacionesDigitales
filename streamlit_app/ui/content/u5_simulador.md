## Simulador BPSK + AWGN extremo a extremo

> **Referencias.** Notebook `simulador_sistema_comunicaciones_digitales.ipynb` (Parcial 2 del
> repo); integra Unidades 2, 3 y 5. Toda la cadena, etapa por etapa, con la teoría de cada
> bloque.

---

### 1. La cadena y de dónde sale cada bloque

$$
\text{fuente}\;\to\;\text{encoder}\;\to\;\text{waveform former}\;\to\;\text{canal AWGN}\;\to\;
\text{matched filter}\;\to\;\text{muestreo}\;\to\;\text{decisor ML}
$$

1. **Fuente:** bits equiprobables $\{0,1\}$ (la $H$ de la Unidad 2).
2. **Encoder antipodal (BPSK):** $0\to-1$, $1\to+1$: constelación de dos puntos con
   $d=2$ a energía unitaria — la mejor decisión binaria posible a igual energía (Unidad 2).
3. **Waveform former:** pulso rectangular de $N_s$ muestras y **energía 1**
   ($\psi[k]=1/\sqrt{N_s}$): tren de pulsos $\sum_j s_j\psi(t-jT)$ (esta Unidad). El rectángulo
   es ortogonal a sus traslados (no se solapan) ⇒ no hay ISI de diseño.
4. **Canal AWGN:** suma ruido gaussiano por muestra, $\sigma^2$ (Unidad 3, versión discreta).
5. **Matched filter:** el mismo rectángulo invertido (Unidad 3, §3.5): maximiza la SNR en el
   instante de muestreo.
6. **Muestreo en los instantes de decisión:** al final de cada símbolo, donde la salida del
   filtro vale $s_j$ + ruido.
7. **Decisor ML:** signo de la muestra (umbral en 0, priori uniforme — Unidad 2).

---

### 2. La predicción teórica (y por qué)

Con pulso y matched filter de energía unitaria, la muestra de decisión es

$$
Z_j=s_j+N_j,\qquad N_j\sim\mathcal N(0,\sigma^2)
$$

(el Lema del ruido blanco: proyectar sobre una función de norma 1 da varianza $\sigma^2$). Es
la decisión antipodal escalar con $d=2$:

$$
\boxed{\;P_e=Q\!\left(\frac{d}{2\sigma}\right)=Q\!\left(\frac{1}{\sigma}\right).\;}
$$

El simulador **cuenta errores** y compara contra esta fórmula: es la validación Monte Carlo de
todo el edificio (Unidad 2 + 3 + 5 juntas).

---

### 3. Qué mirar en cada etapa (las gráficas)

- **TX**: el tren de pulsos rectangulares (niveles $\pm 1/\sqrt{N_s}$).
- **RX**: lo mismo enterrado en ruido — a simple vista puede no verse nada (¡el punto del GPS
  de la Unidad 2!).
- **Salida del matched filter**: triángulos por símbolo; en los instantes de decisión los
  valores se separan hacia $\pm1$.
- **Muestras de decisión**: histograma bimodal (dos gaussianas en $\pm1$) — la Figura de la
  decisión binaria, generada por el sistema completo.
- **PSD del tren transmitido** (Welch): $\propto\operatorname{sinc}^2(fT)$, como predice la
  fórmula de la PSD con símbolos incorrelacionados.

---

### 4. Para el pizarrón

1. Cadena completa y qué teoría justifica cada bloque (2: fuente/decisor; 3: canal/matched
   filter; 5: tren de pulsos/PSD).
2. Muestra de decisión $=s_j+\mathcal N(0,\sigma^2)$ ⇒ $P_e=Q(1/\sigma)$.
3. Monte Carlo ≈ teoría = validación del modelo.
