"""Unidad 2 — Criterio MAP y ML (página de referencia, Fase 1).

Teoría completa (Markdown+LaTeX) + gráficas Plotly interactivas + verificación
Monte Carlo de la probabilidad de error.
"""
from __future__ import annotations

import numpy as np
import streamlit as st

from core.decision import monte_carlo_pe
from core.distributions import binary_error_probs
from ui.components.plots import decision_regions_figure, q_curve_figure, render_plotly
from ui.components.theory import render_theory


def render() -> None:
    st.title("⭐ Criterio MAP y ML — hipótesis binaria")
    st.caption(
        "Unidad 2 · Diseño de receptor para observaciones en tiempo discreto "
        "(Bixio §2.2 y §2.4.1)"
    )

    tab_teoria, tab_graf, tab_sdr = st.tabs(
        ["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"]
    )

    # ---- 1. Teoría ------------------------------------------------------- #
    with tab_teoria:
        render_theory("u2_map_ml.md")

    # ---- 2. Gráficas de ejemplo ----------------------------------------- #
    with tab_graf:
        st.subheader("Decisión binaria en canal AWGN — interactivo")
        c = st.columns(4)
        c0 = c[0].slider("c₀", -5.0, 5.0, -1.0, 0.1)
        c1 = c[1].slider("c₁", -5.0, 5.0, 1.0, 0.1)
        sigma = c[2].slider("σ (desvío del ruido)", 0.1, 3.0, 1.0, 0.05)
        p0 = c[3].slider("P(H=0)", 0.05, 0.95, 0.5, 0.05)

        if c0 == c1:
            st.warning("c₀ y c₁ deben ser distintos.")
            return

        res = binary_error_probs(c0, c1, sigma, p0, 1.0 - p0)
        render_plotly(decision_regions_figure(c0, c1, sigma, p0, res.theta))

        m = st.columns(4)
        m[0].metric("Umbral θ", f"{res.theta:.3f}")
        m[1].metric("Pₑ (total)", f"{res.pe:.3e}")
        m[2].metric("Pₑ(0)", f"{res.pe0:.3e}")
        m[3].metric("Pₑ(1)", f"{res.pe1:.3e}")
        st.caption(
            "θ = σ²/(c₁−c₀)·ln η + (c₀+c₁)/2, con η = P(H=0)/P(H=1). "
            "Áreas sombreadas = probabilidad de error condicional."
        )

        st.divider()
        st.subheader("Verificación Monte Carlo")
        mc = st.columns([2, 1, 1])
        n = mc[0].select_slider(
            "N muestras",
            options=[10_000, 100_000, 500_000, 1_000_000],
            value=100_000,
        )
        seed = mc[1].number_input("seed", value=0, step=1)
        if mc[2].button("Simular", width="stretch"):
            with st.spinner("Simulando canal AWGN…"):
                pe_mc = monte_carlo_pe(c0, c1, sigma, p0, n=int(n), seed=int(seed))
            d = st.columns(2)
            d[0].metric("Pₑ teórico", f"{res.pe:.4e}")
            d[1].metric("Pₑ Monte Carlo", f"{pe_mc:.4e}")

        st.divider()
        st.subheader("Curva Pₑ = Q(d/2σ) vs σ (caso equiprobable)")
        render_plotly(q_curve_figure(np.linspace(0.1, 3.0, 200), c0, c1))

    # ---- 3. Bonus SDR ---------------------------------------------------- #
    with tab_sdr:
        st.info(
            "Este tema (decisión óptima) es **puramente teórico/simulado**: no requiere SDR. "
            "El vínculo con hardware aparece más adelante — la **caracterización de ruido** "
            "(Unidad 4, Lab 2) verifica que el ruido del receptor Pluto es gaussiano, que es "
            "la hipótesis clave detrás de todo este desarrollo."
        )
