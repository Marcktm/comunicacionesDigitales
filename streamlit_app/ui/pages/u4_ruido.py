"""Unidad 4 — Lab 2: caracterización de ruido del receptor (con bonus real)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy.signal import welch

from core.distributions import gaussian_pdf
from sdr import availability, session
from sdr.registry import ip, uri
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _noise_analysis_figs(iq, fs, title=""):
    """Pipeline del Lab 2: histogramas I/Q + pdf gaussiana, y PSD (Welch)."""
    i, q = np.real(iq), np.imag(iq)

    fig_h = make_subplots(rows=1, cols=2, subplot_titles=("componente I", "componente Q"))
    for col, comp in ((1, i), (2, q)):
        fig_h.add_histogram(x=comp, histnorm="probability density", nbinsx=80,
                            row=1, col=col, showlegend=False, marker_color="#1f77b4")
        xs = np.linspace(comp.min(), comp.max(), 200)
        fig_h.add_scatter(x=xs, y=gaussian_pdf(xs, comp.mean(), comp.var()),
                          mode="lines", line=dict(color="#d62728", width=3),
                          row=1, col=col, showlegend=False)
    fig_h.update_layout(title=f"{title}histogramas + pdf gaussiana (media/var muestrales)",
                        margin=dict(l=10, r=10, t=60, b=10), height=360)

    f, pxx = welch(iq, fs=fs, nperseg=min(4096, len(iq)), return_onesided=False)
    order = np.argsort(f)
    fig_p = go.Figure(go.Scatter(x=f[order] / 1e3, y=10 * np.log10(pxx[order] + 1e-20),
                                 mode="lines"))
    fig_p.update_layout(title=f"{title}PSD (Welch) — debe ser plana en banda",
                        xaxis_title="f [kHz]", yaxis_title="PSD [dB/Hz]",
                        margin=dict(l=10, r=10, t=40, b=10), height=320)
    return fig_h, fig_p


def _stats_row(iq):
    i, q = np.real(iq), np.imag(iq)
    m = st.columns(4)
    m[0].metric("media I", f"{i.mean():+.4f}")
    m[1].metric("media Q", f"{q.mean():+.4f}")
    m[2].metric("var I", f"{i.var():.4f}")
    m[3].metric("var Q", f"{q.var():.4f}")


def render() -> None:
    st.title("Lab 2 — Caracterización del ruido del receptor")
    st.caption("Unidad 4 · notebook laboratorio2.ipynb · valida el modelo AWGN")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR (real)"])

    with tt:
        render_theory("u4_ruido.md")

    with tg:
        st.subheader("El pipeline de análisis, sobre ruido gaussiano simulado")
        st.caption(
            "Igual que la sección de simulación del notebook: se genera ruido complejo "
            "gaussiano y se le aplica el MISMO análisis que a la captura real (histogramas + "
            "pdf, PSD plana). Sirve de referencia de 'cómo debería verse'."
        )
        sigma = st.slider("σ por componente", 0.1, 2.0, 0.5, 0.1)
        rng = np.random.default_rng(0)
        n = 2**16
        iq = rng.normal(0, sigma, n) + 1j * rng.normal(0, sigma, n)
        _stats_row(iq)
        fig_h, fig_p = _noise_analysis_figs(iq, fs=2e6, title="simulado: ")
        render_plotly(fig_h)
        render_plotly(fig_p)

    with ts:
        st.subheader("Capturar ruido real del Pluto (requiere VPN)")
        st.caption(
            "TX en silencio (−89 dB, ceros), TX y RX en portadoras separadas "
            "(2400 / 915 MHz), ganancia RX manual. Se captura y se corre el mismo pipeline."
        )
        name = session.get_active()
        st.write(f"SDR activo: **{name}** · `{uri(name)}`")
        rx_gain = st.slider("Ganancia RX manual [dB]", 0, 70, 70, 5)

        if st.button("▶ Capturar ruido y analizar", width="stretch"):
            if not availability.check_ip(ip(name)):
                st.error(
                    f"🔴 {name} no responde ({ip(name)}). Conectá la VPN o elegí otro SDR."
                )
            else:
                try:
                    from usecases.sdr_experiments import capture_noise

                    with st.spinner(f"Capturando ruido en {name}…"):
                        iq = capture_noise(name, rx_gain=int(rx_gain))
                    st.success(f"Capturadas {len(iq)} muestras de ruido.")
                    _stats_row(iq)
                    fig_h, fig_p = _noise_analysis_figs(iq, fs=2e6, title="real: ")
                    render_plotly(fig_h)
                    render_plotly(fig_p)
                    st.caption(
                        "Si el histograma calza con la gaussiana y la PSD es plana en banda, "
                        "el modelo AWGN de las Unidades 2/3 queda validado sobre tu hardware."
                    )
                except ImportError:
                    st.error(
                        "pyadi-iio no está instalado en esta máquina. "
                        "Instalá `libiio` (brew install libiio) y `pip install pyadi-iio`."
                    )
                except Exception as exc:
                    st.error(f"Error hablando con el SDR: {type(exc).__name__}: {exc}")
