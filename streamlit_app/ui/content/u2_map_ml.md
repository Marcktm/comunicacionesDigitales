## Criterio MAP y ML — prueba de hipótesis binaria

> **Referencias.** Bixio Rimoldi, *Principles of Digital Communication*, §2.2 (prueba de
> hipótesis, **págs. 26–31**) y §2.4.1 (decisión binaria escalar en canal AWGN, **págs. 34–35**;
> la figura del umbral es la **Fig. 2.6, pág. 34**). Apunte Cabrera §1.3–1.11.
>
> El objetivo de esta página es **demostrar de punta a punta** cómo se obtiene el receptor
> óptimo y su probabilidad de error, sin saltar a la fórmula final — tal como hay que
> reproducirlo a mano.

---

### 1. Planteo: fuente, transmisor, canal y receptor

Modelamos el mensaje como una variable aleatoria $H$ que toma valores en el alfabeto finito
$\mathcal H=\{0,1,\dots,m-1\}$, con probabilidades a priori $P_H(i)$. En el **caso binario**
$\mathcal H=\{0,1\}$.

- El **transmisor** mapea cada mensaje $i$ a una señal $c_i$ (la *constelación*
  $\mathcal C=\{c_0,\dots,c_{m-1}\}$).
- El **canal** entrega un *observable* $Y$ con estadística conocida $f_{Y\mid H}(\cdot\mid i)$.
- El **receptor** produce una estimación $\hat H(y)$ a partir de la realización $Y=y$.

Definimos la **probabilidad de error** y la de acierto:

$$
P_e=\Pr\{\hat H\neq H\},\qquad P_c=\Pr\{\hat H=H\}=1-P_e .
$$

El receptor óptimo es el que **minimiza $P_e$** (equivalentemente, maximiza $P_c$).

---

### 2. Regla de Bayes → probabilidad a posteriori

Observado $Y=y$, la información completa sobre $H$ está en la **probabilidad a posteriori**
$P_{H\mid Y}(i\mid y)$. Por la regla de Bayes,

$$
P_{H\mid Y}(i\mid y)=\frac{P_H(i)\,f_{Y\mid H}(y\mid i)}{f_Y(y)},
\qquad f_Y(y)=\sum_{k} P_H(k)\,f_{Y\mid H}(y\mid k).
$$

Si el receptor decide $\hat H=i$, la probabilidad de que sea **correcto**, dado que observó
$y$, es exactamente $P_{H\mid Y}(i\mid y)$.

---

### 3. Regla MAP (Máximo A Posteriori)

Como para cada $y$ queremos maximizar la probabilidad de acertar, elegimos el $i$ que maximiza
la posteriori:

$$
\boxed{\;\hat H_{\mathrm{MAP}}(y)=\arg\max_{i\in\mathcal H} P_{H\mid Y}(i\mid y)\;}
\qquad\text{(regla MAP).}
$$

El denominador $f_Y(y)$ **no depende de $i$** (es una constante positiva para cada $y$), así que
no afecta el $\arg\max$. Podemos descartarlo:

$$
\hat H_{\mathrm{MAP}}(y)=\arg\max_{i\in\mathcal H}\; P_H(i)\,f_{Y\mid H}(y\mid i).
$$

Como la regla MAP maximiza $P_c$ **para cada** $y$, también maximiza la probabilidad
incondicional de acierto
$P_c=\mathbb E\big[P_{H\mid Y}(\hat H(Y)\mid Y)\big]=\int P_{H\mid Y}(\hat H(y)\mid y)\,f_Y(y)\,dy$.
Es, por lo tanto, **óptima**.

---

### 4. Caso especial: regla ML (Máxima Verosimilitud)

Cuando $H$ es **uniforme**, $P_H(i)=1/m$ para todo $i$, el factor $P_H(i)$ es constante y sale
del $\arg\max$. La regla MAP se reduce a la **regla ML**:

$$
\boxed{\;\hat H_{\mathrm{ML}}(y)=\arg\max_{i\in\mathcal H} f_{Y\mid H}(y\mid i)\;}
\qquad\text{(regla ML).}
$$

