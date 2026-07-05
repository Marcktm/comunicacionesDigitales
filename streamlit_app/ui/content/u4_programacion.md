## Cómo programar el SDR (línea por línea)

> **Referencias.** Notebooks *How To Config SDR* (Lab 1) y `laboratorio4_codex` del repo;
> documentación de pyadi-iio. Esta página explica **qué hace cada línea** del código que usan
> todos los laboratorios; al final tenés la **práctica de código** para fijarlo.

---

### 1. Conectar

```python
import adi
sdr = adi.Pluto("ip:192.168.1.32")   # URI = "ip:" + la IP del SDR elegido
```

`adi.Pluto(uri)` abre la conexión con el `iiod` del dispositivo (por la VPN). Si la IP no
responde, acá salta el error — por eso el selector global de la app chequea disponibilidad antes.

---

### 2. Configurar — qué hace cada parámetro

```python
sdr.sample_rate = int(2e6)                    # tasa de muestreo (ambas cadenas)
sdr.loopback = 0                              # 0 antena · 1 digital · 2 RF interno

# --- cadena TX ---
sdr.tx_lo = int(915e6)                        # oscilador local TX (portadora)
sdr.tx_rf_bandwidth = int(2e6)                # filtro analógico TX
sdr.tx_hardwaregain_chan0 = -30               # "ganancia" TX = ATENUACIÓN en dB
sdr.tx_cyclic_buffer = True                   # repetir el buffer TX para siempre

# --- cadena RX ---
sdr.rx_lo = int(915e6)                        # oscilador local RX
sdr.rx_rf_bandwidth = int(2e6)                # filtro analógico RX
sdr.gain_control_mode_chan0 = "slow_attack"   # AGC: manual / slow_attack / fast_attack
sdr.rx_buffer_size = 2**16                    # muestras por llamada a rx()
```

| Parámetro | Rango | Qué controla |
|---|---|---|
| `sample_rate` | 521 kSPS – 61.44 MSPS | frecuencia de muestreo de DAC/ADC |
| `tx_lo` / `rx_lo` | 325 MHz – 3.8 GHz | portadora (mezcladores de subida/bajada) |
| `tx_hardwaregain_chan0` | −90 … 0 dB | atenuación de salida (0 = máxima potencia) |
| `rx_hardwaregain_chan0` | 0 … 90 dB | ganancia RX (sólo si el AGC está en `manual`) |
| `gain_control_mode_chan0` | manual / slow_attack / fast_attack | cómo ajusta el AGC la ganancia RX |
| `tx_rf_bandwidth` / `rx_rf_bandwidth` | 200 kHz – 20 MHz | filtros analógicos anti-imagen/anti-alias |
| `rx_buffer_size` | hasta 2²⁸ | tamaño del bloque que devuelve `rx()` |
| `tx_cyclic_buffer` | True/False | TX una vez o en loop continuo |

**Detalles que muerden:** las frecuencias van como **enteros** (`int(915e6)`); TX y RX en la
**misma** portadora para el loopback/enlace; con AGC automático la amplitud RX **no** es
comparable entre capturas (usá `manual` si vas a medir potencias).

---

### 3. Transmitir y recibir

```python
# TX: escalar al DAC de 12 bits (rango útil ±2¹⁴) y enviar
sdr.tx_destroy_buffer()          # limpiar cualquier buffer TX anterior
sdr.tx(senal * 2**14)            # con tx_cyclic_buffer=True queda repitiéndose

# RX: descartar transitorios y capturar
for _ in range(10):
    sdr.rx()                     # el AGC y los filtros tardan en asentarse
rx = sdr.rx() / 2**14            # capturar y volver a escala ±1
```

Por qué cada cosa: el **escalado 2¹⁴** usa el rango del DAC sin saturar; `tx_destroy_buffer()`
evita mezclar la señal nueva con una vieja; **descartar ~10 buffers** deja pasar los transitorios
del AGC; el `/2**14` a la vuelta normaliza para el procesamiento.

---

### 4. Cierre seguro (siempre, aunque falle algo)

```python
try:
    ...  # experimento
finally:
    sdr.tx_destroy_buffer()               # parar el TX cíclico
    sdr.tx_hardwaregain_chan0 = -89       # atenuar al mínimo
    sdr.tx(np.zeros(1024))                # transmitir silencio
    del sdr                               # liberar el dispositivo para otros
```

El SDR es **compartido**: si te vas sin limpiar, tu TX cíclico queda emitiendo e interfiere al
siguiente. El wrapper `sdr/pluto.py` de esta app hace exactamente esto en su `close()`.

---

### 5. Helpers de los laboratorios (viven en `core/`)

- `complex_exp(N, Fc, Fs)` — tono complejo $e^{j2\pi F_c n/F_s}$ (exige $F_s\ge 2F_c$): la señal
  de prueba del Lab 1.
- `qpsk_gen(num_symbols, sps)` — símbolos QPSK de energía unitaria + versión sobremuestreada.
- `square_wave(n, period)` — onda cuadrada para ver el efecto de los filtros.
- `random_bits` / `bpsk_symbols` — la fuente y el encoder del simulador.
- filtros **RC/RRC** — en la Unidad 5 (Lab 4).

---

### 6. Para el pizarrón (el ciclo completo)

1. `adi.Pluto("ip:...")` → conexión por VPN al iiod.
2. Config: `sample_rate`, `lo` (enteros), ganancias (TX = atenuación), BW, buffer, loopback.
3. TX: `tx_destroy_buffer()` → `tx(x·2¹⁴)` (cíclico).
4. RX: descartar ~10 buffers → `rx()/2¹⁴`.
5. Cierre: destruir buffer, atenuar, silencio, `del sdr`.

*Ahora sí: practicá con las katas de abajo.* 🥋
