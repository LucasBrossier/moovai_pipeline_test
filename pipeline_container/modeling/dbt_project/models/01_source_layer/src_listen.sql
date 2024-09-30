{{ config(materialized='view') }}

with cte_src_listen as (


    select * from moovitamix.listen_history
    WHERE listen_timestamp = CURRENT_DATE
)

select *
from cte_src_listen