## Pipeline que será construída

<p align="center">
<img src="imgs/arquitetura.png" width="500"></img> 
</p>

<p align="justify">
Esse projeto tem um código Python, responsável por 4 principais etapas: 
</p>

- Checar se tem arquivos novos na pasta Source; 
- Transformar o arquivo .csv em .parquet e .json; 
  - Utilizando PyArrow para o Parquet; 
  - Pandas para o Json;
- Realizar o upload dos arquivos .parquet para a AWS S3; 
- Deletar os arquivos da pasta local, Source;

Isso tudo sendo orquestrado pelo Apache Airflow;

## Configurando o Ambiente

<h2>Baixando as bibliotecas necessárias</h2>
<ul>
    <li>Pandas: Para trabalhar com Data Frames;</li>
    <li>Boto3: Biblioteca de comunicação com a AWS;</li>
    <li>PyArrow: Biblioteca para trabalhar com arquivos Parquet, utilizando Python;</li>
    <li>python-dotenv: Para leitura das variaveis de ambiente;</li>
</ul>

### Airflow - Astro CLI

Para download e configurações do Astro CLI: 
<a href='https://www.astronomer.io/docs/astro/cli/install-cli/'>link</a>

```cmd
   astro dev init
   astro dev start
```

#### Fluxo das Dags
<p align="center">
  <a><img src="./imgs/dags_graph_01.png" width="700"></a>
</p>

<p align="center">
  <a><img src="./imgs/dags_graph_02.png" width="700"></a>
</p>

#### Execução das Dags
<p align="center">
  <a><img src="./imgs/trigger_dags.png" width="200"></a>
</p>


## Alteração de Policies S3
Dentro das Policies do Bucket, ainda é mandatório alterar o JSON da política para aceitar que seja alterado qualquer tipo de arquivo.

<p align="center">
  <a><img src="./imgs/policy_S3_save_files.png" width="500"></a>
</p>

## AWS Glue
Para casos em que não sabemos muito bem o esquema, a estrutura dos dados. Ele nos ajuda a descobrir isso e a catalogar.

1) Cria um Database; 
2) Cria um Crawler;

Configurando o Crawler, para ler todos os itens dentro da pasta selecionada do S3.
Isso é importante por que ele pode ler qualquer sub item, sendo pasta ou arquivo. 
<p align="center">
  <a><img src="./imgs/glue_crawler.png" width="500"></a>
</p>

## Consumindo os Dados - Athena 

### Lendo dados do arquivo Parquet enviado ao S3
<p align="center">
  <a><img src="./imgs/query_result.png" width="500"></a>
</p>

### Criando uma tabela utilizando o Athena 
<p align="center">
  <a><img src="./imgs/quantity_type.png" width="500"></a>
</p>