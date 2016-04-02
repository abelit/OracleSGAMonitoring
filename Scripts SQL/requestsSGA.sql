-- select base address from sga
select addr from sys.x$ksmmem where rownum=1;

--  select address of table
select addr from sys.x$ksuse where rownum=1;

-- select size of fixed area
select value from v$sga where name like 'Fixed%'