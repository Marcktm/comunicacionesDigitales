## Ruido gaussiano blanco N(t)

> **Referencias.** Bixio Rimoldi §3.2 (*White Gaussian noise*, **págs. 97–99**). Definimos el
> ruido **a través de lo que se puede medir**: salidas de filtros.

---

### 1. Por qué se define así

$N(t)$ **no es observable directamente**: todo instrumento (antena, cable, filtro) entrega una
versión filtrada. Si el filtro tiene respuesta $h(t)$, lo que se mide en el instante $t_i$ es

$$
Z(t_i)=\int N(\alpha)\,h(t_i-\alpha)\,d\alpha ,
$$

y llamando $g_i(\alpha)=h(t_i-\alpha)$ (una función fija por cada medición), toda medición es de
la forma $Z_i=\int N(\alpha)\,g_i(\alpha)\,d\alpha$. **La definición se hace sobre estos $Z_i$.**

---

### 2. Definición

$N(t)$ es **ruido blanco gaussiano** de densidad espectral de potencia $N_0/2$ si, para toda
colección finita de funciones $g_1,\dots,g_k\in\mathcal L^2$, las variables

$$
Z_i=\int N(\alpha)\,g_i(\alpha)\,d\alpha,\qquad i=1,\dots,k,
$$

son **conjuntamente gaussianas de media cero** con covarianza

$$
\boxed{\;\operatorname{cov}(Z_i,Z_j)=\mathbb E[Z_iZ_j^*]=\frac{N_0}{2}\int g_i(t)\,g_j^*(t)\,dt
=\frac{N_0}{2}\,\langle g_i,g_j\rangle .\;}
$$

**Lecturas de la fórmula:** si $i=j$, la varianza es $\tfrac{N_0}{2}\lVert g_i\rVert^2$; si
$g_i\perp g_j$, la covarianza es 0; $N_0/2$ es la potencia de ruido por unidad de ancho de banda.

---

### 3. El Lema clave (el hecho a recordar)

> **Lema.** Si $\{g_1(t),\dots,g_k(t)\}$ es un conjunto **ortonormal**, entonces
> $Z=(Z_1,\dots,Z_k)^{\mathsf T}$ es un vector gaussiano de media cero con componentes **iid** de
> varianza $\sigma^2=\dfrac{N_0}{2}$:  $Z\sim\mathcal N\!\big(0,\tfrac{N_0}{2}I_k\big)$.

**Demostración.** Por ortonormalidad $\langle g_i,g_j\rangle=\delta_{ij}$, así que la fórmula de
covarianza da $\operatorname{var}(Z_i)=\tfrac{N_0}{2}$ y $\operatorname{cov}(Z_i,Z_j)=0$ para
$i\neq j$. Como además son **conjuntamente gaussianas**, incorrelación ⇒ **independencia**
(propiedad de los vectores gaussianos, Unidad 1). $\blacksquare$

Este Lema es el **puente exacto** al canal discreto de la Unidad 2: proyectar el ruido sobre una
base ortonormal produce el $Z\sim\mathcal N(0,\sigma^2 I)$ que ya sabemos manejar.

---

### 4. Por qué "blanco"

Tomemos dos filtros pasa-banda de bandas **no solapadas** e idénticas salvo traslación en
frecuencia. Por Parseval, sus respuestas al impulso son **ortogonales** ⇒ sus salidas (muestreadas
incluso en instantes distintos) son gaussianas **iid, de igual varianza**. Repitiendo con $n$
bandas: la potencia del ruido se reparte **uniformemente en todas las frecuencias** — igual que
la luz blanca reparte su potencia entre todos los colores.

**Otros ruidos.** El **térmico (Johnson)** de todo conductor es blanco y gaussiano con excelente
aproximación (más el solar y el cósmico, según hacia dónde apunte la antena). Los ruidos
**artificiales** (motores, líneas eléctricas) en general no son ni blancos ni gaussianos, y un
buen diseño intenta no captarlos. El **shot noise** proviene de la naturaleza discreta de la
carga.

---

### 5. Para el pizarrón

1. Sólo se observan **salidas de filtros**: $Z_i=\int N g_i$ ⇒ la definición se hace sobre los $Z_i$.
2. Definición: $Z_i$ conjuntamente gaussianos, media 0, $\operatorname{cov}=\tfrac{N_0}{2}\langle g_i,g_j\rangle$.
3. **Lema:** base ortonormal ⇒ $Z\sim\mathcal N(0,\tfrac{N_0}{2}I)$ (incorrelación + gaussiano ⇒ iid).
4. "Blanco" = potencia uniforme en frecuencia (filtros de bandas disjuntas ⇒ salidas iid).
5. Térmico ≈ blanco gaussiano; artificial en general no.
