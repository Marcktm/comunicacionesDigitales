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


def continuous_awgn_diagram() -> str:
    """Fig. 3.1 (pág. 95) — canal AWGN de tiempo continuo: R(t) = w_i(t) + N(t)."""
    return f"""
digraph {{ {_STYLE}
  src   [shape=plaintext, label="H = i ∈ H"];
  tx    [shape=box, label="Transmisor"];
  sum   [shape=circle, label="+", width=0.4, fixedsize=true];
  rx    [shape=box, label="Receptor"];
  out   [shape=plaintext, label="Ĥ ∈ H"];
  noise [shape=plaintext, label="N(t)  (AWGN, N₀/2)"];
  src  -> tx;
  tx   -> sum [label="w_i(t) ∈ W"];
  noise-> sum;
  sum  -> rx [label="R(t)"];
  rx   -> out;
}}"""


def waveform_abstraction_diagram() -> str:
    """Fig. 3.2 (pág. 96) — abstracción del canal de formas de onda (dos capas)."""
    return f"""
digraph {{ {_STYLE}
  enc   [shape=box, label="Encoder"];
  wf    [shape=box, label="Waveform\\nFormer"];
  sum   [shape=circle, label="+", width=0.4, fixedsize=true];
  ntf   [shape=box, label="n-Tuple\\nFormer"];
  dec   [shape=box, label="Decoder"];
  hin   [shape=plaintext, label="H = i"];
  hout  [shape=plaintext, label="Ĥ"];
  noise [shape=plaintext, label="N(t)"];
  hin -> enc;
  enc -> wf  [label="c_i ∈ Rⁿ"];
  wf  -> sum [label="w_i(t)"];
  noise -> sum;
  sum -> ntf [label="R(t)"];
  ntf -> dec [label="Y ∈ Rⁿ"];
  dec -> hout;
}}"""


def decomposed_txrx_diagram() -> str:
    """Fig. 3.4 (pág. 103) — TX/RX descompuestos: multiplicar por ψ_j / integrar."""
    return f"""
digraph {{ {_STYLE}
  enc  [shape=box, label="Encoder"];
  m1   [shape=circle, label="×", width=0.35, fixedsize=true];
  m2   [shape=circle, label="×", width=0.35, fixedsize=true];
  s1   [shape=plaintext, label="ψ₁(t)"];
  s2   [shape=plaintext, label="ψₙ(t)"];
  sig  [shape=circle, label="Σ", width=0.4, fixedsize=true];
  sum  [shape=circle, label="+", width=0.4, fixedsize=true];
  n    [shape=plaintext, label="N(t)  (AWGN)"];
  d1   [shape=circle, label="×", width=0.35, fixedsize=true];
  d2   [shape=circle, label="×", width=0.35, fixedsize=true];
  p1   [shape=plaintext, label="ψ₁*(t)"];
  p2   [shape=plaintext, label="ψₙ*(t)"];
  i1   [shape=box, label="∫"];
  i2   [shape=box, label="∫"];
  dec  [shape=box, label="Decoder"];
  hin  [shape=plaintext, label="i ∈ H"]; hout [shape=plaintext, label="î"];
  hin -> enc;
  enc -> m1 [label="c_{{i,1}}"];  enc -> m2 [label="c_{{i,n}}"];
  s1 -> m1;  s2 -> m2;
  m1 -> sig; m2 -> sig;
  sig -> sum [label="w_i(t) = Σⱼ c_{{i,j}} ψⱼ(t)"];
  n -> sum;
  sum -> d1 [label="R(t)"]; sum -> d2;
  p1 -> d1;  p2 -> d2;
  d1 -> i1;  d2 -> i2;
  i1 -> dec [label="Y₁"]; i2 -> dec [label="Yₙ"];
  dec -> hout;
}}"""


def correlator_vs_matched_diagram() -> str:
    """Fig. 3.6 (pág. 107) — dos formas de calcular ∫ r(t)·b*(t) dt."""
    return f"""
digraph {{ {_STYLE}
  subgraph cluster_a {{
    label="(a) Correlador"; style=dashed;
    ra  [shape=plaintext, label="r(t)"];
    mul [shape=circle, label="×", width=0.35, fixedsize=true];
    bb  [shape=plaintext, label="b*(t)"];
    int [shape=box, label="Integrador"];
    oa  [shape=plaintext, label="∫ r(t)·b*(t) dt"];
    ra -> mul; bb -> mul; mul -> int; int -> oa;
  }}
  subgraph cluster_b {{
    label="(b) Filtro apareado"; style=dashed;
    rb  [shape=plaintext, label="r(t)"];
    mf  [shape=box, label="h(t) = b*(T − t)"];
    sam [shape=box, label="muestrear en t = T"];
    ob  [shape=plaintext, label="y(T) = ∫ r(t)·b*(t) dt"];
    rb -> mf; mf -> sam; sam -> ob;
  }}
}}"""


def pluto_architecture_diagram() -> str:
    """Bloques del ADALM-Pluto: frontend AD9363 (RF) + backend Zynq (FPGA+ARM+Linux)."""
    return f"""
digraph {{ {_STYLE.replace('rankdir=LR', 'rankdir=TB')}
  anttx [shape=plaintext, label="📡 antena TX"];
  antrx [shape=plaintext, label="📡 antena RX"];
  subgraph cluster_fe {{
    label="FrontEnd — AD9363 (transceptor de conversión directa)"; style=dashed;
    txc [shape=box, label="Cadena TX:\\nFIR → interpolación → DAC → filtro → mezclador (tx_lo) → PA/atenuador"];
    rxc [shape=box, label="Cadena RX:\\nLNA → mezclador (rx_lo) → filtro → ADC → decimación → FIR → AGC"];
  }}
  subgraph cluster_be {{
    label="BackEnd — Zynq Z-7010 (FPGA + ARM Cortex-A9)"; style=dashed;
    fpga  [shape=box, label="FPGA: filtro decimador ÷8\\n(extiende el mínimo a ~65 kSPS)"];
    linux [shape=box, label="Linux embebido + IIO subsystem\\n(iiod escucha por red)"];
  }}
  host [shape=box, label="PC del usuario:\\nPython → pyadi-iio → libiio → [VPN] → iiod"];
  txc -> anttx;
  antrx -> rxc;
  fpga -> txc [label="muestras I/Q"];
  rxc  -> fpga [label="muestras I/Q"];
  linux -> fpga [dir=both, label="config (sample_rate, lo, gain)"];
  host -> linux [dir=both, label="Ethernet (ip:192.168.1.3x)"];
}}"""


def loopback_diagram() -> str:
    """Los tres modos de loopback del Pluto: 0 antena, 1 digital, 2 RF."""
    return f"""
digraph {{ {_STYLE}
  tx  [shape=box, label="TX digital\\n(muestras I/Q)"];
  dac [shape=box, label="DAC + RF TX"];
  aire[shape=plaintext, label="〰 aire 〰"];
  adc [shape=box, label="RF RX + ADC"];
  rx  [shape=box, label="RX digital\\n(muestras I/Q)"];
  tx -> dac; dac -> aire [label="loopback = 0 (antena)"]; aire -> adc; adc -> rx;
  tx -> rx  [label="loopback = 1 (digital: bypass total del RF)", style=dashed, color="#1f77b4"];
  dac -> adc [label="loopback = 2 (RF interno, sin aire)", style=dotted, color="#d62728"];
}}"""


def render(dot: str) -> None:
    """Renderiza un diagrama DOT en la página."""
    st.graphviz_chart(dot, width="stretch")
