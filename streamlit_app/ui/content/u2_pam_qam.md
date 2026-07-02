## Hipótesis M-aria vectorial: m-PAM y m-QAM

> **Referencias.** Bixio Rimoldi §2.4.3; apunte 2026 (ejemplos 6-PAM y 4-QAM). En el canal AWGN
> la regla ML es de **mínima distancia**, y las regiones de decisión son **regiones de Voronoi**.

---

### 1. Decisión de mínima distancia (repaso del resultado que usamos)

Con $m$ hipótesis equiprobables, señales $c_i\in\mathbb R^n$ y $Y=c_i+Z$, $Z\sim\mathcal N(0,\sigma^2 I_n)$,
la regla ML maximiza la verosimilitud gaussiana; como el factor $\tfrac{1}{(2\pi\sigma^2)^{n/2}}$
es común y la exponencial es creciente,

$$
\hat H_{\mathrm{ML}}(y)=\arg\max_i f_{Y\mid H}(y\mid i)=\arg\min_i \lVert y-c_i\rVert .
$$

**Elegir el $c_i$ más cercano.** Las regiones $\mathcal R_i=\{y:\lVert y-c_i\rVert\le\lVert y-c_j\rVert\ \forall j\}$
son las **regiones de Voronoi**. No hace falta conocer $\sigma^2$ para decidir (sí afecta a $P_e$).

---

### 2. m-PAM (unidimensional, $n=1$)

Los $m$ puntos están **equiespaciados** sobre la recta con separación $d$ (distancia mínima):
$c_k=\big(k-\tfrac{m-1}{2}\big)\,d$. Las fronteras de decisión son los **puntos medios** entre
vecinos.

**Error por símbolo.** El ruido escalar es $Z\sim\mathcal N(0,\sigma^2)$.

- Los **2 puntos extremos** ($c_0,c_{m-1}$) tienen un solo vecino: se equivocan sólo hacia
  adentro, cuando el ruido cruza $d/2$:

$$
P_e(\text{extremo})=\Pr\{Z> d/2\}=Q\!\left(\frac{d}{2\sigma}\right).
$$

- Los **$m-2$ puntos internos** tienen dos vecinos: se equivocan a cualquiera de los dos lados.
  Como los eventos $\{Z\ge d/2\}$ y $\{Z<-d/2\}$ son disjuntos,

$$
P_e(\text{interno})=\Pr\{Z\ge d/2\}+\Pr\{Z<-d/2\}=2\,Q\!\left(\frac{d}{2\sigma}\right).
$$

**Promedio** sobre los $m$ símbolos equiprobables:

$$
P_e=\frac{2}{m}\,Q\!\left(\frac{d}{2\sigma}\right)+\frac{m-2}{m}\,2\,Q\!\left(\frac{d}{2\sigma}\right)
=\boxed{\;\left(2-\frac{2}{m}\right)Q\!\left(\frac{d}{2\sigma}\right).\;}
$$

**Ejemplo 6-PAM** ($m=6$): $2-\tfrac{2}{6}=\tfrac{5}{3}$, así que
$P_e=\tfrac{5}{3}\,Q\!\big(\tfrac{d}{2\sigma}\big)$.

---

### 3. 4-QAM (bidimensional, $n=2$)

Cuatro puntos en los vértices de un cuadrado, uno por cuadrante, con distancia mínima $d$ entre
vecinos. El ruido es $Z=(Z_1,Z_2)$ con $Z_1,Z_2\sim\mathcal N(0,\sigma^2)$ **independientes**. Las
regiones de decisión son los cuatro cuadrantes (fronteras = ejes).

**Vía la probabilidad de acierto.** Se transmite, digamos, $c_0$ (primer cuadrante). Se acierta
si **ambas** componentes del ruido no cruzan su umbral $d/2$. Por independencia, la probabilidad
conjunta es el producto:

$$
P_c(0)=\Pr\Big\{Z_1\ge -\tfrac{d}{2}\Big\}\,\Pr\Big\{Z_2\ge -\tfrac{d}{2}\Big\}
=\left[1-Q\!\left(\frac{d}{2\sigma}\right)\right]^2 .
$$

Por simetría $P_c(i)=P_c(0)$, luego

$$
\boxed{\;P_e=1-\left[1-Q\!\left(\frac{d}{2\sigma}\right)\right]^2
=2\,Q\!\left(\frac{d}{2\sigma}\right)-Q^2\!\left(\frac{d}{2\sigma}\right).\;}
$$

**Comprobación vía la unión (inclusión–exclusión).** El error al transmitir $c_0$ es que $Z_1$
saque por la izquierda **o** $Z_2$ por abajo. No son disjuntos, así que

$$
P_e(0)=\Pr\{A\cup B\}=\Pr\{A\}+\Pr\{B\}-\Pr\{A\cap B\}
=Q+Q-Q^2=2Q-Q^2,\qquad Q\triangleq Q\!\left(\tfrac{d}{2\sigma}\right),
$$

idéntico resultado. La diferencia es sólo la estrategia de cuenta: por $P_c$ (intersección de
eventos independientes) o por $P_e$ directa (unión de eventos no disjuntos).

---

### 4. Para el pizarrón

1. ML en AWGN = **mínima distancia** ⇒ regiones de **Voronoi**.
2. **m-PAM:** extremos $Q(d/2\sigma)$, internos $2Q(d/2\sigma)$ ⇒ promedio $(2-\tfrac2m)Q(d/2\sigma)$;
   6-PAM da $\tfrac53 Q$.
3. **4-QAM:** por independencia $P_c=[1-Q]^2$ ⇒ $P_e=2Q-Q^2$; se verifica por inclusión–exclusión.
4. Todo queda en función de la SNR $\tfrac{d}{2\sigma}$ vía la función $Q$.
