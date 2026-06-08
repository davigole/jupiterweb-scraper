import json

from .instituto import Instituto
from .paths import PATHS


def obter_institutos() -> list[Instituto]:
    """
    Retorna lista com todas as unidades de ensino cadastradas no Jupiterweb (delega
    o scraping da pagina da unidade e de suas disciplinas, que é feito sob demanda).
    """

    with open(PATHS["institutos"], "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Instituto(codigo, data[codigo]["nome"], data[codigo]["campus"], data[codigo]["abrev"]) for codigo in data]
