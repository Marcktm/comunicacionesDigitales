## Coseno realzado y raíz de coseno realzado (RRC)

> **Referencias.** Bixio Rimoldi §5.5 (**págs. 170–172**; la Fig. **5.6, pág. 170** muestra
> $|\psi_{\mathcal F}|^2$ y el pulso para $\beta=\tfrac12$) y apéndice §5.14 (respuesta al
> impulso). La familia de pulsos de Nyquist **estándar de la industria**.

---

### 1. El coseno realzado

Para $\beta\in(0,1)$ (factor de **roll-off**) se define $|\psi_{\mathcal F}(f)|^2$ por tramos:

$$
|\psi_{\mathcal F}(f)|^2=
\begin{cases}
T, & |f|\le\dfrac{1-\beta}{2T},\\[6pt]
\dfrac{T}{2}\left[1+\cos\!\Big(\dfrac{\pi T}{\beta}\Big(|f|-\dfrac{1-\beta}{2T}\Big)\Big)\right],
& \dfrac{1-\beta}{2T}<|f|<\dfrac{1+\beta}{2T},\\[6pt]
0, & |f|\ge\dfrac{1+\beta}{2T}.
\end{cases}
$$

Zona plana + transición coseno + cero. La transición está construida con la **simetría de
banda** alrededor de $\tfrac{1}{2T}$, así que **cumple el criterio de Nyquist** con parámetro
$T$ (verificable plegando; la demo de abajo lo hace numéricamente).

- $\beta$ chico → transición abrupta, ancho de banda casi mínimo, pulso que decae lento.
- $\beta$ grande → transición suave, hasta $\tfrac{1+\beta}{2T}$ de banda, pulso que decae rápido.

---

### 2. Por qué se usa la RAÍZ (root-raised-cosine)

Lo que debe cumplir Nyquist es el **conjunto TX + RX**: el transmisor conforma con
$\psi_{\mathcal F}(f)$ y el receptor aplica el **matched filter** (de nuevo $\psi$), así que el
efecto total es $|\psi_{\mathcal F}(f)|^2$. Por eso se reparte: **media raíz en TX, media raíz en
RX**, y el producto es el coseno realzado completo. Con la identidad
$\tfrac12(1+\cos\alpha)=\cos^2\tfrac\alpha2$, la raíz queda

$$
\psi_{\mathcal F}(f)=
\begin{cases}
\sqrt T, & |f|\le\frac{1-\beta}{2T},\\[4pt]
\sqrt T\,\cos\!\Big(\frac{\pi T}{2\beta}\big(|f|-\frac{1-\beta}{2T}\big)\Big), & \frac{1-\beta}{2T}<|f|\le\frac{1+\beta}{2T},\\[4pt]
0, & \text{si no.}
\end{cases}
$$

---

### 3. El pulso en el tiempo y sus puntos singulares

La anti-transformada (respuesta al impulso RRC) es

$$
\psi(t)=\frac{4\beta}{\pi\sqrt T}\;
\frac{\cos\!\big((1+\beta)\pi\tfrac tT\big)+\dfrac{(1-\beta)\pi}{4\beta}\,
\operatorname{sinc}\!\big((1-\beta)\tfrac tT\big)}
{1-\big(4\beta\tfrac tT\big)^2}.
$$

En $t=\pm\dfrac{T}{4\beta}$ el denominador se anula **y también el numerador** (indeterminación
$0/0$). El valor correcto es el **límite** (regla de L'Hôpital):

$$
\lim_{t\to\pm T/4\beta}\psi(t)=\frac{\beta}{\pi\sqrt{2T}}
\left[(\pi+2)\sin\frac{\pi}{4\beta}+(\pi-2)\cos\frac{\pi}{4\beta}\right].
$$

**Al programarlo** hay que tratar esos puntos aparte o la fórmula devuelve NaN — así está hecho
en `core/pulses.py` (y verificado por test). Con $\beta=0$ el pulso se reduce al
$\tfrac{1}{\sqrt T}\operatorname{sinc}(t/T)$: el sinc es el caso límite de la familia.

---

### 4. El trade-off de β (lo que se ve en el Lab 4)

El pulso es real, par y de **soporte infinito**: en la práctica se **trunca** (y se retrasa para
hacerlo causal). Ahí manda $\beta$:

- **β grande** ⇒ decae rápido ⇒ se puede truncar corto sin generar ISI… pero ocupa más banda.
- **β chico** ⇒ banda casi mínima… pero decae lento: truncarlo corto **rompe la ortogonalidad**
  y aparece ISI (se ve en el diagrama de ojo, página siguiente).

---

### 5. Para el pizarrón

1. RC por tramos (plano/coseno/cero) — cumple Nyquist por simetría de banda.
2. TX·RX = $|\psi_{\mathcal F}|^2$ ⇒ usar la **raíz** en cada extremo ($\cos^2$ ⇒ $\cos$).
3. Pulso temporal: fórmula + **L'Hôpital en $t=\pm T/4\beta$** (¡tratarlo en el código!).
4. $\beta=0$ ⇒ sinc. Trade-off: banda ($\propto 1+\beta$) vs decaimiento/truncado.
