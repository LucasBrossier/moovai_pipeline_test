
  
  create view "moovai_data"."main"."src_listen__dbt_tmp" as (
    

with cte_src_listen as (


    select * from moovai_data.listen_history
    WHERE listen_timestamp = CURRENT_DATE
)

select *
from cte_src_listen
  );
