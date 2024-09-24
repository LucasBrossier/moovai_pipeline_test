{{ config(materialized='incremental') }}

with cte_int_listen as (

    select * from {{ ref('src_listen') }}

)

--INSERT INTO int_listen
select *
from cte_int_listen