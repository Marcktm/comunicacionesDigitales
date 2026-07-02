"""Tests de core/modulation.py (constelaciones, Pe, helpers de señal)."""
import numpy as np
import pytest

from core.distributions import q_function
from core.modulation import (
    avg_min_neighbors,
    bpsk_symbols,
    complex_exp,
    min_distance,
    nearest_neighbor_pe,
    pam_constellation,
    pam_symbol_error_prob,
    psk_constellation,
    qam4_constellation,
    qam4_symbol_error_prob,
    qam_square_constellation,
    qpsk_gen,
    square_wave,
    union_bound_pe,
)


# --- helpers de señal ------------------------------------------------------- #
def test_complex_exp_magnitud_unitaria():
    x = complex_exp(1024, Fc=250e3, Fs=2e6)
    assert np.allclose(np.abs(x), 1.0)
    assert x[0] == pytest.approx(1.0 + 0j)


def test_complex_exp_nyquist_falla():
    with pytest.raises(ValueError):
        complex_exp(100, Fc=2e6, Fs=1e6)


def test_bpsk_mapea_antipodal():
    assert list(bpsk_symbols([0, 1, 0, 1])) == [-1, 1, -1, 1]


def test_qpsk_gen_forma_y_energia():
    sym, ups = qpsk_gen(num_symbols=100, sps=4, seed=0)
    assert sym.shape == (100,)
    assert ups.shape == (400,)
    assert np.allclose(np.abs(sym), 1.0)  # energía unitaria por símbolo


def test_square_wave_valores():
    w = square_wave(20, period=4, amp=2.0)
    assert set(np.unique(w)) <= {-2.0, 2.0}


# --- constelaciones y Pe ---------------------------------------------------- #
def test_pam_constellation_espaciado_y_centrado():
    pts = pam_constellation(6, d=2.0)
    assert len(pts) == 6
    assert np.allclose(np.diff(pts), 2.0)          # separación d
    assert pts.mean() == pytest.approx(0.0)        # centrada en 0


def test_pam_pe_6pam_es_cinco_tercios_Q():
    d, sigma = 2.0, 0.7
    esperado = (5.0 / 3.0) * q_function(d / (2 * sigma))
    assert pam_symbol_error_prob(6, d, sigma) == pytest.approx(esperado)


def test_pam_pe_binario_coincide_con_Q():
    # 2-PAM equivale a antipodal: Pe = Q(d/2σ)
    d, sigma = 2.0, 1.0
    assert pam_symbol_error_prob(2, d, sigma) == pytest.approx(q_function(d / (2 * sigma)))


def test_qam4_constellation_distancia_minima():
    c = qam4_constellation(d=2.0)
    assert len(c) == 4
    # distancia entre vecinos horizontales/verticales = d
    assert abs(c[0] - c[1]) == pytest.approx(2.0)


def test_qam4_pe_formula():
    d, sigma = 2.0, 0.6
    q = q_function(d / (2 * sigma))
    assert qam4_symbol_error_prob(d, sigma) == pytest.approx(2 * q - q**2)


def test_psk_constellation_radio():
    c = psk_constellation(8, radius=1.5)
    assert len(c) == 8
    assert np.allclose(np.abs(c), 1.5)


def test_qam_square_distancia_minima():
    assert min_distance(qam_square_constellation(16, d=2.0)) == pytest.approx(2.0)
    with pytest.raises(ValueError):
        qam_square_constellation(8)  # 8 no es cuadrado perfecto


def test_avg_min_neighbors_qam4():
    nmin, dmin = avg_min_neighbors(qam4_constellation(2.0))
    assert dmin == pytest.approx(2.0)
    assert nmin == pytest.approx(2.0)  # cada punto tiene 2 vecinos a d_min


def test_union_bound_es_cota_superior():
    # La cota de la unión no puede ser menor que la Pe exacta (4-QAM).
    const = qam4_constellation(2.0)
    sigma = 0.5
    d = 2.0
    exacta = qam4_symbol_error_prob(d, sigma)
    assert union_bound_pe(const, sigma) >= exacta - 1e-12
    assert nearest_neighbor_pe(const, sigma) >= exacta - 1e-12
