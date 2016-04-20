#!/usr/bin/env python
# readSGA.py

from ctypes import *
import cx_Oracle
import os
from subprocess import Popen, PIPE


## ORACLE CONNECTION ESTABLISHMENT
"""
# USE THIS IF CONNECTION IS MADE NOT FROM SYSDBA ON LOCALHOST!
# conn_str = u'oracle/beer4Admin@TEST1'
# conn = cx_Oracle.connect(conn_str)
# host = 'localhost'
# port = 1521
# sid = 'test1'
# dsn = cx_Oracle.makedsn(host, port, sid)
"""
conn = cx_Oracle.Connection('/', mode = cx_Oracle.SYSDBA)
cur = conn.cursor()

#c.execute(u'SELECT view_name FROM ALL_VIEWS')
## SQL REQUESTS
sqlKsuseAddr = "SELECT RAWTONHEX(min(addr)) FROM X$KSUSE"
sqlSgaBase = "SELECT RAWTOHEX(addr) FROM sys.x$ksmmem WHERE rownum=1"
sqlRowCount = "SELECT count(addr) FROM sys.x$ksuse"
sqlRowSize = "SELECT ((to_dec(f.addr)-to_dec(e.addr))) row_size FROM (SELECT addr FROM x$ksuse WHERE rownum < 2)f, (SELECT min(addr) addr FROM x$ksuse WHERE rownum < 3)e"

## OBTAINING DATA FROM DATABASE
cur.execute(u'SELECT RAWTONHEX(min(addr)) FROM X$KSUSE')
for row in cur:
  ksuseAddrSQL = row[0]
  ksuseAddrHEX = hex(int(ksuseAddrSQL, 16))
  print "ksuseAddrHEX:", ksuseAddrHEX

cur.execute(sqlSgaBase)
sgaBaseSQL = cur.fetchone()
sgaBaseHEX = hex(int(sgaBaseSQL[0],16))
print "sgaBaseHEX:", sgaBaseHEX

cur.execute(sqlRowCount)
rowCountSQL = cur.fetchone()
rowCountDEC = int(rowCountSQL[0])
print "rowCountDEC:", rowCountDEC

cur.execute(sqlRowSize)
rowSizeSQL = cur.fetchone()
rowSizeDEC = int(rowSizeSQL[0])
print "rowSizeDEC:", rowSizeDEC

conn.close()

## OBTAINING SHMID ID FROM SHARED MEMORY
osRequest = "pmap `ps ax | grep ora_pmon_${ORACLE_SID} | awk '{print $1}'` | grep shm | awk '{print $5,$1,$2}'"

proc = Popen(
    osRequest,
    shell=True,
    stdout=PIPE, stderr=PIPE
)
proc.wait()
res = proc.communicate()  #tuple('stdout', 'stderr')
if proc.returncode:
    print res[1]
print 'Pmap Result:\n', res[0]
i = res[0]
#b = dict( [ (i.split()) for i in i.split('\n') if i != ''])
#print "TESTING", b



## GETTING VARIABLES
# PMAP
shmid     = shmidDEC #851973
sgaBase   = sgaBaseHEX #0x60c00000 !SHOULD BE SECOND SEGMENT!

# SQL SELECT
ksuseAddr = ksuseAddrHEX #0x9A034020 !changes each time
rowCount  = rowCountDEC #247
rowSize   = rowSizeDEC #12512

## SQL OFFSET FOR IDENTIFICATORS
#  ksspaflg = readSGA.read4(memaddr+0)
#  ksuseflg = readSGA.read4(memaddr + 5936)
#  serial = readSGA.read2(memaddr + 5922)
#  username = readSGA.reads(memaddr + 6200, 30)
#  machinename = readSGA.reads(memaddr + 6240, 64)
#  statusid = readSGA.read1(memaddr + 5976)


class SGAException(Exception):
  pass

class ReadSGA:
  libc = cdll.LoadLibrary("/lib64/libc.so.6")
  def __init__(self,shmid,sgaBase):
    self.mem = self.libc.shmat(shmid,sgaBase,010000) # 010000 == SHM_RDONLY
    if self.mem == -1:
      raise SGAException, "can't attach to SGA with id %s" % shmid
  def read1(self,addr):
    val = (c_byte * 1).from_address(addr)
    return val[0]
  def read2(self,addr):
    val = (c_byte * 2).from_address(addr)
    return val[0]+val[1]*256
  def read4(self,addr):
    val = (c_long * 1).from_address(addr)
    return val[0]
  def reads(self,addr,size):
    val = (c_char * size).from_address(addr)
    return val.value
  def __del__(self):
    self.libc.shmdt(self.mem)

def readstatus(statusid,ksuseflg):
  if (statusid & 11 == 1):
    status = 'ACTIVE'
  elif (statusid & 11 == 0):
    if (ksuseflg & 4096 == 0):
      status = 'INACTIVE'
    else:
      status = 'CACHED'
  elif (statusid & 11 == 2):
    status = 'SNIPED'
  elif (statusid & 11 == 3):
    status = 'SNIPED'
  else:
    status = 'KILLED'
  return status

readSGA = ReadSGA(shmid,sgaBase)

# Open a file
fo = open("foo.txt", "wb")
print "Writing to file: ", fo.name

fo.write( "'select from v$session' made by reading SGA directly:\n");
fo.write( "       SID    SERIAL# USERNAME   MACHINENAME          STATUS                                                             \n");
fo.write( "---------- ---------- ---------- -------------------- --------------------------------------------------------------------\n");

# MyDefenitions Oracle 11g
memaddr = ksuseAddr
for i in range(1,rowCount):
  ksspaflg = readSGA.read4(memaddr+0)
  ksuseflg = readSGA.read4(memaddr+5936)
  sid      = i
  serial   = readSGA.read2(memaddr+5922)
  username = readSGA.reads(memaddr+6200,30)
  machinename = readSGA.reads(memaddr+6240,64)
  statusid = readSGA.read1(memaddr+5976)
  status   = readstatus(statusid,ksuseflg)
  if (ksspaflg & 1 != 0) and (ksuseflg & 1 != 0) and (serial >= 0):
    fo.write( "%10d %10d %-10s %-20s %-8s\n" % (sid,serial,username,machinename,status));
  memaddr += rowSize


# Close opend file
fo.close()





"""
#Use SQL as PMAP in python:

import os
from subprocess import Popen, PIPE

sqlplus = Popen(["sqlplus", "-S", "/", "as", "sysdba"], stdout=PIPE, stdin=PIPE)
sqlplus.stdin.write("select sysdate from dual;"+os.linesep)
sqlplus.stdin.write("select count(*) from all_objects;"+os.linesep)
out, err = sqlplus.communicate()
print out

"""