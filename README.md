# 🌿 Sentinela Paranoá

### Monitoramento Ambiental Comunitário — Ciência Cidadã

**Desenvolvedor:** Atan Pinho  
**Área de desenvolvimento:** Engenharia de Software e Ciências da Computação  
**Local de atuação do projeto:** Lago Paranoá e seus afluentes — Brasília, Distrito Federal  
**Ano:** 2026

---

## 1. Apresentação

O **Sentinela Paranoá** é uma aplicação de monitoramento ambiental comunitário voltada à observação e ao registro de possíveis ocorrências ambientais no Lago Paranoá e em seus afluentes, em Brasília, Distrito Federal.

O projeto utiliza a tecnologia como instrumento de participação cidadã, permitindo que visitantes registrem situações que mereçam atenção por meio de descrições, fotografias e informações de localização geográfica, quando disponíveis.

Sua proposta é aproximar a comunidade da preservação ambiental, organizando informações que possam contribuir para o acompanhamento e a conscientização sobre as condições ambientais da região.

A ideia central é transformar a participação das pessoas em uma ferramenta de apoio à observação e à preservação dos recursos naturais.

**Cada cidadão pode ser um sentinela do meio ambiente.**

## 2. Objetivos

- Incentivar a participação da comunidade no monitoramento ambiental.
- Facilitar o registro de possíveis ocorrências ambientais.
- Permitir o envio de fotografias para contextualizar os relatos.
- Registrar coordenadas geográficas quando o visitante autorizar a localização.
- Apresentar em mapa as ocorrências que possuem coordenadas.
- Organizar os registros para consulta e acompanhamento.
- Estimular a consciência ambiental e a colaboração cidadã.

Os registros representam relatos enviados pela comunidade. Eles não constituem, por si só, comprovação de infrações ou de danos ambientais.

## 3. Funcionalidades

O sistema reúne as seguintes funcionalidades:

- **Painel ambiental:** apresenta indicadores gerais sobre os registros.
- **Registro de ocorrências:** permite informar o tipo de ocorrência, a descrição e o local.
- **Envio de fotografias:** recebe imagens anexadas ao formulário e realiza validações antes do armazenamento.
- **Geolocalização:** permite solicitar a localização do dispositivo, mediante autorização do visitante.
- **Mapa interativo:** apresenta marcadores das ocorrências que possuem coordenadas geográficas.
- **Consulta de ocorrências:** permite pesquisar registros por descrição, local e tipo.
- **Comentários da comunidade:** disponibiliza um espaço para participação dos visitantes.

A localização GPS é opcional. O formulário atual exige o envio de uma fotografia.

## 4. Tecnologias utilizadas

| Tecnologia | Função no projeto |
|---|---|
| Python | Linguagem principal da aplicação. |
| FastAPI | Framework utilizado para construir a aplicação e suas rotas. |
| Uvicorn | Servidor utilizado para executar a aplicação. |
| SQLite | Banco de dados para armazenamento dos registros. |
| HTML | Estrutura das páginas. |
| CSS | Estilização e apresentação visual. |
| JavaScript | Interações executadas no navegador. |
| Jinja2 | Integração entre os dados do Python e os modelos HTML. |
| Leaflet | Biblioteca utilizada para construir o mapa interativo. |
| OpenStreetMap | Fonte dos dados cartográficos exibidos no mapa. |
| Pillow | Biblioteca utilizada para abrir e validar imagens. |

## 5. Estrutura de pastas e arquivos

A aplicação está organizada em diretórios que separam a lógica do sistema, os arquivos estáticos, os modelos das páginas e os dados armazenados.

```text
sentinela-paranoa/
│
├── .gitignore
├── inserir_dados.py
├── requirements.txt
├── sentinela.db
│
└── app/
    │
    ├── api/
    │   ├── banco.py
    │   └── main.py
    │
    ├── static/
    │   ├── estilo.css
    │   ├── mapa-1.png
    │   └── fotos/
    │
    └── templates/
        ├── index.html
        └── ocorrencias.html
```

### Responsabilidade dos principais arquivos

- **`banco.py`:** inicializa o banco de dados e organiza a estrutura das tabelas.
- **`main.py`:** controla as rotas da aplicação, recebe formulários, consulta e registra informações.
- **`estilo.css`:** contém regras de apresentação visual.
- **`mapa-1.png`:** arquivo de imagem utilizado pelo projeto.
- **`fotos/`:** armazena as fotografias enviadas nas ocorrências.
- **`index.html`:** apresenta o painel principal, o mapa, o formulário de ocorrências e os comentários.
- **`ocorrencias.html`:** apresenta a consulta dos registros, com pesquisa e filtros.
- **`inserir_dados.py`:** script auxiliar para inserção de dados.
- **`requirements.txt`:** registra as dependências Python e suas versões.
- **`sentinela.db`:** arquivo do banco de dados SQLite.
- **`.gitignore`:** arquivo destinado a definir quais arquivos e pastas devem ser ignorados pelo Git.

