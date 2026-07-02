"""Carga y renderizado de teoría en Markdown + LaTeX (KaTeX de Streamlit).

Las demostraciones viven en ``ui/content/*.md`` (un archivo por página) para
separar el contenido del código. Streamlit renderiza ``$...$`` y ``$$...$$`` con
KaTeX (integrales, sumatorias, \\begin{cases}, \\begin{aligned}, matrices).
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

_CONTENT_DIR = Path(__file__).resolve().parents[1] / "content"


def load_markdown(name: str) -> str:
    """Lee ``ui/content/<name>`` (por ejemplo ``u2_map_ml.md``)."""
    return (_CONTENT_DIR / name).read_text(encoding="utf-8")


def render_theory(name: str) -> None:
    """Renderiza el Markdown+LaTeX de ``ui/content/<name>``."""
    st.markdown(load_markdown(name))
