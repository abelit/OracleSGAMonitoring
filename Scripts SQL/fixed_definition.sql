SELECT sid, serial#, username, status, process, machine, data FROM  v$session;
desc v$session;
select * from v$session
desc v$sql

select to_char(sysdate,'DD-MM-YYYY') from dual


select to_char(sysdate,'DD:MM:YYYY:HH24:MI:SS'), 
s.sid,
s.serial#,
s.username,
s.machine,
s.module,
s.event,
s.p1text,
s.p2text,
s.p3text,
t.sql_text
from v$session s, v$sql t, dual d where t.sql_id=s.sql_id;