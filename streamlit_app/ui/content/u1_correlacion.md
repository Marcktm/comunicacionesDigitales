## Vector de valor esperado y matriz de correlación

> **Referencias.** Roy Yates (vectores aleatorios); se usa en Bixio §2.4.2 (**pág. 35**) y §2.10
> (**pág. 61**). Herramientas
> para trabajar con **varias variables a la vez** (múltiples antenas, muestras, dimensiones).

---

### 1. Vector aleatorio y vector de medias

Un **vector aleatorio** $X=(X_1,\dots,X_n)^{\mathsf T}$ agrupa $n$ variables. Su **vector de
medias** es el vector de las esperanzas componente a componente:

$$
m_X=\mathbb E[X]=(\mathbb E[X_1],\dots,\mathbb E[X_n])^{\mathsf T}.
$$

---

### 2. Matriz de correlación y de covarianza

La **matriz de correlación** (autocorrelación) reúne todos los productos cruzados:

$$
R_X=\mathbb E[X X^{\mathsf T}],\qquad (R_X)_{ij}=\mathbb E[X_i X_j].
$$

La **matriz de covarianza** los centra en la media:

$$
K_X=\mathbb E\big[(X-m_X)(X-m_X)^{\mathsf T}\big],\qquad
(K_X)_{ij}=\operatorname{Cov}(X_i,X_j)=\mathbb E[X_iX_j]-m_i m_j .
$$

Se relacionan por

$$
\boxed{\;R_X=K_X+m_X m_X^{\mathsf T}.\;}
$$

**Propiedades de $K_X$:**

- Es **simétrica** ($K_X=K_X^{\mathsf T}$) y **semidefinida positiva** ($a^{\mathsf T}K_X a\ge0$).
- La **diagonal** son las varianzas: $(K_X)_{ii}=\operatorname{Var}(X_i)=\sigma_i^2$.
- Fuera de la diagonal, las covarianzas. Si las componentes son **incorrelacionadas**, $K_X$ es
  **diagonal**.

---

### 3. Coeficiente de correlación

Normalizando la covarianza:

$$
\rho_{ij}=\frac{\operatorname{Cov}(X_i,X_j)}{\sigma_i\,\sigma_j}\in[-1,1].
$$

$\rho=0$ ⇒ incorrelacionadas; $\rho=\pm1$ ⇒ dependencia lineal exacta. En el plano, $\rho$
controla la **inclinación y el achatamiento** de la nube de puntos (ver la gráfica de abajo, con
su **elipse de covarianza**).

---

### 4. Transformación lineal

Si $Y=AX+b$ (con $A$ matriz y $b$ vector constantes), entonces

$$
\boxed{\;m_Y=A\,m_X+b,\qquad K_Y=A\,K_X\,A^{\mathsf T}.\;}
$$

Esta regla es la que permite, por ejemplo, **blanquear** el ruido (elegir $A$ para que $K_Y$ sea
diagonal) o rotar hacia la dirección de decisión (ver *Observaciones vectoriales* y *Vectores
gaussianos*).

---

### 5. Para el pizarrón

1. $m_X=\mathbb E[X]$; $R_X=\mathbb E[XX^{\mathsf T}]$; $K_X=\mathbb E[(X-m)(X-m)^{\mathsf T}]$.
2. $R_X=K_X+m_X m_X^{\mathsf T}$.
3. $K_X$ simétrica y semidefinida positiva; diagonal = varianzas; incorrelación ⇒ $K$ diagonal.
4. $\rho_{ij}=K_{ij}/(\sigma_i\sigma_j)\in[-1,1]$.
5. $Y=AX+b\Rightarrow m_Y=Am_X+b,\ K_Y=AK_XA^{\mathsf T}$.
