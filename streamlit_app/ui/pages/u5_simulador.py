"""Unidad 5 — Simulador BPSK + AWGN extremo a extremo."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy.signal import welch

from core.simulator import simulate_bpsk_chain
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _stages_figure(res, ns, n_show_sym=12):
    """TX, RX y salida del matched filter en un tramo corto, con los instantes de decisión."""
    n = n_show_sym * ns
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        subplot_titles=("tren transmitido", "recibido (con ruido)",
                                        "salida del matched filter"))
    fig.add_scatter(y=res.tx_wave[:n], mode="lines", row=1, col=1, showlegend=False)
    fig.add_scatter(y=res.rx_wave[:n], mode="lines", row=2, col=1, showlegend=False,
                    line=dict(color="#999"))
    fig.add_scatter(y=res.mf_out[:n], mode="lines", row=3, col=1, showlegend=False,
                    line=dict(color="#1f77b4"))
    idx = ns - 1 + ns * np.arange(n_show_sym)
    fig.add_scatter(x=idx, y=res.mf_out[idx], mode="markers", row=3, col=1,
                    marker=dict(size=8, color="#d62728"), name="decisión",
                    showlegend=False)
    fig.update_layout(height=560, margin=dict(l=10, r=10, t=40, b=10))
    fig.update_xaxes(title_text="n (muestras)", row=3, col=1)
    return fig


def _hist_figure(z):
    fig = go.Figure(go.Histogram(x=z, histnorm="probability density", nbinsx=80,
                                 marker_color="#1f77b4"))
    fig.update_layout(title="histograma de las muestras de decisión (bimodal en ±1)",
                      xaxis_title="Z", yaxis_title="densidad",
                      margin=dict(l=10, r=10, t=40, b=10), height=330)
    return fig


def _psd_figure(tx, ns):
    f, pxx = welch(tx, fs=ns, nperseg=1024, return_onesided=False)
    order = np.argsort(f)
    fig = go.Figure(go.Scatter(x=f[order], y=10 * np.log10(pxx[order] + 1e-15),
                               mode="lines"))
    fig.update_layout(title="PSD del tren transmitido (Welch) — forma sinc²(fT)",
                      xaxis_title="f·T", yaxis_title="PSD [dB]",
                      margin=dict(l=10, r=10, t=40, b=10), height=330)
    return fig


def render() -> None:
    st.title("Simulador BPSK + AWGN extremo a extremo")
    st.caption("Unidad 5 · integra Unidades 2, 3 y 5 · notebook del Parcial 2")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Simulador", "📡 Bonus SDR"])

    with tt:
        render_theory("u5_simulador.md")

    with tg:
        c = st.columns(3)
        num_bits = c[0].select_slider("bits", options=[1024, 4096, 16384, 65536],
                                      value=4096)
        ns = c[1].select_slider("Ns (muestras/símbolo)", options=[4, 8, 16, 32], value=16)
        sigma = c[2].slider("σ del ruido", 0.1, 2.0, 0.5, 0.05)

        res = simulate_bpsk_chain(num_bits=int(num_bits), ns=int(ns),
                                  sigma=sigma, seed=0)

        m = st.columns(3)
        m[0].metric("Pₑ teórica  Q(1/σ)", f"{res.pe_theory:.3e}")
        m[1].metric("Pₑ Monte Carlo", f"{res.pe_est:.3e}")
        m[2].metric("errores", f"{int(res.pe_est * num_bits)} / {num_bits}")

        render_plotly(_stages_figure(res, int(ns)))
        st.caption(
            "Arriba: el tren de pulsos limpio. Medio: lo que 've' el receptor (puede no "
            "distinguirse nada a ojo). Abajo: el matched filter separa los niveles; los "
            "puntos rojos son los instantes de decisión."
        )
        render_plotly(_hist_figure(res.decision_samples))
        render_plotly(_psd_figure(res.tx_wave, int(ns)))

    with ts:
        st.info(
            "La versión física de esta cadena es el **Lab 4** (página *ISI y diagrama de "
            "ojo*): la misma señal BPSK conformada, pero atravesando el Pluto en vez del "
            "canal simulado."
        )
