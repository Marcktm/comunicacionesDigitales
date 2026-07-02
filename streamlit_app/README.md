# App Streamlit — Comunicaciones Digitales

App didáctica de la materia (FCEFyN, UNC), basada en Bixio Rimoldi,
*Principles of Digital Communication*. Cada ítem del temario es una página con tres
secciones: **Teoría** (demostración completa paso a paso, LaTeX), **Gráficas de ejemplo**
(interactivas) y **Bonus SDR** (ADALM-Pluto real por VPN, donde aplique).

## Instalación

**Opción rápida (sin SDR), venv + pip:**

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r streamlit_app/requirements.txt   # pyadi-iio/libiio son opcionales
```

**Opción completa (con SDR), conda:**

```bash
conda env create -f streamlit_app/environment.yml
conda activate comdig-app
```

En macOS, para el SDR: `brew install libiio` (o el paquete de Analog Devices) + `pip install pyadi-iio`.

## Correr

```bash
streamlit run streamlit_app/app.py
```

## SDR (bonus)

1. Conectar la VPN (Cisco AnyConnect `200.16.19.5:443`, user `LabSDR2024`).
2. En el sidebar, **Chequear disponibilidad** y elegir un SDR 🟢 (`192.168.1.31`…`.35`).
3. Ir a una página con sección **Bonus SDR**.

El selector de SDR es global (persiste al navegar). Las páginas de teoría y las gráficas
funcionan sin hardware.

## Tests

```bash
pytest streamlit_app/tests -q
```

## Arquitectura

- `core/` — DSP puro (sin Streamlit ni SDR), testeable.
- `sdr/` — adaptador del Pluto (pyadi-iio), disponibilidad y estado global.
- `usecases/` — casos de uso (orquestan `core` + `sdr`).
- `ui/` — páginas (`pages/`), componentes (`components/`) y teoría (`content/*.md`).

Estado y roadmap: ver [`PLAN.md`](PLAN.md).
