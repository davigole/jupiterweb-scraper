import importlib.metadata

from .disciplina import Disciplina, HorarioAula, Oferecimento, Requisito
from .instituto import Instituto
from .jupiterweb import obter_institutos

try:
    __version__ = importlib.metadata.version("your_package")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "Disciplina",
    "HorarioAula",
    "Oferecimento",
    "Requisito",
    "Instituto",
    "obter_institutos",
]
