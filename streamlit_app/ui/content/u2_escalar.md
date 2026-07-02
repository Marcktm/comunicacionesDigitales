## Decisión binaria para observaciones escalares

> **Referencias.** Bixio Rimoldi §2.4.1; apunte Cabrera §1.9.1–1.9.2. El receptor óptimo para una
> observación escalar es simplemente un **comparador con un umbral**. Acá miramos su
> interpretación como detector (falsos positivos / negativos).

---

### 1. El receptor es un comparador de umbral

Con $H\in\{0,1\}$, señales escalares $c_0,c_1$ y $Y=c_H+Z$, $Z\sim\mathcal N(0,\sigma^2)$, la regla
MAP (ver *Criterio MAP y ML* para la derivación) se reduce a comparar $Y$ con un umbral (suponiendo
$c_1>c_0$):

$$
\hat H(y)=\begin{cases}1,& y\ge\theta,\\ 0,& y<\theta,\end{cases}
\qquad
\theta=\frac{\sigma^2}{c_1-c_0}\ln\eta+\frac{c_0+c_1}{2},\quad \eta=\frac{P_H(0)}{P_H(1)}.
$$

El hardware del receptor es un **detector de umbral**: mide $Y$ y decide según de qué lado de
$\theta$ cayó.

---

### 2. Dos tipos de error

Al ser una prueba de detección, los dos errores condicionales tienen nombre:

- **Falso positivo** (falsa alarma): se transmitió $H=0$ pero $Y\ge\theta$, así que se decide 1.

$$
P_e(0)=\Pr\{Y\ge\theta\mid H=0\}=Q\!\left(\frac{\theta-c_0}{\sigma}\right).
$$

- **Falso negativo** (pérdida): se transmitió $H=1$ pero $Y<\theta$, se decide 0.

$$
P_e(1)=\Pr\{Y<\theta\mid H=1\}=Q\!\left(\frac{c_1-\theta}{\sigma}\right).
$$

El error total: $P_e=P_H(0)\,P_e(0)+P_H(1)\,P_e(1)$.

---

### 3. Mover el umbral: el compromiso FP ↔ FN

El umbral $\theta$ **se corre** cuando cambia la priori (o, más en general, cuando asignamos
distinto costo a cada error). Desde la fórmula: si $P_H(0)$ crece, $\eta$ crece, $\ln\eta>0$ y
$\theta$ se desplaza hacia $c_1$ ⇒ la región donde se decide $0$ se agranda.

**Ejemplo (detección).** Un test de una enfermedad: $H=0$ "sano", $H=1$ "enfermo". Si el sistema
de salud está saturado, conviene **subir el umbral** para descartar más positivos: bajan los
falsos positivos a costa de más falsos negativos. Es el mismo trade-off que en un detector de
humo o un radar: mover $\theta$ intercambia falsas alarmas por pérdidas.

---

### 4. Caso equiprobable

Si $P_H(0)=P_H(1)$, entonces $\theta$ es el **punto medio** $\tfrac{c_0+c_1}{2}$, los dos errores
se igualan y

$$
P_e=Q\!\left(\frac{d}{2\sigma}\right),\qquad d=|c_1-c_0|.
$$

*(En la gráfica de abajo, mové $P(H=0)$ para ver cómo se corre $\theta$ y cómo se intercambian las
áreas de falso positivo y falso negativo.)*

---

### 5. Para el pizarrón

1. Receptor escalar = **comparador** con umbral $\theta$.
2. $P_e(0)=Q((\theta-c_0)/\sigma)$ (falso positivo), $P_e(1)=Q((c_1-\theta)/\sigma)$ (falso negativo).
3. Subir $P_H(0)$ ⇒ $\theta$ hacia $c_1$ ⇒ menos FP, más FN.
4. Equiprobable ⇒ $\theta$ punto medio, $P_e=Q(d/2\sigma)$.
