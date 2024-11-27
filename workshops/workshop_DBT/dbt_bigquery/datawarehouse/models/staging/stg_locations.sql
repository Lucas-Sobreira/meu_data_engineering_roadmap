with

source as (

    select * from {{ source('ecom', 'raw_stores') }}

),

renamed as (

    select

        ----------  ids
        id as location_id,

        ---------- text
        name as location_name,

        ---------- numerics
        tax_rate,

        ---------- timestamps
        -- Substituição manual do dbt.date_trunc
        DATE_TRUNC(opened_at, day) as opened_date

    from source

)

select * from renamed