La función $f_{Y\mid H}(y\mid i)$, vista como función de $i$, se llama **verosimilitud**.

> **Importante.** ML se define incluso si **no** se conoce $P_H$, por eso es la opción cuando
> las priori son desconocidas. **MAP y ML coinciden si y solo si $P_H$ es uniforme.**

---

### 5. Prueba de hipótesis binaria y razón de verosimilitud

En el caso binario, la regla MAP compara las dos posterioris. Cancelando el denominador común
$f_Y(y)>0$:

$$
P_H(1)\,f_{Y\mid H}(y\mid 1)
\;\underset{\hat H=0}{\overset{\hat H=1}{\gtrless}}\;
P_H(0)\,f_{Y\mid H}(y\mid 0).
$$

Dividiendo ambos lados por la cantidad **no negativa** $P_H(1)\,f_{Y\mid H}(y\mid 0)$ se obtiene
la forma más útil:

$$
\Lambda(y)\;\triangleq\;\frac{f_{Y\mid H}(y\mid 1)}{f_{Y\mid H}(y\mid 0)}
\;\underset{\hat H=0}{\overset{\hat H=1}{\gtrless}}\;
\frac{P_H(0)}{P_H(1)}\;\triangleq\;\eta .
$$

- $\Lambda(y)$ es la **razón de verosimilitud**.
- $\eta$ es el **umbral**. Si $P_H(0)$ crece, $\eta$ crece y la región donde se decide $\hat H=0$
  se agranda (lo esperable). Con $P_H(0)=P_H(1)=\tfrac12$ resulta $\eta=1$ y el test MAP se vuelve
  un test **ML**.

---

### 6. Canal AWGN escalar: las densidades

Especializamos al canal **AWGN de tiempo discreto escalar**: se transmite $c_0$ o $c_1$ y se
recibe $Y=c_H+Z$ con $Z\sim\mathcal N(0,\sigma^2)$. Entonces

$$
H=0:\; Y\sim\mathcal N(c_0,\sigma^2),\qquad
H=1:\; Y\sim\mathcal N(c_1,\sigma^2),
$$

es decir

$$
f_{Y\mid H}(y\mid 0)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left\{-\frac{(y-c_0)^2}{2\sigma^2}\right\},
\quad
f_{Y\mid H}(y\mid 1)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left\{-\frac{(y-c_1)^2}{2\sigma^2}\right\}.
$$

---

### 7. Razón de verosimilitud, log-verosimilitud y umbral $\theta$

Calculamos $\Lambda(y)$; los factores $1/\sqrt{2\pi\sigma^2}$ se cancelan:

$$
\Lambda(y)=\exp\!\left\{\frac{-(y-c_1)^2+(y-c_0)^2}{2\sigma^2}\right\}
=\exp\!\left\{\frac{y(c_1-c_0)}{\sigma^2}+\frac{c_0^2-c_1^2}{2\sigma^2}\right\}.
$$

Como $\Lambda(y)$ es una exponencial, tomamos **logaritmo natural** a ambos lados del test
($\ln$ es monótona creciente, no cambia la desigualdad). La **log-verosimilitud** es:

$$
\ln\Lambda(y)=\frac{y(c_1-c_0)}{\sigma^2}+\frac{c_0^2-c_1^2}{2\sigma^2}
\;\underset{\hat H=0}{\overset{\hat H=1}{\gtrless}}\;\ln\eta .
$$

**Despejamos $y$.** Sin pérdida de generalidad suponemos $c_1>c_0$, de modo que
$(c_1-c_0)/\sigma^2>0$ y podemos **dividir por esa cantidad positiva sin invertir la
desigualdad**:

$$
\begin{aligned}
y+\frac{c_0^2-c_1^2}{2(c_1-c_0)}
&\;\underset{\hat H=0}{\overset{\hat H=1}{\gtrless}}\;
\frac{\sigma^2}{c_1-c_0}\,\ln\eta .
\end{aligned}
$$

El término constante se simplifica usando $c_0^2-c_1^2=-(c_1-c_0)(c_1+c_0)$:

$$
\frac{c_0^2-c_1^2}{2(c_1-c_0)}=-\frac{c_0+c_1}{2}.
$$

