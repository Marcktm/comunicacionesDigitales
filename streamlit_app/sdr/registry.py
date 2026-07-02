"""Registro de los 5 SDR del laboratorio (accesibles por VPN).

Las IP van de 192.168.1.31 a 192.168.1.35 (ver instalacion-drivers-sdr.md).
El backend de red de libiio (iiod) escucha en el puerto TCP 30431.
"""
from __future__ import annotations

SDR_DEVICES: dict[str, str] = {
    "SDR-1": "192.168.1.31",
    "SDR-2": "192.168.1.32",
    "SDR-3": "192.168.1.33",
    "SDR-4": "192.168.1.34",
    "SDR-5": "192.168.1.35",
}

IIOD_PORT = 30431  # puerto del daemon iiod (backend de red de libiio)


def uri(name: str) -> str:
    """URI de conexión pyadi-iio, p.ej. ``ip:192.168.1.32``."""
    return f"ip:{SDR_DEVICES[name]}"


def ip(name: str) -> str:
    return SDR_DEVICES[name]
