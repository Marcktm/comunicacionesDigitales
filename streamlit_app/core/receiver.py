"""Operaciones del receptor en tiempo continuo (discretizado): producto interno,
Gram-Schmidt, correlador y filtro apareado. Base: Bixio cap. 3 (§3.3–3.5).

Convención: las señales son arrays muestreados con paso ``dt``; las integrales se
aproximan con la regla del rectángulo  ∫f ≈ Σ f[k]·dt.
"""
from __future__ import annotations

import numpy as np


def inner_product(a, b, dt):
    """⟨a,b⟩ = ∫ a(t)·b*(t) dt  (aprox. por regla del rectángulo)."""
    return complex(np.sum(np.asarray(a) * np.conj(np.asarray(b))) * dt)


def energy(a, dt):
    """‖a‖² = ∫ |a(t)|² dt."""
    return float(np.sum(np.abs(np.asarray(a)) ** 2) * dt)


def gram_schmidt(signals, dt, tol=1e-12):
    """Base ortonormal del espacio generado por ``signals`` (lista de arrays).

    Procedimiento de Gram-Schmidt con el producto interno de funciones. Descarta
    los vectores linealmente dependientes (norma residual < tol).
    """
    basis = []
    for s in signals:
        v = np.asarray(s, dtype=float).copy()
        for phi in basis:
            v = v - np.real(inner_product(v, phi, dt)) * phi
        norm = np.sqrt(energy(v, dt))
        if norm > tol:
            basis.append(v / norm)
    return basis


def correlator(r, b, dt):
    """Correlador: ∫ r(t)·b*(t) dt (multiplicar e integrar). Fig. 3.6a del libro."""
    return inner_product(r, b, dt)


def matched_filter_output(r, b, dt):
    """Salida completa y(t) del filtro apareado h(t)=b*(T−t) alimentado con r(t).

    y(t) = ∫ r(α)·b*(T+α−t) dα. Devuelve el array y(t) (misma grilla temporal que
    la convolución 'full'); su muestra en t=T coincide con el correlador:
    y(T) = ∫ r·b*. Fig. 3.6b del libro.
    """
    r = np.asarray(r, dtype=float)
    b = np.asarray(b, dtype=float)
    return np.convolve(r, b[::-1]) * dt


def awgn(signal, sigma, seed=None):
    """Suma ruido gaussiano blanco discreto N(0, σ²) por muestra."""
    rng = np.random.default_rng(seed)
    s = np.asarray(signal, dtype=float)
    return s + rng.normal(0.0, sigma, size=s.shape)
