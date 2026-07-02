"""Estado global del SDR activo, guardado en ``st.session_state``.

Es el único módulo de la capa ``sdr`` que toca Streamlit: mantiene qué SDR está
seleccionado y el último resultado del chequeo de disponibilidad, de modo que la
elección persista al navegar entre páginas.
"""
from __future__ import annotations

import streamlit as st

from .registry import SDR_DEVICES

_ACTIVE = "sdr_active"
_AVAIL = "sdr_availability"


def get_active() -> str:
    return st.session_state.get(_ACTIVE, next(iter(SDR_DEVICES)))


def set_active(name: str) -> None:
    st.session_state[_ACTIVE] = name


def get_availability() -> dict[str, bool]:
    return st.session_state.get(_AVAIL, {})


def set_availability(mapping: dict[str, bool]) -> None:
    st.session_state[_AVAIL] = mapping
