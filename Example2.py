#!/usr/bin/env python
# readSGA.py

from ctypes import *

"""
IPC Resources for ORACLE_SID "test1" :
Shared Memory:
ID		KEY
18481156	0x00000000
18513925	0x00000000
18546694	0xaa5ccb7c

"""

shmid     = 18513925
sgaBase   = 0x60000000
ksuseAddr = 0x9A034020
rowCount  = 247
rowSize   = 0x30E0

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

print "'select from v$session' made by reading SGA directly:"
print "       SID    SERIAL# USERNAME                       STATUS"
print "---------- ---------- ------------------------------ --------"

# MyDefenitions Oracle 11g
memaddr = ksuseAddr
for i in range(1,rowCount):
  ksspaflg = readSGA.read4(memaddr+0)
  ksuseflg = readSGA.read4(memaddr+5936)
  sid      = i
  serial   = readSGA.read2(memaddr+5922)
  username = readSGA.reads(memaddr+163,30)
  statusid = readSGA.read1(memaddr+5976)
  status   = readstatus(statusid,ksuseflg)
  #if (ksspaflg & 1 != 0) and (ksuseflg & 1 != 0):
  print "%10d %10d %-30s %-8s" % (sid,serial,username,status)


# OriginalDefenitions Oracle 10g
"""
memaddr = ksuseAddr
for i in range(1,rowCount):
  ksspaflg = readSGA.read1(memaddr+1)
  ksuseflg = readSGA.read4(memaddr+1388)
  sid      = i
  serial   = readSGA.read2(memaddr+1382)
  username = readSGA.reads(memaddr+67,30) # (offset,size)
  statusid = readSGA.read1(memaddr+1420)
  status   = readstatus(statusid,ksuseflg)
  if (ksspaflg & 1 != 0) and (ksuseflg & 1 != 0):
    print "%10d %10d %-30s %-8s" % (sid,serial,username,status)
"""

memaddr += rowSize
