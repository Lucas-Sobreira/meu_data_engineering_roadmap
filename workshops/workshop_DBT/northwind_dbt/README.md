link de referência Medium: <a href="https://medium.com/@pahlavan.maryam/streamlining-your-data-workflow-installing-dbt-postgres-with-docker-compose-and-makefile-bf60a2cc9390">link_medium</a>

# Repositório Clonado

Clique aqui para ir para o repositório do Luciano, conteúdo do DBT: <a href="https://github.com/lvgalvao/dbt-core-northwind-project">repo</a>

# Passo a Passo para rodar o DBT

1) Criar um Banco de Dados na AWS [RDS], outra Cloud ou até mesmo local. 
<img src="./imgs/AWS_RDS.png"></img>

2) Configurar o Banco de Dados com os Schemas das tabelas e os Dados. 
   Nesse caso, foi utilizado o "northwind.sql" como padrão de configuração do Banco.

3) Instalar o DBT: 
``` bash: 
poetry add dbt-postgres
```

4) Inicializar o DBT: 
``` bash: 
poetry shell
dbt init
```

5) Após setar as configurações: 
``` bash: 
dbt debug 
``` 

6) Rodar o DBT: 
``` bash: 
dbt run
```