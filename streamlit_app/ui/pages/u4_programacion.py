"""Unidad 4 — Cómo programar el SDR (tutorial línea por línea + katas)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.modulation import complex_exp, qpsk_gen, square_wave
from ui.components.code_kata import render_kata
from ui.components.plots import render_plotly
from ui.components.theory import render_theory
from ui.content.katas.sdr import SDR_KATAS


def _helpers_figure(which):
    fig = go.Figure()
    if which == "complex_exp (tono I/Q)":
        x = complex_exp(256, Fc=1e5, Fs=1e6)
        fig.add_scatter(y=x.real, mode="lines", name="I = Re{x}")
        fig.add_scatter(y=x.imag, mode="lines", name="Q = Im{x}", line=dict(dash="dash"))
    elif which == "square_wave":
        fig.add_scatter(y=square_wave(200, period=20), mode="lines", name="onda cuadrada")
    else:  # qpsk_gen
        sym, ups = qpsk_gen(32, sps=8, seed=1)
        fig.add_scatter(y=ups.real, mode="lines", name="I (sobremuestreada)")
        fig.add_scatter(y=ups.imag, mode="lines", name="Q (sobremuestreada)",
                        line=dict(dash="dash"))
    fig.update_layout(xaxis_title="n (muestras)", yaxis_title="amplitud",
                      margin=dict(l=10, r=10, t=20, b=10), height=320,
                      legend=dict(orientation="h", y=1.1))
    return fig


def render() -> None:
    st.title("Cómo programar el SDR")
    st.caption("Unidad 4 · Tutorial línea por línea + práctica de código")

    tt, tg, ts = st.tabs(["📖 Teoría (tutorial)", "📈 Helpers en acción", "🥋 Práctica de código"])

    with tt:
        render_theory("u4_programacion.md")

    with tg:
        st.subheader("Los helpers de los laboratorios (core/modulation.py)")
        which = st.selectbox(
            "Helper", ["complex_exp (tono I/Q)", "square_wave", "qpsk_gen (I/Q QPSK)"]
        )
        render_plotly(_helpers_figure(which))
        st.caption(
            "Estas señales son las que después se escalan a 2¹⁴ y se pasan a `sdr.tx(...)`. "
            "El tono es la señal del Lab 1; la QPSK sobremuestreada, la base del Lab 4."
        )

    with ts:
        st.subheader("Práctica: completá el código y validalo ✔")
        st.caption(
            "Cada ejercicio se ejecuta en un sandbox con `np` (numpy) disponible y se valida "
            "por comportamiento contra la implementación de referencia. Sin hardware: son "
            "los bloques que después usás contra el Pluto real."
        )
        for kata in SDR_KATAS:
            render_kata(kata)
