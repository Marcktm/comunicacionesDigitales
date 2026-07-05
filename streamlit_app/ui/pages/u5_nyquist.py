"""Unidad 5 — Criterio de Nyquist (espectro plegado interactivo)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.pulses import folded_spectrum, raised_cosine_spectrum
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _triangle_spectrum(f, T=1.0, **_):
    f = np.abs(np.asarray(f, dtype=float))
    return np.where(f < 1.0 / T, T * (1.0 - T * f), 0.0)


def _narrow_rect_spectrum(f, T=1.0, B_frac=0.35, **_):
    # soporte menor a 1/2T: NO cumple el criterio (quedan huecos)
    f = np.abs(np.asarray(f, dtype=float))
    return np.where(f <= B_frac / T, T, 0.0)


def _folding_figure(name, beta, T=1.0):
    f = np.linspace(-2.0 / T, 2.0 / T, 801)
    if name == "Coseno realzado":
        fn, kw = raised_cosine_spectrum, {"beta": beta}
    elif name == "Triángulo":
        fn, kw = _triangle_spectrum, {}
    else:
        fn, kw = _narrow_rect_spectrum, {}

    fig = go.Figure()
    fig.add_scatter(x=f * T, y=fn(f, T=T, **kw), mode="lines",
                    name="|ψF(f)|²", line=dict(color="#1f77b4", width=3))
    for k in (-1, 1):
        fig.add_scatter(x=f * T, y=fn(f - k / T, T=T, **kw), mode="lines",
                        name=f"réplica k={k}", line=dict(dash="dash"))
    total = folded_spectrum(fn, f, T=T, k_range=6, **kw)
    fig.add_scatter(x=f * T, y=total, mode="lines", name="Σ réplicas (plegado)",
                    line=dict(color="#d62728", width=3))
    fig.add_hline(y=T, line_dash="dot", line_color="#333",
                  annotation_text="T", annotation_position="right")
    fig.update_layout(xaxis_title="f·T", yaxis_title="",
                      margin=dict(l=10, r=10, t=20, b=10), height=430,
                      legend=dict(orientation="h", y=1.1))
    ok = bool(np.allclose(total[50:-50], T, atol=1e-6))
    return fig, ok


def render() -> None:
    st.title("Criterio de Nyquist para bases ortonormales")
    st.caption("Unidad 5 · Bixio §5.4 (págs. 167–170)")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u5_nyquist.md")

    with tg:
        st.subheader("El espectro plegado: Σₖ |ψF(f − k/T)|² ¿es constante = T?")
        st.caption(
            "Reproduce el test gráfico del libro (simetría de banda, Fig. 5.3, pág. 168): "
            "se dibujan |ψF|², sus réplicas cada 1/T y la suma (roja)."
        )
        c = st.columns(2)
        name = c[0].selectbox("Pulso", [
            "Coseno realzado", "Triángulo", "Rectángulo angosto (B < 1/2T)",
        ])
        beta = c[1].slider("β (si es coseno realzado)", 0.05, 1.0, 0.5, 0.05)

        fig, ok = _folding_figure(name, beta)
        render_plotly(fig)
        if ok:
            st.success("✅ La suma plegada es constante = T: el pulso **cumple** el criterio "
                       "de Nyquist (ortonormal a sus traslados en T).")
        else:
            st.error("❌ La suma plegada NO es constante: este pulso **no** cumple el criterio "
                     "(soporte menor al ancho de banda mínimo 1/2T ⇒ quedan huecos).")

    with ts:
        st.info(
            "El criterio se 'siente' en el hardware vía el ISI: un pulso que no lo cumple "
            "cierra el ojo (Lab 4, página **ISI y diagrama de ojo**)."
        )
