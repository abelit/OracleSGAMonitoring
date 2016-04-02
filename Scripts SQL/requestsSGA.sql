


-- select base address from sga
select addr from sys.x$ksmmem where rownum=1;

--  select address of table
select min(addr) from sys.x$ksuse;

-- select size of fixed area
select value from v$sga where name like 'Fixed%'

-- select 2 addresses of sessions
select min(addr) from sys.x$ksuse where rownum<3;

-- select size of 1 row on PLSQL (homework)
select

-- get count of sessions in the Oracle output
select addr from sys.x$ksuse;

-- get parameters of sessions in different way))
select name,value from v$parameter where name = 'sessions';

-- find offset of $ksuse it table
select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' order by offset;


