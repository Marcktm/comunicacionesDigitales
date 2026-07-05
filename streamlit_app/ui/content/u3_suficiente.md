## Estadística suficiente y canal discreto equivalente

> **Referencias.** Bixio Rimoldi §3.3 (*Observables and sufficient statistics*, **págs. 99–102**;
> la geometría es la **Fig. 3.3, pág. 101**). El resultado central del capítulo: **proyectar
> $R(t)$ sobre el espacio de señales no pierde información**.

---

### 1. Qué puede medir el receptor

Como $N(t)$ sólo se observa filtrado, toda medición física es de la forma

$$
V_i=\int R(\alpha)\,g_i^*(\alpha)\,d\alpha,\qquad i=1,\dots,k,
$$

para funciones $g_i$ de energía finita y un $k$ **finito pero arbitrario**. (Esto incluye, por
ejemplo, filtrar pasa-bajos con corte enorme y muestrear según el teorema de muestreo.)

---

### 2. El candidato: proyección sobre el espacio de señales

Sea $\mathcal V$ el espacio generado por $\mathcal W=\{w_0,\dots,w_{m-1}\}$ y sea
$\{\psi_1,\dots,\psi_n\}$ una base **ortonormal** de $\mathcal V$. Definimos

$$
Y_j=\int R(\alpha)\,\psi_j^*(\alpha)\,d\alpha,\qquad Y=(Y_1,\dots,Y_n)^{\mathsf T}.
$$

**Afirmación:** $Y$ es **estadística suficiente** para $H$ entre cualquier colección de
mediciones que la contenga.

---

### 3. Demostración

**Paso 1 — completar la base.** Dadas otras mediciones $V=(V_1,\dots,V_k)$ con funciones $g_i$,
sea $\mathcal U$ el espacio generado por $\mathcal V\cup\{g_1,\dots,g_k\}$. Extendemos la base a
$\{\psi_1,\dots,\psi_n,\phi_1,\dots,\phi_{\tilde n}\}$ (los $\phi_j$ ortogonales a $\mathcal V$) y
definimos $U_j=\int R\,\phi_j^*$.

**Paso 2 — $V$ se recupera de $(Y,U)$.** Cada $g_i\in\mathcal U$ se expande en la base:
$g_i=\sum_j\xi_{i,j}\psi_j+\sum_j\xi_{i,j+n}\phi_j$, y por linealidad de la integral

$$
V_i=\sum_{j=1}^{n}\xi_{i,j}^*\,Y_j+\sum_{j=1}^{\tilde n}\xi_{i,j+n}^*\,U_j .
$$

Basta entonces probar que, del par $(Y,U)$, la parte útil es $Y$.

**Paso 3 — qué contiene cada parte.** Con $H=i$, $R=w_i+N$ y $w_i=\sum_j c_{i,j}\psi_j$:

$$
Y_j=\int (w_i+N)\,\psi_j^*=c_{i,j}+Z_{|V,j}
\;\Longrightarrow\;
\boxed{\;Y=c_i+Z_{|V},\quad Z_{|V}\sim\mathcal N\!\big(0,\tfrac{N_0}{2}I_n\big);}
$$

$$
U_j=\int (w_i+N)\,\phi_j^*=\underbrace{\int w_i\,\phi_j^*}_{=0\ (w_i\in\mathcal V\perp\phi_j)}+\int N\,\phi_j^*
\;\Longrightarrow\;
\boxed{\;U=Z_{\perp V}\sim\mathcal N\!\big(0,\tfrac{N_0}{2}I_{\tilde n}\big)\ \text{ — no depende de } H.}
$$

Además $Z_{|V}$ y $Z_{\perp V}$ son independientes entre sí y de $H$ (proyecciones sobre
funciones ortogonales, Lema del ruido blanco).

**Paso 4 — Fisher–Neyman.** La densidad conjunta se **factoriza**:

$$
f_{Y,U\mid H}(y,u\mid i)=f_{Y\mid H}(y\mid i)\cdot f_U(u),
$$

con $f_U$ independiente de $i$. Por el teorema de factorización, $Y$ es **suficiente** y $U$ es
**irrelevante**. $\blacksquare$

---

### 4. Lectura geométrica (Fig. 3.3)

$R(t)$ se descompone en su **proyección sobre $\mathcal V$** (que contiene $c_i$ + ruido en el
plano) y su componente **perpendicular** (sólo ruido). El receptor puede quedarse con la sombra
de $R$ sobre el plano de señales y descartar lo demás. *(La gráfica 3D de abajo reproduce esta
figura.)*

**¿Se puede tirar parte de $Y$?** No: si $Y=(Y_a,Y_b)$ y $c_{i,b}$ no se deduce de $Y_a$,
entonces $Y_b$ sigue aportando información sobre $i$ (no hay cadena de Markov $H\to Y_a\to Y$).
Se necesitan **todas** las componentes.

---

### 5. El canal discreto equivalente

El problema que queda es **exactamente** el de la Unidad 2:

$$
H=i:\qquad Y=c_i+Z,\qquad Z\sim\mathcal N\!\big(0,\tfrac{N_0}{2}I_n\big),
$$

con $\sigma^2=N_0/2$. Todo lo aprendido (MAP/ML, mínima distancia, Voronoi, $Q$) aplica directo.

---

### 6. Para el pizarrón

1. Mediciones = $\int R\,g_i^*$ ($k$ finito arbitrario).
2. Candidato: $Y_j=\langle R,\psi_j\rangle$ con base ortonormal de $\mathcal V$.
3. Extender base; $V$ = combinación de $(Y,U)$.
4. $Y=c_i+Z_{|V}$; $U=Z_{\perp V}$ **sin** $H$; independencia.
5. Factorización de **Fisher–Neyman** ⇒ $Y$ suficiente, $U$ irrelevante.
6. Canal discreto equivalente con $\sigma^2=N_0/2$.
