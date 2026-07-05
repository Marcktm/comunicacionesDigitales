"""Experimentos reales sobre el ADALM-Pluto (requieren VPN + pyadi-iio).

Cada función conecta al SDR elegido, configura, ejecuta y cierra de forma segura
(context manager de PlutoSDR). Los errores suben a la UI, que muestra el mensaje.
"""
from __future__ import annotations

import numpy as np

from core.modulation import complex_exp
from sdr.pluto import PlutoSDR


def tx_rx_tone(name: str, sample_rate=2.0e6, lo_freq=915e6, fc_frac=1.0 / 8.0,
               tx_atten=-30, n_samples=2**16):
    """Lab 1: transmite un tono (exponencial compleja en Fc = fs·fc_frac) y lo recibe.

    Devuelve dict con la señal recibida y los parámetros usados.
    """
    fc = sample_rate * fc_frac
    tone = complex_exp(n_samples, Fc=fc, Fs=sample_rate)
    with PlutoSDR(name) as sdr:
        sdr.configure(
            sample_rate=int(sample_rate), tx_lo=int(lo_freq), rx_lo=int(lo_freq),
            tx_rf_bandwidth=int(sample_rate), rx_rf_bandwidth=int(sample_rate),
            tx_hardwaregain=tx_atten, rx_buffer_size=n_samples, loopback=0,
        )
        sdr.transmit(tone)
        rx = sdr.receive()
    return {"rx": np.asarray(rx), "fs": sample_rate, "fc": fc, "lo": lo_freq}


def capture_noise(name: str, sample_rate=2.0e6, rx_lo=915e6, tx_lo=2400e6,
                  rx_gain=70, n_samples=2**18):
    """Lab 2: captura ruido del receptor con el TX silencioso (atenuación máxima)
    y el TX sintonizado lejos del RX para no autointerferir.
    """
    with PlutoSDR(name) as sdr:
        sdr.configure(
            sample_rate=int(sample_rate), rx_lo=int(rx_lo), tx_lo=int(tx_lo),
            tx_rf_bandwidth=int(sample_rate), rx_rf_bandwidth=int(sample_rate),
            tx_hardwaregain=-89, gain_control_mode="manual",
            rx_buffer_size=n_samples, loopback=0,
        )
        sdr._sdr.rx_hardwaregain_chan0 = rx_gain  # ganancia manual máxima
        sdr.transmit(np.zeros(1024))              # buffer TX en silencio
        rx = sdr.receive()
    return np.asarray(rx)
