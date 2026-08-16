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
        self._disciplinas = []
        self._carregado = False

    def __repr__(self) -> str:
        return f"Instituto(codigo='{self.codigo}',nome='{self.nome}',campus='{self.campus}',abrev='{self.abrev}')"

    def __str__(self) -> str:
        return self.nome

    def _carregar(self) -> None:
        """
        Faz scraping da página de disciplinas do instituto. Armazena as disciplinas
        encontradas e marca o instituto como carregado.
        """

        self._disciplinas = []
        soup = obter_soup(self.url_listagem)
        disciplina_rows = soup.select("tr[bgcolor='#658CCF'] ~tr")

        for row in disciplina_rows:
            tds = row.find_all("td")
            if not tds:
                continue

            sigla_span = tds[0].find("span")
            if not sigla_span:
                continue

            sigla = sigla_span.get_text(strip=True)
            self._disciplinas.append(Disciplina(sigla))

        self._carregado = True

    @property
    def url_listagem(self) -> str:
        """
        URL da página de disciplinas do instituto no Jupiterweb.
        """

        return URLS["listagem"].format(codigo=self.codigo)

    def obter_disciplinas(self, force: bool = False) -> list[Disciplina]:
        """
        Retorna lista de disciplinas oferecidas no instituto. Faz scraping da página de
        disciplinas do instituto caso ainda não tenha sido feito. Se `force` for `True`,
        força o recarregamento da lista de disciplinas, mesmo que já tenha sido
        carregada antes.
        """

        if not self._carregado or force:
            self._carregar()

        return self._disciplinas
