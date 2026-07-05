## Densidad espectral de potencia (PSD) — derivación completa

> **Referencias.** Bixio Rimoldi §5.3 (**págs. 163–167**). Los entes regulatorios exigen que la
> PSD del transmisor quede bajo una **máscara** en frecuencia: hay que saber calcularla. Esta es
> la demostración que se rinde **completa** — cada paso importa.

---

### 1. El modelo (y por qué aparece el dither Θ)

La señal transmitida se modela como

$$
X(t)=\sum_{i=-\infty}^{\infty} X_i\,\xi(t-iT-\Theta),
$$

donde $\{X_i\}$ es un proceso discreto **WSS de media cero**, $\xi(t)$ es un pulso $\mathcal L^2$
arbitrario, y $\Theta\sim\mathcal U[0,T)$ es un **corrimiento aleatorio (dither)** independiente
de los $X_i$.

**Por qué el dither:** para quien mide la PSD, el instante de encendido del transmisor (y el
retardo de propagación) son desconocidos: $\Theta$ modela esa incertidumbre. Matemáticamente,
sin $\Theta$ el proceso sería cicloestacionario (su estadística dependería de $t$); **con** el
dither, $X(t)$ resulta **WSS** y la PSD queda bien definida.

---

### 2. Las dos herramientas

**Autocovarianza de los símbolos** (depende sólo del corrimiento $i$, por WSS y media cero):

$$
K_X[i]\;\triangleq\;\mathbb E\big[X_{j+i}X_j^*\big].
$$

**Función de autosimilitud del pulso:**

$$
R_\xi(\tau)\;\triangleq\;\int_{-\infty}^{\infty}\xi(\alpha+\tau)\,\xi^*(\alpha)\,d\alpha .
$$

---

### 3. Media cero de X(t)

Por independencia entre $X_i$ y $\Theta$, y $\mathbb E[X_i]=0$:

$$
\mathbb E[X(t)]=\sum_i \mathbb E[X_i]\,\mathbb E[\xi(t-iT-\Theta)]=0 .
$$

---

### 4. Autocovarianza de X(t) — el corazón de la demostración

Escribimos $K_X(t+\tau,t)=\mathbb E[X(t+\tau)X^*(t)]$ y expandimos las dos sumas:

$$
K_X(t+\tau,t)=\mathbb E\Big[\sum_i\sum_j X_iX_j^*\;\xi(t+\tau-iT-\Theta)\,\xi^*(t-jT-\Theta)\Big].
$$

**(a) Separar las esperanzas.** $X_iX_j^*$ y $\Theta$ son independientes, así que la esperanza
del producto se factoriza, y $\mathbb E[X_iX_j^*]=K_X[i-j]$:

$$
=\sum_i\sum_j K_X[i-j]\;\mathbb E\big[\xi(t+\tau-iT-\Theta)\,\xi^*(t-jT-\Theta)\big].
$$

**(b) Cambio de variable y promedio sobre el dither.** Con $k=i-j$ y
$\mathbb E_\Theta[\,\cdot\,]=\tfrac1T\int_0^T(\cdot)\,d\theta$, la doble suma se convierte en una
suma en $k$ por una suma en $j$ de integrales sobre un período.

**(c) La identidad que "pega" las integrales.** Para cualquier $u:\mathbb R\to\mathbb R$, $a\in\mathbb R$
y $b>0$:

$$
\sum_{i=-\infty}^{\infty}\int_a^{a+b} u(x+ib)\,dx=\int_{-\infty}^{\infty}u(x)\,dx .
$$

*(Idea: integrar en $[a,a+b]$ la función desplazada $i$ veces equivale a recorrer, tramo a
tramo, toda la recta.)* Aplicándola con $b=T$, la suma en $j$ de integrales sobre $[0,T)$ se
convierte en **una** integral sobre toda la recta, que es exactamente $R_\xi(\tau-kT)$:

$$
\boxed{\;K_X(\tau)=\frac1T\sum_{k} K_X[k]\,R_\xi(\tau-kT).\;}
$$

No depende de $t$: junto con la media nula, **$X(t)$ es WSS** (gracias al dither).

---

### 5. De la autocovarianza a la PSD

Falta un hecho: por Parseval, la autosimilitud del pulso y $|\xi_{\mathcal F}(f)|^2$ son **par de
Fourier**:

