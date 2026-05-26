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
