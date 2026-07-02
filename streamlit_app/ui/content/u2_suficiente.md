## Estadística suficiente

> **Referencias.** Bixio Rimoldi §2.5; apunte 2026 (reducción de dimensionalidad). Una
> **estadística suficiente** resume toda la información del observable sobre la hipótesis, y
> permite tirar el resto **sin perder** capacidad de decisión.

---

### 1. Idea y definición

Una función $T(Y)$ del observable es **suficiente** para $H$ si, conociendo $T(Y)$, el resto de
$Y$ ya no aporta nada sobre $H$:

$$
P_{H\mid Y}(i\mid y)=P_{H\mid T(Y)}\big(i\mid T(y)\big).
$$

Es decir, $H\to T(Y)\to Y$ forma una cadena de Markov: **toda** la información sobre $H$ pasa por
$T(Y)$.

---

### 2. Teorema de factorización de Fisher–Neyman

$T(Y)$ es suficiente para $H$ **si y solo si** la verosimilitud se factoriza como

$$
\boxed{\;f_{Y\mid H}(y\mid i)=g_i\big(T(y)\big)\,h(y),\;}
$$

donde $g_i$ depende de la hipótesis **sólo a través de** $T(y)$, y $h(y)$ **no** depende de $i$.

**Consecuencia clave.** El receptor MAP maximiza $P_H(i)\,f_{Y\mid H}(y\mid i)=P_H(i)\,g_i(T(y))\,h(y)$;
como $h(y)>0$ no depende de $i$, se descarta del $\arg\max$. Por lo tanto **la decisión óptima
depende de $y$ sólo a través de $T(y)$**: podemos quedarnos con $T(Y)$ y tirar el resto sin
perder optimalidad. Esto es **reducción de dimensionalidad**.

---

### 3. Ejemplo: $n$ observaciones ruidosas del mismo símbolo

Se transmite $c\in\{-a,+a\}$ y se reciben $n$ copias independientes
$Y_k=c+Z_k$, $Z_k\sim\mathcal N(0,\sigma^2)$ iid. La verosimilitud del vector $y=(y_1,\dots,y_n)$ es

$$
f_{Y\mid H}(y\mid i)=\prod_{k=1}^{n}\frac{1}{\sqrt{2\pi\sigma^2}}
\exp\!\left\{-\frac{(y_k-c_i)^2}{2\sigma^2}\right\}.
$$

Desarrollando el exponente, $\sum_k (y_k-c_i)^2=\sum_k y_k^2-2c_i\sum_k y_k+n c_i^2$. El único
término que **mezcla** $y$ con la hipótesis $c_i$ es $-2c_i\sum_k y_k$, así que

$$
f_{Y\mid H}(y\mid i)=\underbrace{\exp\!\left\{\frac{c_i}{\sigma^2}\sum_k y_k-\frac{n c_i^2}{2\sigma^2}\right\}}_{g_i\left(T(y)\right)}
\cdot\underbrace{\frac{1}{(2\pi\sigma^2)^{n/2}}\exp\!\left\{-\frac{1}{2\sigma^2}\sum_k y_k^2\right\}}_{h(y)} .
$$

Por Fisher–Neyman, $T(y)=\sum_k y_k$ (equivalentemente el **promedio** $\bar Y=\tfrac1n\sum_k y_k$)
es una **estadística suficiente**. Pasamos de $n$ números a **uno solo** sin perder nada.

**Ganancia por promediar.** $\bar Y\sim\mathcal N\!\big(c,\,\sigma^2/n\big)$: el ruido efectivo se
reduce por $\sqrt n$. Decidiendo por el signo de $\bar Y$,

$$
P_e=Q\!\left(\frac{a}{\sigma/\sqrt n}\right)=Q\!\left(\frac{\sqrt n\,a}{\sigma}\right),
$$

que decae al aumentar $n$. *(La gráfica de abajo muestra $P_e$ vs $n$.)*

---

### 4. Por qué importa

- **Complejidad:** el detector trabaja con $T(Y)$ (1 número) en vez del vector completo.
- **Puente al canal continuo (Cap. 3):** la proyección de la señal recibida sobre el espacio de
  señales, $Y=(\langle R,\psi_1\rangle,\dots)$, es una **estadística suficiente**; el ruido fuera
  de ese subespacio es irrelevante. Es la base del **filtro apareado**.

---

### 5. Para el pizarrón

1. $T(Y)$ suficiente ⇔ **Fisher–Neyman** $f(y\mid i)=g_i(T(y))\,h(y)$.
2. $h(y)$ no depende de $i$ ⇒ MAP depende de $y$ **sólo por** $T(y)$: se tira el resto.
3. Ejemplo $n$ iid: $T(y)=\sum_k y_k$; $\bar Y\sim\mathcal N(c,\sigma^2/n)$ ⇒ $P_e=Q(\sqrt n\,a/\sigma)$.
4. En el canal continuo, la proyección sobre el espacio de señales es suficiente (matched filter).
