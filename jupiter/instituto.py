import requests
from bs4 import BeautifulSoup
from disciplina import Disciplina
from urls import URLS


class Instituto:
    """
    Unidade de ensino cadastrada no Jupiterweb.
    """

    def __init__(self, codigo: str, nome: str, campus: str) -> None:
        self.codigo = codigo
        self.nome = nome
        self.campus = campus
        self.disciplinas = []
        self._carregado = False

    def __repr__(self) -> str:
        return ""

    def __str__(self) -> str:
        return self.nome + " (" + self.codigo + ") - " + self.campus

    def _carregar(self) -> None:
        """
        Faz scraping da pagina com as disciplinas do instituto e armazena
        os objetos do tipo Disciplina correspondentes (delega o scraping das
        disciplinas, que é feito sob demanda).
        """

        if self._carregado:
            return

        response = requests.get(self.url_listagem)
        response.encoding = "iso-8859-1"
        soup = BeautifulSoup(response.text, "html.parser")

        tables = soup.find_all("table")
        disciplinas_table = tables[2]
        disciplina_rows = disciplinas_table.find_all("tr")[1:]

        for row in disciplina_rows:
            tds = row.find_all("td")
            sigla = tds[0].find("span").text.strip()
            self.disciplinas.append(Disciplina(sigla))

        self._carregado = True

    @property
    def url_listagem(self) -> str:
        """
        URL do Jupiterweb com todas as disciplinas oferecidas pela unidade de ensino.
        """

        return URLS["listagem"].format(codigo=self.codigo)

    def obter_disciplinas(self) -> list[Disciplina]:
        """
        Retorna lista de disciplinas oferecidas no instituto.
        """

        if not self._carregado:
            self._carregar()

        return self.disciplinas
