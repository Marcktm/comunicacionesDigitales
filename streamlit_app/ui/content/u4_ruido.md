## Lab 2 — Caracterización del ruido del receptor

> **Referencias.** Notebook `laboratorio2.ipynb` del repo; Bixio §3.2 (ruido blanco gaussiano,
> **págs. 97–99**) y §3.10 (ruido térmico). Verificación **experimental** del modelo AWGN que
> sostiene toda la materia.

---

### 1. La pregunta

Las Unidades 2 y 3 modelan el ruido como **gaussiano, blanco y aditivo**. ¿Es cierto en un
receptor real? El Lab 2 lo mide: se captura la salida del receptor **sin señal transmitida** y
se analiza estadísticamente.

---

### 2. Cómo capturar "sólo ruido"

Configuración clave (la del notebook):

- **TX en silencio**: atenuación máxima (−89 dB) y buffer de ceros.
- **TX y RX en portadoras distintas** (TX 2400 MHz, RX 915 MHz) para que ni el residuo del TX
  se cuele en el RX.
- **Ganancia RX manual y alta** (70 dB): el AGC en manual para que la estadística no cambie
  entre capturas, y alta para que el ruido del frontend domine sobre el de cuantización.
- Buffer grande (2¹⁸ o más): la estadística necesita muestras.

Lo capturado es el **ruido térmico** del frontend (LNA + mezclador + filtros), amplificado.

---

### 3. El análisis (el pipeline del laboratorio)

Sobre las muestras complejas $r[n]=I[n]+jQ[n]$:

1. **Series temporales** de I y Q: deben verse "ruidosas", sin estructura.
2. **Media y varianza** de I y Q: media ≈ 0 (salvo offset de DC pequeño); varianzas de I y Q
   similares.
3. **Histogramas** de I y Q con la **pdf gaussiana** superpuesta (con la media y varianza
   muestrales): deben calzar.
4. **Q–Q plot** contra la normal: si los puntos caen sobre la recta, la distribución es
   gaussiana (las colas son lo primero que se aparta).
5. **PSD** (Welch): debe ser **plana** dentro del ancho de banda del filtro RX — eso es
   "blanco" (dentro de la banda de interés).

**Conclusión esperada:** I y Q ≈ gaussianas independientes de media ~0 e igual varianza, PSD
plana en banda ⇒ el modelo $Z\sim\mathcal N(0,\sigma^2 I)$ (por dimensión) y la definición de
$N(t)$ de la Unidad 3 describen bien el receptor real.

---

### 4. Del dato al modelo (cerrando el círculo)

Este resultado es lo que **autoriza** todo el edificio teórico:

- gaussiano ⇒ las verosimilitudes de la Unidad 2 son las correctas ⇒ MAP/ML con umbrales y
  mínima distancia;
- blanco ⇒ el Lema de proyecciones (Unidad 3) da componentes iid ⇒ el matched filter es óptimo;
- la varianza medida juega el rol de $N_0/2$ en todas las fórmulas de $P_e$.

---

### 5. Para el pizarrón

1. Capturar sólo ruido: TX mudo (−89 dB, ceros), LO separados, RX manual 70 dB, buffer grande.
2. Pipeline: series I/Q → media/varianza → histogramas + pdf → Q–Q → PSD (Welch).
3. Esperado: gaussiano (histograma y Q–Q), blanco en banda (PSD plana), I ⊥ Q.
4. Consecuencia: valida MAP/ML, matched filter y las fórmulas con $N_0/2$.
