## Energía de la señal y espacio de producto interno

> **Referencias.** Bixio Rimoldi §3.1 (*Introduction*, **págs. 95–97**; el modelo del canal es la
> **Fig. 3.1, pág. 95**). Pasamos del canal discreto al **canal AWGN de tiempo continuo**.

---

### 1. El nuevo modelo de canal

Ahora el transmisor emite una **forma de onda continua** $w_i(t)$ del conjunto
$\mathcal W=\{w_0(t),\dots,w_{m-1}(t)\}$, y el canal suma **ruido blanco gaussiano** $N(t)$:

$$
H=i:\qquad R(t)=w_i(t)+N(t).
$$

Los supuestos y el objetivo son los mismos que en la Unidad 2 (fuente, transmisor y canal dados;
minimizar $P_e$). Ejemplos físicos de este canal: un **cable** (si su respuesta es plana en la
banda de la señal) o el enlace **satélite–estación terrestre**.

---

### 2. Energía de una señal

La **norma al cuadrado** de $w_i(t)$ es su energía (a menos de una constante física):

$$
\lVert w_i\rVert^2=\int |w_i(t)|^2\,dt .
$$

**Ejemplo (antena).** Si $w_i(t)$ es la tensión sobre una antena de impedancia resistiva $Z$
(típicamente $50\,\Omega$): la corriente es $w_i(t)/Z$, la potencia instantánea $w_i^2(t)/Z$ y la
energía entregada $\tfrac1Z\int w_i^2(t)\,dt$. Si $w_i(t)$ fuera la corriente, la energía sería
$Z\int w_i^2$. En ambos casos, **proporcional a $\lVert w_i\rVert^2$**.

**Por qué importa la energía (tres razones):**
1. **Regulaciones** limitan la potencia transmitida (seguridad, reutilización del espectro).
2. En **dispositivos móviles** la energía sale de la batería.
3. Sin límite de potencia se podría transmitir a cualquier tasa con cualquier $P_e$: la
   comparación entre esquemas sólo es **justa** a igual potencia.

---

### 3. Dos restricciones técnicas sobre $\mathcal W$

1. **Energía finita:** las señales físicas tienen $\lVert w\rVert^2<\infty$ (y sus combinaciones
   lineales finitas también).
2. **Norma nula ⇒ señal nula:** la única señal de norma cero es la idénticamente nula. (Para una
   $v(t)$ continua con $|v(t_0)|=a>0$, por continuidad $|v(t)|>a/2$ en un intervalo $\mathcal I$
   de largo $\epsilon$, y entonces $\lVert v\rVert^2\ge \tfrac{a^2\epsilon}{4}>0$.)

Con esas dos condiciones, el espacio $\mathcal V$ generado por $\mathcal W$ es un **espacio de
producto interno** de funciones de cuadrado integrable, con

$$
\boxed{\;\langle a,b\rangle=\int a(t)\,b^*(t)\,dt\;}
$$

(el conjugado es superfluo para señales reales). **Toda la geometría de la Unidad 2** — normas,
distancias, proyecciones, planos — se traslada tal cual a funciones.

---

### 4. La estrategia del capítulo

El plan (que se concreta en las páginas siguientes) es **descomponer** transmisor y receptor:

- Transmisor = **encoder** (mensaje → n-tupla $c_i$) + **waveform former** ($c_i$ → $w_i(t)$).
- Receptor = **n-tuple former** ($R(t)$ → $Y\in\mathbb R^n$) + **decoder** (el de la Unidad 2).

Entre el waveform former y el n-tuple former, el sistema se comporta **exactamente** como el
canal AWGN discreto ya resuelto.

---

### 5. Para el pizarrón

1. Canal continuo: $R(t)=w_i(t)+N(t)$ (Fig. 3.1).
2. Energía $=\lVert w\rVert^2=\int|w|^2$; ejemplo antena ($\propto$ tensión² o corriente²).
3. Tres razones para limitar energía: regulación, batería, comparación justa.
4. Energía finita + (norma 0 ⇒ señal 0) ⇒ **espacio de producto interno** $\langle a,b\rangle=\int ab^*$.
5. Estrategia: encoder / waveform former ↔ n-tuple former / decoder.
