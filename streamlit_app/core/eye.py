"""Diagrama de ojo: segmentación de la señal en trazas superpuestas.

La función devuelve datos (las páginas los dibujan con Matplotlib, que maneja
mejor el overlay de muchas trazas con transparencia).
"""
from __future__ import annotations

import numpy as np


def eye_traces(x, sps, span_symbols=2, offset=0, max_traces=200):
    """Corta ``x`` en trazas de ``span_symbols``·``sps`` muestras (solapadas cada
    símbolo) y las devuelve como matriz (n_trazas, L). ``offset`` corre el punto
    de arranque (en muestras) para alinear el ojo."""
    x = np.asarray(x)
    L = span_symbols * sps
    starts = np.arange(offset, len(x) - L, sps)
    if len(starts) > max_traces:
        starts = starts[:max_traces]
    return np.stack([x[s:s + L] for s in starts]) if len(starts) else np.empty((0, L))
