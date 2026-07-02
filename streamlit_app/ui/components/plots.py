"""Helpers de gráficos Plotly reutilizables por las páginas."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from core.distributions import gaussian_pdf


def render_plotly(fig) -> None:
    """Muestra una figura Plotly a lo ancho del contenedor.

    Punto único de configuración: en Streamlit 1.50 ``st.plotly_chart`` usa
    ``use_container_width`` (no tiene ``width``); centralizarlo evita repetir el
    detalle y facilita migrar cuando la API se estabilice.
    """
    st.plotly_chart(fig, use_container_width=True)


def decision_regions_figure(c0, c1, sigma, p0, theta):
    """Densidades ponderadas P_H(i)·f(y|i), umbral θ y áreas de error sombreadas.

    Reproduce la Figura 2.6 del Bixio (decisión binaria en canal AWGN escalar).
    """
    p1 = 1.0 - p0
    lo = min(c0, c1) - 4 * sigma
    hi = max(c0, c1) + 4 * sigma
    y = np.linspace(lo, hi, 800)

    f0 = p0 * gaussian_pdf(y, c0, sigma**2)
    f1 = p1 * gaussian_pdf(y, c1, sigma**2)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=y, y=f0, mode="lines", name="P₀·f(y|H=0)",
                             line=dict(color="#2ca02c")))
    fig.add_trace(go.Scatter(x=y, y=f1, mode="lines", name="P₁·f(y|H=1)",
                             line=dict(color="#d62728")))

    # Región de error para H=0 (se decide 1): cola de f0 del lado de decisión "1".
    if c1 >= c0:
        m0 = y >= theta
        m1 = y <= theta
    else:
        m0 = y <= theta
        m1 = y >= theta
    fig.add_trace(go.Scatter(x=y[m0], y=f0[m0], fill="tozeroy", mode="none",
                             name="error | H=0", fillcolor="rgba(44,160,44,0.35)"))
    fig.add_trace(go.Scatter(x=y[m1], y=f1[m1], fill="tozeroy", mode="none",
                             name="error | H=1", fillcolor="rgba(214,39,40,0.35)"))

    fig.add_vline(x=theta, line_dash="dash", line_color="#333",
                  annotation_text="θ", annotation_position="top")
    fig.add_vline(x=c0, line_dash="dot", line_color="#2ca02c",
                  annotation_text="c₀", annotation_position="bottom")
    fig.add_vline(x=c1, line_dash="dot", line_color="#d62728",
                  annotation_text="c₁", annotation_position="bottom")

    fig.update_layout(
        xaxis_title="y (observable)",
        yaxis_title="densidad ponderada",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=30, b=10),
        height=420,
    )
    return fig


def q_curve_figure(sigma_range, c0, c1):
    """Curva Pe = Q(d/2σ) vs σ (escala log en Pe)."""
    from core.distributions import q_function

    d = abs(c1 - c0)
    sigma = np.asarray(sigma_range, dtype=float)
    pe = q_function(d / (2.0 * sigma))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sigma, y=pe, mode="lines", name="Pe = Q(d/2σ)"))
    fig.update_layout(
        xaxis_title="σ (desvío del ruido)",
        yaxis_title="Pe",
        yaxis_type="log",
        margin=dict(l=10, r=10, t=30, b=10),
        height=360,
    )
    return fig


def q_function_figure(alpha_max=5.0):
    """Q(α) con sus cotas (Bixio, propiedad 4 y cota simple), en escala log."""
    from core.distributions import q_bound_simple, q_bounds, q_function

    a = np.linspace(0.05, alpha_max, 500)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a, y=q_function(a), name="Q(α)",
                             line=dict(color="#1f77b4", width=3)))
    lo, hi = q_bounds(a)
    fig.add_trace(go.Scatter(x=a, y=hi, name="cota superior", line=dict(dash="dash")))
    fig.add_trace(go.Scatter(x=a, y=lo, name="cota inferior", line=dict(dash="dot")))
    fig.add_trace(go.Scatter(x=a, y=q_bound_simple(a), name="½·e^(−α²/2)",
                             line=dict(dash="dashdot")))
    fig.update_layout(
        xaxis_title="α", yaxis_title="Q(α)", yaxis_type="log",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=10, r=10, t=30, b=10), height=440,
    )
    return fig


def pam_constellation_figure(m, d=2.0):
    """Constelación m-PAM sobre la recta con las fronteras de decisión (Fig. 2.9)."""
    from core.modulation import pam_constellation

    pts = pam_constellation(m, d)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=pts, y=np.zeros_like(pts), mode="markers+text",
        text=[f"c{i}" for i in range(m)], textposition="top center",
        marker=dict(size=14, color="#1f77b4"), name="constelación",
    ))
    for i in range(m - 1):  # fronteras de decisión (punto medio entre vecinos)
        fig.add_vline(x=(pts[i] + pts[i + 1]) / 2.0, line_dash="dot", line_color="#bbb")
    fig.update_layout(
        xaxis_title="c", yaxis=dict(visible=False, range=[-1, 1]),
        showlegend=False, margin=dict(l=10, r=10, t=20, b=10), height=220,
    )
    return fig


def qam4_figure(d=2.0):
    """Constelación 4-QAM en el plano con las fronteras (ejes) de decisión (Fig. 2.10)."""
    from core.modulation import qam4_constellation

    c = qam4_constellation(d)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=c.real, y=c.imag, mode="markers+text",
        text=[f"c{i}" for i in range(4)], textposition="top center",
        marker=dict(size=16, color="#1f77b4"),
    ))
    fig.add_hline(y=0, line_dash="dot", line_color="#bbb")
    fig.add_vline(x=0, line_dash="dot", line_color="#bbb")
    fig.update_layout(
        xaxis_title="ψ₁", yaxis_title="ψ₂",
        yaxis=dict(scaleanchor="x", scaleratio=1),
        margin=dict(l=10, r=10, t=20, b=10), height=400, showlegend=False,
    )
    return fig


def voronoi_figure(constellation, labels=None, n=280, title=None):
    """Regiones de decisión (Voronoi) de una constelación en el plano (Fig. 2.8 / 2.3).

    Colorea el plano según el punto más cercano (regla ML de mínima distancia) y
    superpone la constelación. Sirve para el caso binario (plano afín, Fig. 2.7) y
    para constelaciones m-arias (QAM, PSK, …).
    """
    import plotly.colors as pc

    from core.decision import nearest_index

    c = np.asarray(constellation, dtype=complex)
    r = float(np.max(np.abs(c))) * 1.7 + 1.0
    axis = np.linspace(-r, r, n)
    X, Y = np.meshgrid(axis, axis)
    idx = nearest_index(X + 1j * Y, c)

    # Colorscale DISCRETO (una banda por región) a partir de una paleta cualitativa.
    palette = pc.qualitative.Pastel
    mcount = len(c)
    scale = []
    for i in range(mcount):
        col = palette[i % len(palette)]
        scale.append([i / mcount, col])
        scale.append([(i + 1) / mcount, col])

    labels = labels or [f"c{i}" for i in range(mcount)]
    fig = go.Figure()
    fig.add_trace(go.Heatmap(
        x=axis, y=axis, z=idx, showscale=False, colorscale=scale,
        zmin=-0.5, zmax=mcount - 0.5, opacity=0.55, hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=c.real, y=c.imag, mode="markers+text", text=labels,
        textposition="top center", marker=dict(size=13, color="#111"),
    ))
    fig.update_layout(
        xaxis_title="ψ₁", yaxis_title="ψ₂", title=title,
        yaxis=dict(scaleanchor="x", scaleratio=1),
        margin=dict(l=10, r=10, t=30, b=10), height=440, showlegend=False,
    )
    return fig

