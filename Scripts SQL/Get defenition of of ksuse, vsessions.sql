select
              *
          from
              V_$FIXED_VIEW_DEFINITION
         where
              view_name='GV$SQL'
    
    
select * from x$ksuse
select * from v$session

select * from x$kglcursor_child

select value from v$sga where name like 'Fixed%';