"""Sidebar global: selección de SDR + estado de disponibilidad/VPN.

Se renderiza en cada rerun (desde ``app.py``, antes de ``nav.run()``), así el
selector aparece en todas las páginas y la elección persiste vía session_state.
"""
from __future__ import annotations

import streamlit as st

from sdr import availability, session
from sdr.registry import SDR_DEVICES, uri


def _label(name: str, avail: dict[str, bool]) -> str:
    ip = SDR_DEVICES[name]
    if not avail:
        mark = "❔"          # todavía no se chequeó
    else:
        mark = "🟢" if avail.get(name) else "🔴"
    return f"{mark} {name} · {ip}"


def render_sdr_sidebar() -> None:
    with st.sidebar:
        st.header("📡 SDR / Conexión")
        st.caption(
            "Conectá la VPN (Cisco AnyConnect: 200.16.19.5:443) **antes** de usar "
            "el SDR. Luego chequeá disponibilidad y elegí un dispositivo."
        )

        avail = session.get_availability()
        if st.button("🔄 Chequear disponibilidad", width="stretch"):
            with st.spinner("Probando los 5 SDR…"):
                avail = availability.check_all()
                session.set_availability(avail)

        names = list(SDR_DEVICES)
        active = session.get_active()
        idx = names.index(active) if active in names else 0
        chosen = st.radio(
            "SDR activo",
            names,
            index=idx,
            format_func=lambda n: _label(n, avail),
        )
        session.set_active(chosen)
        st.caption(f"URI: `{uri(chosen)}`")

        if avail and not avail.get(chosen, False):
            st.warning(
                "Este SDR no responde. Elegí otro disponible (🟢) o volvé a chequear."
            )
        elif not avail:
            st.info("Todavía no se chequeó la disponibilidad de los SDR.")

        st.divider()
        st.caption(
            "El SDR es un **bonus**: las páginas de teoría y las gráficas de ejemplo "
            "funcionan sin hardware."
        )
