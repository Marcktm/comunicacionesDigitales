"""Chequeo de disponibilidad de los SDR (probe de conexión TCP a iiod).

Un SDR puede estar apagado, ocupado por otro usuario o inaccesible (sin VPN).
Probamos una conexión TCP al puerto de iiod con timeout corto; si abre, el
dispositivo está accesible.
"""
from __future__ import annotations

import socket

from .registry import IIOD_PORT, SDR_DEVICES


def check_ip(ip_addr: str, port: int = IIOD_PORT, timeout: float = 0.6) -> bool:
    try:
        with socket.create_connection((ip_addr, port), timeout=timeout):
            return True
    except OSError:
        return False


def check_all(timeout: float = 0.6) -> dict[str, bool]:
    """Devuelve {nombre: disponible} para todos los SDR del registro."""
    return {name: check_ip(addr, timeout=timeout) for name, addr in SDR_DEVICES.items()}
