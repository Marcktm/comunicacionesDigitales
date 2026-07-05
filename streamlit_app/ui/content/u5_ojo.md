## ISI y diagrama de ojo

> **Referencias.** Bixio Rimoldi §5.6 (**págs. 172–174**; los pulsos superpuestos y la suma son
> las **Figs. 5.7/5.8, págs. 171–172** y los diagramas de ojo la **Fig. 5.9, pág. 173**).
> Notebooks del **Lab 4** del repo. La herramienta visual para diagnosticar la calidad del enlace.

---

### 1. Cuando todo funciona: se recupera el símbolo exacto

Si $\psi$ es ortonormal a sus traslados, su autosimilitud cumple $R_\psi(iT)=\delta_{i0}$.
La señal sin ruido $w(t)=\sum_i s_i\psi(t-iT)$, pasada por el matched filter $\psi^*(-t)$,
produce

$$
y(t)=\sum_i s_i\,R_\psi(t-iT)
\;\Longrightarrow\;
y(jT)=\sum_i s_i\,R_\psi\big((j-i)T\big)=s_j .
$$

**En el instante de muestreo correcto sobrevive sólo el símbolo buscado**: todos los vecinos se
anulan porque $R_\psi$ vale 0 en los múltiplos de $T$.

---

### 2. Interferencia entre símbolos (ISI): las dos causas

Si $R_\psi(iT)\ne\delta_{i0}$, definiendo $l_i=R_\psi(iT)$:

$$
y(jT)=\sum_i s_i\,l_{j-i}
$$

— la muestra depende de **varios** símbolos: eso es **ISI**. Dos causas:

1. **El pulso dejó de ser ortogonal a sus traslados** — típicamente por **truncar** el RRC
   demasiado corto (span chico con β chico).
2. **Error de sincronismo**: muestrear en $jT+\Delta$ da $l_i=R_\psi(iT+\Delta)$, no nulo aunque
   el pulso sea perfecto.

---

### 3. El diagrama de ojo: construcción

Se toma la salida del matched filter **antes de muestrear** y se superponen trazas de duración
$2T$ centradas en cada símbolo: graficar $y(t-iT)$, $t\in[-T,T]$, para muchos $i$, todo encima.
Es exactamente lo que hace un **osciloscopio** disparado con el reloj de símbolo — por eso es la
herramienta estándar de banco de mediciones.

**Lectura:**

- **Sin ISI**: en $t=0$ todas las trazas pasan por los valores del alfabeto (±1 en BPSK): el
  "ojo" está **abierto**.
- **Con ISI**: las trazas pasan por muchos valores intermedios: el ojo se **cierra
  verticalmente**.
- La **apertura horizontal** mide la tolerancia al **jitter**: cuánto podés equivocarte en el
  instante de muestreo sin confundir símbolos. β grande ⇒ pulso que decae rápido ⇒ ojo más
  abierto horizontalmente.
- El **ruido** engrosa las trazas y cierra el ojo verticalmente (se ve bajando la SNR con
  TxAtten en el Lab 4).

---

### 4. El experimento del Lab 4 (lo que hace el Bonus SDR)

Cadena real sobre el Pluto: bits → BPSK → sobremuestreo (sps) → **filtro RRC** en TX →
Pluto (`loopback` 1 digital / 2 RF / 0 antena, `tx_hardwaregain` para variar SNR) → **RRC de
nuevo** en RX (matched filter) → diagrama de ojo. Qué mirar:

| Experimento | Efecto esperado en el ojo |
|---|---|
| bajar β (1 → 0.25) | menos margen horizontal (más sensible al sincronismo) |
| truncar el span (12T → 4T) con β chico | aparece ISI: cierre **vertical** |
| loopback 1 → 2 → 0 | del ojo "de libro" al canal real (ruido, acoples) |
| subir la atenuación TX (−30 → −70 dB) | baja la SNR: trazas gruesas, ojo cerrado |

---

### 5. Para el pizarrón

1. Ortonormal ⇒ $R_\psi(iT)=\delta_{i0}$ ⇒ $y(jT)=s_j$ (demostrarlo con la suma).
2. ISI: $y(jT)=\sum_i s_i l_{j-i}$; causas = truncamiento y error de muestreo $\Delta$.
3. Ojo = superposición de trazas de $2T$; apertura vertical ↔ ISI/ruido, horizontal ↔ jitter.
4. Lab 4: β, span, loopback y TxAtten mueven el ojo de forma predecible.
