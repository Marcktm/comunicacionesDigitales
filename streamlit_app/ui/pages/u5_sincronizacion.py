"""Unidad 5 — Sincronización de símbolo (métrica ML y curva en S del DLL)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.modulation import bpsk_symbols, random_bits
from core.pulses import rrc_taps
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _make_mf_signal(tau_samples, sps=16, num_bits=400, beta=0.5, span=10,
                    sigma=0.05, seed=3):
    """Salida del matched filter con un retardo desconocido de tau_samples."""
    rng = np.random.default_rng(seed)
    symbols = bpsk_symbols(random_bits(num_bits, seed=seed)).astype(float)
    ups = np.zeros(num_bits * sps)
    ups[::sps] = symbols
    taps = rrc_taps(sps, span, beta)
    tx = np.convolve(ups, taps)
    tx = np.concatenate([np.zeros(tau_samples), tx])       # retardo del canal
    rx = tx + rng.normal(0.0, sigma, size=tx.shape)
    mf = np.convolve(rx, taps)
    delay = len(taps) - 1
    return mf[delay:], sps


def _ml_metric_figure(mf, sps, tau_true):
    offsets = np.arange(sps)
    metric = []
    for o in offsets:
        z = mf[o::sps]
        metric.append(np.mean(np.abs(z) ** 2))
    fig = go.Figure(go.Scatter(x=offsets, y=metric, mode="lines+markers",
                               name="M(τ̂) = media |y(jT+τ̂)|²"))
    fig.add_vline(x=tau_true % sps, line_dash="dash", line_color="#d62728",
                  annotation_text="τ verdadero", annotation_position="top")
    fig.update_layout(xaxis_title="offset τ̂ (muestras dentro de un símbolo)",
                      yaxis_title="energía media de las muestras",
                      margin=dict(l=10, r=10, t=30, b=10), height=360)
    best = int(offsets[int(np.argmax(metric))])
    return fig, best


def _s_curve_figure(mf, sps, tau_true, delta=2):
    offsets = np.arange(sps)
    err = []
    for o in offsets:
        early = mf[(o - delta) % sps::sps]
        late = mf[(o + delta) % sps::sps]
        n = min(len(early), len(late))
        err.append(np.mean(np.abs(late[:n]) ** 2 - np.abs(early[:n]) ** 2))
    # centrar el eje en el offset verdadero: Δ = τ̂ − τ
    delta_axis = (offsets - (tau_true % sps) + sps // 2) % sps - sps // 2
    order = np.argsort(delta_axis)
    fig = go.Figure(go.Scatter(x=delta_axis[order], y=np.array(err)[order],
                               mode="lines+markers", name="e(Δ) early–late"))
    fig.add_hline(y=0, line_dash="dot", line_color="#999")
    fig.add_vline(x=0, line_dash="dash", line_color="#d62728",
                  annotation_text="Δ=0", annotation_position="top")
    fig.update_layout(xaxis_title="error de sincronismo Δ (muestras)",
                      yaxis_title="señal de error del DLL",
                      margin=dict(l=10, r=10, t=30, b=10), height=360)
    return fig


def render() -> None:
    st.title("Sincronización de símbolo")
    st.caption("Unidad 5 · Bixio §5.7 (págs. 174–179): ML y delay locked loop")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u5_sincronizacion.md")

    with tg:
        st.subheader("Estimación ML del retardo: la métrica de energía")
        st.caption(
            "El canal mete un retardo desconocido τ. La métrica M(τ̂) = media de |y(jT+τ̂)|² "
            "tiene su máximo cuando muestreás en los picos: ahí está τ."
        )
        sps = 16
        tau = st.slider("retardo verdadero τ (muestras)", 0, sps - 1, 5, 1)
        mf, _ = _make_mf_signal(tau, sps=sps)

        fig, best = _ml_metric_figure(mf, sps, tau)
        render_plotly(fig)
        if best == tau % sps:
            st.success(f"✅ El máximo de la métrica está en τ̂ = {best} = τ: sincronizado.")
        else:
            st.warning(f"El máximo quedó en τ̂ = {best} (τ = {tau}); subí la SNR o los bits.")

        st.divider()
        st.subheader("La curva en S del DLL (error early–late)")
        st.caption(
            "e(Δ) = |y(+δ)|² − |y(−δ)|² promediado: cruza cero en Δ=0 con pendiente definida "
            "— la señal de error que realimenta el lazo para seguir derivas del reloj."
        )
        render_plotly(_s_curve_figure(mf, sps, tau))

    with ts:
        st.info(
            "En el Lab 4 real, la alineación del ojo hace exactamente esto: se busca el offset "
            "de muestreo que maximiza la apertura (la métrica ML) antes de decidir."
        )
