"""Katas de programación del SDR y generación de señales (Unidad 4).

Cada kata valida el código del usuario POR COMPORTAMIENTO contra la
implementación de referencia de `core/` (o contra propiedades verificables).
"""
from __future__ import annotations

from types import SimpleNamespace

import numpy as np

from core.modulation import complex_exp, square_wave
from ui.components.code_kata import Kata


# --------------------------------------------------------------------------- #
# Validadores
# --------------------------------------------------------------------------- #
def _v_square(ns):
    w = ns.get("w")
    if w is None:
        return False, "No encontré la variable `w`."
    w = np.asarray(w, dtype=float)
    ref = square_wave(200, period=20, amp=1.0)
    if w.shape != ref.shape:
        return False, f"`w` debe tener 200 muestras (tiene {w.shape})."
    if not np.allclose(w, ref):
        return False, "Los valores no coinciden: debe arrancar en +1 y alternar cada 10 muestras (período 20)."
    return True, "Onda cuadrada de período 20 y amplitud ±1."


def _v_cexp(ns):
    x = ns.get("x")
    if x is None:
        return False, "No encontré la variable `x`."
    x = np.asarray(x)
    ref = complex_exp(1024, Fc=100e3, Fs=1e6)
    if x.shape != ref.shape:
        return False, f"`x` debe tener 1024 muestras (tiene {x.shape})."
    if not np.iscomplexobj(x):
        return False, "`x` debe ser compleja (usá 1j en el exponente)."
    if not np.allclose(x, ref):
        return False, "Valores incorrectos: x[n] = exp(j·2π·Fc·n/Fs) con n = 0…N−1."
    return True, "Exponencial compleja correcta (|x[n]|=1, fase 2π·Fc·n/Fs)."


def _setup_bits():
    rng = np.random.default_rng(7)
    return {"bits": rng.integers(0, 2, size=64)}


def _v_bpsk(ns):
    s = ns.get("simbolos")
    if s is None:
        return False, "No encontré la variable `simbolos`."
    s = np.asarray(s)
    ref = 2 * np.asarray(ns["bits"]) - 1
    if s.shape != ref.shape:
        return False, "`simbolos` debe tener el mismo largo que `bits`."
    if not np.array_equal(s, ref):
        return False, "El mapeo antipodal es 0 → −1 y 1 → +1 (probá 2*bits − 1)."
    return True, "Mapeo BPSK antipodal correcto."


def _setup_dac():
    rng = np.random.default_rng(3)
    x = rng.normal(size=256) + 1j * rng.normal(size=256)
    return {"x": x}


def _v_dac(ns):
    xtx = ns.get("x_tx")
    if xtx is None:
        return False, "No encontré la variable `x_tx`."
    x = np.asarray(ns["x"])
    xtx = np.asarray(xtx)
    ref = x / np.max(np.abs(x)) * 2**14
    if xtx.shape != x.shape:
        return False, "`x_tx` debe tener la misma forma que `x`."
    if not np.allclose(np.max(np.abs(xtx)), 2**14, rtol=1e-6):
        return False, f"El módulo máximo debe ser 2**14 = {2**14} (te dio {np.max(np.abs(xtx)):.1f})."
    if not np.allclose(xtx, ref):
        return False, "Debe ser la misma señal escalada: x / max|x| · 2**14."
    return True, "Señal normalizada a la escala del DAC (2¹⁴)."


def _setup_sdr():
    return {"sdr": SimpleNamespace()}


def _v_sdr_config(ns):
    sdr = ns["sdr"]
    checks = [
        ("sample_rate", int(4e6)),
        ("loopback", 1),
        ("tx_lo", int(2400e6)),
        ("rx_lo", int(2400e6)),
        ("tx_hardwaregain_chan0", -30),
        ("gain_control_mode_chan0", "slow_attack"),
        ("tx_cyclic_buffer", True),
    ]
    for attr, want in checks:
        if not hasattr(sdr, attr):
            return False, f"Falta configurar `sdr.{attr}`."
        got = getattr(sdr, attr)
        if got != want:
            return False, f"`sdr.{attr}` = {got!r}, esperaba {want!r}."
    return True, "Configuración de loopback digital correcta (la del Lab 4)."


def _v_qpsk(ns):
    c = ns.get("constelacion")
    if c is None:
        return False, "No encontré la variable `constelacion`."
    c = np.asarray(c)
    if c.shape != (4,):
        return False, "Deben ser exactamente 4 símbolos."
    if not np.allclose(np.abs(c), 1.0):
        return False, "Cada símbolo debe tener módulo 1 (dividí por √2)."
    ref = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
    got = {(round(z.real * np.sqrt(2)), round(z.imag * np.sqrt(2))) for z in c}
    if got != ref:
        return False, "Deben ser (±1±1j)/√2 — las cuatro combinaciones de signo."
    return True, "Constelación QPSK de energía unitaria."


