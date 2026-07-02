"""Unidad 2 — Prueba de hipótesis (MAP/ML general + ejemplo de Poisson)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import poisson

from ui.components import diagrams
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _poisson_figure(lam0, lam1):
    """Dos pmf de Poisson, umbral ML γ y regiones de error."""
    kmax = int(poisson.ppf(0.999, max(lam0, lam1))) + 2
    y = np.arange(0, kmax + 1)
    p0, p1 = poisson.pmf(y, lam0), poisson.pmf(y, lam1)
    gamma = (lam1 - lam0) / np.log(lam1 / lam0)

    fig = go.Figure()
    fig.add_bar(x=y, y=p0, name="P(y | H=0)", marker_color="#2ca02c", opacity=0.7)
    fig.add_bar(x=y, y=p1, name="P(y | H=1)", marker_color="#d62728", opacity=0.7)
    fig.add_vline(x=gamma, line_dash="dash", line_color="#333",
                  annotation_text="γ", annotation_position="top")
    fig.update_layout(
        barmode="overlay", xaxis_title="y (fotones detectados)", yaxis_title="probabilidad",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=30, b=10), height=380,
    )
    # Pe (ML exacto: decidir por la pmf mayor en cada y)
    decide1 = p1 >= p0
    pe = 0.5 * p0[decide1].sum() + 0.5 * p1[~decide1].sum()
    return fig, gamma, pe


def render() -> None:
    st.title("Prueba de hipótesis — MAP y ML")
    st.caption("Unidad 2 · Bixio §2.2 (marco general de decisión)")

    tab_teoria, tab_graf, tab_sdr = st.tabs(
        ["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"]
    )

    with tab_teoria:
        render_theory("u2_hipotesis.md")

    with tab_graf:
        st.subheader("Configuración general (Fig. 2.1)")
        st.caption("Fuente → Transmisor → Canal → Receptor. El receptor adivina Ĥ a partir de Y.")
        diagrams.render(diagrams.channel_block_diagram())

        st.divider()
        st.subheader("Ejemplo: un bit por fibra óptica (canal de Poisson)")
        c = st.columns(2)
        lam0 = c[0].slider("λ₀ (LED apagado)", 0.5, 8.0, 2.0, 0.1)
        lam1 = c[1].slider("λ₁ (LED encendido)", 1.0, 20.0, 8.0, 0.1)
        if lam1 <= lam0:
            st.warning("Debe ser λ₁ > λ₀.")
        else:
            fig, gamma, pe = _poisson_figure(lam0, lam1)
            render_plotly(fig)
            m = st.columns(2)
            m[0].metric("Umbral ML  γ", f"{gamma:.2f}")
            m[1].metric("Pₑ (ML)", f"{pe:.3e}")
            st.caption("γ = (λ₁−λ₀)/ln(λ₁/λ₀). Se decide Ĥ=1 cuando se cuentan y ≥ γ fotones.")

    with tab_sdr:
        st.info(
            "Marco teórico general (sin hardware). La verificación con SDR del supuesto de ruido "
            "gaussiano aparece en **Unidad 4 · Caracterización de ruido**."
        )
