"""Unidad 5 — ISI y diagrama de ojo (simulado + Lab 4 real sobre el Pluto)."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from core.eye import eye_traces
from core.modulation import bpsk_symbols, random_bits
from core.pulses import rrc_taps
from sdr import availability, session
from sdr.registry import ip, uri
from ui.components.theory import render_theory


def _eye_figure(signal, sps, title):
    """Diagrama de ojo con Matplotlib (overlay de trazas con transparencia)."""
    traces = eye_traces(np.real(signal), sps, span_symbols=2, max_traces=180)
    fig, ax = plt.subplots(figsize=(7.5, 4))
    x = np.arange(traces.shape[1]) / sps - 1.0        # eje en unidades de T
    for tr in traces:
        ax.plot(x, tr, color="C0", alpha=0.18, lw=1)
    ax.axvline(0.0, color="C3", ls="--", lw=1.2, label="instante de muestreo")
    ax.set_xlabel("t / T")
    ax.set_ylabel("salida del matched filter")
    ax.set_title(title)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(alpha=0.3)
    return fig


def _simulated_eye(beta, span, sigma, sps=8, num_bits=600, seed=2):
    """Cadena BPSK + RRC (TX) + AWGN + RRC (RX) para el ojo simulado."""
    rng = np.random.default_rng(seed)
    symbols = bpsk_symbols(random_bits(num_bits, seed=seed)).astype(float)
    ups = np.zeros(num_bits * sps)
    ups[::sps] = symbols
    taps = rrc_taps(sps, span, beta)
    tx = np.convolve(ups, taps)
    rx = tx + rng.normal(0.0, sigma, size=tx.shape)
    mf = np.convolve(rx, taps)
    # descartar transitorios de los filtros
    delay = len(taps) - 1
    return mf[delay: -delay if delay else None]


def render() -> None:
    st.title("ISI y diagrama de ojo (Lab 4)")
    st.caption("Unidad 5 · Bixio §5.6 (págs. 172–174) · Lab 4 del repo")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR (Lab 4 real)"])

    with tt:
        render_theory("u5_ojo.md")

    with tg:
        st.subheader("Diagrama de ojo simulado (reproduce la Fig. 5.9 del libro, pág. 173)")
        st.caption(
            "Cadena BPSK → RRC(TX) → AWGN → RRC(RX). Jugá con β, el truncado (span) y el "
            "ruido: β chico + span corto ⇒ ISI (cierre vertical); ruido ⇒ trazas gruesas."
        )
        c = st.columns(3)
        beta = c[0].slider("β", 0.05, 1.0, 0.25, 0.05)
        span = c[1].select_slider("span (símbolos)", options=[4, 6, 8, 12, 20], value=12)
        sigma = c[2].slider("σ del ruido", 0.0, 0.5, 0.05, 0.01)

        mf = _simulated_eye(beta, int(span), sigma)
        st.pyplot(_eye_figure(mf, 8, f"ojo simulado — β={beta:.2f}, span={span}T, σ={sigma:.2f}"))

    with ts:
        st.subheader("El experimento del Lab 4 sobre el Pluto (requiere VPN)")
        name = session.get_active()
        st.write(f"SDR activo: **{name}** · `{uri(name)}`")
        c = st.columns(4)
        beta_r = c[0].slider("β (RRC)", 0.25, 1.0, 1.0, 0.25)
        span_r = c[1].select_slider("span", options=[4, 6, 8, 12], value=12)
        loop = c[2].selectbox("loopback", [1, 2, 0],
                              format_func=lambda v: {0: "0 · antena", 1: "1 · digital",
                                                     2: "2 · RF"}[v])
        atten = c[3].slider("TxAtten [dB]", -70, -10, -30, 5)

        if st.button("▶ Transmitir y armar el ojo", width="stretch"):
            if not availability.check_ip(ip(name)):
                st.error(f"🔴 {name} no responde ({ip(name)}). VPN o elegí otro SDR.")
            else:
                try:
                    from usecases.eye_experiment import run_sdr_eye_case

                    with st.spinner(f"TX/RX en {name} (loopback={loop})…"):
                        res = run_sdr_eye_case(
                            name, beta=beta_r, span=int(span_r),
                            loopback=int(loop), tx_atten=int(atten),
                        )
                    st.success(f"Capturado. Componente I de la salida del matched filter:")
                    st.pyplot(_eye_figure(
                        res["mf"], res["sps"],
                        f"ojo real — β={beta_r}, span={span_r}T, loopback={loop}, "
                        f"TxAtten={atten} dB",
                    ))
                    st.caption(
                        "Bajá TxAtten hacia −70 dB y mirá cómo la SNR cae y el ojo se "
                        "cierra; probá loopback 0 (antena) para ver el canal real."
                    )
                except ImportError:
                    st.error(
                        "pyadi-iio no está instalado. `brew install libiio` + "
                        "`pip install pyadi-iio`."
                    )
                except Exception as exc:
                    st.error(f"Error hablando con el SDR: {type(exc).__name__}: {exc}")
