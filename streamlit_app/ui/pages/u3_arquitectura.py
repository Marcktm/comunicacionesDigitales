"""Unidad 3 — Arquitectura TX/RX (encoder, waveform former, n-tuple former)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.receiver import awgn, inner_product
from ui.components import diagrams
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def render() -> None:
    st.title("Arquitectura del transmisor y del receptor")
    st.caption("Unidad 3 · Bixio §3.4 (págs. 102–107)")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u3_arquitectura.md")

    with tg:
        st.subheader("Abstracción del canal de formas de onda (Fig. 3.2 del libro, pág. 96)")
        diagrams.render(diagrams.waveform_abstraction_diagram())

        st.subheader("TX/RX descompuestos (Fig. 3.4 del libro, pág. 103)")
        diagrams.render(diagrams.decomposed_txrx_diagram())

        st.divider()
        st.subheader("Demo: waveform former → canal → n-tuple former (n = 2)")
        st.caption(
            "Base ortonormal ψ₁, ψ₂ = rectángulos disjuntos normalizados. El waveform former "
            "arma w(t) = c₁ψ₁ + c₂ψ₂; el n-tuple former proyecta y recupera (c₁, c₂) + ruido."
        )
        cc = st.columns(3)
        c1 = cc[0].slider("c₁", -2.0, 2.0, 1.0, 0.1)
        c2 = cc[1].slider("c₂", -2.0, 2.0, -0.5, 0.1)
        sigma = cc[2].slider("σ del ruido (por muestra)", 0.0, 2.0, 0.5, 0.1)

        n, T = 800, 2.0
        t = np.linspace(0.0, T, n, endpoint=False)
        dt = t[1] - t[0]
        psi1 = np.where(t < 1.0, 1.0, 0.0)          # ‖ψ‖²=1 (ancho 1, altura 1)
        psi2 = np.where(t >= 1.0, 1.0, 0.0)
        w = c1 * psi1 + c2 * psi2
        r = awgn(w, sigma, seed=1)

        fig = go.Figure()
        fig.add_scatter(x=t, y=r, mode="lines", name="R(t) = w(t)+N(t)",
                        line=dict(color="#bbb"))
        fig.add_scatter(x=t, y=w, mode="lines", name="w(t)",
                        line=dict(color="#1f77b4", width=3))
        fig.update_layout(xaxis_title="t", yaxis_title="amplitud",
                          margin=dict(l=10, r=10, t=20, b=10), height=340,
                          legend=dict(orientation="h", y=1.08))
        render_plotly(fig)

        y1 = inner_product(r, psi1, dt).real
        y2 = inner_product(r, psi2, dt).real
        m = st.columns(4)
        m[0].metric("c₁ enviado", f"{c1:.2f}")
        m[1].metric("Y₁ = ⟨R,ψ₁⟩", f"{y1:.3f}")
        m[2].metric("c₂ enviado", f"{c2:.2f}")
        m[3].metric("Y₂ = ⟨R,ψ₂⟩", f"{y2:.3f}")
        st.caption("Sin ruido, Yⱼ = cⱼ exacto (ortonormalidad). Con ruido, Y = c + Z.")

    with ts:
        st.info(
            "Esta arquitectura ES el SDR: el encoder produce números, el waveform former es el "
            "DAC + filtros del AD9363, y el n-tuple former es el ADC. Se explica sobre el "
            "hardware real en **Unidad 4**."
        )
