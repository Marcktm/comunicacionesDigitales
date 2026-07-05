"""Motor de "code katas": práctica de código validada por tests (✅/❌ + feedback).

El usuario completa un snippet de Python en un text_area; el código se ejecuta en
un sandbox (builtins restringidos, sin import/open) con numpy pre-cargado, y un
validador compara el resultado con la implementación de referencia de `core/`.
Uso local monousuario: la restricción evita accidentes, no es seguridad dura.
"""
from __future__ import annotations

import builtins as _builtins
from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np
import streamlit as st

_SAFE_NAMES = (
    "abs", "min", "max", "sum", "len", "range", "enumerate", "zip", "round",
    "print", "float", "int", "complex", "bool", "list", "tuple", "dict", "set",
    "sorted", "map", "filter", "pow", "divmod", "any", "all", "isinstance",
    "reversed", "str", "ValueError", "TypeError", "ZeroDivisionError",
)
_SAFE_BUILTINS = {name: getattr(_builtins, name) for name in _SAFE_NAMES}


@dataclass
class Kata:
    """Una práctica de código: consigna + validador por comportamiento."""

    id: str
    title: str
    prompt: str                                   # consigna (markdown)
    starter: str                                  # código inicial a completar
    hint: str                                     # pista
    solution: str                                 # solución canónica
    validator: Callable[[dict], tuple[bool, str]] # ns -> (ok, mensaje)
    setup: Optional[Callable[[], dict]] = None    # variables pre-cargadas


def run_user_code(code: str, extra_ns: Optional[dict] = None) -> dict:
    """Ejecuta el código del usuario en el sandbox y devuelve su namespace."""
    ns: dict = {"__builtins__": _SAFE_BUILTINS, "np": np}
    if extra_ns:
        ns.update(extra_ns)
    exec(code, ns)  # noqa: S102 — sandbox local monousuario
    return ns


def check_kata(kata: Kata, code: str) -> tuple[bool, str]:
    """Corre el código contra el validador del kata. Devuelve (ok, mensaje)."""
    try:
        extra = kata.setup() if kata.setup else {}
        ns = run_user_code(code, extra)
    except Exception as exc:  # error de sintaxis/ejecución del usuario
        return False, f"El código no se pudo ejecutar: {type(exc).__name__}: {exc}"
    try:
        return kata.validator(ns)
    except Exception as exc:
        return False, f"Validación fallida: {type(exc).__name__}: {exc}"


def render_kata(kata: Kata) -> None:
    """Renderiza un kata: consigna, editor, verificación, pista y solución."""
    st.markdown(f"#### 🥋 {kata.title}")
    st.markdown(kata.prompt)
    code = st.text_area(
        "Tu código", value=kata.starter, height=140,
        key=f"kata_code_{kata.id}", label_visibility="collapsed",
    )
    c = st.columns([1, 1, 4])
    if c[0].button("Verificar ✔", key=f"kata_check_{kata.id}"):
        ok, msg = check_kata(kata, code)
        if ok:
            st.success(f"✅ ¡Correcto! {msg}")
        else:
            st.error(f"❌ {msg}")
    with st.expander("💡 Pista"):
        st.markdown(kata.hint)
    with st.expander("📖 Ver solución"):
        st.code(kata.solution, language="python")
    st.divider()
