"""Unidad 2 — Prueba de hipótesis M-aria (regiones de Voronoi, union bound)."""
from __future__ import annotations

import streamlit as st

from core.modulation import (
    avg_min_neighbors,
    nearest_neighbor_pe,
    psk_constellation,
    qam_square_constellation,
    union_bound_pe,
)
from ui.components.plots import render_plotly, voronoi_figure
from ui.components.theory import render_theory

_CONSTELLATIONS = {
    "4-QAM": lambda: qam_square_constellation(4, d=2.0),
    "16-QAM": lambda: qam_square_constellation(16, d=2.0),
    "4-PSK (QPSK)": lambda: psk_constellation(4, radius=1.5),
    "8-PSK": lambda: psk_constellation(8, radius=1.5),
}


def render() -> None:
    st.title("Prueba de hipótesis M-aria")
    st.caption("Unidad 2 · Bixio §2.2.2 y §2.4.3")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u2_m_aria.md")

    with tg:
        st.subheader("Regiones de decisión (Voronoi) y cotas de Pe")
        c = st.columns(2)
        name = c[0].selectbox("Constelación", list(_CONSTELLATIONS))
        sigma = c[1].slider("σ (ruido)", 0.1, 1.5, 0.4, 0.05)

        const = _CONSTELLATIONS[name]()
        render_plotly(voronoi_figure(const, title=f"{name} — {len(const)} símbolos"))

        nmin, dmin = avg_min_neighbors(const)
        m = st.columns(3)
        m[0].metric("d_min", f"{dmin:.3f}")
        m[1].metric("Pₑ (cota de unión)", f"{union_bound_pe(const, sigma):.3e}")
        m[2].metric("Pₑ (vecinos ≈)", f"{nearest_neighbor_pe(const, sigma):.3e}")
        st.caption(
            f"N_min ≈ {nmin:.2f} vecinos a distancia mínima. La aproximación de vecinos más "
            "cercanos, N_min·Q(d_min/2σ), suele ser muy ajustada a SNR alta."
        )

    with ts:
        st.info(
            "Decisión m-aria (teórico/simulado). La transmisión real de constelaciones (QPSK) "
            "sobre el Pluto aparece en **Unidad 4**."
        )
