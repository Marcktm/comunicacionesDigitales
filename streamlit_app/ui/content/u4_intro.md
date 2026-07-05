## ¿Qué es un SDR? Arquitectura del ADALM-Pluto

> **Referencias.** Apunte Cabrera, Unidad 4 (SDR); notebook *How To Config SDR* (Lab 1);
> `instalacion-drivers-sdr.md` del repo; Bixio §5.2 (**págs. 160–163**) para el fundamento
> teórico (el teorema de muestreo hace posible el SDR).

---

### 1. La idea

Una **radio definida por software** (SDR) es un sistema de RF cuyas etapas de transmisión y
recepción son **reconfigurables por software**: el mismo hardware sirve para distintos sistemas y
protocolos, cambiando sólo el programa. El fundamento es el **teorema de muestreo** (Unidad 5):
cualquier señal limitada en banda queda descrita por una **secuencia de números**, así que

- el **encoder/decoder** (la inteligencia del estándar) vive en **software**, y
- el hardware genérico sólo convierte números ↔ formas de onda (el *waveform former* y el
  *n-tuple former* de la Unidad 3, hechos silicio).

---

### 2. El ADALM-Pluto: dos chips

**FrontEnd — AD9363** (transceptor de conversión directa): hace la modulación/demodulación y el
acondicionamiento en banda base y RF. Del lado digital tiene filtros FIR, decimación/
interpolación y control de ganancia; del lado analógico, filtros, amplificadores, atenuadores y
mezcladores de RF, con los DAC/ADC integrados. Parámetros configurables: frecuencia de portadora,
ancho de banda, tasa de muestreo, ganancias, filtros.

**BackEnd — Zynq Z-7010** (SoC): una **FPGA** + un **ARM Cortex-A9** con **Linux embebido**. En
el kernel corre el **Linux IIO Subsystem**, que expone los parámetros del AD9363 (osciladores,
ancho de banda, AGC, …) como dispositivos estándar. La FPGA trae además un **filtro decimador
÷8** que extiende la tasa mínima de ~521 kSPS a ~65 kSPS. Al tener Linux, el Pluto funciona
*stand-alone* y se administra por red.

**Rangos útiles** (los vas a ver como límites de los parámetros):
portadora **325 MHz – 3.8 GHz** · muestreo **521 kSPS – 61.44 MSPS** ·
ancho de banda RF **200 kHz – 20 MHz**.

**Antenas:** conectores SMA; las provistas (JCG401) están especificadas para 824–894 y
1710–2170 MHz pero operan en un rango más amplio — la antena también **filtra** (selectividad
suave), por eso capta frecuencias adyacentes.

---

### 3. Los tres modos de loopback

El Pluto puede realimentar TX→RX en tres puntos distintos (ver diagrama):

| `sdr.loopback` | Camino | Para qué sirve |
|---|---|---|
| **0** | por **antena** (aire) | el caso real: canal inalámbrico, atenuación, interferencia |
| **1** | **digital** (bypass del RF) | probar la cadena DSP sin canal: lo que entra al DAC vuelve por el ADC |
| **2** | **RF interno** (sin aire) | probar la cadena RF completa con canal controlado |

Es la herramienta de depuración central de los laboratorios: si algo falla, se prueba primero en
loopback 1 (¿está bien mi DSP?), luego 2 (¿está bien mi RF?), luego 0 (¿qué hace el canal?).

---

### 4. Cómo se accede en el laboratorio

Los 5 Pluto están conectados por Ethernet a la red del laboratorio, con IPs fijas
`192.168.1.31` … `192.168.1.35`. Se accede por **VPN** (Cisco AnyConnect a `200.16.19.5:443`) y
la cadena de software es:

```
Python (tu código) → pyadi-iio → libiio → [VPN] → iiod (en el Pluto)
```

`iiod` es el daemon que corre en el Linux del Pluto y ejecuta las órdenes. Verificaciones útiles:
`ping 192.168.1.31` y `iio_info -u ip:192.168.1.31` (lista los canales del AD9363).

---

### 5. Para el pizarrón

1. SDR = TX/RX reconfigurables por software; fundamento: **teorema de muestreo** (señal ↔ números).
2. Pluto = **AD9363** (RF + DAC/ADC + filtros) + **Zynq** (FPGA ÷8 + ARM con Linux/IIO).
3. Rangos: 325 MHz–3.8 GHz, 521 kSPS–61.44 MSPS, BW 200 kHz–20 MHz.
4. Loopback 0/1/2 = aire / digital / RF interno (orden de depuración: 1 → 2 → 0).
5. Acceso: VPN → `ip:192.168.1.3x` → iiod (stack pyadi-iio/libiio).
