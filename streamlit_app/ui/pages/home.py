"""Página de inicio: portada, temario y cómo usar la app."""
from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("📡 Comunicaciones Digitales — App didáctica")
    st.caption("Ing. en Computación · FCEFyN, UNC · basada en Bixio Rimoldi, *Principles of Digital Communication*")

    st.markdown(
        """
Esta app recorre la materia **capítulo por capítulo**. Cada página tiene tres secciones:

1. **Teoría** — la demostración del libro, **completa y paso a paso**, en español y con LaTeX.
2. **Gráficas de ejemplo** — las figuras del libro generadas en vivo, con controles interactivos.
3. **Bonus — SDR real** — donde aplique, se replica el caso con el ADALM-Pluto del laboratorio.

Usá el menú de la izquierda para navegar por unidades. El **selector de SDR** (también a la
izquierda) es global: elegí el dispositivo y cambialo en cualquier momento.
        """
    )

    st.subheader("Estructura de la materia")
    cols = st.columns(2)
    with cols[0]:
        st.markdown(
            """
- **Unidad 1** — Repaso de probabilidad y vectores aleatorios (Roy Yates).
- **Unidad 2** — Diseño de receptor, observaciones en tiempo discreto *(Bixio cap. 2)*.
- **Unidad 3** — Receptor para canal AWGN de tiempo continuo *(Bixio cap. 3)*.
            """
        )
    with cols[1]:
        st.markdown(
            """
- **Unidad 4** — Radio definida por Software (SDR): PlutoSDR, Lab 1 y Lab 2.
- **Unidad 5** — Symbol-by-symbol en un tren de pulsos: Nyquist, RRC, ISI, diagrama de ojo,
  sincronización *(Bixio cap. 5)*.
            """
        )

    st.subheader("Cómo usar el SDR (bonus)")
    st.markdown(
        """
1. Conectar la **VPN** con Cisco AnyConnect (`200.16.19.5:443`).
2. En el panel de la izquierda, **Chequear disponibilidad** y elegir un SDR 🟢
   (`192.168.1.31`…`.35`).
3. Ir a una página con sección **Bonus SDR** y correr el experimento.

> Las páginas de teoría y las gráficas de ejemplo **funcionan sin hardware**.
        """
    )

    st.info("Página de referencia terminada: **Unidad 2 → Criterio MAP y ML**. El resto se completa por fases.")
