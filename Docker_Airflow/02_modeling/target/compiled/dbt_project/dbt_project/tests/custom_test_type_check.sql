WITH type_check AS (
    SELECT
        listen_timestamp
    FROM "moovai_data"."main"."src_listen"
    WHERE CAST(listen_timestamp AS DATE) IS NULL
)

SELECT COUNT(*)
FROM type_check