{{ config(materialized='table') }}

with employees as (
    select * from {{ ref('stg_employees') }}
), 
employee_territories as (
    select * from {{ ref('stg_employee_territories') }}
), 
territories as (
    select * from {{ ref('stg_territories') }}
),  
region as (
    select * from {{ ref('stg_region') }}
), 

joined as (
    select 
        se.last_name as last_name, 
        se.first_name as first_name, 
        se.title as title, 
        se.title_of_courtesy as title_of_courtesy, 
        se.birth_date as birth_date, 
        se.hire_age as hire_age, 
        se.city as city, 
        se.country as country, 
        st.territory_description as territory_description, 
        rg.region_description as region_description
    from employees as se
    left join employee_territories as et on se.employee_id = et.employee_id
    left join staging.stg_territories st on et.territory_id = st.territory_id 
    left join staging.stg_region rg on st.region_id = rg.region_id
),

relatorio as (
    SELECT 
        *, 
        CASE 
            WHEN title_of_courtesy IN ('dr.', 'mr.') THEN 'Male'
            WHEN title_of_courtesy IN ('ms.', 'mrs.') THEN 'Female'
            ELSE 'Unknown'
        END AS gender
    FROM joined
)

select * from relatorio