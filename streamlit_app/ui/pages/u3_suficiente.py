"""Unidad 3 — Estadística suficiente y canal discreto equivalente (Fig. 3.3 en 3D)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _fig33(ci=(1.6, 0.9), z_in=(0.5, -0.4), z_perp=1.0):
    """Reproduce la geometría de la Fig. 3.3: plano V, señal c_i, Y = c_i + Z|V y Z⊥V."""
    cx, cy = ci
    zx, zy = z_in
    yx, yy = cx + zx, cy + zy

    fig = go.Figure()
    # plano V (z = 0)
    grid = np.linspace(-0.5, 3.0, 2)
    X, Y = np.meshgrid(grid, grid)
    fig.add_surface(x=X, y=Y, z=np.zeros_like(X), opacity=0.25, showscale=False,
                    colorscale=[[0, "#9ecae1"], [1, "#9ecae1"]])

    def arrow(p0, p1, color, name):
        fig.add_scatter3d(x=[p0[0], p1[0]], y=[p0[1], p1[1]], z=[p0[2], p1[2]],
                          mode="lines+text", line=dict(color=color, width=6),
                          text=["", name], textposition="top center",
                          textfont=dict(size=14), showlegend=False)

    arrow((0, 0, 0), (cx, cy, 0), "#111", "c_i")
    arrow((cx, cy, 0), (yx, yy, 0), "#2ca02c", "Z|V")
    arrow((0, 0, 0), (yx, yy, 0), "#1f77b4", "Y")
    arrow((yx, yy, 0), (yx, yy, z_perp), "#d62728", "Z⊥V")
    arrow((0, 0, 0), (yx, yy, z_perp), "#7f7f7f", "(Yᵀ,Uᵀ)ᵀ")
    fig.add_scatter3d(x=[0], y=[0], z=[0], mode="markers+text", text=["0"],
                      marker=dict(size=4, color="#111"), showlegend=False)

    fig.update_layout(
        scene=dict(
            xaxis_title="ψ₁", yaxis_title="ψ₂", zaxis_title="⊥ V",
            zaxis=dict(range=[-0.2, 1.6]),
            camera=dict(eye=dict(x=1.6, y=-1.6, z=0.9)),
        ),
        margin=dict(l=0, r=0, t=20, b=0), height=520,
    )
    return fig


def render() -> None:
    st.title("Estadística suficiente y canal discreto equivalente")
    st.caption("Unidad 3 · Bixio §3.3 (págs. 99–102)")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u3_suficiente.md")

    with tg:
        st.subheader("Geometría de la proyección (Fig. 3.3 del libro, pág. 101)")
        st.caption(
            "El plano celeste es el espacio de señales V. La señal recibida completa "
            "(Yᵀ,Uᵀ)ᵀ se descompone en Y = c_i + Z|V (dentro de V, azul) y Z⊥V "
            "(perpendicular, rojo: sólo ruido, irrelevante). Podés rotar la figura."
        )
        c = st.columns(3)
        zx = c[0].slider("Z|V · ψ₁", -1.0, 1.0, 0.5, 0.1)
        zy = c[1].slider("Z|V · ψ₂", -1.0, 1.0, -0.4, 0.1)
        zp = c[2].slider("‖Z⊥V‖", 0.0, 1.5, 1.0, 0.1)
        render_plotly(_fig33(z_in=(zx, zy), z_perp=zp))
        st.caption(
            "Mové los sliders: Y se mueve **dentro** del plano; Z⊥V sólo lo saca del plano y "
            "no depende de la hipótesis ⇒ se descarta sin perder información (Fisher–Neyman)."
        )

    with ts:
        st.info(
            "Este resultado justifica que el receptor del SDR trabaje con **muestras** (la "
            "proyección) y no con la forma de onda continua: el n-tuple former del Pluto es su "
            "ADC + filtrado. Se retoma en **Unidad 5** con el teorema de muestreo."
        )
