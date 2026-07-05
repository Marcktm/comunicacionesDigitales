## Tren de pulsos y teorema de muestreo

> **Referencias.** Bixio Rimoldi §5.1–§5.2 (**págs. 159–163**; el canal pasa-bajo es la
> **Fig. 5.1, pág. 160** y el esquema símbolo a símbolo la **Fig. 5.2, pág. 161**).

---

### 1. El problema de este capítulo: diseñar el pulso

Hasta ahora la base $\{\psi_j\}$ era arbitraria. Este capítulo se enfoca en el **diseño de la
señal**: usar **un solo pulso** $\psi(t)$ repetido y desplazado cada $T$ segundos,

$$
\boxed{\;w(t)=\sum_{j} s_j\,\psi(t-jT)\;}
$$

("**símbolo a símbolo sobre un tren de pulsos**"). Se omite el índice de mensaje porque las
propiedades que estudiamos (del pulso y del proceso) no dependen del mensaje; $s_j$ es el
**símbolo** j-ésimo. La señalización PAM/QAM/PSK real es esto, con los $s_j$ en el alfabeto que
corresponda.

---

### 2. El canal ideal pasa-bajo

Modelo (Fig. 5.1): un filtro ideal con $h_{\mathcal F}(f)=1$ para $|f|\le B$ y 0 afuera, más AWGN.
Como el canal elimina todo lo que esté fuera de $[-B,B]$, sin pérdida de optimalidad usamos
**señales limitadas en banda** a $[-B,B]$. Y para ellas existe una descripción por números:

---

### 3. Teorema de muestreo

> Si $w(t)$ es continua, de energía finita y su transformada se anula fuera de $[-B,B]$,
> entonces $w(t)$ se **reconstruye exactamente** de sus muestras tomadas cada $T\le\tfrac{1}{2B}$:
>
> $$
> w(t)=\sum_{n=-\infty}^{\infty} w(nT)\,\operatorname{sinc}\!\Big(\frac{t}{T}-n\Big),
> \qquad \operatorname{sinc}(x)=\frac{\sin\pi x}{\pi x}.
> $$

**Lectura:** una señal limitada en banda no tiene infinitos grados de libertad: queda
**totalmente determinada** por una secuencia de números. La reconstrucción es una interpolación:
cada muestra "se esparce" con un sinc centrado en $nT$ y se suman.

**Normalización.** El sinc del teorema no tiene energía 1. Definiendo

$$
\psi(t)=\frac{1}{\sqrt T}\,\operatorname{sinc}\Big(\frac{t}{T}\Big),
$$

el conjunto $\{\psi(t-jT)\}_{j\in\mathbb Z}$ es **ortonormal**, y la reconstrucción se reescribe

$$
w(t)=\sum_j s_j\,\psi(t-jT),\qquad s_j=w(jT)\sqrt T .
$$

**Conclusión clave:** *muestrear = proyectar sobre la base ortonormal de sincs desplazados*. Las
muestras son (a escala) los coeficientes de la expansión ortonormal.

---

### 4. Del teorema al transmisor (el teorema "al revés")

En el uso típico del teorema, primero se muestrea y después se reconstruye. En comunicaciones
**se invierte el orden** (Fig. 5.2): el transmisor hace la (re)construcción primero (el waveform
former interpola los $s_j$), la señal viaja, y el **receptor** muestrea (el n-tuple former
proyecta con el matched filter y muestrea en $t=jT$).

Además $\psi^*(-t)=\psi(t)$ (el sinc es par y real) y su transformada es
$\psi_{\mathcal F}(f)=\sqrt T$ para $|f|\le\tfrac{1}{2T}$ (0 afuera): **el matched filter es un
filtro pasa-bajo** — hace exactamente lo razonable: eliminar el ruido fuera de banda.

---

### 5. La conexión con el SDR

El teorema de muestreo es el **fundamento de la radio definida por software**: cualquier estándar
(GSM, LTE, WiFi, …) queda descrito por una **secuencia de números**; el hardware que convierte
números↔ondas (DAC/ADC + filtros) es **genérico**, y el estándar vive en el **software** del
encoder/decoder. Es exactamente el Pluto de la Unidad 4.

---

### 6. Para el pizarrón

1. Señalización símbolo a símbolo: $w(t)=\sum_j s_j\psi(t-jT)$.
2. Canal pasa-bajo ideal ⇒ señales limitadas en banda.
3. **Teorema de muestreo** ($T\le 1/2B$) + fórmula de reconstrucción con sinc.
4. $\psi=\tfrac{1}{\sqrt T}\operatorname{sinc}(t/T)$ ortonormal ⇒ muestrear = proyectar.
5. TX reconstruye primero, RX muestrea después; matched filter = pasa-bajo.
6. SDR: el estándar en software, el hardware genérico.
