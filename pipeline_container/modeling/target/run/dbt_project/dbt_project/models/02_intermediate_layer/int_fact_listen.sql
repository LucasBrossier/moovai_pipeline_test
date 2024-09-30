
  
    
    

    create  table
      "moovitamix"."main"."int_fact_listen"
  
    as (
      

with cte_int_listen as (

    select * from "moovitamix"."main"."src_listen"

)

--INSERT INTO int_listen
select *
from cte_int_listen
    );
  
  
  