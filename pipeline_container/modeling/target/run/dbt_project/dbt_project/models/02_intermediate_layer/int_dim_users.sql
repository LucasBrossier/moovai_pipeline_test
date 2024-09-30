
  
    
    

    create  table
      "moovitamix"."main"."int_dim_users"
  
    as (
      

with cte_src_users as (

    select * from "moovitamix"."main"."src_users"

)

--INSERT INTO int_users
select *
from cte_src_users
    );
  
  
  