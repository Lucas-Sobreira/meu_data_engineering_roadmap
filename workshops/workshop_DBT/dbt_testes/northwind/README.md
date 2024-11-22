# Criando a Staging
Além de criar a stg_order.sql e a stg_customers.sql, é necessário criar o arquivo schema.yml para dizer o comportamento esperado por cada tabela dessas.

Sempre que quiser rodar seus testes, criar os arquivos de models e source além do comendo SQL desejado para a camada em questão.
``` bash: 
dbt run
```

Após criado ai sim, rodar o test

``` bash: 
dbt test
```

Caso queira pegar o log 
``` bash: 
dbt test | tee -a test.txt
```