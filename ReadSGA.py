#!/usr/bin/env python
# readSGA.py

# AUTHOR: Stanislav Gabenov
# Date: 06-06-2016
# Version: 1.00

from ctypes import *
import cx_Oracle
import os
import time
import struct
from subprocess import Popen, PIPE
from datetime import datetime
from ctypes import string_at # test
from sys import getsizeof    # test
from binascii import hexlify # test
from struct import *

## ORACLE CONNECTION ESTABLISHMENT
conn = cx_Oracle.Connection('/', mode = cx_Oracle.SYSDBA)
cur = conn.cursor()

## SQL REQUESTS
sqlKsuseAddr = "SELECT RAWTONHEX(min(addr)) FROM X$KSUSE"
sqlSgaBase = "SELECT RAWTOHEX(addr) FROM sys.x$ksmmem WHERE rownum=1"
sqlRowCount = "SELECT count(addr) FROM sys.x$ksuse"
sqlRowSize = "SELECT ((to_dec(f.addr)-to_dec(e.addr))) row_size FROM (SELECT addr FROM x$ksuse WHERE rownum < 2)f, (SELECT min(addr) addr FROM x$ksuse WHERE rownum < 3)e"
sqlKsspaflg = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='KSSPAFLG' order by offset"
sqlKsuseflg = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='KSUSEFLG' order by offset"
sqlSerial = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='KSUSESER' order by offset"
sqlUsername = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='KSUSEUNM' order by offset"
sqlMachinename = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='KSUSEMNM' order by offset"
sqlStatusid = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='KSUSEIDL' order by offset"
sqlAllAddr = "SELECT RAWTONHEX(addr) FROM x$ksuse"
sqlIndex = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='INDX' order by offset"
sqlSequence = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='KSUSESEQ' order by offset"
sqlEvent = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='KSUSEOPC' order by offset"
sqlP1 = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='KSUSEP1' order by offset"
sqlP2 = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='KSUSEP2' order by offset"
sqlP3 = "select c.kqfconam field_name, c.kqfcooff offset, c.kqfcosiz sz from x$kqfco c,x$kqfta t where t.indx = c.kqfcotab and t.kqftanam='X$KSUSE' and c.kqfconam='KSUSEP3' order by offset"

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

cur.execute(sqlKsspaflg)
ksspaflgSQL = cur.fetchone()
ksspaflgOffset = int(ksspaflgSQL[1])
ksspaflgSize = int(ksspaflgSQL[2])
print "ksspaflg Offset:", ksspaflgOffset

cur.execute(sqlKsuseflg)
ksuseflgSQL = cur.fetchone()
ksuseflgOffset = int(ksuseflgSQL[1])
ksuseflgSize = int(ksuseflgSQL[2])
print "ksuseflg Offset:", ksuseflgOffset

cur.execute(sqlSerial)
serialSQL = cur.fetchone()
serialOffset = int(serialSQL[1])
serialSize = int(serialSQL[2])
print "serial Offset:", serialOffset

cur.execute(sqlUsername)
usernameSQL = cur.fetchone()
usernameOffset = int(usernameSQL[1])
usernameSize = int(usernameSQL[2])
print "username Offset, Size:", usernameOffset, ",", usernameSize

cur.execute(sqlMachinename)
machinenameSQL = cur.fetchone()
machinenameOffset = int(machinenameSQL[1])
machinenameSize = int(machinenameSQL[2])
print "machinename Offset, Size:", machinenameOffset, ",", machinenameSize

cur.execute(sqlStatusid)
statusidSQL = cur.fetchone()
statusidOffset = int(statusidSQL[1])
statusidSize = int(statusidSQL[2])
print "statusid Offset:", statusidOffset

cur.execute(sqlIndex)
indexSQL = cur.fetchone()
indexOffset = int(indexSQL[1])
indexSize = int(indexSQL[2])
print "index Offset:", indexOffset

cur.execute(sqlSequence)
sequenceSQL = cur.fetchone()
sequenceOffset = int(sequenceSQL[1])
sequenceSize = int(sequenceSQL[2])
print "sequence Offset:", sequenceOffset

cur.execute(sqlEvent)
eventSQL = cur.fetchone()
eventOffset = int(eventSQL[1])
eventSize = int(eventSQL[2])
print "event Offset:", eventOffset

cur.execute(sqlP1)
p1SQL = cur.fetchone()
p1Offset = int(p1SQL[1])
p1Size = int(p1SQL[2])
print "p1 Offset:", p1Offset

cur.execute(sqlP2)
p2SQL = cur.fetchone()
p2Offset = int(p2SQL[1])
p2Size = int(p2SQL[2])
print "p2 Offset:", p2Offset

cur.execute(sqlP3)
p3SQL = cur.fetchone()
p3Offset = int(p3SQL[1])
p3Size = int(p3SQL[2])
print "p3 Offset:", p3Offset