Pasándolo al otro lado, la prueba MAP queda como una **comparación con un umbral**:

$$
\boxed{\;\hat H_{\mathrm{MAP}}(y)=
\begin{cases}1,& y\ge\theta,\\[2pt] 0,& y<\theta,\end{cases}
\qquad
\theta=\frac{\sigma^2}{c_1-c_0}\,\ln\eta+\frac{c_0+c_1}{2}.\;}
$$

**Ventaja práctica:** el receptor ya no calcula exponenciales; sólo compara $y$ con un número
$\theta$ que se calcula una sola vez.

> **Caso equiprobable.** Si $P_H(0)=P_H(1)$ entonces $\eta=1$, $\ln\eta=0$ y el umbral es el
> **punto medio** $\theta=\dfrac{c_0+c_1}{2}$.

---

### 8. Probabilidad de error con la función $Q$

Con el detector $\hat H=1\iff y\ge\theta$, hay error si se transmitió $H=0$ pero $Y$ cayó por
encima del umbral (o viceversa). Condicionando en cada hipótesis:

$$
P_e(0)=\Pr\{Y>\theta\mid H=0\}=\int_\theta^\infty f_{Y\mid H}(y\mid 0)\,dy .
$$

Esta es la probabilidad de que una gaussiana de media $c_0$ y varianza $\sigma^2$ supere
$\theta$. Recordando la definición de la **función $Q$**,
$Q(x)=\Pr\{\mathcal N(0,1)\ge x\}$ y $\Pr\{\mathcal N(m,\sigma^2)\ge x\}=Q\!\big(\tfrac{x-m}{\sigma}\big)$,
obtenemos de inmediato

$$
P_e(0)=Q\!\left(\frac{\theta-c_0}{\sigma}\right),\qquad
P_e(1)=Q\!\left(\frac{c_1-\theta}{\sigma}\right).
$$

La probabilidad de error **total** (ley de probabilidad total):

$$
\boxed{\;P_e=P_H(0)\,Q\!\left(\frac{\theta-c_0}{\sigma}\right)
+P_H(1)\,Q\!\left(\frac{c_1-\theta}{\sigma}\right).\;}
$$

---

### 9. Caso equiprobable: $P_e=Q\!\big(\tfrac{d}{2\sigma}\big)$

Si $P_H(0)=P_H(1)=\tfrac12$, el umbral es el punto medio y

$$
\frac{\theta-c_0}{\sigma}=\frac{c_1-\theta}{\sigma}=\frac{c_1-c_0}{2\sigma}=\frac{d}{2\sigma},
\qquad d=|c_1-c_0|,
$$

de modo que $P_e(0)=P_e(1)$ y

$$
\boxed{\;P_e=Q\!\left(\frac{d}{2\sigma}\right).\;}
$$

La cantidad $\dfrac{d}{2\sigma}$ es la **relación señal-ruido** de la decisión binaria: cuanto
mayor sea la distancia $d$ entre señales y menor el ruido $\sigma$, menor es $P_e$. **Este
resultado conviene saberlo de memoria.**

---

### 10. Para el pizarrón — hilo de la demostración

1. Bayes ⇒ posteriori $P_{H\mid Y}$.
2. Maximizar la posteriori ⇒ **MAP**; descartar $f_Y(y)$; uniforme ⇒ **ML**.
3. Test binario ⇒ **razón de verosimilitud** $\Lambda(y)\gtrless\eta$.
4. AWGN ⇒ gaussianas ⇒ $\Lambda(y)$ exponencial ⇒ **log-verosimilitud**.
5. Dividir por $(c_1-c_0)/\sigma^2>0$ y simplificar $c_0^2-c_1^2$ ⇒ **umbral $\theta$**.
6. Integrar la cola gaussiana ⇒ $P_e$ con la **función $Q$**; equiprobable ⇒ $Q(d/2\sigma)$.

*Usá los controles de abajo para ver cómo cambian el umbral, las regiones de error y $P_e$
(teórico vs. Monte Carlo) al mover $c_0$, $c_1$, $\sigma$ y $P_H(0)$.*
