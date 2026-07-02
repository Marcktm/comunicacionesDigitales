"""Capa `sdr`: adaptador del ADALM-Pluto (pyadi-iio) y estado de dispositivos.

No importa Streamlit salvo ``session.py`` (glue de estado global de la UI).
La librería ``adi`` se importa de forma perezosa dentro de ``pluto.py`` para que
la app corra en máquinas sin pyadi-iio instalado.
"""