A pasta `__pycache__`, criada automaticamente pelo Python, contém arquivos auxiliares de execução e não é necessária para compreender a estrutura principal do projeto.

## 6. Preparação do ambiente

Para executar o projeto localmente, é necessário ter o Python instalado e utilizar um terminal, como o PowerShell do Windows.

### 6.1. Acessar a pasta do projeto

No terminal, entre na pasta principal do projeto.

Exemplo de caminho utilizado durante o desenvolvimento:

```powershell
cd "C:\Users\Usuário\Documents\GitHub\sentinela-paranoa"
```

### 6.2. Instalar as dependências

O arquivo `requirements.txt` registra as bibliotecas utilizadas e suas respectivas versões:

```text
fastapi==0.160.0
uvicorn==0.54.0
Jinja2==3.1.6
python-multipart==0.0.32
Pillow==13.0.0
```

Para instalar as dependências, execute:

```powershell
python -m pip install -r requirements.txt
```

### 6.3. Executar a aplicação

A partir da pasta principal do projeto, execute:

```powershell
python -m uvicorn app.api.main:app --reload
```

O servidor disponibiliza a aplicação localmente no endereço:

http://127.0.0.1:8000

Para encerrar a execução, utilize `Ctrl + C` no terminal.

## 7. Como funciona o registro de uma ocorrência

O fluxo básico de registro segue esta sequência:

1. O visitante acessa o painel principal.
2. Seleciona o tipo de ocorrência ambiental.
3. Preenche a descrição e informa o local.
4. Anexa uma fotografia.
5. Se desejar, autoriza o navegador a obter sua localização.
6. Envia o formulário.
7. A aplicação recebe e valida as informações e a fotografia.
8. Os dados são registrados no banco SQLite e a fotografia é armazenada na pasta destinada aos arquivos.
9. A ocorrência passa a integrar a consulta. Se possuir coordenadas geográficas, também poderá ser representada no mapa.

## 8. Banco de dados

O projeto utiliza **SQLite**, um sistema de banco de dados que armazena informações em um arquivo local.

A estrutura contempla duas tabelas principais:

### Tabela `ocorrencias`

Armazena informações como:

- Identificador do registro.
- Tipo de ocorrência.
- Descrição.
- Local informado.
- Data do registro.
- Latitude e longitude, quando disponíveis.
- Precisão informada pelo dispositivo, quando disponível.
- Data da captura da localização, quando disponível.
- Referência ao arquivo fotográfico.

### Tabela `comentarios`

Armazena:

- Identificador do comentário.
- Nome informado pelo visitante, quando fornecido.
- Mensagem.
- Data do registro.

## 9. Privacidade e proteção de dados

O Sentinela Paranoá recebe informações fornecidas pelos visitantes, como descrições, fotografias, comentários e, quando autorizadas, coordenadas geográficas.

O tratamento dessas informações deverá observar a legislação brasileira de proteção de dados pessoais, especialmente a **Lei Geral de Proteção de Dados (LGPD)**.

A política de privacidade do projeto deverá apresentar, de forma clara, quais informações são coletadas, suas finalidades, como são armazenadas e quais são os direitos dos titulares.

A publicação do projeto deverá considerar também a proteção dos dados presentes no banco de dados e nos arquivos fotográficos.

## 10. Propósito social e ambiental

O Sentinela Paranoá parte de uma ideia: a preservação ambiental também depende da participação das pessoas.

A tecnologia funciona como instrumento de organização, colaboração e observação cidadã.

Cada registro pode contribuir para ampliar o conhecimento sobre situações que merecem atenção no Lago Paranoá e em seus afluentes.

**A comunidade observa. A tecnologia conecta. A informação contribui para a preservação.**

## 11. Desenvolvimento e aprendizado

O Sentinela Paranoá também representa uma experiência prática de aprendizagem em Engenharia de Software e Ciências da Computação.

Sua construção envolve planejamento, organização de arquivos, programação, banco de dados, desenvolvimento web, geolocalização, validação de imagens e integração de tecnologias.

O processo de desenvolvimento é documentado no projeto educacional:

**EU E IA — REPETIÇÃO NÃO É REGRESSÃO**

A proposta é registrar não apenas o resultado, mas também o raciocínio, as decisões, as dificuldades e os aprendizados envolvidos na construção.

---

**Sentinela Paranoá — Ciência Cidadã e Monitoramento Ambiental.**

Desenvolvido por Atan Pinho.