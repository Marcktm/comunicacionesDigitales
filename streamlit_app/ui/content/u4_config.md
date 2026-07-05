## Lab 1 — Configurar el SDR y transmitir un tono

> **Referencias.** Notebook *How To Config SDR* (Lab 1 del repo) y
> `instalacion-drivers-sdr.md`. Primer contacto con el hardware: transmitir una **exponencial
> compleja** (un tono) y verla llegar al receptor.

---

### 1. Objetivo del laboratorio

Cerrar el lazo completo por primera vez: **conectar → configurar → transmitir → recibir →
graficar**. La señal de prueba es la exponencial compleja

$$
x[n]=e^{\,j2\pi F_c n/F_s},\qquad F_c=\frac{F_s}{8},
$$

porque su espectro es **una sola raya** en $F_c$: si al recibir aparece un pico en $F_c$, todo el
lazo (DAC → RF → aire/loopback → RF → ADC) funciona.

**¿Por qué compleja?** El Pluto trabaja con muestras **I/Q** (banda base compleja): la parte real
modula el coseno de la portadora y la imaginaria el seno. Un tono complejo en $F_c$ aparece en el
aire en $f_{LO}+F_c$.

---

### 2. Pasos (con la app o con el notebook)

1. **VPN**: Cisco AnyConnect a `200.16.19.5:443` (sin VPN no hay ruta a los `192.168.1.3x`).
2. **Elegir SDR** disponible (selector global de la app; algunos pueden estar ocupados).
3. **Configurar**: $F_s=2$ MHz, portadora 915 MHz (TX = RX), BW = $F_s$, atenuación TX −30 dB,
   buffer RX 2¹⁶, `tx_cyclic_buffer=True`.
4. **Transmitir** el tono escalado a 2¹⁴ y **recibir** (descartando transitorios).
5. **Graficar**: componentes I y Q en el tiempo (dos senoidales en cuadratura) y la **PSD**
   (método de Welch): un pico en $F_c=F_s/8=250$ kHz.

---

### 3. Qué esperar y qué puede fallar

- **Se ve el pico pero movido**: los osciladores de TX y RX de dos Pluto distintos no son
  idénticos (offset de portadora); dentro del mismo Pluto es despreciable.
- **Amplitud distinta entre capturas**: el AGC (`slow_attack`) reajusta la ganancia; para medir
  potencias usá `manual`.
- **No se ve nada**: ¿VPN activa? ¿el SDR responde (`ping`, `iio_info`)? ¿TX y RX en la misma
  portadora? ¿atenuación TX demasiado alta?
- **Espuria en 0 Hz**: offset de DC del receptor de conversión directa; es normal verla pequeña.

---

### 4. Para el pizarrón

1. Señal de prueba: $x[n]=e^{j2\pi F_cn/F_s}$, espectro = una raya en $F_c$.
2. I/Q = banda base compleja; en el aire queda en $f_{LO}+F_c$.
3. Flujo: VPN → conectar → configurar ($F_s$, LO, BW, ganancias, buffer) → TX cíclico 2¹⁴ →
   descartar transitorios → RX /2¹⁴ → tiempo + PSD.
4. Diagnóstico: pico presente = lazo OK; sin pico = revisar VPN/LO/atenuación.
