"""Tests de core/random_vectors.py (covarianza, correlación, elipse, transf. lineal)."""
import numpy as np
import pytest

from core.random_vectors import (
    correlation_coeffs,
    correlation_matrix,
    covariance_matrix,
    cov_2d,
    ellipse_points,
    linear_transform,
    mean_vector,
    sample_gaussian,
)


def test_cov_2d_estructura():
    K = cov_2d(2.0, 3.0, 0.5)
    assert K[0, 0] == pytest.approx(4.0)
    assert K[1, 1] == pytest.approx(9.0)
    assert K[0, 1] == pytest.approx(0.5 * 2.0 * 3.0)
    assert K[0, 1] == K[1, 0]


def test_correlation_coeffs_recupera_rho():
    K = cov_2d(1.5, 2.5, -0.4)
    C = correlation_coeffs(K)
    assert C[0, 0] == pytest.approx(1.0)
    assert C[1, 1] == pytest.approx(1.0)
    assert C[0, 1] == pytest.approx(-0.4)


def test_identidad_R_igual_K_mas_mmT():
    # Con normalización ÷N, vale R = K + m mᵀ de forma exacta.
    rng = np.random.default_rng(0)
    X = rng.normal(size=(500, 3)) + np.array([1.0, -2.0, 0.5])
    R = correlation_matrix(X)
    K = covariance_matrix(X)
    m = mean_vector(X)
    assert np.allclose(R, K + np.outer(m, m))


def test_covarianza_muestral_recupera_cov():
    K = cov_2d(1.0, 2.0, 0.6)
    X = sample_gaussian([0.0, 0.0], K, n=200_000, seed=1)
    assert np.allclose(covariance_matrix(X), K, atol=0.05)


def test_linear_transform():
    K = cov_2d(1.0, 1.0, 0.0)   # identidad
    A = np.array([[2.0, 0.0], [0.0, 3.0]])
    m_y, k_y = linear_transform([1.0, -1.0], K, A, b=[0.5, 0.5])
    assert np.allclose(m_y, [2.5, -2.5])
    assert np.allclose(k_y, np.array([[4.0, 0.0], [0.0, 9.0]]))


def test_ellipse_identidad_es_circulo():
    # Con K = I y n_sigma = 2, todos los puntos están a distancia 2 del centro.
    x, y = ellipse_points([0.0, 0.0], np.eye(2), n_sigma=2.0, n=64)
    r = np.hypot(x, y)
    assert np.allclose(r, 2.0, atol=1e-6)
