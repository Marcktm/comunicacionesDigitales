"""Vectores aleatorios: media, correlación, covarianza y elipse de confianza (DSP puro).

Base teórica: Roy Yates (vectores aleatorios) y Bixio §2.10 (apéndice de vectores
gaussianos). Funciones numéricas puras (sin Streamlit ni SDR). Convención de muestras:
``samples`` tiene forma ``(N, d)`` (N realizaciones de un vector de dimensión d).
"""
from __future__ import annotations

import numpy as np


def cov_2d(sigma1, sigma2, rho):
    """Matriz de covarianza 2×2 a partir de σ₁, σ₂ y el coeficiente de correlación ρ."""
    c = rho * sigma1 * sigma2
    return np.array([[sigma1**2, c], [c, sigma2**2]], dtype=float)


def sample_gaussian(mean, cov, n, seed=None):
    """n muestras de un vector gaussiano N(mean, cov). Devuelve forma (n, d).

    Usa el método de Cholesky (cov debe ser definida positiva; en la UI |ρ|<1).
    """
    rng = np.random.default_rng(seed)
    # errstate: matmul emite warnings espurios con Accelerate BLAS (macOS ARM)
    with np.errstate(all="ignore"):
        return rng.multivariate_normal(
            np.asarray(mean, dtype=float), np.asarray(cov, dtype=float),
            size=n, method="cholesky",
        )


def mean_vector(samples):
    """Vector de medias m_X = E[X] (estimado por promedio de muestras)."""
    return np.asarray(samples, dtype=float).mean(axis=0)


def correlation_matrix(samples):
    """Matriz de correlación (autocorrelación) R_X = E[X Xᵀ] (sin centrar), MLE (÷N)."""
    X = np.asarray(samples, dtype=float)
    return (X.T @ X) / X.shape[0]


def covariance_matrix(samples):
    """Matriz de covarianza K_X = E[(X−m)(X−m)ᵀ], MLE (÷N).

    Con esta normalización vale exactamente la identidad R_X = K_X + m mᵀ.
    """
    X = np.asarray(samples, dtype=float)
    Xc = X - X.mean(axis=0, keepdims=True)
    return (Xc.T @ Xc) / X.shape[0]


def correlation_coeffs(cov):
    """Matriz de coeficientes de correlación ρ_ij = K_ij / (σ_i σ_j)."""
    cov = np.asarray(cov, dtype=float)
    d = np.sqrt(np.diag(cov))
    return cov / np.outer(d, d)


def linear_transform(mean, cov, A, b=None):
    """Estadística de Y = A X + b:  m_Y = A m_X + b,  K_Y = A K_X Aᵀ."""
    A = np.asarray(A, dtype=float)
    mean = np.asarray(mean, dtype=float)
    cov = np.asarray(cov, dtype=float)
    m_y = A @ mean + (0.0 if b is None else np.asarray(b, dtype=float))
    k_y = A @ cov @ A.T
    return m_y, k_y


def ellipse_points(mean, cov, n_sigma=2.0, n=200):
    """Puntos (x, y) de la elipse de confianza a ``n_sigma`` desvíos (autovectores de K)."""
    mean = np.asarray(mean, dtype=float)
    cov = np.asarray(cov, dtype=float)
    vals, vecs = np.linalg.eigh(cov)
    t = np.linspace(0.0, 2.0 * np.pi, n)
    circle = np.stack([np.cos(t), np.sin(t)])            # 2 × n
    axes = vecs @ np.diag(np.sqrt(np.maximum(vals, 0.0)) * n_sigma)
    pts = axes @ circle + mean[:, None]
    return pts[0], pts[1]
