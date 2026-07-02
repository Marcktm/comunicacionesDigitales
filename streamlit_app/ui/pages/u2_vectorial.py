"""Unidad 2 — Decisión binaria con observaciones vectoriales (geometría)."""
from __future__ import annotations

import numpy as np
import streamlit as st

from core.distributions import q_function
from ui.components.plots import render_plotly, voronoi_figure
from ui.components.theory import render_theory


def render() -> None:
    st.title("Decisión binaria con observaciones vectoriales")
    st.caption("Unidad 2 · Bixio §2.4.2")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u2_vectorial.md")

    with tg:
        st.subheader("Plano afín de decisión en ℝ² (priori uniforme)")
        st.caption(
            "Mové las dos señales c₀ y c₁: la frontera es el bisector perpendicular "
            "(plano afín). Con priori uniforme, Pe = Q(d/2σ) sólo depende de la distancia d."
        )
        c = st.columns(4)
        x0 = c[0].slider("c₀ · x", -3.0, 3.0, -1.0, 0.1)
        y0 = c[1].slider("c₀ · y", -3.0, 3.0, -0.5, 0.1)
        x1 = c[2].slider("c₁ · x", -3.0, 3.0, 1.0, 0.1)
        y1 = c[3].slider("c₁ · y", -3.0, 3.0, 0.8, 0.1)
        sigma = st.slider("σ (ruido)", 0.1, 2.0, 0.6, 0.05)

        c0, c1 = complex(x0, y0), complex(x1, y1)
        d = abs(c1 - c0)
        if d < 1e-6:
            st.warning("c₀ y c₁ deben ser distintos.")
        else:
            render_plotly(voronoi_figure([c0, c1], labels=["c₀", "c₁"]))
            m = st.columns(2)
            m[0].metric("Distancia d = ‖c₁−c₀‖", f"{d:.3f}")
            m[1].metric("Pₑ = Q(d/2σ)", f"{float(q_function(d / (2 * sigma))):.3e}")
            st.caption(
                "Con priori no uniforme el plano se corre σ²·ln η / d hacia una de las señales "
                "(ver la derivación de p y q en la teoría)."
            )

    with ts:
        st.info(
            "Resultado geométrico (teórico). El caso vectorial modela múltiples antenas / slots "
            "de tiempo / frecuencias; la reducción a escalar muestra que **sólo importa la "
            "distancia d** entre señales."
        )
