from .disciplina import Disciplina
from .urls import URLS


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
        return ""

    def _carregar(self) -> None:
        """
        Faz scraping da pagina com as disciplinas do instituto e armazena
        os objetos do tipo Disciplina correspondentes (delega o scraping das
        disciplinas, que é feito sob demanda).
        """

        pass

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

        return []
