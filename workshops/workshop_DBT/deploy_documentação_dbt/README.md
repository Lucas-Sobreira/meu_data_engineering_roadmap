Link para a aula do Luciano sobre o Deploy no Render e Documentação do Projeto: 
<a href="https://jornadadedados.alpaclass.com/c/cursos/YbsKtM?lessonSlug=7gzXTj">link aula</a>

# Deploy e Documentação do projeto de DBT Core 

- Deploy: 
    Durante a aula foi utilizado o Render para deploy do projeto. Qualquer nova atualização no Banco de Dados Postgres (AWS RDS), os reports ou os Data Marts eram afetados, atualizando automaticamente, seguindo o fluxo Staging -> Intermediate -> Reports/Marts.

    Sobre o deploy da documentação, foi utilizado o Workflow do Github. Toda e qualquer alteração do projeto, é atualizada automaticamente, bastando dar um "git pull" para a branch. 

Comandos para gerar a documentação do projeto: 
``` bash: 
dbt docs generate
dbt docs serve
``` 

# Organização do CTE (Common Table Expression)

## Staging
1) Import da ou das tabelas: 

``` sql 
with table_01 as (
    select * from table_01
), 

table_02 as (
    select * from table_02
)
```

2) Transform / Regra de Negócio: 

``` sql 
with result as (
    select 
        columns -- transformação ou seleção das colunas
    from 
        table_01
)
```

3) Final: 
``` sql 
select * from result
```

## Marts
1) Config
2) Import da(s) tabela(s)
3) Transform / Regra de Negócio
4) Final 