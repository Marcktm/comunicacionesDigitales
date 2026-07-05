"""Tests de core/receiver.py y core/waveforms.py."""
import numpy as np
import pytest

from core.receiver import (
    awgn,
    correlator,
    energy,
    gram_schmidt,
    inner_product,
    matched_filter_output,
)
from core.waveforms import fsk, rect_ppm, sinc_ppm, spread_spectrum


# --- receiver ---------------------------------------------------------------- #
def test_inner_product_y_energia():
    n, dt = 1000, 1e-3
    t = np.arange(n) * dt
    a = np.ones(n)                       # ‖a‖² = 1 (duración 1)
    assert energy(a, dt) == pytest.approx(1.0)
    b = np.sin(2 * np.pi * 5 * t)        # ⟨1, sen⟩ ≈ 0 sobre períodos enteros
    assert abs(inner_product(a, b, dt).real) < 1e-6


def test_gram_schmidt_ortonormaliza():
    n, dt = 400, 1.0 / 400
    s1 = np.ones(n)
    s2 = np.linspace(0, 1, n, endpoint=False)  # no ortogonal a s1
    basis = gram_schmidt([s1, s2], dt)
    assert len(basis) == 2
    assert energy(basis[0], dt) == pytest.approx(1.0)
    assert energy(basis[1], dt) == pytest.approx(1.0)
    assert abs(inner_product(basis[0], basis[1], dt).real) < 1e-9


def test_gram_schmidt_descarta_dependiente():
    n, dt = 200, 1.0 / 200
    s = np.ones(n)
    basis = gram_schmidt([s, 2.0 * s], dt)
    assert len(basis) == 1


def test_matched_filter_en_T_igual_correlador():
    # y(T) del filtro apareado == ∫ r·b (correlador); rect → triángulo pico = a.
    n, T = 500, 1.0
    dt = T / n
    psi = np.ones(n) / np.sqrt(T)        # ‖ψ‖²=1
    a = 1.7
    r = a * psi
    y = matched_filter_output(r, psi, dt)
    yT = y[n - 1]                        # índice de t=T en convolución 'full'
    assert yT == pytest.approx(a, rel=1e-6)
    assert yT == pytest.approx(correlator(r, psi, dt).real, rel=1e-9)
    assert np.max(y) == pytest.approx(yT, rel=1e-6)   # el pico está en t=T


def test_awgn_media_y_varianza():
    x = awgn(np.zeros(200_000), sigma=0.7, seed=0)
    assert np.mean(x) == pytest.approx(0.0, abs=0.01)
    assert np.std(x) == pytest.approx(0.7, abs=0.01)


# --- waveforms (Ejemplo 3.7: energía E y ortogonalidad) ---------------------- #
@pytest.mark.parametrize("gen", [rect_ppm, fsk, spread_spectrum])
def test_waveforms_energia_y_ortogonalidad(gen):
    E = 2.0
    t, w0, w1 = gen(E=E)
    dt = t[1] - t[0]
    assert energy(w0, dt) == pytest.approx(E, rel=1e-2)
    assert energy(w1, dt) == pytest.approx(E, rel=1e-2)
    assert abs(inner_product(w0, w1, dt).real) < 1e-2 * E


def test_sinc_ppm_aprox_ortogonal():
    # truncado ⇒ tolerancia más laxa
    t, w0, w1 = sinc_ppm(E=1.0)
    dt = t[1] - t[0]
    assert energy(w0, dt) == pytest.approx(1.0, rel=5e-2)
    assert abs(inner_product(w0, w1, dt).real) < 5e-2


def test_spread_spectrum_chips_potencia_de_dos():
    with pytest.raises(ValueError):
        spread_spectrum(chips=6)
