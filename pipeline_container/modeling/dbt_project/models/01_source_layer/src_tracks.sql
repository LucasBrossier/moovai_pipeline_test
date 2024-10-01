{{ config(materialized='view') }}

with cte_src_tracks as (

    select * from moovitamix.tracks
    WHERE created_at = CURRENT_DATE
)

select *
from cte_src_tracks