"""Tests de la capa core/ (función Q, umbral MAP/ML, Pe, Monte Carlo)."""
import numpy as np
import pytest

from core.decision import likelihood_ratio, map_decision, monte_carlo_pe, nearest_index
from core.distributions import (
    binary_error_probs,
    map_threshold,
    pe_binary_equiprobable,
    q_bounds,
    q_function,
)


# --- función Q -------------------------------------------------------------- #
def test_q_valores_conocidos():
    assert q_function(0.0) == pytest.approx(0.5)
    assert q_function(50.0) == pytest.approx(0.0, abs=1e-12)
    # Q(1) ≈ 0.158655
    assert q_function(1.0) == pytest.approx(0.15865525, abs=1e-6)


def test_q_simetria():
    # Q(-x) + Q(x) = 1
    for x in [0.2, 1.0, 2.5]:
        assert q_function(-x) + q_function(x) == pytest.approx(1.0, abs=1e-12)


def test_q_cotas_sandwich():
    # lower < Q(alpha) < upper para alpha > 0
    for a in [0.5, 1.0, 2.0, 3.0]:
        lo, hi = q_bounds(a)
        q = q_function(a)
        assert lo < q < hi


# --- umbral MAP/ML ---------------------------------------------------------- #
def test_umbral_equiprobable_es_punto_medio():
    theta = map_threshold(-1.0, 1.0, sigma=1.0, p0=0.5, p1=0.5)
    assert theta == pytest.approx(0.0)


def test_umbral_formula():
    c0, c1, sigma, p0 = -1.0, 2.0, 0.7, 0.3
    p1 = 1 - p0
    esperado = (sigma**2 / (c1 - c0)) * np.log(p0 / p1) + (c0 + c1) / 2.0
    assert map_threshold(c0, c1, sigma, p0, p1) == pytest.approx(esperado)


def test_umbral_c0_igual_c1_falla():
    with pytest.raises(ValueError):
        map_threshold(1.0, 1.0, sigma=1.0)


def test_razon_verosimilitud_cruza_en_theta():
    # En el umbral MAP, Λ(θ) = η = P0/P1.
    c0, c1, sigma, p0 = -1.0, 1.5, 0.9, 0.4
    p1 = 1 - p0
    theta = map_threshold(c0, c1, sigma, p0, p1)
    assert likelihood_ratio(theta, c0, c1, sigma) == pytest.approx(p0 / p1)


# --- probabilidad de error -------------------------------------------------- #
def test_pe_equiprobable_es_Q_d_sobre_2sigma():
    c0, c1, sigma = -1.0, 1.0, 0.8
    res = binary_error_probs(c0, c1, sigma, 0.5, 0.5)
    esperado = pe_binary_equiprobable(c0, c1, sigma)
    assert res.pe == pytest.approx(esperado)
    assert res.pe == pytest.approx(q_function(abs(c1 - c0) / (2 * sigma)))


def test_pe_orientacion_c1_menor_que_c0():
    # El resultado no debe depender del orden de c0, c1.
    a = binary_error_probs(-1.0, 1.0, 1.0, 0.5, 0.5).pe
    b = binary_error_probs(1.0, -1.0, 1.0, 0.5, 0.5).pe
    assert a == pytest.approx(b)


# --- decisión y Monte Carlo ------------------------------------------------- #
def test_map_decision_umbral():
    c0, c1, sigma = -1.0, 1.0, 1.0
    y = np.array([-2.0, -0.01, 0.0, 0.01, 2.0])
    d = map_decision(y, c0, c1, sigma, 0.5, 0.5)
    assert list(d) == [0, 0, 1, 1, 1]  # decide 1 cuando y >= θ=0


def test_nearest_index_recta():
    # constelación en la recta: {-1, 1}
    idx = nearest_index(np.array([-2.0, -0.1, 0.1, 2.0]), np.array([-1.0, 1.0]))
    assert list(idx) == [0, 0, 1, 1]


def test_nearest_index_plano_complejo():
    import numpy as np
    const = np.array([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j])  # 4-QAM (a=1)
    # un punto cerca de c2 = -1-1j
    assert int(nearest_index(np.array([-0.9 - 0.8j]), const)[0]) == 2


def test_monte_carlo_se_acerca_a_teorico():
    c0, c1, sigma = -1.0, 1.0, 1.0
    teorico = pe_binary_equiprobable(c0, c1, sigma)  # ≈ Q(1) ≈ 0.1587
    estimado = monte_carlo_pe(c0, c1, sigma, p0=0.5, n=300_000, seed=1)
    assert estimado == pytest.approx(teorico, abs=0.01)
