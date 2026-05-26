from urllib.parse import urljoin

URL_BASE = "https://uspdigital.usp.br/jupiterweb/"
URLS: dict[str, str] = {
    "listagem": urljoin(URL_BASE, "jupDisciplinaLista?codcg={codigo}&letra=0-Z&tipo=D"),
    "disciplina": urljoin(URL_BASE, "obterDisciplina?sgldis={sigla}&verdis=1"),
    "oferecimento": urljoin(URL_BASE, "obterTurma?sgldis={sigla}"),
    "requisitos": urljoin(URL_BASE, "listarCursosRequisitos?coddis={sigla}"),
    "institutos": urljoin(URL_BASE, "jupColegiadoLista?tipo=D"),
}
