"""Unidad 2 — Decisión binaria escalar (receptor de umbral, FP/FN)."""
from __future__ import annotations

import streamlit as st

from core.distributions import binary_error_probs
from ui.components.plots import decision_regions_figure, render_plotly
from ui.components.theory import render_theory


def render() -> None:
    st.title("Decisión binaria para observaciones escalares")
    st.caption("Unidad 2 · Bixio §2.4.1")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u2_escalar.md")

    with tg:
        st.subheader("Detector de umbral: falso positivo vs falso negativo")
        c = st.columns(4)
        c0 = c[0].slider("c₀", -5.0, 5.0, -1.0, 0.1)
        c1 = c[1].slider("c₁", -5.0, 5.0, 1.0, 0.1)
        sigma = c[2].slider("σ (ruido)", 0.1, 3.0, 1.0, 0.05)
        p0 = c[3].slider("P(H=0)", 0.05, 0.95, 0.5, 0.05)

        if c0 == c1:
            st.warning("c₀ y c₁ deben ser distintos.")
            return

        res = binary_error_probs(c0, c1, sigma, p0, 1.0 - p0)
        render_plotly(decision_regions_figure(c0, c1, sigma, p0, res.theta))
        m = st.columns(4)
        m[0].metric("Umbral θ", f"{res.theta:.3f}")
        m[1].metric("Falso positivo Pₑ(0)", f"{res.pe0:.3e}")
        m[2].metric("Falso negativo Pₑ(1)", f"{res.pe1:.3e}")
        m[3].metric("Pₑ total", f"{res.pe:.3e}")
        st.caption(
            "Subí P(H=0): θ se corre hacia c₁ y se intercambian las áreas de falso positivo "
            "(verde) y falso negativo (rojo)."
        )

    with ts:
        st.info(
            "Receptor de umbral (teórico). Es exactamente lo que hace un detector físico: medir "
            "y comparar con θ. La verificación del ruido gaussiano está en **Unidad 4 · "
            "Caracterización de ruido**."
        )