# --------------------------------------------------------------------------- #
# Katas
# --------------------------------------------------------------------------- #
SDR_KATAS = [
    Kata(
        id="square",
        title="Generar una onda cuadrada",
        prompt=(
            "Creá `w`: una **onda cuadrada** de **200 muestras**, período **20 muestras**, "
            "amplitud **±1**, que arranca en +1 (10 muestras en +1, 10 en −1, …). "
            "Es la señal de prueba típica para ver el efecto de los filtros del SDR."
        ),
        starter="n = np.arange(200)\nw = ...",
        hint="El resto `n % 20` dice en qué parte del ciclo estás; compará con 10 y usá `np.where`.",
        solution="n = np.arange(200)\nw = np.where((n % 20) < 10, 1.0, -1.0)",
        validator=_v_square,
    ),
    Kata(
        id="cexp",
        title="Exponencial compleja (el tono del Lab 1)",
        prompt=(
            "Creá `x`: la **exponencial compleja** $x[n]=e^{j2\\pi F_c n/F_s}$ con "
            "**N = 1024** muestras, **Fc = 100 kHz** y **Fs = 1 MHz**. "
            "Es la señal que transmite el Lab 1 (un tono en Fc)."
        ),
        starter="N, Fc, Fs = 1024, 100e3, 1e6\nn = np.arange(N)\nx = ...",
        hint="`np.exp(1j * 2 * np.pi * Fc * n / Fs)` — el `1j` la hace compleja.",
        solution=(
            "N, Fc, Fs = 1024, 100e3, 1e6\n"
            "n = np.arange(N)\n"
            "x = np.exp(1j * 2 * np.pi * Fc * n / Fs)"
        ),
        validator=_v_cexp,
    ),
    Kata(
        id="bpsk",
        title="Mapeo BPSK antipodal",
        prompt=(
            "Tenés un array `bits` con 0s y 1s. Creá `simbolos` con el **mapeo antipodal** "
            "0 → −1, 1 → +1 (el encoder del simulador BPSK)."
        ),
        starter="simbolos = ...",
        hint="Una sola operación aritmética sobre el array: multiplicar y restar.",
        solution="simbolos = 2 * bits - 1",
        validator=_v_bpsk,
        setup=_setup_bits,
    ),
    Kata(
        id="qpsk",
        title="Inicializar la constelación QPSK",
        prompt=(
            "Creá `constelacion`: un array con los **4 símbolos QPSK** de **energía unitaria**: "
            "$(\\pm1\\pm 1j)/\\sqrt{2}$ (las cuatro combinaciones de signo, en cualquier orden)."
        ),
        starter="constelacion = np.array([...])",
        hint="Escribí los 4 complejos 1+1j, 1-1j, -1+1j, -1-1j y dividí el array por np.sqrt(2).",
        solution="constelacion = np.array([1+1j, 1-1j, -1+1j, -1-1j]) / np.sqrt(2)",
        validator=_v_qpsk,
    ),
    Kata(
        id="dac",
        title="Normalizar la señal para el DAC del Pluto",
        prompt=(
            "Tenés una señal compleja `x`. Creá `x_tx`: la misma señal **escalada para el DAC** "
            "del Pluto, de modo que su **módulo máximo sea 2¹⁴** (así se transmite con "
            "`sdr.tx(x_tx)` sin saturar)."
        ),
        starter="x_tx = ...",
        hint="Dividí por `np.max(np.abs(x))` (queda máximo 1) y multiplicá por `2**14`.",
        solution="x_tx = x / np.max(np.abs(x)) * 2**14",
        validator=_v_dac,
        setup=_setup_dac,
    ),
    Kata(
        id="config",
        title="Configurar el Pluto en loopback digital",
        prompt=(
            "Tenés un objeto `sdr` (como el que devuelve `adi.Pluto(uri)`). Configuralo como en "
            "el **Lab 4, loopback digital**: `sample_rate` = **4 MHz** (entero), `loopback` = "
            "**1** (digital), `tx_lo` **y** `rx_lo` = **2400 MHz** (enteros), "
            "`tx_hardwaregain_chan0` = **−30**, `gain_control_mode_chan0` = "
            "**'slow_attack'** y `tx_cyclic_buffer` = **True**."
        ),
        starter=(
            "sdr.sample_rate = ...\n"
            "sdr.loopback = ...\n"
            "sdr.tx_lo = ...\n"
            "sdr.rx_lo = ...\n"
            "sdr.tx_hardwaregain_chan0 = ...\n"
            "sdr.gain_control_mode_chan0 = ...\n"
            "sdr.tx_cyclic_buffer = ..."
        ),
        hint="Las frecuencias van como enteros: `int(4e6)`, `int(2400e6)`. Loopback digital = 1.",
        solution=(
            "sdr.sample_rate = int(4e6)\n"
            "sdr.loopback = 1\n"
            "sdr.tx_lo = int(2400e6)\n"
            "sdr.rx_lo = int(2400e6)\n"
            "sdr.tx_hardwaregain_chan0 = -30\n"
            "sdr.gain_control_mode_chan0 = 'slow_attack'\n"
            "sdr.tx_cyclic_buffer = True"
        ),
        validator=_v_sdr_config,
        setup=_setup_sdr,
    ),
]
