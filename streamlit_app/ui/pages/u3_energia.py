"""Unidad 3 — Energía de la señal y espacio de producto interno."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.receiver import energy, inner_product
from core.waveforms import fsk, rect_ppm
from ui.components import diagrams
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def render() -> None:
    st.title("Energía de la señal y espacio de producto interno")
    st.caption("Unidad 3 · Bixio §3.1 (págs. 95–97)")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u3_energia.md")

    with tg:
        st.subheader("Canal AWGN de tiempo continuo (Fig. 3.1 del libro, pág. 95)")
        diagrams.render(diagrams.continuous_awgn_diagram())

        st.divider()
        st.subheader("Energía y producto interno de señales (numérico)")
        st.caption(
            "‖w‖² = ∫|w(t)|²dt y ⟨w₀,w₁⟩ = ∫w₀·w₁dt, aproximados por regla del rectángulo. "
            "Con E=1 ambas señales tienen energía 1 y son ortogonales."
        )
        choice = st.radio("Par de señales", ["PPM rectangular", "FSK ortogonal"],
                          horizontal=True)
        E = st.slider("Energía E", 0.5, 4.0, 1.0, 0.1)
        t, w0, w1 = rect_ppm(E=E) if choice == "PPM rectangular" else fsk(E=E)
        dt = t[1] - t[0]

        fig = go.Figure()
        fig.add_scatter(x=t, y=w0, mode="lines", name="w₀(t)")
        fig.add_scatter(x=t, y=w1, mode="lines", name="w₁(t)", line=dict(dash="dash"))
        fig.update_layout(xaxis_title="t", yaxis_title="amplitud",
                          margin=dict(l=10, r=10, t=20, b=10), height=360,
                          legend=dict(orientation="h", y=1.05))
        render_plotly(fig)

        m = st.columns(3)
        m[0].metric("‖w₀‖²", f"{energy(w0, dt):.4f}")
        m[1].metric("‖w₁‖²", f"{energy(w1, dt):.4f}")
        m[2].metric("⟨w₀,w₁⟩", f"{inner_product(w0, w1, dt).real:.4f}")

    with ts:
        st.info(
            "En el Pluto, la energía transmitida se controla con `tx_hardwaregain_chan0` "
            "(atenuación en dB) y la escala digital 2¹⁴ del DAC — se ve en **Unidad 4 · "
            "Cómo programar el SDR**."
        )
