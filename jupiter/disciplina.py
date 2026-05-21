from typing import Any

from .urls import URLS


class Disciplina:
    """
    Disciplina cadastrada no Jupiterweb.
    """

    def __init__(self, sigla: str) -> None:
        self.sigla = sigla
        self._carregado = False

    def __repr__(self) -> str:
        return ""

    def __str__(self) -> str:
        return ""

    def __getattr__(self, name: str) -> Any:
        pass

    def _carregar(self) -> None:
        """
        Faz scraping da pagina da disciplina e armazena os seus dados.
        """

        pass

    @property
    def url_disciplina(self) -> str:
        """
        URL da pagina principal da disciplina no Jupiterweb.
        """

        return URLS["disciplina"].format(sigla=self.sigla)

    @property
    def url_oferecimento(self) -> str:
        """
        URL da pagina de oferecimentos da disciplina no Jupiterweb.
        """

        return URLS["oferecimento"].format(sigla=self.sigla)

    @property
    def url_requisitos(self) -> str:
        """
        URL da pagina de requisitos da disciplina no Jupiterweb.
        """

        return URLS["requisitos"].format(sigla=self.sigla)


class Oferecimento:
    """
    Oferecimento de uma turma no Jupiterweb.
    """

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return ""

    def __str__(self) -> str:
        return ""
