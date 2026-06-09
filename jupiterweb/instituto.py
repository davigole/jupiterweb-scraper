from .disciplina import Disciplina
from .urls import URLS
from .utils import obter_soup


class Instituto:
    """
    Unidade de ensino cadastrada no Jupiterweb.
    """

    def __init__(self, codigo: str, nome: str, campus: str = "", abrev: str = "") -> None:
        self.codigo = str(codigo)
        self.nome = nome
        self.campus = campus
        self.abrev = abrev
        self.disciplinas = []
        self._carregado = False

    def __repr__(self) -> str:
        return f"Instituto(codigo='{self.codigo}',nome='{self.nome}',campus='{self.campus}',abrev='{self.abrev}')"

    def __str__(self) -> str:
        return self.nome

    def _carregar(self) -> None:
        """
        Faz scraping da pagina com as disciplinas do instituto e armazena
        os objetos do tipo Disciplina correspondentes (delega o scraping das
        disciplinas, que é feito sob demanda).
        """

        if self._carregado:
            return

        soup = obter_soup(self.url_listagem)
        disciplina_rows = soup.select("tr[bgcolor='#658CCF'] ~tr")

        for row in disciplina_rows:
            tds = row.find_all("td")
            sigla = tds[0].find("span").get_text(strip=True)
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
