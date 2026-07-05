## La función Q

> **Referencias.** Bixio Rimoldi §2.3 (*The Q function*, **págs. 31–32**; las demostraciones de
> las propiedades están en la pág. 32); apunte Cabrera §1.6–1.8. La función $Q$ es la herramienta
> con la que se expresan las probabilidades de error en canales con ruido gaussiano.

---

### 1. Definición

Para una gaussiana estándar $Z\sim\mathcal N(0,1)$, la integral de su densidad no tiene forma
cerrada elemental, así que se le da nombre propio: la **función $Q$** es el área de la cola
derecha,

$$
\boxed{\;Q(x)\;\triangleq\;\Pr\{Z\ge x\}=\frac{1}{\sqrt{2\pi}}\int_x^{\infty} e^{-\xi^2/2}\,d\xi.\;}
$$

Está definida justamente para que $\Pr\{Z\ge x\}=Q(x)$ sea cierto.

---

### 2. Generalización a $\mathcal N(m,\sigma^2)$

Si $Z\sim\mathcal N(m,\sigma^2)$, **estandarizamos** restando la media y dividiendo por el desvío.
El evento $\{Z\ge x\}$ equivale a $\left\{\dfrac{Z-m}{\sigma}\ge\dfrac{x-m}{\sigma}\right\}$, y
$\dfrac{Z-m}{\sigma}\sim\mathcal N(0,1)$, por lo que

$$
\boxed{\;\Pr\{Z\ge x\}=Q\!\left(\frac{x-m}{\sigma}\right).\;}
$$

Este resultado es el que usamos todo el tiempo para pasar de "probabilidad de que el ruido
supere un umbral" a un valor de $Q$.

---

### 3. Propiedades

Sea $Z\sim\mathcal N(0,1)$ y $F_Z$ su función de distribución acumulada.

1. **Relación con la CDF:** $F_Z(z)=\Pr\{Z\le z\}=1-Q(z)$.
   ($Q(z)$ es el área a la derecha; $F_Z(z)$, a la izquierda; juntas suman 1.)
2. **Valores particulares:** $Q(0)=\tfrac12$, $\;Q(-\infty)=1$, $\;Q(+\infty)=0$.
3. **Simetría:** $Q(-x)+Q(x)=1$ (por la simetría de la campana alrededor de 0).
4. **Cotas (sándwich), para $\alpha>0$:**

$$
\frac{1}{\sqrt{2\pi}\,\alpha}\,e^{-\alpha^2/2}\!\left(\frac{\alpha^2}{1+\alpha^2}\right)
\;<\;Q(\alpha)\;<\;
\frac{1}{\sqrt{2\pi}\,\alpha}\,e^{-\alpha^2/2}.
$$

   Para $\alpha$ grande ambas cotas se juntan: aproximan muy bien a $Q$ en las colas.
5. **Forma con límites fijos** (los límites de integración no dependen de $x$; útil para promediar):

$$
Q(x)=\frac{1}{\pi}\int_0^{\pi/2} \exp\!\left(-\frac{x^2}{2\sin^2\theta}\right)d\theta,\qquad x\ge 0.
$$

6. **Cota superior simple** (la más usada en la práctica):

$$
Q(\alpha)\le \tfrac12\,e^{-\alpha^2/2},\qquad \alpha\ge 0.
$$

---

### 4. Cálculo en Python

Para media 0 y varianza 1 alcanza con la función de supervivencia de SciPy, o la forma con
`erfc` (que sirve para cualquier media/varianza tras estandarizar):

```python
from scipy.special import erfc
import numpy as np

def Q(x):
    return 0.5 * erfc(x / np.sqrt(2.0))   # = scipy.stats.norm.sf(x)

# Pr{Z > x} con Z ~ N(m, sigma^2):  Q((x - m) / sigma)
```

---

### 5. Conexión con la probabilidad de error

En un canal AWGN binario equiprobable, la probabilidad de error resulta
$P_e=Q\!\big(\tfrac{d}{2\sigma}\big)$, donde $d$ es la distancia entre las dos señales. La
función $Q$ traduce directamente la **relación señal-ruido** $\tfrac{d}{2\sigma}$ en una
probabilidad de error. En la gráfica de abajo se ve $Q(\alpha)$ junto con sus cotas (eje $Q$ en
escala logarítmica), tal como aparece en el libro.
