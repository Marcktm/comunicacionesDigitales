## Vectores aleatorios gaussianos

> **Referencias.** Roy Yates (vectores gaussianos) y Bixio §2.10 (apéndice). Es la distribución
> del **ruido** en el canal AWGN y la que hace tan tratable el diseño del receptor.

---

### 1. Definición

Un vector $X=(X_1,\dots,X_n)^{\mathsf T}$ es **conjuntamente gaussiano** si **toda combinación
lineal** $a^{\mathsf T}X=\sum_i a_i X_i$ es una variable gaussiana (escalar). Queda caracterizado
por su vector de medias $m_X$ y su matriz de covarianza $K_X$: se escribe $X\sim\mathcal N(m_X,K_X)$.

Si $K_X$ es invertible, la **densidad** es

$$
f_X(x)=\frac{1}{(2\pi)^{n/2}\,|K_X|^{1/2}}
\exp\!\left\{-\tfrac12 (x-m_X)^{\mathsf T} K_X^{-1}(x-m_X)\right\}.
$$

Las curvas de nivel de $f_X$ son **elipses** (elipsoides) centradas en $m_X$, con ejes dados por
los autovectores de $K_X$ (ver la gráfica de abajo).

---

### 2. Caso esférico $\mathcal N(0,\sigma^2 I)$: el ruido blanco

Cuando $K_X=\sigma^2 I$ (componentes iid, media cero), la densidad se **factoriza**:

$$
f_X(x)=\prod_{k=1}^{n}\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left\{-\frac{x_k^2}{2\sigma^2}\right\}
=\frac{1}{(2\pi\sigma^2)^{n/2}}\exp\!\left\{-\frac{\lVert x\rVert^2}{2\sigma^2}\right\}.
$$

Depende de $x$ **sólo por su norma** $\lVert x\rVert$: es **esféricamente simétrica** (curvas de
nivel = círculos). Éste es exactamente el ruido $Z\sim\mathcal N(0,\sigma^2 I_n)$ del canal AWGN, y
la razón por la que la regla ML resulta de **mínima distancia**.

---

### 3. Tres propiedades que usamos todo el tiempo

1. **Cerradura bajo transformaciones lineales.** Si $X\sim\mathcal N(m_X,K_X)$ y $Y=AX+b$, entonces
   $Y\sim\mathcal N(Am_X+b,\;AK_XA^{\mathsf T})$ — **sigue siendo gaussiano**. (Se deduce de la
   definición: toda combinación lineal de $Y$ es combinación lineal de $X$, gaussiana.)

2. **Incorrelación ⇒ independencia** (¡sólo para gaussianos!). Si las componentes conjuntamente
   gaussianas están incorrelacionadas ($K_X$ diagonal), entonces son **independientes**. En
   general la incorrelación no implica independencia, pero en el caso gaussiano sí.

3. **Blanqueo (whitening).** Como $K_X$ es simétrica semidefinida positiva, se diagonaliza
   $K_X=U\Lambda U^{\mathsf T}$. Tomando $W=\Lambda^{-1/2}U^{\mathsf T}$, el vector
   $Z=W(X-m_X)$ cumple $\mathbb E[Z]=0$ y $K_Z=I$: ruido **blanco** de componentes iid. Es el paso
   que convierte ruido coloreado en el caso estándar.

---

### 4. Por qué es tan importante

- El **teorema del límite central** justifica modelar el ruido térmico como gaussiano.
- La simetría esférica de $\mathcal N(0,\sigma^2 I)$ ⇒ **mínima distancia** ⇒ regiones de Voronoi
  (Unidad 2).
- La cerradura lineal ⇒ la **proyección** de la señal recibida sobre el espacio de señales es
  gaussiana y **suficiente** ⇒ base del **filtro apareado** (Unidad 3).

---

### 5. Para el pizarrón

1. Conjuntamente gaussiano ⇔ toda combinación lineal es gaussiana; pdf con $K^{-1}$ y $|K|$.
2. $\mathcal N(0,\sigma^2I)$: $f(x)\propto e^{-\lVert x\rVert^2/2\sigma^2}$, **esférico** ⇒ mínima distancia.
3. Lineal de gaussiano = gaussiano ($AK A^{\mathsf T}$).
4. Gaussianos: **incorrelación ⇒ independencia**.
5. **Blanqueo:** $K=U\Lambda U^{\mathsf T}$, $W=\Lambda^{-1/2}U^{\mathsf T}$ ⇒ $K_Z=I$.
