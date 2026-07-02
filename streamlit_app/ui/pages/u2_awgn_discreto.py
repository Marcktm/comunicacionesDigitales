"""Unidad 2 — Receptor para el canal AWGN de tiempo discreto."""
from __future__ import annotations

import streamlit as st

from core.modulation import qam4_constellation
from ui.components import diagrams
from ui.components.plots import render_plotly, voronoi_figure
from ui.components.theory import render_theory


def render() -> None:
    st.title("Receptor para el canal AWGN de tiempo discreto")
    st.caption("Unidad 2 · Bixio §2.4")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u2_awgn_discreto.md")

    with tg:
        st.subheader("Canal AWGN discreto (Fig. 2.5)")
        st.caption("El transmisor envía c_i; el canal suma ruido Z ~ N(0, σ²Iₙ); Y = c_i + Z.")
        diagrams.render(diagrams.awgn_discrete_diagram())

        st.divider()
        st.subheader("Regiones de decisión de mínima distancia (Voronoi)")
        st.caption(
            "Ejemplo 4-QAM: cada color es el conjunto de observaciones y más cercanas a ese c_i. "
            "La regla ML elige el punto más cercano; no necesita conocer σ²."
        )
        render_plotly(voronoi_figure(qam4_constellation(2.0)))

    with ts:
        st.info(
            "Modelo y regla de decisión (teórico/simulado). La transmisión real de una "
            "constelación sobre el Pluto se ve en **Unidad 4** y en el diagrama de ojo de "
            "**Unidad 5**."
        )
