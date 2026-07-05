"""Unidad 3 — Casos de modulación (Ejemplo 3.7: 4 elecciones, mismo codebook)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.distributions import q_function
from core.receiver import energy, inner_product
from core.waveforms import WAVEFORM_CHOICES
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _pe_curve():
    eb_db = np.linspace(0, 14, 200)
    e_n0 = 10 ** (eb_db / 10.0)
    fig = go.Figure()
    fig.add_scatter(x=eb_db, y=q_function(np.sqrt(e_n0)), mode="lines",
                    name="ortogonal: Q(√(E/N₀))")
    fig.add_scatter(x=eb_db, y=q_function(np.sqrt(2.0 * e_n0)), mode="lines",
                    line=dict(dash="dash"), name="antipodal: Q(√(2E/N₀))")
    fig.update_layout(
        xaxis_title="E/N₀ [dB]", yaxis_title="Pe", yaxis_type="log",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=30, b=10), height=400,
    )
    return fig


def render() -> None:
    st.title("Casos de modulación en tiempo continuo")
    st.caption("Unidad 3 · Bixio Ejemplo 3.7 (págs. 103–106) y Ejemplos 3.8–3.10 (pág. 106)")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u3_casos.md")

    with tg:
        st.subheader("Las 4 elecciones de W (Fig. 3.5 del libro, pág. 103)")
        name = st.selectbox("Elección", list(WAVEFORM_CHOICES))
        E = st.slider("Energía E", 0.5, 4.0, 1.0, 0.1)
        t, w0, w1 = WAVEFORM_CHOICES[name](E=E)
        dt = t[1] - t[0]

        fig = go.Figure()
        fig.add_scatter(x=t, y=w0, mode="lines", name="w₀(t)")
        fig.add_scatter(x=t, y=w1, mode="lines", name="w₁(t)", line=dict(dash="dash"))
        fig.update_layout(xaxis_title="t", yaxis_title="amplitud",
                          margin=dict(l=10, r=10, t=20, b=10), height=340,
                          legend=dict(orientation="h", y=1.08))
        render_plotly(fig)

        m = st.columns(3)
        m[0].metric("‖w₀‖² (≈E)", f"{energy(w0, dt):.3f}")
        m[1].metric("‖w₁‖² (≈E)", f"{energy(w1, dt):.3f}")
        m[2].metric("⟨w₀,w₁⟩ (≈0)", f"{inner_product(w0, w1, dt).real:.4f}")
        st.caption(
            "Formas de onda muy distintas, pero todas ortogonales de energía E ⇒ el mismo "
            "codebook c₀=(√E,0), c₁=(0,√E) ⇒ la misma Pe. (El sinc-PPM está truncado, por eso "
            "su ⟨w₀,w₁⟩ no es exactamente 0.)"
        )

        st.divider()
        st.subheader("Pe = Q(√(E/N₀)) — idéntica para las cuatro")
        render_plotly(_pe_curve())
        st.caption(
            "Comparación con la señalización antipodal (w, −w): a igual energía gana 3 dB "
            "porque su distancia es 2√E en vez de √(2E)."
        )

    with ts:
        st.info(
            "FSK y QPSK se transmiten de verdad sobre el Pluto en **Unidad 4** (helpers "
            "`complex_exp` y `qpsk_gen` de los laboratorios)."
        )
