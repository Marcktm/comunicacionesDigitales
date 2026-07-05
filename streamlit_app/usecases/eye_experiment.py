"""Lab 4 real: transmitir BPSK con pulso RRC por el Pluto y capturar para el ojo.

Reproduce el flujo del laboratorio: bits → símbolos ±1 → sobremuestreo → filtro
RRC (TX) → Pluto (loopback digital/RF/antena) → filtro RRC (RX, apareado) → señal
lista para el diagrama de ojo.
"""
from __future__ import annotations

import numpy as np

from core.modulation import bpsk_symbols, random_bits
from core.pulses import rrc_taps
from sdr.pluto import PlutoSDR


def build_tx_signal(num_bits=2**12, sps=8, span=12, beta=0.5, seed=None):
    """Construye la señal BPSK conformada con RRC (y devuelve también los taps)."""
    bits = random_bits(num_bits, seed=seed)
    symbols = bpsk_symbols(bits).astype(float)
    ups = np.zeros(num_bits * sps)
    ups[::sps] = symbols                       # impulsos cada T
    taps = rrc_taps(sps, span, beta)
    tx = np.convolve(ups, taps)
    tx = tx / np.max(np.abs(tx))               # normalizar antes del DAC
    return tx, taps


def run_sdr_eye_case(name: str, beta=0.5, span=12, loopback=1, tx_atten=-30,
                     sample_rate=4e6, lo_freq=2400e6, sps=8, num_bits=2**12,
                     seed=0):
    """Ejecuta el caso del Lab 4 en el Pluto y devuelve la señal filtrada RX.

    Devuelve dict con `mf` (salida del filtro apareado RX, real e imaginaria),
    `sps` y los parámetros, listo para `core.eye.eye_traces`.
    """
    tx, taps = build_tx_signal(num_bits=num_bits, sps=sps, span=span,
                               beta=beta, seed=seed)
    with PlutoSDR(name) as sdr:
        sdr.configure(
            sample_rate=int(sample_rate), loopback=int(loopback),
            tx_lo=int(lo_freq), rx_lo=int(lo_freq),
            tx_rf_bandwidth=int(sample_rate), rx_rf_bandwidth=int(sample_rate),
            tx_hardwaregain=int(tx_atten), rx_buffer_size=2**18,
        )
        sdr.transmit(tx.astype(complex))
        rx = sdr.receive()
    mf = np.convolve(np.asarray(rx), taps)      # filtro apareado en RX
    return {"mf": mf, "sps": sps, "beta": beta, "span": span,
            "loopback": loopback, "tx_atten": tx_atten}
