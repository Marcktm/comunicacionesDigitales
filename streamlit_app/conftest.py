"""Hace importables los paquetes del proyecto (core/sdr/ui) al correr pytest."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
