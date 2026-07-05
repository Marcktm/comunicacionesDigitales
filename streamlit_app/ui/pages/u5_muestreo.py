"""Unidad 5 — Tren de pulsos y teorema de muestreo (reconstrucción sinc)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from ui.components import diagrams
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _reconstruction_figure(n_terms, T=1.0):
    """Señal limitada en banda, sus muestras y la reconstrucción sinc truncada."""
    rng = np.random.default_rng(4)
    n_samp = 16
    s = rng.normal(0.0, 1.0, n_samp)                     # muestras w(nT)
    t = np.linspace(0, (n_samp - 1) * T, 1200)

    def reconstruct(k_terms):
        y = np.zeros_like(t)
        for n in range(min(k_terms, n_samp)):
            y += s[n] * np.sinc(t / T - n)
        return y

    full = reconstruct(n_samp)
    partial = reconstruct(n_terms)

    fig = go.Figure()
    fig.add_scatter(x=t, y=full, mode="lines", name="w(t) (todos los términos)",
                    line=dict(color="#bbb"))
    fig.add_scatter(x=t, y=partial, mode="lines",
                    name=f"reconstrucción con {n_terms} sincs",
                    line=dict(color="#1f77b4", width=3))
    fig.add_scatter(x=np.arange(n_samp) * T, y=s, mode="markers",
                    name="muestras w(nT)", marker=dict(size=9, color="#d62728"))
    fig.update_layout(xaxis_title="t / T", yaxis_title="amplitud",
                      margin=dict(l=10, r=10, t=20, b=10), height=400,
                      legend=dict(orientation="h", y=1.1))
    return fig


def render() -> None:
    st.title("Tren de pulsos y teorema de muestreo")
    st.caption("Unidad 5 · Bixio §5.1–§5.2 (págs. 159–163)")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u5_muestreo.md")

    with tg:
        st.subheader("Canal pasa-bajo ideal (Fig. 5.1 del libro, pág. 160)")
        diagrams.render(diagrams.lowpass_channel_diagram())

        st.subheader("Símbolo a símbolo sobre un tren de pulsos (Fig. 5.2, pág. 161)")
        diagrams.render(diagrams.symbol_by_symbol_diagram())

        st.divider()
        st.subheader("Reconstrucción por interpolación sinc (el teorema en acción)")
        st.caption(
            "Cada muestra w(nT) aporta un sinc centrado en nT; la suma reconstruye la señal. "
            "Agregá términos y mirá cómo la reconstrucción converge a la señal completa."
        )
        n_terms = st.slider("sincs incluidos", 1, 16, 4, 1)
        render_plotly(_reconstruction_figure(n_terms))

    with ts:
        st.info(
            "Este teorema ES el SDR (Unidad 4): el transmisor 'reconstruye' primero (DAC) y el "
            "receptor muestrea después (ADC). El estándar vive en el software que genera los "
            "números s_j."
        )
