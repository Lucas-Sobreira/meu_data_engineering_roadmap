with orders as (
    select * from {{ source('northwind', 'orders')}}
)

select 
    *
from orders
    