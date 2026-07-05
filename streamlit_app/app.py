"""App Streamlit didáctica — Comunicaciones Digitales (FCEFyN UNC).

Entrypoint: define la navegación por unidades (st.navigation) y renderiza el
sidebar global de SDR. Correr con:  ``streamlit run streamlit_app/app.py``.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Asegura que los paquetes del proyecto (core/sdr/ui) sean importables sin
# importar cómo se lanza la app (streamlit run / AppTest / python -m).
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

from ui.components.sidebar import render_sdr_sidebar
from ui.pages import (
    home,
    u1_correlacion,
    u1_gaussianos,
    u1_probabilidad,
    u3_arquitectura,
    u3_casos,
    u3_energia,
    u3_matched_filter,
    u3_ruido_blanco,
    u3_suficiente,
    u4_config,
    u4_intro,
    u4_programacion,
    u4_ruido,
    u2_awgn_discreto,
    u2_escalar,
    u2_funcion_q,
    u2_hipotesis,
    u2_m_aria,
    u2_map_ml,
    u2_pam_qam,
    u2_pe,
    u2_suficiente,
    u2_vectorial,
)
from ui.pages.common import render_placeholder

st.set_page_config(
    page_title="Comunicaciones Digitales",
    page_icon="📡",
    layout="wide",
)


def _placeholder(title: str, unit: str):
    """Devuelve una función-página que muestra el placeholder de 3 secciones."""

    def page() -> None:
        render_placeholder(title, unit)

    return page


PAGES = {
    "Inicio": [
        st.Page(home.render, title="Inicio", icon="🏠", url_path="inicio", default=True),
    ],
    "Unidad 1 — Probabilidad y vectores aleatorios": [
        st.Page(u1_probabilidad.render, title="Repaso de probabilidad",
                url_path="u1-probabilidad"),
        st.Page(u1_correlacion.render, title="Valor esperado y correlación",
                url_path="u1-correlacion"),
        st.Page(u1_gaussianos.render, title="Vectores gaussianos",
                url_path="u1-gaussianos"),
    ],
    "Unidad 2 — Decisión en tiempo discreto": [
        st.Page(u2_hipotesis.render, title="Prueba de hipótesis", url_path="u2-hipotesis"),
        st.Page(u2_map_ml.render, title="Criterio MAP y ML", icon="⭐",
                url_path="u2-map-ml"),
        st.Page(u2_m_aria.render, title="Hipótesis M-aria", url_path="u2-m-aria"),
        st.Page(u2_pe.render, title="Probabilidad de error", url_path="u2-pe"),
        st.Page(u2_funcion_q.render, title="Función Q", url_path="u2-funcion-q"),
        st.Page(u2_awgn_discreto.render, title="Receptor AWGN discreto",
                url_path="u2-awgn-discreto"),
        st.Page(u2_escalar.render, title="Observación escalar", url_path="u2-escalar"),
        st.Page(u2_vectorial.render, title="Observaciones vectoriales",
                url_path="u2-vectorial"),
        st.Page(u2_pam_qam.render, title="m-PAM y m-QAM", url_path="u2-pam-qam"),
        st.Page(u2_suficiente.render, title="Estadística suficiente",
                url_path="u2-suficiente"),
    ],
    "Unidad 3 — Canal AWGN de tiempo continuo": [
        st.Page(u3_energia.render, title="Energía de señal", url_path="u3-energia"),
        st.Page(u3_ruido_blanco.render, title="Ruido blanco N(t)", url_path="u3-ruido-blanco"),
        st.Page(u3_suficiente.render, title="Estadística suficiente (continuo)",
                url_path="u3-suficiente"),
        st.Page(u3_arquitectura.render, title="Arquitectura TX/RX", url_path="u3-arquitectura"),
        st.Page(u3_casos.render, title="Casos de modulación", url_path="u3-casos"),
        st.Page(u3_matched_filter.render, title="Filtro apareado",
                url_path="u3-matched-filter"),
    ],
    "Unidad 4 — Radio definida por Software (SDR)": [
        st.Page(u4_intro.render, title="Introducción al SDR", url_path="u4-intro"),
        st.Page(u4_programacion.render, title="Cómo programar el SDR", icon="🥋",
                url_path="u4-programacion"),
        st.Page(u4_config.render, title="Lab 1 — Configurar el SDR", url_path="u4-config"),
        st.Page(u4_ruido.render, title="Lab 2 — Caracterización de ruido",
                url_path="u4-ruido"),
    ],
    "Unidad 5 — Tren de pulsos (Nyquist, ISI, ojo)": [
        st.Page(_placeholder("Tren de pulsos y teorema de muestreo", "Unidad 5"),
                title="Teorema de muestreo", url_path="u5-muestreo"),
        st.Page(_placeholder("Densidad espectral de potencia (PSD)", "Unidad 5"),
                title="Densidad espectral (PSD)", url_path="u5-psd"),
        st.Page(_placeholder("Criterio de Nyquist para bases ortonormales", "Unidad 5"),
                title="Criterio de Nyquist", url_path="u5-nyquist"),
        st.Page(_placeholder("Coseno realzado y RRC", "Unidad 5"),
                title="Coseno realzado / RRC", url_path="u5-rrc"),
        st.Page(_placeholder("ISI y diagrama de ojo (Lab 4)", "Unidad 5"),
                title="ISI y diagrama de ojo", url_path="u5-ojo"),
        st.Page(_placeholder("Muestreo, aliasing y filtrado (Lab 3)", "Unidad 5"),
                title="Muestreo y filtrado", url_path="u5-lab3"),
        st.Page(_placeholder("Simulador BPSK + AWGN extremo a extremo", "Unidad 5"),
                title="Simulador BPSK", url_path="u5-simulador"),
        st.Page(_placeholder("Sincronización de símbolo (ML, DLL)", "Unidad 5"),
                title="Sincronización", url_path="u5-sincronizacion"),
    ],
}


def main() -> None:
    nav = st.navigation(PAGES)
    render_sdr_sidebar()  # panel global de SDR (debajo del menú de navegación)
    nav.run()


if __name__ == "__main__":
    main()
