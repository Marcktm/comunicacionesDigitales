## Probabilidad de error

> **Referencias.** Bixio Rimoldi §2.2, §2.3, §2.6; apunte Cabrera §1.9–1.11. Reunimos aquí las
> herramientas para **calcular o acotar** $P_e$ en un canal AWGN.

---

### 1. Error condicional y error total

Con regiones de decisión $\mathcal R_i=\{y:\hat H(y)=i\}$, el error condicionado a $H=i$ es

$$
P_e(i)=1-P_c(i)=1-\int_{\mathcal R_i} f_{Y\mid H}(y\mid i)\,dy,
$$

y el error total promedia sobre las priori:

$$
\boxed{\;P_e=\sum_{i\in\mathcal H} P_H(i)\,P_e(i).\;}
$$

---

### 2. El caso que sí tiene forma cerrada: binario en AWGN

Cuando hay dos señales, la región es un semiespacio y la integral se reduce a una **función $Q$**.
Con priori uniforme,

$$
P_e=Q\!\left(\frac{d}{2\sigma}\right),\qquad d=\lVert c_1-c_0\rVert .
$$

La cantidad $\dfrac{d}{2\sigma}$ es la **relación señal-ruido** de la decisión: aumentar $d$ o
disminuir $\sigma$ baja $P_e$ (y $Q$ decae muy rápido).

---

### 3. Cuando no hay forma cerrada: cotas

Para $m>2$, $\mathcal R_i$ es un poliedro y la integral no es elemental. Se usan cotas.

**Cota de la unión.** El error dado $H=i$ está contenido en la unión de los eventos binarios
"más cerca de $c_j$ que de $c_i$":

$$
P_e(i)\le\sum_{j\neq i} Q\!\left(\frac{\lVert c_i-c_j\rVert}{2\sigma}\right).
$$

**Vecinos más cercanos.** Como $Q$ decae exponencialmente, domina la distancia mínima:

$$
P_e\approx N_{\min}\,Q\!\left(\frac{d_{\min}}{2\sigma}\right),
$$

con $d_{\min}$ la distancia mínima y $N_{\min}$ el número medio de vecinos a esa distancia. Es la
herramienta práctica para estimar $P_e$ de cualquier constelación.

---

### 4. Curvas de BER y energía por bit

En la práctica se grafican **curvas de probabilidad de error vs relación señal-ruido** (escala
log en $P_e$). Un eje habitual es $\varepsilon_b/N_0$ (energía por bit sobre densidad espectral de
ruido), porque permite **comparar de forma justa** esquemas con distinta cantidad de bits por
símbolo. Para señalización antipodal,

$$
P_e=Q\!\left(\sqrt{\frac{2\varepsilon_b}{N_0}}\right).
$$

Abajo se comparan las curvas de m-PAM y 4-QAM en función de la SNR $\tfrac{d}{2\sigma}$: a mayor
orden $m$, se necesita más SNR para la misma $P_e$.

---

### 5. Para el pizarrón

1. $P_e=\sum_i P_H(i)\big[1-\int_{\mathcal R_i} f\big]$.
2. Binario AWGN ⇒ $P_e=Q(d/2\sigma)$.
3. m-ario ⇒ **cota de unión** $P_e(i)\le\sum_{j\ne i}Q(\lVert c_i-c_j\rVert/2\sigma)$.
4. **Vecinos más cercanos:** $P_e\approx N_{\min}Q(d_{\min}/2\sigma)$.
5. Se compara con curvas vs $\varepsilon_b/N_0$; antipodal: $Q(\sqrt{2\varepsilon_b/N_0})$.
