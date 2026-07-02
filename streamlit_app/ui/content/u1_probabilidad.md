## Repaso de probabilidad y variable aleatoria

> **Referencias.** Roy Yates, *Probability and Stochastic Processes* (base); se usa en toda la
> materia. Repaso de lo imprescindible para el diseño de receptores.

---

### 1. Espacio de probabilidad y axiomas

Un experimento aleatorio se describe con un **espacio muestral** $\Omega$ (resultados posibles) y
una probabilidad $P$ sobre eventos $A\subseteq\Omega$ que cumple los axiomas de Kolmogorov:

$$
P(A)\ge 0,\qquad P(\Omega)=1,\qquad
P\!\Big(\bigcup_k A_k\Big)=\sum_k P(A_k)\ \ \text{(eventos disjuntos).}
$$

**Probabilidad condicional** e **independencia**:

$$
P(A\mid B)=\frac{P(A\cap B)}{P(B)},\qquad A\perp B\iff P(A\cap B)=P(A)P(B).
$$

**Probabilidad total** y **Bayes** (con $\{B_i\}$ una partición de $\Omega$):

$$
P(A)=\sum_i P(A\mid B_i)P(B_i),\qquad
P(B_i\mid A)=\frac{P(A\mid B_i)P(B_i)}{\sum_j P(A\mid B_j)P(B_j)}.
$$

Bayes es la base de la regla **MAP** del receptor.

---

### 2. Variable aleatoria

Una **variable aleatoria** $X$ asigna un número a cada resultado. Se describe con la **función de
distribución acumulada** $F_X(x)=P\{X\le x\}$, y según su tipo:

- **Discreta:** función de masa $p_X(x)=P\{X=x\}$, con $\sum_x p_X(x)=1$.
- **Continua:** densidad $f_X(x)=\dfrac{dF_X}{dx}$, con $\int f_X(x)\,dx=1$ y
  $P\{a\le X\le b\}=\int_a^b f_X(x)\,dx$.

---

### 3. Esperanza, varianza y momentos

$$
\mathbb E[X]=\sum_x x\,p_X(x)\ \ \text{ó}\ \ \int x\,f_X(x)\,dx,\qquad
\operatorname{Var}(X)=\mathbb E[(X-\mathbb E[X])^2]=\mathbb E[X^2]-\mathbb E[X]^2 .
$$

**Propiedades** (muy usadas): linealidad $\mathbb E[aX+b]=a\,\mathbb E[X]+b$;
$\operatorname{Var}(aX+b)=a^2\operatorname{Var}(X)$; si $X\perp Y$ entonces
$\mathbb E[XY]=\mathbb E[X]\mathbb E[Y]$ y $\operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)$.

---

### 4. Distribuciones que aparecen en la materia

| Distribución | pmf/pdf | $\mathbb E[X]$ | $\operatorname{Var}(X)$ |
|---|---|---|---|
| Bernoulli($p$) | $p^x(1-p)^{1-x}$, $x\in\{0,1\}$ | $p$ | $p(1-p)$ |
| Binomial($n,p$) | $\binom{n}{x}p^x(1-p)^{n-x}$ | $np$ | $np(1-p)$ |
| Poisson($\lambda$) | $\dfrac{\lambda^x}{x!}e^{-\lambda}$ | $\lambda$ | $\lambda$ |
| Uniforme($a,b$) | $\dfrac{1}{b-a}$ en $[a,b]$ | $\dfrac{a+b}{2}$ | $\dfrac{(b-a)^2}{12}$ |
| Exponencial($\lambda$) | $\lambda e^{-\lambda x}$, $x\ge0$ | $1/\lambda$ | $1/\lambda^2$ |
| Laplaciana($\mu,b$) | $\dfrac{1}{2b}e^{-|x-\mu|/b}$ | $\mu$ | $2b^2$ |
| Gaussiana($m,\sigma^2$) | $\dfrac{1}{\sqrt{2\pi\sigma^2}}e^{-(x-m)^2/2\sigma^2}$ | $m$ | $\sigma^2$ |

La **Poisson** modela el conteo de fotones (canal óptico); la **gaussiana** modela el ruido
térmico (canal AWGN).

---

### 5. La gaussiana en detalle

Si $Z\sim\mathcal N(0,1)$, se **estandariza** cualquier $X\sim\mathcal N(m,\sigma^2)$ mediante
$Z=\dfrac{X-m}{\sigma}$. La probabilidad de cola derecha se expresa con la **función $Q$**:

$$
P\{X\ge x\}=Q\!\left(\frac{x-m}{\sigma}\right),\qquad
Q(x)=\frac{1}{\sqrt{2\pi}}\int_x^\infty e^{-\xi^2/2}\,d\xi .
$$

Es la herramienta central para calcular probabilidades de error (ver *Función Q* en Unidad 2).

---

### 6. Para el pizarrón

1. Axiomas + condicional + **Bayes** (base de MAP).
2. V.a.: $F_X$, pmf/pdf; $\mathbb E$, $\operatorname{Var}=\mathbb E[X^2]-\mathbb E[X]^2$.
3. Linealidad de $\mathbb E$; varianza escala con $a^2$; independencia ⇒ producto de esperanzas.
4. Poisson (fotones) y **gaussiana** (ruido térmico) son las clave.
5. Estandarizar + **función $Q$** para colas gaussianas.
