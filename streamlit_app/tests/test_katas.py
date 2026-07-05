"""Tests del motor de katas y de las katas SDR: solución pasa, error falla, sandbox."""
import pytest

from ui.components.code_kata import check_kata, run_user_code
from ui.content.katas.sdr import SDR_KATAS

_WRONG = {
    "square": "w = np.ones(200)",
    "cexp": "N, Fc, Fs = 1024, 100e3, 1e6\nx = np.cos(2*np.pi*Fc*np.arange(N)/Fs)",
    "bpsk": "simbolos = bits",
    "qpsk": "constelacion = np.array([1+1j, 1-1j, -1+1j, -1-1j])",  # sin normalizar
    "dac": "x_tx = x * 2**14",   # no normaliza el máximo
    "config": "sdr.loopback = 2\nsdr.sample_rate = int(4e6)",
}


@pytest.mark.parametrize("kata", SDR_KATAS, ids=[k.id for k in SDR_KATAS])
def test_solucion_canonica_pasa(kata):
    ok, msg = check_kata(kata, kata.solution)
    assert ok, f"la solución de '{kata.id}' no pasó su validador: {msg}"


@pytest.mark.parametrize("kata", SDR_KATAS, ids=[k.id for k in SDR_KATAS])
def test_respuesta_incorrecta_falla(kata):
    ok, _ = check_kata(kata, _WRONG[kata.id])
    assert not ok, f"una respuesta incorrecta de '{kata.id}' pasó el validador"


@pytest.mark.parametrize("kata", SDR_KATAS, ids=[k.id for k in SDR_KATAS])
def test_starter_no_pasa(kata):
    # El código inicial (con ...) no debe validar como correcto.
    ok, _ = check_kata(kata, kata.starter)
    assert not ok


def test_sandbox_bloquea_import():
    with pytest.raises(Exception):
        run_user_code("import os")


def test_sandbox_bloquea_open():
    with pytest.raises(Exception):
        run_user_code("open('/etc/passwd')")


def test_sandbox_provee_numpy():
    ns = run_user_code("a = np.arange(3).sum()")
    assert ns["a"] == 3
