## Diseño de receptor para el canal AWGN de tiempo discreto

> **Referencias.** Bixio Rimoldi §2.4 (*Receiver design for the discrete-time AWGN channel*,
> **págs. 32–34**; el modelo es la **Fig. 2.5, pág. 31**); apunte Cabrera §1.9. Especializamos la
> prueba de hipótesis al canal más importante: el **AWGN de tiempo discreto**.

---

### 1. El modelo del canal

La hipótesis $H\in\{0,\dots,m-1\}$ se mapea a una **señal** $c_i\in\mathbb R^n$ (una n-tupla). El
canal **suma ruido gaussiano** de media cero, componentes iid de varianza $\sigma^2$:

$$
H=i:\qquad Y=c_i+Z,\qquad Z\sim\mathcal N(0,\sigma^2 I_n).
$$

*(Ver el diagrama de bloques abajo: transmisor → suma de ruido → receptor.)* La densidad del
observable es la gaussiana multivariada

$$
f_{Y\mid H}(y\mid i)=\frac{1}{(2\pi\sigma^2)^{n/2}}
\exp\!\left\{-\frac{\lVert y-c_i\rVert^2}{2\sigma^2}\right\}.
$$

---

### 2. De MAP a "mínima distancia"

El receptor MAP elige el $i$ que maximiza $P_H(i)\,f_{Y\mid H}(y\mid i)$. Como $f$ es una
exponencial, tomamos $\ln$ (monótona) y descartamos la constante $\tfrac{1}{(2\pi\sigma^2)^{n/2}}$
(no depende de $i$):

$$
\hat H(y)=\arg\max_i\left[\ln P_H(i)-\frac{\lVert y-c_i\rVert^2}{2\sigma^2}\right]
=\arg\min_i\left[\lVert y-c_i\rVert^2-2\sigma^2\ln P_H(i)\right].
$$

**Caso equiprobable** ($P_H(i)=1/m$): el término $2\sigma^2\ln P_H(i)$ es constante y se cae,
quedando la **regla de mínima distancia**:

$$
\boxed{\;\hat H_{\mathrm{ML}}(y)=\arg\min_i \lVert y-c_i\rVert\;}
$$

**elegir el $c_i$ más cercano a $y$.** Notablemente, **no hace falta conocer $\sigma^2$** para
decidir (sí afecta a la probabilidad de error).

---

### 3. Regiones de decisión = regiones de Voronoi

La regla de mínima distancia parte el espacio $\mathbb R^n$ en $m$ **regiones de Voronoi**:

$$
\mathcal R_i=\{y:\lVert y-c_i\rVert\le\lVert y-c_j\rVert\ \ \forall j\neq i\}.
$$

Las fronteras entre regiones vecinas son los **bisectores perpendiculares** (hiperplanos a
igual distancia de dos señales). En la gráfica de abajo se ven las regiones para una
constelación de ejemplo.

---

### 4. Dos caminos que siguen

- Si $n=1$ (**observación escalar**): la decisión se reduce a comparar $y$ con un **umbral**
  (ver *Criterio MAP y ML*).
- Si $n>1$ (**observaciones vectoriales**): la decisión binaria se reduce a **proyectar** sobre
  la dirección que une las dos señales y comparar con un umbral; el resto de las coordenadas es
  ruido irrelevante (ver *Observaciones vectoriales*).

---

### 5. Para el pizarrón

1. AWGN discreto: $Y=c_i+Z$, $Z\sim\mathcal N(0,\sigma^2 I_n)$ ⇒ gaussiana multivariada.
2. MAP ⇒ minimizar $\lVert y-c_i\rVert^2-2\sigma^2\ln P_H(i)$.
3. Equiprobable ⇒ **mínima distancia**; no depende de $\sigma^2$.
4. Regiones de decisión = **Voronoi** (bisectores perpendiculares).
