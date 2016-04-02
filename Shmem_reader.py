import sysv_ipc

# Create shared memory object
memory = sysv_ipc.SharedMemory(0x0001e240)

# Read value from shared memory
memory_value = memory.read()

# Find the 'end' of the string and strip
# Can be esed only Key definition. No shmemid.
i = memory_value.find('\0')
if i != -1:
    memory_value = memory_value[:i]

print memory_value