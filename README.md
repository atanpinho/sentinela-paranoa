# 🌿 Sentinela Paranoá

**Uma iniciativa de monitoramento ambiental comunitário**

Desenvolvi o Sentinela Paranoá como um projeto de Ciência Cidadã voltado ao registro colaborativo de possíveis ocorrências ambientais na região do Lago Paranoá e de seus afluentes, em Brasília (DF).

Minha proposta é aproximar a comunidade do monitoramento ambiental, permitindo que moradores e visitantes contribuam com informações sobre situações que mereçam atenção.

> **Status do projeto:** protótipo funcional com testes manuais realizados.
>
> Concluí uma rodada de testes das funcionalidades implementadas. Os resultados confirmam o funcionamento observado durante esses testes, mas não representam uma certificação de segurança nem garantem que a aplicação esteja pronta para uso público em produção.

## 1. Objetivo

Criei o Sentinela Paranoá para facilitar a participação da comunidade no acompanhamento de possíveis problemas ambientais.

Acredito que moradores e visitantes podem contribuir com a preservação do território quando encontram meios simples de registrar aquilo que observam. Por isso, adoto a ideia de que cada participante pode atuar como uma **sentinela ambiental**.

O projeto busca reunir informações que possam apoiar a observação, a consulta e a avaliação de ocorrências ambientais.

## 2. Funcionalidades implementadas

No estágio atual, o sistema permite:

- Registrar ocorrências ambientais por meio de formulário.
- Selecionar o tipo de ocorrência, incluindo descarte irregular de lixo.
- Enviar fotografias obrigatórias associadas aos registros.
- Validar as imagens recebidas antes de armazená-las.
- Armazenar fotografias e informações correspondentes no sistema.
- Publicar a fotografia junto com a ocorrência na página de ocorrências, no momento do envio.
- Solicitar a localização do dispositivo por GPS.
- Registrar uma ocorrência mesmo sem informar coordenadas geográficas.
- Consultar a listagem de ocorrências registradas.
- Visualizar no mapa as ocorrências que possuem coordenadas disponíveis.
- Registrar comentários da comunidade.

Essas funcionalidades foram verificadas durante os testes manuais que realizei.

A publicação da ocorrência e de sua fotografia acontece antes da análise ambiental. Portanto, o registro publicado deve ser entendido como um relato comunitário ainda não confirmado, e não como comprovação de infração ou dano ambiental.

## 3. Tecnologias utilizadas

Para desenvolver o projeto, utilizei:

- **Python:** linguagem de programação principal.
- **FastAPI:** estrutura utilizada para construir a aplicação web e suas rotas.
- **SQLite:** banco de dados utilizado para armazenar as informações.
- **Leaflet:** biblioteca JavaScript utilizada na exibição do mapa interativo.
- **HTML:** linguagem utilizada na estrutura das páginas.
- **CSS:** linguagem utilizada na apresentação visual.
- **JavaScript:** linguagem utilizada nas interações da interface.
- **Uvicorn:** servidor utilizado para executar a aplicação.
- **Jinja2:** ferramenta utilizada na integração entre os dados da aplicação e os modelos HTML.
- **Pillow:** biblioteca utilizada na validação das fotografias.

## 4. Estrutura do projeto

Organizei os arquivos do projeto da seguinte maneira:

```text
sentinela-paranoa/
├── app/
│   ├── api/
│   │   ├── banco.py
│   │   └── main.py
│   ├── static/
│   │   ├── fotos/
│   │   ├── estilo.css
│   │   └── mapa-1.png
│   └── templates/
│       ├── index.html
│       ├── ocorrencias.html
│       └── politica_privacidade.html
├── backups/
├── .gitignore
├── inserir_dados.py
├── README.md
├── requirements.txt
└── sentinela.db
```

A pasta `__pycache__` é criada automaticamente pelo Python e contém arquivos auxiliares de execução.

A pasta `fotos` armazena as imagens enviadas nas ocorrências, enquanto `backups` reúne cópias de segurança do banco de dados e das fotografias.

O banco `sentinela.db` fica na pasta principal do projeto. O arquivo `.gitignore` define quais arquivos e pastas locais não devem ser enviados ao repositório Git.

## 5. Como executar localmente

### 5.1. Pré-requisitos

Para executar o projeto, é necessário ter:

- Python instalado.
- Os arquivos do projeto disponíveis no computador.
- As dependências indicadas em `requirements.txt`.

Na pasta principal do projeto, instale as dependências com:

```powershell
python -m pip install -r requirements.txt
```

### 5.2. Iniciar a aplicação

No PowerShell, acesse a pasta principal do projeto e execute:

```powershell
python -m uvicorn app.api.main:app --reload
```

Depois que o servidor iniciar, acesse no navegador:

```text
http://127.0.0.1:8000
```

O parâmetro `--reload` facilita o desenvolvimento local, reiniciando o servidor quando há alterações no código. Ele não deve ser utilizado como configuração de produção.

## 6. Fluxo básico de utilização

O fluxo de utilização que implementei é:

1. A pessoa acessa a página inicial do Sentinela Paranoá.
2. Escolhe o tipo de ocorrência ambiental.
3. Preenche as informações solicitadas.
4. Pode solicitar a localização do dispositivo por GPS.
5. Pode registrar a ocorrência mesmo sem informar coordenadas.
6. Anexa uma fotografia, obrigatória no formulário atual.
7. Envia o formulário