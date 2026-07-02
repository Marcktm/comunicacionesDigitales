"""Unidad 1 — Repaso de probabilidad y variable aleatoria (explorador)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _make_dist(name):
    """Devuelve (dist_scipy, es_discreta) según la distribución y sus sliders."""
    if name == "Gaussiana":
        m = st.slider("media m", -5.0, 5.0, 0.0, 0.1)
        s = st.slider("σ", 0.2, 3.0, 1.0, 0.1)
        return stats.norm(m, s), False
    if name == "Uniforme":
        a = st.slider("a", -5.0, 4.0, -1.0, 0.1)
        b = st.slider("b", a + 0.1, 5.0, max(a + 0.1, 1.0), 0.1)
        return stats.uniform(a, b - a), False
    if name == "Exponencial":
        lam = st.slider("λ", 0.2, 3.0, 1.0, 0.1)
        return stats.expon(scale=1.0 / lam), False
    if name == "Laplaciana":
        mu = st.slider("μ", -5.0, 5.0, 0.0, 0.1)
        b = st.slider("b (escala)", 0.2, 3.0, 1.0, 0.1)
        return stats.laplace(mu, b), False
    if name == "Bernoulli":
        p = st.slider("p", 0.0, 1.0, 0.5, 0.05)
        return stats.bernoulli(p), True
    if name == "Binomial":
        n = st.slider("n", 1, 40, 10, 1)
        p = st.slider("p", 0.0, 1.0, 0.5, 0.05)
        return stats.binom(n, p), True
    # Poisson
    lam = st.slider("λ", 0.5, 20.0, 4.0, 0.5)
    return stats.poisson(lam), True


def _dist_figure(dist, discrete):
    if discrete:
        lo, hi = int(dist.ppf(0.001)), int(dist.ppf(0.999))
        x = np.arange(max(lo, 0), hi + 1)
        fig = go.Figure(go.Bar(x=x, y=dist.pmf(x), marker_color="#1f77b4"))
        ytitle = "pmf  p(x)"
    else:
        lo, hi = dist.ppf(0.001), dist.ppf(0.999)
        x = np.linspace(lo, hi, 400)
        fig = go.Figure(go.Scatter(x=x, y=dist.pdf(x), mode="lines",
                                   line=dict(color="#1f77b4", width=3)))
        ytitle = "pdf  f(x)"
    fig.update_layout(xaxis_title="x", yaxis_title=ytitle,
                      margin=dict(l=10, r=10, t=20, b=10), height=400)
    return fig


def render() -> None:
    st.title("Repaso de probabilidad y variable aleatoria")
    st.caption("Unidad 1 · Roy Yates")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u1_probabilidad.md")

    with tg:
        st.subheader("Explorador de distribuciones")
        name = st.selectbox("Distribución", [
            "Gaussiana", "Uniforme", "Exponencial", "Laplaciana",
            "Bernoulli", "Binomial", "Poisson",
        ])
        dist, discrete = _make_dist(name)
        render_plotly(_dist_figure(dist, discrete))
        m = st.columns(2)
        m[0].metric("E[X]", f"{float(dist.mean()):.3f}")
        m[1].metric("Var(X)", f"{float(dist.var()):.3f}")

    with ts:
        st.info(
            "Repaso teórico. La **gaussiana** modela el ruido térmico del receptor (verificado "
            "sobre el Pluto en **Unidad 4**); la **Poisson**, el conteo de fotones (canal óptico)."
        )
