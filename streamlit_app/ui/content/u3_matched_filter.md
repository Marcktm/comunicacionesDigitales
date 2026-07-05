## Filtro apareado (matched filter) y estructuras del receptor

> **Referencias.** Bixio Rimoldi §3.5 (*Generalization and alternative receiver structures*,
> **págs. 107–111**; correlador vs filtro apareado: **Fig. 3.6, pág. 107**; ejemplo PAM binaria:
> **Fig. 3.8, pág. 108**; arquitecturas: **Fig. 3.9, pág. 109**).

---

### 1. Tres tests MAP equivalentes

Con $Y_j=\langle R,\psi_j\rangle$, el observable es $Y=c_i+Z$, $\sigma^2=N_0/2$, y

$$
f_{Y\mid H}(y\mid i)=\frac{1}{(2\pi\sigma^2)^{n/2}}\exp\!\left\{-\frac{\lVert y-c_i\rVert^2}{2\sigma^2}\right\}.
$$

El MAP maximiza $P_H(i)f_{Y\mid H}(y\mid i)$. Tomando $\ln$, descartando lo que no depende de
$i$ y escalando por $-N_0$ (negativo ⇒ max→min), quedan tres formas equivalentes:

**(i) Distancia penalizada:**
$\displaystyle \hat H=\arg\min_j\big[\lVert y-c_j\rVert^2-N_0\ln P_H(j)\big]$
*(equiprobable ⇒ mínima distancia pura).*

**(ii) Producto interno con sesgo** (expandir $\lVert y-c_j\rVert^2=\lVert y\rVert^2-2\langle y,c_j\rangle+\lVert c_j\rVert^2$, tirar $\lVert y\rVert^2$, escalar por $-\tfrac12$):
$\displaystyle \hat H=\arg\max_j\Big[\langle y,c_j\rangle-\frac{\lVert c_j\rVert^2}{2}+\frac{N_0}{2}\ln P_H(j)\Big].$

**(iii) Correlación con las formas de onda** (usando $\int r\,w_j^*=\sum_k y_k c_{j,k}^*=\langle y,c_j\rangle$):
$\displaystyle \hat H=\arg\max_j\Big[\int r(t)\,w_j^*(t)\,dt-\frac{\lVert w_j\rVert^2}{2}+\frac{N_0}{2}\ln P_H(j)\Big].$

La (iii) es notable: **no necesita ni la base ni el codebook** — trabaja directo con las $w_j(t)$.

---

### 2. Correlador vs filtro apareado (Fig. 3.6)

Las tres reglas piden calcular $\int r(t)\,b^*(t)\,dt$ (con $b=\psi_j$ o $b=w_j$). Dos
implementaciones:

**(a) Correlador:** multiplicar $r(t)\cdot b^*(t)$ e integrar.

**(b) Filtro apareado:** filtrar $r(t)$ con un LTI de respuesta al impulso

$$
h(t)=b^*(T-t)
$$

($T$ elegido para que $h$ sea causal) y **muestrear en $t=T$**. En efecto,

$$
y(t)=\int r(\alpha)\,h(t-\alpha)\,d\alpha=\int r(\alpha)\,b^*(T+\alpha-t)\,d\alpha
\;\Longrightarrow\;
y(T)=\int r(\alpha)\,b^*(\alpha)\,d\alpha .
$$

**Idénticos en $t=T$.** Elegir uno u otro es cuestión de tecnología: en software la correlación
es gratis; en analógico conviene el filtro si su $h(t)$ es fácil de construir.

---

### 3. Ejemplo: PAM binaria antipodal (Fig. 3.8)

Señales $w_0=a\,\psi(t)$ y $w_1=-a\,\psi(t)$ con $\psi(t)=\sqrt{1/T}\,\mathbb 1_{[0,T]}$
(rectangular normalizado). El filtro apareado es $h(t)=\psi(T-t)=\psi(t)$, y su salida **sin
ruido** para la entrada $\pm a\,\psi$ es un **triángulo** de pico $\pm a$ exactamente en $t=T$.

**Por qué $t=T$ es el instante óptimo:** la varianza del ruido a la salida del filtro **no
depende** del instante de muestreo (Lema del ruido blanco con $\lVert h\rVert=1$), mientras que la
señal es **máxima** en $t=T$. Muestrear en el pico maximiza la relación señal-ruido ⇒ minimiza
$P_e$. *(La demo de abajo reproduce la Fig. 3.8, con ruido ajustable.)*

---

### 4. Dos arquitecturas (Fig. 3.9)

- **$n$ filtros apareados a la base** $\{\psi_j\}$ → n-tupla $Y$ → decoder que minimiza
  $\lVert y-c_j\rVert^2-N_0\ln P_H(j)$.
- **$m$ filtros apareados a las señales** $\{w_j\}$ → sumar el sesgo
  $q_j=-\tfrac{\lVert w_j\rVert^2}{2}+\tfrac{N_0}{2}\ln P_H(j)$ → elegir el mayor
  (regla (iii); no requiere base ni codebook).

En sistemas reales $n$ y $m$ son enormes: ninguna de las dos se implementa por fuerza bruta; el
diseño inteligente (codificación) reduce la complejidad.

---

### 5. Para el pizarrón

1. Tres tests MAP equivalentes: distancia penalizada / $\langle y,c_j\rangle$ con sesgo /
   correlación con $w_j$.
2. $\int r\,b^*$ = **correlador** = **filtro apareado** $h(t)=b^*(T-t)$ muestreado en $t=T$
   (derivar $y(T)$).
3. PAM binaria: rectángulo → triángulo, pico en $T$; varianza del ruido constante ⇒ muestrear el
   pico es óptimo.
4. Arquitecturas: $n$ filtros (base) vs $m$ filtros (señales) + sesgos $q_j$.
