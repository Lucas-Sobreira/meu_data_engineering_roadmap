link de referência Medium: <a href="https://medium.com/@pahlavan.maryam/streamlining-your-data-workflow-installing-dbt-postgres-with-docker-compose-and-makefile-bf60a2cc9390">link_medium</a>
aula Luciano Galvao: <a href="https://jornadadedados.alpaclass.com/c/cursos/YbsKtM?lessonSlug=3kzubm">aula_ao_vivo</a>

# Repositório Clonado

Clique aqui para ir para o repositório do Luciano, conteúdo do DBT: <a href="https://github.com/lvgalvao/dbt-core-northwind-project">repo</a>

# Passo a Passo para rodar o DBT

1) Instalar o DBT: 
``` bash: 
poetry add dbt-postgres
```

2) Inicializar o DBT: 
``` bash: 
poetry shell
dbt init
```

3) Após setar as configurações: 
``` bash: 
dbt debug 
``` 

4) Rodar o DBT: 
``` bash: 
dbt run
```

## Criando Banco de Dados AWS

Foi acessado o portal da AWS e criada uma instância do <b>AWS RDS</b>.