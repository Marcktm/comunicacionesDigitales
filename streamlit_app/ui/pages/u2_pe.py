"""Unidad 2 — Probabilidad de error (marco general + curvas BER)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.modulation import pam_symbol_error_prob, qam4_symbol_error_prob
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _ber_curves(d=2.0):
    """Curvas Pe vs SNR = d/2σ (dB) para varios esquemas."""
    snr_db = np.linspace(0, 18, 200)
    snr = 10 ** (snr_db / 20.0)          # = d/2σ
    sigma = d / (2.0 * snr)
    fig = go.Figure()
    for m in (2, 4, 8):
        fig.add_trace(go.Scatter(x=snr_db, y=pam_symbol_error_prob(m, d, sigma),
                                 name=f"{m}-PAM"))
    fig.add_trace(go.Scatter(x=snr_db, y=qam4_symbol_error_prob(d, sigma),
                             name="4-QAM", line=dict(dash="dash")))
    fig.update_layout(
        xaxis_title="SNR = d/2σ [dB]", yaxis_title="Pe (símbolo)", yaxis_type="log",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=30, b=10), height=440,
    )
    fig.update_yaxes(range=[-8, 0])
    return fig


def render() -> None:
    st.title("Probabilidad de error")
    st.caption("Unidad 2 · Bixio §2.2, §2.3, §2.6")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u2_pe.md")

    with tg:
        st.subheader("Curvas de probabilidad de error vs SNR")
        st.caption(
            "A mayor orden m, se necesita más SNR para la misma Pe. La antipodal (2-PAM) es la "
            "referencia; 4-QAM es dos 2-PAM ortogonales (misma Pe por dimensión)."
        )
        render_plotly(_ber_curves())

    with ts:
        st.info(
            "Cálculo teórico de Pe. La medición real de BER sobre el Pluto (transmitir bits y "
            "contar errores) se puede hacer en la sección SDR de **Unidad 4/5**."
        )
