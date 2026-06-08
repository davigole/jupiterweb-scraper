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

*A fazer*

## 🤝 Como contribuir

Caso queira contribuir mas não saiba por onde começar, aqui estão algumas melhorias e funcionalidades que ainda não foram implementadas:

- Buscar disciplinas por parte do nome, horário, vagas remanescentes, etc. (o Jupiterweb já tem essas funcionalidades)
- Obter os cursos oferecidos por cada unidade e informações sobre cada curso (descrição, objetivos, grade curricular, etc.), disponíveis na seção "Cursos de ingresso" do Jupiterweb
- Obter informações sobre docentes (nome, instituto, departamento, disciplinas que ministra/ministrou, etc.)
- Obter informações do calendário escolar, disponível em PDF no Jupiterweb
- Testes automáticos para verificar o funcionamento do scraping
- Documentação mais completa e exemplos de uso
- Qualquer alteração nas funções de scraping que torne a biblioteca mais robusta

Contribuições são muito bem-vindas!

## 📄 Licença

MIT © [IME Jr](https://imejr.com/)
