"""Unidad 5 — Coseno realzado y RRC (Fig. 5.6 + puntos singulares)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.pulses import raised_cosine_spectrum, rrc_pulse, rrc_taps
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _spectrum_figure(beta, T=1.0):
    f = np.linspace(-1.2 / T, 1.2 / T, 601)
    fig = go.Figure()
    fig.add_scatter(x=f * T, y=raised_cosine_spectrum(f, T, beta), mode="lines",
                    name=f"|ψF|² (β={beta:.2f})", line=dict(width=3))
    fig.add_scatter(x=f * T, y=raised_cosine_spectrum(f, T, 1e-9), mode="lines",
                    name="β→0 (rectángulo)", line=dict(dash="dot"))
    fig.add_vline(x=0.5, line_dash="dash", line_color="#999",
                  annotation_text="1/2T", annotation_position="top")
    fig.update_layout(xaxis_title="f·T", yaxis_title="|ψF(f)|²",
                      margin=dict(l=10, r=10, t=20, b=10), height=360,
                      legend=dict(orientation="h", y=1.1))
    return fig


def _pulse_figure(beta, T=1.0):
    t = np.linspace(-6 * T, 6 * T, 1201)
    fig = go.Figure()
    fig.add_scatter(x=t / T, y=rrc_pulse(t, T, beta), mode="lines",
                    name=f"ψ(t), β={beta:.2f}", line=dict(width=3))
    fig.add_scatter(x=t / T, y=rrc_pulse(t, T, 1e-9), mode="lines",
                    name="β→0 (sinc)", line=dict(dash="dot"))
    if beta > 0:
        ts = T / (4 * beta)
        if ts <= 6 * T:
            v = rrc_pulse(np.array([ts]), T, beta)[0]
            fig.add_scatter(x=[ts / T, -ts / T], y=[v, v], mode="markers",
                            name="t = ±T/4β (L'Hôpital)",
                            marker=dict(size=10, color="#d62728", symbol="x"))
    fig.update_layout(xaxis_title="t / T", yaxis_title="ψ(t)",
                      margin=dict(l=10, r=10, t=20, b=10), height=380,
                      legend=dict(orientation="h", y=1.1))
    return fig


def _isi_vs_span_figure(beta, sps=8):
    spans = np.arange(2, 26, 2)
    isi = []
    for span in spans:
        taps = rrc_taps(sps, int(span), beta)
        rc = np.convolve(taps, taps[::-1])
        c = len(rc) // 2
        isi.append(max(abs(rc[c + k * sps]) for k in range(1, int(span))))
    fig = go.Figure(go.Scatter(x=spans, y=isi, mode="lines+markers"))
    fig.update_layout(xaxis_title="span (símbolos de truncado)",
                      yaxis_title="ISI residual máx |R(kT)|", yaxis_type="log",
                      margin=dict(l=10, r=10, t=20, b=10), height=340)
    return fig


def render() -> None:
    st.title("Coseno realzado y raíz de coseno realzado (RRC)")
    st.caption("Unidad 5 · Bixio §5.5 (págs. 170–172) y apéndice §5.14")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u5_rrc.md")

    with tg:
        beta = st.slider("factor de roll-off β", 0.05, 1.0, 0.5, 0.05)

        st.subheader("Espectro |ψF(f)|² (Fig. 5.6a del libro, pág. 170)")
        render_plotly(_spectrum_figure(beta))

        st.subheader("Pulso ψ(t) (Fig. 5.6b) — con los puntos singulares marcados")
        render_plotly(_pulse_figure(beta))
        st.caption(
            "Las ✕ rojas son t = ±T/4β, donde la fórmula da 0/0 y el valor sale por L'Hôpital "
            "(así está resuelto en core/pulses.py). Con β chico el pulso decae lento."
        )

        st.divider()
        st.subheader("ISI residual al truncar el RRC (el trade-off del Lab 4)")
        render_plotly(_isi_vs_span_figure(beta))
        st.caption(
            "Truncar más corto deja R(kT) ≠ 0 (ISI). Con β grande podés truncar corto; con β "
            "chico necesitás span largo. Esto es lo que se ve cerrarse en el ojo."
        )

    with ts:
        st.info(
            "El RRC es el filtro del **Lab 4**: TX conforma con RRC y RX aplica el mismo RRC "
            "(matched filter) — el total cumple Nyquist. Probalo sobre el Pluto en la página "
            "**ISI y diagrama de ojo**."
        )
