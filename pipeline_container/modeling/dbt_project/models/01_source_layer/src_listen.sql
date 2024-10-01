{{ config(materialized='view') }}

with cte_src_listen as (

    select * from moovitamix.listen_history
    WHERE created_at = CURRENT_DATE
)

select *
from cte_src_listen