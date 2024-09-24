
    
    

select
    track_id as unique_field,
    count(*) as n_records

from "moovai_data"."main"."src_listen"
where track_id is not null
group by track_id
having count(*) > 1


