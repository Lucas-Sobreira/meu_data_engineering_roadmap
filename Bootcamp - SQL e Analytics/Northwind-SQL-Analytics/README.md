# Relatórios Avançados em SQL Northwind

## Objetivo

Este repositório tem como objetivo apresentar relatórios avançados construídos em SQL. As análises disponibilizadas aqui podem ser aplicadas em empresas de todos os tamanhos que desejam se tornar mais analíticas. Através destes relatórios, organizações poderão extrair insights valiosos de seus dados, ajudando na tomada de decisões estratégicas.

## Relatórios que vamos criar

1. **Relatórios de Receita**
    
    * Qual foi o total de receitas no ano de 1997?

    ```sql
    CREATE VIEW total_revenues_1997_view AS
    SELECT 
        SUM(od.unit_price * od.quantity * (1-od.discount)) AS total_revenue_1997
    FROM order_details od
    INNER JOIN orders o on o.order_id = od.order_id
    WHERE EXTRACT(YEAR FROM o.order_date) = 1997;
    ```

    * Faça uma análise de crescimento mensal e o cálculo de YTD

    ```sql
    CREATE VIEW view_receitas_acumuladas AS
    WITH receita_mensal_ano AS (
    SELECT 
        EXTRACT(YEAR FROM o.order_date) AS ano, 
        EXTRACT(MONTH FROM o.order_date) AS mes,
        SUM(od.unit_price * od.quantity * (1-od.discount)) AS receita_mensal
    FROM order_details od
        INNER JOIN orders o on o.order_id = od.order_id
    GROUP BY 
        EXTRACT(YEAR FROM o.order_date),
        EXTRACT(MONTH FROM o.order_date)
    ORDER BY 
        EXTRACT(YEAR FROM o.order_date),
        EXTRACT(MONTH FROM o.order_date)
    )

    SELECT 
        ano,
        mes, 
        receita_mensal, 
        (receita_mensal - LAG(receita_mensal) OVER (PARTITION BY ano ORDER BY mes)) as diferenca_mes,
        SUM(receita_mensal) OVER (PARTITION BY ano ORDER BY mes) as receita_ytd,
        ((receita_mensal - LAG(receita_mensal) OVER (PARTITION BY ano ORDER BY mes)) / LAG(receita_mensal) OVER (PARTITION BY ano ORDER BY mes)) * 100 as percent_dif_mes
    FROM receita_mensal_ano
    ORDER BY 
        ano, 
        mes;
    ```

2. **Segmentação de clientes**
    
    * Qual é o valor total que cada cliente já pagou até agora?

    ```sql
    CREATE VIEW view_total_revenues_per_customer AS
    SELECT 
        c.customer_id,
        company_name, 
        SUM(od.unit_price * od.quantity * (1-od.discount)) AS total
    FROM customers AS c 
    INNER JOIN orders AS o 
        ON o.customer_id = c.customer_id
    INNER JOIN order_details AS od 
        ON od.order_id = o.order_id
    GROUP BY c.customer_id
    ORDER BY total DESC;
    ```

    * Separe os clientes em 5 grupos de acordo com o valor pago por cliente

    ```sql
    CREATE VIEW view_total_revenues_per_customer_group AS
    SELECT 
        c.customer_id,
        company_name, 
        SUM(od.unit_price * od.quantity * (1-od.discount)) AS total, 
        NTILE(5) OVER (ORDER BY SUM(od.unit_price * od.quantity * (1-od.discount)) DESC) AS n_grupo
    FROM customers AS c 
    INNER JOIN orders AS o 
        ON o.customer_id = c.customer_id
    INNER JOIN order_details AS od 
        ON od.order_id = o.order_id
    GROUP BY c.customer_id
    ORDER BY total DESC
    ```


    * Agora somente os clientes que estão nos grupos 3, 4 e 5 para que seja feita uma análise de Marketing especial com eles

    ```sql
    CREATE VIEW clients_to_marketing AS
    WITH total_per_client_group AS (
    SELECT 
        c.customer_id,
        company_name, 
        SUM(od.unit_price * od.quantity * (1-od.discount)) AS total, 
        NTILE(5) OVER (ORDER BY SUM(od.unit_price * od.quantity * (1-od.discount)) DESC) AS n_grupo
    FROM customers AS c 
    INNER JOIN orders AS o 
        ON o.customer_id = c.customer_id
    INNER JOIN order_details AS od 
        ON od.order_id = o.order_id
    GROUP BY c.customer_id
    ORDER BY total DESC
        )

    SELECT * 
    FROM total_per_client_group
    WHERE n_grupo >= 3;
    ```

