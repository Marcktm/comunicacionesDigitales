"""Unidad 5 — PSD del tren de pulsos (fórmula + verificación empírica)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.signal import welch

from core.pulses import pulse_train_psd, rect_pulse_spectrum
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _theory_psd_figure(case, T=1.0, E=1.0):
    f = np.linspace(-3.0 / T, 3.0 / T, 601)
    rect = rect_pulse_spectrum(f, T)
    if case == "incorrelados + pulso rectangular":
        sx = pulse_train_psd(f, rect, K={0: E}, T=T)
        label = "S_X = E·|ξF|²/T ∝ sinc²(fT)"
    elif case == "incorrelados + pulso sinc":
        flat = np.where(np.abs(f) <= 1 / (2 * T), T, 0.0)
        sx = pulse_train_psd(f, flat, K={0: E}, T=T)
        label = "S_X plana en [−1/2T, 1/2T]"
    else:  # codificación correlativa
        sx = pulse_train_psd(f, rect, K={0: E, 2: -E / 2, -2: -E / 2}, T=T)
        label = "S_X ∝ sin²(2πfT) — nula en DC"
    fig = go.Figure(go.Scatter(x=f * T, y=sx, mode="lines", name=label))
    fig.update_layout(xaxis_title="f·T", yaxis_title="S_X(f)",
                      title=label, margin=dict(l=10, r=10, t=40, b=10), height=380)
    return fig


def _empirical_figure(correlative, T_samples=8, n_sym=4000, seed=0):
    """Tren de pulsos simulado + PSD de Welch vs la predicción teórica."""
    rng = np.random.default_rng(seed)
    b = rng.integers(0, 2, n_sym).astype(float)
    if correlative:
        x_sym = np.sqrt(2.0) * (b - np.roll(b, 2))    # X_i = √2E (B_i − B_{i−2}), E=1
    else:
        x_sym = 2 * b - 1.0                            # ±1 incorrelados
    pulse = np.ones(T_samples) / np.sqrt(T_samples)    # rect energía 1
    x = np.convolve(np.repeat(x_sym, T_samples) / np.sqrt(T_samples), np.ones(1))
    x = np.repeat(x_sym, T_samples) * pulse[0]         # tren rectangular
    f, pxx = welch(x, fs=T_samples, nperseg=1024, return_onesided=False)
    order = np.argsort(f)
    fig = go.Figure(go.Scatter(x=f[order], y=pxx[order], mode="lines",
                               name="PSD empírica (Welch)"))
    fig.update_layout(xaxis_title="f·T", yaxis_title="PSD",
                      margin=dict(l=10, r=10, t=20, b=10), height=340)
    return fig


def render() -> None:
    st.title("Densidad espectral de potencia (PSD)")
    st.caption("Unidad 5 · Bixio §5.3 (págs. 163–167) — derivación completa en la teoría")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u5_psd.md")

    with tg:
        st.subheader("La fórmula S_X(f) = (|ξF|²/T)·Σ K[k]e^(−j2πkfT), por casos")
        case = st.selectbox("Caso", [
            "incorrelados + pulso rectangular",
            "incorrelados + pulso sinc",
            "codificación correlativa (Bi − Bi−2)",
        ])
        render_plotly(_theory_psd_figure(case))
        st.caption(
            "El pulso pone la forma (sinc² para el rectángulo, plana para el sinc); la "
            "correlación de símbolos la modula (el encoder correlativo anula el DC)."
        )

        st.divider()
        st.subheader("Verificación empírica (tren simulado + Welch)")
        corr = st.toggle("usar codificación correlativa (X_i = √2E·(B_i − B_{i−2}))", value=False)
        render_plotly(_empirical_figure(corr))
        st.caption(
            "La PSD medida por Welch reproduce la teórica: sinc² con símbolos incorrelados, "
            "sinc²·sin² (nula en DC) con el encoder correlativo."
        )

    with ts:
        st.info(
            "La PSD real de lo que emite el Pluto se mide capturando y aplicando Welch "
            "(igual que en el Lab 1, Unidad 4). La máscara regulatoria se verifica ahí."
        )
