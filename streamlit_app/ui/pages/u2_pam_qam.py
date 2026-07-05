"""Unidad 2 — m-PAM y m-QAM: constelaciones y probabilidad de error."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.distributions import q_function
from core.modulation import pam_symbol_error_prob, qam4_symbol_error_prob
from ui.components.plots import pam_constellation_figure, qam4_figure, render_plotly
from ui.components.theory import render_theory


def _pe_vs_snr_figure(m, d):
    """Pe de símbolo vs SNR = d/2σ (dB) para m-PAM y 4-QAM."""
    snr_db = np.linspace(0, 16, 200)
    snr = 10 ** (snr_db / 20.0)  # = d/2σ
    sigma = d / (2.0 * snr)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=snr_db, y=pam_symbol_error_prob(m, d, sigma),
                             name=f"{m}-PAM"))
    fig.add_trace(go.Scatter(x=snr_db, y=qam4_symbol_error_prob(d, sigma),
                             name="4-QAM", line=dict(dash="dash")))
    fig.update_layout(
        xaxis_title="SNR = d/2σ [dB]", yaxis_title="Pe (símbolo)", yaxis_type="log",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=30, b=10), height=400,
    )
    return fig


def render() -> None:
    st.title("m-PAM y m-QAM")
    st.caption("Unidad 2 · Bixio §2.4.3 (decisión M-aria, regiones de Voronoi)")

    tab_teoria, tab_graf, tab_sdr = st.tabs(
        ["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"]
    )

    with tab_teoria:
        render_theory("u2_pam_qam.md")

    with tab_graf:
        c = st.columns(3)
        m = c[0].select_slider("Orden m (PAM)", options=[2, 4, 6, 8, 16], value=6)
        d = c[1].slider("Distancia mínima d", 0.5, 4.0, 2.0, 0.1)
        sigma = c[2].slider("σ (ruido)", 0.1, 2.0, 0.5, 0.05)

        st.subheader(f"Constelación {m}-PAM (Fig. 2.9 del libro, pág. 39)")
        render_plotly(pam_constellation_figure(m, d))
        mp = st.columns(2)
        mp[0].metric(f"Pe {m}-PAM", f"{float(pam_symbol_error_prob(m, d, sigma)):.3e}")
        mp[0].caption(f"(2 − 2/{m})·Q(d/2σ) = {2 - 2/m:.3f}·Q({d/(2*sigma):.2f})")

        st.subheader("Constelación 4-QAM (Fig. 2.10 del libro, pág. 40)")
        render_plotly(qam4_figure(d))
        mp[1].metric("Pe 4-QAM", f"{float(qam4_symbol_error_prob(d, sigma)):.3e}")
        mp[1].caption("2Q(d/2σ) − Q²(d/2σ)")

        st.divider()
        st.subheader("Probabilidad de error vs SNR")
        render_plotly(_pe_vs_snr_figure(m, d))

    with tab_sdr:
        st.info(
            "Constelaciones y decisión (teórico/simulado). La transmisión real de una "
            "constelación (QPSK) sobre el Pluto se muestra en **Unidad 4** y en el diagrama de "
            "ojo de **Unidad 5**."
        )