$$
R_\xi(\tau)=\int \xi_{\mathcal F}(f)\,\xi_{\mathcal F}^*(f)\,e^{j2\pi f\tau}\,df
=\int |\xi_{\mathcal F}(f)|^2 e^{j2\pi f\tau}\,df .
$$

Transformando $K_X(\tau)$ (cada término $R_\xi(\tau-kT)$ aporta $|\xi_{\mathcal F}|^2e^{-j2\pi kfT}$):

$$
\boxed{\;S_X(f)=\frac{|\xi_{\mathcal F}(f)|^2}{T}\sum_{k}K_X[k]\,e^{-j2\pi k fT}.\;}
$$

**Lectura en dos factores:** $\dfrac{|\xi_{\mathcal F}(f)|^2}{T}$ es la "PSD del pulso" y
$\sum_k K_X[k]e^{-j2\pi kfT}$ la "PSD de la secuencia de símbolos" (su transformada de tiempo
discreto evaluada en $fT$). **El pulso pone la forma; la correlación de los símbolos la modula.**

---

### 6. Caso 1: símbolos incorrelacionados

Si $K_X[k]=\mathcal E\,\delta_{k0}$ (con $\mathcal E=\mathbb E[|X_i|^2]$):

$$
\boxed{\;S_X(f)=\mathcal E\,\frac{|\xi_{\mathcal F}(f)|^2}{T}.\;}
$$

La PSD **es** el espectro del pulso. Diseño directo: si querés cierta máscara, elegí el pulso.
Con el pulso sinc, $S_X$ es **plana** en $[-\tfrac{1}{2T},\tfrac{1}{2T}]$; con el rectángulo,
$\propto\operatorname{sinc}^2(fT)$ (lóbulos que decaen lento).

---

### 7. Caso 2: codificación correlativa (moldear la PSD con el encoder)

Sea $X_i=\sqrt{2\mathcal E}\,(B_i-B_{i-2})$ con $B_i$ iid uniformes en $\{0,1\}$. Es de media
cero, y calculando $K_X[k]=\mathbb E[X_{j+k}X_j]$ quedan sólo tres términos:

$$
K_X[0]=\mathcal E,\qquad K_X[\pm2]=-\tfrac{\mathcal E}{2},\qquad K_X[k]=0\ \text{si no}.
$$

Sustituyendo en la fórmula y usando $e^{j\alpha}+e^{-j\alpha}=2\cos\alpha$,
$1-\cos\alpha=2\sin^2\tfrac{\alpha}{2}$:

$$
S_X(f)=\frac{|\xi_{\mathcal F}(f)|^2}{T}\,\mathcal E\big(1-\cos 4\pi fT\big)
=\frac{|\xi_{\mathcal F}(f)|^2}{T}\;2\mathcal E\sin^2(2\pi fT).
$$

**Se anula en $f=0$**: útil si el canal bloquea DC (amplificadores acoplados en AC). Como este
encoder es lineal e invariante, equivale a usar el pulso $\tilde\xi(t)=\xi(t)-\xi(t-2T)$
(*señalización de respuesta parcial*).

---

### 8. Para el pizarrón (hilo completo)

1. Modelo con **dither** $\Theta\sim\mathcal U[0,T)$ → WSS.
2. Definir $K_X[k]$ y $R_\xi(\tau)$; media de $X(t)$ = 0.
3. Expandir $\mathbb E[X(t+\tau)X^*(t)]$ → (a) independencia, (b) $k=i-j$ + promedio en $\Theta$,
   (c) identidad $\sum_i\int_a^{a+b}=\int_{\mathbb R}$ ⇒ $K_X(\tau)=\tfrac1T\sum_k K_X[k]R_\xi(\tau-kT)$.
4. Parseval: $R_\xi\leftrightarrow|\xi_{\mathcal F}|^2$ ⇒
   $S_X=\tfrac{|\xi_{\mathcal F}|^2}{T}\sum_k K_X[k]e^{-j2\pi kfT}$.
5. Incorrelados ⇒ $S_X=\mathcal E|\xi_{\mathcal F}|^2/T$; correlativo $B_i-B_{i-2}$ ⇒
   $2\mathcal E\sin^2(2\pi fT)$ (nulo en DC).
