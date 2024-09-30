
  
    
    

    create  table
      "moovitamix"."main"."int_dim_tracks"
  
    as (
      

with cte_src_tracks as (

    select * from "moovitamix"."main"."src_tracks"

)

--INSERT INTO int_tracks
select *
from cte_src_tracks
    );
  
  
  