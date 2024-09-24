

with mart_listen_and_tracks as (

SELECT *
FROM  "moovitamix"."main"."int_fact_listen" AS l
LEFT JOIN "moovitamix"."main"."int_dim_tracks" as r
ON l.track_id = r.id

)

select * from mart_listen_and_tracks