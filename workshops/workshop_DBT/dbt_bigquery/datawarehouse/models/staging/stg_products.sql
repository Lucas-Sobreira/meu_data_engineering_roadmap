with

source as (

    select * from {{ source('ecom', 'raw_products') }}

),

renamed as (

    select

        ----------  ids
        sku as product_id,

        ---------- text
        name as product_name,
        type as product_type,
        description as product_description,

        ---------- numerics
        -- Substituição manual do cents_to_dollars
        round(cast((price / 100) as numeric), 2) as product_price,

        ---------- booleans
        coalesce(type = 'jaffle', false) as is_food_item,
        coalesce(type = 'beverage', false) as is_drink_item

    from source

)

select * from renamed
