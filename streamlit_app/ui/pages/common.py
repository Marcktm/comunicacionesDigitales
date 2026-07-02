"""Utilidades compartidas por las páginas (plantilla de 3 secciones, placeholder)."""
from __future__ import annotations

import streamlit as st


def render_placeholder(title: str, unit: str, note: str = "") -> None:
    """Página aún no autorada: muestra la plantilla de 3 secciones."""
    st.title(title)
    st.caption(f"{unit} · página en construcción")
    st.info(
        "Esta página seguirá la estructura de **3 secciones**:\n\n"
        "1. **Teoría** — demostración completa paso a paso (LaTeX/KaTeX), fiel al libro.\n"
        "2. **Gráficas de ejemplo** — figuras del libro generadas en vivo (interactivas).\n"
        "3. **Bonus SDR** — replicación real con el ADALM-Pluto (donde aplique)."
    )
    if note:
        st.write(note)
