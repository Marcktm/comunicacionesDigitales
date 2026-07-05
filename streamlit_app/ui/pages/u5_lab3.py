"""Unidad 5 — Lab 3: muestreo, aliasing y filtrado."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.modulation import square_wave
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _alias_figure(fc, fs=10.0):
    """Tono 'continuo' de frecuencia fc, sus muestras a fs y el alias reconstruido."""
    t = np.linspace(0, 2.0, 2000)
    x = np.cos(2 * np.pi * fc * t)
    ts = np.arange(0, 2.0, 1.0 / fs)
    xs = np.cos(2 * np.pi * fc * ts)
    k = np.round(fc / fs)
    fa = abs(fc - k * fs)
    xa = np.cos(2 * np.pi * fa * t)

    fig = go.Figure()
    fig.add_scatter(x=t, y=x, mode="lines", name=f"tono real ({fc:.1f} Hz)",
                    line=dict(color="#bbb"))
    fig.add_scatter(x=t, y=xa, mode="lines", name=f"alias ({fa:.1f} Hz)",
                    line=dict(color="#d62728", width=2, dash="dash"))
    fig.add_scatter(x=ts, y=xs, mode="markers", name=f"muestras (Fs={fs:.0f} Hz)",
                    marker=dict(size=8, color="#1f77b4"))
    fig.update_layout(xaxis_title="t [s]", yaxis_title="amplitud",
                      margin=dict(l=10, r=10, t=20, b=10), height=380,
                      legend=dict(orientation="h", y=1.1))
    return fig, fa


def _harmonics_figure(n_harm):
    """Cuadrada reconstruida con sus primeros armónicos impares (efecto pasa-bajos)."""
    t = np.linspace(0, 2.0, 2000)
    f0 = 1.0
    square = np.sign(np.sin(2 * np.pi * f0 * t))
    y = np.zeros_like(t)
    for i in range(n_harm):
        n = 2 * i + 1
        y += (4 / np.pi) * np.sin(2 * np.pi * n * f0 * t) / n
    fig = go.Figure()
    fig.add_scatter(x=t, y=square, mode="lines", name="cuadrada ideal",
                    line=dict(color="#bbb"))
    fig.add_scatter(x=t, y=y, mode="lines",
                    name=f"salida del pasa-bajos ({n_harm} armónicos)",
                    line=dict(color="#1f77b4", width=2))
    fig.update_layout(xaxis_title="t [s]", yaxis_title="amplitud",
                      margin=dict(l=10, r=10, t=20, b=10), height=380,
                      legend=dict(orientation="h", y=1.1))
    return fig


def render() -> None:
    st.title("Lab 3 — Muestreo, aliasing y filtrado")
    st.caption("Unidad 5 · notebooks laboratorio3 · Bixio §5.2")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u5_lab3.md")

    with tg:
        st.subheader("Aliasing: el tono disfrazado")
        st.caption(
            "Subí la frecuencia del tono más allá de Fs/2 = 5 Hz: las muestras (azul) dejan "
            "de distinguir el tono real (gris) del alias (rojo)."
        )
        fc = st.slider("frecuencia del tono [Hz]", 0.5, 14.0, 3.0, 0.5)
        fig, fa = _alias_figure(fc)
        render_plotly(fig)
        if fc <= 5.0:
            st.success(f"✅ fc = {fc:.1f} Hz ≤ Fs/2: sin aliasing (el alias coincide con el tono).")
        else:
            st.error(f"❌ fc = {fc:.1f} Hz > Fs/2 = 5 Hz: las muestras 'ven' {fa:.1f} Hz.")

        st.divider()
        st.subheader("Filtrado de una cuadrada: cuántos armónicos pasan")
        n_harm = st.slider("armónicos impares que deja pasar el filtro", 1, 25, 3, 1)
        render_plotly(_harmonics_figure(n_harm))
        st.caption(
            "Con 1 armónico la cuadrada sale senoidal; al abrir el corte se va 'cuadrando' "
            "(con el rizado de Gibbs en los flancos). Es lo que hacen los filtros del AD9363."
        )

    with ts:
        st.info(
            "Versión con hardware: transmitir un tono cerca de Fs/2 y bajar `sample_rate` para "
            "ver el alias, o transmitir la cuadrada (kata de la Unidad 4) y observar el "
            "redondeo de flancos por los filtros de la cadena TX/RX del Pluto."
        )
