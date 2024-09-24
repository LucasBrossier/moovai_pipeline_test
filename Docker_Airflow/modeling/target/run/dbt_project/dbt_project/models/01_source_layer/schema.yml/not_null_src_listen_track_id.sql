select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select track_id
from "moovai_data"."main"."src_listen"
where track_id is null



      
    ) dbt_internal_test