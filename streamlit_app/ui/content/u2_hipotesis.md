## Prueba de hipótesis — MAP y ML (caso general)

> **Referencias.** Bixio Rimoldi §2.2 (*Hypothesis testing*, **págs. 26–31**); apunte Cabrera
> §1.3–1.5. Esta página establece el marco
> general (m hipótesis, observable cualquiera). El caso AWGN binario escalar se desarrolla con
> todo detalle en *Criterio MAP y ML*.

---

### 1. El problema y su vocabulario

**Probar una hipótesis** es adivinar el valor de una variable aleatoria discreta $H$ (el
*mensaje*) que toma valores en un alfabeto finito $\mathcal H=\{0,1,\dots,m-1\}$, a partir de
otra variable aleatoria $Y$ (el *observable*, posiblemente un vector).

En comunicaciones, $H$ es el mensaje transmitido e $Y$ es la salida del canal; adivinar $H$ a
partir de $Y$ se llama **decodificar**. En un detector de humo, adivinar se llama **detección**.
Decodificación, detección y toma de decisiones son lo mismo: **prueba de hipótesis**.

Suponemos conocidos, para todo $i$: la **probabilidad a priori** $P_H(i)$ y la **verosimilitud**
$f_{Y\mid H}(\cdot\mid i)$ (densidad de $Y$ dado $H=i$; si $Y$ es discreto, una pmf $P_{Y\mid H}$).

El receptor produce $\hat H(y)$; buscamos **minimizar** la probabilidad de error
$P_e=\Pr\{\hat H\neq H\}$ (equivalente a **maximizar** $P_c=1-P_e$).

---

### 2. Regla de Bayes: de la priori a la posteriori

Al observar $Y=y$, la información se resume en la **probabilidad a posteriori**:

$$
P_{H\mid Y}(i\mid y)=\frac{P_H(i)\,f_{Y\mid H}(y\mid i)}{f_Y(y)},
\qquad f_Y(y)=\sum_{k\in\mathcal H} P_H(k)\,f_{Y\mid H}(y\mid k).
$$

Si el receptor decide $\hat H=i$, la probabilidad de acertar (dado $y$) es $P_{H\mid Y}(i\mid y)$.

---

### 3. Regla MAP y por qué es óptima

Para maximizar la probabilidad de acierto en **cada** $y$, elegimos el $i$ de mayor posteriori:

$$
\boxed{\;\hat H_{\mathrm{MAP}}(y)=\arg\max_{i\in\mathcal H} P_{H\mid Y}(i\mid y).\;}
$$

El denominador $f_Y(y)$ es una constante positiva en $y$ y **no** afecta al $\arg\max$, así que

$$
\hat H_{\mathrm{MAP}}(y)=\arg\max_{i\in\mathcal H}\; P_H(i)\,f_{Y\mid H}(y\mid i).
$$

Como maximiza $P_c$ punto a punto, también maximiza la probabilidad **incondicional**

$$
P_c=\mathbb E\big[P_{H\mid Y}(\hat H(Y)\mid Y)\big]=\int P_{H\mid Y}(\hat H(y)\mid y)\,f_Y(y)\,dy,
$$

por lo tanto **ninguna** regla logra menor $P_e$: la regla MAP es óptima.

> En caso de empate (dos $i$ con la misma posteriori máxima) da igual cuál elegir: $P_c$ es la
> misma.

---

### 4. Regla ML (priori uniforme)

Si $H$ es **uniforme**, $P_H(i)=1/m$ es constante y sale del $\arg\max$:

$$
\boxed{\;\hat H_{\mathrm{ML}}(y)=\arg\max_{i\in\mathcal H} f_{Y\mid H}(y\mid i).\;}
$$

**ML se define aun sin conocer $P_H$**, por eso es la opción cuando las priori son desconocidas.
MAP y ML **coinciden si y solo si $P_H$ es uniforme**.

---

### 5. Regiones de decisión y probabilidad de error

Una función de decisión $\hat H:\mathcal Y\to\mathcal H$ queda descrita por sus **regiones de
decisión**

$$
\mathcal R_i=\{y:\hat H(y)=i\}.
$$

El espacio de observaciones queda partido en $m$ zonas, una por hipótesis. Condicionando en
$H=i$, la probabilidad de acierto es la integral de la verosimilitud sobre su región, y el error
es el complemento:

$$
P_e(i)=1-P_c(i)=1-\int_{\mathcal R_i} f_{Y\mid H}(y\mid i)\,dy,
\qquad
P_e=\sum_{i} P_H(i)\,P_e(i).
$$

---

### 6. Ejemplo: un bit por fibra óptica (canal de Poisson)

Transmitimos $H\in\{0,1\}$ con $P_H(0)=\tfrac12$. Si $H=1$ encendemos un LED y un fotodetector
cuenta $Y\in\mathbb N$ fotones. Incluso con el LED apagado hay cuentas (luz ambiente), así que
modelamos $Y$ como **Poisson** con intensidad que depende de $H$:

$$
P_{Y\mid H}(y\mid 0)=\frac{\lambda_0^{\,y}}{y!}e^{-\lambda_0},\qquad
P_{Y\mid H}(y\mid 1)=\frac{\lambda_1^{\,y}}{y!}e^{-\lambda_1},\qquad 0\le\lambda_0<\lambda_1 .
$$

**Regla ML** (priori uniforme): decidir $\hat H=1$ cuando $P_{Y\mid H}(y\mid 1)\ge P_{Y\mid H}(y\mid 0)$.
Tomando el cociente y luego logaritmo,

$$
\frac{P_{Y\mid H}(y\mid 1)}{P_{Y\mid H}(y\mid 0)}
=\left(\frac{\lambda_1}{\lambda_0}\right)^{\!y}e^{-(\lambda_1-\lambda_0)}
\;\underset{\hat H=0}{\overset{\hat H=1}{\gtrless}}\;1,
$$

$$
y\,\ln\!\frac{\lambda_1}{\lambda_0}
\;\underset{\hat H=0}{\overset{\hat H=1}{\gtrless}}\;
\lambda_1-\lambda_0
\;\Longrightarrow\;
\boxed{\;\hat H=1 \iff y\ge \gamma,\quad
\gamma=\frac{\lambda_1-\lambda_0}{\ln(\lambda_1/\lambda_0)}.\;}
$$

Es decir: **contar los fotones y comparar con un umbral $\gamma$**. Es el mismo patrón que en el
canal gaussiano — sólo cambian las densidades. (Para la priori no uniforme, la regla MAP agrega
$\ln\eta$ del lado derecho, con $\eta=P_H(0)/P_H(1)$.)

---

### 7. Para el pizarrón

1. Bayes: $P_{H\mid Y}\propto P_H(i)\,f_{Y\mid H}(y\mid i)$.
2. **MAP** = elegir el $i$ que maximiza eso (descartar $f_Y(y)$); es óptimo.
3. Uniforme ⇒ **ML** = maximizar la verosimilitud.
4. **Regiones de decisión** $\mathcal R_i$ ⇒ $P_e=\sum_i P_H(i)\,P_e(i)$.
5. El método no depende de la distribución: Poisson, gaussiana, etc. — se compara con un umbral.