3. **Top 10 Produtos Mais Vendidos**
    
    * Identificar os 10 produtos mais vendidos.

    ```sql
    CREATE VIEW top_10_products AS
    SELECT 
        p.product_name, 
        SUM(od.unit_price * od.quantity * (1.0 - od.discount)) AS sales
    FROM products AS p
    INNER JOIN order_details AS od ON od.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY sales DESC
    LIMIT 10;
    ```

4. **Clientes do Reino Unido que Pagaram Mais de 1000 Dólares**
    
    * Quais clientes do Reino Unido pagaram mais de 1000 dólares?

    ```sql
    CREATE VIEW uk_clients_who_pay_more_then_1000 AS
    SELECT 
        c.contact_name, 
        SUM(od.unit_price * od.quantity * (1.0 - od.discount) * 100) / 100 AS payments
    FROM customers AS c
    INNER JOIN orders AS o ON o.customer_id = c.customer_id
    INNER JOIN order_details AS od ON od.order_id = o.order_id
    WHERE LOWER(c.country) = 'uk'
    GROUP BY c.contact_name
    HAVING SUM(od.unit_price * od.quantity * (1.0 - od.discount)) > 1000
    ORDER BY payments DESC;
    ```

## Contexto

O banco de dados `Northwind` contém os dados de vendas de uma empresa  chamada `Northwind Traders`, que importa e exporta alimentos especiais de todo o mundo. 

O banco de dados Northwind é ERP com dados de clientes, pedidos, inventário, compras, fornecedores, remessas, funcionários e contabilidade.

O conjunto de dados Northwind inclui dados de amostra para o seguinte:

* **Fornecedores:** Fornecedores e vendedores da Northwind
* **Clientes:** Clientes que compram produtos da Northwind
* **Funcionários:** Detalhes dos funcionários da Northwind Traders
* **Produtos:** Informações do produto
* **Transportadoras:** Os detalhes dos transportadores que enviam os produtos dos comerciantes para os clientes finais
* **Pedidos e Detalhes do Pedido:** Transações de pedidos de vendas ocorrendo entre os clientes e a empresa

O banco de dados `Northwind` inclui 14 tabelas e os relacionamentos entre as tabelas são mostrados no seguinte diagrama de relacionamento de entidades.

![northwind](https://github.com/lvgalvao/Northwind-SQL-Analytics/blob/main/pics/northwind-er-diagram.png?raw=true)

## Objetivo

O objetivo desse 

## Configuração Inicial

### Manualmente

Utilize o arquivo SQL fornecido, `nortwhind.sql`, para popular o seu banco de dados.

### Com Docker e Docker Compose

**Pré-requisito**: Instale o Docker e Docker Compose

* [Começar com Docker](https://www.docker.com/get-started)
* [Instalar Docker Compose](https://docs.docker.com/compose/install/)

### Passos para configuração com Docker:

1. **Iniciar o Docker Compose** Execute o comando abaixo para subir os serviços:
    
    ```
    docker-compose up
    ```
    
    Aguarde as mensagens de configuração, como:
    
    ```csharp
    Creating network "northwind_psql_db" with driver "bridge"
    Creating volume "northwind_psql_db" with default driver
    Creating volume "northwind_psql_pgadmin" with default driver
    Creating pgadmin ... done
    Creating db      ... done
    ```
       
2. **Conectar o PgAdmin** Acesse o PgAdmin pelo URL: [http://localhost:5050](http://localhost:5050), com a senha `postgres`. 

Configure um novo servidor no PgAdmin:
    
    * **Aba General**:
        * Nome: db
    * **Aba Connection**:
        * Nome do host: db
        * Nome de usuário: postgres
        * Senha: postgres Em seguida, selecione o banco de dados "northwind".

3. **Parar o Docker Compose** Pare o servidor iniciado pelo comando `docker-compose up` usando Ctrl-C e remova os contêineres com:
    
    ```
    docker-compose down
    ```
    
4. **Arquivos e Persistência** Suas modificações nos bancos de dados Postgres serão persistidas no volume Docker `postgresql_data` e podem ser recuperadas reiniciando o Docker Compose com `docker-compose up`. Para deletar os dados do banco, execute:
    
    ```
    docker-compose down -v
    ```
