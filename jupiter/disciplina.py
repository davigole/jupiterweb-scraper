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
        centered_text = [(centered_text[i] if len(centered_text) > i else "") for i in range(4)]

        self._dados["instituto"] = centered_text[0]
        self._dados["departamento"] = centered_text[1]
        self._dados["nome"] = centered_text[2].removeprefix("Disciplina:").strip()
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

        self._dados["oferecimento"] = []

        soup = obter_soup(self.url_oferecimento)
        table = soup.select_one("div#layout_principal > table:nth-of-type(4)")

        if not table:
            return  # sem oferecimentos

        boxes = table.select_one("td").find_all("div", recursive=False)

        for box in boxes:
            box_tables = box.find_all("table", recursive=False)

            # ----- Informacao basica -----
            info_text = [i.get_text(strip=True) for i in box_tables[0].select("span.txt_arial_8pt_gray")]
            info_text = [(info_text[i] if len(info_text) > i else "") for i in range(5)]

            oferecimento = Oferecimento(
                codigo=info_text[0],
                data_inicio=info_text[1],
                data_fim=info_text[2],
                tipo_turma=info_text[3],
                observacoes=info_text[4],
                sigla_disciplina=self.sigla,
            )

            # ----- Horarios -----
            horarios_rows = box_tables[1].find_all("tr", recursive=False)[1:]

            for row in horarios_rows:
                row_text = [i.get_text(strip=True) for i in row.find_all("td", recursive=False)]
                row_text = [(row_text[i] if len(row_text) > i else "") for i in range(4)]

                oferecimento.adicionar_horario(row_text[0], row_text[1], row_text[2], row_text[3])

            # ----- Vagas -----
            vagas_rows = box_tables[2].find_all("tr", recursive=False)
            vagas_labels = [i.get_text(strip=True).lower() for i in vagas_rows[0].find_all("td", recursive=False)][1:]
            vagas_labels = [self._normalizar_titulo(i) for i in vagas_labels]

            tipo_vaga = ""

            for row in vagas_rows[1:]:
                row_text = [i.get_text(strip=True) for i in row.find_all("td", recursive=False)]

                istitle = row_text[0] != ""
                if not istitle:
                    row_text = row_text[1:]

                row_name = row_text[0]
                row_vals = [(int(i) if i.isnumeric() else "-") for i in row_text[1:]]
                row_vals = [(row_vals[i] if len(row_vals) > i else "-") for i in range(len(vagas_labels))]
                row_items = {vagas_labels[i]: row_vals[i] for i in range(len(vagas_labels))}

                if istitle:  # novo tipo de vaga
                    tipo_vaga = self._normalizar_titulo(row_name)
                    oferecimento.vagas[tipo_vaga] = row_items
                    oferecimento.vagas[tipo_vaga]["cursos"] = {}
                else:
                    oferecimento.vagas[tipo_vaga]["cursos"][row_name] = row_items

            self._dados["oferecimento"].append(oferecimento)

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

    def possui_oferecimento(self) -> bool:
        """
        Verifica se disciplina tem algum oferecimento no semestre atual.
        """

        return bool(self.obter_dados().get("oferecimento"))


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


class Oferecimento:
    """
    Oferecimento de turma no Jupiterweb.
    """

    def __init__(
        self,
        codigo: str,
        data_inicio: str,
        data_fim: str,
        tipo_turma: str,
        observacoes: str = "",
        sigla_disciplina: str = "",
    ) -> None:
        self.codigo = str(codigo).upper()
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.tipo_turma = str(tipo_turma).lower()
        self.observacoes = observacoes
        self.sigla_disciplina = str(sigla_disciplina).upper()
        self.horarios: list[HorarioAula] = []
        self.vagas = {}

    def __repr__(self) -> str:
        return f"Oferecimento(codigo='{self.codigo}',data_inicio='{self.data_inicio}',data_fim='{self.data_fim}',tipo_turma='{self.tipo_turma}',observacoes='{self.observacoes}',sigla_disciplina='{self.sigla_disciplina}')"

    def __str__(self) -> str:
        return f"Turma {self.codigo}"

    def adicionar_horario(self, dia_semana: str, hora_inicio: str, hora_fim: str, professor: str) -> None:
        """
        Adiciona horario de aula ao oferecimento.
        """

        horario = HorarioAula(dia_semana, hora_inicio, hora_fim, professor)
        self.horarios.append(horario)


class HorarioAula:
    """
    Horario de aula no Jupiterweb.
    """

    def __init__(self, dia_semana: str, hora_inicio: str, hora_fim: str, professor: str) -> None:
        self.dia_semana = str(dia_semana).lower()
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.professor = professor

    def __repr__(self) -> str:
        return f"HorarioAula(dia_semana='{self.dia_semana}',hora_inicio='{self.hora_inicio}',hora_fim='{self.hora_fim}',professor='{self.professor}')"

    def __str__(self) -> str:
        return f"{self.dia_semana} ({self.hora_inicio} - {self.hora_fim}) Prof(a). {self.professor}"
