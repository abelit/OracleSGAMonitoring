# OracleSGAMonitoring
# Example4 - Последняя версия

To Do List:
  1. Ignore Event Class (Idle)
  2. Read SGA in cycle
  3. Print time of when execution
  4. Parameterize sleep time in cycle
  5. PMAP for different OS-types
  6. P1, P2, P3 - show. Данные по событиям
  7. Разбить программу на несколько модулей. 1 - преднастройка, 2 - чтение в цикле. И переходы по событиям из блока в блок.
  8. Исполняемый код SQL. v$session имеет поле SQL_ADDRES. Длина строки может быть любой длины и заканчивается Zero termination \0
  
wait event enqueue - блокировка и тип блокировки (P2?). Latch free wait event (защелки внутренние) - вывести тип, что за защелка. Latch name



After:
  1. Error handler. SIGSEGV?
  2. Обработчик sigterm, sigkill...
  3. 


Additional:
  1. Disassamble sysresv (sysresv.o)
