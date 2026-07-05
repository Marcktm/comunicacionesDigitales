## Decisión binaria con observaciones vectoriales

> **Referencias.** Bixio Rimoldi §2.4.2 (*Binary decision for n-tuple observations*,
> **págs. 35–39**; la geometría del plano afín con p y q es la **Fig. 2.7, pág. 36**); apunte
> 2026 (decisión binaria de n-tuplas). Extendemos
> la decisión binaria a $n$ dimensiones y descubrimos que **sólo importa la dirección que une
> las dos señales**.

---

### 1. Planteo

Se transmite $c_0$ o $c_1$ en $\mathbb R^n$ y se recibe $Y=c_H+Z$, con $Z\sim\mathcal N(0,\sigma^2 I_n)$.
Las densidades son

$$
f_{Y\mid H}(y\mid i)=\frac{1}{(2\pi\sigma^2)^{n/2}}\exp\!\left\{-\frac{\lVert y-c_i\rVert^2}{2\sigma^2}\right\},
\qquad i\in\{0,1\}.
$$

---

### 2. Razón de verosimilitud → log-verosimilitud

$$
\Lambda(y)=\frac{f_{Y\mid H}(y\mid 1)}{f_{Y\mid H}(y\mid 0)}
=\exp\!\left\{\frac{\lVert y-c_0\rVert^2-\lVert y-c_1\rVert^2}{2\sigma^2}\right\}.
$$

Tomando $\ln$ y desarrollando cada norma con
$\lVert y-c_i\rVert^2=\lVert y\rVert^2-2\langle y,c_i\rangle+\lVert c_i\rVert^2$, el término
$\lVert y\rVert^2$ se cancela al restar:

$$
\lVert y-c_0\rVert^2-\lVert y-c_1\rVert^2
=2\langle y,\,c_1-c_0\rangle+\lVert c_0\rVert^2-\lVert c_1\rVert^2 .
$$

Por lo tanto

$$
\ln\Lambda(y)=\left\langle y,\frac{c_1-c_0}{\sigma^2}\right\rangle+\frac{\lVert c_0\rVert^2-\lVert c_1\rVert^2}{2\sigma^2}.
$$

---

### 3. La regla se vuelve una proyección contra un umbral

El test MAP es $\ln\Lambda(y)\gtrless\ln\eta$, con $\eta=P_H(0)/P_H(1)$. Definimos la **dirección
unitaria** que une las señales y la distancia entre ellas:

$$
\psi=\frac{c_1-c_0}{d},\qquad d=\lVert c_1-c_0\rVert .
$$

Dividiendo por $d/\sigma^2>0$ y despejando, la regla queda

$$
\boxed{\;\hat H(y)=\begin{cases}1,&\langle y,\psi\rangle\ge\theta,\\ 0,&\langle y,\psi\rangle<\theta,\end{cases}
\qquad
\theta=\frac{\sigma^2}{d}\ln\eta+\frac{\lVert c_1\rVert^2-\lVert c_0\rVert^2}{2d}.\;}
$$

$\langle y,\psi\rangle$ es la **proyección** de $y$ sobre la recta que va de $c_0$ a $c_1$. Las
regiones de decisión son dos semiespacios separados por un **plano afín**
$\{y:\langle y,\psi\rangle=\theta\}$ (la frontera de Voronoi entre $c_0$ y $c_1$).

---

### 4. Geometría: las distancias $p$ y $q$

Sean $p$ y $q$ las distancias con signo de $c_0$ y $c_1$ al plano de decisión. De

$$
\lVert y-c_0\rVert^2-\lVert y-c_1\rVert^2=p^2-q^2=2\sigma^2\ln\eta,\qquad p+q=d,
$$

resolvemos:

$$
p=\frac{d}{2}+\frac{\sigma^2\ln\eta}{d},\qquad q=\frac{d}{2}-\frac{\sigma^2\ln\eta}{d}.
$$

Con $\eta=1$ (priori uniforme) el plano queda en el **medio**: $p=q=d/2$.

---

### 5. Probabilidad de error

El error cuando se transmite $H=0$ es que el ruido cruce el plano, a distancia $p$; como la
proyección del ruido sobre $\psi$ es $\mathcal N(0,\sigma^2)$,

$$
P_e(0)=Q\!\left(\frac{p}{\sigma}\right)=Q\!\left(\frac{d}{2\sigma}+\frac{\sigma\ln\eta}{d}\right),
\qquad
P_e(1)=Q\!\left(\frac{q}{\sigma}\right)=Q\!\left(\frac{d}{2\sigma}-\frac{\sigma\ln\eta}{d}\right),
$$

$$
P_e=P_H(0)\,P_e(0)+P_H(1)\,P_e(1).
$$

**Caso equiprobable:** $P_e=Q\!\big(\tfrac{d}{2\sigma}\big)$, con la **SNR** $\tfrac{d}{2\sigma}$.

---

### 6. Reducción al caso escalar

Cambiando de coordenadas para que la primera apunte en la dirección $\psi$, las señales van a
$\tilde c_0=(-d/2,0,\dots,0)^{\mathsf T}$ y $\tilde c_1=(d/2,0,\dots,0)^{\mathsf T}$, y sólo la
**primera coordenada** $\langle y,\psi\rangle$ interviene en la decisión. Las demás coordenadas
son ruido que no aporta información. **La conclusión potente:** en una decisión binaria, sólo
importa la **distancia** $d$ entre las dos señales (y $\sigma$), nada más.

---

### 7. Para el pizarrón

1. $\ln\Lambda(y)=\langle y,(c_1-c_0)/\sigma^2\rangle+(\lVert c_0\rVert^2-\lVert c_1\rVert^2)/2\sigma^2$.
2. $\psi=(c_1-c_0)/d$ ⇒ regla = **proyectar** y comparar con $\theta$ (plano afín).
3. $p,q$ con $p+q=d$, $p^2-q^2=2\sigma^2\ln\eta$.
4. $P_e(0)=Q(p/\sigma)$, $P_e(1)=Q(q/\sigma)$; equiprobable ⇒ $Q(d/2\sigma)$.
5. Reducción a escalar: **sólo cuenta $d$**.
