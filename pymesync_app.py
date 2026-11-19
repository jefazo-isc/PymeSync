import sys
from pathlib import Path

# Ejecuta el sistema PymeSync con el tema, iconos y logo horizontal oficial
src_dir = Path(__file__).resolve().parent / "segundo video" / "Tiendita" / "frontend" / "src"
sys.path.insert(0, str(src_dir))

import main  # noqa: F401
