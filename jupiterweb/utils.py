import requests
from bs4 import BeautifulSoup


def obter_soup(url: str) -> BeautifulSoup:
    """
    Faz request para URL e retorna objeto BeautifulSoup com o texto da resposta.
    """

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    response.encoding = "iso-8859-1"
    soup = BeautifulSoup(response.text, "html.parser")

    return soup


def truncate_string(s: str, max_length: int) -> str:
    """
    Trunca string para um comprimento máximo, adicionando "..." no final se necessário.
    """

    if len(s) <= max_length:
        return s
    return s[: max(max_length - 3, 0)] + "..."
