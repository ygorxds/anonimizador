# Documentação do Projeto Anonimizador

## 1. Instalação do Poetry no Windows

Para instalar o Poetry, abra o PowerShell como administrador e execute o comando abaixo:

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

## 2. Adicionar o Poetry ao PATH

Após a instalação, certifique-se de que o diretório do Poetry está no seu PATH. Normalmente, ele é instalado em:

```
C:\Users\SeuUsuario\AppData\Roaming\Python\Scripts
```

Para adicionar ao PATH:
- Abra as **Configurações do Sistema** e vá para **Variáveis de Ambiente**.
- Encontre **Path** em **Variáveis do Sistema** e edite.
- Adicione o caminho acima.

## 3. Instalação das Dependências do Projeto

Antes de rodar o projeto, você precisa instalar as dependências. Com o Poetry instalado, navegue até a pasta raiz do seu projeto (onde está o `pyproject.toml`) e execute:

```bash
poetry install
```

Isso instalará todas as dependências necessárias conforme especificado no arquivo `pyproject.toml`.

## 4. Instalação do spaCy e Streamlit

Certifique-se de que o `spaCy` e o `Streamlit` estão instalados. No terminal, ainda na pasta raiz do projeto, execute:

```bash
pip install spacy streamlit
```

Em seguida, baixe o modelo de linguagem em português do spaCy:

```bash
python -m spacy download pt_core_news_sm
```

## 5. Executar o Projeto

### Ativar o Ambiente Virtual

O Poetry cria um ambiente virtual para o projeto. Para ativá-lo, execute:

```bash
poetry shell
```

### Rodar a Aplicação Streamlit

Com o ambiente virtual ativo, inicie a aplicação Streamlit usando o comando abaixo:

```bash
streamlit run anonimizador/main.py
```

Isso abrirá o aplicativo no navegador padrão, permitindo que você utilize a interface para anonimizar informações sensíveis.
