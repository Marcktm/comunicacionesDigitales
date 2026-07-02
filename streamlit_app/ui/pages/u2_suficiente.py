"""Unidad 2 — Estadística suficiente (Fisher-Neyman, reducción de dimensión)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.distributions import q_function
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _pe_vs_n_figure(a, sigma, nmax=30):
    n = np.arange(1, nmax + 1)
    pe = q_function(np.sqrt(n) * a / sigma)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=pe, mode="lines+markers",
                             name="Pe = Q(√n · a/σ)"))
    fig.update_layout(
        xaxis_title="n (observaciones promediadas)", yaxis_title="Pe",
        yaxis_type="log", margin=dict(l=10, r=10, t=30, b=10), height=380,
        showlegend=False,
    )
    return fig


def _montecarlo_mean_decision(a, sigma, n, trials=200_000, seed=0):
    """Simula n obs iid y decide por el signo del promedio (estadística suficiente)."""
    rng = np.random.default_rng(seed)
    h = rng.integers(0, 2, size=trials)          # 0 -> -a, 1 -> +a
    c = np.where(h == 0, -a, a)
    noise = rng.normal(0.0, sigma, size=(trials, n))
    ybar = c[:, None] + noise
    ybar = ybar.mean(axis=1)
    hhat = (ybar >= 0).astype(int)
    return float(np.mean(hhat != h))


def render() -> None:
    st.title("Estadística suficiente")
    st.caption("Unidad 2 · Bixio §2.5")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u2_suficiente.md")

    with tg:
        st.subheader("n observaciones iid → una sola estadística suficiente (el promedio)")
        c = st.columns(3)
        a = c[0].slider("amplitud a (señal ±a)", 0.1, 2.0, 0.5, 0.05)
        sigma = c[1].slider("σ (ruido)", 0.2, 3.0, 1.0, 0.1)
        n = c[2].slider("n (para Monte Carlo)", 1, 30, 8, 1)

        render_plotly(_pe_vs_n_figure(a, sigma))
        st.caption("Promediar n copias reduce el ruido efectivo por √n: Pe = Q(√n·a/σ).")

        st.divider()
        st.subheader("Verificación: decidir por el promedio ≡ ML sobre el vector completo")
        if st.button("Simular", width="stretch"):
            with st.spinner("Simulando…"):
                pe_mc = _montecarlo_mean_decision(a, sigma, n)
            teorico = float(q_function(np.sqrt(n) * a / sigma))
            d = st.columns(2)
            d[0].metric("Pₑ teórico  Q(√n·a/σ)", f"{teorico:.4e}")
            d[1].metric("Pₑ Monte Carlo (por promedio)", f"{pe_mc:.4e}")
            st.caption(
                "Decidir por el signo del promedio (1 número) da el mismo Pe que usar las n "
                "observaciones: el promedio es estadística suficiente."
            )

    with ts:
        st.info(
            "Concepto (teórico). En el canal continuo (Unidad 3), la proyección de la señal "
            "recibida sobre el espacio de señales es la estadística suficiente: es la base del "
            "**filtro apareado**."
        )
