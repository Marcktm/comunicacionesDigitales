"""Reglas de decisión y verificación Monte Carlo (canal AWGN escalar).

Base teórica: Bixio Rimoldi §2.2–2.4. Funciones numéricas puras.
"""
from __future__ import annotations

import numpy as np

from .distributions import map_threshold


def likelihood_ratio(y, c0, c1, sigma):
    r"""Razón de verosimilitud Λ(y) = f(y|1)/f(y|0) para el canal AWGN escalar.

    .. math::
        \Lambda(y) = \exp\!\left\{ \frac{y(c_1-c_0)}{\sigma^2}
        + \frac{c_0^2 - c_1^2}{2\sigma^2} \right\}.
    """
    y = np.asarray(y, dtype=float)
    return np.exp(y * (c1 - c0) / sigma**2 + (c0**2 - c1**2) / (2.0 * sigma**2))


def map_decision(y, c0, c1, sigma, p0=0.5, p1=0.5):
    """Decisión MAP: devuelve 0 o 1 comparando ``y`` con el umbral θ."""
    theta = map_threshold(c0, c1, sigma, p0, p1)
    y = np.asarray(y, dtype=float)
    if c1 >= c0:
        return (y >= theta).astype(int)
    return (y <= theta).astype(int)


def nearest_index(y, constellation):
    """Índice del punto de la constelación más cercano a cada ``y`` (regla ML AWGN).

    ``y`` y ``constellation`` pueden ser complejos (plano) o reales (recta). Devuelve,
    para cada elemento de ``y``, el índice ``i`` que minimiza ``|y − c_i|`` (regiones
    de Voronoi). Base: en canal AWGN la regla ML es de mínima distancia.
    """
    y = np.asarray(y)
    c = np.asarray(constellation)
    dist = np.abs(y[..., None] - c.reshape((1,) * y.ndim + (-1,)))
    return np.argmin(dist, axis=-1)


def monte_carlo_pe(c0, c1, sigma, p0=0.5, n=100_000, seed=None):
    r"""Estima Pe por simulación Monte Carlo del canal Y = c_H + Z, Z~N(0,σ²).

    Genera H con P(H=0)=p0, transmite c_H, agrega ruido gaussiano, decide con
    la regla MAP y cuenta los errores. Devuelve la fracción de errores.
    """
    rng = np.random.default_rng(seed)
    h = (rng.random(n) >= p0).astype(int)  # H=1 con prob 1-p0
    means = np.where(h == 0, c0, c1)
    y = means + rng.normal(0.0, sigma, size=n)
    hhat = map_decision(y, c0, c1, sigma, p0, 1.0 - p0)
    return float(np.mean(hhat != h))
