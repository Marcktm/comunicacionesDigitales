"""Simulador BPSK + AWGN extremo a extremo (el del notebook del Parcial 2).

Cadena: fuente binaria → encoder antipodal → waveform former (pulso rectangular
de Ns muestras, energía 1) → canal AWGN → filtro apareado → muestreo en los
instantes de decisión → detector ML (signo) → conteo de errores.

Con pulso de energía unitaria y matched filter igual, la muestra de decisión es
s ± n con n ~ N(0, σ²)  ⇒  Pe teórica = Q(1/σ).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .distributions import q_function
from .modulation import bpsk_symbols, random_bits


@dataclass
class BpskChainResult:
    bits: np.ndarray
    symbols: np.ndarray
    tx_wave: np.ndarray
    rx_wave: np.ndarray
    mf_out: np.ndarray
    decision_samples: np.ndarray
    bits_hat: np.ndarray
    pe_est: float
    pe_theory: float


def simulate_bpsk_chain(num_bits=2**12, ns=16, sigma=0.5, seed=None) -> BpskChainResult:
    """Corre la cadena completa y devuelve las señales de cada etapa."""
    rng = np.random.default_rng(seed)
    bits = random_bits(num_bits, seed=rng.integers(1 << 31))
    symbols = bpsk_symbols(bits).astype(float)

    pulse = np.ones(ns) / np.sqrt(ns)                 # energía 1
    tx = np.repeat(symbols, ns) / np.sqrt(ns)         # Σ s_j ψ(t−jT) discreto
    rx = tx + rng.normal(0.0, sigma, size=tx.shape)   # canal AWGN

    mf = np.convolve(rx, pulse[::-1])                 # filtro apareado
    idx = ns - 1 + ns * np.arange(num_bits)           # instantes de decisión
    z = mf[idx]

    bits_hat = (z >= 0).astype(int)
    pe_est = float(np.mean(bits_hat != bits))
    pe_theory = float(q_function(1.0 / sigma))
    return BpskChainResult(bits, symbols, tx, rx, mf, z, bits_hat, pe_est, pe_theory)
