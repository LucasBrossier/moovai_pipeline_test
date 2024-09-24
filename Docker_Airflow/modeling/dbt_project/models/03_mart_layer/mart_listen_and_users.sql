{{ config(materialized='table') }}

with mart_listen_and_tracks as (

SELECT *
FROM  {{ ref('int_fact_listen') }} AS l
LEFT JOIN {{ ref('int_dim_users') }} as r
ON l.user_id = r.id

)

select * from mart_listen_and_tracks