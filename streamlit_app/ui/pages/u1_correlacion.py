"""Unidad 1 — Vector de valor esperado y matriz de correlación."""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from core.random_vectors import cov_2d, ellipse_points, sample_gaussian
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def render() -> None:
    st.title("Vector de valor esperado y matriz de correlación")
    st.caption("Unidad 1 · Roy Yates")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u1_correlacion.md")

    with tg:
        st.subheader("Nube de puntos y elipse de covarianza (ℝ²)")
        st.caption(
            "El coeficiente ρ inclina y achata la nube; la elipse (2σ) son los autovectores de K."
        )
        c = st.columns(3)
        s1 = c[0].slider("σ₁", 0.3, 3.0, 1.0, 0.1)
        s2 = c[1].slider("σ₂", 0.3, 3.0, 1.5, 0.1)
        rho = c[2].slider("ρ (correlación)", -0.95, 0.95, 0.6, 0.05)

        K = cov_2d(s1, s2, rho)
        X = sample_gaussian([0.0, 0.0], K, 1500, seed=0)
        ex, ey = ellipse_points([0.0, 0.0], K, n_sigma=2.0)

        fig = go.Figure()
        fig.add_scatter(x=X[:, 0], y=X[:, 1], mode="markers",
                        marker=dict(size=4, color="#1f77b4", opacity=0.35), name="muestras")
        fig.add_scatter(x=ex, y=ey, mode="lines",
                        line=dict(color="#d62728", width=3), name="elipse 2σ")
        fig.update_layout(
            xaxis_title="X₁", yaxis_title="X₂",
            yaxis=dict(scaleanchor="x", scaleratio=1),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=30, b=10), height=470,
        )
        render_plotly(fig)
        cov = rho * s1 * s2
        st.latex(
            rf"K_X=\begin{{bmatrix}} {s1**2:.2f} & {cov:.2f} \\ {cov:.2f} & {s2**2:.2f} \end{{bmatrix}}"
            rf",\qquad \rho=\frac{{K_{{12}}}}{{\sigma_1\sigma_2}}={rho:.2f}"
        )

    with ts:
        st.info(
            "El caso vectorial modela múltiples antenas / slots / frecuencias. La regla "
            "K_Y = A K_X Aᵀ es la que se usa para **blanquear** el ruido (Unidad 3)."
        )
