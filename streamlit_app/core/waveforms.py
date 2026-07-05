"""Conjuntos de señales del Ejemplo 3.7 del Bixio (pág. 103 y ss.).

Cuatro elecciones de W = {w0(t), w1(t)} que lucen distintas pero comparten el
mismo codebook  c0 = (√E, 0)ᵀ,  c1 = (0, √E)ᵀ  (señales ortogonales de energía E)
⇒ misma probabilidad de error  Pe = Q(√(E/N0)).

Cada generador devuelve (t, w0, w1) muestreados con ``n`` puntos.
"""
from __future__ import annotations

import numpy as np


def _grid(t_max, n):
    t = np.linspace(0.0, t_max, n, endpoint=False)
    dt = t[1] - t[0]
    return t, dt


def rect_ppm(E=1.0, T=1.0, n=2000):
    """Elección 1 — PPM rectangular: pulso en [0,T] vs pulso en [T,2T]."""
    t, dt = _grid(2.0 * T, n)
    a = np.sqrt(E / T)
    w0 = np.where(t < T, a, 0.0)
    w1 = np.where(t >= T, a, 0.0)
    return t, w0, w1


def fsk(E=1.0, T=1.0, k=3, l=4, n=2000):
    """Elección 2 — FSK ortogonal: senos de frecuencias k/2T y l/2T en [0,T], k≠l."""
    t, dt = _grid(T, n)
    a = np.sqrt(2.0 * E / T)
    w0 = a * np.sin(np.pi * k * t / T)
    w1 = a * np.sin(np.pi * l * t / T)
    return t, w0, w1


def sinc_ppm(E=1.0, T=1.0, n=4000, span=8.0):
    """Elección 3 — PPM sinc: sinc(t/T) vs sinc((t−T)/T) (soporte truncado a ±span·T)."""
    t = np.linspace(-span * T, span * T, n)
    a = np.sqrt(E / T)
    w0 = a * np.sinc(t / T)
    w1 = a * np.sinc((t - T) / T)
    return t, w0, w1


def spread_spectrum(E=1.0, T=1.0, chips=8, n=2000, seed=0):
    """Elección 4 — espectro ensanchado: secuencias de chips ±1 ortogonales.

    Usa filas de una matriz de Hadamard (ortogonales por construcción) como
    secuencias de signos, con ``chips`` chips por símbolo en [0,T].
    """
    if chips & (chips - 1):
        raise ValueError("chips debe ser potencia de 2 (Hadamard)")
    H = np.array([[1.0]])
    while H.shape[0] < chips:
        H = np.block([[H, H], [H, -H]])
    s0, s1 = H[1], H[2]              # dos filas ortogonales (≠ fila de todos unos)
    t, dt = _grid(T, n)
    idx = np.minimum((t / T * chips).astype(int), chips - 1)
    a = np.sqrt(E / T)
    return t, a * s0[idx], a * s1[idx]


WAVEFORM_CHOICES = {
    "Elección 1 — PPM rectangular": rect_ppm,
    "Elección 2 — FSK ortogonal": fsk,
    "Elección 3 — PPM sinc": sinc_ppm,
    "Elección 4 — Espectro ensanchado": spread_spectrum,
}
