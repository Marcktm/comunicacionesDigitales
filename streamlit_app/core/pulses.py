"""Pulsos y espectros del cap. 5: sinc, coseno realzado (RC), raíz de coseno
realzado (RRC), criterio de Nyquist (espectro plegado) y PSD de trenes de pulsos.

Implementaciones propias de las fórmulas estándar. El pulso RRC trata los puntos
singulares t=0 y t=±T/(4β) por límite (L'Hôpital).
"""
from __future__ import annotations

import numpy as np


# --------------------------------------------------------------------------- #
# Pulsos y espectros
# --------------------------------------------------------------------------- #
def sinc_pulse(t, T=1.0):
    """ψ(t) = (1/√T)·sinc(t/T) — el pulso de ancho de banda mínimo (norma 1)."""
    t = np.asarray(t, dtype=float)
    return np.sinc(t / T) / np.sqrt(T)


def raised_cosine_spectrum(f, T=1.0, beta=0.5):
    """|ψF(f)|² del coseno realzado: plano hasta (1−β)/2T, transición coseno,
    cero desde (1+β)/2T. Cumple el criterio de Nyquist con parámetro T."""
    f = np.abs(np.asarray(f, dtype=float))
    f1 = (1.0 - beta) / (2.0 * T)
    f2 = (1.0 + beta) / (2.0 * T)
    out = np.zeros_like(f)
    out[f <= f1] = T
    if beta > 0:
        mid = (f > f1) & (f < f2)
        out[mid] = (T / 2.0) * (1.0 + np.cos(np.pi * T / beta * (f[mid] - f1)))
    return out


def rrc_spectrum(f, T=1.0, beta=0.5):
    """ψF(f) de la raíz de coseno realzado = √(coseno realzado)."""
    return np.sqrt(raised_cosine_spectrum(f, T, beta))


def rrc_pulse(t, T=1.0, beta=0.5):
    """Respuesta al impulso de la raíz de coseno realzado (norma 1).

    Fórmula estándar con dos puntos singulares resueltos por límite:
    t = 0 y t = ±T/(4β) (indeterminación 0/0, L'Hôpital).
    Para beta = 0 se reduce al pulso sinc.
    """
    t = np.asarray(t, dtype=float)
    if beta == 0.0:
        return sinc_pulse(t, T)

    x = t / T
    out = np.empty_like(x)

    # puntos regulares
    den = 1.0 - (4.0 * beta * x) ** 2
    regular = np.abs(den) > 1e-10
    xr = x[regular]
    num = (np.cos((1.0 + beta) * np.pi * xr)
           + (1.0 - beta) * np.pi / (4.0 * beta) * np.sinc((1.0 - beta) * xr))
    out[regular] = (4.0 * beta / (np.pi * np.sqrt(T))) * num / den[regular]

    # t = ±T/(4β): límite por L'Hôpital
    lim = (beta / (np.pi * np.sqrt(2.0 * T))) * (
        (np.pi + 2.0) * np.sin(np.pi / (4.0 * beta))
        + (np.pi - 2.0) * np.cos(np.pi / (4.0 * beta))
    )
    out[~regular] = lim

    # t = 0 (den=1, regular, pero verificamos el valor exacto por claridad)
    zero = np.abs(x) < 1e-12
    out[zero] = (1.0 - beta + 4.0 * beta / np.pi) / np.sqrt(T)
    return out


def rrc_taps(sps, span, beta):
    """Coeficientes del filtro RRC discreto: ``span`` símbolos, ``sps`` muestras
    por símbolo, normalizados a energía unitaria (Σ taps² = 1)."""
    n = span * sps
    t = (np.arange(n + 1) - n / 2.0) / float(sps)   # en unidades de T
    taps = rrc_pulse(t, T=1.0, beta=beta)
    return taps / np.sqrt(np.sum(taps**2))


# --------------------------------------------------------------------------- #
# Criterio de Nyquist (espectro plegado)
# --------------------------------------------------------------------------- #
def folded_spectrum(spectrum_fn, f, T=1.0, k_range=8, **kw):
    """Σ_k |ψF(f − k/T)|² — el 'espectro plegado'. Si el pulso cumple el criterio
    de Nyquist, la suma es la constante T para todo f."""
    f = np.asarray(f, dtype=float)
    total = np.zeros_like(f)
    for k in range(-k_range, k_range + 1):
        total += spectrum_fn(f - k / T, T=T, **kw)
    return total


# --------------------------------------------------------------------------- #
# PSD de un tren de pulsos  X(t) = Σ X_i ξ(t − iT − Θ)
# --------------------------------------------------------------------------- #
def rect_pulse_spectrum(f, T=1.0):
    """|ξF(f)|² del rectángulo de duración T y energía 1: T·sinc²(fT)."""
    f = np.asarray(f, dtype=float)
    return T * np.sinc(f * T) ** 2


def pulse_train_psd(f, pulse_spectrum, K, T=1.0):
    """S_X(f) = (|ξF(f)|²/T) · Σ_k K[k]·e^{−j2πkfT}  (resultado real).

    ``pulse_spectrum`` = |ξF(f)|² evaluado en f; ``K`` = dict {k: K_X[k]} con la
    autocovarianza de los símbolos (K simétrica: incluir k y −k).
    """
    f = np.asarray(f, dtype=float)
    s = np.zeros_like(f, dtype=complex)
    for k, val in K.items():
        s += val * np.exp(-1j * 2.0 * np.pi * k * f * T)
    return np.real(np.asarray(pulse_spectrum) / T * s)
