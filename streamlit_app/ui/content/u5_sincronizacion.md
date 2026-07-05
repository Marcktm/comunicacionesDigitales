## Sincronización de símbolo

> **Referencias.** Bixio Rimoldi §5.7 (**págs. 174–179**): enfoque ML (§5.7.1) y delay locked
> loop (§5.7.2, con las **Figs. 5.10–5.11, págs. 176–177**). El último eslabón: encontrar
> **cuándo** muestrear.

---

### 1. El problema

Todo lo anterior asume que el receptor muestrea en $t=jT$ exactos. Pero entre TX y RX hay un
**retardo desconocido** $\tau$ (propagación + relojes no alineados): la señal útil es

$$
y(t)=\sum_i s_i\,R_\psi(t-iT-\tau)+\text{ruido},
$$

y muestrear con error $\Delta=\hat\tau-\tau$ genera **ISI** (Unidad 5, página del ojo: la
apertura horizontal es justamente cuánta $\Delta$ tolerás). Sincronizar = estimar $\tau$.

---

### 2. Enfoque de máxima verosimilitud (ML)

La idea: probar cada retardo candidato $\hat\tau$ y quedarse con el que hace más "verosímil" lo
observado. Desarrollando la verosimilitud gaussiana (como en la Unidad 3, los términos que no
dependen de $\hat\tau$ se descartan), maximizarla equivale a **maximizar la energía de las
muestras de decisión** tomadas con ese retardo:

$$
\hat\tau_{\mathrm{ML}}=\arg\max_{\hat\tau}\;\sum_j \big|y(jT+\hat\tau)\big|^2 .
$$

**Intuición:** con el retardo correcto, muestreás en los **picos** de $R_\psi$ (valores $\pm1$,
energía máxima); con retardo equivocado, muestreás en las faldas (valores intermedios, energía
menor). La métrica $M(\hat\tau)=\sum_j|y(jT+\hat\tau)|^2$ tiene un **máximo periódico** en el
retardo verdadero (módulo $T$). *(La demo de abajo la grafica.)*

En la práctica se calcula por búsqueda sobre una grilla de offsets dentro de un símbolo — es lo
que hace el receptor del Lab 4 para alinear el ojo.

---

### 3. Delay locked loop (DLL): seguir el retardo en línea

La búsqueda ML es costosa para seguir un $\tau$ que **deriva** (relojes reales). El **DLL** lo
sigue con lazo cerrado usando dos muestras auxiliares alrededor del instante de decisión
(*early* y *late*, a $\pm\delta$):

$$
e(\hat\tau)=\big|y(\hat t+\delta)\big|^2-\big|y(\hat t-\delta)\big|^2 .
$$

- Si $\hat\tau$ es correcto, el pico de $R_\psi$ queda **centrado**: early y late caen simétricos
  y $e=0$.
- Si muestreás **tarde**, la muestra early es mayor ⇒ $e<0$ ⇒ corregir hacia atrás; **temprano**,
  al revés.

La curva $e(\Delta)$ (la **curva en S**) cruza cero en $\Delta=0$ con pendiente negativa: es una
señal de error válida para un lazo realimentado que ajusta $\hat\tau$ de a poco, muestreo a
muestreo. Mismo principio que un PLL, pero en el tiempo de símbolo.

---

### 4. Para el pizarrón

1. Retardo desconocido $\tau$ ⇒ muestrear mal ⇒ ISI (ojo horizontal).
2. **ML:** $\hat\tau=\arg\max\sum_j|y(jT+\hat\tau)|^2$ — máximo en los picos de $R_\psi$.
3. **DLL:** error early-late $e=|y(+\delta)|^2-|y(-\delta)|^2$; curva en S, cruce por cero en el
   instante correcto; lazo realimentado para seguir derivas.
