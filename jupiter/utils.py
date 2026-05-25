import requests #É o mensageiro que vai até os servidores da USP e faz o download da página inteira no programa.
from bs4 import BeautifulSoup #Serve como tradutor. BeautifulSoup pega as informações e organiza de uma forma que facilite a pesquisa.
from .instituto import Instituto


def obter_institutos() -> list[Instituto]:
    """
    Retorna lista com todas as unidades de ensino cadastradas no Jupiterweb (delega
    o scraping da pagina da unidade e de suas disciplinas, que é feito sob demanda).
    """
    #Define o endereço e manda o mensageiro ir buscar os dados:
    url_jupiter = "https://uspdigital.usp.br/jupiterweb/jupColegiadoLista?tipo=D"
    resposta = requests.get(url_jupiter)

    #Entrega o texto da resposta para o tradutor:
    soup = BeautifulSoup(resposta.text, 'html.parser')

    lista_de_institutos = []

    #Linha de tabela. Ela manda o código pegar todas as linhas da tabela da página de uma vez só:
    linhas = soup.find_all('tr')

    for linha in linhas: #Serve para analisar linha por linha dessa tabela
        colunas = linha.find_all('td') #procura as colunas.

        #Uma trava de segurança. Só entra no if se a linha tiver pelo menos duas informações (código e nome):
        if len(colunas) >= 2:
            #Pega a primeira coluna (índice 0) e a segunda (índice 1).
            #O comando .get_text(strip=True) joga fora as tags HTML e apaga os espaços em branco sobrando, deixando só a palavra pura:
            codigo_extraido = colunas[0].get_text(strip=True)
            nome_extraido = colunas[1].get_text(strip=True)

            #Orientação a Objetos. Passa uma string vazia "" para o campus:
            instituto_obj = Instituto(codigo=codigo_extraido, nome=nome_extraido, campus="")

            lista_de_institutos.append(instituto_obj) #guarda o objeto na lista e, quando o loop terminar, a função devolve a lista pronta.

    return lista_de_institutos
