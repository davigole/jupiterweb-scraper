import logging

import requests
from bs4 import BeautifulSoup
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

@retry(
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=30),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)
def obter_soup(url: str) -> BeautifulSoup:
    """
    Faz request para URL e retorna objeto BeautifulSoup com o texto da resposta.

    Tenta até 5 vezes com backoff exponencial em caso de erro de rede/HTTP.
    Lança a última exceção caso todas as tentativas falhem.
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
