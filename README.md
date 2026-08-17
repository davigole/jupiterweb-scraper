# Jupiterweb Scraper

![Python Version](https://img.shields.io/pypi/pyversions/jupiterweb-scraper)
![License](https://img.shields.io/github/license/davigole/jupiterweb-scraper)
[![PyPI](https://img.shields.io/pypi/v/jupiterweb-scraper)](https://pypi.org/project/jupiterweb-scraper/)

Biblioteca para extrair informações sobre disciplinas da Universidade de São Paulo a partir do [Jupiterweb](https://uspdigital.usp.br/jupiterweb/).

## 📖 Sobre o projeto

O **Jupiterweb Scraper** é uma biblioteca Python que permite extrair informações sobre disciplinas da USP a partir do [Jupiterweb](https://uspdigital.usp.br/jupiterweb/), o sistema oficial de gestão acadêmica da universidade.

Inicialmente, a biblioteca foi desenvolvida para atender às demandas de um projeto interno da [IME Jr](https://imejr.com/) — a empresa júnior do IME-USP. Com o tempo, percebemos que a obtenção de dados do Jupiterweb é uma necessidade recorrente em projetos voltados à comunidade USP. Por isso, decidimos disponibilizar o scraper como projeto open-source, com o intuito de facilitar o desenvolvimento de novas ferramentas destinadas à universidade.

> ⚠️ **Aviso:** O Jupiterweb é um site antigo, com uma estrutura HTML complexa e por vezes inconsistente, o que torna o processo de scraping desafiador. É esperado que a biblioteca contenha erros que ainda passaram despercebidos. Caso algum problema ou comportamento inesperado seja encontrado, pedimos que se abra uma [Issue](https://github.com/davigole/jupiterweb-scraper/issues) descrevendo o ocorrido.

## 🚀 Instalação

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

A biblioteca é organizada em três níveis: **institutos** têm **disciplinas**, e disciplinas têm **dados**.

```python
>>> import jupiterweb

# Institutos da USP
>>> institutos = jupiterweb.obter_institutos()
>>> instituto = institutos[37]
>>> instituto
Instituto(codigo='45',nome='Instituto de Matemática, Estatística e Ciência da Computação',campus='Butantã',abrev='IME')

# Disciplinas do instituto
>>> disciplinas = instituto.obter_disciplinas()
>>> disciplina = disciplinas[15]
>>> disciplina
Disciplina(sigla='MAC0323')

# Dados completos da disciplina
>>> dados = disciplina.obter_dados()
>>> dados = disciplina.obter_dados()
>>> dados["nome"]
'Algoritmos e Estruturas de Dados II'
>>> dados["departamento"]
'Ciência da Computação'
>>> dados["ementa"]
'Tipos abstratos de dados e suas implementações. Tabelas ...'
>>> dados.keys()
dict_keys([ 'instituto', 'departamento', 'nome', 'nome ingles',
            'creditos aula', 'creditos trabalho', 'carga horaria total',
            'tipo', 'ativacao', 'desativacao', 'ementa', 'objetivos',
            'conteudo programatico', 'instrumentos e criterios de avaliacao',
            'bibliografia', 'docente(s) responsavel(eis)',
            'requisitos', 'periodo ideal', 'oferecimento' ])
```

#### Instanciando diretamente

Quando o código do instituto ou a sigla da disciplina já são conhecidos, não é necessário passar por `obter_institutos()`: os objetos podem ser instanciados diretamente.

```python
>>> from jupiterweb import Instituto, Disciplina

# Obter instituto por código
>>> instituto = Instituto("27", "Escola de Comunicações e Artes", "Butantã", "ECA")
>>> instituto.obter_disciplinas()[30]
Disciplina(sigla='CCA0293')

# Obter disciplina por sigla
>>> disciplina = Disciplina("MAT0112")
>>> disciplina.obter_dados()["nome"]
'Vetores e Geometria'
```

#### Métodos auxiliares

Além de `obter_dados()`, a classe `Disciplina` oferece alguns métodos utilitários para o dia a dia:

```python
>>> disciplina = Disciplina("MAC0520")

>>> disciplina.encontrada()
True  # a disciplina foi encontrada no Jupiterweb?

>>> disciplina.possui_oferecimento()
False  # há alguma turma sendo oferecida atualmente?
```

## 🔍 Detalhes de implementação

O uso básico da biblioteca é simples, mas alguns pontos merecem atenção.

### Lazy loading e cache

Como o scraping pode ser demorado, os dados de `Instituto` e `Disciplina` são carregados sob demanda, e não na criação do objeto.

- Um `Instituto` recém-criado não contém disciplinas até a primeira chamada de `obter_disciplinas()`.
- Uma `Disciplina` recém-criada não contém dados até a primeira chamada de `obter_dados()`.

A partir da primeira chamada, o resultado fica em cache no próprio objeto, e chamadas seguintes não fazem scraping novamente:

```python
>>> disciplina = Disciplina("FLT0123")
>>> disciplina.obter_dados()  # faz scraping (mais lento)
>>> disciplina.obter_dados()  # retorna o cache (instantâneo)
```

Para forçar um novo scraping — por exemplo, para atualizar dados que podem ter mudado — use `force=True`, tanto em `Disciplina.obter_dados()` quanto em `Instituto.obter_disciplinas()`:

```python
>>> disciplina.obter_dados(force=True)  # faz scraping novamente
```

Analogamente,
```python
>>> institutos = jupiterweb.obter_institutos()
>>> instituto = institutos[21]
>>> instituto.obter_disciplinas()  # faz scraping (mais lento)
>>> instituto.obter_disciplinas()  # retorna o cache (instantâneo)
>>> instituto.obter_disciplinas(force=True)  # faz scraping novamente
```

### Dados da disciplina

`Disciplina.obter_dados()` retorna um dicionário como o abaixo:

```python
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

Um ponto importante: **as chaves desse dicionário variam de disciplina para disciplina**, dependendo do que está disponível no Jupiterweb.
As chaves `"sigla"`, `"instituto"`, `"departamento"`, `"nome"`, `"nome ingles"`, `"requisitos"`, `"periodo ideal"` e `"oferecimento"` aparecem em todas as disciplinas **válidas**. Já as outras, como `"viagem didatica"` acima, só estão presentes nas páginas de algumas disciplinas específicas.

A maior parte das chaves vem diretamente dos campos da página principal da disciplina no Jupiterweb ("Ementa", "Instrumentos e Critérios de Avaliação", "Créditos Aula", etc.). Os títulos desses campos são convertidos para minúsculo e sem acentos para formar as chaves (`"ementa"`, `"instrumentos e criterios de avaliacao"`, `"creditos aula"`, etc.). Quando um campo tem subseções — como "Viagem Didática" no exemplo acima —, o valor correspondente é um dicionário aninhado, com uma chave para cada subseção.

Já `"requisitos"`, `"periodo ideal"` e `"oferecimento"` são obtidos de páginas específicas do Jupiterweb (não da página principal) e por isso sempre aparecem, mesmo que vazios, com essas chaves fixas. Cada um é detalhado a seguir.

### Disciplinas inexistentes ou inválidas

Quando não é possível fazer o scraping da página principal — seja porque ela está vazia, seja porque houve algum erro ao encontrá-la — a disciplina é considerada carregada, mas **inexistente**. Nesse caso, obter_dados() retorna {}, e chamadas seguintes não tentam um novo scraping, a não ser que `force=True` seja passado. Como consequência, `disciplina.encontrada()` retorna `False`:

```python
>>> disciplina = Disciplina("ABC1234")
>>> disciplina.obter_dados()
{}
>>> disciplina.encontrada()
False
```

### Requisitos

No Jupiterweb, os requisitos de uma disciplina são organizados por curso. Para cada curso, os requisitos formam um ou mais conjuntos de alternativas: o aluno precisa satisfazer um conjunto **ou** outro. Ou seja, os requisitos seguem o tipo:

> "Para fazer a disciplina *X*, o aluno do curso *123* precisa ter cursado as disciplinas *A* e *B*, ou ter cursado as disciplinas *C* e *D*, ou ter cursado a disciplina *E*."

A imagem abaixo mostra que, para fazer "*MAE0227 - Probabilidade II*", alunos do curso "*45031 Matemática - Bacharelado (integral)*" precisam ter cursado "*MAE0127*" e "*MAT2453*", **ou** ter cursado apenas "*MAE0121*":

![Requisitos de MAE0227 no Jupiterweb](https://raw.githubusercontent.com/davigole/jupiterweb-scraper/refs/heads/main/images/exemplo_requisitos_1.png)

Uma mesma disciplina pode aparecer em mais de um grupo de alternativas — nesse caso, ela é obrigatória em ambos os caminhos. Por exemplo, para "*MAT0334 - Análise Funcional*", alunos do curso "*45031 Matemática - Bacharelado*" precisam ter cursado "*MAT0222*" e "*MAT0311*", ou ter cursado "*MAT0222*" e "*MAT0317*" ("*MAT0222*" é sempre necessária):

![Requisitos de MAT0334 no Jupiterweb](https://raw.githubusercontent.com/davigole/jupiterweb-scraper/refs/heads/main/images/exemplo_requisitos_2.png)

Essa estrutura é representada por um dicionário cujas chaves são os cursos, e cujos valores são listas de alternativas — cada alternativa sendo, por sua vez, uma lista de requisitos. Ou seja, `dados["requisitos"] = {'CURSO': [[x, y], [w, z]]}` significa que, para cursar a disciplina, alunos de `"CURSO"` precisam ter cumprido os requisitos `x` **e** `y`, **ou** os requisitos `w` **e** `z`:

```python
>>> disciplina = Disciplina("MAE0227")
>>> dados = disciplina.obter_dados()
>>> dados["requisitos"]
{'45031 Matemática - Bacharelado (integral)': [
        [Requisito(sigla='MAE0127',tipo='requisito'), Requisito(sigla='MAT2453',tipo='requisito')],
        [Requisito(sigla='MAE0121',tipo='requisito')]
    ],
    '45062 Estatística - Bacharelado (integral)': [
        [Requisito(sigla='MAE0127',tipo='requisito'), Requisito(sigla='MAT2453',tipo='requisito')]
    ]
}
```

Cada requisito é um objeto `Requisito`, que guarda a sigla da disciplina exigida e o tipo do requisito (em letras minúsculas). O Jupiterweb também usa tipos especiais, como "requisito fraco" e "indicação de conjunto":

```python
>>> disciplina = Disciplina("RCG4041")
>>> dados = disciplina.obter_dados()
>>> dados["requisitos"]
{'17200 Terapia Ocupacional (noturno)': [
        [Requisito(sigla='RCG4040',tipo='indicação de conjunto'), Requisito(sigla='RCG3052',tipo='requisito')]
    ],
    '17201 Terapia Ocupacional (integral)': [
        [Requisito(sigla='RCG4040',tipo='indicação de conjunto'), Requisito(sigla='RCG3052',tipo='requisito')]
    ]
}
```
![Requisitos de RCG4041 no Jupiterweb](https://raw.githubusercontent.com/davigole/jupiterweb-scraper/refs/heads/main/images/exemplo_requisitos_3.png)

A partir de um `Requisito`, é possível obter diretamente o objeto `Disciplina` correspondente:

```python
>>> req = dados["requisitos"]['17200 Terapia Ocupacional (noturno)'][0][0]
>>> req
Requisito(sigla='RCG4040',tipo='indicação de conjunto')
>>> req.obter_disciplina()
Disciplina(sigla='RCG4040')
```

### Período ideal

O período ideal de uma disciplina também é organizado por curso, e fica disponível na mesma página de requisitos do Jupiterweb. Os dados ficam em um dicionário simples, mapeando curso para o semestre recomendado:

```python
>>> disciplina = Disciplina("MAE0501")
>>> dados = disciplina.obter_dados()
>>> dados["periodo ideal"]
{
    '12042 Bacharelado em Ciências Atuariais (noturno)': 6,
    '45061 Estatística - Bacharelado (integral)': 8,
    '45062 Estatística - Bacharelado (integral)': 6,
}
```

### Oferecimento (turmas)

A chave `"oferecimento"` traz a lista de turmas já abertas para a disciplina, cada uma representada por um objeto `Oferecimento`. Cada `Oferecimento` guarda dados básicos da turma (código, datas de início e fim, tipo de turma, observações), além de:

- **`horarios`**: lista de objetos `HorarioAula`, cada um com dia da semana, horário de início e fim, e o professor responsável.
- **`vagas`**: dicionário com as vagas oferecidas no oferecimento, por tipo (ex.: vagas para a USP, vagas remanescentes) e por curso, conforme disponibilizado na página de oferecimento do Jupiterweb.

```python
>>> disciplina = Disciplina("MAC0110")
>>> dados = disciplina.obter_dados()
>>> oferecimento = dados["oferecimento"]
>>> turma = oferecimento[0]
>>> turma
Oferecimento(codigo='2026247',data_inicio='03/08/2026',data_fim='12/12/2026',tipo_turma='teórica',observacoes='',sigla_disciplina='MAC0110')

>>> turma.horarios
[
    HorarioAula(dia_semana='ter',hora_inicio='21:10',hora_fim='22:50',professor='(R) Alair Pereira do Lago'),
    HorarioAula(dia_semana='sex',hora_inicio='19:20',hora_fim='21:00',professor='(R) Alair Pereira do Lago')
]

>>> turma.vagas
{
    'obrigatoria': {
        'vagas': 65,
        'inscritos': 51,
        'pendentes': 0,
        'matriculados': 51,
        'cursos': {
            'IME - Matemática Licenciatura Noturno': {'vagas': 60, 'inscritos': 43, 'pendentes': 0, 'matriculados': 43},
            'IME - Matemática Licenciatura Matutino': {'vagas': 5, 'inscritos': 4, 'pendentes': 0, 'matriculados': 4}
        }
    },
    'optativa livre': {
        'vagas': 7,
        'inscritos': 7,
        'pendentes': 0,
        'matriculados': 7,
        'cursos': {
            'IB - Licenciatura Diurno ou Noturno': {'vagas': 3, 'inscritos': 1, 'pendentes': 0, 'matriculados': 1},
            'EACH - Lic Ciências da Natureza - Noturno': {'vagas': 3, 'inscritos': 1, 'pendentes': 0, 'matriculados': 1},
            'FFLCH - Letras - Linguística (Bach.)': {'vagas': 1, 'inscritos': 0, 'pendentes': 0, 'matriculados': 0},
            'Qualquer Unidade da USP': {'vagas': 0, 'inscritos': 0, 'pendentes': 0, 'matriculados': 0}
        }
    }
}
```
![Oferecimento de Turma de MAC0110](https://raw.githubusercontent.com/davigole/jupiterweb-scraper/refs/heads/main/images/exemplo_oferecimento_1.png)


As chaves dentro de `vagas` (nomes dos tipos de vaga e das colunas, como `"oferecidas"`) seguem exatamente o que está disponível na página do Jupiterweb, e podem variar de disciplina para disciplina.

## 🤝 Como contribuir

Para quem quiser contribuir mas não sabe por onde começar, seguem algumas melhorias e funcionalidades ainda não implementadas:

- Buscar disciplinas por parte do nome, horário, vagas remanescentes, etc. (o Jupiterweb já tem essas funcionalidades)
- Obter os cursos oferecidos por cada unidade e informações sobre cada curso (descrição, objetivos, grade curricular, etc.), disponíveis na seção "Cursos de ingresso" do Jupiterweb
- Obter informações sobre docentes (nome, instituto, departamento, disciplinas que ministra/ministrou, etc.)
- Obter informações do calendário escolar, disponível em PDF no Jupiterweb
- Controle de erros mais robusto, para lidar com as inconsistências do Jupiterweb
- Carregamento segmentado dos dados da disciplina, para evitar que o processo de scraping demore muito (por exemplo, para obter apenas o nome da disciplina, não seria necessário fazer scraping das páginas de requisitos e de oferecimento)
- Testes automáticos para verificar o funcionamento do scraping
- Documentação mais completa e exemplos de uso
- Qualquer alteração nas funções de scraping que torne a biblioteca mais robusta

Contribuições são muito bem-vindas!

## 📄 Licença

MIT © [IME Jr](https://imejr.com/)
