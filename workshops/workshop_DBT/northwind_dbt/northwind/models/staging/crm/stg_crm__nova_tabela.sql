with renamed as (
    select 
        category_id as id,
        category_name as name, 
        description,
        picture, 
        updated_at
    from 
        {{ref('raw_crm__nova_tabela')}}
)

select * from renamed