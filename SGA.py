import cx_Oracle
import os
from subprocess import Popen, PIPE
from ctypes import *

### start of something
os.environ["PATH"] = "/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:/opt/oracle/.local/bin:/opt/oracle/bin:/opt/oracle/app/oracle/product/11.2.0/dbhome_1/bin"
os.environ["ORACLE_HOME"] = "/opt/oracle/app/oracle/product/11.2.0/dbhome_1"
os.environ["TNS_ADMIN"] = "/opt/oracle/app/oracle/product/11.2.0/dbhome_1/network/admin"
os.environ["ORACLE_SID"] = "test1"
os.chdir('/opt/oracle/Desktop/python')

# execute sys

proc = Popen(
    "sysresv | sed -n '/Shared Memory:/,/Semaphores:/p'| sed '1,2d;$d'",
    shell=True,
    stdout=PIPE, stderr=PIPE
)
proc.wait()
res = proc.communicate()  #tuple('stdout', 'stderr')
if proc.returncode:
    print res[1]
print 'result:\n', res[0]
i = res[0]
b = dict( [ (i.split()) for i in i.split('\n') if i != ''])
print b

# get SQL from oracle
conn_str = u'oracle/beer4Admin@TEST1'
conn = cx_Oracle.connect(conn_str, mode=cx_Oracle.SYSDBA)
c = conn.cursor()
# get size of Fixed Area
c.execute(u'select value from v$sga where name like \'Fixed%\'')
for row in c:
    shmem_size = row[0]

# select base address of SGA start
c.execute(u'select \'0x\'||to_number(addr) from sys.x$ksmmem where rownum=1')
for row in c:
    shmem_ksmem = int(row[0], 16)

# select address of table
c.execute(u'select \'0x\'||addr from sys.x$ksuse where rownum=1')
for row in c:
    shmem_ksuse = int(row[0], 16)

conn.close()
print 'shmem_size: ',shmem_size
print 'x$ksmmem: ', shmem_ksmem
print 'x$ksuse: ', shmem_ksuse

# get result from sys. Using ctypes
