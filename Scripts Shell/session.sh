#!/bin/bash

while :
do
sqlplus oracle/beer4Admin@TEST1 << EOF
set heading off
set pagesize 0
set linesize 1000
SET FEEDBACK OFF
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
from v\$session s, v\$sql t, dual d where t.sql_id=s.sql_id;
EOF
done
