import json
from pathlib import Path

from .instituto import Instituto

PATH_INSTITUTOS = Path(__file__).parent / "data" / "institutos.json"


def obter_institutos() -> list[Instituto]:
    """
    Retorna lista com todas as unidades de ensino cadastradas no Jupiterweb (delega
    o scraping da pagina da unidade e de suas disciplinas, que é feito sob demanda).
    """

    with open(PATH_INSTITUTOS, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Instituto(codigo, data[codigo]["nome"], data[codigo]["campus"], data[codigo]["abrev"]) for codigo in data]
