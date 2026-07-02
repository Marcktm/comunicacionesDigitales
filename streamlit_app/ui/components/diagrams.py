"""Diagramas de bloques del libro reproducidos con Graphviz (DOT nativo).

Cada función devuelve un string DOT (testeable) que las páginas renderizan con
``st.graphviz_chart(dot)``. No requiere el binario de Graphviz del sistema: el
render ocurre en el navegador.
"""
from __future__ import annotations

import streamlit as st

_STYLE = 'rankdir=LR; bgcolor="transparent"; node [fontname="Helvetica"]; edge [fontname="Helvetica"];'


def channel_block_diagram() -> str:
    """Fig. 2.1 — configuración general: i∈H → Transmisor → Canal → Receptor → Ĥ."""
    return f"""
digraph {{ {_STYLE}
  src [shape=plaintext, label="i ∈ H"];
  tx  [shape=box, label="Transmisor"];
  ch  [shape=box, label="Canal"];
  rx  [shape=box, label="Receptor"];
  out [shape=plaintext, label="Ĥ ∈ H"];
  src -> tx;
  tx  -> ch [label="c_i ∈ C ⊂ Xⁿ"];
  ch  -> rx [label="Y ∈ Yⁿ"];
  rx  -> out;
}}"""


def awgn_discrete_diagram() -> str:
    """Fig. 2.5 — canal AWGN discreto: Y = c_i + Z, con Z ~ N(0, σ²Iₙ)."""
    return f"""
digraph {{ {_STYLE}
  src   [shape=plaintext, label="i ∈ H"];
  tx    [shape=box, label="Transmisor"];
  sum   [shape=circle, label="+", width=0.4, fixedsize=true];
  rx    [shape=box, label="Receptor"];
  out   [shape=plaintext, label="Ĥ"];
  noise [shape=plaintext, label="Z ~ N(0, σ²Iₙ)"];
  src  -> tx;
  tx   -> sum [label="c_i ∈ Rⁿ"];
  noise-> sum;
  sum  -> rx [label="Y = c_i + Z"];
  rx   -> out;
}}"""


def render(dot: str) -> None:
    """Renderiza un diagrama DOT en la página."""
    st.graphviz_chart(dot, width="stretch")
