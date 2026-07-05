"""Unidad 4 — Lab 1: configurar el SDR y transmitir un tono (con bonus real)."""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.signal import welch

from core.modulation import complex_exp
from sdr import availability, session
from sdr.registry import ip, uri
from ui.components.plots import render_plotly
from ui.components.theory import render_theory


def _iq_and_psd_figs(x, fs, title_prefix=""):
    """Figuras I/Q en el tiempo (primeras muestras) y PSD por Welch."""
    x = np.asarray(x)
    fig_t = go.Figure()
    nshow = min(400, len(x))
    fig_t.add_scatter(y=x.real[:nshow], mode="lines", name="I")
    fig_t.add_scatter(y=x.imag[:nshow], mode="lines", name="Q", line=dict(dash="dash"))
    fig_t.update_layout(title=f"{title_prefix}componentes I/Q (primeras {nshow} muestras)",
                        xaxis_title="n", yaxis_title="amplitud",
                        margin=dict(l=10, r=10, t=40, b=10), height=320,
                        legend=dict(orientation="h", y=1.12))

    f, pxx = welch(x, fs=fs, nperseg=min(4096, len(x)), return_onesided=False)
    order = np.argsort(f)
    fig_f = go.Figure(go.Scatter(x=f[order] / 1e3, y=10 * np.log10(pxx[order] + 1e-20),
                                 mode="lines"))
    fig_f.update_layout(title=f"{title_prefix}PSD (Welch)",
                        xaxis_title="f [kHz]", yaxis_title="PSD [dB/Hz]",
                        margin=dict(l=10, r=10, t=40, b=10), height=320)
    return fig_t, fig_f


def render() -> None:
    st.title("Lab 1 — Configurar el SDR y transmitir un tono")
    st.caption("Unidad 4 · notebook *How To Config SDR*")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR (real)"])

    with tt:
        render_theory("u4_config.md")

    with tg:
        st.subheader("La señal del Lab 1, simulada (sin hardware)")
        st.caption(
            "La exponencial compleja con Fc = Fs/8: I y Q en cuadratura y una sola raya "
            "espectral. Es exactamente lo que deberías ver del lado RX si el lazo funciona."
        )
        fs = 2.0e6
        x = complex_exp(2**14, Fc=fs / 8, Fs=fs)
        fig_t, fig_f = _iq_and_psd_figs(x, fs)
        render_plotly(fig_t)
        render_plotly(fig_f)

    with ts:
        st.subheader("Ejecutar el Lab 1 en el Pluto (requiere VPN)")
        name = session.get_active()
        st.write(f"SDR activo: **{name}** · `{uri(name)}`")
        c = st.columns(3)
        lo_mhz = c[0].number_input("Portadora [MHz]", 325.0, 3800.0, 915.0, 5.0)
        atten = c[1].slider("Atenuación TX [dB]", -80, 0, -30, 1)
        fs_mhz = c[2].select_slider("Fs [MHz]", options=[1.0, 2.0, 4.0], value=2.0)

        if st.button("▶ Transmitir tono y capturar", width="stretch"):
            if not availability.check_ip(ip(name)):
                st.error(
                    f"🔴 {name} no responde ({ip(name)}). Conectá la VPN o elegí otro SDR "
                    "en el selector de la izquierda."
                )
            else:
                try:
                    from usecases.sdr_experiments import tx_rx_tone

                    with st.spinner(f"TX/RX en {name}…"):
                        res = tx_rx_tone(
                            name, sample_rate=fs_mhz * 1e6,
                            lo_freq=lo_mhz * 1e6, tx_atten=int(atten),
                        )
                    st.success(
                        f"Capturadas {len(res['rx'])} muestras. El pico de la PSD debería "
                        f"estar en Fc = Fs/8 = {res['fc']/1e3:.0f} kHz."
                    )
                    fig_t, fig_f = _iq_and_psd_figs(res["rx"], res["fs"], "RX real: ")
                    render_plotly(fig_t)
                    render_plotly(fig_f)
                except ImportError:
                    st.error(
                        "pyadi-iio no está instalado en esta máquina. "
                        "Instalá `libiio` (brew install libiio) y `pip install pyadi-iio`."
                    )
                except Exception as exc:
                    st.error(f"Error hablando con el SDR: {type(exc).__name__}: {exc}")
