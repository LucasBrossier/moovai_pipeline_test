{{ config(materialized='view') }}

with cte_src_tracks as (


    select * from moovai_data.tracks
    WHERE created_at = CURRENT_DATE

)

select *
from cte_src_tracks