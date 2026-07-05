"""Unidad 3 — Ruido gaussiano blanco N(t) (definición y Lema)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from core.distributions import gaussian_pdf
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _project_noise(n0_half, trials, seed=0):
    """Proyecta ruido blanco discreto sobre dos funciones ortonormales (rects disjuntos).

    Devuelve Z1, Z2 ~ iid N(0, N0/2) según el Lema (Bixio §3.2).
    """
    rng = np.random.default_rng(seed)
    n, dt = 400, 1.0 / 400.0
    t = np.arange(n) * dt
    g1 = np.where(t < 0.5, np.sqrt(2.0), 0.0)   # ortonormales: ‖g‖²=1, ⟨g1,g2⟩=0
    g2 = np.where(t >= 0.5, np.sqrt(2.0), 0.0)
    # ruido blanco discreto con PSD N0/2  ⇔  var por muestra = (N0/2)/dt
    noise = rng.normal(0.0, np.sqrt(n0_half / dt), size=(trials, n))
    # errstate: matmul emite warnings espurios con Accelerate BLAS (macOS ARM)
    with np.errstate(all="ignore"):
        z1 = noise @ g1 * dt
        z2 = noise @ g2 * dt
    return z1, z2


def render() -> None:
    st.title("Ruido gaussiano blanco N(t)")
    st.caption("Unidad 3 · Bixio §3.2 (págs. 97–99)")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u3_ruido_blanco.md")

    with tg:
        st.subheader("Verificación del Lema: proyecciones sobre funciones ortonormales")
        st.caption(
            "Se proyecta ruido blanco sobre dos funciones ortonormales g₁, g₂ "
            "(rectángulos disjuntos). El Lema predice Z₁, Z₂ iid N(0, N₀/2)."
        )
        c = st.columns(2)
        n0_half = c[0].slider("N₀/2", 0.1, 2.0, 0.5, 0.1)
        trials = c[1].select_slider("realizaciones", options=[2000, 10000, 50000], value=10000)

        z1, z2 = _project_noise(n0_half, int(trials))

        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=("Z₁ vs Z₂ (incorrelación)", "histograma de Z₁"))
        fig.add_scatter(x=z1[:3000], y=z2[:3000], mode="markers",
                        marker=dict(size=3, opacity=0.3), row=1, col=1, showlegend=False)
        fig.add_histogram(x=z1, histnorm="probability density", nbinsx=60,
                          row=1, col=2, showlegend=False, marker_color="#1f77b4")
        xs = np.linspace(z1.min(), z1.max(), 200)
        fig.add_scatter(x=xs, y=gaussian_pdf(xs, 0.0, n0_half), mode="lines",
                        line=dict(color="#d62728", width=3), row=1, col=2,
                        name="N(0, N₀/2)")
        fig.update_xaxes(title_text="Z₁", row=1, col=1)
        fig.update_yaxes(title_text="Z₂", row=1, col=1)
        fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=420,
                          showlegend=False)
        render_plotly(fig)

        m = st.columns(3)
        m[0].metric("var(Z₁) medida", f"{np.var(z1):.4f}")
        m[1].metric("N₀/2 (teórico)", f"{n0_half:.4f}")
        m[2].metric("corr(Z₁,Z₂)", f"{np.corrcoef(z1, z2)[0,1]:+.4f}")

    with ts:
        st.info(
            "La **caracterización de ruido real** del receptor Pluto (Lab 2: capturar con TX "
            "silencioso, histogramas I/Q, Q-Q plots, PSD plana) está en **Unidad 4 · "
            "Caracterización de ruido** — es la verificación experimental de esta definición."
        )
