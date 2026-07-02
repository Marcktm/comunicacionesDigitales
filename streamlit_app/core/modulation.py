"""Modulación, constelaciones y generación de señales (DSP puro).

Constelaciones m-PAM y 4-QAM con sus probabilidades de error (Bixio §2.4.3), más
helpers de laboratorio reutilizados por las páginas del SDR y las katas de práctica
(exponencial compleja, QPSK, onda cuadrada, símbolos aleatorios).
"""
from __future__ import annotations

import numpy as np

from .distributions import q_function


# --------------------------------------------------------------------------- #
# Helpers de generación de señales (de los notebooks del laboratorio)
# --------------------------------------------------------------------------- #
def complex_exp(N, Fc, Fs):
    r"""Exponencial compleja de N muestras: x[n] = e^{j 2π Fc n / Fs}.

    Requiere Fs ≥ 2·Fc (Nyquist). Es la señal de prueba de `How To Config SDR`.
    """
    if Fs < 2 * Fc:
        raise ValueError("Fs debe ser al menos 2·Fc (Nyquist)")
    n = np.arange(N)
    return np.exp(1j * 2.0 * np.pi * Fc * n / Fs)


def random_bits(n, seed=None):
    """n bits equiprobables ∈ {0,1}."""
    rng = np.random.default_rng(seed)
    return rng.integers(0, 2, size=n)


def bpsk_symbols(bits):
    """Mapeo antipodal BPSK: 0 → −1, 1 → +1."""
    return 2 * np.asarray(bits) - 1


def random_symbols(alphabet, n, seed=None):
    """n símbolos tomados uniformemente de ``alphabet``."""
    rng = np.random.default_rng(seed)
    alphabet = np.asarray(alphabet)
    return alphabet[rng.integers(0, len(alphabet), size=n)]


def qpsk_gen(num_symbols, sps, seed=None):
    """Genera símbolos QPSK (energía unitaria) y su versión sobremuestreada (sps).

    Devuelve ``(symbols, upsampled)`` donde ``upsampled`` repite cada símbolo sps veces.
    """
    rng = np.random.default_rng(seed)
    mapper = np.array([1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]) / np.sqrt(2.0)
    idx = rng.integers(0, 4, size=num_symbols)
    symbols = mapper[idx]
    return symbols, np.repeat(symbols, sps)


def square_wave(n_samples, period, duty=0.5, amp=1.0):
    """Onda cuadrada de amplitud ±amp, ``period`` muestras por ciclo."""
    n = np.arange(n_samples)
    phase = (n % period) / float(period)
    return np.where(phase < duty, amp, -amp).astype(float)


# --------------------------------------------------------------------------- #
# Constelaciones y probabilidad de error (Bixio §2.4.3)
# --------------------------------------------------------------------------- #
def pam_constellation(m, d=2.0):
    """m puntos PAM equiespaciados, centrados en 0, con separación ``d``."""
    return (np.arange(m) - (m - 1) / 2.0) * d


def pam_symbol_error_prob(m, d, sigma):
    r"""Probabilidad de error de símbolo m-PAM: Pe = (2 − 2/m) Q(d/2σ).

    Los 2 puntos extremos tienen un vecino (error a un lado); los m−2 internos
    tienen dos vecinos (error a ambos lados). Promediando: (2 − 2/m) Q(d/2σ).
    """
    return (2.0 - 2.0 / m) * q_function(d / (2.0 * sigma))


def qam4_constellation(d=2.0):
    """4-QAM: cuatro puntos en los vértices de un cuadrado de lado ``d``."""
    a = d / 2.0
    return np.array([a + 1j * a, -a + 1j * a, -a - 1j * a, a - 1j * a])


def qam4_symbol_error_prob(d, sigma):
    r"""Probabilidad de error de símbolo 4-QAM: Pe = 2Q(d/2σ) − Q(d/2σ)².

    Se decide bien si ambas componentes del ruido no cruzan su umbral:
    Pc = [1 − Q(d/2σ)]²  ⇒  Pe = 1 − Pc = 2Q(d/2σ) − Q(d/2σ)².
    """
    q = q_function(d / (2.0 * sigma))
    return 2.0 * q - q**2


def psk_constellation(m, radius=1.0):
    """m-PSK: m puntos equiespaciados en un círculo de radio ``radius``."""
    k = np.arange(m)
    return radius * np.exp(1j * 2.0 * np.pi * k / m)


def qam_square_constellation(m, d=2.0):
    """m-QAM cuadrada (m = 4, 16, 64, …) en grilla con separación ``d``."""
    side = int(round(np.sqrt(m)))
    if side * side != m:
        raise ValueError("m debe ser un cuadrado perfecto (4, 16, 64, …)")
    levels = (np.arange(side) - (side - 1) / 2.0) * d
    re, im = np.meshgrid(levels, levels)
    return (re + 1j * im).ravel()


def min_distance(constellation):
    """Distancia mínima entre pares de puntos de la constelación."""
    c = np.asarray(constellation)
    d = np.abs(c[:, None] - c[None, :])
    np.fill_diagonal(d, np.inf)
    return float(d.min())


def avg_min_neighbors(constellation):
    """Promedio de vecinos a distancia mínima (N_min) y la distancia mínima d_min."""
    c = np.asarray(constellation)
    d = np.abs(c[:, None] - c[None, :])
    np.fill_diagonal(d, np.inf)
    dmin = d.min()
    counts = (np.abs(d - dmin) < 1e-9 * max(1.0, dmin)).sum(axis=1)
    return float(counts.mean()), float(dmin)


def union_bound_pe(constellation, sigma):
    r"""Cota de la unión de Pe (promedio sobre símbolos equiprobables):
    Pe ≤ (1/m) Σᵢ Σ_{j≠i} Q(‖cᵢ−cⱼ‖ / 2σ)."""
    c = np.asarray(constellation)
    d = np.abs(c[:, None] - c[None, :])
    np.fill_diagonal(d, np.inf)   # Q(∞)=0, así el propio símbolo no aporta
    return float(q_function(d / (2.0 * sigma)).sum(axis=1).mean())


def nearest_neighbor_pe(constellation, sigma):
    """Aproximación de vecinos más cercanos: Pe ≈ N_min · Q(d_min/2σ)."""
    nmin, dmin = avg_min_neighbors(constellation)
    return float(nmin * q_function(dmin / (2.0 * sigma)))
