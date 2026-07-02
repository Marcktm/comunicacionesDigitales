"""Unidad 2 — La función Q (propiedades, cotas y figura fiel al libro)."""
from __future__ import annotations

import streamlit as st

from core.distributions import q_function
from ui.components.plots import q_function_figure, render_plotly
from ui.components.theory import render_theory


def render() -> None:
    st.title("La función Q")
    st.caption("Unidad 2 · Bixio §2.3")

    tab_teoria, tab_graf, tab_sdr = st.tabs(
        ["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"]
    )

    with tab_teoria:
        render_theory("u2_funcion_q.md")

    with tab_graf:
        st.subheader("Q(α) y sus cotas (escala logarítmica)")
        alpha_max = st.slider("α máximo", 2.0, 8.0, 5.0, 0.5)
        render_plotly(q_function_figure(alpha_max))
        st.caption(
            "Q(α) con la cota superior/inferior (propiedad 4) y la cota simple ½·e^(−α²/2). "
            "En las colas (α grande) las cotas se pegan a Q."
        )

        st.divider()
        st.subheader("Calculadora: Pr{Z ≥ x} con Z ~ N(m, σ²)")
        c = st.columns(3)
        x = c[0].number_input("x", value=0.2, step=0.1, format="%.3f")
        m = c[1].number_input("media m", value=0.0, step=0.1, format="%.3f")
        sigma = c[2].number_input("σ", value=1.0, min_value=1e-6, step=0.1, format="%.3f")
        z = (x - m) / sigma
        st.latex(rf"\Pr\{{Z \ge {x:g}\}} = Q\!\left(\frac{{{x:g}-{m:g}}}{{{sigma:g}}}\right) "
                 rf"= Q({z:.4f}) = {float(q_function(z)):.6f}")

    with tab_sdr:
        st.info(
            "Herramienta matemática (sin hardware). Se usa para calcular la probabilidad de error "
            "de todos los esquemas de modulación de las unidades siguientes."
        )
