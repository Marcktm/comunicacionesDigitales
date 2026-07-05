"""Unidad 3 — Filtro apareado (correlador vs matched filter, Fig. 3.8)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.receiver import awgn, correlator, matched_filter_output
from ui.components import diagrams
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def render() -> None:
    st.title("Filtro apareado (matched filter)")
    st.caption("Unidad 3 · Bixio §3.5 (págs. 107–111)")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u3_matched_filter.md")

    with tg:
        st.subheader("Correlador vs filtro apareado (Fig. 3.6 del libro, pág. 107)")
        diagrams.render(diagrams.correlator_vs_matched_diagram())

        st.divider()
        st.subheader("PAM binaria: rectángulo → triángulo (Fig. 3.8 del libro, pág. 108)")
        st.caption(
            "Se transmite w(t) = ±a·ψ(t) con ψ rectangular en [0,T]. La salida del filtro "
            "apareado h(t)=ψ(T−t) es un triángulo con pico ±a en t=T: el instante óptimo de "
            "muestreo."
        )
        c = st.columns(3)
        a = c[0].slider("amplitud a", 0.5, 3.0, 1.0, 0.1)
        signo = c[1].radio("símbolo", ["+a (H=0)", "−a (H=1)"], horizontal=True)
        sigma = c[2].slider("σ del ruido (por muestra)", 0.0, 3.0, 0.8, 0.1)

        n, T = 600, 1.0
        t = np.linspace(0.0, T, n, endpoint=False)
        dt = t[1] - t[0]
        psi = np.ones(n) / np.sqrt(T)                    # ‖ψ‖²=1
        s = a if signo.startswith("+") else -a
        r = awgn(s * psi, sigma, seed=3)

        y = matched_filter_output(r, psi, dt)            # y(t), grilla 'full'
        ty = np.arange(len(y)) * dt                      # y(T) cae en el índice n-1

        fig = go.Figure()
        fig.add_scatter(x=t, y=r, mode="lines", name="r(t) (con ruido)",
                        line=dict(color="#bbb"))
        fig.add_scatter(x=ty, y=y, mode="lines", name="salida del filtro y(t)",
                        line=dict(color="#1f77b4", width=3))
        fig.add_vline(x=T, line_dash="dash", line_color="#d62728",
                      annotation_text="t = T", annotation_position="top")
        fig.update_layout(xaxis_title="t", yaxis_title="amplitud",
                          margin=dict(l=10, r=10, t=20, b=10), height=380,
                          legend=dict(orientation="h", y=1.08))
        render_plotly(fig)

        yT = float(y[n - 1])
        corr = correlator(r, psi, dt).real
        m = st.columns(3)
        m[0].metric("símbolo enviado", f"{s:+.2f}")
        m[1].metric("y(T) (filtro apareado)", f"{yT:+.3f}")
        m[2].metric("∫r·ψ (correlador)", f"{corr:+.3f}")
        st.caption(
            "y(T) y el correlador coinciden (misma integral). El decisor compara y(T) con 0: "
            "sin ruido el pico vale exactamente ±a."
        )

    with ts:
        st.info(
            "En los laboratorios (Lab 4), el filtro apareado es el RRC del receptor: TX usa "
            "raíz de coseno realzado y RX aplica el mismo filtro → el conjunto cumple Nyquist. "
            "Se desarrolla en **Unidad 5** y se prueba con el Pluto."
        )
