import re
import unicodedata
from pprint import pprint
from typing import Any
from warnings import warn

from .urls import URLS
from .utils import obter_soup


class Disciplina:
    """
    Disciplina cadastrada no Jupiterweb.
    """

    def __init__(self, sigla: str) -> None:
        self.sigla = str(sigla).upper()
        self._dados: dict[str, Any] = {}
        self._carregado = False

    def __repr__(self) -> str:
        return f"Disciplina(sigla='{self.sigla}')"

    def __str__(self) -> str:
        return self.sigla

    def __getitem__(self, key: str) -> Any:
        return self.obter_dados()[key]

    def obter_dados(self) -> dict[str, Any]:
        """
        Retorna dados da disciplina no Jupiterweb. Se disciplina ainda nao foi carregada,
        faz o scraping antes de retornar.
        """

        if not self._carregado:
            self._carregar()
        return self._dados

    @property
    def url_principal(self) -> str:
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

    def _normalizar_titulo(self, title: str) -> str:
        """
        Converte titulo ao formato padrao para chaves de dicionario.
        """

        title = title.strip().rstrip(":")
        title = unicodedata.normalize("NFKD", title)
        title = title.encode("ascii", "ignore").decode()
        title = title.lower()
        title = re.sub(r" +", " ", title)
        return title

    def _carregar_principal(self) -> None:
        """
        Faz scraping da pagina principal da disciplina e armazena os dados obtidos.
        """

        soup = obter_soup(self.url_principal)

        table = soup.select_one("form[name='form1'] > table")
        if not table:
            warn(f"Nao foi possivel carregar pagina principal da disciplina {self.sigla}")
            return

        # ----- Texto centralizado -----
        centered_text = [i.get_text(strip=True) for i in table.select("td[align='CENTER']")]

        if len(centered_text) > 0:
            self._dados["instituto"] = centered_text[0]
        if len(centered_text) > 1:
            self._dados["departamento"] = centered_text[1]
        if len(centered_text) > 2:
            self._dados["nome"] = centered_text[2].removeprefix("Disciplina:").strip()
        if len(centered_text) > 3:
            self._dados["nome ingles"] = centered_text[3]

        # ----- Texto livre -----
        span_text = table.select("span.txt_arial_8pt_gray, span.txt_arial_8pt_black")

        title = ""  # guardar texto em self._dados[title] (se subtitle = "")
        subtitle = ""  # guardar texto em self._dados[title][subtitle] (se subtitle != "")

        for t in span_text:
            txt = t.get_text(strip=True, separator="\n")

            if "txt_arial_8pt_black" in t["class"]:  # titulo ou subtitulo
                txt = self._normalizar_titulo(txt)
                parent = t.find_parent("table")
                grandparent = parent.find_parent("table") if parent else None

                if grandparent == table:  # nivel principal (titulo)
                    title = txt
                    subtitle = ""
                    self._dados[title] = ""
                else:  # nivel secundario (titulo > subtitulo)
                    subtitle = txt
                    if isinstance(self._dados[title], str):
                        self._dados[title] = {}
                    self._dados[title][subtitle] = ""
            elif subtitle:  # adicionar texto ao subtitulo
                if txt and self._dados[title][subtitle]:
                    txt = "\n" + txt
                self._dados[title][subtitle] += txt
            else:  # adicionar texto a titulo
                if txt and self._dados[title]:
                    txt = "\n" + txt
                self._dados[title] += txt

    def _carregar_requisitos(self) -> None:
        """
        Faz scraping da pagina de requisitos da disciplina e armazena os dados obtidos.
        """

        # dados["requisitos"][curso] = [["x"], ["y", "z"]] significa que, para fazer a
        # disciplina, alunos de 'curso' precisam ter feito a disciplina "x", ou ter
        # feito ambas as disciplinas "y" e "z".

        self._dados["requisitos"] = {}
        self._dados["periodo ideal"] = {}

        soup = obter_soup(self.url_requisitos)
        table = soup.select_one("form[name='form1'] > table")

        if not table:
            return  # sem requisitos

        rows = table.select("tr.txt_verdana_8pt_gray")
        curso = ""
        index = 0  # adicionar em self._dados["requisitos"][curso][index]

        for row in rows:
            td = row.find_all("td")
            if not td:
                continue

            txt = " ".join(td[0].text.strip().split())
            if not txt:
                continue

            if txt.startswith("Curso"):
                sep = txt.removeprefix("Curso:").split(" - Período ideal:", 1)

                curso = sep[0].strip()
                index = 0
                self._dados["requisitos"][curso] = [[]]

                if len(sep) > 1:
                    self._dados["periodo ideal"][curso] = int(sep[1])
            elif curso and txt.lower() == "ou":
                index += 1
                self._dados["requisitos"][curso].append([])
            elif curso:
                sigla = txt.split("-", 1)[0].strip().upper()
                tipo = td[1].get_text(strip=True)
                if not tipo:
                    tipo = "requisito"

                req = Requisito(sigla, tipo)
                self._dados["requisitos"][curso][index].append(req)

    def _carregar_oferecimento(self) -> None:
        """
        Faz scraping da pagina de oferecimento da disciplina e armazena os dados obtidos.
        """

        pass

    def _carregar(self) -> None:
        """
        Faz scraping da disciplina e armazena os seus dados.
        """

        self._dados = {
            "sigla": self.sigla,
        }

        self._carregar_principal()
        self._carregar_requisitos()
        self._carregar_oferecimento()
        self._carregado = True


class Requisito:
    """
    Requisito de disciplina no Jupiterweb.
    """

    def __init__(self, sigla: str, tipo: str = "requisito") -> None:
        self.sigla = str(sigla)
        self.tipo = str(tipo).lower()  # requisito fraco, indicacao de conjunto, etc.

    def __repr__(self) -> str:
        return f"Requisito(sigla='{self.sigla}',tipo='{self.tipo}')"

    def __str__(self) -> str:
        return self.sigla

    def obter_disciplina(self) -> Disciplina:
        """
        Retorna objeto Disciplina correspondente ao requisito.
        """

        return Disciplina(self.sigla)


# TODO Remover
def main() -> None:
    d = Disciplina("mac0110")
    print(d["instrumentos e criterios de avaliacao"]["norma de recuperacao"])


if __name__ == "__main__":
    main()
