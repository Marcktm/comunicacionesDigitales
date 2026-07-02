"""Wrapper del ADALM-Pluto (pyadi-iio) con conexión, configuración y cierre seguro.

Reproduce el flujo de los notebooks (`How To Config SDR`, `laboratorio4_codex`):
conectar -> configurar TX/RX -> transmitir -> recibir -> cierre seguro (bajar
potencia, mover rx_lo, destruir buffer). ``adi`` se importa de forma perezosa.
"""
from __future__ import annotations

import numpy as np

from .registry import uri

DEFAULTS = dict(
    sample_rate=int(4e6),
    tx_lo=int(2400e6),
    rx_lo=int(2400e6),
    tx_rf_bandwidth=int(4e6),
    rx_rf_bandwidth=int(4e6),
    tx_hardwaregain=-30,          # atenuación TX (dB)
    gain_control_mode="slow_attack",
    rx_buffer_size=2**18,
    loopback=0,                    # 0=antena, 1=digital, 2=RF
)


class PlutoSDR:
    """Envuelve ``adi.Pluto`` para uso desde los casos de uso de la app."""

    def __init__(self, name: str):
        self.name = name
        self.uri = uri(name)
        self._sdr = None

    # -- ciclo de vida ----------------------------------------------------- #
    def connect(self) -> "PlutoSDR":
        import adi  # perezoso: la app corre sin pyadi-iio instalado

        self._sdr = adi.Pluto(self.uri)
        return self

    def configure(self, **kw) -> "PlutoSDR":
        cfg = {**DEFAULTS, **kw}
        s = self._sdr
        s.sample_rate = int(cfg["sample_rate"])
        s.loopback = int(cfg["loopback"])
        # TX
        s.tx_lo = int(cfg["tx_lo"])
        s.tx_rf_bandwidth = int(cfg["tx_rf_bandwidth"])
        s.tx_hardwaregain_chan0 = cfg["tx_hardwaregain"]
        s.tx_cyclic_buffer = True
        # RX
        s.rx_lo = int(cfg["rx_lo"])
        s.gain_control_mode_chan0 = cfg["gain_control_mode"]
        s.rx_rf_bandwidth = int(cfg["rx_rf_bandwidth"])
        s.rx_cyclic_buffer = False
        s.rx_buffer_size = int(cfg["rx_buffer_size"])
        return self

    # -- transmisión / recepción ------------------------------------------ #
    def transmit(self, signal, scale: int = 2**14) -> None:
        self._sdr.tx_destroy_buffer()
        self._sdr.tx(np.asarray(signal) * scale)

    def receive(self, flush: int = 10, scale: int = 2**14):
        for _ in range(flush):      # descartar buffers transitorios
            self._sdr.rx()
        return self._sdr.rx() / scale

    def close(self) -> None:
        """Cierre seguro: baja potencia, mueve rx_lo y libera el dispositivo."""
        if self._sdr is None:
            return
        try:
            self._sdr.tx_destroy_buffer()
            self._sdr.tx_hardwaregain_chan0 = -70
            self._sdr.rx_lo = int(2400e6)
            self._sdr.tx(np.zeros(1024))
        except Exception:
            pass
        finally:
            del self._sdr
            self._sdr = None

    # -- context manager --------------------------------------------------- #
    def __enter__(self) -> "PlutoSDR":
        return self.connect()

    def __exit__(self, *exc) -> None:
        self.close()
