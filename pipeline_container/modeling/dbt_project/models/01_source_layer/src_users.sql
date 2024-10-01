{{ config(materialized='view') }}

with cte_src_users as (

    select * from moovitamix.users
    WHERE created_at = CURRENT_DATE
)

select *
from cte_src_users