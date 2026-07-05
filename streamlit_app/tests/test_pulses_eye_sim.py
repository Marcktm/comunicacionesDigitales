"""Tests de core/pulses.py, core/eye.py y core/simulator.py."""
import numpy as np
import pytest

from core.distributions import q_function
from core.eye import eye_traces
from core.pulses import (
    folded_spectrum,
    pulse_train_psd,
    raised_cosine_spectrum,
    rect_pulse_spectrum,
    rrc_pulse,
    rrc_taps,
    sinc_pulse,
)
from core.simulator import simulate_bpsk_chain


# --- pulsos y criterio de Nyquist -------------------------------------------- #
def test_rc_cumple_nyquist_espectro_plegado():
    # Σ_k |ψF(f−k/T)|² = T para todo f (criterio de Nyquist, Bixio §5.4).
    # Grid desplazado para no pisar |f| ≡ 1/2T (mod 1/T): para β=0 el rectángulo
    # tiene un salto ahí y la igualdad puntual falla en ese conjunto de medida
    # nula — es el "l.i.m." del enunciado del teorema (Bixio §5.4).
    T = 1.0
    f = np.linspace(-1.5, 1.5, 300) + 1e-4
    for beta in (0.0, 0.25, 0.5, 0.9):
        total = folded_spectrum(raised_cosine_spectrum, f, T=T, beta=beta)
        assert np.allclose(total, T, atol=1e-9), f"β={beta}"


def test_rrc_beta0_es_sinc():
    t = np.linspace(-5, 5, 401)
    assert np.allclose(rrc_pulse(t, T=1.0, beta=0.0), sinc_pulse(t, T=1.0))


def test_rrc_puntos_singulares_finitos():
    beta, T = 0.5, 1.0
    ts = np.array([0.0, T / (4 * beta), -T / (4 * beta)])
    vals = rrc_pulse(ts, T=T, beta=beta)
    assert np.all(np.isfinite(vals))
    # continuidad: el valor en el punto singular ≈ el de un vecino muy próximo
    near = rrc_pulse(np.array([T / (4 * beta) + 1e-7]), T=T, beta=beta)
    assert vals[1] == pytest.approx(near[0], rel=1e-3)


def test_rrc_taps_ortogonalidad_a_desplazamientos():
    # R(kT) ≈ δ_k0 con span largo: convolución taps*taps muestreada cada sps.
    sps, span, beta = 8, 16, 0.35
    taps = rrc_taps(sps, span, beta)
    rc = np.convolve(taps, taps[::-1])          # coseno realzado total
    center = len(rc) // 2
    assert rc[center] == pytest.approx(1.0, rel=1e-6)
    for k in range(1, span):
        assert abs(rc[center + k * sps]) < 5e-3


def _max_isi(sps, span, beta):
    taps = rrc_taps(sps, span, beta)
    rc = np.convolve(taps, taps[::-1])
    c = len(rc) // 2
    return max(abs(rc[c + k * sps]) for k in range(1, span))


def test_truncar_mas_corto_aumenta_isi():
    # El fenómeno del Lab 4: truncar el RRC más corto agranda el ISI residual.
    assert _max_isi(8, 24, 0.35) < _max_isi(8, 10, 0.35) < _max_isi(8, 4, 0.35)


def test_psd_simbolos_incorrelados_es_espectro_del_pulso():
    # K[k]=E·δ ⇒ S_X = E·|ξF|²/T (Bixio §5.3).
    f = np.linspace(-2, 2, 201)
    E, T = 2.0, 1.0
    sx = pulse_train_psd(f, rect_pulse_spectrum(f, T), K={0: E}, T=T)
    assert np.allclose(sx, E * rect_pulse_spectrum(f, T) / T)


def test_psd_codificacion_correlativa_se_anula_en_dc():
    # K[0]=E, K[±2]=−E/2 ⇒ S_X(f) ∝ sin²(2πfT): se anula en f=0.
    T, E = 1.0, 1.0
    f = np.array([0.0, 1.0 / (8 * T), 1.0 / (4 * T)])
    spec = rect_pulse_spectrum(f, T)
    sx = pulse_train_psd(f, spec, K={0: E, 2: -E / 2, -2: -E / 2}, T=T)
    assert sx[0] == pytest.approx(0.0, abs=1e-12)
    esperado = spec / T * 2 * E * np.sin(2 * np.pi * f * T) ** 2
    assert np.allclose(sx, esperado, atol=1e-12)


# --- diagrama de ojo ---------------------------------------------------------- #
def test_eye_traces_forma():
    x = np.arange(1000, dtype=float)
    tr = eye_traces(x, sps=10, span_symbols=2)
    assert tr.shape[1] == 20
    assert tr.shape[0] > 0
    # trazas consecutivas arrancan cada sps muestras
    assert tr[1][0] - tr[0][0] == pytest.approx(10.0)


# --- simulador BPSK ------------------------------------------------------------ #
def test_simulador_pe_coincide_con_teoria():
    sigma = 0.6
    res = simulate_bpsk_chain(num_bits=40_000, ns=8, sigma=sigma, seed=5)
    assert res.pe_theory == pytest.approx(float(q_function(1.0 / sigma)))
    assert res.pe_est == pytest.approx(res.pe_theory, abs=0.01)


def test_simulador_sin_ruido_no_hay_errores():
    res = simulate_bpsk_chain(num_bits=2000, ns=8, sigma=1e-9, seed=1)
    assert res.pe_est == 0.0
