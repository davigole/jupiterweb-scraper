from .instituto import Instituto
from .urls import URLS
from .utils import obter_soup


def obter_institutos() -> list[Instituto]:
    """
    Retorna lista com todas as unidades de ensino cadastradas no Jupiterweb (delega
    o scraping da pagina da unidade e de suas disciplinas, que é feito sob demanda).
    """

    soup = obter_soup(URLS["institutos"])
    tables = soup.select("table:nth-of-type(2), table:nth-of-type(4)")

    linhas = []
    for tab in tables:
        linhas.extend(tab.select("tr:not(:first-of-type)"))

    lista_de_institutos = []

    for linha in linhas:  # Serve para analisar linha por linha dessa tabela
        colunas = linha.find_all("td")  # procura as colunas.

        # Uma trava de segurança. Só entra no if se a linha tiver pelo menos duas informações (código e nome):
        if len(colunas) >= 2:
            # Pega a primeira coluna (índice 0) e a segunda (índice 1).
            # O comando .get_text(strip=True) joga fora as tags HTML e apaga os espaços em branco sobrando, deixando só a palavra pura:
            codigo_extraido = colunas[0].get_text(strip=True)
            nome_extraido = colunas[1].get_text(strip=True)

            # Orientação a Objetos. Passa uma string vazia "" para o campus:
            instituto_obj = Instituto(codigo=codigo_extraido, nome=nome_extraido, campus="")

            # Guarda o objeto na lista e, quando o loop terminar, a função devolve a lista pronta.
            lista_de_institutos.append(instituto_obj)

    return lista_de_institutos
