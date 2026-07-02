"""Tests de los diagramas de bloques (DOT válido con los nodos esperados)."""
from ui.components import diagrams


def test_channel_diagram_dot_valido():
    dot = diagrams.channel_block_diagram()
    assert dot.strip().startswith("digraph")
    assert dot.count("{") == dot.count("}")
    for token in ["Transmisor", "Canal", "Receptor", "i ∈ H", "Ĥ ∈ H"]:
        assert token in dot


def test_awgn_diagram_dot_valido():
    dot = diagrams.awgn_discrete_diagram()
    assert dot.strip().startswith("digraph")
    assert dot.count("{") == dot.count("}")
    for token in ["Transmisor", "Receptor", "Y = c_i + Z", "N(0, σ²Iₙ)"]:
        assert token in dot
