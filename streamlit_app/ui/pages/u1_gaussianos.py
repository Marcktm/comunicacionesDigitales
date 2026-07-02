"""Unidad 1 — Vectores aleatorios gaussianos (densidad bivariada)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import multivariate_normal

from core.random_vectors import cov_2d
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def render() -> None:
    st.title("Vectores aleatorios gaussianos")
    st.caption("Unidad 1 · Roy Yates + Bixio §2.10")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u1_gaussianos.md")

    with tg:
        st.subheader("Densidad gaussiana bivariada (curvas de nivel)")
        st.caption(
            "ρ = 0 ⇒ curvas alineadas a los ejes (componentes independientes). "
            "ρ ≠ 0 ⇒ elipses inclinadas. El caso esférico σ₁=σ₂, ρ=0 da círculos: N(0, σ²I)."
        )
        c = st.columns(3)
        s1 = c[0].slider("σ₁", 0.3, 3.0, 1.0, 0.1)
        s2 = c[1].slider("σ₂", 0.3, 3.0, 1.0, 0.1)
        rho = c[2].slider("ρ (correlación)", -0.95, 0.95, 0.0, 0.05)

        K = cov_2d(s1, s2, rho)
        r = 3.0 * max(s1, s2)
        axis = np.linspace(-r, r, 160)
        Xg, Yg = np.meshgrid(axis, axis)
        Z = multivariate_normal(mean=[0.0, 0.0], cov=K).pdf(np.dstack([Xg, Yg]))

        fig = go.Figure(go.Contour(x=axis, y=axis, z=Z, colorscale="Blues", showscale=False))
        fig.update_layout(
            xaxis_title="x₁", yaxis_title="x₂",
            yaxis=dict(scaleanchor="x", scaleratio=1),
            margin=dict(l=10, r=10, t=20, b=10), height=470,
        )
        render_plotly(fig)

    with ts:
        st.info(
            "El ruido del canal AWGN es un vector gaussiano N(0, σ²Iₙ) (esférico). Su simetría "
            "explica la regla de **mínima distancia** (Unidad 2) y la suficiencia de la "
            "**proyección** sobre el espacio de señales (Unidad 3, filtro apareado)."
        )
