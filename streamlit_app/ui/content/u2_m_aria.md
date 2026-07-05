## Prueba de hipótesis M-aria

> **Referencias.** Bixio Rimoldi §2.2.2 (**pág. 30**), §2.4.3 (**págs. 39–41**; las regiones de
> Voronoi son la **Fig. 2.8, pág. 38**) y §2.6.1 (*Union bound*, **págs. 44–48**); apunte 2026
> (decisión m-aria de n-tuplas). Generalizamos de 2 a $m$ hipótesis.

---

### 1. Regla MAP y ML para $m$ hipótesis

Con $\mathcal H=\{0,1,\dots,m-1\}$, la regla óptima sigue siendo elegir la de mayor posteriori:

$$
\hat H_{\mathrm{MAP}}(y)=\arg\max_{i\in\mathcal H}P_{H\mid Y}(i\mid y)
=\arg\max_{i\in\mathcal H} f_{Y\mid H}(y\mid i)\,P_H(i).
$$

Cuando las hipótesis son **equiprobables** ($P_H(i)=1/m$), el factor $P_H(i)$ es constante y

$$
\boxed{\;\hat H_{\mathrm{ML}}(y)=\arg\max_{i\in\mathcal H} f_{Y\mid H}(y\mid i).\;}
$$

---

### 2. En AWGN: mínima distancia y regiones de Voronoi

Para el canal AWGN, $f_{Y\mid H}(y\mid i)\propto\exp\{-\lVert y-c_i\rVert^2/2\sigma^2\}$, y
maximizar la verosimilitud equivale a **minimizar la distancia**:

$$
\hat H_{\mathrm{ML}}(y)=\arg\min_{i}\lVert y-c_i\rVert .
$$

El espacio queda partido en **regiones de decisión (Voronoi)**
$\mathcal R_i=\{y:\lVert y-c_i\rVert\le\lVert y-c_j\rVert\ \forall j\}$, delimitadas por los
bisectores perpendiculares entre pares de señales (ver la gráfica de abajo). Si $y$ cae en
$\mathcal R_i$, se decide $\hat H=i$.

---

### 3. Probabilidad de error

Condicionando en $H=i$ y usando las regiones:

$$
P_e(i)=1-P_c(i)=1-\int_{\mathcal R_i}f_{Y\mid H}(y\mid i)\,dy,
\qquad
P_e=\sum_{i\in\mathcal H}P_H(i)\,P_e(i).
$$

En general la integral sobre $\mathcal R_i$ (un poliedro) no tiene forma cerrada. Por eso se usan
**cotas**.

---

### 4. Cota de la unión (union bound)

El error dado $H=i$ es que $Y$ caiga en la región de algún otro $c_j$. Ese evento está contenido
en la unión de los eventos "más cerca de $c_j$ que de $c_i$", cada uno con probabilidad
$Q\!\big(\tfrac{\lVert c_i-c_j\rVert}{2\sigma}\big)$ (¡un problema binario!). Por la cota de la unión,

$$
\boxed{\;P_e(i)\le\sum_{j\neq i}Q\!\left(\frac{\lVert c_i-c_j\rVert}{2\sigma}\right).\;}
$$

**Aproximación de vecinos más cercanos.** Como $Q$ decae muy rápido, domina la distancia mínima
$d_{\min}=\min_{i\neq j}\lVert c_i-c_j\rVert$. Si cada señal tiene en promedio $N_{\min}$ vecinos a
esa distancia,

$$
P_e\approx N_{\min}\,Q\!\left(\frac{d_{\min}}{2\sigma}\right).
$$

Es la herramienta práctica: **contar vecinos a distancia mínima** y evaluar una $Q$. (Los
ejemplos cerrados m-PAM y 4-QAM se derivan exactos en la página *m-PAM y m-QAM*.)

---

### 5. Para el pizarrón

1. MAP m-ario = $\arg\max_i f(y\mid i)P_H(i)$; equiprobable ⇒ **ML**.
2. AWGN ⇒ **mínima distancia** ⇒ regiones de **Voronoi**.
3. $P_e=\sum_i P_H(i)\big[1-\int_{\mathcal R_i}f\big]$.
4. **Union bound:** $P_e(i)\le\sum_{j\neq i}Q(\lVert c_i-c_j\rVert/2\sigma)$.
5. **Vecinos más cercanos:** $P_e\approx N_{\min}\,Q(d_{\min}/2\sigma)$.
