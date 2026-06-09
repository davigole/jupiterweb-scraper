# Jupiterweb Scraper

![Python Version](https://img.shields.io/pypi/pyversions/jupiterweb-scraper)
![License](https://img.shields.io/github/license/davigole/jupiterweb-scraper)
[![PyPI](https://img.shields.io/pypi/v/jupiterweb-scraper)](https://pypi.org/project/jupiterweb-scraper/)

Biblioteca para extração de informações sobre disciplinas da Universidade de São Paulo a partir do [Jupiterweb](https://uspdigital.usp.br/jupiterweb/).

## 📖 Sobre o projeto

O **Jupiterweb Scraper** é uma biblioteca Python que permite a extração de informações sobre disciplinas da Universidade de São Paulo a partir do [Jupiterweb](https://uspdigital.usp.br/jupiterweb/), o sistema oficial de gestão acadêmica da universidade.

A biblioteca foi desenvolvida por alunos do IME-USP, inicialmente para atender às demandas de um projeto interno da [IME Jr](https://imejr.com/) — a empresa júnior do instituto. No entanto, percebemos que a obtenção de dados do Jupiterweb é uma necessidade recorrente em projetos voltados à comunidade USP. Por isso, decidimos disponibilizar o scraper como projeto open-source, com o intuito de facilitar o desenvolvimento de novas ferramentas destinadas à universidade.

> ⚠️ **Aviso:** O Jupiterweb é um site antigo, com uma estrutura HTML complexa e por vezes inconsistente, o que torna o processo de scraping muito desafiador. É esperado que a biblioteca contenha erros que passaram despercebidos. Se você encontrar algum problema ou comportamento inesperado, pedimos que abra uma [Issue](https://github.com/davigole/jupiterweb-scraper/issues) descrevendo o ocorrido.

## 🚀 Instalação

Para instalar a biblioteca, utilize o comando
```bash
pip install jupiterweb-scraper
```

Ou, para instalar a partir do repositório:
```bash
git clone https://github.com/davigole/jupiterweb-scraper.git
cd jupiterweb-scraper
pip install -e .
```

## 📚 Como usar

```python
>>> import jupiterweb
```

A função `obter_institutos()` retorna todos os institutos da USP na forma de objetos da classe `Instituto`:

```python
>>> institutos_usp = jupiterweb.obter_institutos()
>>> instituto = institutos_usp[37]
>>> instituto
Instituto(codigo='45',nome='Instituto de Matemática, Estatística e Ciência da Computação',campus='Butantã',abrev='IME')
```

A partir de um instituto, é possível obter as suas disciplinas:
```python
>>> disciplinas_instituto = instituto.obter_disciplinas()
>>> disciplina = disciplinas_instituto[314]
>>> disciplina
Disciplina(sigla='MAC0520')
```

E a partir de uma disciplina, podemos obter os seus dados completos:
```python
>>> dados = disciplina.obter_dados()
>>> dados["nome"]
'Teoria dos Grafos'
>>> dados["departamento"]
'Ciência da Computação'
>>> dados["carga horaria total"]
'60 h'
>>> dados["ementa"]
'Conexidade. Emparelhamentos. Coloração de vértices. Problemas extremais. Grafos planares. Fluxos e colorações. Grafos menores.\nConnectivity. Matchings. Vertex colouring. Extremal problems. Planar graphs. Flows and colouring. Minors.'
>>> dados["requisitos"]
{'45052 Bacharelado em Ciência da Computação (integral)': [[Requisito(sigla='MAC0320',tipo='requisito')]]}
```

#### Obter instituto pelo código

Caso já conheça o código do instituto, é possível instanciá-lo diretamente:
```python
>>> from jupiterweb import Instituto
>>> instituto = Instituto("27", "Escola de Comunicações e Artes", "Butantã", "ECA")
>>> disciplinas_instituto = instituto.obter_disciplinas()
>>> disciplinas_instituto[30]
Disciplina(sigla='CAP0260')
```

#### Obter disciplina pela sigla

Da mesma forma, é possível instanciar uma disciplina diretamente por sua sigla:
```python
>>> from jupiterweb import Disciplina
>>> disciplina = Disciplina("MAT0112")
>>> dados = disciplina.obter_dados()
>>> dados["nome"]
'Vetores e Geometria'
>>> dados["departamento"]
'Matemática'
```

## 🔍 Detalhes de implementação

No geral, o uso da biblioteca é simples. Porém, alguns detalhes merecem atenção.

#### Lazy loading

Como o processo de scraping pode ser demorado, os dados da classe `Instituto` e `Disciplina` são carregados sob demanda.
Um objeto `Instituto` recém-criado não contém disciplinas.
Elas são carregadas apenas na primeira chamada de `Instituto.obter_disciplinas()`.
A partir daí, o resultado fica armazenado no objeto, e as chamadas subsequentes retornam o cache sem realizar scraping novamente.
O mesmo vale para objetos `Disciplina` — os dados são obtidos somente na primeira chamada de `Disciplina.obter_dados()`, e ficam armazenados no objeto a partir daí.

```python
>>> from jupiterweb import Disciplina
>>> disciplina = Disciplina("FLT0123") # vazia (sem dados)
>>> disciplina.obter_dados() # faz scraping (devagar)
{'sigla': 'FLT0123',
 'instituto': 'Faculdade de Filosofia, Letras e Ciências Humanas',
 ... }
>>> disciplina.obter_dados() # retorna cache (rápido)
{'sigla': 'FLT0123',
 'instituto': 'Faculdade de Filosofia, Letras e Ciências Humanas',
 ... }
```

#### Dados da disciplina

A função `Disciplina.obter_dados()` retorna um dicionário com as informações obtidas no scraping da disciplina, como a seguir
```python
>>> from jupiterweb import Disciplina
>>> disciplina = Disciplina("CBM0190")
>>> disciplina.obter_dados()
{
    'sigla': 'CBM0190',
    'instituto': 'Centro de Biologia Marinha',
    'departamento': 'Centro de Biologia Marinha',
    'nome': 'Conservação Marinha',
    ...
    'ementa': 'Serão apresentadas informações sobre:\n1) o histórico da di'...,
    'objetivos': 'A disciplina tem como objetivos:\n1) apresentar os princ'...,
    'conteudo programatico': '- Histórico da conservação marinha no mundo '...,
    'viagem didatica': {
        'e estruturante?': 'Sim',
        'atividades a serem desenvolvidas': 'As atividades práticas desta '...,
    },
    'instrumentos e criterios de avaliacao': {
        'metodo de avaliacao': 'Uma prova escrita, atividades teórico-prát'...,
        'criterio de avaliacao': 'Prova escrita 30%\nAtividades teórico-pr'...,
        'norma de recuperacao': 'Sem recuperação.',
    },
    ...
    'requisitos': {},
    'periodo ideal': {},
    'oferecimento': [],
}
```

É importante notar que **as chaves do dicionário de dados variam de disciplina para disciplina**, dependendo das informações disponíveis no Jupiterweb. Enquanto algumas chaves são esperadas em todas as disciplinas (como "sigla", "nome", "requisitos", etc.), outras podem ser exclusivas de algumas disciplinas (como "viagem didatica" acima).

O processo de scraping da página principal da disciplina no Jupiterweb percorre todos os campos disponíveis ("Ementa", "Instrumentos e Critérios de Avaliação", "Créditos Aula", etc.) e converte os seus títulos para minúsculo e sem acentos ("ementa", "instrumentos e criterios de avaliacao", "creditos aula", etc.) para usar como chaves no dicionário.
Já outras informações, como requisitos, período ideal e oferecimento, são obtidas a partir de páginas específicas do Jupiterweb, e por isso ficam em chaves fixas ("requisitos", "periodo ideal" e "oferecimento", respectivamente).

Algumas seções da página principal da disciplina possuem subseções, como "Viagem Didática" e "Instrumentos e Critérios de Avaliação" acima. Nesses casos, os dados são organizados em um dicionário aninhado, onde as chaves do dicionário interno correspondem aos títulos das subseções ("e estruturante?", "atividades a serem desenvolvidas", "método de avaliação", "critério de avaliação", etc.).

#### Requisitos da disciplina

No Jupiterweb, os requisitos de uma disciplina são organizados em cursos.
Para cada curso, os requisitos são organizados em conjuntos de alternativas: o aluno daquele curso deve satisfazer um conjunto **ou** outro.
Ou seja, os requisitos podem ser da forma
> "Para fazer a disciplina *X*, o aluno do curso *123* precisa ter cursado as disciplinas *A* e *B*, ou ter cursado as disciplinas *C* e *D*, ou ter cursado a disciplina *E*."

A imagem abaixo mostra que, para fazer a disciplina "*MAE0227 - Probabilidade II*", alunos do curso "*45031 Matemática - Bacharelado (integral)*" precisam ter cursado as disciplinas "*MAE0127*" e "*MAT2453*", **ou** ter cursado a disciplina "*MAE0121*":

![Requisitos de MAE0227 no Jupiterweb](https://raw.githubusercontent.com/davigole/jupiterweb-scraper/refs/heads/main/images/exemplo_requisitos_1.png)

Uma mesma disciplina pode estar em dois grupos de alternativas. Por exemplo, para fazer "*MAT0334 - Análise Funcional*", alunos do curso "*45031 Matemática - Bacharelado*" devem ter cursado "*MAT0222*" e "*MAT0311*", ou ter cursado "*MAT0222*" e "*MAT0317*" (então "*MAT0222*" é obrigatória):

![Requisitos de MAT0334 no Jupiterweb](https://raw.githubusercontent.com/davigole/jupiterweb-scraper/refs/heads/main/images/exemplo_requisitos_2.png)

Para representar essa estrutura, os requisitos de uma disciplina ficam armazenados em um dicionário, cujas chaves são cursos, e os valores são as listas de alternativas correspondentes. Cada alternativa é uma lista de requisitos. Por exemplo, `disciplina.obter_dados()["requisitos"] = {'CURSO': [[x, y], [w, z]]}` mostra que, para cursar a `disciplina`,alunos de `"CURSO"` devem ter cumprido os requisitos `x` e `y`, **ou** os requisitos `w` e `z`.
O código abaixo elucida essa ideia:

```python
>>> from jupiterweb import Disciplina
>>> disciplina = Disciplina("MAE0227")
>>> dados = disciplina.obter_dados()
>>> dados["requisitos"]
{
    '45031 Matemática - Bacharelado (integral)': [
        [Requisito(sigla='MAE0127',tipo='requisito'), Requisito(sigla='MAT2453',tipo='requisito')],
        [Requisito(sigla='MAE0121',tipo='requisito')]
    ],
    '45062 Estatística - Bacharelado (integral)': [
        [Requisito(sigla='MAE0127',tipo='requisito'), Requisito(sigla='MAT2453',tipo='requisito')]
    ]
}
```

Cada requisito é representado como um objeto da classe `Requisito`, que armazena a sigla da disciplina que exige, e o tipo do requisito (em letras minúsculas).
No Jupiterweb, alguns requisitos possuem tipos especiais ("requisito fraco", "indicação de conjunto", etc.) Por exemplo,

![Requisitos de RCG4041 no Jupiterweb](https://raw.githubusercontent.com/davigole/jupiterweb-scraper/refs/heads/main/images/exemplo_requisitos_3.png)

Os requisitos do tipo "*Indicação de Conjunto*" acima ficam armazenados como a seguir:
```python
>>> from jupiterweb import Disciplina
>>> disciplina = Disciplina("RCG4041")
>>> dados = disciplina.obter_dados()
>>> dados["requisitos"]
{
    '17200 Terapia Ocupacional (noturno)': [
        [Requisito(sigla='RCG4040',tipo='indicação de conjunto'), Requisito(sigla='RCG3052',tipo='requisito')]
    ],
    '17201 Terapia Ocupacional (integral)': [
        [Requisito(sigla='RCG4040',tipo='indicação de conjunto'), Requisito(sigla='RCG3052',tipo='requisito')]
    ]
}
```

Também é possível obter o período ideal da disciplina para cada curso, que fica disponível na página de requisitos de Jupiterweb. Esses dados ficam armazenados em um dicionário semelhante ao de requisitos:
```python
>>> from jupiterweb import Disciplina
>>> disciplina = Disciplina("MAE0501")
>>> dados = disciplina.obter_dados()
>>> dados["periodo ideal"]
{
    '12042 Bacharelado em Ciências Atuariais (noturno)': 6,
    '45061 Estatística - Bacharelado (integral)': 8,
    '45062 Estatística - Bacharelado (integral)': 6,
}
```

## 🤝 Como contribuir

Caso queira contribuir mas não saiba por onde começar, aqui estão algumas melhorias e funcionalidades que ainda não foram implementadas:

- Buscar disciplinas por parte do nome, horário, vagas remanescentes, etc. (o Jupiterweb já tem essas funcionalidades)
- Obter os cursos oferecidos por cada unidade e informações sobre cada curso (descrição, objetivos, grade curricular, etc.), disponíveis na seção "Cursos de ingresso" do Jupiterweb
- Obter informações sobre docentes (nome, instituto, departamento, disciplinas que ministra/ministrou, etc.)
- Obter informações do calendário escolar, disponível em PDF no Jupiterweb
- Controle de erros mais robusto, para lidar com as inconsistências do Jupiterweb
- Carregamento segmentado dos dados da disciplina, para evitar que o processo de scraping demore muito (por exemplo, para obter apenas o nome da disciplina, não deveríamos fazer scraping das páginas de requisitos e de oferecimento)
- Testes automáticos para verificar o funcionamento do scraping
- Documentação mais completa e exemplos de uso
- Qualquer alteração nas funções de scraping que torne a biblioteca mais robusta

Contribuições são muito bem-vindas!

## 📄 Licença

MIT © [IME Jr](https://imejr.com/)
