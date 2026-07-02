"""Distribuciones, función Q y decisión binaria en canal AWGN escalar.

Base teórica: Bixio Rimoldi cap. 2 (§2.2–2.4) y apunte Cabrera §1.3–1.11.
Todas las funciones son numéricas puras (sin Streamlit ni SDR).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import special


# --------------------------------------------------------------------------- #
# Función Q
# --------------------------------------------------------------------------- #
def q_function(x):
    r"""Q(x) = Pr{Z >= x} con Z ~ N(0,1).

    Se calcula como Q(x) = 1/2 * erfc(x/sqrt(2)), equivalente a
    ``scipy.stats.norm.sf(x)`` pero sin la dependencia de ``stats``.
    """
    x = np.asarray(x, dtype=float)
    return 0.5 * special.erfc(x / np.sqrt(2.0))


def q_inv(p):
    """Inversa de la función Q."""
    p = np.asarray(p, dtype=float)
    return np.sqrt(2.0) * special.erfcinv(2.0 * p)


def q_bounds(alpha):
    r"""Cotas inferior y superior de Q(alpha) para alpha > 0 (Bixio, propiedad 4).

    .. math::
        \frac{1}{\sqrt{2\pi}\,\alpha} e^{-\alpha^2/2}
        \frac{\alpha^2}{1+\alpha^2}
        < Q(\alpha) <
        \frac{1}{\sqrt{2\pi}\,\alpha} e^{-\alpha^2/2}.
    """
    alpha = np.asarray(alpha, dtype=float)
    coef = np.exp(-(alpha**2) / 2.0) / (np.sqrt(2.0 * np.pi) * alpha)
    lower = coef * (alpha**2 / (1.0 + alpha**2))
    upper = coef
    return lower, upper


def q_bound_simple(alpha):
    r"""Cota superior simple: Q(alpha) <= 1/2 * exp(-alpha^2/2), alpha >= 0."""
    alpha = np.asarray(alpha, dtype=float)
    return 0.5 * np.exp(-(alpha**2) / 2.0)


# --------------------------------------------------------------------------- #
# Densidades
# --------------------------------------------------------------------------- #
def gaussian_pdf(y, mean=0.0, var=1.0):
    """f(y) para Y ~ N(mean, var)."""
    y = np.asarray(y, dtype=float)
    return np.exp(-((y - mean) ** 2) / (2.0 * var)) / np.sqrt(2.0 * np.pi * var)


def laplacian_pdf(y, mu=0.0, b=1.0):
    """f(y) para una v.a. Laplaciana de media ``mu`` y escala ``b``."""
    y = np.asarray(y, dtype=float)
    return np.exp(-np.abs(y - mu) / b) / (2.0 * b)


# --------------------------------------------------------------------------- #
# Decisión binaria escalar en canal AWGN
# --------------------------------------------------------------------------- #
def map_threshold(c0, c1, sigma, p0=0.5, p1=0.5):
    r"""Umbral óptimo θ de la regla MAP para observación escalar (canal AWGN).

    .. math::
        \theta = \frac{\sigma^2}{c_1 - c_0}\ln\eta + \frac{c_0 + c_1}{2},
        \qquad \eta = \frac{P_H(0)}{P_H(1)}.

    Si P_H(0) = P_H(1) entonces ln η = 0 y θ es el punto medio (c0+c1)/2.
    """
    if c0 == c1:
        raise ValueError("c0 y c1 deben ser distintos")
    if sigma <= 0:
        raise ValueError("sigma debe ser > 0")
    eta = p0 / p1
    return (sigma**2 / (c1 - c0)) * np.log(eta) + (c0 + c1) / 2.0


@dataclass
class BinaryErrors:
    theta: float
    pe0: float  # Pr{decidir 1 | H=0}
    pe1: float  # Pr{decidir 0 | H=1}
    pe: float   # Pe = P0*pe0 + P1*pe1


def binary_error_probs(c0, c1, sigma, p0=0.5, p1=0.5) -> BinaryErrors:
    r"""Probabilidad de error condicional y total (Bixio §2.4.1).

    .. math::
        P_e(0) = Q\!\left(\frac{\theta-c_0}{\sigma}\right),\quad
        P_e(1) = Q\!\left(\frac{c_1-\theta}{\sigma}\right),\quad
        P_e = P_H(0)P_e(0) + P_H(1)P_e(1).
    """
    theta = map_threshold(c0, c1, sigma, p0, p1)
    if c1 >= c0:
        pe0 = float(q_function((theta - c0) / sigma))
        pe1 = float(q_function((c1 - theta) / sigma))
    else:
        pe0 = float(q_function((c0 - theta) / sigma))
        pe1 = float(q_function((theta - c1) / sigma))
    pe = p0 * pe0 + p1 * pe1
    return BinaryErrors(theta=float(theta), pe0=pe0, pe1=pe1, pe=float(pe))


def pe_binary_equiprobable(c0, c1, sigma):
    r"""Caso equiprobable: Pe = Q(d/2σ) con d = |c1 - c0|."""
    d = abs(c1 - c0)
    return float(q_function(d / (2.0 * sigma)))
