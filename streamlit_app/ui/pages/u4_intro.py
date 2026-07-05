"""Unidad 4 — ¿Qué es un SDR? Arquitectura del ADALM-Pluto."""
from __future__ import annotations

import streamlit as st

from sdr import availability, session
from sdr.registry import ip, uri
from ui.components import diagrams
from ui.components.theory import render_theory


def render() -> None:
    st.title("¿Qué es un SDR? Arquitectura del ADALM-Pluto")
    st.caption("Unidad 4 · Radio definida por Software")

    tt, tg, ts = st.tabs(["📖 Teoría", "📈 Gráficas de ejemplo", "📡 Bonus SDR"])

    with tt:
        render_theory("u4_intro.md")

    with tg:
        st.subheader("Bloques del ADALM-Pluto (AD9363 + Zynq)")
        st.caption(
            "Reproduce el diagrama de bloques del apunte (Unidad 4): frontend RF (AD9363) y "
            "backend con Linux embebido (Zynq Z-7010), conectados a tu PC por VPN."
        )
        diagrams.render(diagrams.pluto_architecture_diagram())

        st.divider()
        st.subheader("Modos de loopback (0 = antena, 1 = digital, 2 = RF)")
        diagrams.render(diagrams.loopback_diagram())

    with ts:
        st.subheader("Probar la conexión con el SDR activo")
        name = session.get_active()
        st.write(f"SDR activo: **{name}** · `{uri(name)}`")
        if st.button("Probar conexión (puerto iiod)", width="stretch"):
            with st.spinner(f"Probando {ip(name)}…"):
                ok = availability.check_ip(ip(name))
            if ok:
                st.success(f"🟢 {name} responde en {ip(name)} — podés usarlo en los Labs.")
            else:
                st.error(
                    f"🔴 {name} no responde. Verificá la VPN (Cisco AnyConnect "
                    "200.16.19.5:443) o probá otro SDR con el selector de la izquierda."
                )
        st.caption(
            "Verificaciones equivalentes por terminal: `ping 192.168.1.3x` y "
            "`iio_info -u ip:192.168.1.3x` (lista los canales del AD9363)."
        )