cur.execute(sqlAllAddr)
allAddrSQL = cur.fetchall()
stack = []
for row in allAddrSQL:
  stack.append(int(row[0],16))

cur.execute("select INDX, KSLEDNAM from X$KSLED")
ksledTableSQL = cur.fetchall()
tableKsled = dict([i for i in ksledTableSQL])

conn.close()

## OBTAINING SHMID ID FROM SHARED MEMORY
osRequest = "pmap `ps ax | grep [o]ra_pmon_${ORACLE_SID} | awk '{print $1}'` | grep shm | awk '{print $5,$1,$2}' | awk -F '=' '{print $2}'"

proc = Popen(
    osRequest,
    shell=True,
    stdout=PIPE, stderr=PIPE
)
proc.wait()
res = proc.communicate()  #tuple('stdout', 'stderr')
if proc.returncode:
    print res[1]
print 'Pmap Result:\nshmid segment_start_addr size\n-------------------------------\n', res[0]
i = res[0]
b = i.split()
print "All Segments attached to Ora_mon as a tumple:", b

## Cycle to find in which segment containing our SHMID
i=0
while i < len(b) :
    if int(b[i+1],16)<int(ksuseAddrHEX,16)<int(b[i+1],16)+int(b[i+2][0:len(b[i+2])-1],10)*1024 :
	  break
#    print "--------------------------------------"
    i+=3

print "SHMID: ", b[i], " BASE ADDR: ",b[i+1]
shmid     = int(b[i],16) # 851973
sgaBase   = int(b[i+1],16) # 0x60c00000 !SHOULD BE SECOND SEGMENT!
print "SHMID in DEC:", int(b[i],16)

## GETTING VARIABLES
# SQL SELECT
ksuseAddr = int(ksuseAddrHEX,16) # 0x9A034020 !CHANGES EACH TIME!
rowCount  = int(rowCountDEC) # 247
rowSize   = int(rowSizeDEC) # 12512

## READ SGA
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


## Open a file to write data
fo = open("foo.txt", "wb")

## CYCLE_BEGIN
#for i in xrange(3):
t_end = time.time() + 15
while time.time() < t_end:
     # MyDefenitions Oracle 11g
     memaddr = ksuseAddr
     print "memaddr:", hex(memaddr)
     print stack

     # get time execution
     execTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
     print execTime, "\n"

     #print "Writing to file: ", fo.name
     fo.write( "'select from v$session' made by reading SGA directly at time: %s\n" % (execTime));
     fo.write( "       SID    SERIAL# USERNAME   MACHINENAME          STATUS                                                             \n");
     fo.write( "---------- ---------- ---------- -------------------- --------------------------------------------------------------------\n");

     print( "\n'select from v$session' made by reading SGA directly: %s\n" % (execTime));
     print( "       SID    SERIAL# USERNAME   MACHINENAME          STATUS        Index   Sequence Event     P1        Event_defenition                \n");
     print( "---------- ---------- ---------- -------------------- --------------------------------------------------------------------\n");

     sid = 0
     for i in stack:
       ksspaflg = readSGA.read4(i + ksspaflgOffset)
       ksuseflg = readSGA.read4(i + ksuseflgOffset)
       sid += 1
       serial = readSGA.read2(i + serialOffset)
       username = readSGA.reads(i + usernameOffset, usernameSize)
       machinename = readSGA.reads(i + machinenameOffset, machinenameSize)
       statusid = readSGA.read1(i + statusidOffset)
       status = readstatus(statusid, ksuseflg)
       index    = readSGA.read4(i+indexOffset)
       sequence = readSGA.read2(i+sequenceOffset)
       event    = readSGA.read2(i+eventOffset)
       if event in tableKsled:
         eventDef = tableKsled[event]
       else:
         eventDef = "Can't find definition in X$KSLED table for session: %s" % (i)
       p1 = readSGA.reads(i+p1Offset,p1Size)
       z1 = hexlify(string_at(id(p1),p1Size))
       #print (calcsize(p1))
       if len(p1) == 0:
           continue
       #print type(i),len(p1),'REPRESENTATION_P1:', repr(p1)
       print
       #t1 = struct.unpack('P',p1)
       p2 = readSGA.reads(i+p2Offset,p2Size)
       p3 = readSGA.reads(i+p3Offset,p3Size)
       if (ksspaflg & 1 != 0) and (ksuseflg & 1 != 0) and (serial >= 1):
         #print "%10d %10d %-10s %-20s %-8s %10d %10d %-10s '%8s' %-10s" % (sid, serial, username, machinename, status, index, sequence, event, p1, eventDef)
         print "%10d %10d %-10s %-20s %-8s %10d %10d %-10s %-10s" % (sid, serial, username, machinename, status, index, sequence, event, eventDef)
         fo.write("%10d %10d %-10s %-64s %-8s %10d %10d %-10s %-10s\n" % (sid, serial, username, machinename, status, index, sequence, event, eventDef));
     #time.sleep(5)

## Close opened file
fo.close()
