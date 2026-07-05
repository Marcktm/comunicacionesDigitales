## Criterio de Nyquist para bases ortonormales

> **Referencias.** Bixio Rimoldi §5.4 (**págs. 167–170**; la simetría de banda es la
> **Fig. 5.3, pág. 168**). Buscamos la condición **en frecuencia** para que el pulso sea
> ortonormal a sus traslados — la herramienta central de diseño del pulso.

---

### 1. Qué queremos y por qué

De la PSD sabemos que con símbolos incorrelacionados $S_X\propto|\psi_{\mathcal F}(f)|^2$: el
espectro del pulso decide la máscara. Pero el pulso arrastra otra restricción: para que
$\{\psi(t-jT)\}$ sirva de **base ortonormal** (y el receptor recupere símbolos sin
interferencia), debe cumplir

$$
\int_{-\infty}^{\infty}\psi(t-nT)\,\psi^*(t)\,dt=\delta_{n0}
\qquad(\text{norma 1 y ortogonal a sus traslados}).
$$

El criterio de Nyquist traduce esta condición temporal a una condición **simple** sobre
$|\psi_{\mathcal F}(f)|^2$.

---

### 2. La derivación

**Paso 1 — Parseval.** El producto interno temporal pasa a frecuencia (el traslado $nT$ se
vuelve una exponencial):

$$
\delta_{n0}=\int \psi(t-nT)\psi^*(t)\,dt
=\int |\psi_{\mathcal F}(f)|^2\,e^{-j2\pi n T f}\,df .
$$

**Paso 2 — plegar el espectro.** Partimos la recta de frecuencias en tramos de ancho $1/T$ y
trasladamos cada tramo al intervalo base $[-\tfrac{1}{2T},\tfrac{1}{2T}]$. Como
$e^{-j2\pi nT(f-k/T)}=e^{-j2\pi nTf}$ (pues $e^{j2\pi nk}=1$), las exponenciales no cambian y

$$
\delta_{n0}=\int_{-1/2T}^{1/2T}\underbrace{\sum_{k\in\mathbb Z}\Big|\psi_{\mathcal F}\Big(f-\frac kT\Big)\Big|^2}_{\triangleq\,g(f)}\;e^{-j2\pi n T f}\,df .
$$

**Paso 3 — identificar coeficientes de Fourier.** $g(f)$ es periódica de período $1/T$, y la
integral de arriba es ($1/T$ veces) su $n$-ésimo coeficiente de Fourier. La condición
$\delta_{n0}$ dice que todos los coeficientes son cero salvo el de orden 0 (que vale $T$). Una
función periódica con esos coeficientes es **constante**:

$$
\boxed{\;\sum_{k=-\infty}^{\infty}\Big|\psi_{\mathcal F}\Big(f-\frac kT\Big)\Big|^2=T
\quad\text{para todo } f\;}
\qquad\text{(criterio de Nyquist con parámetro } T\text{)}.
$$

*(Rigurosamente la igualdad es en el sentido $\mathcal L^2$ — "l.i.m." —: cambiar el espectro en
puntos aislados no cambia el pulso. En la práctica los espectros son suaves y se ignora.)*

**Lectura:** replicá $|\psi_{\mathcal F}|^2$ cada $1/T$ y sumá: si da **plano = T**, el pulso es
ortonormal a sus traslados. Como el plegado es periódico, alcanza verificar **un** intervalo de
ancho $1/T$.

---

### 3. Consecuencias

**Ancho de banda mínimo.** Si el soporte de $|\psi_{\mathcal F}|^2$ cabe en $[-B,B]$ con
$B<\tfrac{1}{2T}$, las réplicas dejan huecos y la suma no puede ser constante: **no existe**
pulso de Nyquist con menos de $B_N=\tfrac{1}{2T}$ (coherente con el teorema de muestreo). El
sinc lo logra exactamente con $B_N$ (rectángulo de altura $T$).

**Simetría de banda (test rápido para $B\le\tfrac1T$).** Si el soporte no pasa de
$[-\tfrac1T,\tfrac1T]$ y el pulso es real, el criterio equivale a

$$
\Big|\psi_{\mathcal F}\Big(\tfrac{1}{2T}-\epsilon\Big)\Big|^2
+\Big|\psi_{\mathcal F}\Big(\tfrac{1}{2T}+\epsilon\Big)\Big|^2=T,
\qquad \epsilon\in\big[0,\tfrac{1}{2T}\big]:
$$

lo que el espectro "pierde" a un lado del borde $\tfrac{1}{2T}$ lo "gana" del otro (antisimetría
alrededor del punto medio, con $|\psi_{\mathcal F}(\tfrac{1}{2T})|^2=\tfrac T2$). El **coseno
realzado** está construido exactamente así.

**Ejemplos que cumplen** (verificables plegando): el rectángulo de altura $T$ en
$[-\tfrac{1}{2T},\tfrac{1}{2T}]$; $T\cos^2(\tfrac\pi2 fT)$ en $[-\tfrac1T,\tfrac1T]$; el
triángulo $T(1-T|f|)$ en $[-\tfrac1T,\tfrac1T]$.

---

### 4. Para el pizarrón

1. Condición temporal: $\int\psi(t-nT)\psi^*=\delta_{n0}$.
2. Parseval ⇒ integral con $e^{-j2\pi nTf}$; plegar en tramos de $1/T$ (las exponenciales no
   cambian).
3. $g(f)$ periódica; $\delta_{n0}$ = sus coeficientes de Fourier ⇒ $g(f)=T$ constante.
4. **Criterio:** $\sum_k|\psi_{\mathcal F}(f-k/T)|^2=T$; basta un período.
5. Mínimo $B_N=\tfrac{1}{2T}$; simetría de banda para $B\le\tfrac1T$.
